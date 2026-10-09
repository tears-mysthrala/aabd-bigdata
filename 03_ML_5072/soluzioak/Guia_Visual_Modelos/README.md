# Guía visual de modelos

Abre [la galería](index.html) directamente en el navegador: funciona sin servidor,
sin conexión y sin instalaciones. Permite buscar modelos y filtrar clasificación
o regresión. Contiene **20 figuras**, diez por tarea, con explicación, parámetros,
métricas de test y enlaces a las prácticas. Incluye AdaBoost, Gradient Boosting y
XGBoost junto a los modelos de la carpeta aportada.

## Cómo interpretar las figuras

Clasificación usa dos medias lunas sintéticas: 224 observaciones de entrenamiento
y 96 de test. Color y forma indican la clase verdadera; puntos vacíos son train
y rellenos son test. El fondo indica la **clase predicha**, no su probabilidad.
Los errores son puntos de test situados en la región de otra clase.

Regresión usa `y = 0.2*x² + sin(1.7*x) + ruido gaussiano`, con 168 muestras de
train y 72 de test. La línea naranja es la predicción; la discontinua es la señal
conocida sin ruido. No representa un intervalo de confianza. Ridge y Lasso usan
expansión polinómica de grado cinco; su curva no corresponde a regresión sobre
una única variable lineal sin expansión. GaussianNB es una variante para variables
continuas y no reproduce el ejercicio de texto con MultinomialNB.

Todos los modelos de cada tarea comparten datos, partición y escalas gráficas.
El escalado se aprende dentro del Pipeline, exclusivamente con train. Los
parámetros están fijados antes de evaluar; no se optimizan con test. Accuracy/F1
y R²/MAE/RMSE son resultados de estos datos sintéticos, no un ranking general.
R² puede ser negativo; una buena métrica aislada no demuestra generalización
a datos reales. Observa también la diferencia entre entrenamiento y test.

## Reproducir y comprobar

Desde la raíz del repositorio:

```bash
cd 03_ML_5072/soluzioak/Guia_Visual_Modelos
uv sync --frozen
MPLBACKEND=Agg uv run --frozen python generar.py
uv run --frozen pytest -q
uv run --frozen --group security pip-audit
```

Python 3.13, entorno propio y [lock](uv.lock). [Script](generar.py) y
[notebook ejecutado](generar.ipynb) contienen la misma narrativa y código.
Para Jupyter selecciona `.venv/bin/python` y ejecuta desde esta carpeta.
La generación no descarga datos ni abre servicios: sobrescribe `figuras/`,
`datos/`, `metricas.json` e `index.html`. Instalación y auditoría sí consultan
registros externos. La plantilla es [plantilla.html](plantilla.html).

[Datos y resultados](metricas.json) incluyen versiones, semilla 42, hashes de
los dos datasets y matrices de confusión. Los CSV de predicciones permiten
recalcular las métricas sin confiar en el texto de la tarjeta. Las pruebas
comprueban esa correspondencia, la separación train/test y el escalado.

## Procedencia y límites

Los **14 gráficos originales** y su HTML/JSON se conservan byte a byte en
[originales/](originales/index.html), con [hashes](originales/PROCEDENCIA.json).
La carpeta entregada no incluía generador ni datos: sus métricas no se han
reproducido independientemente. La galería principal es una variante nueva,
con datos y parámetros explícitos; no pretende certificar esas cifras originales.

Referencias de los estimadores: [AdaBoostRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostRegressor.html),
[RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
y [R²](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html).
Las validaciones locales se registran en [EJECUCION.json](EJECUCION.json).
