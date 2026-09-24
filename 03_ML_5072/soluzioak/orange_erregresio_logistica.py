"""UCI WDBC one-feature logistic regression with Orange and out-of-fold outputs."""
from __future__ import annotations

import csv
import json
import warnings
from pathlib import Path

import numpy as np
import Orange
from Orange.classification import LogisticRegressionLearner
from Orange.evaluation import CrossValidation
from Orange.preprocess import Continuize, Normalize, RemoveNaNColumns, SklImpute
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, confusion_matrix,
    f1_score, precision_score, recall_score, roc_auc_score,
)

# Orange 3.40 passes legacy sklearn parameters; suppress only their deprecation
# notices while leaving convergence and data warnings visible.
warnings.filterwarnings("ignore", message="'penalty' was deprecated.*", category=FutureWarning)
warnings.filterwarnings("ignore", message="'n_jobs' has no effect.*", category=FutureWarning)

AUTHOR = "Unai Urzainqui Perez"
HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "datos" / "breast_cancer_wisconsin"
DATA_PATH = DATA_DIR / "wdbc_texture_mean.tab"
PREDICTIONS_PATH = DATA_DIR / "wdbc_cv_predicciones.csv"
CURVE_PATH = DATA_DIR / "wdbc_sigmoide_ajuste_completo.csv"
METRICS_PATH = DATA_DIR / "wdbc_cv_metricas.json"


def main() -> dict:
    data = Orange.data.Table(str(DATA_PATH))
    classes = tuple(data.domain.class_var.values)
    if len(data) != 569 or [v.name for v in data.domain.attributes] != ["texture_mean"]:
        raise ValueError("The Orange table must contain all 569 rows and only texture_mean as feature")
    if set(classes) != {"B", "M"}:
        raise ValueError(f"Unexpected diagnosis levels: {classes}")
    if np.isnan(data.X).any() or np.isnan(data.Y).any():
        raise ValueError("WDBC data has unexpected missing values")

    learner = LogisticRegressionLearner(
        penalty="l2", C=1.0, class_weight=None, random_state=42, max_iter=1000,
        preprocessors=[Continuize(), Normalize(), RemoveNaNColumns(), SklImpute()],
    )
    learner.name = "Logistic Regression (texture_mean)"
    evaluation = CrossValidation(k=10, stratified=True, random_state=42, store_data=True)(data, [learner])

    indices = np.asarray(evaluation.row_indices, dtype=int)
    order = np.argsort(indices)
    indices = indices[order]
    y_code = np.asarray(evaluation.actual, dtype=int).reshape(-1)[order]
    pred_code = np.asarray(evaluation.predicted[0], dtype=int).reshape(-1)[order]
    probs = np.asarray(evaluation.probabilities, dtype=float)
    if probs.ndim == 3:
        probs = probs[0]
    probs = probs[order]
    malignant_idx = classes.index("M")
    y = np.asarray([classes[i] for i in y_code])
    predicted = np.asarray([classes[i] for i in pred_code])
    p_malignant = probs[:, malignant_idx]
    p_safe = np.clip(p_malignant, np.finfo(float).eps, 1 - np.finfo(float).eps)
    logit_score = np.log(p_safe / (1 - p_safe))
    actual_malignant = y == "M"
    predicted_malignant = predicted == "M"
    tn, fp, fn, tp = confusion_matrix(actual_malignant, predicted_malignant, labels=[False, True]).ravel()
    texture = np.asarray(data.X[indices, 0], dtype=float)
    sample_ids = [str(x) for x in data.metas[indices, 0]]

    # Fit the same Orange learner to all rows only to draw the descriptive sigmoid.
    full_model = learner(data)
    full_probabilities = np.asarray(full_model(data, Orange.classification.Model.Probs))[:, malignant_idx]
    full_safe = np.clip(full_probabilities, np.finfo(float).eps, 1 - np.finfo(float).eps)
    full_logit_score = np.log(full_safe / (1 - full_safe))
    texture_grid = np.linspace(float(np.min(data.X[:, 0])), float(np.max(data.X[:, 0])), 400)
    curve_domain = Orange.data.Domain(data.domain.attributes, data.domain.class_var)
    grid_table = Orange.data.Table.from_numpy(
        curve_domain, X=texture_grid.reshape(-1, 1), Y=np.zeros(len(texture_grid)),
    )
    curve_probs = np.asarray(full_model(grid_table, Orange.classification.Model.Probs))[:, malignant_idx]
    curve_safe = np.clip(curve_probs, np.finfo(float).eps, 1 - np.finfo(float).eps)
    curve_logit_score = np.log(curve_safe / (1 - curve_safe))
    crossings = np.flatnonzero(curve_probs >= 0.5)
    threshold_texture = float(texture_grid[crossings[0]]) if len(crossings) else None

    benign_texture = texture[y == "B"]
    malignant_texture = texture[y == "M"]
    metrics = {
        "creator": AUTHOR,
        "dataset": "UCI Breast Cancer Wisconsin (Diagnostic)",
        "dataset_doi": "10.24432/C5DW2B",
        "rows": len(data),
        "feature_count_in_model": 1,
        "predictor": "texture_mean",
        "predictor_definition": "standard deviation of gray-scale values in the cell nucleus image region",
        "target": "diagnosis",
        "classes": list(classes),
        "positive_class": "M (malignant)",
        "class_counts": {"B (benign)": int((y == "B").sum()), "M (malignant)": int((y == "M").sum())},
        "texture_mean_by_class": {"B": float(benign_texture.mean()), "M": float(malignant_texture.mean())},
        "full_data_threshold_texture_mean": threshold_texture,
        "model": "Orange LogisticRegressionLearner; L2; C=1; one predictor texture_mean",
        "evaluation": "10-fold stratified cross-validation; random_state=42; out-of-fold predictions",
        "threshold_for_cv_classes": 0.5,
        "accuracy": float(accuracy_score(y, predicted)),
        "balanced_accuracy": float(balanced_accuracy_score(y, predicted)),
        "roc_auc": float(roc_auc_score(actual_malignant, p_malignant)),
        "precision_malignant": float(precision_score(actual_malignant, predicted_malignant, zero_division=0)),
        "recall_malignant": float(recall_score(actual_malignant, predicted_malignant, zero_division=0)),
        "f1_malignant": float(f1_score(actual_malignant, predicted_malignant, zero_division=0)),
        "confusion_matrix": {"tn_benign": int(tn), "fp_benign_as_malignant": int(fp), "fn_malignant_as_benign": int(fn), "tp_malignant": int(tp)},
        "predictions_file": PREDICTIONS_PATH.name,
        "curve_file": CURVE_PATH.name,
        "medical_use": "educational only; not for clinical decisions",
    }
    with PREDICTIONS_PATH.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["sample_id", "texture_mean", "logit_score_z_cv", "logit_score_full_fit", "diagnosis_observed", "diagnosis_cv_predicted", "probability_malignant_cv", "probability_malignant_full_fit", "correct_at_0_5"])
        writer.writerows(
            (sid, f"{x:.5f}", f"{z_cv:.12f}", f"{z_full:.12f}", actual, predicted_, f"{prob_cv:.12f}", f"{prob_full:.12f}", str(actual == predicted_).lower())
            for sid, x, z_cv, z_full, actual, predicted_, prob_cv, prob_full in zip(sample_ids, texture, logit_score, full_logit_score, y, predicted, p_malignant, full_probabilities)
        )
    with CURVE_PATH.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["logit_score_z", "probability_malignant_full_data_fit"])
        writer.writerows((f"{z:.12f}", f"{p:.12f}") for z, p in zip(curve_logit_score, curve_probs))
    METRICS_PATH.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    main()
