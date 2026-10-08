"""Comprueba eventos reales de Logstash, tipos, fechas y etiquetado del PDF."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = [500, 200, 404, 200, 401, 403]
REPORT = {}
for practice, count in (("p18", 1), ("p20", 3), ("p21", 6), ("p22", 6)):
    events = []
    for line in (
        (ROOT / "evidencias" / f"{practice}.stdout.log").read_text().splitlines()
    ):
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict) and "message" in event and "@timestamp" in event:
            events.append(event)
    assert len(events) == count, (practice, len(events))
    for event in events:
        assert not {"_grokparsefailure", "_dateparsefailure"}.intersection(
            event.get("tags", [])
        )
    if practice == "p18":
        e = events[0]
        assert e["maila"] == "ERROR" and e["zerbitzua"] == "nginx"
        assert e["mezua"] == "Connection refused" and e["bezero_ip"] == "203.0.113.5"
        assert e["@timestamp"] == "2026-10-05T08:30:45.000Z"
    else:
        assert [e["status_code"] for e in events] == EXPECTED[:count]
        assert all(type(e["status_code"]) is int for e in events)
        assert events[0]["@timestamp"] == "2026-10-05T12:32:10.000Z"
        assert events[1]["metodoa"] == "POST"
        if count == 6:
            assert events[3]["@timestamp"] == "2026-10-06T07:15:20.000Z"
            assert events[5]["metodoa"] == "DELETE"
        for e in events:
            assert ("errorea" in e.get("tags", [])) == (
                practice == "p22" and e["status_code"] >= 400
            )
    (ROOT / "evidencias" / f"{practice}.events.json").write_text(
        json.dumps(events, indent=2) + "\n"
    )
    REPORT[practice] = {"events": count, "verified": True}
# Los errores de formato deben quedar visibles, sin confundirse con HTTP válido.
invalid = []
for line in (ROOT / "evidencias" / "p22_invalid.stdout.log").read_text().splitlines():
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        continue
    if isinstance(event, dict) and "message" in event and "@timestamp" in event:
        invalid.append(event)
assert len(invalid) == 4
assert all("_grokparsefailure" in e.get("tags", []) for e in invalid[:3])
assert "_dateparsefailure" in invalid[3].get("tags", [])
assert all("errorea" not in e.get("tags", []) for e in invalid)
(ROOT / "evidencias" / "p22_invalid.events.json").write_text(
    json.dumps(invalid, indent=2) + "\n"
)
REPORT["p22_invalid"] = {"events": 4, "format_errors_visible": True, "verified": True}
(ROOT / "evidencias" / "validacion.json").write_text(
    json.dumps(REPORT, indent=2) + "\n"
)
print(json.dumps(REPORT, indent=2))
