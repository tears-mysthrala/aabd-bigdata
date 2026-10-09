# %% [markdown]
# # Denbora Serieak — práctica de 19 pasos, edición 2026-10-09
# Enunciado: [02_Denbora_Serieak.pdf](../../materialak/02_Denbora_Serieak.pdf). Respuestas y práctica Pandas; el documento no incluye `sentsorea.csv` y no se ha encontrado ese archivo en el repositorio. Generamos una **variante sintética explícita**, no mediciones de una fábrica. Ejecutar desde esta carpeta; resultados bajo `resultados/`. No modifica servicios NiFi/Kafka.

# %% [markdown]
# ## 1. Regularidad, muestreo y calidad
# Situaciones: 1 temperatura cada 5s regular; 2 alerta al abrir puerta irregular; 3 CPU por minuto regular; 4 parada de máquina irregular; 5 energía cada 15min regular; 6 botón/log irregular. «Regular» describe el calendario esperado, no que nunca se pierdan datos.
# 100ms = 0.1s: 10 muestras/s, 600/min, 36.000/h, 864.000/día por sensor. Para 500: 5.000/s, 300.000/min, 18.000.000/h, 432.000.000/día. Son valores escalares, sin bytes/protocolo/índices; estimar almacenamiento requiere tamaño y retención.
# Tabla de 10:00–10:06: falta 10:05, 85.2 a las 10:03 es sospechoso y 10:06/21.8 está duplicado. Esperamos cadencia de un minuto. 85.2 puede ser fallo, unidad incorrecta o evento real: marcar/investigar, no borrarlo automáticamente.
# Patrones A–D: A tendencia, B estacionalidad diaria, C ciclo de carga/descarga (si fija duración también puede ser estacional), D ruido. Descomposición aditiva: observado=tendencia+estacional+residuo; el residuo puede incluir anomalías/estructura, no es necesariamente ruido blanco.

# %%
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.seasonal import seasonal_decompose

if "__file__" in globals():
    exercise_dir = Path(__file__).resolve().parent
else:
    exercise_dir = Path.cwd()
    if not (exercise_dir / "denbora_serieak.ipynb").is_file():
        exercise_dir = exercise_dir / "06_NiFi" / "soluzioak" / "08_Denbora_Serieak"
    if not (exercise_dir / "denbora_serieak.ipynb").is_file():
        raise RuntimeError(
            "Ejecuta el notebook desde su carpeta o desde la raiz del repositorio"
        )
OUTPUT = exercise_dir / "resultados"
OUTPUT.mkdir(exist_ok=True)
assert [10, 10 * 60, 10 * 3600, 10 * 86400] == [10, 600, 36000, 864000]
raw_example = pd.DataFrame(
    {
        "timestamp": pd.to_datetime(
            [
                "2026-10-01 10:00",
                "2026-10-01 10:01",
                "2026-10-01 10:02",
                "2026-10-01 10:03",
                "2026-10-01 10:04",
                "2026-10-01 10:06",
                "2026-10-01 10:06",
            ]
        ),
        "tenperatura": [21.1, 21.3, 21.4, 85.2, 21.6, 21.8, 21.8],
    }
)
assert raw_example.duplicated().sum() == 1
missing_times = pd.date_range(
    raw_example.timestamp.min(), raw_example.timestamp.max(), freq="min"
).difference(raw_example.timestamp)
assert list(missing_times) == [pd.Timestamp("2026-10-01 10:05")]
print(raw_example[raw_example.tenperatura > 50])
print("Falta:", missing_times.tolist())
# Cadencia UTC para evitar ambigüedad de zona/horario de verano.
rng = np.random.default_rng(42)
index = pd.date_range("2026-10-01 07:00", periods=180, freq="min", tz="UTC")
temperature = 21 + 0.01 * np.arange(180) + rng.normal(0, 0.15, 180)
vibration = 0.2 + rng.normal(0, 0.015, 180)
temperature[[20, 21, 90]] = np.nan
temperature[75] = 65.0  # Pico deliberado: no representa una avería real.
fixture = pd.DataFrame(
    {"timestamp": index, "tenperatura": temperature, "bibrazioa": vibration}
)
fixture.to_csv(OUTPUT / "sentsorea_sintetikoa.csv", index=False)

# %% [markdown]
# ## 2. Práctica Pandas, pasos 1–18
# Pasos 1–5: importar, cargar, ordenar, mostrar head y shape. Pasos 6–7: usar 08:00–09:00 inclusivo, como el `.loc` docente: 61 registros a cadencia de un minuto. La media corresponde solo a ese intervalo. Pasos 8–10: resample de las dos magnitudes y conteo de filas. Pasos 11–13: identificar NaN, interpolar por tiempo en una columna nueva y mostrar temperaturas superiores a 50 °C sin eliminarlas. Pasos 14–15: rolling de cinco valores sobre la temperatura ya interpolada y gráfico. Pasos 16–18: ejecutar este script y comprobar sus salidas. La interpolación es retrospectiva; usa información futura y no sirve como imputación causal en predicción online. UTC es una convención explícita de la variante sintética.

# %%
df = pd.read_csv(
    OUTPUT / "sentsorea_sintetikoa.csv",
    parse_dates=["timestamp"],
    index_col="timestamp",
)
df = df.sort_index()
assert (
    isinstance(df.index, pd.DatetimeIndex)
    and df.index.is_monotonic_increasing
    and df.index.is_unique
)
print("Primeras cinco filas:")
print(df.head())
print("Filas y columnas:", df.shape)
hour = df.loc["2026-10-01 08:00":"2026-10-01 09:00"]
hour_mean = hour.tenperatura.mean()
print("Intervalo 08:00–09:00 (extremos incluidos):")
print(hour.to_string())
print("Media del intervalo:", hour_mean)
assert len(hour) == 61
assert hour.index.min().hour == 8 and hour.index.max().hour == 9
assert np.isclose(hour_mean, hour.tenperatura.sum() / hour.tenperatura.count())
assert not np.isclose(hour_mean, df.tenperatura.mean())
means = df.resample("10min").mean()
counts = df.resample("10min").count()
print("Media por 10 minutos:")
print(means)
print("Filas resample:", len(means))
print("Valores disponibles por ventana:")
print(counts)
original = df.tenperatura.copy()
print("NaN por columna:")
print(df.isna().sum())
assert original.isna().sum() == 3
df["tenperatura_beteta"] = original.interpolate(method="time", limit_area="inside")
interpolated = df.tenperatura_beteta
df["tenperatura_leundua"] = interpolated.rolling(window=5, min_periods=5).mean()
smoothed = df.tenperatura_leundua
anomalies = df.loc[original > 50, ["tenperatura", "bibrazioa"]]
print("Temperaturas superiores a 50 °C (conservadas):")
print(anomalies)
assert len(anomalies) == 1 and anomalies.tenperatura.iloc[0] == 65.0
assert interpolated.isna().sum() == 0
assert np.isclose(
    interpolated.iloc[20],
    original.iloc[19] + (original.iloc[22] - original.iloc[19]) / 3,
)
assert smoothed.iloc[:4].isna().all()
assert smoothed.iloc[4:].notna().all()
assert np.isclose(smoothed.iloc[22], interpolated.iloc[18:23].mean())
assert len(means) == 18
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df.index, original, label="Original (huecos)")
ax.plot(df.index, smoothed, label="Media móvil 5")
ax.plot(df.index, interpolated, alpha=0.4, label="Interpolación retrospectiva")
ax.set(xlabel="Tiempo UTC", ylabel="Temperatura sintética (°C)")
ax.legend()
fig.tight_layout()
fig.savefig(OUTPUT / "tenperatura.png")
plt.show()
df.to_csv(OUTPUT / "practica.csv")

# %% [markdown]
# Paso 19 — interpretación: tendencia ascendente diseñada de 0.01°C/min y ruido normal de σ=0.15°C. El rolling suaviza las oscilaciones, pero retrasa cambios. Faltan tres temperaturas, rellenadas retrospectivamente entre valores observados; conservar el original permite distinguir medición y estimación. Hay un pico deliberado de 65 °C: en una fábrica habría que contrastarlo con vibración, calibración y eventos antes de decidir si es error o problema real. Resample reduce 180 filas a 18 ventanas; rolling conserva 180 filas con cuatro NaN iniciales. Las medias atenúan el pico: por eso se conservarían también máximos, alertas y datos originales. No inferimos estacionalidad diaria de tres horas ni una avería a partir de datos sintéticos.
#
# ## 3. Sistema IoT de 20 máquinas
# Dos magnitudes por máquina cada segundo: 40 valores escalares/s, 3.456.000/día. Si ambos viajan en un mensaje por máquina: 20 mensajes/s y 1.728.000/día. Cadencia regular esperada. Problemas: timestamps desordenados/reloj, pérdidas, reintentos duplicados, unidades, outliers, ruido y drift.
# Si cada medición escalar ocupa 100 bytes: 345.600.000 bytes/día = 345.6 MB decimales = 329.59 MiB, sin índices, réplicas ni protocolo. Si «medición» significa mensaje que reúne ambas magnitudes, serían 172.8 MB/día a 100 bytes/mensaje. La ambigüedad se declara, no se mezclan las dos cuentas. Diez minutos de promedios pierden picos, duración y orden de eventos; conservar máximo, count y originales con retención adecuada. Grafana sobre TSDB permitiría visualizar la temperatura temporal.
# Diseño: sensor → buffer edge → ingesta NiFi → Kafka (clave máquina, orden por partición) → consumidor/TSDB para consultas temporales → Elastic/dashboard según necesidad. Kafka desacopla y permite replay; no reemplaza una política de retención ni hace exactamente una vez todo el sistema. Guardar unidades, sensor, tiempo de evento UTC, tiempo de recepción, quality flag y ID para deduplicar; conservar evidencia antes de corregir. Elegir TSDB por consultas/retención/volumen, Mongo por esquema flexible y Elastic por búsqueda, sin obligar a usar todos.
# Analizar tendencias de temperatura, anomalías de vibración y periodicidad por turnos. Son candidatos a investigar, no predicción demostrada de fallos.
#
# ## 4. Actividad adicional y proyecto del índice
# (a) último intervalo: filtro temporal; (b) segundos a minutos: resample con agregación adecuada; (c) ruido: rolling con ventana justificada; (d) tres faltantes: investigar y rellenar solo si razonable con flags; (e) pico diario a las 08:00: estacionalidad, comparar días suficientes.
# El índice menciona un proyecto de energía pero este PDF no desarrolla un enunciado/dataset. Añadimos una extensión sintética de descomposición y predicción temporal claramente delimitada; no se inventa una entrega del profesor.

# %%

energy_index = pd.date_range("2026-09-01", periods=24 * 14, freq="h", tz="UTC")
energy = pd.Series(
    100
    + 0.05 * np.arange(len(energy_index))
    + 10 * np.sin(2 * np.pi * np.arange(len(energy_index)) / 24)
    + rng.normal(0, 1, len(energy_index)),
    index=energy_index,
    name="energia_sintetica",
)
decomp = seasonal_decompose(energy, model="additive", period=24)
valid = decomp.trend.notna() & decomp.resid.notna()
assert np.allclose(
    energy[valid], (decomp.trend + decomp.seasonal + decomp.resid)[valid]
)
fig = decomp.plot()
fig.tight_layout()
fig.savefig(OUTPUT / "descomposicion.png")
plt.show()
# Pronóstico de las últimas 48 horas: baseline de repetición diaria recursiva.
train, test = energy.iloc[:-48], energy.iloc[-48:]
pred = pd.Series(np.tile(train.iloc[-24:].to_numpy(), 2), index=test.index)
mae = mean_absolute_error(test, pred)
assert train.index.max() < test.index.min()
assert len(pred) == 48 and np.isfinite(mae)
print("MAE seasonal-naive (energía sintética):", mae)
report = {
    "source": "synthetic_seed_42",
    "practice_rows": len(df),
    "missing_temperature": int(original.isna().sum()),
    "selected_hour_rows": len(hour),
    "selected_hour_mean": float(hour_mean),
    "selected_interval": "2026-10-01 08:00–09:00 UTC, inclusive",
    "resample_rows": len(means),
    "anomalies_above_50": len(anomalies),
    "original_peak": float(original.max()),
    "resample_peak": float(means.tenperatura.max()),
    "rolling_peak": float(smoothed.max()),
    "rolling_missing_after_warmup": int(smoothed.iloc[4:].isna().sum()),
    "sensor_values_per_day_20_machines": 40 * 86400,
    "bytes_per_day_100_bytes_per_scalar": 40 * 86400 * 100,
    "energy_test_hours": 48,
    "energy_mae": float(mae),
}
(OUTPUT / "validacion.json").write_text(json.dumps(report, indent=2) + "\n")

# %% [markdown]
# La descomposición es retrospectiva, no se usa como feature del pronóstico: puede utilizar observaciones futuras. El baseline usa solo el último día de train repetido para dos días, sin realimentarse con test. MAE es error absoluto en unidades sintéticas, no calidad de una predicción energética real. Comparar otros modelos exigiría validación por tiempo y evitar imputar/escalar con test. Pendiente: `sentsorea.csv` real, interpretación de sus datos y cualquier ingestión/GUI que se quiera implementar; el PDF de práctica solo exige Pandas.
