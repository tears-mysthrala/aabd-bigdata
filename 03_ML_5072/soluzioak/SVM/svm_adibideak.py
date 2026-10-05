# %%
"""Ejemplos literales de la página física 9 del PDF SVM y evaluación separada."""

from __future__ import annotations

import importlib.metadata
import json
from pathlib import Path

import numpy as np
from sklearn.datasets import load_iris
from sklearn.dummy import DummyRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.model_selection import KFold, cross_val_predict, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, SVR

HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()


def adibideak_docente() -> dict:
    """Mismos datos, orden del RNG y parámetros de los dos ejemplos del PDF."""
    X_svc = np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]])
    y_svc = np.array([1, 1, 2, 2])
    clf = make_pipeline(StandardScaler(), SVC(gamma="auto"))
    clf.fit(X_svc, y_svc)

    n_samples, n_features = 10, 5
    rng = np.random.RandomState(0)
    y_svr = rng.randn(n_samples)
    X_svr = rng.randn(n_samples, n_features)
    regr = make_pipeline(StandardScaler(), SVR(C=1.0, epsilon=0.2))
    regr.fit(X_svr, y_svr)
    return {
        "svc": clf,
        "svr": regr,
        "X_svr": X_svr,
        "y_svr": y_svr,
        "svc_accuracy_train": float(clf.score(X_svc, y_svc)),
        "svr_r2_train": float(regr.score(X_svr, y_svr)),
    }


# %%
def orokortzea(adibideak: dict) -> dict:
    """Extensión didáctica explícita: Iris reservado y SVR fuera de muestra."""
    # Iris NO pertenece al ejemplo de cuatro puntos del PDF.
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )
    clf = make_pipeline(StandardScaler(), SVC(gamma="auto"))
    clf.fit(X_train, y_train)
    assert np.allclose(clf.named_steps["standardscaler"].mean_, X_train.mean(axis=0))

    # El scaler se ajusta dentro de cada fold: no observa las filas reservadas.
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    X_reg, y_reg = adibideak["X_svr"], adibideak["y_svr"]
    pipeline = make_pipeline(StandardScaler(), SVR(C=1.0, epsilon=0.2))
    prediction = cross_val_predict(pipeline, X_reg, y_reg, cv=cv)
    baseline = cross_val_predict(DummyRegressor(strategy="mean"), X_reg, y_reg, cv=cv)
    assert np.isfinite(prediction).all() and len(prediction) == len(y_reg)
    return {
        "iris_train_rows": len(y_train),
        "iris_test_rows": len(y_test),
        "iris_accuracy_train": float(clf.score(X_train, y_train)),
        "iris_accuracy_test": float(accuracy_score(y_test, clf.predict(X_test))),
        "svr_cv_folds": 5,
        "svr_cv_rows": len(y_reg),
        "svr_r2_oof": float(r2_score(y_reg, prediction)),
        "svr_mae_oof": float(mean_absolute_error(y_reg, prediction)),
        "dummy_r2_oof": float(r2_score(y_reg, baseline)),
        "dummy_mae_oof": float(mean_absolute_error(y_reg, baseline)),
    }


def ejecutar() -> dict:
    examples = adibideak_docente()
    results = {
        "source": "03_ML_5072/materialak/5072_2_05_SVM.pdf, página física 9",
        "seed_svr_pdf": 0,
        "seed_evaluation": 42,
        "pdf_training": {
            "svc_rows": 4,
            "svc_accuracy": examples["svc_accuracy_train"],
            "svr_rows": 10,
            "svr_r2": examples["svr_r2_train"],
        },
        "educational_extension": orokortzea(examples),
        "versions": {
            p: importlib.metadata.version(p) for p in ["numpy", "scikit-learn", "scipy"]
        },
        "limits": [
            "PDF scores evaluate the same rows used for fit, not generalization.",
            "Iris is an added educational holdout, not a PDF requirement.",
            "SVR has only ten random rows; pooled OOF R2 is unstable.",
            "Moodle task SVM - Ariketa (id 63380) exists; no visible instructions/rubric or due date. No submission made or complete rubric coverage verified.",
        ],
    }
    (HERE / "emaitzak.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return results


if __name__ == "__main__":
    ejecutar()
