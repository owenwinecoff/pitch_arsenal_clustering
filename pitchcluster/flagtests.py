"""Cross-season tests of the platoon and costly-pitch flags.

Usage:  python -m pitchcluster.flagtests [train_year] [test_year]

Platoon: does a pitcher's LHB-vs-RHB run-value gap persist the next season?
  - slope of test gap on train gap (1 = fully persistent, 0 = pure noise)
  - for flagged pitchers (top quartile of |gap|), how often does the weak side stay the
    weak side (50% = coin flip)
Costly pitches: pitches flagged as heavy-use run-costers; are they still below the
  pitch-type average next year, versus unflagged heavy-use pitches?
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.model_selection import GroupKFold

from .command import command_scores, contact_luck
from .data import load_season
from .holdout import _wls
from .report import SHRINK_K, platoon, prep, usage_flags

OUT = Path(__file__).resolve().parent.parent / "outputs" / "report"


def _gaps(df: pd.DataFrame, min_n: int) -> pd.DataFrame:
    g = df.groupby(["pitcher", "stand"]).agg(n=("rv", "size"), rv=("rv", "sum")).reset_index()
    g["rv100"] = 100 * g["rv"] / g["n"]
    w = g.pivot(index="pitcher", columns="stand", values=["n", "rv100"]).dropna().astype(float)
    w.columns = [f"{a}_{b}" for a, b in w.columns]
    w = w[(w["n_L"] >= min_n) & (w["n_R"] >= min_n)]
    w["gap"] = w["rv100_L"] - w["rv100_R"]
    return w.reset_index()[["pitcher", "n_L", "n_R", "gap"]]


def platoon_test(tr: pd.DataFrame, te: pd.DataFrame, rng) -> list[dict]:
    a = _gaps(tr, 400)
    b = _gaps(te, 250).rename(columns={"gap": "gap_test", "n_L": "nL_t", "n_R": "nR_t"})
    m = a.merge(b, on="pitcher")
    print(f"platoon: {len(a)} train-qualified, {len(m)} also have test data")
    # slope via pitcher bootstrap
    def slope(d): return np.polyfit(d["gap"], d["gap_test"], 1)[0]
    bs = [slope(m.sample(len(m), replace=True, random_state=int(s))) for s in rng.integers(0, 1e6, 500)]
    rows = [dict(flag="platoon", n=len(m), metric="slope of test gap on train gap",
                 estimate=round(slope(m), 3), ci_lo=round(np.percentile(bs, 2.5), 3),
                 ci_hi=round(np.percentile(bs, 97.5), 3))]
    top = m[m["gap"].abs() >= m["gap"].abs().quantile(0.75)]
    hit = (np.sign(top["gap"]) == np.sign(top["gap_test"])).astype(float)
    bs = [hit.sample(len(hit), replace=True, random_state=int(s)).mean() for s in rng.integers(0, 1e6, 500)]
    rows.append(dict(flag="platoon", n=len(top), metric="share where weak side stays weak side (top-quartile gaps)",
                     estimate=round(hit.mean(), 3), ci_lo=round(np.percentile(bs, 2.5), 3),
                     ci_hi=round(np.percentile(bs, 97.5), 3)))
    return rows


def costly_test(tr: pd.DataFrame, te: pd.DataFrame, rng) -> list[dict]:
    flagged = usage_flags(tr, None)[["player_name", "pitch_type"]]
    # all heavy-use pitches in train (same usage/n cutoffs) as the comparison pool
    tot = tr.groupby("pitcher").size().rename("total")
    g = tr.groupby(["pitcher", "player_name", "pitch_type"]).size().rename("n").reset_index().join(tot, on="pitcher")
    g = g[(g["n"] >= 300) & (g["n"] / g["total"] >= 0.15)]
    g = g.merge(flagged.assign(flag=1), on=["player_name", "pitch_type"], how="left").fillna({"flag": 0})
    t = te.groupby(["pitcher", "pitch_type"]).agg(n_t=("rv", "size"), rv_t=("rv", "sum")).reset_index()
    lg = t.groupby("pitch_type")["rv_t"].sum() / t.groupby("pitch_type")["n_t"].sum()
    t["rel_rv100"] = 100 * (t["rv_t"] / t["n_t"] - t["pitch_type"].map(lg))
    m = g.merge(t, on=["pitcher", "pitch_type"])
    m = m[m["n_t"] >= 200]
    f, u = m[m["flag"] == 1], m[m["flag"] == 0]
    print(f"costly pitches: {len(f)} flagged / {len(u)} unflagged heavy-use with >=200 test pitches")
    bf = [f["rel_rv100"].sample(len(f), replace=True, random_state=int(s)).mean() for s in rng.integers(0, 1e6, 500)]
    bu = [u["rel_rv100"].sample(len(u), replace=True, random_state=int(s)).mean() for s in rng.integers(0, 1e6, 500)]
    diff = np.array(bf) - np.array(bu)
    return [dict(flag="costly pitch", n=len(f),
                 metric="test-year RV/100 vs pitch-type avg: flagged minus unflagged heavy-use",
                 estimate=round(f["rel_rv100"].mean() - u["rel_rv100"].mean(), 3),
                 ci_lo=round(np.percentile(diff, 2.5), 3), ci_hi=round(np.percentile(diff, 97.5), 3))]


def _ci(vals, rng, n=500):
    vals = np.asarray(vals, float)
    bs = [rng.choice(vals, len(vals)).mean() for _ in range(n)]
    return float(vals.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def _cv_gain(pair, y, w, base, plus, rng, dummies=None, n_boot=400):
    """Pitcher-grouped 5-fold CV: does adding `plus` columns beat `base` for predicting y?"""
    def X(cols):
        parts = [np.ones(len(pair))] + [pair[c].to_numpy(float) for c in cols]
        if dummies is not None:
            parts += [dummies]
        return np.column_stack(parts)
    yv, wv = pair[y].to_numpy(float), pair[w].to_numpy(float)
    oof = {k: np.zeros(len(pair)) for k in ("base", "plus")}
    for tr_i, te_i in GroupKFold(5).split(pair, groups=pair["pitcher"]):
        for k, cols in (("base", base), ("plus", base + plus)):
            Xm = X(cols)
            oof[k][te_i] = Xm[te_i] @ _wls(Xm[tr_i], yv[tr_i], wv[tr_i])
    def rmse(p, s): return float(np.sqrt(np.average((yv[s] - p[s]) ** 2, weights=wv[s])))
    ids = pair["pitcher"].to_numpy(); up = np.unique(ids); idx = {p: np.where(ids == p)[0] for p in up}
    gains = []
    for _ in range(n_boot):
        s = np.concatenate([idx[p] for p in rng.choice(up, len(up))])
        gains.append(rmse(oof["base"], s) - rmse(oof["plus"], s))
    allr = np.arange(len(pair))
    return (rmse(oof["base"], allr), rmse(oof["plus"], allr), float(np.mean(gains)),
            float(np.percentile(gains, 2.5)), float(np.percentile(gains, 97.5)))


def _pitch_prof(df):
    g = df.groupby(["pitcher", "pitch_type"]).agg(n=("rv", "size"), swings=("is_swing", "sum"),
                                                  whiffs=("is_whiff", "sum")).reset_index()
    g["whiff"] = g["whiffs"] / g["swings"].clip(lower=1)
    return g


def command_test(tr, te, rng) -> list[dict]:
    ct, cn = command_scores(tr), command_scores(te)
    a = _pitch_prof(tr).merge(ct, on=["pitcher", "pitch_type"])
    a = a[(a["n"] >= 200) & (a["swings_loc"] >= 100)]
    b = _pitch_prof(te).merge(cn, on=["pitcher", "pitch_type"])
    b = b[(b["n"] >= 100) & (b["swings"] >= 40) & (b["swings_loc"] >= 60)]
    m = a.merge(b, on=["pitcher", "pitch_type"], suffixes=("_t", "_n")).reset_index(drop=True)
    print(f"command: {len(m)} pitcher-pitches in both seasons")
    rows = []
    corr = lambda d: float(np.corrcoef(d["command_t"], d["command_n"])[0, 1])
    bs = [corr(m.sample(len(m), replace=True, random_state=int(s))) for s in rng.integers(0, 1e6, 400)]
    rows.append(dict(flag="command", n=len(m), metric="year-to-year correlation of command score",
                     estimate=round(corr(m), 3), ci_lo=round(np.percentile(bs, 2.5), 3),
                     ci_hi=round(np.percentile(bs, 97.5), 3)))
    dm = pd.get_dummies(m["pitch_type"], drop_first=True).astype(float).to_numpy()
    r = _cv_gain(m, "whiff_n", "swings_n", ["whiff_t", "xw_shape_t"], ["xw_loc_t"], rng, dm)
    rows.append(dict(flag="command", n=len(m),
                     metric="RMSE gain predicting next-year whiff: adding location-aware expected whiff",
                     estimate=round(r[2], 4), ci_lo=round(r[3], 4), ci_hi=round(r[4], 4)))
    return rows


def contact_test(tr, te, rng) -> list[dict]:
    a, b = contact_luck(tr), contact_luck(te)
    a = a[a["n_bip"] >= 150]
    b = b[b["n_bip"] >= 100].drop(columns=["player_name", "p_throws"])
    m = a.merge(b, on="pitcher", suffixes=("_t", "_n")).reset_index(drop=True)
    print(f"contact luck: {len(m)} pitchers in both seasons")
    rows = []
    r = _cv_gain(m, "wobacon_n", "n_bip_n", ["wobacon_t"], ["xwobacon_t"], rng)
    rows.append(dict(flag="contact luck", n=len(m),
                     metric="RMSE gain predicting next-year wOBA on contact: adding expected wOBA",
                     estimate=round(r[2], 4), ci_lo=round(r[3], 4), ci_hi=round(r[4], 4)))
    z = (m["luck_gap_t"] - m["luck_gap_t"].mean()) / m["luck_gap_t"].std()
    m["d"] = m["wobacon_n"] - m["wobacon_t"]
    pool = m[z.abs() < 1]
    for lab, mask in (("unlucky (actual above expected)", z >= 1), ("lucky (actual below expected)", z <= -1)):
        fl = m[mask]
        diffs = []
        for _, rr in fl.iterrows():
            c = pool.iloc[(pool["wobacon_t"] - rr["wobacon_t"]).abs().argsort()[:5]]
            diffs.append(rr["d"] - c["d"].mean())
        e, lo, hi = _ci(diffs, rng)
        rows.append(dict(flag="contact luck", n=len(fl),
                         metric=f"next-year wOBA-on-contact change vs matched controls: {lab}",
                         estimate=round(e, 4), ci_lo=round(lo, 4), ci_hi=round(hi, 4)))
    return rows


def main(train: int, test: int) -> None:
    tr, te = prep(load_season(train)), prep(load_season(test))
    rng = np.random.default_rng(0)
    res = pd.DataFrame(platoon_test(tr, te, rng) + costly_test(tr, te, rng)
                       + command_test(tr, te, rng) + contact_test(tr, te, rng))
    res.insert(0, "train->test", f"{train}->{test}")
    print(res.to_string(index=False))
    res.to_csv(OUT / f"flagtests_{train}_{test}.csv", index=False)


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:] if x.isdigit()]
    main(a[0] if a else 2024, a[1] if len(a) > 1 else 2025)


