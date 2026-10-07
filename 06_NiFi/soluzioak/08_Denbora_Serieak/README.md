# Series temporales — todas las actividades del PDF

Enunciado: [02_Denbora_Serieak.pdf](../../materialak/02_Denbora_Serieak.pdf).
[Cuaderno completo](denbora_serieak.ipynb) y [script equivalente](denbora_serieak.py).

Cubre clasificación regular/irregular, cálculo de muestras, los cinco problemas de calidad, patrones A–D, diseño IoT de 20 máquinas, las nueve tareas Pandas y cinco asociaciones finales. El índice del PDF menciona energía sin desarrollar un enunciado: la extensión de descomposición/pronóstico se identifica como añadida.

## Ejecutar

Desde esta carpeta, Python 3.13 y uv:

```bash
uv sync --frozen
MPLBACKEND=Agg uv run --frozen python denbora_serieak.py
```

Para el notebook seleccionar `.venv/bin/python` como kernel y ejecutar en orden desde esta carpeta. El script sobrescribe sus artefactos propios en `resultados/`: CSV sintético, CSV de operaciones, dos PNG y JSON de validación. Copiarlos antes si se quiere conservar una ejecución distinta. No modifica servicios ni descarga datos.

No está disponible el `sentsorea.csv` docente. La variante sintética declara semilla, tendencia, ruido y huecos; sus conclusiones no describen una fábrica real. Tampoco se ha ejecutado un pipeline NiFi/Kafka: el ejercicio Pandas no lo pide. La arquitectura IoT es una respuesta de diseño.

## Evidencias

[Ejecución del notebook](EJECUCION.json): tres celdas ejecutadas sin errores; script también ejecutado. [Resultado](resultados/validacion.json): 180 filas, tres NaN, 60 minutos seleccionados y 18 ventanas de diez minutos. El conteo industrial distingue 40 valores/s de 20 mensajes/s.

[Gráfico de práctica](resultados/tenperatura.png), [descomposición](resultados/descomposicion.png) y [CSV con operaciones](resultados/practica.csv). La interpolación es retrospectiva; no se usa para entrenar el pronóstico. Descomposición con periodo 24 sobre 14 días sintéticos; test de las últimas 48 horas, baseline del último día de train repetido, MAE 2.1115 en unidades sintéticas. No prueba rendimiento energético real ni ausencia de sesgo temporal en otro modelo.

[Auditoría de dependencias](AUDITORIA_DEPENDENCIAS.json): sin vulnerabilidades conocidas detectadas en este entorno.
