"""Ejemplos de los dos PDF de Boosting, con evaluación y cálculos auditables.

Ejecutar desde esta carpeta con uv run --frozen python boosting.py.
Los datos sklearn están incluidos en el paquete: no se descargan datasets.
Sobrescribe resultados propios; no guarda ni carga modelos pickle.
"""

# %% AdaBoost: las dos rondas del ejemplo manual, sin redondeo intermedio.
import json
from importlib.metadata import version
from pathlib import Path

import matplotlib
import numpy as np
from sklearn.datasets import (
    load_diabetes,
    load_iris,
    make_classification,
    make_regression,
)
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingRegressor
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier, XGBRegressor

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()


def adaboost_manual():
    """Reproduce las reglas elegidas en el PDF; no afirma que sean óptimas."""
    y = np.array([1, 1, -1, 1])
    predictions = [np.array([1, 1, -1, -1]), np.array([-1, -1, -1, 1])]
    weights = np.full(4, 0.25)
    margin = np.zeros(4)
    rounds = []
    for pred in predictions:
        error = float(weights[pred != y].sum())
        alpha = float(0.5 * np.log((1 - error) / error))
        weights *= np.exp(-alpha * y * pred)
        weights /= weights.sum()
        margin += alpha * pred
        rounds.append({"error": error, "alpha": alpha, "weights": weights.tolist()})
    return {
        "rounds": rounds,
        "margin": margin.tolist(),
        "prediction": np.sign(margin).astype(int).tolist(),
        "accuracy_train": float(np.mean(np.sign(margin) == y)),
    }


# %% Gradient Boosting manual: media, residuos y dos stumps fijados.
def gradient_manual():
    """Pérdida cuadrática; para otras pérdidas se usan gradientes negativos."""
    y = np.array([30.0, 32.0, 48.0, 50.0])
    prediction = np.full(4, y.mean())
    stages = [
        {
            "prediction": prediction.tolist(),
            "residual": (y - prediction).tolist(),
            "mse": float(mean_squared_error(y, prediction)),
        }
    ]
    for _ in range(2):
        residual = y - prediction
        stump = np.repeat([residual[:2].mean(), residual[2:].mean()], 2)
        prediction += 0.5 * stump
        stages.append(
            {
                "prediction": prediction.tolist(),
                "residual": (y - prediction).tolist(),
                "mse": float(mean_squared_error(y, prediction)),
            }
        )
    return stages


# %% XGBoost manual: separar la puntuación docente de la ganancia del objetivo.
def xgboost_manual():
    """Gradiente pred-y, Hessiano 1; lambda=1, eta=.3 y base_score=40."""
    residual = np.array([-10.0, -8.0, 8.0, 10.0])

    def score(values):
        return float(values.sum() ** 2 / (len(values) + 1))

    scores = {
        str(split): score(residual[:split]) + score(residual[split:]) - score(residual)
        for split in (1, 2, 3)
    }
    outputs = np.repeat([residual[:2].sum() / 3, residual[2:].sum() / 3], 2)
    prediction = 40 + 0.3 * outputs
    return {
        "score_improvement_pdf": scores,
        "objective_improvement_half_squared": scores["2"] / 2,
        "leaf_output": outputs.tolist(),
        "prediction": prediction.tolist(),
        "residual": (np.array([30, 32, 48, 50]) - prediction).tolist(),
    }


# %% Cuatro ejemplos del PDF principal: conservar datos y divisiones.
def examples_pdf():
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    ada = AdaBoostClassifier(
        estimator=DecisionTreeClassifier(max_depth=1), n_estimators=50, random_state=42
    )
    ada.fit(X_train, y_train)
    dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    ada_result = {
        "accuracy_test": float(ada.score(X_test, y_test)),
        "baseline_accuracy_test": float(dummy.score(X_test, y_test)),
        "n_train": len(y_train),
        "n_test": len(y_test),
    }

    X, y = make_regression(random_state=0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    gb = GradientBoostingRegressor(random_state=0).fit(X_train, y_train)
    baseline = DummyRegressor().fit(X_train, y_train)
    gb_result = {
        "r2_test": float(gb.score(X_test, y_test)),
        "mae_test": float(mean_absolute_error(y_test, gb.predict(X_test))),
        "baseline_r2_test": float(baseline.score(X_test, y_test)),
        "n_train": len(y_train),
        "n_test": len(y_test),
    }

    X, y = load_iris(return_X_y=True)
    # El PDF no estratifica. Se conserva su split; no se seleccionan parámetros con test.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    clf = XGBClassifier(n_jobs=2, random_state=42).fit(X_train, y_train)
    iris_result = {
        "accuracy_test": float(accuracy_score(y_test, clf.predict(X_test))),
        "n_train": len(y_train),
        "n_test": len(y_test),
    }

    X, y = load_diabetes(return_X_y=True)
    # Literal del PDF: eval_set es entrenamiento, no validación fuera de muestra.
    reg = XGBRegressor(
        tree_method="hist", eval_metric=mean_absolute_error, n_jobs=2, random_state=0
    )
    reg.fit(X, y, eval_set=[(X, y)], verbose=False)
    diabetes_train = {
        "mae_train": float(mean_absolute_error(y, reg.predict(X))),
        "r2_train": float(reg.score(X, y)),
        "n_train": len(y),
        "n_test": 0,
        "eval_set_is_train": True,
    }
    return {
        "adaboost": ada_result,
        "gradient_boosting": gb_result,
        "xgboost_iris": iris_result,
        "xgboost_diabetes_literal": diabetes_train,
    }


# %% Extensión: test diabetes separado, baseline y parámetros definidos antes.
def diabetes_holdout():
    X, y = load_diabetes(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    models = {
        "baseline": DummyRegressor(),
        "gradient_boosting": GradientBoostingRegressor(random_state=42),
        "xgboost": XGBRegressor(tree_method="hist", n_jobs=2, random_state=42),
    }
    result = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        prediction = model.predict(X_test)
        result[name] = {
            "mae_test": float(mean_absolute_error(y_test, prediction)),
            "r2_test": float(r2_score(y_test, prediction)),
            "n_train": len(y_train),
            "n_test": len(y_test),
        }
    return result


# %% Comprobar una ronda manual con la biblioteca, lambda/eta y pruning.
def xgboost_one_tree():
    X = np.arange(1, 5, dtype=float).reshape(-1, 1)
    y = np.array([30.0, 32.0, 48.0, 50.0])
    result = {}
    for gamma in (0, 100, 150, 250):
        model = XGBRegressor(
            n_estimators=1,
            max_depth=1,
            reg_lambda=1,
            learning_rate=0.3,
            gamma=gamma,
            base_score=40,
            tree_method="hist",
            n_jobs=2,
            random_state=0,
        )
        model.fit(X, y)
        result[str(gamma)] = {
            "prediction": model.predict(X).tolist(),
            "tree": json.loads(
                model.get_booster().get_dump(dump_format="json", with_stats=True)[0]
            ),
        }
    return result


def main():
    results = {
        "versions": {
            name: version(name) for name in ("numpy", "scikit-learn", "xgboost-cpu")
        },
        "manual_ada": adaboost_manual(),
        "manual_gb": gradient_manual(),
        "manual_xgb": xgboost_manual(),
        "pdf_examples": examples_pdf(),
        "diabetes_holdout_extension": diabetes_holdout(),
        "xgb_one_tree": xgboost_one_tree(),
    }
    assert np.allclose(
        results["manual_ada"]["rounds"][0]["weights"], [1 / 6, 1 / 6, 1 / 6, 1 / 2]
    )
    assert np.allclose(
        results["manual_gb"][2]["prediction"], [33.25, 33.25, 46.75, 46.75]
    )
    assert np.allclose(
        results["xgb_one_tree"]["0"]["prediction"], [38.2, 38.2, 41.8, 41.8]
    )
    assert np.allclose(results["xgb_one_tree"]["250"]["prediction"], [40, 40, 40, 40])
    output = ROOT / "resultados"
    output.mkdir(exist_ok=True)
    (output / "emaitzak.json").write_text(
        json.dumps(results, indent=2, allow_nan=False) + "\n"
    )
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    stages = results["manual_gb"]
    axes[0].plot([0, 1, 2], [s["mse"] for s in stages], marker="o")
    axes[0].set(
        xlabel="Iteración GB manual",
        ylabel="MSE entrenamiento",
        title="Reducción observada, cuatro puntos",
    )
    holdout = results["diabetes_holdout_extension"]
    axes[1].bar(list(holdout), [v["mae_test"] for v in holdout.values()])
    axes[1].set(
        ylabel="MAE test diabetes", title="Una división reservada; menor es mejor"
    )
    axes[1].tick_params(axis="x", labelrotation=20)
    fig.tight_layout()
    fig.savefig(output / "boosting.png", dpi=150)
    plt.close(fig)
    print(json.dumps(results, indent=2, allow_nan=False))
    return results


if __name__ == "__main__":
    main()
