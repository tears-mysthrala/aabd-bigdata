"""Render figures for the UCI Auto MPG linear-regression report."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import Orange


HERE = Path(__file__).resolve().parents[1]
DATA = HERE / "datos" / "auto_mpg" / "auto_mpg_weight.tab"
OUTPUT = HERE / "irudiak"
METRICS = json.loads((HERE / "datos" / "auto_mpg" / "auto_mpg_cv_metrics.json").read_text())
PREDICTIONS = np.genfromtxt(
    HERE / "datos" / "auto_mpg" / "auto_mpg_cv_iragarpenak.csv",
    delimiter=",", names=True, dtype=None, encoding="utf-8",
)
TABLE = Orange.data.Table(str(DATA))
WEIGHT = np.asarray(TABLE.X[:, 0], dtype=float)
MPG = np.asarray(TABLE.Y, dtype=float).reshape(-1)
OBSERVED = PREDICTIONS["mpg_observed"]
PREDICTED = PREDICTIONS["mpg_cv_predicted"]
RESIDUAL = PREDICTIONS["cv_residual"]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#52616b",
    "axes.labelcolor": "#263746",
    "text.color": "#263746",
    "xtick.color": "#52616b",
    "ytick.color": "#52616b",
})
BLUE, ORANGE, GREY = "#2878B5", "#E1812C", "#667781"


def workflow() -> None:
    fig, ax = plt.subplots(figsize=(11, 3.4), dpi=240)
    ax.axis("off")
    labels = [
        (0.08, "File\nauto_mpg_weight.tab"),
        (0.32, "Scatter Plot\nweight → mpg"),
        (0.56, "Linear Regression\nOLS"),
        (0.79, "Test & Score\n10-fold CV"),
        (0.96, "Predictions\nData Table"),
    ]
    for index, (x, label) in enumerate(labels):
        ax.text(x, 0.55, label, ha="center", va="center", transform=ax.transAxes,
                color="white", fontsize=10, weight="bold",
                bbox={"boxstyle": "round,pad=0.7", "facecolor": BLUE if index in (2, 3) else GREY,
                      "edgecolor": "white", "linewidth": 1.4})
        if index < len(labels) - 1:
            ax.annotate("", xy=(labels[index + 1][0] - 0.065, 0.55), xytext=(x + 0.07, 0.55),
                        xycoords=ax.transAxes, arrowprops={"arrowstyle": "-|>", "color": ORANGE, "lw": 1.8})
    ax.text(0.50, 0.08, "Unai Urzainqui Perez · Orange Data Mining · regresión lineal simple",
            transform=ax.transAxes, ha="center", color=GREY, fontsize=9)
    fig.tight_layout()
    fig.savefig(OUTPUT / "reg_workflow.png", bbox_inches="tight")
    plt.close(fig)


def relation() -> None:
    slope = float(METRICS["full_data_slope_mpg_per_pound"])
    intercept = float(METRICS["full_data_intercept_mpg"])
    r = float(METRICS["pearson_r_weight_mpg"])
    x = np.linspace(WEIGHT.min(), WEIGHT.max(), 200)
    fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=240)
    ax.scatter(WEIGHT, MPG, s=24, alpha=0.55, color=BLUE, edgecolors="none", label=f"Coches observados (n={len(MPG)})")
    ax.plot(x, intercept + slope * x, color=ORANGE, linewidth=2.5,
            label=f"OLS: mpg = {intercept:.2f} {slope:+.5f} × peso\nr = {r:.3f}")
    ax.set(title="Peso y consumo urbano en UCI Auto MPG",
           xlabel="Peso del vehículo (libras)", ylabel="Consumo urbano (millas por galón, mpg)")
    ax.grid(True, color="#dbe2e6", linewidth=0.7)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(OUTPUT / "reg_scatter_ols.png", bbox_inches="tight")
    plt.close(fig)


def predictions_and_residuals() -> None:
    minimum = min(float(OBSERVED.min()), float(PREDICTED.min()))
    maximum = max(float(OBSERVED.max()), float(PREDICTED.max()))
    fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=240)
    left.scatter(OBSERVED, PREDICTED, s=21, alpha=0.55, color=BLUE, edgecolors="none")
    left.plot([minimum, maximum], [minimum, maximum], color=ORANGE, linestyle="--", linewidth=2, label="Predicción perfecta")
    left.set(title="Predicciones fuera de muestra", xlabel="MPG observado", ylabel="MPG predicho · 10-fold CV")
    left.legend(frameon=False, fontsize=8)
    left.grid(True, color="#dbe2e6", linewidth=0.7)

    right.scatter(WEIGHT, RESIDUAL, s=21, alpha=0.55, color=BLUE, edgecolors="none")
    right.axhline(0, color=ORANGE, linestyle="--", linewidth=1.8)
    right.set(title="Residuos frente al peso", xlabel="Peso del vehículo (libras)", ylabel="Residuo CV (mpg observado − predicho)")
    right.grid(True, color="#dbe2e6", linewidth=0.7)
    fig.tight_layout()
    fig.savefig(OUTPUT / "reg_residuals.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if len(PREDICTIONS) != len(TABLE):
        raise ValueError("Expected one out-of-fold prediction per source row")
    workflow()
    relation()
    predictions_and_residuals()
    print(f"Created three Auto MPG figures in {OUTPUT}")
