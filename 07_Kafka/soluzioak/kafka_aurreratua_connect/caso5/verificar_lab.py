#!/usr/bin/env python3
"""Read-only checks of the real local MySQL -> Kafka -> MongoDB pipeline."""

import argparse
import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = "aabd-kafka-connect-20261005-v78"
TOPIC = "iabd-retail_db-categories"
FIELDS = ("category_id", "category_department_id", "category_name")


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
    with urllib.request.urlopen(
        "http://127.0.0.1:18083" + path, timeout=20
    ) as response:
        return json.load(response)


def collect(etapa):
    expected_names = ["Football", "Basketball", "Running"]
    if etapa != "inicial":
        expected_names.append("Streaming")
    expected = [
        dict(zip(FIELDS, (i, i if i < 4 else 2, name)))
        for i, name in enumerate(expected_names, 1)
    ]
    mysql_raw = execute(
        "mysql",
        "sh",
        "-c",
        'MYSQL_PWD="$MYSQL_PASSWORD" mysql -uiabd retail_db -B -N '
        '-e "SELECT category_id,category_department_id,category_name '
        'FROM categories ORDER BY category_id"',
    )
    mysql_rows = []
    for line in mysql_raw.splitlines():
        category_id, department_id, name = line.split("\t")
        mysql_rows.append(
            dict(zip(FIELDS, (int(category_id), int(department_id), name)))
        )

    connectors = get("/connectors")
    statuses = {name: get("/connectors/" + name + "/status") for name in connectors}
    relevant_plugins = [
        plugin
        for plugin in get("/connector-plugins")
        if plugin["class"]
        in (
            "io.confluent.connect.jdbc.JdbcSourceConnector",
            "com.mongodb.kafka.connect.MongoSinkConnector",
        )
    ]
    offsets_raw = execute(
        "kafka",
        "kafka-get-offsets",
        "--bootstrap-server",
        "kafka:29092",
        "--topic",
        TOPIC,
        "--time",
        "-1",
    )
    offsets = [
        {"topic": topic, "partition": int(partition), "offset": int(offset)}
        for topic, partition, offset in (
            line.split(":") for line in offsets_raw.splitlines()
        )
    ]
    count = sum(item["offset"] for item in offsets)
    messages_raw = execute(
        "kafka",
        "kafka-console-consumer",
        "--bootstrap-server",
        "kafka:29092",
        "--topic",
        TOPIC,
        "--from-beginning",
        "--max-messages",
        str(max(count, 1)),
        "--timeout-ms",
        "10000",
    )
    messages = [json.loads(line) for line in messages_raw.splitlines() if line.strip()]
    mongo_rows = json.loads(
        execute(
            "mongodb",
            "mongosh",
            "--quiet",
            "--eval",
            'print(JSON.stringify(db.getSiblingDB("iabd").categories.find({})'
            ".sort({category_id:1}).toArray()))",
        )
    )
    mongo_normalized = [{key: row[key] for key in FIELDS} for row in mongo_rows]
    offset_file = execute(
        "connect",
        "sh",
        "-c",
        "test -s /var/lib/kafka-connect/source.offsets && "
        'stat -c "%s" /var/lib/kafka-connect/source.offsets && '
        "sha256sum /var/lib/kafka-connect/source.offsets",
    ).splitlines()
    schema_fields = [
        {"type": "int32", "optional": False, "field": FIELDS[0]},
        {"type": "int32", "optional": False, "field": FIELDS[1]},
        {"type": "string", "optional": False, "field": FIELDS[2]},
    ]
    checks = {
        "connectors_expected": sorted(connectors) == ["mongodb-sink", "mysql-source"],
        "connectors_and_tasks_running": all(
            status["connector"]["state"] == "RUNNING"
            and len(status["tasks"]) == 1
            and all(task["state"] == "RUNNING" for task in status["tasks"])
            for status in statuses.values()
        )
        and len(statuses) == 2,
        "plugins_loaded": len(relevant_plugins) == 2,
        "mysql_exact_rows": mysql_rows == expected,
        "topic_one_partition_exact_count": len(offsets) == 1 and count == len(expected),
        "topic_exact_payloads": [message.get("payload") for message in messages]
        == expected,
        "topic_schema_matches_sql": all(
            message.get("schema", {}).get("fields") == schema_fields
            for message in messages
        )
        and bool(messages),
        "mongo_exact_rows": mongo_normalized == expected,
        "mongo_stable_ids": all(
            row.get("_id") == {"category_id": row["category_id"]} for row in mongo_rows
        )
        and bool(mongo_rows),
        "persistent_source_offset_file_nonempty": bool(offset_file),
    }
    container_ids = run("docker", "compose", "-p", PROJECT, "ps", "-q").splitlines()
    containers = []
    for container_id in container_ids:
        info = json.loads(run("docker", "inspect", container_id))[0]
        containers.append(
            {
                "name": info["Name"],
                "image": info["Config"]["Image"],
                "image_id": info["Image"],
                "state": info["State"]["Status"],
                "oom_killed": info["State"]["OOMKilled"],
                "memory_limit_bytes": info["HostConfig"]["Memory"],
                "ports": info["NetworkSettings"]["Ports"],
                "volumes": [
                    {key: mount[key] for key in ("Type", "Destination")}
                    for mount in info["Mounts"]
                ],
            }
        )
    checks["containers_not_oom_killed"] = len(containers) == 4 and all(
        not item["oom_killed"] and item["state"] == "running" for item in containers
    )
    return {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": PROJECT,
        "stage": etapa,
        "worker": get("/"),
        "plugins": relevant_plugins,
        "connector_statuses": statuses,
        "mysql": {"database": "retail_db", "table": "categories", "rows": mysql_rows},
        "kafka": {"topic": TOPIC, "end_offsets": offsets, "messages": messages},
        "mongodb": {
            "database": "iabd",
            "collection": "categories",
            "documents": mongo_rows,
        },
        "source_offset_file": {
            "path": "/var/lib/kafka-connect/source.offsets",
            "bytes": int(offset_file[0]),
            "sha256": offset_file[1].split()[0],
        },
        "containers": containers,
        "checks": checks,
        "passed": all(checks.values()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--etapa", choices=["inicial", "streaming", "reinicio"], required=True
    )
    parser.add_argument("--salida", type=Path, required=True)
    args = parser.parse_args()
    if args.salida.exists():
        raise SystemExit(
            "Evidence path already exists. Choose a new path; no evidence overwritten."
        )
    evidence = collect(args.etapa)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
    print(
        json.dumps(
            {
                "evidence": str(args.salida),
                "checks": evidence["checks"],
                "passed": evidence["passed"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    raise SystemExit(0 if evidence["passed"] else 1)


if __name__ == "__main__":
    main()
