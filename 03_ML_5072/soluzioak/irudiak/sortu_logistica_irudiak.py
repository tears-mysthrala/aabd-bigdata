"""Build figures for the one-predictor WDBC logistic-regression report."""
from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, roc_curve

HERE = Path(__file__).resolve().parents[1]
DATA_DIR = HERE / "datos" / "breast_cancer_wisconsin"
OUT = HERE / "irudiak"
AUTHOR = "Unai Urzainqui Perez"
NAVY, BLUE, GOLD, GREY = "#17324D", "#2878B5", "#E1812C", "#718096"


def read_inputs():
    metrics = json.loads((DATA_DIR / "wdbc_cv_metricas.json").read_text(encoding="utf-8"))
    with (DATA_DIR / "wdbc_cv_predicciones.csv").open(encoding="utf-8", newline="") as f:
        predictions = list(csv.DictReader(f))
    with (DATA_DIR / "wdbc_sigmoide_ajuste_completo.csv").open(encoding="utf-8", newline="") as f:
        curve = list(csv.DictReader(f))
    actual = np.array([row["diagnosis_observed"] for row in predictions])
    full_logit_score = np.array([float(row["logit_score_full_fit"]) for row in predictions])
    p_malignant = np.array([float(row["probability_malignant_cv"]) for row in predictions])
    return metrics, full_logit_score, actual, p_malignant, curve


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    metrics, full_logit_score, actual, p_malignant, curve = read_inputs()
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 13, "axes.labelcolor": NAVY, "text.color": NAVY})

    counts = [int((actual == "B").sum()), int((actual == "M").sum())]
    labels = ["Benigno (B)", "Maligno (M)"]
    fig, ax = plt.subplots(figsize=(7.7, 2.7))
    bars = ax.barh(labels, counts, color=[BLUE, GOLD], height=.55)
    ax.set_xlim(0, max(counts) * 1.2)
    ax.set_xlabel("Muestras (n)")
    ax.set_title("Distribución del diagnóstico", loc="left", weight="bold")
    ax.grid(axis="x", color="#D9E2E8", linewidth=.8); ax.set_axisbelow(True)
    for bar, n in zip(bars, counts):
        ax.text(n + max(counts)*.015, bar.get_y()+bar.get_height()/2, f"{n} ({n/len(actual):.1%})", va="center", color=NAVY)
    ax.spines[["top", "right", "left"]].set_visible(False); ax.spines["bottom"].set_color("#CBD5E0")
    fig.tight_layout(); fig.savefig(OUT/"logistica_clases.png", dpi=180, bbox_inches="tight", facecolor="white"); plt.close(fig)

    # Plot one out-of-fold confidence score per sample, colored by its observed diagnosis.
    curve_x = np.array([float(row["logit_score_z"]) for row in curve])
    curve_y = np.array([float(row["probability_malignant_full_data_fit"]) for row in curve])
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    x_min = min(float(curve_x.min()), float(full_logit_score.min())) - .35
    x_max = max(float(curve_x.max()), float(full_logit_score.max())) + .35
    ax.fill_betweenx([0,.5], x_min, 0, color="#FCE8E6", alpha=.88, zorder=0, label="Región de decisión: B")
    ax.fill_betweenx([.5,1], 0, x_max, color="#E4F0FA", alpha=.9, zorder=0, label="Región de decisión: M")
    ax.plot(curve_x, curve_y, color=NAVY, linewidth=2.6, label="Sigmoide σ(z)", zorder=2)
    ax.scatter(full_logit_score[actual == "B"], np.zeros((actual == "B").sum()), s=25, alpha=.70, color=BLUE, edgecolor="white", linewidth=.35, label="Diagnóstico observado: B (0)", zorder=3)
    ax.scatter(full_logit_score[actual == "M"], np.ones((actual == "M").sum()), s=25, alpha=.70, color=GOLD, edgecolor="white", linewidth=.35, label="Diagnóstico observado: M (1)", zorder=3)
    ax.axvline(0, color=GREY, linestyle="--", linewidth=1.15, label="z=0")
    ax.axhline(.5, color=GREY, linestyle=":", linewidth=1.15, label="Umbral p=0,5")
    ax.set(xlim=(x_min,x_max), ylim=(0,1), xlabel="Puntuación logística z = β₀ + β₁ · texture_mean", ylabel="Diagnóstico observado (0/1) / probabilidad estimada", title="Diagnóstico observado y sigmoide logística")
    ax.set_yticks([0,.25,.5,.75,1],["0","0,25","0,5","0,75","1"])
    ax.grid(color="#D9E2E8", linewidth=.7); ax.spines[["top","right"]].set_visible(False)
    ax.legend(loc="center left", bbox_to_anchor=(1.01,.5), frameon=False, fontsize=8)
    fig.tight_layout(); fig.savefig(OUT/"logistica_sigmoide_clasificacion.png", dpi=180, bbox_inches="tight", facecolor="white"); plt.close(fig)

    cm = metrics["confusion_matrix"]
    matrix = np.array([[cm["tn_benign"], cm["fp_benign_as_malignant"]], [cm["fn_malignant_as_benign"], cm["tp_malignant"]]])
    row_pct = matrix / matrix.sum(axis=1, keepdims=True)
    fig, ax = plt.subplots(figsize=(6.0, 4.4)); ax.imshow(matrix, cmap="Blues", vmin=0)
    ax.set_xticks([0,1],["Predicho benigno","Predicho maligno"]); ax.set_yticks([0,1],["Real benigno","Real maligno"])
    ax.set_title("Matriz de confusión - validación cruzada", loc="left", weight="bold", pad=14)
    for i in range(2):
        for j in range(2):
            color="white" if matrix[i,j] > matrix.max()*.42 else NAVY
            ax.text(j,i,f"{matrix[i,j]}\n{row_pct[i,j]:.1%}",ha="center",va="center",color=color,weight="bold",fontsize=10)
    ax.set_xlabel("Clase predicha"); ax.set_ylabel("Clase observada")
    ax.set_xticks(np.arange(-.5,2,1),minor=True); ax.set_yticks(np.arange(-.5,2,1),minor=True)
    ax.grid(which="minor",color="white",linewidth=2); ax.tick_params(which="minor",bottom=False,left=False)
    fig.tight_layout(); fig.savefig(OUT/"logistica_confusion.png",dpi=180,bbox_inches="tight",facecolor="white"); plt.close(fig)

    fpr,tpr,_=roc_curve(actual=="M",p_malignant)
    fig,ax=plt.subplots(figsize=(6.2,4.0))
    ax.plot(fpr,tpr,color=BLUE,linewidth=2.4,label=f"Logística: AUC = {metrics['roc_auc']:.3f}")
    ax.plot([0,1],[0,1],color=GREY,linestyle="--",linewidth=1.2,label="Azar")
    ax.set(xlim=(0,1),ylim=(0,1.02),xlabel="Tasa de falsos positivos",ylabel="Sensibilidad (recall maligno)",title="Curva ROC - predicciones fuera de muestra")
    ax.grid(color="#D9E2E8",linewidth=.7); ax.legend(loc="lower right",frameon=False)
    ax.spines[["top","right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(OUT/"logistica_curvas.png",dpi=180,bbox_inches="tight",facecolor="white"); plt.close(fig)

    fig, ax=plt.subplots(figsize=(10.6,2.3)); ax.set_xlim(0,10.6); ax.set_ylim(0,2.2); ax.axis("off")
    nodes=[(.1,1.2,1.75,.65,"File\nWDBC · UCI","#EFF4F7"),(2.35,1.2,1.8,.65,"Select Columns\ntexture_mean -> X\ndiagnosis -> Y","#EFF4F7"),(4.65,1.2,1.8,.65,"Logistic Regression\nL2, C = 1","#DDECF7"),(6.95,1.2,1.55,.65,"Test & Score\n10-fold CV","#DDECF7"),(8.95,1.2,1.5,.65,"ROC / Confusion\nPredictions","#EFF4F7")]
    for x,y,w,h,label,fill in nodes:
        ax.add_patch(plt.Rectangle((x,y),w,h,facecolor=fill,edgecolor=BLUE if "Logistic" in label or "Score" in label else "#AAB8C2",linewidth=1.2))
        ax.text(x+w/2,y+h/2,label,ha="center",va="center",fontsize=8,weight="bold" if "Logistic" in label or "Score" in label else "normal")
    for a,b in [(1.85,2.35),(4.15,4.65),(6.45,6.95),(8.5,8.95)]: ax.annotate("",xy=(b,1.525),xytext=(a,1.525),arrowprops={"arrowstyle":"->","color":GOLD,"lw":1.5})
    ax.text(5.3,.45,"Puntos = diagnósticos reales; curva = P(M) estimada. Las métricas se evalúan con validación cruzada.",ha="center",fontsize=8,color=GREY)
    ax.text(5.3,.12,AUTHOR,ha="center",fontsize=7,color=GREY)
    fig.savefig(OUT/"logistica_workflow.png",dpi=180,bbox_inches="tight",facecolor="white"); plt.close(fig)
    print("Created five Wisconsin Breast Cancer logistic-regression figures")


if __name__ == "__main__":
    main()
