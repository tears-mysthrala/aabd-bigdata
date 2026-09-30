#!/usr/bin/env python3
"""2. kasua — Faker producer: 10 pertsona (izena, adina, hiria, emaila).

Erabilera:
  BOOTSTRAP=127.0.0.1:19092 TOPIC=codex-personas python personas_producer.py [--n 10] [--seed 42]
"""

import argparse
import json
import os
import sys

from faker import Faker
from kafka import KafkaProducer


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    bootstrap = os.environ.get("BOOTSTRAP", "127.0.0.1:19092")
    topic = os.environ.get("TOPIC", "codex-personas")

    fake = Faker("es_ES")
    Faker.seed(args.seed)

    producer = KafkaProducer(
        bootstrap_servers=bootstrap.split(","),
        key_serializer=lambda k: k.encode("utf-8"),
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
    )
    sent = []
    for _ in range(args.n):
        persona = {
            "izena": fake.name(),
            "adina": fake.random_int(min=18, max=80),
            "hiria": fake.city(),
            "emaila": fake.email(),
        }
        fut = producer.send(topic, key=persona["emaila"], value=persona)
        meta = fut.get(timeout=30)
        sent.append((meta.partition, meta.offset, persona["emaila"]))
        print(
            f"P:{meta.partition} O:{meta.offset} K:{persona['emaila']} V:{json.dumps(persona, ensure_ascii=False)}"
        )
    producer.flush()
    producer.close()
    print(f"Bidaliak: {len(sent)}/{args.n}")
    return 0 if len(sent) == args.n else 1


if __name__ == "__main__":
    sys.exit(main())
