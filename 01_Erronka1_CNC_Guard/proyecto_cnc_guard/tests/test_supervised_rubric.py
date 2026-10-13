"""Regression tests for chronology, label correctness and serving feature parity."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from cnc_guard.supervised import FEATURES, features_for_reading, prepare_frame, train


def sample(n=240):
    rng = np.random.default_rng(42)
    t = rng.normal(65, 5, n)
    v = rng.normal(3, 0.8, n).clip(0.1)
    y = ((t > 67) & (v > 3)).astype(int)
    return pd.DataFrame(
        {
            "ts": np.arange(n) * 30 + 1700000000,
            "makina_id": np.where(np.arange(n) % 2 == 0, "M1", "M2"),
            "tenperatura": t,
            "bibrazioa": v,
            "presioa": 1012.0 - 0.1 * t,
            "errorea": y,
        }
    )


def test_history_never_uses_future_or_other_machine():
    data = sample(12)
    df = prepare_frame(data)
    row = df.iloc[6]
    machine_past = df.loc[(df["makina_id"] == row["makina_id"]) & (df["ts"] < row["ts"])].tail(3)
    history = [
        {"temperature": float(item["tenperatura"]), "vibration": float(item["bibrazioa"])}
        for _, item in machine_past.iterrows()
    ]
    online = features_for_reading(
        float(row["tenperatura"]), float(row["bibrazioa"]), float(row["presioa"]), history
    )
    for col in FEATURES:
        assert online[col] == pytest.approx(float(row[col]))


def test_duplicate_timestamp_rejected():
    data = sample(100)
    with pytest.raises(ValueError, match="Duplicate"):
        prepare_frame(pd.concat([data, data.iloc[[0]]], ignore_index=True))


def test_missing_sensor_and_invalid_label_do_not_pass():
    with pytest.raises(ValueError, match="Missing"):
        prepare_frame(sample(100).drop(columns=["presioa"]))
    df = sample(100)
    df["errorea"] = 7
    with pytest.raises(ValueError, match="No usable"):
        prepare_frame(df)


def test_training_has_temporal_holdout_and_metrics():
    bundle, metrics = train(sample())
    assert bundle["features"] == list(FEATURES)
    assert metrics["split"]["test"] > 0
    assert metrics["test"]["examples"] == metrics["split"]["test"]
    assert metrics["label_definition"].startswith("Same-instant")
    assert len(metrics["test"]["confusion_matrix"]) == 2
