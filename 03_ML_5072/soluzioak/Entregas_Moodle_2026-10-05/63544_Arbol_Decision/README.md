# Árbol de decisión: clasificación de Iris

Entrega autónoma de la tarea Moodle 63544: [informe PDF](Arbol_Decision_Iris.pdf), [flujo Orange](Arbol_Decision_Iris.ows), [datos](datos/iris.csv), ejecución reproducible y salidas auditables.

## Alcance y supuesto adoptado

La tarea Moodle existe, pero su introducción, archivos adjuntos y rúbrica estaban vacíos y no había plazo visible en la consulta del 05/10/2026. Por autorización del usuario se adopta el patrón de otras prácticas: dataset elegido y descrito, modelo Orange, evaluación sin fuga, análisis de salidas y conclusiones. Es un candidato académico completo con ese supuesto explícito; no se inventa una consigna del profesorado ni se afirma satisfacer una rúbrica no disponible. No se ha enviado a Moodle.

## Datos y experimento

Iris (Fisher, 1936), UCI, DOI [10.24432/C56C76](https://doi.org/10.24432/C56C76), licencia CC BY 4.0. Copia local del repositorio comprobada exactamente contra `sklearn.datasets.load_iris`: 150 flores, cuatro medidas en cm, 50 registros por especie y cero valores ausentes. `datos/iris.csv` conserva el formato Orange con tres filas iniciales: nombres, tipos y roles. La variable objetivo es `iris`.

Validación cruzada estratificada de 10 folds, barajada, semilla 42. En cada fold: 135 filas de entrenamiento y 15 de evaluación (5 por especie). Las 150 predicciones OOF cubren cada fila exactamente una vez. Las métricas no son de entrenamiento; no hay test externo ni selección de hiperparámetros con los resultados evaluados. El modelo completo se usa solo para inspección.

Parámetros explícitos: `{"max_depth": 3, "min_samples_leaf": 2, "min_samples_split": 5, "binarize": true, "sufficient_majority": 0.95}`.

En SVM, los preprocesadores pertenecen al learner: el escalado se aprende dentro de cada fold, sin transformar previamente toda la tabla. La auditoría de medias y factores por fold figura en `salidas/metricas.json` para SVM. El árbol nativo de Orange es determinista con estos parámetros; no necesita una semilla de ajuste. Random Forest y calibración SVM fijan semilla 42.

## Resultados y evidencia

- Accuracy: 0.946667; F1 ponderado: 0.946645; F1 macro: 0.946645.
- Matriz (filas reales; columnas predichas; orden setosa, versicolor, virginica): `[[50, 0, 0], [0, 45, 5], [0, 3, 47]]`.
- `salidas/predicciones_oof.csv`: row_id 1-150, fold, cuatro medidas, real, predicha, acierto y probabilidades.
- `salidas/metricas.json`: métricas completas, informe por especie, errores, versiones y hashes.
- `capturas/`: ventanas Orange reales mostradas en Wayland y capturadas con `QWidget.grab()`. No son montajes o interfaces dibujadas. ROC muestra versicolor frente al resto.
- `verificacion/verificacion.json`: comprobaciones del artefacto final.
- `verificacion/portabilidad.json`: copia del workflow/dataset reubicada dentro de verificación y abierta desde otro cwd con WidgetsScheme; señales reales File → Script → Test & Score → CM/ROC sin inyección manual, y coincidencia exacta de OOF/probabilidades. Las páginas renderizadas y revisión visual se documentan en `verificacion/revision_visual.json`.

La salida del widget Test & Score coincide con una segunda ejecución independiente de `Orange.evaluation.CrossValidation` en índices, predicciones y probabilidades. Se contrastan los folds con `sklearn.model_selection.StratifiedKFold`, se relee el CSV entregado y se recomputan los totales de la matriz. Los hashes de capturas se registran tras guardarlas.

## Abrir el flujo Orange

Abrir `Arbol_Decision_Iris.ows` en Orange 3.40.0. Mantener juntos el `.ows` y `datos/iris.csv`. El workflow guarda la ruta relativa `datos/iris.csv` y el contenido exacto de `modelo_orange.py` en el widget Python Script. File entrega datos originales a Test & Score; Python Script entrega el learner. Confusion Matrix y ROC Analysis reciben sus resultados. Para el árbol, Tree Viewer recibe el modelo ajustado con las 150 filas, destinado solo a explicación.

El uso de Python Script permite fijar parámetros sin discrepancias ocultas: en Orange 3.40 el widget estándar Random Forest utiliza semilla 0 al activar entrenamiento replicable, por lo que no serviría para reproducir este experimento de semilla 42. El script no modifica archivos ni usa red al ejecutarse dentro del `.ows`.

## Reproducir la ejecución y capturas

Desde esta carpeta, con Orange instalado y un compositor Wayland disponible:

```bash
flock /tmp/aabd-orange-entregas-20261005.lock env \
  XDG_RUNTIME_DIR=/run/user/$(id -u) WAYLAND_DISPLAY=wayland-1 \
  QT_QPA_PLATFORM=wayland \
  /home/tears/.local/share/uv/tools/orange3/bin/python reproducir.py
flock /tmp/aabd-orange-entregas-20261005.lock \
  /home/tears/.local/share/uv/tools/orange3/bin/python verificar.py --record
flock /tmp/aabd-orange-entregas-20261005.lock env \
  XDG_RUNTIME_DIR=/run/user/$(id -u) WAYLAND_DISPLAY=wayland-1 \
  QT_QPA_PLATFORM=wayland \
  /home/tears/.local/share/uv/tools/orange3/bin/python verificar_portabilidad.py
```

`reproducir.py` genera OOF, métricas, capturas y `.ows`; comprueba que las ventanas son visibles y cierra únicamente sus widgets al terminar. La variable Wayland y la ruta del intérprete se adaptan si se ejecuta en otro equipo. El entorno verificado: Orange 3.40.0, scikit-learn 1.9.1, NumPy 2.3.5, Python 3.13.13.

## Regenerar el PDF

El generador utiliza únicamente salidas y capturas ya producidas. Las fuentes Liberation incluidas tienen su licencia en `recursos/LICENCIA_Liberation.txt`. Instalar ReportLab en un entorno temporal local, sin actualizar el entorno Orange:

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements-pdf.txt
.venv/bin/python generar_pdf.py
pdftoppm -r 85 -png Arbol_Decision_Iris.pdf verificacion/pagina
```

No se incluyen `.venv`, `.pdf-deps` ni `__pycache__` en el entregable. `verificar.py` requiere el intérprete Orange para leer sus propiedades serializadas y `pdfinfo`/`pdftotext` (Poppler). No abrir flujos `.ows` no confiables: este verificador deserializa solo el pickle producido aquí.

## Límites de interpretación

Iris es un conjunto pequeño, equilibrado y muy usado para aprendizaje. No establece la superioridad general de este algoritmo. Las conclusiones se limitan a este modelo y protocolo. Una ROC con AUC alta puede coexistir con errores de etiquetas. Los resultados del modelo completo son explicativos y no sustituyen las predicciones OOF.

Documentación: [Orange Test & Score](https://orangedatamining.com/widget-catalog/evaluate/testandscore/). Fuente de datos: [UCI Iris](https://archive.ics.uci.edu/dataset/53/iris).
