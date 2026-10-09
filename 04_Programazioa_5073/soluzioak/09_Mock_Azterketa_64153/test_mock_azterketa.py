"""Verifica limpieza, split/escalado, métricas y validación del mock."""

import numpy as np
import pandas as pd
import pytest
from pydantic import ValidationError

from mock_azterketa import SOURCE, MachineInput, clean_data, fit_and_evaluate


def test_cleaning_preserves_source_and_rejects_invalid_measurements():
    raw = pd.read_csv(SOURCE)
    before = raw.copy(deep=True)
    clean, rejected = clean_data(raw)
    pd.testing.assert_frame_equal(raw, before)
    assert len(clean) + len(rejected) == 100
    assert len(rejected) == 4
    assert clean.tenperatura.between(0, 150).all()
    assert clean.bibrazioa.ge(0).all()
    assert clean.notna().all().all()
    assert set(clean.index).isdisjoint(rejected.index)


def test_split_scaler_and_manual_metrics():
    clean, _ = clean_data(pd.read_csv(SOURCE))
    model, train, test, pred, metrics = fit_and_evaluate(clean)
    assert set(train.makina_id).isdisjoint(test.makina_id)
    scaler = model.named_steps["standardscaler"]
    np.testing.assert_allclose(scaler.mean_, train[["tenperatura", "bibrazioa"]].mean())
    true = test.errorea.to_numpy()
    tp = np.sum((true == 1) & (pred == 1))
    fn = np.sum((true == 1) & (pred == 0))
    assert metrics["tp"] == tp and metrics["fn"] == fn
    assert metrics["recall_class_1"] == pytest.approx(tp / (tp + fn))
    assert metrics["accuracy"] == pytest.approx(np.mean(true == pred))


@pytest.mark.parametrize(
    "values",
    [
        {"tenperatura": -1, "bibrazioa": 2},
        {"tenperatura": 60, "bibrazioa": -1},
        {"tenperatura": 151, "bibrazioa": 2},
        {"tenperatura": float("nan"), "bibrazioa": 2},
        {"tenperatura": 60, "bibrazioa": float("inf")},
        {"tenperatura": 60},
        {"tenperatura": 60, "bibrazioa": 2, "extra": 1},
    ],
)
def test_invalid_api_inputs(values):
    with pytest.raises(ValidationError):
        MachineInput(**values)


def test_valid_api_input_accepts_boundaries():
    assert MachineInput(tenperatura=0, bibrazioa=0).tenperatura == 0
    assert MachineInput(tenperatura=150, bibrazioa=2).tenperatura == 150


def test_single_class_split_fails_with_explicit_message():
    clean, _ = clean_data(pd.read_csv(SOURCE))
    clean["errorea"] = 0
    with pytest.raises(ValueError, match="ambas clases"):
        fit_and_evaluate(clean)
