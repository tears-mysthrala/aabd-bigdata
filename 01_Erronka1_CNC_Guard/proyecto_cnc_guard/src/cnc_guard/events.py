"""Validate, normalize, and fingerprint telemetry without hiding invalid records."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import re
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
    if not (
        -40 <= readings["temperature"] <= 200
        and 0 <= readings["vibration"] <= 100
        and 0 <= readings["pressure"] <= 5000
    ):
        raise ValueError("Sensor out of range")
    if not all(math.isfinite(v) for v in readings.values()):
        raise ValueError("Sensor value must be finite")
    payload = {"machine_id": machine, "timestamp": timestamp.isoformat(), **readings}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return {**payload, "event_id": digest, "sha256": digest}


def classify_alert(probability: float) -> str:
    if not 0 <= probability <= 1:
        raise ValueError("Probability must be in [0, 1]")
    return "CRITICA" if probability >= 0.7 else "AVISO" if probability >= 0.15 else "OK"


OUTPUT_COLUMNS = ("event_id", "machine_id", "timestamp", "temperature", "vibration", "pressure")


def to_csv_message(original: dict) -> tuple[str, dict]:
    """One validated, schema-stable CSV record for a Kafka message."""
    normalized = normalize_record(original)
    output = io.StringIO()
    csv.writer(output, lineterminator="").writerow(
        [normalized[column] for column in OUTPUT_COLUMNS]
    )
    return output.getvalue(), normalized


ALERT_DOCUMENT_FIELDS = (
    "machine_id", "timestamp", "failure_predicted",
    "failure_probability", "alert_level", "history_available", "model_schema",
)


def alert_document(event_id: str, prediction: dict) -> dict:
    """Translate a /predict response into the strict Elasticsearch alert contract.

    NiFi must preserve the original input event_id; the scoring API does not
    invent one. Use event_id as Elasticsearch _id for idempotent replay.
    """
    if not isinstance(event_id, str) or re.fullmatch(r"[0-9a-f]{64}", event_id) is None:
        raise ValueError("event_id must be lowercase SHA-256")
    if not isinstance(prediction, dict) or set(prediction) != set(ALERT_DOCUMENT_FIELDS):
        raise ValueError("Invalid scoring-response fields")
    raw_time = prediction["timestamp"]
    if not isinstance(raw_time, str):
        raise ValueError("timestamp must be an ISO8601 string")
    try:
        parsed = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Invalid scoring timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError("timestamp requires a timezone")
    if (not isinstance(prediction["machine_id"], str)
            or not prediction["machine_id"].strip()):
        raise ValueError("machine_id missing")
    probability = prediction["failure_probability"]
    if isinstance(probability, bool) or not isinstance(probability, (int, float)):
        raise ValueError("failure_probability must be numeric")
    if not math.isfinite(probability) or not 0 <= probability <= 1:
        raise ValueError("failure_probability must be finite in [0,1]")
    for field in ("failure_predicted", "history_available"):
        if type(prediction[field]) is not bool:
            raise ValueError(f"{field} must be boolean")
    if type(prediction["model_schema"]) is not int:
        raise ValueError("model_schema must be an integer")
    if prediction["alert_level"] != classify_alert(probability):
        raise ValueError("Alert level does not match probability")
    return {
        "event_id": event_id,
        "@timestamp": parsed.isoformat(),
        **{k: prediction[k] for k in ALERT_DOCUMENT_FIELDS if k != "timestamp"},
    }
