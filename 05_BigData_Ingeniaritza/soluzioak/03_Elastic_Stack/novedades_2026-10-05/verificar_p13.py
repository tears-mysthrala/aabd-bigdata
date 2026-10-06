#!/usr/bin/env python3
"""Send fresh requests and assert Apache -> shared volume -> Filebeat -> ES."""

import hashlib
import json
import re
import subprocess
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "evidencias"
OUT.mkdir(exist_ok=True)
TOKEN = "aabd" + uuid.uuid4().hex


def request(url, body=None, headers=None):
    req = urllib.request.Request(url, data=body, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.status, response.read(), dict(response.headers)
    except urllib.error.HTTPError as error:
        return error.code, error.read(), dict(error.headers)


requests = []
etag = None
for path in ["/"] * 8 + ["/proba", "/ikasleak", "/ez-dago"] * 2 + ["/"]:
    headers = {"If-None-Match": etag} if len(requests) == 14 else {}
    status, _, response_headers = request(
        f"http://127.0.0.1:18080{path}?run={TOKEN}", headers=headers
    )
    if not requests:
        etag = response_headers["ETag"]
    requests.append({"path": path, "status": status})
assert [r["status"] for r in requests] == [200] * 8 + [404] * 6 + [304], requests

logs = {}
for service, path in [
    ("apache", "/usr/local/apache2/logs/access_log"),
    ("filebeat", "/var/log/apache/access_log"),
]:
    logs[service] = subprocess.check_output(
        ["docker", "compose", "exec", "-T", service, "cat", path], cwd=BASE
    ).decode()
    (OUT / f"p13_{service}_access.log").write_text(logs[service])
assert logs["apache"] == logs["filebeat"], "Shared log contents differ"
expected = [line for line in logs["apache"].splitlines() if TOKEN in line]
assert len(expected) == 15, expected

query = json.dumps({"size": 100, "query": {"match": {"message": TOKEN}}}).encode()
deadline = time.monotonic() + 180
while True:
    status, raw, _ = request(
        "http://127.0.0.1:19200/filebeat-*/_search",
        query,
        {"Content-Type": "application/json"},
    )
    response = json.loads(raw)
    hits = response.get("hits", {}).get("hits", [])
    if len(hits) >= 15:
        break
    if time.monotonic() > deadline:
        raise RuntimeError(f"Filebeat ingestion timeout: HTTP {status}, {response}")
    time.sleep(3)
messages = [hit["_source"]["message"] for hit in hits]
assert sorted(messages) == sorted(expected), (
    "ES does not contain the exact original Apache lines"
)
assert all("@timestamp" in hit["_source"] for hit in hits)
statuses = [int(re.search(r'" (\d{3}) ', m).group(1)) for m in messages]
result = {
    "verified_at_utc": datetime.now(timezone.utc).isoformat(),
    "request_batch_id": TOKEN,
    "requests": requests,
    "shared_log_equal": True,
    "shared_log_sha256": hashlib.sha256(logs["apache"].encode()).hexdigest(),
    "http_status_counts": {str(s): statuses.count(s) for s in sorted(set(statuses))},
    "es_document_count_this_run": len(hits),
    "original_lines_equal_es_messages": True,
    "search_response": response,
}
(OUT / "p13_resultado.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n"
)
print(json.dumps({k: v for k, v in result.items() if k != "search_response"}, indent=2))
