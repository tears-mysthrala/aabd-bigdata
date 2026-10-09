# %% [markdown]
# # Guía visual reproducible de modelos
# Objetivo: relacionar fronteras y curvas con el mecanismo de cada algoritmo.
# Los datos son sintéticos: dos medias lunas para clasificación y una curva
# con ruido para regresión. No son datos de fábrica ni una competición entre
# algoritmos. Todos los modelos de una tarea usan exactamente el mismo split.
# El preprocesado se aprende únicamente en train; test solo evalúa.
# Ejecutar desde esta carpeta con `uv sync --frozen` y
# `MPLBACKEND=Agg uv run --frozen python generar.py`.
# Sobrescribe solo figuras/, datos/, metricas.json e index.html de esta guía.
# No modifica originales/, no descarga datos ni carga modelos externos.

# %%
import hashlib
import html
import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
import xgboost
from matplotlib.colors import ListedColormap
from sklearn.datasets import make_moons
from sklearn.ensemble import (
    AdaBoostClassifier,
    AdaBoostRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import Lasso, LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from xgboost import XGBClassifier, XGBRegressor

HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
SEED = 42
BLUE, ORANGE = "#2459a8", "#b64f15"


@dataclass
class Example:
    task: str
    key: str
    name: str
    model: object
    explanation: str
    look: str
    lesson: str


def signal(x):
    return 0.2 * x**2 + np.sin(1.7 * x)


def dataset(task):
    if task == "clasificacion":
        X, y = make_moons(n_samples=320, noise=0.22, random_state=SEED)
        stratify = y
    else:
        rng = np.random.default_rng(SEED)
        X = rng.uniform(-3.5, 3.5, (240, 1))
        y = signal(X[:, 0]) + rng.normal(0, 0.25, len(X))
        stratify = None
    train, test = train_test_split(
        np.arange(len(X)), test_size=0.3, random_state=SEED, stratify=stratify
    )
    return X, y, train, test


def examples():
    def scale(model):
        return make_pipeline(StandardScaler(), model)

    def poly(model):
        return make_pipeline(
            PolynomialFeatures(degree=5, include_bias=False), StandardScaler(), model
        )

    c = "clasificacion"
    r = "regresion"
    return [
        Example(
            c,
            "logistica",
            "Regresión logística",
            scale(LogisticRegression(max_iter=1000)),
            "Modela P(clase 1) con una sigmoide sobre una combinación lineal.",
            "La frontera es recta aunque los datos formen medias lunas. El fondo muestra clase, no probabilidad.",
            "../Iris_LogReg_KNN/README.md",
        ),
        Example(
            c,
            "knn",
            "KNN · k=5",
            scale(KNeighborsClassifier(n_neighbors=5)),
            "Vota entre los cinco vecinos más cercanos en el espacio escalado.",
            "La frontera sigue detalles locales; cambiar k cambia cuánto se suaviza.",
            "../Iris_LogReg_KNN/README.md",
        ),
        Example(
            c,
            "svm-lineal",
            "SVM lineal",
            scale(SVC(kernel="linear", C=1)),
            "Busca una separación lineal con margen y penalización C.",
            "Una recta no sigue la curvatura de las medias lunas. No se dibuja aquí el margen.",
            "../SVM/README.md",
        ),
        Example(
            c,
            "svm-rbf",
            "SVM · kernel RBF",
            scale(SVC(kernel="rbf", C=1, gamma="scale")),
            "El kernel RBF permite una frontera no lineal; C y gamma controlan el ajuste.",
            "La separación curva puede seguir la forma de los datos.",
            "../SVM/README.md",
        ),
        Example(
            c,
            "arbol",
            "Árbol de decisión",
            DecisionTreeClassifier(max_depth=4, random_state=SEED),
            "Construye reglas mediante cortes sobre una variable cada vez.",
            "Los bordes son horizontales o verticales; profundidad limitada a cuatro.",
            "../Entregas_Moodle_2026-10-05/63544_Arbol_Decision/README.md",
        ),
        Example(
            c,
            "forest",
            "Random Forest",
            RandomForestClassifier(
                n_estimators=200, max_depth=6, random_state=SEED, n_jobs=1
            ),
            "Agrega probabilidades de árboles entrenados con bootstrap y selección de atributos.",
            "Muchos cortes se combinan; su frontera puede seguir siendo irregular.",
            "../Entregas_Moodle_2026-10-05/63386_Random_Forest/README.md",
        ),
        Example(
            c,
            "naive-bayes",
            "Naive Bayes gaussiano",
            GaussianNB(),
            "Supone independencia condicional y distribución gaussiana por variable y clase.",
            "Este ejemplo continuo no es MultinomialNB: la variante de texto docente utiliza conteos.",
            "../README.md",
        ),
        Example(
            c,
            "adaboost",
            "AdaBoost",
            AdaBoostClassifier(
                estimator=DecisionTreeClassifier(max_depth=1),
                n_estimators=100,
                learning_rate=0.8,
                random_state=SEED,
            ),
            "Combina clasificadores débiles y aumenta el peso de observaciones mal clasificadas.",
            "Stumps sucesivos forman una frontera más compleja que un solo corte.",
            "../Boosting/README.md",
        ),
        Example(
            c,
            "gradient-boosting",
            "Gradient Boosting",
            GradientBoostingClassifier(
                n_estimators=100, max_depth=2, learning_rate=0.1, random_state=SEED
            ),
            "Añade árboles para reducir la pérdida siguiendo su gradiente.",
            "Es una construcción secuencial; no equivale al bagging de Random Forest.",
            "../Boosting/README.md",
        ),
        Example(
            c,
            "xgboost",
            "XGBoost",
            XGBClassifier(
                n_estimators=100,
                max_depth=3,
                learning_rate=0.1,
                reg_lambda=1,
                n_jobs=1,
                random_state=SEED,
                tree_method="hist",
                eval_metric="logloss",
            ),
            "Boosting de árboles con regularización y optimización mediante gradientes y Hessianos.",
            "Otra configuración y profundidad: una mejor métrica aquí no demuestra superioridad universal.",
            "../Boosting/README.md",
        ),
        Example(
            r,
            "lineal",
            "Regresión lineal",
            LinearRegression(),
            "Ajusta una recta minimizando la suma de errores cuadrados.",
            "La recta no reproduce las oscilaciones de esta señal sintética.",
            "../README.md",
        ),
        Example(
            r,
            "ridge",
            "Ridge · polinomio grado 5",
            poly(Ridge(alpha=1)),
            "Penaliza con L2 los coeficientes de los términos polinómicos escalados.",
            "La curva proviene de la expansión polinómica; Ridge por sí solo es lineal en sus atributos.",
            "../README.md",
        ),
        Example(
            r,
            "lasso",
            "Lasso · polinomio grado 5",
            poly(Lasso(alpha=0.02, max_iter=20000)),
            "La penalización L1 puede dejar algunos coeficientes exactamente en cero.",
            "Se usa la misma expansión y escalado que Ridge; comprobar coeficientes, no solo la curva.",
            "../README.md",
        ),
        Example(
            r,
            "knn",
            "KNN Regressor · k=5",
            scale(KNeighborsRegressor(n_neighbors=5)),
            "Promedia el valor observado de cinco vecinos del entrenamiento.",
            "Las predicciones son locales y no extrapolan una tendencia fuera del soporte observado.",
            "../README.md",
        ),
        Example(
            r,
            "svr-rbf",
            "SVR · kernel RBF",
            scale(SVR(C=10, epsilon=0.1, gamma="scale")),
            "Ajusta una función no lineal con tolerancia epsilon y penalización C.",
            "La banda epsilon forma parte del método, pero no se representa como intervalo de confianza.",
            "../SVM/README.md",
        ),
        Example(
            r,
            "arbol",
            "Árbol de regresión",
            DecisionTreeRegressor(max_depth=4, random_state=SEED),
            "Devuelve la media de los valores de cada hoja.",
            "La curva es escalonada: constante dentro de cada región.",
            "../README.md",
        ),
        Example(
            r,
            "forest",
            "Random Forest Regressor",
            RandomForestRegressor(
                n_estimators=200, max_depth=6, random_state=SEED, n_jobs=1
            ),
            "Promedia predicciones de muchos árboles de regresión.",
            "Los escalones se combinan; fuera del rango de train no aprende una ley de extrapolación.",
            "../README.md",
        ),
        Example(
            r,
            "adaboost",
            "AdaBoost Regressor",
            AdaBoostRegressor(
                estimator=DecisionTreeRegressor(max_depth=3),
                n_estimators=100,
                learning_rate=0.05,
                random_state=SEED,
            ),
            "AdaBoost.R2 repondera muestras y combina predicciones mediante mediana ponderada.",
            "No aplica exactamente la regla de voto del clasificador AdaBoost.",
            "../Boosting/README.md",
        ),
        Example(
            r,
            "gradient-boosting",
            "Gradient Boosting Regressor",
            GradientBoostingRegressor(
                n_estimators=100, max_depth=2, learning_rate=0.1, random_state=SEED
            ),
            "Añade árboles que corrigen residuos para la pérdida cuadrática.",
            "La suma secuencial sigue la señal; learning_rate reduce cada contribución.",
            "../Boosting/README.md",
        ),
        Example(
            r,
            "xgboost",
            "XGBoost Regressor",
            XGBRegressor(
                n_estimators=100,
                max_depth=3,
                learning_rate=0.1,
                reg_lambda=1,
                n_jobs=1,
                random_state=SEED,
                tree_method="hist",
            ),
            "Optimiza una suma regularizada de árboles con información de primer y segundo orden.",
            "La figura usa una configuración fijada antes de evaluar, sin buscar parámetros con test.",
            "../Boosting/README.md",
        ),
    ]


def plot(example, X, y, train, test, destination):
    fig, ax = plt.subplots(figsize=(7.2, 4.9), layout="constrained")
    ax.grid(alpha=0.18)
    if example.task == "clasificacion":
        xlim = (X[:, 0].min() - 0.3, X[:, 0].max() + 0.3)
        ylim = (X[:, 1].min() - 0.3, X[:, 1].max() + 0.3)
        xx, yy = np.meshgrid(np.linspace(*xlim, 180), np.linspace(*ylim, 180))
        zz = example.model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        ax.contourf(
            xx,
            yy,
            zz,
            levels=[-0.5, 0.5, 1.5],
            cmap=ListedColormap(["#e4ebf8", "#f8e9df"]),
        )
        ax.contour(xx, yy, zz, levels=[0.5], colors=["#454545"], linewidths=1)
        for cls, color, marker in [(0, BLUE, "o"), (1, ORANGE, "^")]:
            a, b = train[y[train] == cls], test[y[test] == cls]
            ax.scatter(
                X[a, 0],
                X[a, 1],
                marker=marker,
                s=20,
                facecolors="none",
                edgecolors=color,
                alpha=0.6,
                label=f"Train · clase {cls}",
            )
            ax.scatter(
                X[b, 0],
                X[b, 1],
                marker=marker,
                s=38,
                c=color,
                edgecolors="#222",
                linewidths=0.6,
                label=f"Test · clase {cls}",
            )
        ax.set(
            xlim=xlim,
            ylim=ylim,
            xlabel="Variable sintética X1",
            ylabel="Variable sintética X2",
        )
    else:
        xx = np.linspace(-3.5, 3.5, 400)
        ax.scatter(
            X[train, 0],
            y[train],
            s=20,
            facecolors="none",
            edgecolors="#7d8794",
            alpha=0.6,
            label="Train",
        )
        ax.scatter(X[test, 0], y[test], s=30, c=BLUE, marker="x", label="Test")
        ax.plot(
            xx,
            example.model.predict(xx.reshape(-1, 1)),
            c=ORANGE,
            linewidth=2,
            label="Predicción",
        )
        ax.plot(
            xx,
            signal(xx),
            c="#51545a",
            linestyle="--",
            linewidth=1,
            label="Señal sin ruido",
        )
        ax.set(
            xlim=(-3.5, 3.5),
            ylim=(float(y.min() - 0.5), float(y.max() + 0.5)),
            xlabel="Variable sintética X",
            ylabel="Valor sintético y",
        )
    ax.set_title(example.name, fontsize=13)
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.17),
        ncol=2,
        fontsize=8,
        frameon=False,
    )
    fig.savefig(destination, dpi=140, metadata={"Software": "AABD · generar.py"})
    plt.close(fig)


def generate(output=HERE):
    output = Path(output)
    (output / "figuras").mkdir(parents=True, exist_ok=True)
    (output / "datos").mkdir(exist_ok=True)
    datasets = {task: dataset(task) for task in ("clasificacion", "regresion")}
    metadata = {}
    for task, (X, y, train, test) in datasets.items():
        frame = pd.DataFrame(X, columns=[f"X{i + 1}" for i in range(X.shape[1])])
        frame["y"] = y
        frame["split"] = "train"
        frame.loc[test, "split"] = "test"
        payload = frame.to_csv(index_label="id")
        (output / "datos" / f"{task}.csv").write_text(
            payload, encoding="utf-8", newline=""
        )
        metadata[task] = {
            "train": len(train),
            "test": len(test),
            "features": X.shape[1],
            "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        }
    records = []
    for example in examples():
        X, y, train, test = datasets[example.task]
        example.model.fit(X[train], y[train])
        pred = example.model.predict(X[test])
        if example.task == "clasificacion":
            metrics = {
                "accuracy_test": float(accuracy_score(y[test], pred)),
                "accuracy_train": float(
                    accuracy_score(y[train], example.model.predict(X[train]))
                ),
                "f1_test": float(f1_score(y[test], pred)),
                "confusion_matrix": confusion_matrix(
                    y[test], pred, labels=[0, 1]
                ).tolist(),
            }
        else:
            metrics = {
                "r2_test": float(r2_score(y[test], pred)),
                "r2_train": float(r2_score(y[train], example.model.predict(X[train]))),
                "mae_test": float(mean_absolute_error(y[test], pred)),
                "rmse_test": float(np.sqrt(mean_squared_error(y[test], pred))),
            }
        filename = f"{example.task}_{example.key}.png"
        plot(example, X, y, train, test, output / "figuras" / filename)
        predictions = f"{example.task}_{example.key}.csv"
        pd.DataFrame({"id": test, "y_true": y[test], "y_pred": pred}).to_csv(
            output / "datos" / predictions, index=False
        )
        records.append(
            {
                "task": example.task,
                "key": example.key,
                "name": example.name,
                "filename": filename,
                "predictions": predictions,
                "metrics": metrics,
                "parameters": str(example.model),
                "explanation": example.explanation,
                "look": example.look,
                "lesson": example.lesson,
            }
        )
    result = {
        "source": "synthetic; make_moons(noise=0.22) and 0.2*x^2+sin(1.7*x)+Gaussian noise(sigma=0.25)",
        "seed": SEED,
        "test_fraction": 0.3,
        "datasets": metadata,
        "versions": {
            "numpy": np.__version__,
            "sklearn": sklearn.__version__,
            "xgboost": xgboost.__version__,
            "matplotlib": matplotlib.__version__,
        },
        "models": records,
    }
    (output / "metricas.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    cards = []
    for record in records:
        metrics = record["metrics"]
        if record["task"] == "clasificacion":
            text = f"Accuracy test {metrics['accuracy_test']:.3f} · train {metrics['accuracy_train']:.3f} · F1 test {metrics['f1_test']:.3f}"
        else:
            text = f"R² test {metrics['r2_test']:.3f} · train {metrics['r2_train']:.3f} · RMSE test {metrics['rmse_test']:.3f}"
        esc = html.escape
        cards.append(f'''<article class="card" data-task="{record["task"]}" data-name="{esc(record["name"])}">
<a href="figuras/{record["filename"]}" aria-label="Ampliar {esc(record["name"])} ({record["task"]})"><img src="figuras/{record["filename"]}" alt="{esc(record["name"])}: {"frontera de clases y muestras train/test" if record["task"] == "clasificacion" else "curva ajustada, señal y muestras train/test"}" width="1008" height="686" loading="lazy"></a>
<div class="inner"><span class="kind">{"Clasificación" if record["task"] == "clasificacion" else "Regresión"}</span><h2>{esc(record["name"])}</h2><p class="metric">{esc(text)}</p><p>{esc(record["explanation"])}</p><p><strong>Qué observar:</strong> {esc(record["look"])}</p><details><summary>Parámetros y resultados</summary><pre>{esc(record["parameters"])}</pre><a href="datos/{record["predictions"]}">Predicciones de test (CSV)</a></details><a class="lesson" href="{record["lesson"]}">Ir a la práctica del repositorio →</a></div></article>''')
    template = (HERE / "plantilla.html").read_text(encoding="utf-8")
    (output / "index.html").write_text(
        template.replace("<!-- CARDS -->", "\n".join(cards)), encoding="utf-8"
    )
    return result


# %% [markdown]
# ## Leer las figuras
# Los símbolos huecos son train y los rellenos son test en clasificación;
# círculo y triángulo distinguen clases también sin depender solo del color.
# El fondo indica clase predicha por un modelo aprendido únicamente en train.
# En regresión, la línea discontinua es la función sintética sin ruido; no es
# un intervalo de confianza. Se mantienen ejes y split iguales por tarea.
# Accuracy/F1 miden clasificación; R²/RMSE miden regresión y no se comparan
# numéricamente con accuracy. R² puede ser negativo y no es porcentaje de aciertos.
# La configuración está fijada, sin búsqueda con test. Un único dataset/split
# no demuestra superioridad estadística ni transferibilidad a otra población.

# %%
if __name__ == "__main__":
    report = generate()
    print(f"Generadas {len(report['models'])} figuras con datos y métricas auditables")
