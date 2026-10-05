#!/usr/bin/env python3
"""Evaluate Orange KNN without a GUI; export each OOF result by source row."""
from pathlib import Path
import csv
import hashlib
import json
import platform

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import Orange
import sklearn
from Orange.data import Table
from Orange.classification import KNNLearner
from Orange.evaluation import CrossValidation, CA
from sklearn.datasets import load_iris
from sklearn.metrics import confusion_matrix, classification_report

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "datos/iris"
FIGURES = ROOT / "irudiak"


def main():
    source = DATA / "iris.csv"
    data = Table(str(source))
    reference = load_iris()
    labels = list(data.domain.class_var.values)
    assert labels == list(reference.target_names)
    np.testing.assert_array_equal(data.X, reference.data)
    np.testing.assert_array_equal(data.Y, reference.target)
    evaluation = CrossValidation(k=10, stratified=True, random_state=42)
    results = evaluation(data, [KNNLearner(n_neighbors=3, metric="euclidean", weights="uniform")])
    indices = results.row_indices
    assert sorted(indices.tolist()) == list(range(len(data)))
    np.testing.assert_array_equal(results.actual, data.Y[indices])
    predictions = np.empty(len(data), dtype=int)
    predictions[indices] = results.predicted[0].astype(int)
    probabilities = np.empty((len(data), len(labels)))
    probabilities[indices] = results.probabilities[0]
    folds = np.empty(len(data), dtype=int)
    for fold, position in enumerate(results.folds, 1):
        folds[indices[position]] = fold
    # Audit the stored fold IDs against the independent sklearn splitter used by Orange.
    from sklearn.model_selection import StratifiedKFold
    for fold, (train, test) in enumerate(StratifiedKFold(10, shuffle=True, random_state=42).split(data.X, data.Y), 1):
        np.testing.assert_array_equal(np.flatnonzero(folds == fold), test)
        assert not set(train) & set(test)
    out = DATA / "iris_knn_predicciones.csv"
    with out.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["row_id", "fold", *[v.name for v in data.domain.attributes], "iris_real", "iris_knn_predicho", "acierto", *["p_" + x for x in labels]])
        for i in range(len(data)):
            writer.writerow([i + 1, folds[i], *data.X[i], labels[int(data.Y[i])], labels[predictions[i]], int(predictions[i] == data.Y[i]), *probabilities[i]])
    # Re-read the actual deliverable: do not validate only the in-memory export.
    with out.open(encoding="utf-8") as stream:
        exported = list(csv.DictReader(stream))
    assert len(exported) == len(data)
    for i, row in enumerate(exported):
        assert int(row["row_id"]) == i + 1
        assert row["iris_real"] == labels[reference.target[i]]
        np.testing.assert_array_equal([float(row[v.name]) for v in data.domain.attributes], reference.data[i])
        assert int(row["acierto"]) == (row["iris_real"] == row["iris_knn_predicho"])
    cm = confusion_matrix(data.Y.astype(int), predictions, labels=range(3))
    accuracy = float(np.trace(cm) / len(data))
    assert accuracy == float(CA(results)[0])
    metrics = {
        "k": 3, "CA": accuracy, "CM": cm.tolist(), "labels": labels,
        "samples": len(data), "correct": int(np.trace(cm)),
        "protocol": {"folds": 10, "stratified": True, "shuffle": True, "random_state": 42, "metric": "euclidean", "weights": "uniform", "scaling": False,
                     "preprocessors": [type(p).__name__ for p in KNNLearner.preprocessors]},
        "versions": {"Orange": Orange.__version__, "sklearn": sklearn.__version__, "numpy": np.__version__, "python": platform.python_version()},
        "sha256": {"iris.csv": hashlib.sha256(source.read_bytes()).hexdigest(), out.name: hashlib.sha256(out.read_bytes()).hexdigest()},
        "validation": {"source_equals_sklearn": True, "export_label_feature_mismatches": 0, "each_row_evaluated_once": True, "fold_ids_verified": True},
        "classification_report": classification_report(data.Y.astype(int), predictions, target_names=labels, output_dict=True),
        "error_row_ids": (np.flatnonzero(predictions != data.Y) + 1).tolist(),
        "execution": "Orange Python API; no GUI screenshots or workflow execution claimed"
    }
    (DATA / "knn_iris.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    FIGURES.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.imshow(cm, cmap="Blues", vmin=0, vmax=50)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center", color="white" if cm[i, j] > 25 else "black", fontsize=17)
    ax.set(xticks=range(3), yticks=range(3), xticklabels=labels, yticklabels=labels,
           xlabel="Clase predicha", ylabel="Clase real", title=f"KNN Iris: CV estratificada, 10 folds, semilla 42\n{np.trace(cm)}/150 aciertos (CA={accuracy:.4f})")
    fig.tight_layout()
    fig.savefig(FIGURES / "knn_iris_confusion.png", dpi=180)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 5))
    for label, name in enumerate(labels):
        rows = data.Y == label
        ax.scatter(data.X[rows, 2], data.X[rows, 3], label=name, alpha=.7)
    errors = predictions != data.Y
    ax.scatter(data.X[errors, 2], data.X[errors, 3], facecolors="none", edgecolors="black", s=150, linewidths=1.5, label="Error OOF")
    offsets = {71: (10, 14), 73: (-35, -22), 84: (18, 18),
               107: (-32, 12), 120: (-5, -35), 134: (24, -18)}
    for i in np.flatnonzero(errors):
        ax.annotate(str(i + 1), (data.X[i, 2], data.X[i, 3]),
                    xytext=offsets.get(i + 1, (5, 7)),
                    textcoords="offset points", fontsize=8,
                    arrowprops={"arrowstyle": "-", "lw": .6, "color": "black"})
    ax.set(xlabel="Longitud del pétalo (cm)", ylabel="Anchura del pétalo (cm)", title="Etiquetas reales y errores fuera de muestra\nProyección de dos medidas; KNN utiliza las cuatro")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "knn_iris_errores.png", dpi=180)
    plt.close(fig)
    print(json.dumps(metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
