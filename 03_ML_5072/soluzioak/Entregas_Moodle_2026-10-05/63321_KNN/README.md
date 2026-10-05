# KNN Iris - tarea 63321

Autor: Unai Urzainqui Perez. Preparado y verificado el 05/10/2026.

La consigna pide elegir y explicar datos, aplicar el modelo en Orange, analizar salidas y extraer conclusiones. El PDF, el workflow portable y las capturas nativas acompañan ese trabajo. No se ha enviado esta entrega a Moodle.

## Archivos

- PDF individual: informe académico en español, con resultados y límites.
- `Flujo_Orange.ows`: File, learner, Test & Score y Confusion Matrix.
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

150 filas, cuatro medidas en cm, iris como objetivo. k=3, euclídea, voto uniforme, sin escalado. Datos contrastados exactamente con sklearn.datasets.load_iris().

CV estratificada de 10 folds, shuffle y semilla 42 (la semilla nativa de Test & Score Orange 3.40.0). No hay evaluación sobre el entrenamiento. La normalización, si se usa, se aplica dentro del entrenamiento de cada fold. Las columnas nativas F1, precisión y recall son promedios ponderados por clase; el informe muestra también cada clase.

## Abrir el workflow

Abrir `Flujo_Orange.ows` con Orange 3.40.0 en esta carpeta. File guarda la ruta relativa `datos/iris.csv`. El flujo conecta los datos originales a Test & Score y el learner configurado al evaluador. No se conecta un preprocesador de normalización.

## Repetir la ejecución nativa

Usar un entorno Python con Orange 3.40.0, NumPy 2.3.5 y scikit-learn 1.9.1, las versiones de la ejecución conservada. Una sesión Wayland activa debe estar disponible. Desde esta carpeta, con ese entorno activado:

```bash
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"
export QT_QPA_PLATFORM=wayland
flock /tmp/aabd-orange-entregas-20261005.lock python reproducir.py
```

El programa muestra y captura sus propios widgets, los cierra y no captura el escritorio ni ventanas ajenas. Sobrescribe únicamente los resultados de esta carpeta. Se serializan las ejecuciones para limitar el uso de memoria.

Para regenerar el PDF en un entorno con ReportLab 5.0.1 y Pillow:

```bash
python generar_pdf.py
```

Después de regenerarlo, renderizar todas las páginas con `pdftoppm -png archivo.pdf pagina` y comprobarlas. Los hashes del manifiesto deben actualizarse si cambia algún archivo.

## Verificaciones y alcance

Se verificaron filas/clases, ausencia de NaN, cada fila evaluada una vez, etiquetas y medidas alineadas, folds idénticos a StratifiedKFold, total y diagonal de la matriz, y probabilidades idénticas a una evaluación independiente de la API Orange. El OOF se exporta en el orden de entrada, no en el orden de los folds. El .ows se parsea con orangecanvas y se empaquetan los settings de los widgets reales. Además se ha copiado workflow+datos a un directorio temporal distinto y se ha ejecutado con WidgetsScheme y propagación nativa de señales: las predicciones y probabilidades vuelven a coincidir con el CSV. Para repetir esa comprobación, ejecutar `verificar_workflow.py` bajo el mismo flock y entorno Wayland.

Ejemplo educativo: CV interna de 150 flores; no demuestra generalización a otras poblaciones o especies. Las probabilidades de vecinos no representan certeza.

## Fuente y licencia

Fisher (1936). UCI Iris, https://doi.org/10.24432/C56C76. CC BY 4.0. Copia del ejercicio contrastada con la distribución de scikit-learn.
