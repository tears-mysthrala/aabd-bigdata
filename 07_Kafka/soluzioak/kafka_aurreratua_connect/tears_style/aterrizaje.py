#!/usr/bin/env python3
"""Landing: tears-raw -> MySQL raw table with per-row hash verification.

Raw is raw: EVERYTHING lands, including the poison record (evidence is
preserved; judgement happens at the curated boundary). The PRIMARY KEY on
id is the idempotency mechanism: Kafka replays of an already-landed id
fail on duplicate key instead of duplicating rows. Reruns are safe.
"""

import argparse
import json
import os

from modelos import sha_de, validar

TOPIC_RAW = "tears-raw"


def conectar_mysql():
    import mysql.connector

    return mysql.connector.connect(
        host="127.0.0.1",
        port=13308,
        user="tears",
        password=os.environ["MYSQL_PASSWORD"],
        database="tears_db",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bootstrap", default="127.0.0.1:19095")
    args = parser.parse_args()

    from kafka import KafkaConsumer

    consumidor = KafkaConsumer(
        TOPIC_RAW,
        bootstrap_servers=args.bootstrap,
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        consumer_timeout_ms=15000,
        value_deserializer=lambda v: json.loads(v.decode()),
    )
    db = conectar_mysql()
    cursor = db.cursor()
    insertados = duplicados = 0
    for mensaje in consumidor:
        registro = mensaje.value
        valido, _ = validar(registro)
        if not valido:
            # El veneno también aterriza: la zona raw no juzga, conserva.
            body = {k: v for k, v in registro.items() if k != "sha256"}
            assert registro.get("sha256") != sha_de(body), "veneno esperado"
        try:
            cursor.execute(
                "INSERT INTO raw (id, ts, schema_v, payload, sha256)"
                " VALUES (%s, %s, %s, %s, %s)",
                (
                    registro["id"],
                    registro["ts"],
                    registro["schema_v"],
                    json.dumps(registro),
                    registro["sha256"],
                ),
            )
            # Commit por fila: un ROLLBACK tras el duplicado solo puede
            # anular esa sentencia, nunca el lote ya confirmado. Un commit
            # único al final perdería todo lo anterior al primer duplicado.
            db.commit()
            insertados += 1
        except Exception as error:
            if "Duplicate entry" in str(error):
                duplicados += 1  # replay at-least-once: PK lo frena
                db.rollback()
            else:
                raise
    print(
        json.dumps(
            {"tabla": "raw", "insertados": insertados, "duplicados_pk": duplicados}
        )
    )


if __name__ == "__main__":
    main()
