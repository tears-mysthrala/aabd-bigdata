"""Pure tests for CSV -> NiFi -> API wire format."""

from __future__ import annotations

import csv
import importlib.util
import json
import sys
import types
from io import StringIO
from pathlib import Path

import pytest

from cnc_guard.events import OUTPUT_COLUMNS, normalize_record, to_csv_message


def record():
    return {
        "ts": 1700000000,
        "makina_id": "M3",
        "tenperatura": 68.1,
        "bibrazioa": 3.3,
        "presioa": 1009,
        "errorea": 1,
    }


def test_csv_message_one_row_with_stable_identity():
    wire, data = to_csv_message(record())
    parsed = next(csv.reader(StringIO(wire)))
    assert len(parsed) == len(OUTPUT_COLUMNS)
    assert parsed[1] == "M3"
    assert parsed[0] == data["event_id"]
    assert data["event_id"] == normalize_record(record())["event_id"]
    assert "errorea" not in OUTPUT_COLUMNS


def test_invalid_source_rejected():
    with pytest.raises(ValueError):
        to_csv_message({**record(), "tenperatura": "missing"})



def test_kafka_delivery_failure_preserves_evidence(monkeypatch, tmp_path):
    """A publish failure must produce a nonzero exit and retained error evidence."""

    class FakeKafkaError(Exception):
        pass

    class FailedFuture:
        def get(self, *, timeout):
            raise FakeKafkaError("Kafka broker refused delivery")

    class FailedProducer:
        def __init__(self, **kwargs):
            pass

        def send(self, *args, **kwargs):
            return FailedFuture()

        def flush(self, *, timeout):
            return None

        def close(self):
            return None

    kafka = types.ModuleType("kafka")
    kafka_errors = types.ModuleType("kafka.errors")
    kafka.KafkaProducer = FailedProducer
    kafka_errors.KafkaError = FakeKafkaError
    monkeypatch.setitem(sys.modules, "kafka", kafka)
    monkeypatch.setitem(sys.modules, "kafka.errors", kafka_errors)

    script = Path(__file__).resolve().parents[1] / "scripts" / "produce_telemetry.py"
    spec = importlib.util.spec_from_file_location("test_producer", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    src = tmp_path / "telemetry.csv"
    with src.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(record()))
        writer.writeheader()
        writer.writerow(record())
    evidence = tmp_path / "rejects.json"
    monkeypatch.setattr(
        sys, "argv",
        ["produce_telemetry", "--csv", str(src), "--limit", "1", "--publish",
         "--errors", str(evidence)],
    )
    with pytest.raises(SystemExit) as raised:
        module.main()
    assert raised.value.code == 1
    rows = json.loads(evidence.read_text(encoding="utf-8"))
    assert rows == [{"row": 2, "stage": "kafka_delivery", "reason": "FakeKafkaError"}]
