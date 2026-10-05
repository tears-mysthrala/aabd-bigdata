#!/usr/bin/env python3
"""Create the lab-only data view and print a Discover URL for the verified run."""

import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "evidencias"
ID = "aabd-novedades-filebeat"
HOST = "http://127.0.0.1:15601"


def call(path, body=None):
    req = urllib.request.Request(
        HOST + path,
        data=json.dumps(body).encode() if body else None,
        headers={"Content-Type": "application/json", "kbn-xsrf": "lab"},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)


status = call("/api/status")
assert status["status"]["overall"]["level"] == "available", status["status"]["overall"]
(OUT / "kibana_status.json").write_text(json.dumps(status, indent=2) + "\n")
try:
    view = call(f"/api/data_views/data_view/{ID}")
except urllib.error.HTTPError as error:
    if error.code != 404:
        raise
    view = call(
        "/api/data_views/data_view",
        {
            "data_view": {
                "id": ID,
                "title": "filebeat-*",
                "name": "P13 Apache Filebeat",
                "timeFieldName": "@timestamp",
            }
        },
    )
assert view["data_view"]["title"] == "filebeat-*"
assert view["data_view"]["timeFieldName"] == "@timestamp"
(OUT / "kibana_data_view.json").write_text(json.dumps(view, indent=2) + "\n")
result = json.loads((OUT / "p13_resultado.json").read_text())
day = result["verified_at_utc"][:10]
state_g = f"(time:(from:'{day}T00:00:00.000Z',to:'{day}T23:59:59.999Z'))"
state_a = f"(columns:!(message),index:'{ID}',query:(language:kuery,query:'message: \"{result['request_batch_id']}\"'))"
url = HOST + "/app/discover#/?" + urllib.parse.urlencode({"_g": state_g, "_a": state_a})
(OUT / "discover_url.txt").write_text(url + "\n")
print(url)
