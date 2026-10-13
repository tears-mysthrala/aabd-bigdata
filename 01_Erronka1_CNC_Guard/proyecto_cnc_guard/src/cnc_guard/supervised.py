"""Supervised CNC fault classification on synthetic, same-instant labels.

No claims of future failure forecasting or plant reliability. Features include
only the current sensors and past sensor values of the *same* machine.
"""
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import TimeSeriesSplit

COLUMNS = ("ts", "makina_id", "tenperatura", "bibrazioa", "presioa", "errorea")
FEATURES = (
    "tenperatura", "bibrazioa", "presioa", "txv", "t2",
    "temp_prev3", "vib_prev3", "delta_temp",
)
SEED = 42


def features_for_reading(
    temperature: float, vibration: float, pressure: float,
    history: list[dict] | None = None,
) -> dict[str, float]:
    """Online equivalent of the batch feature calculation.

    history must contain at most the three most recent *earlier* readings,
    in chronological order, for the same machine. Never use future samples.
    """
    history = history or []
    if len(history) > 3:
        raise ValueError("history accepts up to 3 prior readings")
    return {
        "tenperatura": temperature,
        "bibrazioa": vibration,
        "presioa": pressure,
        "txv": temperature * vibration,
        "t2": temperature**2,
        "temp_prev3": float(np.mean([v["temperature"] for v in history]))
        if history else temperature,
        "vib_prev3": float(np.mean([v["vibration"] for v in history]))
        if history else vibration,
        "delta_temp": temperature - history[-1]["temperature"] if history else 0.0,
    }


def prepare_frame(data: pd.DataFrame) -> pd.DataFrame:
    """Validate required fields, sort in time and create past-only features."""
    missing = set(COLUMNS) - set(data.columns)
    if missing:
        raise ValueError(f"Missing CSV columns: {sorted(missing)}")
    df = data.copy()
    for col in ("tenperatura", "bibrazioa", "presioa", "errorea", "ts"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["makina_id"] = df["makina_id"].astype("string")
    df = df.dropna(subset=list(COLUMNS))
    df = df.loc[
        df["errorea"].isin([0, 1])
        & df["tenperatura"].between(-40, 200)
        & df["bibrazioa"].between(0, 100)
        & df["presioa"].between(0, 5000)
    ].copy()
    if df.empty:
        raise ValueError("No usable rows")
    if df.duplicated(["makina_id", "ts"]).any():
        raise ValueError("Duplicate machine/timestamp records; resolve before training")
    df = df.sort_values(["ts", "makina_id"], kind="stable").reset_index(drop=True)
    grouped = df.groupby("makina_id", sort=False, observed=True)
    for source, destination in (("tenperatura", "temp_prev3"), ("bibrazioa", "vib_prev3")):
        df[destination] = grouped[source].transform(
            lambda s: s.shift(1).rolling(3, min_periods=1).mean()
        ).fillna(df[source])
    prev_temp = grouped["tenperatura"].shift(1)
    df["delta_temp"] = (df["tenperatura"] - prev_temp).fillna(0.0)
    df["txv"] = df["tenperatura"] * df["bibrazioa"]
    df["t2"] = df["tenperatura"] ** 2
    return df


def _quality(y: np.ndarray, scores: np.ndarray, threshold: float) -> dict:
    pred = scores >= threshold
    result = {
        "threshold": float(threshold),
        "confusion_matrix": confusion_matrix(y, pred, labels=[0, 1]).tolist(),
        "precision": float(precision_score(y, pred, zero_division=0)),
        "recall": float(recall_score(y, pred, zero_division=0)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "positives": int(np.sum(y == 1)),
        "examples": int(len(y)),
    }
    if len(np.unique(y)) == 2:
        result["roc_auc"] = float(roc_auc_score(y, scores))
        result["average_precision"] = float(average_precision_score(y, scores))
    else:
        result["roc_auc"] = None
        result["average_precision"] = None
    return result


def _f2(y: np.ndarray, score: np.ndarray, cutoff: float) -> float:
    pred = score >= cutoff
    precision = precision_score(y, pred, zero_division=0)
    recall = recall_score(y, pred, zero_division=0)
    return float(5 * precision * recall / (4 * precision + recall)) if precision + recall else 0.0


def train(data: pd.DataFrame, *, trees: int = 120) -> tuple[dict, dict]:
    df = prepare_frame(data)
    if len(df) < 80:
        raise ValueError("At least 80 valid observations are required")
    # Chronological split; machine history uses only sensors at earlier times.
    n = len(df)
    first, second = int(n * 0.6), int(n * 0.8)
    train_df, val_df, test_df = df.iloc[:first], df.iloc[first:second], df.iloc[second:]
    xtrain, ytrain = train_df[list(FEATURES)], train_df["errorea"].to_numpy(dtype=int)
    if len(np.unique(ytrain)) < 2:
        raise ValueError("Training segment must contain both target classes")
    forest = RandomForestClassifier(
        n_estimators=trees, class_weight="balanced_subsample",
        min_samples_leaf=3, max_depth=12, random_state=SEED, n_jobs=1,
    )
    forest.fit(xtrain, ytrain)
    vscores = forest.predict_proba(val_df[list(FEATURES)])[:, 1]
    candidates = (0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7)
    selected = max(candidates, key=lambda p: (_f2(val_df["errorea"].to_numpy(), vscores, p), -p))
    tscores = forest.predict_proba(test_df[list(FEATURES)])[:, 1]
    metrics = {
        "label_definition": "Same-instant synthetic errorea, NOT failure within 24h",
        "sample_count": n,
        "observed_failure_rate": float(df["errorea"].mean()),
        "split": {"train": len(train_df), "validation": len(val_df), "test": len(test_df),
                  "method": "global chronological 60/20/20"},
        "validation_selected_binary_threshold": selected,
        "validation": _quality(val_df["errorea"].to_numpy(dtype=int), vscores, selected),
        "test": _quality(test_df["errorea"].to_numpy(dtype=int), tscores, selected),
        "test_at_0_15": _quality(test_df["errorea"].to_numpy(dtype=int), tscores, 0.15),
        "feature_importance": dict(zip(FEATURES, map(float, forest.feature_importances_), strict=True)),
        "caveats": ["Synthetic sensor-dependent target and random noise",
                    "No measured industrial early warning", "Single sampled time period"],
    }
    if len(train_df) >= 90 and int(np.sum(ytrain)) >= 3:
        cv = []
        for tr, va in TimeSeriesSplit(n_splits=3).split(xtrain):
            if len(np.unique(ytrain[tr])) < 2 or len(np.unique(ytrain[va])) < 2:
                continue
            candidate = RandomForestClassifier(
                n_estimators=min(trees, 40), max_depth=12,
                min_samples_leaf=3, class_weight="balanced_subsample",
                random_state=SEED, n_jobs=1,
            )
            candidate.fit(xtrain.iloc[tr], ytrain[tr])
            ps = candidate.predict_proba(xtrain.iloc[va])[:, 1]
            cv.append(_quality(ytrain[va], ps, selected)["recall"])
        metrics["train_time_series_cv_recall"] = cv
    bundle = {
        "model": forest, "features": list(FEATURES),
        "model_schema": 1, "trained_at_utc": datetime.now(UTC).isoformat(),
        "binary_threshold": selected,
        "alert_thresholds": {"warning": 0.15, "critical": 0.7},
        "history_size": 3,
    }
    return bundle, metrics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--metrics", type=Path, required=True)
    parser.add_argument("--max-rows", type=int, default=50_000)
    args = parser.parse_args()
    if args.max_rows < 80:
        parser.error("--max-rows must be >= 80")
    # Explicit cap prevents accidentally loading the full 10M-row CSV into RAM.
    df = pd.read_csv(args.csv, nrows=args.max_rows)
    bundle, metrics = train(df)
    for path in (args.out, args.metrics):
        path.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists() or args.metrics.exists():
        parser.error("Output exists; choose fresh paths to preserve prior evidence")
    joblib.dump(bundle, args.out)
    args.metrics.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"model": str(args.out), "metrics": str(args.metrics),
                      "test": metrics["test"]}, indent=2))


if __name__ == "__main__":
    main()
