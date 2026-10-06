#!/usr/bin/env python3
"""Recheck saved runtime evidence; does not run NiFi or contact any service."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq


def verify(folder: Path) -> dict:
    report = json.loads((folder / "validacion.json").read_text())
    paths = {"bronze": "bronze.json", "silver": "silver.json", "gold": "gold.parquet"}
    manifest = {obj["layer"]: obj for obj in report["s3_objects"]}
    assert set(manifest) == set(paths), "Expected one object per Medallion layer"
    for layer, name in paths.items():
        raw = (folder / name).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == manifest[layer]["sha256"], name
        assert len(raw) == manifest[layer]["bytes"], name
    bronze = json.loads((folder / paths["bronze"]).read_text())
    silver = json.loads((folder / paths["silver"]).read_text())
    parquet = pq.read_table(folder / paths["gold"])
    gold = parquet.to_pylist()
    assert len(silver) == report["silver_rows"] == 24
    assert parquet.num_rows == report["gold_rows"] == 1
    assert bronze["utc_offset_seconds"] == 0
    assert bronze["hourly_units"]["temperature_2m"] == "°C"
    assert bronze["hourly_units"]["relative_humidity_2m"] == "%"
    hourly = bronze["hourly"]
    assert len(hourly["time"]) == len(hourly["temperature_2m"]) == len(hourly["relative_humidity_2m"]) == 24
    assert len({row["timestamp_utc"] for row in silver}) == 24
    times = []
    for index, row in enumerate(silver):
        assert type(row["temperatura_c"]) is float and type(row["humedad_pct"]) is float
        assert math.isfinite(row["temperatura_c"]) and 0 <= row["humedad_pct"] <= 100
        assert row["timestamp_utc"] == hourly["time"][index] + ":00Z"
        assert row["temperatura_c"] == hourly["temperature_2m"][index]
        assert row["humedad_pct"] == hourly["relative_humidity_2m"][index]
        assert row["provider"] == "open-meteo" and row["data_kind"] == "modeled_forecast"
        assert row["timezone"] == "UTC"
        assert row["source_url"] == report["source_url"]
        assert row["source_object"] == manifest["bronze"]["key"]
        assert row["fetched_at_utc"] == report["request_started_at_utc"]
        instant = datetime.fromisoformat(row["timestamp_utc"])
        assert instant.utcoffset().total_seconds() == 0
        times.append(instant)
    assert all((right - left).total_seconds() == 3600 for left, right in zip(times, times[1:]))
    result = gold[0]
    assert result["n_hours"] == result["n_distinct_hours"] == 24
    assert result["start_utc"] == silver[0]["timestamp_utc"]
    assert result["end_utc"] == silver[-1]["timestamp_utc"]
    for key in ["municipio", "provider", "data_kind", "timezone", "source_url", "source_object", "fetched_at_utc"]:
        assert result[key] == silver[0][key]
    temps = [row["temperatura_c"] for row in silver]
    humidity = [row["humedad_pct"] for row in silver]
    expected = {"temperatura_media_c": sum(temps) / 24,
                "temperatura_min_c": min(temps), "temperatura_max_c": max(temps),
                "humedad_media_pct": sum(humidity) / 24}
    for name, value in expected.items():
        assert pa.types.is_floating(parquet.schema.field(name).type), name
        assert math.isclose(result[name], value, rel_tol=1e-12, abs_tol=1e-12), name
    assert pa.types.is_integer(parquet.schema.field("n_hours").type)
    mongo_silver = json.loads((folder / "mongo_silver.json").read_text())
    mongo_gold = json.loads((folder / "mongo_gold.json").read_text())
    assert sorted(mongo_silver, key=lambda row: row["timestamp_utc"]) == sorted(silver, key=lambda row: row["timestamp_utc"])
    assert mongo_gold == gold == [report["gold"]]
    assert len(mongo_silver) == report["mongo_silver_documents"] == 24
    assert len(mongo_gold) == report["mongo_gold_documents"] == 1
    return {"status": "saved_evidence_valid", "provider": "open-meteo",
            "silver_hours": 24, "gold_records": 1, "aggregates": expected,
            "runtime_utc": report["validated_utc"],
            "scope": "Rechecks saved artifacts; does not execute NiFi or certify a new live run"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence_dir", nargs="?", type=Path,
                        default=Path(__file__).parent / "evidencias_open_meteo_2026-10-02")
    args = parser.parse_args()
    print(json.dumps(verify(args.evidence_dir), ensure_ascii=False, indent=2))
