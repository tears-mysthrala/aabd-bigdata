"""UCI Auto MPG: reproducible Orange OLS regression and out-of-fold outputs."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import Orange
from Orange.evaluation import CrossValidation, MAE, MSE, R2, RMSE
from Orange.regression import LinearRegressionLearner


AUTHOR = "Unai Urzainqui Perez"
HERE = Path(__file__).resolve().parent
DATA_PATH = HERE / "datos" / "auto_mpg" / "auto_mpg_weight.tab"
OUTPUT_DIR = HERE / "datos" / "auto_mpg"
PREDICTIONS_PATH = OUTPUT_DIR / "auto_mpg_cv_iragarpenak.csv"
METRICS_PATH = OUTPUT_DIR / "auto_mpg_cv_metrics.json"


def main() -> dict[str, float | int | str]:
    data = Orange.data.Table(str(DATA_PATH))
    assert len(data) == 398
    assert data.domain.class_var.name == "mpg"
    assert [var.name for var in data.domain.attributes] == ["weight"]
    assert not np.isnan(data.X).any() and not np.isnan(data.Y).any()

    learner = LinearRegressionLearner()
    evaluation = CrossValidation(k=10, random_state=42)(data, [learner])
    row_indices = np.asarray(evaluation.row_indices, dtype=int)
    order = np.argsort(row_indices)
    row_indices = row_indices[order]
    y = np.asarray(evaluation.actual, dtype=float).reshape(-1)
    y = y[order]
    y_pred = np.asarray(evaluation.predicted[0], dtype=float).reshape(-1)[order]
    residual = y - y_pred

    # Fit to the full table only to report a readable slope/intercept. The
    # headline error metrics and exported predictions are out-of-fold CV values.
    fitted = learner(data)
    coefficient = float(np.asarray(fitted.coefficients).reshape(-1)[0])
    intercept = float(fitted.intercept)
    weight = np.asarray(data.X[row_indices, 0], dtype=float)
    car_names = [str(value) for value in data.metas[row_indices, 0]]

    metrics = {
        "creator": AUTHOR,
        "dataset": "UCI Auto MPG",
        "dataset_doi": "10.24432/C5859H",
        "rows": len(data),
        "predictor": "weight",
        "predictor_unit": "pounds",
        "target": "mpg",
        "target_unit": "miles per US gallon, city-cycle",
        "model": "Orange LinearRegressionLearner (ordinary least squares)",
        "evaluation": "10-fold cross-validation; random_state=42",
        "cv_r2": float(R2(evaluation)[0]),
        "cv_mse": float(MSE(evaluation)[0]),
        "cv_rmse": float(RMSE(evaluation)[0]),
        "cv_mae": float(MAE(evaluation)[0]),
        "full_data_slope_mpg_per_pound": coefficient,
        "full_data_intercept_mpg": intercept,
        "pearson_r_weight_mpg": float(np.corrcoef(weight, y)[0, 1]),
        "cv_residual_mean_mpg": float(residual.mean()),
        "cv_residual_median_mpg": float(np.median(residual)),
        "cv_residual_95th_percentile_abs_mpg": float(np.quantile(np.abs(residual), 0.95)),
        "cv_predictions_file": PREDICTIONS_PATH.name,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with PREDICTIONS_PATH.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["car_name", "weight_lb", "mpg_observed", "mpg_cv_predicted", "cv_residual"])
        writer.writerows(
            (name, f"{x:.1f}", f"{actual:.3f}", f"{pred:.3f}", f"{err:.3f}")
            for name, x, actual, pred, err in zip(car_names, weight, y, y_pred, residual)
        )
    METRICS_PATH.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")

    print(f"Creator: {AUTHOR}")
    print(f"Dataset: UCI Auto MPG; {len(data)} rows; mpg ~ weight (lb)")
    print(f"OLS equation on all rows: mpg = {intercept:.4f} {coefficient:+.6f} * weight_lb")
    print(f"10-fold CV: R2={metrics['cv_r2']:.4f}, RMSE={metrics['cv_rmse']:.3f} mpg, MAE={metrics['cv_mae']:.3f} mpg")
    print(f"Out-of-fold predictions: {PREDICTIONS_PATH}")
    print(f"Metrics: {METRICS_PATH}")
    return metrics


if __name__ == "__main__":
    main()
