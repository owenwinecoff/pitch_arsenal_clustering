"""Front-office decision report from Statcast pitch data.

Usage:  python -m pitchcluster.report [year]

Outputs (outputs/report/):
  buy_low_sell_high_<yr>.csv  pitch-level: physical "stuff" vs. results
  platoon_risks.csv      pitchers with large L/R whiff or run-value gaps
  pitch_usage_flags.csv  pitches that cost runs at meaningful usage
  REPORT.md              readable summary of the above
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import GroupKFold

from .data import load_season
from .features import EXCLUDE, SWING, WHIFF, _normalize_handedness

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs" / "report"

MIN_PITCHES = 200      # per pitcher-pitch for stuff/results comparison
PLATOON_PERSISTENCE = 0.2   # share of a platoon RV gap that persisted next season (flagtests.py)
SHRINK_K = 400         # pseudo-pitches of league-average RV to shrink toward
FEATS = ["velo", "spin", "hmov", "vmov", "ext", "rel_z", "rel_x", "axis_sin", "axis_cos"]


def prep(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.dropna(subset=["pitch_type", "release_speed", "pfx_x", "pfx_z",
                            "release_spin_rate", "spin_axis"]).copy()
    df = df[~df["pitch_type"].isin(EXCLUDE)]
    df = _normalize_handedness(df)
    df["velo"] = df["release_speed"]
    df["spin"] = df["release_spin_rate"]
    df["ext"] = df["release_extension"]
    df["is_swing"] = df["description"].isin(SWING)
    df["is_whiff"] = df["description"].isin(WHIFF)
    df["rv"] = -df["delta_run_exp"]          # pitcher's perspective, + = good
    df["game_date"] = pd.to_datetime(df["game_date"])
    return df


def _swing_features(sw: pd.DataFrame) -> pd.DataFrame:
    """Add features beyond raw shape: how each pitch differs from the pitcher's own primary
    fastball (speed and break separation), and whether batter and pitcher share a side."""
    sw = sw.copy()
    fb = sw[sw["pitch_type"].isin(["FF", "SI", "FC"])]
    counts = fb.groupby(["pitcher", "pitch_type"]).size().reset_index(name="c")
    primary = counts.sort_values("c").groupby("pitcher").tail(1)[["pitcher", "pitch_type"]]
    ref = fb.merge(primary, on=["pitcher", "pitch_type"]).groupby("pitcher")[["velo", "hmov", "vmov"]].mean()
    ref.columns = ["fb_velo", "fb_hmov", "fb_vmov"]
    sw = sw.join(ref, on="pitcher")
    sw["d_velo"] = sw["velo"] - sw["fb_velo"]
    sw["d_hmov"] = sw["hmov"] - sw["fb_hmov"]
    sw["d_vmov"] = sw["vmov"] - sw["fb_vmov"]
    sw["same_side"] = (sw["stand"] == sw["p_throws"]).astype(float)
    sw["ptype"] = sw["pitch_type"].astype("category").cat.codes
    return sw


SWING_FEATS = FEATS + ["d_velo", "d_hmov", "d_vmov", "same_side", "ptype"]


def _pitch_level_xwhiff(df: pd.DataFrame) -> pd.DataFrame:
    """Expected whiff rate per (pitcher, pitch_type) from a pitch-level model on every swing.

    Out-of-fold by pitcher, so a pitcher's own results never inform his own expectation.
    """
    sw = _swing_features(df[df["is_swing"]].reset_index(drop=True))
    cat = [SWING_FEATS.index("ptype")]
    pred = np.zeros(len(sw))
    for tr, te in GroupKFold(5).split(sw, groups=sw["pitcher"]):
        m = HistGradientBoostingClassifier(max_depth=4, learning_rate=0.08, max_iter=250,
                                           min_samples_leaf=100, categorical_features=cat,
                                           random_state=0)
        m.fit(sw.loc[tr, SWING_FEATS], sw.loc[tr, "is_whiff"])
        pred[te] = m.predict_proba(sw.loc[te, SWING_FEATS])[:, 1]
    sw["xw"] = pred
    return sw.groupby(["pitcher", "pitch_type"])["xw"].mean().rename("xwhiff").reset_index()


def buy_low_sell_high(df: pd.DataFrame, min_pitches: int = MIN_PITCHES) -> pd.DataFrame:
    g = df.groupby(["pitcher", "player_name", "p_throws", "pitch_type"])
    prof = g.agg(n=("velo", "size"), swings=("is_swing", "sum"), whiffs=("is_whiff", "sum"),
                 rv_sum=("rv", "sum"),
                 **{f: (f, "mean") for f in FEATS if f not in ("axis_sin", "axis_cos")},
                 axis_sin=("axis_sin", "mean"), axis_cos=("axis_cos", "mean")).reset_index()
    prof = prof[prof["n"] >= min_pitches].reset_index(drop=True)
    prof["whiff_rate"] = prof["whiffs"] / prof["swings"].clip(lower=1)
    prof = prof.merge(_pitch_level_xwhiff(df), on=["pitcher", "pitch_type"], how="left")
    prof["whiff_gap"] = prof["whiff_rate"] - prof["xwhiff"]

    # Shrunk run value per 100: noisy RV pulled toward the pitch-type league mean.
    lg = prof.groupby("pitch_type").apply(
        lambda d: d["rv_sum"].sum() / d["n"].sum(), include_groups=False)
    mu = prof["pitch_type"].map(lg)
    prof["rv100"] = 100 * prof["rv_sum"] / prof["n"]
    prof["rv100_shrunk"] = 100 * (prof["rv_sum"] + SHRINK_K * mu) / (prof["n"] + SHRINK_K)

    # Stuff-implied whiff vs actual: negative gap = results worse than shape deserves.
    # Verdict combines the whiff gap with run-value results.
    z = (prof["whiff_gap"] - prof["whiff_gap"].mean()) / prof["whiff_gap"].std()
    prof["whiff_gap_z"] = z
    conds = [
        (z <= -1.0) & (prof["rv100_shrunk"] <= prof["rv100_shrunk"].median()),
        (z >= 1.0) & (prof["rv100_shrunk"] >= prof["rv100_shrunk"].median()),
    ]
    prof["verdict"] = np.select(conds, ["UNDERPERFORMS SHAPE (investigate/buy)",
                                        "OUTPERFORMS SHAPE (command/deception)"], "hold")
    cols = ["pitcher", "player_name", "p_throws", "pitch_type", "n", "velo", "spin", "hmov", "vmov",
            "whiff_rate", "xwhiff", "whiff_gap", "whiff_gap_z", "rv100", "rv100_shrunk", "verdict"]
    return prof[cols].round(3).sort_values("whiff_gap_z")


def platoon(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby(["pitcher", "player_name", "p_throws", "stand"]).agg(
        n=("rv", "size"), swings=("is_swing", "sum"), whiffs=("is_whiff", "sum"),
        rv_sum=("rv", "sum")).reset_index()
    g["whiff_rate"] = g["whiffs"] / g["swings"].clip(lower=1)
    g["rv100"] = 100 * g["rv_sum"] / g["n"]
    w = g.pivot(index=["pitcher", "player_name", "p_throws"], columns="stand",
                values=["n", "whiff_rate", "rv100"]).dropna()
    w.columns = [f"{a}_{b}" for a, b in w.columns]
    w = w.reset_index()
    w = w[(w["n_L"] >= 400) & (w["n_R"] >= 400)]
    w["rv100_gap"] = w["rv100_L"] - w["rv100_R"]       # + = better vs LHB
    w["weak_side"] = np.where(w["rv100_gap"] > 0, "vs RHB", "vs LHB")
    w["abs_gap"] = w["rv100_gap"].abs()
    return w.sort_values("abs_gap", ascending=False).drop(columns="abs_gap").round(2)


def usage_flags(df: pd.DataFrame, bb: pd.DataFrame) -> pd.DataFrame:
    tot = df.groupby("pitcher").size().rename("total")
    g = df.groupby(["pitcher", "player_name", "pitch_type"]).agg(
        n=("rv", "size"), rv_sum=("rv", "sum")).reset_index().join(tot, on="pitcher")
    g["usage"] = g["n"] / g["total"]
    g = g[(g["n"] >= 300) & (g["usage"] >= 0.15)].copy()
    lg = g.groupby("pitch_type")["rv_sum"].sum() / g.groupby("pitch_type")["n"].sum()
    g["rv100_shrunk"] = 100 * (g["rv_sum"] + SHRINK_K * g["pitch_type"].map(lg)) / (g["n"] + SHRINK_K)
    g["runs_lost_vs_avg"] = -(g["rv_sum"] - g["n"] * g["pitch_type"].map(lg))
    g = g[(g["rv100_shrunk"] < -0.5)]
    return g.sort_values("runs_lost_vs_avg", ascending=False).round(3)[
        ["pitcher", "player_name", "pitch_type", "n", "usage", "rv100_shrunk", "runs_lost_vs_avg"]]


LATEST_TESTED = 2026   # last season used in the year-ahead tests (see holdout.py / flagtests.py)


# ----------------------------- formatting helpers -----------------------------
def flip(name: str) -> str:
    """"Last, First" -> "First Last"."""
    last, _, first = str(name).partition(", ")
    return f"{first} {last}".strip()


def pct(v, d=1): return f"{100 * v:.{d}f}%"
def num(v, d=2): return f"{v:.{d}f}"
def sgn(v, d=2): return f"{v:+.{d}f}"
def pts(v): return f"{100 * v:+.1f}"                       # rate difference in percentage points
def woba(v): return f"{v:.3f}".lstrip("0")                 # .345
def swoba(v): return f"{v:+.3f}".replace("+0.", "+.").replace("-0.", "-.")


def md_table(d: pd.DataFrame, spec: dict, n: int = 10) -> str:
    """spec: header -> (source column, formatter or None). Names are flipped to First Last."""
    out = {}
    for head, (src, fmt) in spec.items():
        col = d[src].head(n)
        if src == "player_name":
            col = col.map(flip)
        elif fmt is not None:
            col = col.map(fmt)
        out[head] = col.to_list()
    return pd.DataFrame(out).to_markdown(index=False, disable_numparse=True)


def names(d: pd.DataFrame, col: str = "player_name", extra: str | None = None, k: int = 3) -> str:
    parts = []
    for _, r in d.head(k).iterrows():
        parts.append(flip(r[col]) + (f" ({r[extra]})" if extra else ""))
    return ", ".join(parts)


# ----------------------------- evidence from the saved test outputs -----------------------------
def _load_evidence() -> dict:
    """Read the year-ahead test CSVs so the report's evidence statements never go stale."""
    pairs = [(2024, 2025), (2025, 2026)]
    ev = {"pairs": pairs, "ok": True}
    try:
        hs = [pd.read_csv(OUT / f"holdout_summary_{a}_{b}.csv") for a, b in pairs]
        ft = [pd.read_csv(OUT / f"flagtests_{a}_{b}.csv") for a, b in pairs]
        cv = pd.read_csv(OUT / "command_vs_shape_flags.csv")
    except FileNotFoundError:
        return {"ok": False}

    def whiff(h, flag):
        r = h[(h["flag"] == flag) & h["metric"].str.startswith("whiff rate", na=False)].iloc[0]
        return 100 * r["estimate"], 100 * r["ci_lo"], 100 * r["ci_hi"], int(r["n"])
    ev["under"] = [whiff(h, "UNDER") for h in hs]
    ev["over"] = [whiff(h, "OUTPERF") for h in hs]
    ev["rmse_gain"] = [float(str(h.loc[h["model"].str.startswith("shape", na=False), "rmse_gain_shape_vs_baseline"]
                                 .iloc[0]).split()[0]) for h in hs]

    def ftest(f, flag, key):
        r = f[(f["flag"] == flag) & f["metric"].str.contains(key, regex=False)].iloc[0]
        return float(r["estimate"]), float(r["ci_lo"]), float(r["ci_hi"]), int(r["n"])
    ev["platoon_slope"] = [ftest(f, "platoon", "slope") for f in ft]
    ev["platoon_weak"] = [ftest(f, "platoon", "weak side") for f in ft]
    ev["costly"] = [ftest(f, "costly pitch", "flagged minus unflagged") for f in ft]
    ev["cmd_persist"] = [ftest(f, "command", "correlation") for f in ft]
    ev["cmd_gain"] = [ftest(f, "command", "RMSE gain") for f in ft]
    ev["luck_gain"] = [ftest(f, "contact luck", "RMSE gain") for f in ft]
    ev["unlucky"] = [ftest(f, "contact luck", "unlucky") for f in ft]
    ev["lucky"] = [ftest(f, "contact luck", "lucky (actual below") for f in ft]
    c = cv[cv["part"] == "corr(whiff_gap, command)"]["est_pts_or_corr"].to_list()
    ev["gap_cmd_corr"] = c
    sp = {}
    for _, r in cv[cv["part"].isin(["high command", "low command"])].iterrows():
        sp[(int(r["pair_start"]), r["flag"], r["part"])] = float(r["est_pts"] if "est_pts" in r else r["est_pts_or_corr"])
    ev["split"] = sp
    return ev


def _nsig(rows, sign):
    """How many of the (est, lo, hi, n) rows have an interval excluding zero in the expected direction."""
    return sum(1 for e, lo, hi, *_ in rows if (sign > 0 and lo > 0) or (sign < 0 and hi < 0))


def sig_phrase(k: int) -> str:
    return {0: "neither test", 1: "one of the two tests", 2: "both tests"}[k]


def _range(vals, code):
    """Format min-to-max of `vals`. code: 'p0' = percent, '1'/'2'/'4' = decimals."""
    f = (lambda v: f"{100 * v:.0f}%") if code == "p0" else (lambda v: f"{v:.{code}f}")
    lo, hi = min(vals), max(vals)
    return f(lo) if f(lo) == f(hi) else f"{f(lo)} to {f(hi)}"


# ----------------------------- the report -----------------------------
def write_md(year, bl, pl, uf, cs, cl) -> str:
    ev = _load_evidence()
    out: list[str] = []
    add = out.append

    # ---- pick the rows each section shows ----
    shape = bl[bl["n"] >= 400]
    under = shape[shape["verdict"].str.startswith("UNDER")].sort_values("whiff_gap_z")
    over = shape[shape["verdict"].str.startswith("OUTPERF")].sort_values("whiff_gap_z", ascending=False)
    cs = cs[(cs["n"] >= 300) & (cs["swings_loc"] >= 150)].copy()
    cs["command_pts"] = cs["command"]
    cmd_best = cs.sort_values("command", ascending=False)
    cmd_worst = cs.sort_values("command")
    cl = cl[cl["n_bip"] >= 250].copy()
    luck_bad = cl.sort_values("luck_gap", ascending=False)
    luck_good = cl.sort_values("luck_gap")
    pl = pl.copy()
    pl["expected_next_gap"] = pl["rv100_gap"] * PLATOON_PERSISTENCE
    uf = uf.copy()

    # ---- pitchers flagged in more than one section ----
    tags: dict[int, list[tuple[str, str]]] = {}
    def tag(df, section, label_fn):
        for _, r in df.iterrows():
            tags.setdefault(r["pitcher"], []).append((section, label_fn(r)))
    tag(under, "Underperforms shape", lambda r: f"{r['pitch_type']}")
    tag(over, "Outperforms shape", lambda r: f"{r['pitch_type']}")
    tag(cmd_best.head(20), "Strong command", lambda r: f"{r['pitch_type']}")
    tag(cmd_worst.head(20), "Weak command", lambda r: f"{r['pitch_type']}")
    tag(luck_bad.head(15), "Unlucky contact", lambda r: "")
    tag(luck_good.head(15), "Lucky contact", lambda r: "")
    tag(pl.head(25), "Platoon gap", lambda r: r["weak_side"])
    tag(uf, "Costly pitch", lambda r: f"{r['pitch_type']}")
    team_of = {}
    for d in (bl, pl, cl, uf, cs):
        for pid, tm in d[["pitcher", "team"]].drop_duplicates().itertuples(index=False):
            team_of.setdefault(pid, tm)
    name_of = {}
    for d in (bl, pl, cl, uf):
        for _, r in d[["pitcher", "player_name"]].drop_duplicates().iterrows():
            name_of.setdefault(r["pitcher"], r["player_name"])
    rows = []
    for pid, items in tags.items():
        sections = sorted({s for s, _ in items})
        if len(sections) >= 2:
            txt = "; ".join(f"{s}" + (f" ({l})" if l else "") for s, l in sorted(set(items)))
            rows.append(dict(player_name=name_of.get(pid, str(pid)), team=team_of.get(pid, ""),
                             flags=len(sections), detail=txt))
    multi = pd.DataFrame(rows)
    if len(multi):
        multi = multi.sort_values(["flags", "player_name"], ascending=[False, True])

    # ---- header ----
    add(f"# Pitching Decision Report, {year}\n")
    add(f"Source: Statcast regular-season pitches, {year}. Run value (RV) is per 100 pitches from the pitcher's "
        "view (positive = good for the pitcher). Team is the pitcher's last team of the season, so traded pitchers "
        "show their final club.\n")
    if year < LATEST_TESTED:
        add(f"> **Retrospective report.** The evidence cited below comes from tests that use seasons after {year}, "
            "which were not available at the time. Read it as a back-cast, not as what could have been known then.\n")

    # ---- key takeaways ----
    add("## Key takeaways\n")
    if ev["ok"]:
        add(f"- **What held up in later seasons:** platoon gaps persist only about {pct(ev['platoon_slope'][0][0], 0)} "
            f"(the weak side holds {_range([e for e, *_ in ev['platoon_weak']], 'p0')} of the time for the biggest gaps), "
            "and heavily used pitches that cost runs kept costing runs. Command is a repeatable skill. Shape-based and contact-luck "
            "flags are modest hints, not calls.")
    add(f"- **Pitches whose results lag their shape (look at video):** {names(under, extra='pitch_type')}.")
    add(f"- **Pitches whose results beat their shape (expect some give-back):** {names(over, extra='pitch_type')}.")
    add(f"- **Best command:** {names(cmd_best, extra='pitch_type')}. **Weakest:** {names(cmd_worst, extra='pitch_type')}.")
    add(f"- **Platoon, largest gaps:** " + ", ".join(
        f"{flip(r['player_name'])} ({r['weak_side']})" for _, r in pl.head(3).iterrows()) + ".")
    add(f"- **Costliest heavy-use pitches:** {names(uf, extra='pitch_type')}.")
    if len(multi):
        add(f"- **Flagged in more than one section:** {len(multi)} pitchers, led by "
            + names(multi, k=3) + " (table below).")
    add("")

    # ---- trust table ----
    add("## How much to trust each section\n")
    add("Each measure was tested on a later season than the one it was built from "
        "(2024->2025 and 2025->2026). Treat the sections accordingly.\n")
    if ev["ok"]:
        n_u, n_o = _nsig(ev["under"], +1), _nsig(ev["over"], -1)
        luck_dir = 0
        luck_sig = 0
        for e, lo, hi, _ in ev["unlucky"]:
            luck_dir += e < 0; luck_sig += hi < 0
        for e, lo, hi, _ in ev["lucky"]:
            luck_dir += e > 0; luck_sig += lo > 0
        add("| Section | Evidence | Use it for |")
        add("|---|---|---|")
        add(f"| 1. Underperforms shape | Modest: next-year whiff rate rose {_range([e for e, *_ in ev['under']], '1')} points "
            f"more than matched controls; significant in {sig_phrase(n_u)} | A reason to look at video, not a prediction |")
        add(f"| 2. Outperforms shape | Modest: whiff rate fell {_range([-e for e, *_ in ev['over']], '1')} points "
            f"more than controls; significant in {sig_phrase(n_o)} | Discounting results, not selling |")
        add(f"| 3. Command score | A repeatable skill (year-to-year correlation {_range([e for e, *_ in ev['cmd_persist']], '2')}); "
            "it does not improve next-year whiff forecasts | Explaining why results differ from shape |")
        add(f"| 4. Contact luck | Weak: right direction in {luck_dir} of 4 comparisons, significant in {luck_sig}; "
            "expected wOBA did not beat actual wOBA at predicting next year | Context only |")
        add(f"| 5. Platoon gaps | Validated: about {pct(ev['platoon_slope'][0][0], 0)} of the gap persists | Shrunk platoon deployment |")
        add(f"| 6. Costly heavy-use pitches | Validated: flagged pitches did {_range([-e for e, *_ in ev['costly']], '2')} "
            "runs/100 worse next year than other heavy-use pitches | Usage and pitch-mix review |")
        add("")
        add(f"As a *projection*, the shape model adds only about 1% to simply regressing last year's whiff rate toward the mean "
            f"(RMSE gain {_range(ev['rmse_gain'], '4')}). Its value is as a flag for pitches to look at, not as a forecasting tool.\n")
    else:
        add("_Test outputs not found; run `holdout.py`, `flagtests.py` and `commandsplit.py` to include evidence._\n")

    # ---- multi-flag table ----
    add("## Pitchers flagged in more than one section\n")
    add("Overlap is a useful place to start, but it is descriptive: several of these measures share inputs, so overlapping flags "
        "are not independent evidence. Strong/weak command counts the 20 highest/lowest scores; platoon counts the 25 largest gaps; "
        "contact luck the 15 largest gaps each way.\n")
    if len(multi):
        m = multi.head(12).rename(columns={"player_name": "Pitcher", "team": "Team", "flags": "Sections", "detail": "Flags"})
        m["Pitcher"] = m["Pitcher"].map(flip)
        add(m[["Pitcher", "Team", "Sections", "Flags"]].to_markdown(index=False, disable_numparse=True))
    else:
        add("_No pitcher appears in more than one section this year._")
    add("")

    # ---- section 1 ----
    gap_spec = {"Pitcher": ("player_name", None), "Team": ("team", str), "Pitch": ("pitch_type", str),
                "Pitches": ("n", lambda v: f"{int(v)}"), "Velo": ("velo", lambda v: num(v, 1)),
                "Whiff%": ("whiff_rate", pct), "Expected whiff%": ("xwhiff", pct),
                "Gap (pts)": ("whiff_gap", pts), "RV/100": ("rv100_shrunk", sgn)}
    add("## 1. Underperforms shape: look closer\n")
    add("A pitch-level model predicts the chance of a miss on every swing from velocity, spin, movement, extension, release point, "
        "how the pitch differs from the pitcher's own fastball (speed and break separation) and batter side, fit out-of-fold by "
        "pitcher. Averaging over a pitcher's swings gives an expected whiff rate. The gap is actual minus expected. Pitches that "
        "whiff far fewer hitters than their shape predicts, with below-median run value, are candidates for a mechanical, "
        "sequencing or location fix. A very large gap can also mean the model is extrapolating, so check video before acting.\n")
    add(md_table(under, gap_spec, 12) + "\n")

    # ---- section 2 ----
    add("## 2. Outperforms shape: discount the results\n")
    over_txt = ""
    if ev["ok"]:
        over_txt = (" In the year-ahead tests these pitches gave back "
                    + " and ".join(f"{-e:.1f}" for e, *_ in ev["over"]) + " whiff points versus matched controls")
        if _nsig(ev["over"], -1) < 2:
            over_txt += f" (significant in {sig_phrase(_nsig(ev['over'], -1))})"
        over_txt += ", so expect partial regression, not collapse."
    add("Whiff rate and run value well above what the shape predicts. This is usually command, location, tunneling or deception, "
        "which is partly real (see section 3: command explains much of the gap but does not protect against regression)."
        + over_txt + " Do not pay for their shape; weigh their results with some discount.\n")
    add(md_table(over, gap_spec, 12) + "\n")

    # ---- section 3 ----
    add("## 3. Command: whose locations create misses\n")
    cmd_txt = ("Command score is how many more misses per swing (in percentage points) a pitcher's locations create than the same pitch "
               "shape would league-wide (a location-aware model minus a shape-only model, both fit out-of-fold by pitcher). "
               "Zone% is the share of pitches in the zone; chase% is how often hitters swing at pitches out of it. ")
    if ev["ok"]:
        sp = ev["split"]
        hi_o = [sp.get((a, "OUTPERF", "high command")) for a, _ in ev["pairs"]]
        lo_o = [sp.get((a, "OUTPERF", "low command")) for a, _ in ev["pairs"]]
        cmd_txt += (f"It is a repeatable skill (year-to-year correlation {_range([e for e, *_ in ev['cmd_persist']], '2')}) "
                    f"and tracks the shape gap closely (correlation {_range(ev['gap_cmd_corr'], '2')} with actual-minus-expected whiff), "
                    "so it explains much of why a pitch beats or lags its shape. But last year's whiff rate already contains it, so it does not "
                    "improve forecasts, and high-command \"outperformers\" regressed about as much as low-command ones "
                    f"({hi_o[0]:+.1f} vs {lo_o[0]:+.1f} and {hi_o[1]:+.1f} vs {lo_o[1]:+.1f} whiff points), so command alone does not make those "
                    "results durable. ")
    add(cmd_txt + "Pitch types with at least 300 pitches and 150 swings are shown.\n")
    cmd_spec = {"Pitcher": ("player_name", None), "Team": ("team", str), "Pitch": ("pitch_type", str),
                "Pitches": ("n", lambda v: f"{int(v)}"), "Command (pts)": ("command", pts),
                "Zone%": ("zone_rate", pct), "Chase%": ("chase_rate", pct),
                "Whiff%": ("whiff", pct), "Shape-expected whiff%": ("xw_shape", pct)}
    add("**Strongest command:**\n")
    add(md_table(cmd_best, cmd_spec, 10) + "\n")
    add("**Weakest command:**\n")
    add(md_table(cmd_worst, cmd_spec, 8) + "\n")

    # ---- section 4 ----
    add("## 4. Contact luck (weak evidence)\n")
    add("Actual wOBA on balls in play vs. the wOBA expected from exit velocity and launch angle (min 250 balls in play). "
        "Gap is actual minus expected: positive means the pitcher allowed more damage than the contact deserved. "
        "In testing, expected wOBA did not beat actual wOBA at predicting next year, and the \"unlucky\" and \"lucky\" groups moved the "
        "expected way in most comparisons but rarely significantly. Use as context, not as a call.\n")
    luck_spec = {"Pitcher": ("player_name", None), "Team": ("team", str), "Throws": ("p_throws", str),
                 "Balls in play": ("n_bip", lambda v: f"{int(v)}"), "Actual wOBA": ("wobacon", woba),
                 "Expected wOBA": ("xwobacon", woba), "Gap": ("luck_gap", swoba)}
    add("**Results worse than contact quality (possible rebound):**\n")
    add(md_table(luck_bad, luck_spec, 8) + "\n")
    add("**Results better than contact quality (possible give-back):**\n")
    add(md_table(luck_good, luck_spec, 8) + "\n")

    # ---- section 5 ----
    add("## 5. Platoon vulnerabilities\n")
    add("Largest run-value gaps between left- and right-handed batters (at least 400 pitches each side). Gap is RV/100 against "
        "lefties minus RV/100 against righties: positive means the pitcher is weaker against right-handed batters. ")
    if ev["ok"]:
        add(f"Only about {pct(ev['platoon_slope'][0][0], 0)} of a pitcher's gap carried into the following season in testing, so the "
            f"expected next-year gap shrinks it accordingly. The weak side stayed the weak side "
            f"{_range([e for e, *_ in ev['platoon_weak']], 'p0')} of the time for the biggest gaps. ")
    add("Use for deployment hints, not hard role limits.\n")
    pl_spec = {"Pitcher": ("player_name", None), "Team": ("team", str), "Throws": ("p_throws", str),
               "Pitches vs L": ("n_L", lambda v: f"{int(v)}"), "Pitches vs R": ("n_R", lambda v: f"{int(v)}"),
               "RV/100 vs L": ("rv100_L", sgn), "RV/100 vs R": ("rv100_R", sgn), "Gap": ("rv100_gap", sgn),
               "Expected next-year gap": ("expected_next_gap", sgn), "Weak side": ("weak_side", str)}
    add(md_table(pl, pl_spec, 12) + "\n")

    # ---- section 6 ----
    add("## 6. Heavily used pitches that cost runs\n")
    cost_txt = ""
    if ev["ok"]:
        cost_txt = (f" Flagged pitches did {_range([-e for e, *_ in ev['costly']], '2')} runs per 100 worse than "
                    "unflagged heavy-use pitches the following year.")
    add("Pitch types thrown at least 15% of the time with shrunk RV below -0.5 per 100, ranked by runs lost vs. the league average "
        "for that pitch type over the season." + cost_txt + " Candidates for usage reduction, a shape or location change, or replacement.\n")
    uf_spec = {"Pitcher": ("player_name", None), "Team": ("team", str), "Pitch": ("pitch_type", str),
               "Pitches": ("n", lambda v: f"{int(v)}"), "Usage": ("usage", lambda v: pct(v, 0)),
               "RV/100": ("rv100_shrunk", sgn), "Runs lost vs avg": ("runs_lost_vs_avg", lambda v: f"{v:.1f}")}
    add(md_table(uf, uf_spec, 12) + "\n")

    # ---- caveats ----
    add("## Caveats\n")
    add("- Run value is noisy at these sample sizes. Shrinkage mitigates but does not remove that.")
    add("- The shape model sees physical shape, separation from the pitcher's own fastball and batter side. Location is handled "
        "separately by the command score; sequencing and pitch-to-pitch tunneling are not modeled.")
    ns = [r[3] for key in ("under", "over", "unlucky", "lucky", "costly") if ev["ok"] for r in ev[key]]
    if ns:
        add(f"- Flag tests used only three seasons and small flagged samples ({min(ns)} to {max(ns)} per test), so intervals are wide.")
    return "\n".join(out) + "\n"


def main(year: int) -> None:
    from .command import command_scores, contact_luck, zone_stats
    OUT.mkdir(parents=True, exist_ok=True)
    df = prep(load_season(year))
    bl = buy_low_sell_high(df)

    # pitcher -> last team of the season (home team pitches in the top of the inning)
    side = np.where(df["inning_topbot"] == "Top", df["home_team"], df["away_team"])
    team = df.assign(team=side).sort_values("game_date").groupby("pitcher")["team"].last()

    prof = df.groupby(["pitcher", "player_name", "pitch_type"]).agg(
        n=("rv", "size"), swings=("is_swing", "sum"), whiffs=("is_whiff", "sum")).reset_index()
    prof["whiff"] = prof["whiffs"] / prof["swings"].clip(lower=1)
    cs = (command_scores(df).merge(zone_stats(df), on=["pitcher", "pitch_type"])
          .merge(prof, on=["pitcher", "pitch_type"]))
    cl = contact_luck(df)
    pl, uf = platoon(df), usage_flags(df, bl)
    bl, cs, cl, pl, uf = (d.assign(team=d["pitcher"].map(team)) for d in (bl, cs, cl, pl, uf))

    bl.to_csv(OUT / f"buy_low_sell_high_{year}.csv", index=False)
    cs.round(4).to_csv(OUT / f"command_scores_{year}.csv", index=False)
    cl.round(4).to_csv(OUT / f"contact_luck_{year}.csv", index=False)
    pl.to_csv(OUT / f"platoon_risks_{year}.csv", index=False)
    uf.to_csv(OUT / f"pitch_usage_flags_{year}.csv", index=False)
    (OUT / f"REPORT_{year}.md").write_text(write_md(year, bl, pl, uf, cs, cl), encoding="utf-8")
    print(bl["verdict"].value_counts().to_string())
    print(f"Report written to {OUT / f'REPORT_{year}.md'}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2024)
