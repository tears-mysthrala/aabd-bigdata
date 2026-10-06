#!/usr/bin/env python3
"""Validate saved accessibility snapshots; this does not replace a fresh GUI run."""

import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent / "evidencias"
discover = (OUT / "p13_discover_snapshot.txt").read_text()
assert "Documents ( 15 )" in discover
for status in (200, 304, 404):
    assert re.search(rf'HTTP/1\.1\\" {status} ', discover), status
document = (
    (OUT / "p13_documento_message_snapshot.txt")
    .read_text()
    .split('dialog "Document"', 1)[1]
)
assert "message" in document and "HTTP/1.1" in document and "304" in document
results = {}
for variant in ("usuario", "fecha"):
    snapshot = (OUT / f"p15_{variant}_grok_snapshot.txt").read_text()
    section = snapshot.split('StaticText "json code block:"', 1)[1]
    pieces = re.findall(r'- StaticText (".*")', section)
    result = json.loads("".join(json.loads(piece) for piece in pieces))
    assert (
        result["bezero_ip"],
        result["metodoa"],
        result["request"],
        result["status_code"],
        result["bytes"],
    ) == ("10.0.0.25", "POST", "/login", "401", "856")
    if variant == "usuario":
        assert result["erabiltzailea"] == "erabiltzailea 1"
    else:
        assert result["data"] == "2026-10-04"
    results[variant] = result
report = {
    "source": "actual agent-browser accessibility snapshots",
    "p13_discover_documents": 15,
    "p13_visible_codes": [200, 304, 404],
    "p13_open_document_message": True,
    "p15_structured_data": results,
}
(OUT / "gui_verificacion.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n"
)
print(json.dumps(report, ensure_ascii=False, indent=2))
