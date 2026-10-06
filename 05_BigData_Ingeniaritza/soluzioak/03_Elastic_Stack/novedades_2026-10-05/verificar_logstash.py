#!/usr/bin/env python3
"""Assert actual Logstash output, including invalid date and Grok failures."""

import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent / "evidencias"
events = {}
for practice in ("p15", "p16", "p17"):
    events[practice] = []
    for line in (OUT / f"{practice}.stdout.log").read_text().splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and "@timestamp" in value:
            events[practice].append(value)
    (OUT / f"{practice}.events.json").write_text(
        json.dumps(events[practice], indent=2, ensure_ascii=False) + "\n"
    )

p15 = events["p15"]
assert len(p15) == 5, p15
assert [
    (e["bezero_ip"], e["metodoa"], e["request"], e["status_code"], e["bytes"])
    for e in p15[:4]
] == [
    ("192.168.1.105", "GET", "/api", "500", "1234"),
    ("10.0.0.25", "POST", "/login", "200", "856"),
    ("10.0.0.25", "POST", "/login", "401", "856"),
    ("10.0.0.25", "POST", "/login", "401", "856"),
]
assert p15[2]["erabiltzailea"] == "erabiltzailea 1"
assert p15[3]["data"] == "2026-10-04"
assert "_grokparsefailure" in p15[4]["tags"]
assert all("_grokparsefailure" not in e.get("tags", []) for e in p15[:4])

p16 = events["p16"]
assert len(p16) == 3, p16
assert p16[0]["timestamp"] == "30/Sep/2026:10:30:45"
assert p16[0]["@timestamp"] == "2026-09-30T08:30:45.000Z"
assert (
    p16[0]["bezero_ip"],
    p16[0]["metodoa"],
    p16[0]["request"],
    p16[0]["status_code"],
) == ("192.168.1.105", "GET", "/api", "500")
assert "_dateparsefailure" in p16[1]["tags"]
assert "_grokparsefailure" in p16[2]["tags"]

p17 = events["p17"]
assert len(p17) == 1, p17
e = p17[0]
assert type(e["status_code"]) is int and e["status_code"] == 500
assert type(e["bytes"]) is int and e["bytes"] == 1234
assert e["uri"] == "/api" and "request" not in e and "message" not in e
assert e["bezero_ip"] == "192.168.1.105" and e["metodoa"] == "GET"
result = {
    "verified_at_utc": datetime.now(timezone.utc).isoformat(),
    "events_per_practice": {p: len(v) for p, v in events.items()},
    "p15_variants": "OK",
    "p15_invalid_ip": "_grokparsefailure",
    "p16_timestamp": p16[0]["@timestamp"],
    "p16_invalid_date": "_dateparsefailure",
    "p16_invalid_structure": "_grokparsefailure",
    "p17_integer_rename_remove": "OK",
}
(OUT / "logstash_verificacion.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
