"""Clustering of pitch shapes (Gaussian mixture)."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

from .features import SHAPE_FEATURES

SEED = 42


def select_k_gmm(X: np.ndarray, k_range=range(4, 15)) -> pd.DataFrame:
    """BIC and silhouette across k so the choice of k is documented, not assumed."""
    rows = []
    for k in k_range:
        gmm = GaussianMixture(k, covariance_type="full", n_init=5, random_state=SEED).fit(X)
        labels = gmm.predict(X)
        rows.append({"k": k, "bic": gmm.bic(X), "silhouette": silhouette_score(X, labels)})
    return pd.DataFrame(rows)


def fit_pitch_shapes(prof: pd.DataFrame, k: int):
    """Soft-cluster pitch profiles. Returns (profiles with labels, scaler, gmm, X)."""
    scaler = StandardScaler()
    X = scaler.fit_transform(prof[SHAPE_FEATURES])
    gmm = GaussianMixture(k, covariance_type="full", n_init=10, random_state=SEED).fit(X)
    probs = gmm.predict_proba(X)

    out = prof.copy()
    out["shape_cluster"] = probs.argmax(axis=1)
    out["cluster_conf"] = probs.max(axis=1)
    return out, scaler, gmm, X


def name_clusters(prof: pd.DataFrame) -> dict[int, str]:
    """Label each cluster with its dominant Statcast pitch_type (weighted by pitches thrown)."""
    names = {}
    for c, d in prof.groupby("shape_cluster"):
        share = d.groupby("pitch_type")["n"].sum()
        top = share.idxmax()
        names[c] = f"C{c}:{top} ({share[top] / share.sum():.0%})"
    return names

