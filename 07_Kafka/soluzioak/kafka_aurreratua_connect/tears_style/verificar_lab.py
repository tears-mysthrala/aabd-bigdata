#!/usr/bin/env python3
"""Read-only end-to-end checks of the tears_style pipeline.

Chain of custody per record: manifest (seed) -> tears-raw -> MySQL raw
(hash recomputed at read) -> tears-curated / tears-dlq -> MongoDB.
The final extra read compares Mongo documents against the manifest,
closing the loop the user asked for.
"""

import argparse
import json
import subprocess
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

from modelos import ID_VENENO, SEMILLA, manifiesto_esperado, sha_de

ROOT = Path(__file__).resolve().parent
PROJECT = "aabd-kafka-tears-style"
CONNECT_API = "http://127.0.0.1:18084"
RAW, CURATED, DLQ = "tears-raw", "tears-curated", "tears-dlq"
FIELDS = ("id", "sensor", "temp_c", "bateria")


def run(*args):
    result = subprocess.run(
        args, cwd=ROOT, text=True, capture_output=True, timeout=90, check=False
    )
    if result.returncode:
        # Commands never contain credentials; database clients read container env.
        raise RuntimeError(
            f"{args!r}: exit {result.returncode}: {result.stderr[-1500:]}"
        )
    return result.stdout.strip()


def execute(service, *args):
    return run("docker", "compose", "-p", PROJECT, "exec", "-T", service, *args)


def get(path):
    with urllib.request.urlopen(CONNECT_API + path, timeout=20) as response:
        return json.load(response)


def leer_topic(topic):
    crudo = run(
        "docker",
        "compose",
        "-p",
        PROJECT,
        "exec",
        "-T",
        "kafka",
        "kafka-console-consumer",
        "--bootstrap-server",
        "kafka:29092",
        "--topic",
        topic,
        "--from-beginning",
        "--timeout-ms",
        "10000",
    )
    return [json.loads(line) for line in crudo.splitlines() if line.strip()]


def contar(topic):
    crudo = execute(
        "kafka",
        "kafka-get-offsets",
        "--bootstrap-server",
        "kafka:29092",
        "--topic",
        topic,
        "--time",
        "-1",
    )
    return sum(int(line.split(":")[2]) for line in crudo.splitlines())


def ejson(valor):
    """Normaliza el JSON extendido de mongosh a tipos Python.
    El sink guarda enteros como BSON int64 y cada versión de mongosh los
    serializa distinto ({"$numberLong": "3"} o {"high":0,"low":3,...}).
    Sin esto, id/_id no comparan con los enteros del manifiesto aunque
    sean el mismo valor."""
    if isinstance(valor, dict):
        if set(valor) == {"$numberLong"}:
            return int(valor["$numberLong"])
        if set(valor) == {"high", "low", "unsigned"}:
            return int(valor["high"]) * 2**32 + (int(valor["low"]) & 0xFFFFFFFF)
        return {k: ejson(v) for k, v in valor.items()}
    if isinstance(valor, list):
        return [ejson(v) for v in valor]
    return valor


def collect(etapa):
    verdad = {r["id"]: r for r in manifiesto_esperado(SEMILLA)["registros"]}
    ids_validos = sorted(verdad)
    # En aterrizaje aún no hay curado/DLQ/Mongo: se espera vacío.
    completo = etapa in ("curado", "reinicio")
    esperado_mongo = (
        [
            {
                "id": i,
                "sensor": verdad[i]["sensor"],
                "temp_c": verdad[i]["temp"],
                "bateria": verdad[i].get("bateria"),
            }
            for i in ids_validos
        ]
        if completo
        else []
    )

    mysql_raw = execute(
        "mysql",
        "sh",
        "-c",
        'MYSQL_PWD="$MYSQL_PASSWORD" mysql -utears tears_db -B -N '
        '-e "SELECT id,ts,schema_v,payload,sha256 FROM raw ORDER BY id"',
    )
    filas = []
    for linea in mysql_raw.splitlines():
        id_, ts, schema_v, payload, sha = linea.split("\t")
        filas.append(
            {
                "id": int(id_),
                "ts": ts,
                "schema_v": int(schema_v),
                "payload": json.loads(payload),
                "sha256": sha,
            }
        )

    mensajes_raw = leer_topic(RAW)
    mensajes_curated = leer_topic(CURATED)
    mensajes_dlq = leer_topic(DLQ)
    mongo_docs = [
        ejson(doc)
        for doc in json.loads(
            execute(
                "mongodb",
                "mongosh",
                "--quiet",
                "--eval",
                'print(JSON.stringify(db.getSiblingDB("tears").curated.find({})'
                ".sort({id:1}).toArray()))",
            )
        )
    ]
    conectores = get("/connectors")
    estados = {n: get("/connectors/" + n + "/status") for n in conectores}

    # Cadena de custodia: hash recalculado en cada lectura, no confiado.
    # El sha se calcula sobre el cuerpo SIN el propio campo sha256.
    # El veneno (id=99) DEBE discrepar: es la prueba de corrupción.
    def cuerpo(fila):
        return {k: v for k, v in fila["payload"].items() if k != "sha256"}

    veneno_fila = [f for f in filas if f["id"] == ID_VENENO]
    normales = [f for f in filas if f["id"] != ID_VENENO]
    hashes_mysql_ok = (
        len(veneno_fila) == 1
        and veneno_fila[0]["sha256"] != sha_de(cuerpo(veneno_fila[0]))
        and all(
            fila["sha256"] == sha_de(cuerpo(fila))
            and fila["payload"]["sha256"] == fila["sha256"]
            for fila in normales
        )
    )
    mysql_vs_manifiesto = sorted(f["id"] for f in filas) == ids_validos + [
        ID_VENENO
    ] and all(
        f["payload"] == verdad[f["id"]] and f["sha256"] == verdad[f["id"]]["sha256"]
        for f in filas
        if f["id"] in verdad
    )
    curados = [m for m in mensajes_curated]
    linaje_ok = all(
        m["linaje"]["sha_origen"] == verdad[m["id"]]["sha256"]
        and m["sensor"] == verdad[m["id"]]["sensor"]
        and m["temp_c"] == verdad[m["id"]]["temp"]
        and m["bateria"] == verdad[m["id"]].get("bateria")
        for m in curados
    )
    # Replay-aware: un reprocesado duplica mensajes en el topic (at-least-once);
    # lo que importa es el CONJUNTO de ids y que cada mensaje sea válido.
    # El sink lo absorbe con upsert por id (ver mongo estable).
    ids_curados = {m["id"] for m in curados}
    if completo:
        curated_ok = ids_curados == set(ids_validos) and linaje_ok
    else:
        curated_ok = curados == []
    mongo_normalizado = [{k: d.get(k) for k in FIELDS} for d in mongo_docs]
    esperado_mongo = (
        [
            {
                "id": i,
                "sensor": verdad[i]["sensor"],
                "temp_c": verdad[i]["temp"],
                "bateria": verdad[i].get("bateria"),
            }
            for i in ids_validos
        ]
        if completo
        else []
    )
    # Lectura extra final: Mongo comparado contra el manifiesto, no contra MySQL.
    mongo_vs_manifiesto = mongo_normalizado == esperado_mongo
    veneno = [m for m in mensajes_dlq]
    if completo:
        dlq_ok = (
            len(veneno) >= 1
            and all(v["id"] == ID_VENENO and "sha256" in v["motivo"] for v in veneno)
            and not any(m["id"] == ID_VENENO for m in curados)
            and not any(d["id"] == ID_VENENO for d in mongo_docs)
        )
    else:
        dlq_ok = veneno == []
    # _id es documento {id: ...} por PartialValueStrategy (igual que caso5):
    # el upsert por id hace que los replays sean idempotentes.
    mongo_ids_estables = (not mongo_docs and not completo) or (
        bool(mongo_docs)
        and all(d.get("_id") == {"id": d.get("id")} for d in mongo_docs)
    )

    checks = {
        "raw_15_mensajes": len(mensajes_raw) == 15 and contar(RAW) == 15,
        "mysql_14_filas_hash_ok": len(filas) == 14 and hashes_mysql_ok,
        "mysql_coincide_manifiesto": mysql_vs_manifiesto,
        "duplicado_id3_sin_duplicar": sum(1 for f in filas if f["id"] == 3) == 1,
        "curated_linaje_ok": curated_ok,
        "dlq_segun_etapa": dlq_ok,
        "mongo_vs_manifiesto": mongo_vs_manifiesto,
        "mongo_ids_estables": mongo_ids_estables,
        "sink_running": estados.get("mongo-sink-curated", {})
        .get("connector", {})
        .get("state")
        == "RUNNING"
        and any(
            task.get("state") == "RUNNING"
            for task in estados.get("mongo-sink-curated", {}).get("tasks", [])
        ),
    }
    return {
        "captured_at_utc": datetime.now(UTC).isoformat(),
        "project": PROJECT,
        "stage": etapa,
        "mysql_raw_ids": [f["id"] for f in filas],
        "kafka_counts": {
            RAW: len(mensajes_raw),
            CURATED: len(curados),
            DLQ: len(veneno),
        },
        "mongodb_ids": [d["id"] for d in mongo_docs],
        "connector_statuses": estados,
        "checks": checks,
        "passed": all(checks.values()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--etapa", choices=["aterrizaje", "curado", "reinicio"])
    parser.add_argument("--salida", type=Path, required=True)
    args = parser.parse_args()
    if args.salida.exists():
        raise SystemExit(
            "Evidence path already exists. Choose a new path; no evidence overwritten."
        )
    evidencia = collect(args.etapa)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + "\n")
    print(
        json.dumps(
            {
                "evidence": str(args.salida),
                "checks": evidencia["checks"],
                "passed": evidencia["passed"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    raise SystemExit(0 if evidencia["passed"] else 1)


if __name__ == "__main__":
    main()
