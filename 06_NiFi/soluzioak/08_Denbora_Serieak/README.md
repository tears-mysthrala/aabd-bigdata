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

No está disponible el `sentsorea.csv` docente. La variante sintética declara semilla, tendencia, ruido y huecos; sus conclusiones no describen una fábrica real. Tampoco se ha ejecutado un pipeline NiFi/Kafka: el ejercicio Pandas no lo pide. La arquitectura IoT es una respuesta de diseño.

## Evidencias

[Ejecución del notebook](EJECUCION.json): tres celdas de código ejecutadas sin errores; script también ejecutado el 9 de octubre. [Resultado](resultados/validacion.json): 180 filas, tres NaN, **61 registros de 08:00 a 09:00 UTC con extremos incluidos**, media del intervalo 22.587 °C y 18 ventanas de diez minutos. El conteo industrial distingue 40 valores/s de 20 mensajes/s; a 100 bytes por valor son 345.6 MB/día, sin overhead.

La variante incorpora un pico deliberado de 65 °C y lo conserva: la máxima media de diez minutos es 26.030 °C y la máxima media móvil, 30.425 °C. Ilustra pérdida de picos, no una avería observada. `tenperatura_beteta` usa interpolación temporal; `tenperatura_leundua` se calcula después sobre los valores rellenados y tiene solo cuatro NaN iniciales. Las respuestas del paso 19 aparecen junto al código. Con CSV docente habría que recalcular todos estos resultados.

[Gráfico de práctica](resultados/tenperatura.png), [descomposición](resultados/descomposicion.png) y [CSV con operaciones](resultados/practica.csv). La interpolación es retrospectiva; no se usa para entrenar el pronóstico. Descomposición con periodo 24 sobre 14 días sintéticos; test de las últimas 48 horas, baseline del último día de train repetido, MAE 2.1115 en unidades sintéticas. No prueba rendimiento energético real ni ausencia de sesgo temporal en otro modelo.

[Auditoría de dependencias](AUDITORIA_DEPENDENCIAS.json): sin vulnerabilidades conocidas detectadas en este entorno.
