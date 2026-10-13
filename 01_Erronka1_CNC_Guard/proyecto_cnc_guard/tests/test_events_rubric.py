"""Data quality, schema, idempotence and alert contracts."""

from __future__ import annotations

import pytest

from cnc_guard.events import alert_document, classify_alert, normalize_record


def sample():
    return {
        "ts": 1700000000,
        "makina_id": "M1",
        "tenperatura": "64.2",
        "bibrazioa": "3.4",
        "presioa": "1013.8",
    }


def test_deterministic_event_identity_and_types():
    a, b = normalize_record(sample()), normalize_record(sample())
    assert a == b
    assert a["sha256"] == a["event_id"]
    assert isinstance(a["temperature"], float)
    assert a["timestamp"].endswith("+00:00")


@pytest.mark.parametrize(
    "changes",
    [
        {"ts": "garbage"},
        {"bibrazioa": None},
        {"tenperatura": float("nan")},
        {"presioa": -1},
        {"makina_id": " "},
        {"bibrazioa": -5},
    ],
)
def test_bad_telemetry_rejected(changes):
    with pytest.raises(ValueError):
        normalize_record({**sample(), **changes})


def test_missing_fields_and_alert_boundaries():
    with pytest.raises(ValueError, match="Missing fields"):
        normalize_record({"ts": 1700000000})
    assert classify_alert(0.149) == "OK"
    assert classify_alert(0.15) == "AVISO"
    assert classify_alert(0.7) == "CRITICA"


def test_alert_document_matches_strict_elasticsearch_template():
    event_id = normalize_record(sample())["event_id"]
    response = {
        "machine_id": "M1",
        "timestamp": "2026-10-13T09:00:00Z",
        "failure_predicted": True,
        "failure_probability": 0.7,
        "alert_level": "CRITICA",
        "history_available": False,
        "model_schema": 1,
    }
    doc = alert_document(event_id, response)
    assert doc["event_id"] == event_id
    assert "@timestamp" in doc and "timestamp" not in doc
    assert doc["alert_level"] == "CRITICA"
    with pytest.raises(ValueError, match="scoring-response"):
        alert_document(event_id, {**response, "unexpected": "field"})
    with pytest.raises(ValueError, match="Alert level"):
        alert_document(event_id, {**response, "alert_level": "OK"})
    with pytest.raises(ValueError, match="event_id"):
        alert_document("invalid", response)
