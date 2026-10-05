# Regresión logística - tarea 63320

Autor: Unai Urzainqui Perez. Preparado y verificado el 05/10/2026.

La consigna pide elegir y explicar datos, aplicar el modelo en Orange, analizar salidas y extraer conclusiones. El PDF, el workflow portable y las capturas nativas acompañan ese trabajo. No se ha enviado esta entrega a Moodle.

## Archivos

- PDF individual: informe académico en español, con resultados y límites.
- `Flujo_Orange.ows`: File, learner, Test & Score y Confusion Matrix + Preprocess y ROC Analysis.
- `datos/`: copia local del conjunto de datos, no requiere red.
- `reproducir.py`: ejecuta widgets Orange reales, exporta resultados y comprueba cada fila/fold.
- `predicciones_oof.csv`: una fila por ejemplo original, fold 1-10, etiqueta real, predicción y probabilidades.
- `resultados.json`: matriz, métricas, clases, parámetros, versiones y hashes.
- `evidencias/`: PNG de widgets mostrados en Wayland mediante QWidget.grab(), y `settings_gui.json`.
- `generar_pdf.py`: builder ReportLab reproducible.
- `verificar_workflow.py`: recarga y ejecuta el .ows desde otra carpeta temporal; verifica datos relativos y resultados.
- `evidencias/validacion_workflow.json`: evidencia de esa prueba de portabilidad y ejecución real.
- `MANIFEST_SHA256.json`: hashes de los archivos finales y verificación visual del PDF.

## Protocolo

569 filas, texture_mean como único predictor, diagnosis B/M. Ridge L2, C=1, sin ponderación. Normalize dentro de cada fold. El widget usa max_iter=10000 y random_state=0; se ha verificado igualdad de probabilidades (1e-10) respecto al script previo con max_iter=1000 y random_state=42, solver determinista lbfgs.

CV estratificada de 10 folds, shuffle y semilla 42 (la semilla nativa de Test & Score Orange 3.40.0). No hay evaluación sobre el entrenamiento. La normalización, si se usa, se aplica dentro del entrenamiento de cada fold. Las columnas nativas F1, precisión y recall son promedios ponderados por clase; el informe muestra también cada clase.

## Abrir el workflow

Abrir `Flujo_Orange.ows` con Orange 3.40.0 en esta carpeta. File guarda la ruta relativa `datos/wdbc_texture_mean.tab`. El flujo conecta los datos originales a Test & Score y el learner configurado al evaluador. Preprocess se conecta al learner para evitar normalizar globalmente antes de la CV.

## Repetir la ejecución nativa

Usar un entorno Python con Orange 3.40.0, NumPy 2.3.5 y scikit-learn 1.9.1, las versiones de la ejecución conservada. Una sesión Wayland activa debe estar disponible. Desde esta carpeta, con ese entorno activado:

```bash
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"
export QT_QPA_PLATFORM=wayland
flock /tmp/aabd-orange-entregas-20261005.lock python reproducir.py
```

El programa muestra y captura sus propios widgets, los cierra y no captura el escritorio ni ventanas ajenas. Sobrescribe únicamente los resultados de esta carpeta. Se serializan las ejecuciones para limitar el uso de memoria.

El script `curva_explicativa.py` exporta una figura de ajuste completo con texture_mean en X y diagnósticos observados B=0/M=1. La línea muestra probabilidades del modelo, no observaciones. Sus CSV no sustituyen la evaluación OOF. Repetirlo bajo el mismo flock.

Para regenerar el PDF en un entorno con ReportLab 5.0.1 y Pillow:

```bash
python generar_pdf.py
```

Después de regenerarlo, renderizar todas las páginas con `pdftoppm -png archivo.pdf pagina` y comprobarlas. Los hashes del manifiesto deben actualizarse si cambia algún archivo.

## Verificaciones y alcance

Se verificaron filas/clases, ausencia de NaN, cada fila evaluada una vez, etiquetas y medidas alineadas, folds idénticos a StratifiedKFold, total y diagonal de la matriz, y probabilidades idénticas a una evaluación independiente de la API Orange. El OOF se exporta en el orden de entrada, no en el orden de los folds. El .ows se parsea con orangecanvas y se empaquetan los settings de los widgets reales. Además se ha copiado workflow+datos a un directorio temporal distinto y se ha ejecutado con WidgetsScheme y propagación nativa de señales: las predicciones y probabilidades vuelven a coincidir con el CSV. Para repetir esa comprobación, ejecutar `verificar_workflow.py` bajo el mismo flock y entorno Wayland.

Modelo educativo de una variable: no hay validación clínica, externa o prospectiva; no debe usarse para decisiones sanitarias.

## Fuente y licencia

Wolberg, Mangasarian y Street (1993). UCI Breast Cancer Wisconsin (Diagnostic), https://doi.org/10.24432/C5DW2B. CC BY 4.0. Copia derivada con una variable y etiquetas.
