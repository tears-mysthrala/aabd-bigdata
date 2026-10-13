"""Validate, normalize, and fingerprint telemetry without hiding invalid records."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

REQUIRED = ("ts", "makina_id", "tenperatura", "bibrazioa", "presioa")
FIELDS = ("temperature", "vibration", "pressure")


def normalize_record(record: dict) -> dict:
    """Map canonical course CSV keys to the API/Elasticsearch contract."""
    if not isinstance(record, dict):
        raise ValueError("record must be an object")
    missing = [k for k in REQUIRED if k not in record]
    if missing:
        raise ValueError(f"Missing fields: {missing}")
    try:
        timestamp = datetime.fromtimestamp(int(record["ts"]), tz=timezone.utc)
        machine = str(record["makina_id"])
        readings = {
            "temperature": float(record["tenperatura"]),
            "vibration": float(record["bibrazioa"]),
            "pressure": float(record["presioa"]),
        }
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("Invalid timestamp or sensor type") from exc
    if not machine or len(machine) > 32 or not all(c.isalnum() or c in "_-" for c in machine):
        raise ValueError("Invalid machine identifier")
    if not (-40 <= readings["temperature"] <= 200 and
            0 <= readings["vibration"] <= 100 and
            0 <= readings["pressure"] <= 5000):
        raise ValueError("Sensor out of range")
    if not all(__import__("math").isfinite(v) for v in readings.values()):
        raise ValueError("Sensor value must be finite")
    payload = {"machine_id": machine, "timestamp": timestamp.isoformat(), **readings}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return {**payload, "event_id": digest, "sha256": digest}


def classify_alert(probability: float) -> str:
    if not 0 <= probability <= 1:
        raise ValueError("Probability must be in [0, 1]")
    return "CRITICA" if probability >= 0.7 else "AVISO" if probability >= 0.15 else "OK"
