"""Anomalia-detektzioa (IsolationForest) + fusioa arrisku lausoarekin.

Ezaugarriak: tenperatura, bibrazioa, presioa + ingeniaritza (txv, t2),
makina one-hot gabe (anomalia fisikoa da, ez makina-menpekoa).
Determinista: random_state finkoa. Ez du gaitasun prediktiborik ziurtatzen:
ebaluazioa holdout-ean neurtzen da (CNC_Guard.ipynb).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

FEATS = ["tenperatura", "bibrazioa", "presioa", "txv", "t2"]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Ezaugarri numerikoak + ingeniaritza (txv, t2)."""
    out = df[["tenperatura", "bibrazioa", "presioa"]].astype("float32").copy()
    out["txv"] = out["tenperatura"] * out["bibrazioa"]
    out["t2"] = out["tenperatura"] ** 2
    return out[FEATS]


def fit_anomaly(
    X: pd.DataFrame, contamination: float = 0.012, seed: int = 42
) -> tuple[IsolationForest, StandardScaler, float, float]:
    """Entrena IsolationForest; devuelve (modelo, scaler, min, max de decision en train)."""
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    model = IsolationForest(
        n_estimators=200, contamination=contamination, random_state=seed, n_jobs=-1
    )
    model.fit(Xs)
    dec = model.decision_function(Xs)
    return model, scaler, float(dec.min()), float(dec.max())


def anomaly_score(
    model: IsolationForest, scaler: StandardScaler, X: pd.DataFrame, dmin: float, dmax: float
) -> np.ndarray:
    """Anomalia-puntuazioa [0, 1] (1 = anomalia handiena), train min/max-ekin normalizatua."""
    dec = model.decision_function(scaler.transform(X))
    norm = (dec - dmin) / (dmax - dmin) if dmax > dmin else np.zeros_like(dec)
    return np.clip(1.0 - norm, 0.0, 1.0)


def riesgo_final(fuzzy01: float, anomaly01: float) -> float:
    """Fusioa: max (alarma bietako batek piztuz gero). [0, 1]."""
    return float(max(min(fuzzy01, 1.0), min(anomaly01, 1.0)))
