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

DEFAULT_TOPIC = "iabd-topic"
DEFAULT_GROUP = "iabd-taldea-1"
DEFAULT_BOOTSTRAP = "localhost:9092"


def run_mock(mock_file: Path, max_msgs: int) -> list[dict]:
    out = []
    with mock_file.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
            if len(out) >= max_msgs:
                break
    for m in out:
        print(m)
    return out


def run_kafka(topic: str, group: str, bootstrap: str, max_msgs: int) -> None:
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
        for i, m in enumerate(consumer):
            print(m.value)  # m.topic, m.partition, m.offset, m.key, m.timestamp
            if i + 1 >= max_msgs:
                break
    finally:
        consumer.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", default=DEFAULT_TOPIC)
    ap.add_argument("--group", default=DEFAULT_GROUP)
    ap.add_argument("--bootstrap", default=DEFAULT_BOOTSTRAP)
    ap.add_argument("--max", type=int, default=10)
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--mock-file", default="mock_log.jsonl")
    args = ap.parse_args()
    if args.mock:
        out = run_mock(Path(args.mock_file), args.max)
        print(f"mock: {len(out)} mezu irakurrita")
    else:
        run_kafka(args.topic, args.group, args.bootstrap, args.max)


if __name__ == "__main__":
    main()
