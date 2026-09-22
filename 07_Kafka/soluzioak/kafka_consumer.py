"""KafkaConsumer Python-en (PDF 10.2, localhost-era egokitua + --mock modua).

Broker errealarekin:
    python kafka_consumer.py --topic iabd-topic --group iabd-taldea-1
Broker gabe:
    python kafka_consumer.py --mock --mock-file mock_log.jsonl --max 10
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import os

DEFAULT_TOPIC = os.environ.get("TOPIC", "iabd-topic")
DEFAULT_GROUP = os.environ.get("GROUP", "iabd-taldea-1")
DEFAULT_BOOTSTRAP = os.environ.get("BOOTSTRAP", "localhost:9092")


def run_mock(mock_file: Path, max_msgs: int, quiet: bool = False) -> list[dict]:
    out = []
    with mock_file.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
            if len(out) >= max_msgs:
                break
    if not quiet:
        for m in out:
            print(m)
    return out


def run_kafka(topic: str, group: str, bootstrap: str, max_msgs: int, quiet: bool = False) -> None:
    from kafka import KafkaConsumer
    from json import loads

    consumer = KafkaConsumer(
        topic,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=group,
        value_deserializer=lambda m: loads(m.decode("utf-8")),
        bootstrap_servers=[bootstrap],
        consumer_timeout_ms=10000,
    )
    try:
        n = 0
        for m in consumer:
            if not quiet:
                print(m.value)  # m.topic, m.partition, m.offset, m.key, m.timestamp
            n += 1
            if n >= max_msgs:
                break
        print(f"kafka: {n} mezu irakurrita ({topic}/{group})")
    finally:
        consumer.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", default=DEFAULT_TOPIC)
    ap.add_argument("--group", default=DEFAULT_GROUP)
    ap.add_argument("--bootstrap", default=DEFAULT_BOOTSTRAP)
    ap.add_argument("--max", type=int, default=10)
    ap.add_argument("--quiet", action="store_true", help="zenbatu bakarrik (bolumen handietarako)")
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--mock-file", default="mock_log.jsonl")
    args = ap.parse_args()
    if args.mock:
        out = run_mock(Path(args.mock_file), args.max, args.quiet)
        print(f"mock: {len(out)} mezu irakurrita")
    else:
        run_kafka(args.topic, args.group, args.bootstrap, args.max, args.quiet)


if __name__ == "__main__":
    main()
