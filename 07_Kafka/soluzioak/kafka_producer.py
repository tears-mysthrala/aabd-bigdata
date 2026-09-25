"""KafkaProducer Python-en (PDF 10.3, localhost-era egokitua + --mock modua).

Broker errealarekin:
    python kafka_producer.py --topic iabd-topic --n 10
Broker gabe (test/didáktika):
    python kafka_producer.py --mock --mock-file mock_log.jsonl --n 10
"""

from __future__ import annotations

import argparse
import csv as csvlib
import json
import os
import time
from itertools import islice
from pathlib import Path

DEFAULT_TOPIC = os.environ.get("TOPIC", "iabd-topic")
DEFAULT_BOOTSTRAP = os.environ.get("BOOTSTRAP", "localhost:9092")


def build_message(i: int) -> dict:
    return {"izena": f"ekoizlea {i}"}


def run_mock(n: int, mock_file: Path) -> int:
    with mock_file.open("w", encoding="utf-8") as fh:
        for i in range(n):
            fh.write(json.dumps(build_message(i), ensure_ascii=False) + "\n")
    return n


def run_kafka(
    n: int,
    topic: str,
    bootstrap: str,
    keys: bool,
    interval: float,
    csv: str | None = None,
    skip: int = 0,
) -> int:
    from json import dumps

    from kafka import KafkaProducer

    producer = KafkaProducer(
        value_serializer=lambda m: dumps(m).encode("utf-8"),
        key_serializer=(lambda k: k.encode("utf-8")) if keys else None,
        bootstrap_servers=[bootstrap],
        linger_ms=20,
        batch_size=64 * 1024,
        acks="all",
    )

    def messages():
        if csv:
            with open(csv, encoding="utf-8", newline="") as fh:
                reader = csvlib.DictReader(fh)
                yield from islice(reader, skip, None if n <= 0 else skip + n)
        else:
            for i in range(n):
                yield build_message(i)

    confirmed = 0
    pending = []
    try:
        for i, message in enumerate(messages()):
            key = (message.get("makina_id", "") if csv else f"gakoa{i % 2}") if keys else None
            pending.append(producer.send(topic, value=message, key=key))
            if len(pending) == 1000:
                for future in pending:
                    future.get(timeout=30)
                confirmed += len(pending)
                pending.clear()
            if interval > 0:
                time.sleep(interval)
        for future in pending:
            future.get(timeout=30)
        confirmed += len(pending)
    finally:
        producer.close()
    return confirmed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", default=DEFAULT_TOPIC)
    ap.add_argument("--bootstrap", default=DEFAULT_BOOTSTRAP)
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument(
        "--keys", action="store_true", help="gakoak bidali (partizio-banaketa)"
    )
    ap.add_argument(
        "--interval", type=float, default=0.0, help="segundo arteko pausa (demo: 0.2)"
    )
    ap.add_argument(
        "--csv",
        default=None,
        help="CSV-etik bidali (Dituen zutabeak JSON gisa, lehen n lerroak)",
    )
    ap.add_argument(
        "--skip", type=int, default=0, help="CSV lerroak saltatu (producers paralelos)"
    )
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--mock-file", default="mock_log.jsonl")
    args = ap.parse_args()
    if args.n < 0 or args.skip < 0 or args.interval < 0:
        ap.error("--n, --skip eta --interval ezin dira negatiboak izan")
    if args.mock:
        sent = run_mock(args.n, Path(args.mock_file))
        print(f"mock: {sent} mezu {args.mock_file}-n")
    else:
        t0 = time.time()
        sent = run_kafka(
            args.n,
            args.topic,
            args.bootstrap,
            args.keys,
            args.interval,
            args.csv,
            args.skip,
        )
        dt = time.time() - t0
        print(f"kafka: {sent} ACK mezu -> {args.topic} ({dt:.1f}s, {sent / dt:.0f}/s)")


if __name__ == "__main__":
    main()
