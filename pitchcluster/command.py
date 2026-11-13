"""Command (location) and contact-luck measures, from plate location and batted-ball data.

Command score (per pitcher and pitch type):
    mean over his swings of [P(miss | shape + location + count) - P(miss | shape only)]
Positive = his locations produce more misses than the same pitch shape would on average.
Both models are fit on the same swings, out-of-fold by pitcher, so the difference isolates
what location adds.

Contact luck (per pitcher):
    actual wOBA on balls in play minus expected wOBA from exit velocity and launch angle.
Positive = the pitcher allowed more damage than the contact quality deserved (unlucky).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import GroupKFold

from .report import FEATS, _swing_features

# strike zone half-width (17in plate / 2) plus ball radius, in feet; vertical pad likewise
ZONE_X, ZONE_PAD_Z = 0.83, 0.12
SHAPE_F = FEATS + ["d_velo", "d_hmov", "d_vmov", "same_side", "ptype"]
LOC_F = SHAPE_F + ["px_b", "plate_z", "z_norm", "balls", "strikes"]
LOC_COLS = ["plate_x", "plate_z", "sz_top", "sz_bot", "balls", "strikes"]


def _oof_prob(sw: pd.DataFrame, feats: list[str]) -> np.ndarray:
    cat = [feats.index("ptype")]
    pred = np.zeros(len(sw))
    for tr, te in GroupKFold(5).split(sw, groups=sw["pitcher"]):
        m = HistGradientBoostingClassifier(max_depth=4, learning_rate=0.08, max_iter=250,
                                           min_samples_leaf=100, categorical_features=cat,
                                           random_state=0)
        m.fit(sw.loc[tr, feats], sw.loc[tr, "is_whiff"])
        pred[te] = m.predict_proba(sw.loc[te, feats])[:, 1]
    return pred


def command_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Per (pitcher, pitch_type): swings, shape-only and location-aware expected whiff, command."""
    sw = df[df["is_swing"]].dropna(subset=LOC_COLS).reset_index(drop=True)
    sw = _swing_features(sw)
    sw["px_b"] = sw["plate_x"] * np.where(sw["stand"] == "L", -1.0, 1.0)  # + = toward batter's far side
    sw["z_norm"] = (sw["plate_z"] - sw["sz_bot"]) / (sw["sz_top"] - sw["sz_bot"])
    sw["xw_shape"] = _oof_prob(sw, SHAPE_F)
    sw["xw_loc"] = _oof_prob(sw, LOC_F)
    out = sw.groupby(["pitcher", "pitch_type"]).agg(
        swings_loc=("is_whiff", "size"), xw_shape=("xw_shape", "mean"), xw_loc=("xw_loc", "mean")
    ).reset_index()
    out["command"] = out["xw_loc"] - out["xw_shape"]
    return out


def zone_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Per (pitcher, pitch_type): zone rate and chase rate induced (swings at out-of-zone pitches)."""
    d = df.dropna(subset=LOC_COLS).copy()
    d["in_zone"] = ((d["plate_x"].abs() <= ZONE_X)
                    & (d["plate_z"] >= d["sz_bot"] - ZONE_PAD_Z)
                    & (d["plate_z"] <= d["sz_top"] + ZONE_PAD_Z))
    d["ooz_swing"] = (~d["in_zone"]) & d["is_swing"]
    d["ooz"] = ~d["in_zone"]
    g = d.groupby(["pitcher", "pitch_type"]).agg(
        n_loc=("in_zone", "size"), zone_rate=("in_zone", "mean"),
        ooz=("ooz", "sum"), ooz_swing=("ooz_swing", "sum")).reset_index()
    g["chase_rate"] = g["ooz_swing"] / g["ooz"].clip(lower=1)
    return g[["pitcher", "pitch_type", "n_loc", "zone_rate", "chase_rate"]]


def contact_luck(df: pd.DataFrame) -> pd.DataFrame:
    """Per pitcher: actual vs. expected wOBA on balls in play."""
    b = df[(df["type"] == "X")].dropna(subset=["launch_speed", "launch_angle",
                                              "estimated_woba_using_speedangle", "woba_value"])
    g = b.groupby("pitcher").agg(
        player_name=("player_name", "first"), p_throws=("p_throws", "first"),
        n_bip=("woba_value", "size"), wobacon=("woba_value", "mean"),
        xwobacon=("estimated_woba_using_speedangle", "mean")).reset_index()
    g["luck_gap"] = g["wobacon"] - g["xwobacon"]    # + = unlucky for the pitcher
    return g
