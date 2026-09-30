#!/usr/bin/env python3
"""2. kasua — Python consumer: Partition | Offset | Key | Value.

Erabilera:
  BOOTSTRAP=127.0.0.1:19092 TOPIC=codex-personas GROUP=codex-personas-py \
    python personas_consumer.py [--max 10] [--from-beginning]
"""

import argparse
import os
import sys

from kafka import KafkaConsumer


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=0, help="0 = mugagabea")
    ap.add_argument("--from-beginning", action="store_true")
    args = ap.parse_args()

    bootstrap = os.environ.get("BOOTSTRAP", "127.0.0.1:19092")
    topic = os.environ.get("TOPIC", "codex-personas")
    group = os.environ.get("GROUP")
    if not group:
        print("GROUP ingurune-aldagaia behar da", file=sys.stderr)
        return 2

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap.split(","),
        group_id=group,
        auto_offset_reset="earliest" if args.from_beginning else "latest",
        enable_auto_commit=True,
        key_deserializer=lambda k: k.decode("utf-8") if k else None,
        value_deserializer=lambda v: v.decode("utf-8"),
        consumer_timeout_ms=60000,
    )
    n = 0
    try:
        for msg in consumer:
            print(f"P:{msg.partition} O:{msg.offset} K:{msg.key} V:{msg.value}")
            n += 1
            if args.max and n >= args.max:
                break
    finally:
        consumer.close()
    print(f"Jasoak: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
