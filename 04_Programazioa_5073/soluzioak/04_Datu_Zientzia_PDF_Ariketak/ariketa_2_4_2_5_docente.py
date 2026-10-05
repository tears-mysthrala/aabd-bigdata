# %%
"""Nuevas tablas docentes 2.4/2.5; fuentes originales solo de lectura."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
SOURCE_DIR = HERE.parents[1] / "data" / "mock_datuak"
SALES_CSV = SOURCE_DIR / "Ariketa2.4" / "salmentak.csv"
OUTPUT_DIR = HERE / "data" / "docente_2_4_2_5"


def agregatu_salmentak(df: pd.DataFrame | None = None) -> dict:
    """CSV docente por defecto; el máximo es una suma de ciudad/categoría."""
    if df is None:
        df = pd.read_csv(SALES_CSV)
    expected = {"hiria", "kategoria", "produktua", "salmenta"}
    if not expected.issubset(df.columns) or df.empty:
        raise ValueError(
            "2.4 requiere ventas no vacías: hiria,kategoria,produktua,salmenta"
        )
    salm_hiriak = df.groupby("hiria")["salmenta"].sum().sort_values(ascending=False)
    agg_kategoriak = df.groupby("kategoria")["salmenta"].agg(["mean", "max", "count"])
    pivot = df.pivot_table(
        index="hiria",
        columns="kategoria",
        values="salmenta",
        aggfunc="sum",
        fill_value=0,
    )
    # GUZTIRA ayuda a comprobar sumas, pero nunca compite como ciudad/categoría.
    pivot_totals = df.pivot_table(
        index="hiria",
        columns="kategoria",
        values="salmenta",
        aggfunc="sum",
        fill_value=0,
        margins=True,
        margins_name="GUZTIRA",
    )
    combinations = pivot.stack()
    bikote_max = combinations.idxmax()
    balio_max = float(combinations.loc[bikote_max])
    individual = df.loc[df["salmenta"].idxmax()]
    print("=== 2.4: HIRI BAKOITZEKO SALMENTA OSOA ===\n", salm_hiriak)
    print("\nKATEGORIAKO MEAN/MAX/COUNT:\n", agg_kategoriak.round(2))
    print("\nPIVOT (SUM), GUZTIRA BARNE:\n", pivot_totals)
    print(f"\nKonbinazio gorena: {bikote_max[0]} x {bikote_max[1]} = {balio_max:.0f} €")
    print(
        f"Salmenta indibiduala (beste kontzeptu bat): {individual['hiria']} x "
        f"{individual['kategoria']} = {individual['salmenta']:.0f} €"
    )
    return {
        "salm_hiriak": salm_hiriak,
        "agg_kategoriak": agg_kategoriak,
        "pivot": pivot,
        "pivot_totals": pivot_totals,
        "bikote_max": bikote_max,
        "balio_max": balio_max,
        "max_individual": individual,
        "rows": len(df),
    }


# %%
def taulak_docente() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Copia literal de las tablas de la celda 97, no de los CSV mal etiquetados."""
    bezeroak = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "izena": ["Ane", "Mikel", "Leire", "Jon", "Amaia"],
            "hiri_id": [10, 20, 10, 30, np.nan],
        }
    )
    hiriak = pd.DataFrame(
        {
            "id": [10, 20, 30, 40],
            "hiri_izena": ["Bilbo", "Donostia", "Gasteiz", "Iruñea"],
            "probintzia": ["Bizkaia", "Gipuzkoa", "Araba", "Nafarroa"],
        }
    )
    return bezeroak, hiriak


def batu_taulak(bezeroak=None, hiriak=None) -> dict:
    """Inner/left de celda 97 y concat mensual de seis ventas."""
    if bezeroak is None and hiriak is None:
        bezeroak, hiriak = taulak_docente()
    if bezeroak is None or hiriak is None:
        raise ValueError("Proporciona las dos tablas o ninguna")
    kwargs = {
        "left_on": "hiri_id",
        "right_on": "id",
        "suffixes": ("_bez", "_hiri"),
        "validate": "many_to_one",
    }
    inner = pd.merge(bezeroak, hiriak, how="inner", **kwargs)
    left = pd.merge(bezeroak, hiriak, how="left", **kwargs)
    urtarrila = pd.DataFrame({"bezero_id": [1, 2, 3], "salmenta": [120, 80, 95]})
    otsaila = pd.DataFrame({"bezero_id": [1, 4, 5], "salmenta": [150, 200, 60]})
    concat = pd.concat(
        [urtarrila.assign(hila="urtarrila"), otsaila.assign(hila="otsaila")],
        ignore_index=True,
    )
    print("\n=== 2.5: TABLAS EMBEBIDAS DEL NOTEBOOK DOCENTE, CELDA 97 ===")
    print("INNER JOIN:\n", inner)
    print("\nLEFT JOIN:\n", left)
    print("\nCONCAT:\n", concat)
    return {"inner": inner, "left": left, "concat": concat}


# %%
def egiaztatu_csv_2_5() -> list[dict]:
    """Evidencia reproducible de esquema; no repara ni consume estos CSV para JOIN."""
    info = []
    for name, expected in [
        ("bezeroak.csv", {"id", "izena", "hiri_id"}),
        ("hiriak.csv", {"id", "hiri_izena", "probintzia"}),
    ]:
        path = SOURCE_DIR / "Ariketa2.5" / name
        df = pd.read_csv(path)
        info.append(
            {
                "file": str(path.relative_to(HERE.parents[2])),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "rows": len(df),
                "columns": list(df.columns),
                "expected_columns": sorted(expected),
                "schema_valid": expected.issubset(df.columns),
            }
        )
    return info


def registrar_resultados() -> dict:
    sales = agregatu_salmentak()
    joins = batu_taulak()
    invalid = egiaztatu_csv_2_5()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sales["pivot_totals"].to_csv(OUTPUT_DIR / "pivot_2_4.csv")
    sales["agg_kategoriak"].to_csv(OUTPUT_DIR / "kategoriak_2_4.csv")
    for key, frame in joins.items():
        frame.to_csv(OUTPUT_DIR / f"{key}_2_5.csv", index=False)
    summary = {
        "source_2_4": str(SALES_CSV.relative_to(HERE.parents[2])),
        "sha256_2_4": hashlib.sha256(SALES_CSV.read_bytes()).hexdigest(),
        "source_2_5": "materialak/2_SOLUZIOAK_URLa.ipynb, celda 97 (índice base 0)",
        "rows_2_4": sales["rows"],
        "max_group": {
            "hiria": sales["bikote_max"][0],
            "kategoria": sales["bikote_max"][1],
            "salmenta": sales["balio_max"],
        },
        "max_individual": {
            k: sales["max_individual"][k] for k in ["hiria", "kategoria", "salmenta"]
        },
        "city_totals": {k: float(v) for k, v in sales["salm_hiriak"].items()},
        "inner_rows": len(joins["inner"]),
        "left_rows": len(joins["left"]),
        "concat_rows": len(joins["concat"]),
        "concat_total": int(joins["concat"]["salmenta"].sum()),
        "invalid_csv_2_5": invalid,
    }
    (OUTPUT_DIR / "emaitzak.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        "\nCSV 2.5: esquema incompatible; originales conservados.\n",
        json.dumps(invalid, indent=2),
    )
    return summary


if __name__ == "__main__":
    registrar_resultados()
