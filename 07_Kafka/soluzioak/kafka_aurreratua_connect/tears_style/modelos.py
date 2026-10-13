"""Canonical sensor-record model shared by generator, landing, processor.

The sha256 travels WITH each record so every stage can recompute it and
prove no corruption happened in transit (datalake-style verification).
Hash input is the canonical JSON of the body WITHOUT the sha field itself.
"""

import hashlib
import json
import random

SEMILLA = 7
SENSORES = ("T-01", "T-02", "T-03")

# Expected stream for the lab: 10 v1 + 3 v2 (schema evolution) + 1 poison.
IDS_V1 = list(range(1, 11))
IDS_V2 = (11, 12, 13)
ID_DUPLICADO = 3
ID_VENENO = 99


def cuerpo(id_: int, schema_v: int, rng: random.Random) -> dict:
    base = {
        "id": id_,
        "ts": f"2026-10-06T08:{id_:02d}:00Z",
        "schema_v": schema_v,
        "sensor": rng.choice(SENSORES),
        "temp": round(rng.uniform(18.0, 26.0), 1),
    }
    if schema_v == 2:
        # Schema evolution: new optional field. v1 consumers must ignore
        # unknown fields, never crash on them.
        base["bateria"] = round(rng.uniform(20.0, 100.0), 1)
    return base


def sha_de(cuerpo_: dict) -> str:
    canonical = json.dumps(cuerpo_, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def registro(id_: int, schema_v: int, rng: random.Random) -> dict:
    body = cuerpo(id_, schema_v, rng)
    return {**body, "sha256": sha_de(body)}


def manifiesto_esperado(semilla: int = SEMILLA) -> dict:
    """Recomputable truth: no need to trust files, only the seed."""
    rng = random.Random(semilla)
    registros = [registro(i, 1, rng) for i in IDS_V1]
    registros += [registro(i, 2, rng) for i in IDS_V2]
    return {"semilla": semilla, "registros": registros}


def validar(registro_: dict) -> tuple[bool, str]:
    """Pure validation used by landing and processor. Returns (ok, reason)."""
    if not isinstance(registro_, dict):
        return False, "registro no es objeto"
    body = {k: v for k, v in registro_.items() if k != "sha256"}
    if registro_.get("sha256") != sha_de(body):
        return False, "sha256 no coincide: corrupción o veneno"
    if type(registro_.get("schema_v")) is not int or registro_["schema_v"] not in (
        1,
        2,
    ):
        return False, f"schema_v desconocido: {registro_.get('schema_v')}"
    if type(registro_.get("id")) is not int:
        return False, "id ausente o no entero"
    if not isinstance(registro_.get("sensor"), str) or not registro_["sensor"].strip():
        return False, "sensor ausente o vacío"
    temp = registro_.get("temp")
    if isinstance(temp, bool) or not isinstance(temp, (int, float)):
        return False, "temp ausente o no numérica"
    # Compare bounds before math.isfinite: huge JSON integers overflow
    # when converted to float. Such records belong in DLQ, not in curated.
    if not -273.15 <= temp <= 1000:
        return False, "temp fuera de rango"
    if isinstance(temp, float) and not __import__("math").isfinite(temp):
        return False, "temp no finita"
    return True, ""


def transformar(registro_: dict, procesado_en: str) -> dict:
    """v1/v2 -> curated document with lineage. Unknown fields are dropped
    except the known v2 extension; missing v2 fields become None."""
    return {
        "id": registro_["id"],
        "sensor": registro_["sensor"],
        "temp_c": registro_["temp"],
        "bateria": registro_.get("bateria"),
        "procesado_en": procesado_en,
        "linaje": {
            "sha_origen": registro_["sha256"],
            "schema_v": registro_["schema_v"],
        },
    }
