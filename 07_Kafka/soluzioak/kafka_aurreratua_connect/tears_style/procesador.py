#!/usr/bin/env python3
"""Processor: MySQL raw -> tears-curated (+ tears-dlq quarantine).

Reads the landing table in id order, revalidates every row (hash + schema),
transforms v1/v2 into curated documents with lineage, and produces them
keyed by id. The poison record is quarantined to the DLQ with its reason:
it never reaches curated/Mongo. Stateless: reruns reproduce the same
curated records, and the Mongo sink upserts by id (restart-safe).
"""

import argparse
import json
import os
from datetime import UTC, datetime

from modelos import transformar, validar

TOPIC_CURATED = "tears-curated"
TOPIC_DLQ = "tears-dlq"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bootstrap", default="127.0.0.1:19095")
    args = parser.parse_args()

    import mysql.connector
    from kafka import KafkaProducer

    db = mysql.connector.connect(
        host="127.0.0.1",
        port=13308,
        user="tears",
        password=os.environ["MYSQL_PASSWORD"],
        database="tears_db",
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, payload, sha256 FROM raw ORDER BY id")

    productor = KafkaProducer(
        bootstrap_servers=args.bootstrap,
        key_serializer=lambda v: str(v).encode(),
        value_serializer=lambda v: json.dumps(v).encode(),
    )
    ahora = datetime.now(UTC).isoformat()
    curados = cuarentena = 0
    for fila in cursor.fetchall():
        registro = json.loads(fila["payload"])
        valido, motivo = validar(registro)
        if not valido:
            productor.send(
                TOPIC_DLQ,
                key=registro.get("id", -1),
                value={
                    "id": registro.get("id"),
                    "motivo": motivo,
                    "sha_recibido": registro.get("sha256"),
                    "origen": "aterrizaje raw",
                },
            )
            cuarentena += 1
            continue
        productor.send(
            TOPIC_CURATED, key=registro["id"], value=transformar(registro, ahora)
        )
        curados += 1
    productor.flush()
    print(json.dumps({"curados": curados, "cuarentena_dlq": cuarentena}))


if __name__ == "__main__":
    main()
