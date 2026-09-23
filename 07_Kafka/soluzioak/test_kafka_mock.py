"""Roundtrip mock test: producer --mock -> consumer --mock (brokerrik gabe)."""

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent


def run(*args: str) -> str:
    r = subprocess.run(
        [sys.executable, *args], cwd=HERE, capture_output=True, text=True
    )
    assert r.returncode == 0, r.stderr
    return r.stdout


def test_mock_roundtrip(tmp_path) -> None:
    mock = tmp_path / "mock_log.jsonl"
    run("kafka_producer.py", "--mock", "--mock-file", str(mock), "--n", "10")
    lines = mock.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 10, len(lines)
    assert json.loads(lines[0]) == {"izena": "ekoizlea 0"}
    out = run("kafka_consumer.py", "--mock", "--mock-file", str(mock), "--max", "10")
    assert "ekoizlea 9" in out
