# UCI Auto MPG — datos para regresión en Orange

El fichero `auto_mpg_weight.tab` es una selección reproducible de **398 coches** del conjunto [Auto MPG de UCI](https://archive.ics.uci.edu/dataset/9/auto). Conserva `mpg` (millas por galón, variable objetivo), `weight` (peso en libras, predictor) y `car_name` como metadato. Los seis registros con potencia ausente no afectan a este modelo porque `horsepower` no se usa; no se descartan observaciones ni se imputan valores.

El modelo del ejercicio es la regresión lineal simple `mpg ~ weight`. Se elige un predictor para poder interpretar la pendiente en unidades comprensibles y estudiar con un diagrama de dispersión una pregunta concreta: cómo se asocia el peso de los coches de esta muestra con su consumo urbano. El nombre del coche es solo un identificador; no se introduce como predictor.

## Procedencia y licencia

- Conjunto: Auto MPG, R. Quinlan (1993), UCI Machine Learning Repository.
- DOI: [10.24432/C5859H](https://doi.org/10.24432/C5859H).
- Licencia indicada por UCI: Creative Commons Attribution 4.0 International (CC BY 4.0).
- Se incluyen `auto-mpg.data` y `auto-mpg.names` tal como aparecen en el archivo oficial para hacer trazable la transformación.
- Para regenerar la tabla de Orange, ejecuta `python preparatu_auto_mpg.py`. Si los ficheros de origen no están presentes, descarga el ZIP oficial de UCI.

La muestra histórica cubre coches de los años modelo 1970–1982 y mide consumo en ciclo urbano; no es una estimación del consumo de vehículos actuales ni representa necesariamente otros mercados.
