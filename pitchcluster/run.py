"""Pitch-shape clustering: data -> features -> clusters -> figure + tables.

Usage:  python -m pitchcluster.run [year] [--k N]
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .cluster import fit_pitch_shapes, name_clusters, select_k_gmm
from .data import load_season
from .features import SHAPE_FEATURES, pitch_profiles

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"
OUT = ROOT / "outputs"


def _order(names):
    """Cluster names like "C10:SL (91%)" sorted by cluster index, not by string."""
    return sorted(set(names), key=lambda s: int(s.split(":")[0][1:]))


LEGEND_TITLE = "cluster: most common Statcast\ntype (% of members with that label)"


def main(year: int, k: int | None) -> None:
    FIG.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid")

    raw = load_season(year)
    prof = pitch_profiles(raw)
    print(f"{len(prof)} pitcher-pitch profiles from {prof['pitcher'].nunique()} pitchers")

    # --- 1. Choose k --------------------------------------------------------
    from sklearn.preprocessing import StandardScaler
    Xs = StandardScaler().fit_transform(prof[SHAPE_FEATURES])
    sel = select_k_gmm(Xs)
    sel.to_csv(OUT / "k_selection.csv", index=False)
    if k is None:
        k = int(sel.loc[sel["bic"].idxmin(), "k"])
    print(f"Using k={k} pitch-shape clusters")

    fig, ax = plt.subplots(1, 2, figsize=(10, 3.5))
    ax[0].plot(sel["k"], sel["bic"], marker="o"); ax[0].set(title="BIC (lower is better)", xlabel="k")
    ax[1].plot(sel["k"], sel["silhouette"], marker="o"); ax[1].set(title="Silhouette", xlabel="k")
    fig.tight_layout(); fig.savefig(FIG / "k_selection.png", dpi=150); plt.close(fig)

    # --- 2. Pitch-shape clusters -------------------------------------------
    prof, scaler, gmm, X = fit_pitch_shapes(prof, k)
    names = name_clusters(prof)
    prof["cluster_name"] = prof["shape_cluster"].map(names)

    summary = (prof.groupby("cluster_name")
               .agg(pitches=("n", "sum"), profiles=("n", "size"),
                    velo=("velo", "mean"), spin=("spin", "mean"),
                    hmov=("hmov", "mean"), vmov=("vmov", "mean"),
                    whiff_rate=("whiff_rate", "mean"), rv_per_100=("rv_per_100", "mean"))
               .round(2))
    summary.to_csv(OUT / "pitch_shape_clusters.csv")
    print(summary.to_string())

    # Movement plot (arm-side positive), the picture analysts expect to see.
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.scatterplot(data=prof, x="hmov", y="vmov", hue="cluster_name",
                    hue_order=_order(prof["cluster_name"]), s=14, alpha=0.7, ax=ax)
    ax.set(title="Movement profile by cluster (arm-side = +x)",
           xlabel="Horizontal break (in)", ylabel="Induced vertical break (in)")
    ax.legend(fontsize=7, title=LEGEND_TITLE, title_fontsize=7,
              bbox_to_anchor=(1.01, 1), loc="upper left")
    fig.tight_layout(); fig.savefig(FIG / "movement_by_cluster.png", dpi=150); plt.close(fig)

    # Hybrid / ambiguous pitches: low cluster confidence = between archetypes.
    hybrids = prof.nsmallest(25, "cluster_conf")[
        ["player_name", "pitch_type", "cluster_name", "cluster_conf", "velo", "hmov", "vmov",
         "whiff_rate", "rv_per_100"]]
    hybrids.round(2).to_csv(OUT / "hybrid_pitches.csv", index=False)

    # Pitches whose Statcast label disagrees with their shape cluster.
    prof.round(3).to_csv(OUT / "pitch_profiles_labeled.csv", index=False)

    print(f"Done. Tables in {OUT}, figures in {FIG}")


if __name__ == "__main__":
    args = sys.argv[1:]
    k = int(args[args.index("--k") + 1]) if "--k" in args else None
    nums = [a for a in args if a.isdigit() and len(a) == 4]
    main(int(nums[0]) if nums else 2024, k)


