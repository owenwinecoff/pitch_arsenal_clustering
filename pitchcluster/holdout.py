"""True out-of-sample test: train on 2024, predict 2025.

Usage:  python -m pitchcluster.holdout [train_year] [test_year]

1. Forecast coefficients are fit ONLY on the train-year first-half -> second-half relationship.
2. They are frozen, then applied to full train-year profiles to forecast test-year whiff rate.
3. Compared with a naive baseline (same regression, past whiff rate only).  Scored on actual
   test-year data: swing-weighted RMSE/MAE, with a pitcher-level bootstrap CI on the RMSE gain.
4. Train-year flags (UNDER/OUTPERF) are checked against matched controls in the test year.

Outputs in outputs/report/: holdout_forecast_<train>_<test>.csv, holdout_summary_<train>_<test>.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from .data import load_season
from .report import SHRINK_K, buy_low_sell_high, prep

OUT = Path(__file__).resolve().parent.parent / "outputs" / "report"


KEY = ["pitcher", "pitch_type"]


def _agg(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby(KEY).agg(n=("rv", "size"), swings=("is_swing", "sum"),
                            whiffs=("is_whiff", "sum"), rv_sum=("rv", "sum")).reset_index()
    g["whiff_rate"] = g["whiffs"] / g["swings"].clip(lower=1)
    lg = g.groupby("pitch_type")["rv_sum"].sum() / g.groupby("pitch_type")["n"].sum()
    mu = g["pitch_type"].map(lg)
    g["rv100_shrunk"] = 100 * (g["rv_sum"] + SHRINK_K * mu) / (g["n"] + SHRINK_K)
    return g


def _wls(X: np.ndarray, y: np.ndarray, w: np.ndarray) -> np.ndarray:
    sw = np.sqrt(w)[:, None]
    return np.linalg.lstsq(X * sw, y * sw[:, 0], rcond=None)[0]

def design(d: pd.DataFrame, cols: list[str], types: list[str]) -> np.ndarray:
    dm = pd.get_dummies(d["pitch_type"]).astype(float).reindex(columns=types[1:], fill_value=0.0)
    return np.column_stack([np.ones(len(d)), d[cols].values, dm.values])


def main(train: int, test: int) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tr = prep(load_season(train))
    te = prep(load_season(test))

    # --- 1. fit forecast coefficients on train-year H1 -> H2 only ---
    mid = tr["game_date"].min() + (tr["game_date"].max() - tr["game_date"].min()) / 2
    f1 = buy_low_sell_high(tr[tr["game_date"] < mid], min_pitches=120)
    a2 = _agg(tr[tr["game_date"] >= mid])[KEY + ["n", "swings", "whiff_rate"]]
    a2 = a2.rename(columns={"n": "n_h2", "swings": "swings_h2", "whiff_rate": "whiff_h2"})
    fit = f1.merge(a2, on=KEY)
    fit = fit[(fit["swings_h2"] >= 40) & (fit["n_h2"] >= 100)]
    types = sorted(fit["pitch_type"].unique())
    betas = {}
    for name, cols in [("baseline", ["whiff_rate"]), ("shape", ["whiff_rate", "xwhiff"])]:
        betas[name] = _wls(design(fit, cols, types), fit["whiff_h2"].values,
                           fit["swings_h2"].values)
    print(f"Fit on {len(fit)} {train} H1->H2 pitch profiles. "
          f"shape coefs (whiff, xwhiff): {betas['shape'][1]:.3f}, {betas['shape'][2]:.3f}")

    # --- 2. forecast test year from full train year ---
    prof = buy_low_sell_high(tr, min_pitches=200)
    prof = prof[prof["pitch_type"].isin(types)]
    prof["pred_baseline"] = design(prof, ["whiff_rate"], types) @ betas["baseline"]
    prof["pred_shape"] = design(prof, ["whiff_rate", "xwhiff"], types) @ betas["shape"]

    act = _agg(te)[KEY + ["n", "swings", "whiff_rate", "rv100_shrunk"]]
    act = act.rename(columns={"n": "n_test", "swings": "swings_test",
                              "whiff_rate": "whiff_test", "rv100_shrunk": "rv100_test"})
    m = prof.merge(act, on=KEY)
    m = m[(m["swings_test"] >= 40) & (m["n_test"] >= 100)].reset_index(drop=True)
    print(f"{len(m)} pitcher-pitch combos with enough data in {train} and {test}")

    w = m["swings_test"].values
    def wrmse(p): return float(np.sqrt(np.average((m["whiff_test"] - p) ** 2, weights=w)))
    def wmae(p): return float(np.average((m["whiff_test"] - p).abs(), weights=w))
    naive = m["whiff_rate"]    # "next year = last year"
    rows = []
    for nm, p in [("naive (last year's whiff)", naive),
                  ("baseline (regressed whiff)", m["pred_baseline"]),
                  ("shape model (whiff + xwhiff)", m["pred_shape"])]:
        rows.append(dict(model=nm, rmse=round(wrmse(p), 4), mae=round(wmae(p), 4),
                         corr=round(float(np.corrcoef(p, m["whiff_test"])[0, 1]), 3)))
    summ = pd.DataFrame(rows)

    # bootstrap RMSE gain (baseline - shape) over pitchers
    rng = np.random.default_rng(0)
    groups = {p: np.where(m["pitcher"] == p)[0] for p in m["pitcher"].unique()}
    ids = np.array(list(groups))
    gains = []
    for _ in range(500):
        idx = np.concatenate([groups[p] for p in rng.choice(ids, len(ids))])
        s = m.iloc[idx]; ww = s["swings_test"].values
        r = lambda p: np.sqrt(np.average((s["whiff_test"] - s[p]) ** 2, weights=ww))
        gains.append(r("pred_baseline") - r("pred_shape"))
    lo, hi = np.percentile(gains, [2.5, 97.5])
    print(summ.to_string(index=False))
    print(f"RMSE gain, shape vs baseline: {np.mean(gains):.4f} (95% CI {lo:.4f} to {hi:.4f})")

    # --- 3. flag test vs matched controls ---
    m["d_whiff"] = m["whiff_test"] - m["whiff_rate"]
    m["d_rv"] = m["rv100_test"] - m["rv100_shrunk"]
    flag_rows = []
    for label, mask in [("UNDER", m["verdict"].str.startswith("UNDER")),
                        ("OUTPERF", m["verdict"].str.startswith("OUTPERF"))]:
        fl, pool = m[mask], m[m["verdict"] == "hold"]
        mc = pd.concat([pool[pool["pitch_type"] == r["pitch_type"]].iloc[
            (pool[pool["pitch_type"] == r["pitch_type"]]["whiff_rate"] - r["whiff_rate"])
            .abs().argsort()[:5]] for _, r in fl.iterrows()])
        for col, nm, nd in [("d_whiff", "whiff rate change", 4), ("d_rv", "shrunk RV/100 change", 3)]:
            bs = [fl[col].sample(len(fl), replace=True, random_state=int(s)).mean()
                  for s in rng.integers(0, 1e6, 500)]
            flag_rows.append(dict(
                flag=label, n=len(fl), metric=f"{nm}, flagged minus control",
                estimate=round(fl[col].mean() - mc[col].mean(), nd),
                ci_lo=round(np.percentile(bs, 2.5) - mc[col].mean(), nd),
                ci_hi=round(np.percentile(bs, 97.5) - mc[col].mean(), nd)))
    flags = pd.DataFrame(flag_rows)
    print("\n", flags.to_string(index=False))

    summ["rmse_gain_shape_vs_baseline"] = ""
    summ.loc[2, "rmse_gain_shape_vs_baseline"] = f"{np.mean(gains):.4f} ({lo:.4f} to {hi:.4f})"
    pd.concat([summ, flags], axis=0, ignore_index=True).to_csv(OUT / f"holdout_summary_{train}_{test}.csv", index=False)
    cols = ["player_name", "pitch_type", "n", "whiff_rate", "xwhiff", "verdict",
            "pred_baseline", "pred_shape", "whiff_test", "n_test"]
    m[cols].round(3).to_csv(OUT / f"holdout_forecast_{train}_{test}.csv", index=False)


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:] if x.isdigit()]
    main(a[0] if a else 2024, a[1] if len(a) > 1 else 2025)



