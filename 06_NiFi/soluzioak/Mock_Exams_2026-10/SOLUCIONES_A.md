# Soluciones y rúbrica — NiFi y series temporales, simulacro A

[Volver al examen](../../materialak/Mock_Exams_2026-10/EXAMEN_A.md).
Corrección propuesta, no baremo docente. Se admiten alternativas coherentes con
los requisitos. Concede crédito parcial por razonamiento correcto aunque haya
un error aritmético posterior; no cuentes dos veces el mismo mérito.
Los valores calculados son respuestas de casos sintéticos, no resultados de planta.

## 1 — 2 puntos

Content son bytes del payload, attributes metadatos clave/valor; cambiar atributo
no convierte contenido. Processor realiza operación; Connection almacena cola;
Relationship dirige resultados; back pressure limita entrada al alcanzar umbral.
Controller Service comparte/configura lectura/escritura o conexiones, no procesa
por sí mismo un flujo. Provenance traza eventos del dato; logs describen ejecución
y errores. 0.5 cada apartado.

## 2 — 2.5 puntos

GetFile (o ListFile+FetchFile con seguimiento) → ConvertRecord → QueryRecord →
PutFile. En ConvertRecord: CSVReader con cabecera y esquema id int, ciudad string,
precio numérico, unidades int; JsonRecordSetWriter con salida array de objetos.
En QueryRecord: JsonTreeReader para ese JSON y JsonRecordSetWriter de salida;
no reutilizar un Reader CSV sobre contenido ya convertido. Consulta válida:
`SELECT * FROM FLOWFILE WHERE precio >= 0 AND ciudad = 'Eibar'`.
Salida dos registros IDs 1 y 3; pueden quedar juntos en un FlowFile. Para auditar
rechazos, separar precio<0 de válidos de otras ciudades, sin ocultar descartes.
UpdateAttribute con fuente/instante y nombre único o política de conflicto fail.
Failure a cuarentena, transitorios con retry acotado; verificar tres entradas,
una inválida, dos aceptadas, contenido/tipos y eventos provenance. No afirmar
3 FlowFiles si un CSV contiene 3 registros. Puntos 1/0.5/0.5/0.5.

## 3 — 2 puntos

DBCPConnectionPool con credenciales externas → ExecuteSQLRecord con Writer JSONL
→ SplitText (una línea por FlowFile) → PutMongo con MongoDBControllerService.
Aceptar PutMongoRecord con Reader compatible, alternativa indicada en la página
31. ID estable y modo upsert permiten tratar repeticiones del caso; verificar
conteo y documento, no solo cola vacía. Bronze conserva original, Silver
normaliza campos y Gold agrega. En el caso NiFi del material, MergeContent
reúne diez FlowFiles; con salida JSONL, separar objetos con salto de línea y
leerlos mediante JsonTreeReader antes de QueryRecord AVG/MAX/COUNT. Evitar unir
objetos sin separador o mezclar un array JSON con una configuración JSONL.
InvokeHTTP realiza GET a la URL configurada; UpdateAttribute añade fecha/nombre
y PutFile conserva la respuesta sin transformar en Bronze. Comprobar contenido
y recorrido en provenance. No se evalúan watermarks ni errores concretos de
proveedores que solo se observaron en ejecuciones locales. 0.75/0.75/0.5.

## 4 — 2.5 puntos

```python
from io import StringIO

import matplotlib.pyplot as plt
import pandas as pd

# csv_text = bloque CSV del enunciado copiado literalmente
frame = pd.read_csv(StringIO(csv_text))
frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
df = frame.set_index("timestamp").sort_index()
intervalo = df.loc["2026-10-09 08:01":"2026-10-09 08:03"]
ventanas = df.resample("5min", closed="left", label="left").agg(
    {"temperatura": "mean", "kwh_intervalo": "sum"}
)
df["rellena"] = df["temperatura"].interpolate(method="time")
df["suave"] = df["rellena"].rolling(3, min_periods=3).mean()
```

Intervalo tiene 3 filas, media **54 °C**. Ventanas temperatura **50.5 y 44**;
kWh **7 y 1**. Rellena 08:04=**50**; primera rolling en 08:02:
(40+52+54)/3=**48.6667**. Lecturas >50 originales: 08:01,02,03;
tercera lectura alerta en **08:03**. Continuación para detectar solo el comienzo
de cada episodio (usar temperatura original):

```python
run = 0
previous = None
alerts = []
for timestamp, value in df["temperatura"].items():
    contiguous = previous is not None and timestamp - previous == pd.Timedelta("1min")
    high = pd.notna(value) and value > 50
    run = (run + 1 if contiguous else 1) if high else 0
    if run == 3:
        alerts.append(timestamp)
    previous = timestamp
assert alerts == [pd.Timestamp("2026-10-09T08:03:00Z")]
```

Un hueco reinicia la racha con uno si la nueva lectura es alta; NaN/valor<=50
la reinicia con cero. Interpolados no activan alertas.
Resample agrega ventanas temporales; rolling(3) las últimas tres filas.
El suavizado reduce oscilaciones, pero puede ocultar el pico de 08:03.
La interpolación estima; no recupera una medición real. Continuación:

```python
ax = df[["temperatura", "suave"]].plot(marker="o")
ax.set(
    title="Temperatura original y suavizada",
    xlabel="Hora (UTC)",
    ylabel="Temperatura (°C)",
)
ax.grid(True)
ax.figure.tight_layout()
ax.figure.savefig("temperatura_mock.png", dpi=140)
plt.close(ax.figure)
```

Se genera el gráfico en la carpeta de trabajo de esta práctica; se sobrescribe
solo esa figura al repetir. La explicación acompaña al gráfico y a los cálculos.
Rúbrica 0.5 por apartado.

## 5 — 1 punto

**20 mensajes/s**, **40 valores/s**, 3.456.000 valores/día,
345.600.000 bytes=**345.6 MB/día**, sin IDs, timestamps, transporte ni réplicas.
Medias ocultan picos y duración de episodios. Temperatura máxima=max,
mínima=min, número de lecturas=conteo, energía en kWh de intervalos=sum.
Con temperaturas ausentes, indicar si se cuentan filas recibidas o mediciones
válidas; aquí se recibieron seis filas y cinco temperaturas. No se exige una
API concreta de conteo. 0.5/0.5.
