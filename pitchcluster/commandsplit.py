"""Does command explain the shape flags?

Usage:  python -m pitchcluster.commandsplit      (run report.py for 2024-2026 first)

1. Correlation between each pitch's whiff gap (actual minus shape-expected) and its command score.
2. For pitches flagged UNDER/OUTPERFORMS shape, split by high vs. low command and compare the
   next-year whiff-rate change with matched controls (5 nearest unflagged pitches of the same type).
"""
from pathlib import Path

import numpy as np
import pandas as pd

R = Path(__file__).resolve().parent.parent / "outputs" / "report"


def _table(y: int) -> pd.DataFrame:
    t = pd.read_csv(R / f"buy_low_sell_high_{y}.csv")[
        ["pitcher", "pitch_type", "n", "whiff_rate", "xwhiff", "whiff_gap", "verdict"]]
    c = pd.read_csv(R / f"command_scores_{y}.csv")[["pitcher", "pitch_type", "command", "swings"]]
    return t.merge(c, on=["pitcher", "pitch_type"])


def _diffs_vs_controls(fl: pd.DataFrame, pool: pd.DataFrame) -> np.ndarray:
    out = []
    for _, r in fl.iterrows():
        c = pool[pool["pitch_type"] == r["pitch_type"]]
        if len(c):
            out.append(r["d"] - c.iloc[(c["whiff_rate_t"] - r["whiff_rate_t"]).abs().argsort()[:5]]["d"].mean())
    return np.array(out)


def _ci(v: np.ndarray, rng) -> tuple[float, float, float]:
    bs = [rng.choice(v, len(v)).mean() for _ in range(600)]
    return 100 * v.mean(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5)


def main() -> None:
    rng = np.random.default_rng(0)
    rows = []
    for a, b in ((2024, 2025), (2025, 2026)):
        ta, tb = _table(a), _table(b)
        m = ta.merge(tb[["pitcher", "pitch_type", "whiff_rate", "swings", "n"]],
                     on=["pitcher", "pitch_type"], suffixes=("_t", "_n"))
        m = m[(m["swings_n"] >= 40) & (m["n_n"] >= 100) & (m["swings_t"] >= 100)].copy()
        m["d"] = m["whiff_rate_n"] - m["whiff_rate_t"]
        corr = m["whiff_gap"].corr(m["command"])
        print(f"{a}->{b}: {len(m)} rows; corr(whiff_gap, command) = {corr:.2f}")
        rows.append((a, "all", "corr(whiff_gap, command)", len(m), corr, np.nan, np.nan))
        pool = m[m["verdict"] == "hold"]
        for lab in ("OUTPERF", "UNDER"):
            fl = m[m["verdict"].str.startswith(lab)]
            med = fl["command"].median()
            for part, sel in (("high command", fl["command"] >= med), ("low command", fl["command"] < med)):
                v = _diffs_vs_controls(fl[sel], pool)
                e, lo, hi = _ci(v, rng)
                print(f"  {lab:8s} {part:13s} n={len(v):3d}  next-yr whiff change vs controls "
                      f"{e:+.2f} pts (CI {lo:+.2f} to {hi:+.2f})")
                rows.append((a, lab, part, len(v), e, lo, hi))
    pd.DataFrame(rows, columns=["pair_start", "flag", "part", "n", "est_pts_or_corr", "ci_lo_pts", "ci_hi_pts"]
                 ).round(3).to_csv(R / "command_vs_shape_flags.csv", index=False)


if __name__ == "__main__":
    main()
