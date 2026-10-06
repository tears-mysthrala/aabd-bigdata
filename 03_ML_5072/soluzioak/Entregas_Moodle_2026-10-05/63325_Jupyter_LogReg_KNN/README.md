# Jupyter: LogReg frente a KNN — tarea 63325

Entregar `iris_logreg_knn.ipynb`, `txostena_beteta.md` y `erabaki_mugak.png` juntos. `Informe_LogReg_KNN.pdf` es una copia autónoma para lectura; no sustituye el notebook solicitado. `resultados.json` permite contrastar las cifras.

El informe y notebook completan las plantillas docentes. Usan las primeras dos variables de Iris, LogReg max_iter=200 y KNN k=3. Las salidas son de entrenamiento, no de test.

## Abrir y ejecutar

Extraer esta carpeta y abrir una terminal dentro de ella. Con Python 3.13 y uv:

```bash
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python ejecutar_notebook.py
.venv/bin/python crear_pdf.py
```

`ejecutar_notebook.py` inicia un kernel limpio, ejecuta todas las celdas, comprueba la ausencia de errores, las matrices y 123/128 aciertos, y guarda el notebook con sus salidas. Sobrescribe solamente los archivos de esta carpeta. Para ejecutar interactivamente, seleccionar ese entorno como kernel y usar «Restart Kernel and Run All» desde esta carpeta.

La figura también está embebida en el notebook. El informe Markdown usa un enlace local a ella, de modo que ambos archivos deben viajar juntos. No hay dependencia de un checkout del repositorio ni de rutas privadas del autor.

## Alcance

La reflexión explica k=1 y k=50 como pregunta hipotética del docente; no se presenta un experimento con esos valores. No hay holdout ni CV. No se realizó entrega en Moodle.

Fuente docente: [tarea 63325](https://elearning20.hezkuntza.net/012053/mod/assign/view.php?id=63325), con `ikaskuntza_gainbegiratua_ikaslea.ipynb` y `txostena_ikaslea.md`, verificados contra las copias locales el 05/10/2026.
