"""Pure tests for CSV -> NiFi -> API wire format."""

from __future__ import annotations

import csv
from io import StringIO

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
