"""DF2.3 Medallion simulazioa sintetikoki; ez da NiFi/AEMET exekuzioaren froga.

Bronze: JSON sintetikoak (AEMETen payload erreala ez da hemen erabiltzen) -> bronze/
Silver: EvaluateJsonPath + AttributesToJSON -> silver/*.json + silver_mongo.jsonl
Gold: MergeContent(10) + QueryRecord (AVG/MAX/MIN per hiria) -> gold/*.parquet + gold_mongo.jsonl
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
BRONZE = HERE / "bronze"
SILVER = HERE / "silver"
GOLD = HERE / "gold"
N = 10
HIRIAK = ["Gasteiz", "Bilbo", "Donostia"]


def bronze() -> list[Path]:
    BRONZE.mkdir(exist_ok=True)
    base = datetime(2026, 9, 22, 8, 0, 0)
    out = []
    for i in range(N):
        ts = (base + timedelta(seconds=30 * i)).strftime("%Y-%m-%d_%H-%M-%S")
        raw = {
            "municipio": {"NOMBRE": HIRIAK[i % len(HIRIAK)]},
            "temperatura_actual": round(14.0 + (i % 5) * 0.7 + (i % len(HIRIAK)) * 0.3, 1),
            "humedad": 55 + (i * 3) % 20,
            "presion": 1012 - (i % 4),
            "fecha_raw": ts,
        }
        p = BRONZE / f"{ts}.json"
        p.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
        out.append(p)
    return out


def silver(raw_files: list[Path]) -> pd.DataFrame:
    SILVER.mkdir(exist_ok=True)
    rows = []
    for p in raw_files:
        raw = json.loads(p.read_text(encoding="utf-8"))
        # EvaluateJsonPath: $.municipio.NOMBRE, $.temperatura_actual, $.humedad
        curated = {
            "fecha": raw["fecha_raw"],
            "hiria": raw["municipio"]["NOMBRE"],
            "tenperatura": float(raw["temperatura_actual"]),
            "hezetasuna": int(raw["humedad"]),
            "presioa": int(raw["presion"]),
        }
        (SILVER / f"{raw['fecha_raw']}.json").write_text(
            json.dumps(curated, ensure_ascii=False), encoding="utf-8"
        )
        rows.append(curated)
    df = pd.DataFrame(rows)
    # PutMongo 7kasua-silver (simulazioa: JSONL biltegi bikoitza)
    with (SILVER / "silver_mongo.jsonl").open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return df


def gold(df: pd.DataFrame) -> pd.DataFrame:
    GOLD.mkdir(exist_ok=True)
    assert len(df) == N, f"MergeContent: 10 espero, {len(df)}"
    # QueryRecord: hiria, max(fecha), avg(tenperatura), avg(hezetasuna), min(presioa)
    agg = (
        df.groupby("hiria", as_index=False)
        .agg(fecha=("fecha", "max"), tenperatura=("tenperatura", "mean"),
             hezetasuna=("hezetasuna", "mean"), presioa=("presioa", "min"))
        .round({"tenperatura": 2, "hezetasuna": 2})
    )
    agg.to_parquet(GOLD / "tempMedia.parquet", index=False)
    agg.to_json(GOLD / "tempMedia.json", orient="records", force_ascii=False, indent=2)
    with (GOLD / "gold_mongo.jsonl").open("w", encoding="utf-8") as fh:
        for r in agg.to_dict(orient="records"):
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return agg


def main() -> None:
    raw = bronze()
    assert len(raw) == N
    df = silver(raw)
    assert len(df) == N and set(df["hiria"]) == set(HIRIAK)
    agg = gold(df)
    assert len(agg) == len(HIRIAK)
    print(f"bronze={len(raw)} silver={len(df)} gold_hiriak={len(agg)}")
    print(agg.to_string(index=False))
    print("OK — DF2.3 Medallion ebidentziak bronze/ silver/ gold/-n.")


if __name__ == "__main__":
    main()
