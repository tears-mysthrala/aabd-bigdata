"""Comprueba eventos reales de Logstash, tipos, fechas y etiquetado del PDF."""

import json
from pathlib import Path


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


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
    require(len(events) == count, (practice, len(events)))
    for event in events:
        require(
            not {"_grokparsefailure", "_dateparsefailure"}.intersection(
                event.get("tags", [])
            ),
            'Eventos inválidos: not {"_grokparsefailure", "_dateparsefailure"}.intersection(             event.get("tags", [])         )',
        )
    if practice == "p18":
        e = events[0]
        require(
            e["maila"] == "ERROR" and e["zerbitzua"] == "nginx",
            'Eventos inválidos: e["maila"] == "ERROR" and e["zerbitzua"] == "nginx"',
        )
        require(
            e["mezua"] == "Connection refused" and e["bezero_ip"] == "203.0.113.5",
            'Eventos inválidos: e["mezua"] == "Connection refused" and e["bezero_ip"] == "203.0.113.5"',
        )
        require(
            e["@timestamp"] == "2026-10-05T08:30:45.000Z",
            'Eventos inválidos: e["@timestamp"] == "2026-10-05T08:30:45.000Z"',
        )
    else:
        require(
            [e["status_code"] for e in events] == EXPECTED[:count],
            'Eventos inválidos: [e["status_code"] for e in events] == EXPECTED[:count]',
        )
        require(
            all(type(e["status_code"]) is int for e in events),
            'Eventos inválidos: all(type(e["status_code"]) is int for e in events)',
        )
        require(
            events[0]["@timestamp"] == "2026-10-05T12:32:10.000Z",
            'Eventos inválidos: events[0]["@timestamp"] == "2026-10-05T12:32:10.000Z"',
        )
        require(
            events[1]["metodoa"] == "POST",
            'Eventos inválidos: events[1]["metodoa"] == "POST"',
        )
        if count == 6:
            require(
                events[3]["@timestamp"] == "2026-10-06T07:15:20.000Z",
                'Eventos inválidos: events[3]["@timestamp"] == "2026-10-06T07:15:20.000Z"',
            )
            require(
                events[5]["metodoa"] == "DELETE",
                'Eventos inválidos: events[5]["metodoa"] == "DELETE"',
            )
        for e in events:
            require(
                ("errorea" in e.get("tags", []))
                == (practice == "p22" and e["status_code"] >= 400),
                'Eventos inválidos: ("errorea" in e.get("tags", [])) == (                 practice == "p22" and e["status_code"] >= 400           ',
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
require(len(invalid) == 4, "Eventos inválidos: len(invalid) == 4")
require(
    all("_grokparsefailure" in e.get("tags", []) for e in invalid[:3]),
    'Eventos inválidos: all("_grokparsefailure" in e.get("tags", []) for e in invalid[:3])',
)
require(
    "_dateparsefailure" in invalid[3].get("tags", []),
    'Eventos inválidos: "_dateparsefailure" in invalid[3].get("tags", [])',
)
require(
    all("errorea" not in e.get("tags", []) for e in invalid),
    'Eventos inválidos: all("errorea" not in e.get("tags", []) for e in invalid)',
)
(ROOT / "evidencias" / "p22_invalid.events.json").write_text(
    json.dumps(invalid, indent=2) + "\n"
)
REPORT["p22_invalid"] = {"events": 4, "format_errors_visible": True, "verified": True}
(ROOT / "evidencias" / "validacion.json").write_text(
    json.dumps(REPORT, indent=2) + "\n"
)
print(json.dumps(REPORT, indent=2))
