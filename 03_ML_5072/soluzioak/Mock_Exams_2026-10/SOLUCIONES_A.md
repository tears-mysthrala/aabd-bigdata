# Soluciones y rúbrica — 5072 — Machine Learning, simulacro A

[Volver al examen](../../materialak/Mock_Exams_2026-10/EXAMEN_A.md).
Corrección propuesta, no baremo docente. Se admiten alternativas coherentes con
los requisitos. Concede crédito parcial por razonamiento correcto aunque haya
un error aritmético posterior; no cuentes dos veces el mismo mérito.
Los valores calculados son respuestas de casos sintéticos, no resultados de planta.

## 1 — 2 puntos

Eliminar feature posterior; quitar ID como predictor salvo razón defendible,
conservarlo para grupos. Imputación numérica median y nominal most_frequent,
OneHot para nominal; Ordinal solo con orden real. Ajustar todo preprocesado en
train y en cada fold mediante Pipeline/ColumnTransformer. Group split para
máquinas nuevas; temporal para futuro. En selección usar CV adecuada al objetivo;
el test final no determina parámetros ni umbral. 0.5 por apartado.

## 2 — 2 puntos

Errores absolutos 1,1,0: **MAE=2/3**, **MSE=2/3**; SSE=2 y SST=8,
**R²=0.75**. Lineal estima valor continuo; logística modela probabilidad de
clase, mediante sigmoide en el caso binario. Ridge penaliza L2, Lasso L1 y puede anular coeficientes;
regularización limita complejidad, no garantiza mejor score. K pequeño favorece
fronteras irregulares y varianza; C grande penaliza más violaciones de margen,
reduce regularización y puede sobreajustar según kernel/datos; árbol sin límite
puede memorizar ruido. Rúbrica 0.75/0.5/0.75.

## 3 — 2 puntos

N=200; accuracy=184/200=**0.92**; precisión=4/14=**0.2857**;
recall=4/10=**0.4**; F1=8/(8+10+6)=**1/3**. Baseline siempre 0:
accuracy=190/200=**0.95**, recall/F1=0 para clase 1 (precisión sin positivos
predichos es indefinida; zero_division=0 es convención). Mejor accuracy no
significa detección útil. Recall importa para no omitir fallos junto al coste FP.
ROC-AUC evalúa ranking a distintos umbrales, F1 una decisión concreta y depende
de prevalencia. Elegir umbral en validación. Macro promedia clases por igual,
weighted por support. Rúbrica 1/0.5/0.5.

## 4 — 1.5 puntos

Bagging entrena sobre remuestreos; RF añade selección aleatoria de features.
Boosting construye modelos secuenciales corrigiendo errores. AdaBoost repondera
muestras; Gradient Boosting ajusta gradientes/residuos de una pérdida; XGBoost
implementa boosting de árboles con regularización y optimizaciones. Árbol muestra
gran brecha train/val; forest candidato por CV, pero pedir dispersión de folds y
coste. No abrir test para elegir entre ambos. 0.5 por apartado.

## 5 — 2.5 puntos

Código de referencia del núcleo (ejecutar con dependencias locales disponibles):

```python
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_iris(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
assert len(ytr) == 105 and len(yte) == 45
cv = StratifiedKFold(5, shuffle=True, random_state=42)
lr = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
search = GridSearchCV(
    make_pipeline(StandardScaler(), KNeighborsClassifier()),
    {"kneighborsclassifier__n_neighbors": [3, 5, 7]},
    cv=cv,
    scoring="accuracy",
)
lr.fit(Xtr, ytr)
search.fit(Xtr, ytr)
for name, model in [("LogReg", lr), ("KNN", search.best_estimator_)]:
    pred = model.predict(Xte)
    cm = confusion_matrix(yte, pred, labels=[0, 1, 2])
    assert cm.sum() == 45
    print(name, accuracy_score(yte, pred), cm)
```

Filas de cm: reales; columnas: predichas; 0=setosa,1=versicolor,2=virginica.
Para visualizar 2D se entrenan modelos nuevos: el modelo de cuatro features no
puede predecir con solo dos. Continuación del código anterior:

```python
import matplotlib.pyplot as plt
from sklearn.base import clone

lr2 = clone(lr).fit(Xtr[:, :2], ytr)
search2 = clone(search).fit(Xtr[:, :2], ytr)
x0, x1 = Xtr[:, 0].min() - 0.5, Xtr[:, 0].max() + 0.5
y0, y1 = Xtr[:, 1].min() - 0.5, Xtr[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.linspace(x0, x1, 180), np.linspace(y0, y1, 180))
mesh = np.c_[xx.ravel(), yy.ravel()]
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, name, model2 in zip(
    axes, ["LogReg 2D", "KNN 2D"], [lr2, search2.best_estimator_]
):
    ax.contourf(
        xx,
        yy,
        model2.predict(mesh).reshape(xx.shape),
        levels=[-0.5, 0.5, 1.5, 2.5],
        cmap="viridis",
        alpha=0.25,
    )
    for label, name_class in enumerate(["setosa", "versicolor", "virginica"]):
        mask = ytr == label
        ax.scatter(
            Xtr[mask, 0],
            Xtr[mask, 1],
            label=name_class,
            color=plt.get_cmap("viridis")(label / 2),
            edgecolor="black",
        )
    ax.set(xlabel="Longitud sépalo (cm)", ylabel="Anchura sépalo (cm)", title=name)
    ax.legend()
fig.tight_layout()
# Guardar solo salida propia, en el directorio actual de la práctica.
fig.savefig("limites_iris_mock.png", dpi=140)
plt.close(fig)
```

La CV de k se repite solo con las dos features de train; no usar test para elegir
el modelo del dibujo. Logística da fronteras lineales en este plano; KNN votación
local, sensibilidad a k. Comparar métricas 4D producidas realmente; no prescribir
un ganador ni score exacto por versión. El test pequeño tiene incertidumbre.
El gráfico explica frontera 2D, no acredita rendimiento externo.
Puntos 0.5/0.75/0.5/0.5/0.25; un gráfico sin código o sin ejes no completa (d).
