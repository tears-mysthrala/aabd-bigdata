"""Regresiones conceptuales: pesos, residuos y pruning; no umbrales arbitrarios."""

import numpy as np

from boosting import adaboost_manual, gradient_manual, xgboost_manual, xgboost_one_tree


def test_ada_second_vote_does_not_fix_all_samples():
    result = adaboost_manual()
    assert np.isclose(result["rounds"][1]["error"], 1 / 3)
    assert np.isclose(result["rounds"][1]["alpha"], np.log(2) / 2)
    assert result["prediction"] == [1, 1, -1, -1]
    assert result["accuracy_train"] == 0.75
    assert all(np.isclose(sum(r["weights"]), 1) for r in result["rounds"])


def test_gb_residuals_and_shrinkage():
    stages = gradient_manual()
    assert np.allclose(stages[0]["residual"], [-10, -8, 8, 10])
    assert np.allclose(stages[1]["prediction"], [35.5, 35.5, 44.5, 44.5])
    assert np.allclose(stages[2]["residual"], [-3.25, -1.25, 1.25, 3.25])
    assert stages[0]["mse"] > stages[1]["mse"] > stages[2]["mse"]


def test_xgb_manual_gain_convention_and_library_pruning():
    manual = xgboost_manual()
    assert manual["score_improvement_pdf"] == {"1": 75.0, "2": 216.0, "3": 75.0}
    assert manual["objective_improvement_half_squared"] == 108.0
    observed = xgboost_one_tree()
    assert np.allclose(observed["0"]["prediction"], manual["prediction"])
    assert "children" in observed["100"]["tree"]
    assert "children" in observed["150"]["tree"]
    assert np.isclose(observed["150"]["tree"]["gain"], 216.0)
    assert "children" not in observed["250"]["tree"]
