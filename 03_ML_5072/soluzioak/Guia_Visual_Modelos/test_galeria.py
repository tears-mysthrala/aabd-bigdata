"""Recalcula métricas desde predicciones y verifica ausencia de fuga al escalar."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from generar import dataset, examples

HERE = Path(__file__).resolve().parent


@pytest.mark.parametrize("task", ["clasificacion", "regresion"])
def test_split_and_metrics_from_predictions(task):
    report = json.loads((HERE / "metricas.json").read_text())
    source = HERE / "datos" / f"{task}.csv"
    assert (
        hashlib.sha256(source.read_bytes()).hexdigest()
        == report["datasets"][task]["sha256"]
    )
    frame = pd.read_csv(source, index_col="id")
    train = set(frame.index[frame["split"] == "train"])
    test = set(frame.index[frame["split"] == "test"])
    assert train.isdisjoint(test) and train | test == set(frame.index)
    records = [r for r in report["models"] if r["task"] == task]
    assert len(records) == 10
    for record in records:
        pred = pd.read_csv(HERE / "datos" / record["predictions"])
        assert pred["id"].is_unique and set(pred["id"]) == test
        np.testing.assert_allclose(pred["y_true"], frame.loc[pred["id"], "y"])
        true, estimated = pred["y_true"].to_numpy(), pred["y_pred"].to_numpy()
        metrics = record["metrics"]
        if task == "clasificacion":
            assert metrics["accuracy_test"] == pytest.approx(np.mean(true == estimated))
            matrix = [
                [int(np.sum((true == a) & (estimated == b))) for b in (0, 1)]
                for a in (0, 1)
            ]
            assert metrics["confusion_matrix"] == matrix
            _tn, fp, fn, tp = np.array(matrix).ravel()
            assert metrics["f1_test"] == pytest.approx(2 * tp / (2 * tp + fp + fn))
        else:
            residual = true - estimated
            assert metrics["mae_test"] == pytest.approx(np.mean(np.abs(residual)))
            assert metrics["rmse_test"] == pytest.approx(np.sqrt(np.mean(residual**2)))
            assert metrics["r2_test"] == pytest.approx(
                1 - np.sum(residual**2) / np.sum((true - true.mean()) ** 2)
            )


def test_scalers_fit_training_only():
    for example in examples():
        if not isinstance(example.model, Pipeline):
            continue
        X, y, train, test = dataset(example.task)
        example.model.fit(X[train], y[train])
        scaler = example.model.named_steps["standardscaler"]
        features = X[train]
        if "polynomialfeatures" in example.model.named_steps:
            features = example.model.named_steps["polynomialfeatures"].transform(
                features
            )
        assert scaler.n_samples_seen_ == len(train)
        np.testing.assert_allclose(scaler.mean_, features.mean(axis=0))
        assert len(test) > 0


def test_original_hashes_and_practice_links():
    provenance = json.loads((HERE / "originales" / "PROCEDENCIA.json").read_text())
    for item in provenance["files"]:
        assert (
            hashlib.sha256(
                (HERE / "originales" / item["file"]).read_bytes()
            ).hexdigest()
            == item["sha256"]
        )
    for record in json.loads((HERE / "metricas.json").read_text())["models"]:
        assert (HERE / record["lesson"]).is_file()
        assert (HERE / "figuras" / record["filename"]).is_file()
