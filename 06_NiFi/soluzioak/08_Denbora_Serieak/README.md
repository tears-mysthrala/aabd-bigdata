# Series temporales — todas las actividades del PDF

Enunciado: [02_Denbora_Serieak.pdf](../../materialak/02_Denbora_Serieak.pdf).
[Cuaderno completo](denbora_serieak.ipynb) y [script equivalente](denbora_serieak.py).

Cubre clasificación regular/irregular, cálculo de muestras, problemas de calidad, patrones A–D, diseño IoT de 20 máquinas y la práctica industrial de **19 pasos de la edición del 9 de octubre**. La extensión de descomposición/pronóstico es añadida, no una entrega docente.

## Ejecutar

Desde esta carpeta, Python 3.13 y uv:

```bash
uv sync --frozen
MPLBACKEND=Agg uv run --frozen python denbora_serieak.py
```

Para el notebook seleccionar `.venv/bin/python` como kernel y ejecutar en orden desde esta carpeta. El script resuelve la salida respecto a su archivo y funciona también desde la raíz sin crear una carpeta resultados allí. En notebook se reconoce la carpeta de práctica o la raíz y se rechazan otros directorios. Sobrescribe sus artefactos propios en `resultados/`: CSV sintético, CSV de operaciones, dos PNG y JSON de validación. Copiarlos antes si se quiere conservar una ejecución distinta. No modifica servicios ni descarga datos.

El CSV docente ya está disponible desde el 9 de octubre; la resolución actual está al final de esta guía. Esta primera resolución se hizo antes de recibirlo. La variante sintética declara semilla, tendencia, ruido y huecos; sus conclusiones no describen una fábrica real. Tampoco se ha ejecutado un pipeline NiFi/Kafka: el ejercicio Pandas no lo pide. La arquitectura IoT es una respuesta de diseño.

## Evidencias

[Ejecución del notebook](EJECUCION.json): tres celdas de código ejecutadas sin errores; script también ejecutado el 9 de octubre. [Resultado](resultados/validacion.json): 180 filas, tres NaN, **61 registros de 08:00 a 09:00 UTC con extremos incluidos**, media del intervalo 22.587 °C y 18 ventanas de diez minutos. El conteo industrial distingue 40 valores/s de 20 mensajes/s; a 100 bytes por valor son 345.6 MB/día, sin overhead.

La variante incorpora un pico deliberado de 65 °C y lo conserva: la máxima media de diez minutos es 26.030 °C y la máxima media móvil, 30.425 °C. Ilustra pérdida de picos, no una avería observada. `tenperatura_beteta` usa interpolación temporal; `tenperatura_leundua` se calcula después sobre los valores rellenados y tiene solo cuatro NaN iniciales. Las respuestas del paso 19 aparecen junto al código. Los resultados docentes recalculados se guardan por separado, sin mezclar variantes.

[Gráfico de práctica](resultados/tenperatura.png), [descomposición](resultados/descomposicion.png) y [CSV con operaciones](resultados/practica.csv). La interpolación es retrospectiva; no se usa para entrenar el pronóstico. Descomposición con periodo 24 sobre 14 días sintéticos; test de las últimas 48 horas, baseline del último día de train repetido, MAE 2.1115 en unidades sintéticas. No prueba rendimiento energético real ni ausencia de sesgo temporal en otro modelo.

[Auditoría de dependencias](AUDITORIA_DEPENDENCIAS.json): sin vulnerabilidades conocidas detectadas en este entorno.

## Retos adicionales recibidos el 9 de octubre a las 10:02

La nueva edición incorpora dos retos y un repaso. [Solución](retos_adicionales.ipynb) y [script equivalente](retos_adicionales.py): selección de temperaturas >50 °C y alertas por episodio de tres medidas consecutivas, agregación adecuada según magnitud/unidades y cinco emparejamientos del repaso. En la variante sintética: una lectura de 65 °C y cero episodios de tres consecutivas. Los NaN y huecos rompen la secuencia; no se ordena detener ninguna máquina. `size` cuenta filas y `count` valores no nulos; los kWh de intervalos se suman, una potencia se integra y un contador acumulativo requiere diferencias.

Ejecutar desde esta carpeta `uv run --frozen python denbora_serieak.py`, después `uv run --frozen python retos_adicionales.py` y `uv run --frozen pytest -q`. Se sobrescribe solo `resultados/retos_adicionales.json`; el script adicional lee el CSV sintético generado por la práctica principal. [Ejecución adicional](EJECUCION_RETOS.json), tres casos de persistencia/NaN/huecos (incluido `pd.NA` nullable) y auditoría de dependencias actualizada. Esta variante sigue usando su CSV sintético; la resolución docente siguiente usa el nuevo recurso.

## CSV y plantilla docentes recibidos hoy (recursos 64608 y 64609)

[Solución docente](denbora_serieak_docente.ipynb) y [script](denbora_serieak_docente.py)
cubren las 15 tareas de la plantilla, ejecución/comprobaciones/reflexiones de los
19 pasos del PDF, ambos retos y el repaso. Las [seis actividades de aula](ARIKETAK_2026-10-09.md)
se resuelven con sus parámetros nuevos: 250 ms, 100 sensores y fábrica de 50 máquinas.
No confundirlos con los números del ejercicio anterior.

Desde esta carpeta:

```bash
uv sync --frozen
MPLBACKEND=Agg uv run --frozen python denbora_serieak_docente.py
uv run --frozen pytest -q test_retos_adicionales.py test_denbora_docente.py
```

Se conserva el [CSV original](../../materialak/sentsorea.csv), sin zona horaria
especificada, y la plantilla vacía. Salidas propias en `resultados/docente/`:
[CSV de operaciones](resultados/docente/operaciones.csv), [medias de 10 minutos](resultados/docente/medias_10min.csv),
[agregaciones](resultados/docente/agregaciones_10min.csv), [gráfico](resultados/docente/tenperatura.png)
y [validación con SHA de entrada](resultados/docente/validacion.json).
[Ejecución del notebook](EJECUCION_DOCENTE.json): no sustituye al informe histórico
de la variante sintética. Notebook muestra el gráfico embebido.

180 filas entre 08:00 y 10:59; tres NaN de temperatura, ninguno de vibración.
08:00–09:00 incluye 61 filas y 60 temperaturas válidas: media **42.2283 °C**.
18 ventanas; interpolación interior completa; rolling(5) conserva cuatro NaN
de calentamiento. Un pico **84.8 °C a las 09:53**; una alerta por lectura y
cero episodios de tres consecutivas. La media agregada atenúa ese pico bajo 50.
Procedencia docente no significa datos verificados de planta. Son operaciones
Pandas y razonamiento de arquitectura, sin ejecutar NiFi/Kafka ni entregar en Moodle.
