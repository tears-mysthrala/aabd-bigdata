#!/usr/bin/env python3
"""Generate the deterministic sensor stream into tears-raw.

Stream (seed 7): 10 v1 records + 3 v2 records (schema evolution) + 1 exact
duplicate of id=3 (at-least-once delivery) + 1 poison record id=99 with a
deliberately broken sha256 (corruption case). Total: 15 messages.
Writes manifest.json: the expected truth for later verification.
"""

import argparse
import json
from pathlib import Path

from modelos import ID_DUPLICADO, ID_VENENO, manifiesto_esperado

TOPIC_RAW = "tears-raw"

DEPS = ["kafka-python"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bootstrap", default="127.0.0.1:19095")
    parser.add_argument("--semilla", type=int, default=7)
    parser.add_argument("--manifiesto", type=Path, required=True)
    args = parser.parse_args()

    from kafka import KafkaProducer

    manifiesto = manifiesto_esperado(args.semilla)
    registros = manifiesto["registros"]
    por_id = {r["id"]: r for r in registros}

    productor = KafkaProducer(
        bootstrap_servers=args.bootstrap,
        value_serializer=lambda v: json.dumps(v).encode(),
    )
    enviados = 0
    for registro in registros:
        productor.send(TOPIC_RAW, value=registro)
        enviados += 1
    # Caso duplicado: mismo id, mismos bytes (replay de Kafka).
    productor.send(TOPIC_RAW, value=por_id[ID_DUPLICADO])
    enviados += 1
    # Caso veneno: sha256 deliberadamente roto.
    veneno = {**por_id[1], "id": ID_VENENO, "sha256": "0" * 64}
    productor.send(TOPIC_RAW, value=veneno)
    enviados += 1
    productor.flush()

    args.manifiesto.write_text(
        json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps({"topic": TOPIC_RAW, "mensajes": enviados, "veneno": ID_VENENO}))


if __name__ == "__main__":
    main()
