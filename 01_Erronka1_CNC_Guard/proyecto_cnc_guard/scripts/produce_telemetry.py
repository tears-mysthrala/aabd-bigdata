"""Validate a source CSV; optionally publish stable CSV messages to Kafka.

Dry-run is the default; --publish requires a local laboratory broker.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from cnc_guard.events import to_csv_message

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--topic", default="cnc-telemetry-csv")
    parser.add_argument("--bootstrap", default="127.0.0.1:19095")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--errors", type=Path)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    if args.errors and args.errors.exists():
        parser.error("Error evidence already exists. Choose a new path.")
    producer = None
    if args.publish:
        from kafka import KafkaProducer

        producer = KafkaProducer(
            bootstrap_servers=args.bootstrap, acks="all", retries=3,
            value_serializer=lambda v: v.encode(), key_serializer=lambda v: v.encode(),
        )
    sent = invalid = duplicates = 0
    seen: set[str] = set()
    rejected = []
    try:
        with args.csv.open(encoding="utf-8-sig", newline="") as src:
            for rowno, row in enumerate(csv.DictReader(src), 2):
                if rowno > args.limit + 1:
                    break
                try:
                    wire, item = to_csv_message(row)
                    if item["event_id"] in seen:
                        duplicates += 1
                        continue
                    seen.add(item["event_id"])
                    if producer:
                        producer.send(args.topic, key=item["machine_id"], value=wire).get(timeout=20)
                    sent += 1
                except (ValueError, TypeError) as exc:
                    invalid += 1
                    rejected.append({"row": rowno, "reason": str(exc)})
    finally:
        if producer:
            producer.flush(timeout=30)
            producer.close()
    if args.errors:
        args.errors.parent.mkdir(parents=True, exist_ok=True)
        args.errors.write_text(
            json.dumps(rejected, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    print(json.dumps({"mode": "published" if args.publish else "validated-only",
                      "accepted": sent, "invalid": invalid, "duplicates": duplicates}))


if __name__ == "__main__":
    main()
