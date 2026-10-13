# %% [markdown]
# # Retos adicionales · PDF recuperado el 9 de octubre
# Fuente: [02_Denbora_Serieak.pdf](../../materialak/02_Denbora_Serieak.pdf),
# páginas «1. erronka: Anomaliak detektatu», «2. erronka: Zein agregazio da
# egokiena?» y «Azken errepasoa». El PDF actualizado añade estas tres páginas.
# Ejecutar aquí primero `uv run --frozen python denbora_serieak.py` y después
# `uv run --frozen python retos_adicionales.py`. Lee la variante sintética previa;
# no representa mediciones reales. Sobrescribe solo resultados/retos_adicionales.json.

# %%
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()


def alert_episodes(series, threshold=50, consecutive=3, cadence="1min"):
    """Una alerta al completar N medidas consecutivas, sin unir huecos/NaN."""
    if (
        consecutive < 1
        or not series.index.is_monotonic_increasing
        or not series.index.is_unique
    ):
        raise ValueError("Índice temporal ordenado y único; consecutive >= 1")
    count, previous, alerts = 0, None, []
    for timestamp, value in series.items():
        if pd.notna(value) and np.isfinite(value) and value > threshold:
            count = (
                count + 1
                if previous is not None
                and timestamp - previous == pd.Timedelta(cadence)
                else 1
            )
        else:
            count = 0
        alerts.append(count == consecutive)
        previous = timestamp
    return pd.Series(alerts, index=series.index, name="alerta_episodio")


# %% [markdown]
# ## Reto 1: temperatura > 50 °C
# Seleccionar con `df[df.tenperatura > 50]`, mostrar hora y temperatura, y contar
# lecturas: en la variante sintética hay un único pico deliberado de 65 °C.
# Un umbral solo no demuestra una avería. Revisar calibración, unidad, rango,
# persistencia y otros sensores/eventos; conservar la lectura y su quality flag.
# El PDF sitúa el rango habitual en 40–50 °C; esta variante reutiliza la práctica
# sintética anterior, cuyo fondo es 21–23 °C. Solo demuestra el filtro >50 y la
# persistencia; no reproduce el régimen físico de la máquina del enunciado.
#
# Tres medidas consecutivas reducen alertas de picos aislados, pero retrasan
# detección y pueden omitir episodios breves. Un NaN o hueco temporal rompe la
# secuencia. Emitimos una alerta por episodio al alcanzar la tercera medida,
# no una alerta por cada lectura posterior. No se ordena detener ninguna máquina.


# %%
def run():
    output = HERE / "resultados"
    df = pd.read_csv(
        output / "sentsorea_sintetikoa.csv",
        parse_dates=["timestamp"],
        index_col="timestamp",
    ).sort_index()
    above = df.loc[df.tenperatura > 50, ["tenperatura"]]
    sustained = alert_episodes(df.tenperatura)
    print("Horas y temperaturas superiores a 50 °C:", above.to_string(), sep="\n")
    print(
        "Alertas por lectura:",
        len(above),
        "; episodios de tres consecutivas:",
        int(sustained.sum()),
    )
    assert len(above) == 1 and above.tenperatura.iloc[0] == 65
    assert sustained.sum() == 0
    aggregated = df.tenperatura.resample("10min").agg(
        ["mean", "max", "min", "count", "size"]
    )
    assert int(aggregated["size"].sum()) == len(df)
    assert int(aggregated["count"].sum()) == df.tenperatura.notna().sum()
    report = {
        "source": "synthetic_seed_42; variante previa, no usa el CSV docente",
        "alerts_per_reading": len(above),
        "alerts_three_consecutive": int(sustained.sum()),
        "above_50": [
            {"timestamp": str(t), "temperature": float(v)}
            for t, v in above.tenperatura.items()
        ],
        "aggregation_answers": {
            "average_temperature": "mean",
            "highest_temperature": "max",
            "lowest_temperature": "min",
            "measurement_rows": "size (count solo valores no nulos)",
            "interval_kwh": "sum",
        },
        "review_answers": [
            "loc",
            "resample",
            "rolling",
            "interpolate",
            "estacionalidad",
        ],
    }
    (output / "retos_adicionales.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(aggregated.to_string())
    return report


if __name__ == "__main__":
    results = run()

# %% [markdown]
# ## Reto 2: elegir agregación y justificar unidades
# Media de temperatura: **mean**; temperatura más alta: **max**; más baja: **min**.
# Número de registros recibidos: **size**; **count** cuenta solo no nulos por
# columna. La variante permite comprobar la diferencia por sus tres NaN.
# Energía si cada dato ya es kWh consumido durante su intervalo: **sum**.
# Si es lectura acumulativa del contador, usar diferencias tratando reinicios;
# si es potencia en kW, integrar con la duración, no sumar kW como si fueran kWh.
# ## Repaso: emparejamientos razonados
# 1. Consultar última hora: **loc** con límites temporales.
# 2. Segundos a medias por minuto: **resample** y **mean**.
# 3. Suavizar pequeñas oscilaciones: **rolling**, con ventana justificada.
# 4. Estimar temperatura faltante: **interpolate**, conservando marca de calidad;
# una interpolación retrospectiva no sirve sin más para predicción online.
# 5. Pico repetido cada día a las 08:00: **estacionalidad diaria**; hace falta
# observar varios días, no se demuestra con las tres horas de esta variante.
