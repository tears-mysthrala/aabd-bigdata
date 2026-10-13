#!/usr/bin/env python3
"""Preview/register the MongoDB sink from this local lab's properties files."""

import argparse
import json
import urllib.request
from pathlib import Path

API = "http://127.0.0.1:18084"


def get(path):
    with urllib.request.urlopen(API + path, timeout=20) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("connector", choices=["mongo-sink-curated"])
    parser.add_argument(
        "--aplicar", action="store_true", help="POST the connector to the local lab"
    )
    args = parser.parse_args()
    path = Path(__file__).resolve().parent / f"config/{args.connector}.properties"
    properties = {}
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#"):
            key, value = line.split("=", 1)
            properties[key.strip()] = value.strip()
    name = properties.pop("name")
    body = {"name": name, "config": properties}
    if not args.aplicar:
        print(json.dumps(body, indent=2))
        print("Preview only. Use --aplicar to register in this local lab.")
        return
    if name in get("/connectors"):
        print("Existing connector preserved; no configuration overwritten.")
        return
    request = urllib.request.Request(
        API + "/connectors",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
    print(json.dumps({"registered": result["name"], "http_status": response.status}))


if __name__ == "__main__":
    main()
