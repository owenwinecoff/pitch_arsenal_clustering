"""Feature engineering: pitcher x pitch-type profiles."""
from __future__ import annotations

import numpy as np
import pandas as pd

WHIFF = {"swinging_strike", "swinging_strike_blocked", "foul_tip"}
SWING = WHIFF | {
    "foul", "hit_into_play", "foul_bunt", "missed_bunt", "bunt_foul_tournament",
}

# Pitch types we treat as noise (too rare / not real pitches).
EXCLUDE = {"PO", "IN", "EP", "AB", "UN", "FA", "CS"}

SHAPE_FEATURES = [
    "velo", "spin", "hmov", "vmov", "rel_x", "rel_z", "ext", "axis_sin", "axis_cos",
]


def _normalize_handedness(df: pd.DataFrame) -> pd.DataFrame:
    """Mirror LHP so horizontal movement/release are comparable (arm-side = positive).

    Statcast pfx_x is from the catcher's view: RHP arm-side is negative.
    We flip so that positive hmov always means arm-side run.
    """
    df = df.copy()
    sign = np.where(df["p_throws"] == "R", -1.0, 1.0)
    df["hmov"] = df["pfx_x"] * 12 * sign  # feet -> inches
    df["vmov"] = df["pfx_z"] * 12
    df["rel_x"] = df["release_pos_x"] * sign * -1  # positive = arm-side release
    df["rel_z"] = df["release_pos_z"]
    # Spin axis in degrees (0-360); encode circularly, mirrored for LHP.
    axis = np.deg2rad(df["spin_axis"])
    df["axis_sin"] = np.where(df["p_throws"] == "R", np.sin(axis), np.sin(-axis))
    df["axis_cos"] = np.cos(axis)
    return df


def pitch_profiles(raw: pd.DataFrame, min_pitches: int = 150) -> pd.DataFrame:
    """One row per (pitcher, pitch_type) with physical shape + outcome metrics."""
    df = raw.dropna(subset=["pitch_type", "release_speed", "pfx_x", "pfx_z",
                            "release_spin_rate", "spin_axis"]).copy()
    df = df[~df["pitch_type"].isin(EXCLUDE)]
    df = _normalize_handedness(df)
    df["velo"] = df["release_speed"]
    df["spin"] = df["release_spin_rate"]
    df["ext"] = df["release_extension"]
    df["is_swing"] = df["description"].isin(SWING)
    df["is_whiff"] = df["description"].isin(WHIFF)
    # delta_run_exp is from the batting team's view; negate for pitcher value.
    df["run_value"] = -df["delta_run_exp"]

    g = df.groupby(["pitcher", "player_name", "p_throws", "pitch_type"])
    prof = g.agg(
        n=("velo", "size"),
        **{c: (c, "mean") for c in SHAPE_FEATURES if c not in ("axis_sin", "axis_cos")},
        axis_sin=("axis_sin", "mean"),
        axis_cos=("axis_cos", "mean"),
        swings=("is_swing", "sum"),
        whiffs=("is_whiff", "sum"),
        rv_sum=("run_value", "sum"),
    ).reset_index()

    prof = prof[prof["n"] >= min_pitches].copy()
    prof["whiff_rate"] = prof["whiffs"] / prof["swings"].clip(lower=1)
    prof["rv_per_100"] = 100 * prof["rv_sum"] / prof["n"]
    prof["usage"] = prof["n"] / prof.groupby("pitcher")["n"].transform("sum")
    return prof.reset_index(drop=True)

