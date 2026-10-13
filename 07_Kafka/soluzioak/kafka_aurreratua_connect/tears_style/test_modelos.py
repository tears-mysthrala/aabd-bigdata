"""Unit checks of the pure record logic (no Docker, no broker)."""

import random

from modelos import (
    ID_DUPLICADO,
    ID_VENENO,
    IDS_V1,
    IDS_V2,
    manifiesto_esperado,
    registro,
    sha_de,
    transformar,
    validar,
)


def test_manifiesto_determinista_y_recomputable():
    primero = manifiesto_esperado(7)
    segundo = manifiesto_esperado(7)
    assert primero == segundo
    assert [r["id"] for r in primero["registros"]] == IDS_V1 + list(IDS_V2)
    assert {r["schema_v"] for r in primero["registros"] if r["id"] in IDS_V2} == {2}


def test_sha_viaja_y_se_recomputa():
    for entry in manifiesto_esperado()["registros"]:
        body = {k: v for k, v in entry.items() if k != "sha256"}
        assert entry["sha256"] == sha_de(body)
        assert validar(entry) == (True, "")


def test_veneno_detectado_y_duplicado_identico():
    por_id = {r["id"]: r for r in manifiesto_esperado()["registros"]}
    veneno = {**por_id[1], "id": ID_VENENO, "sha256": "0" * 64}
    assert validar(veneno)[0] is False
    assert "sha256" in validar(veneno)[1]
    assert validar({**por_id[ID_DUPLICADO]}) == (True, "")
    assert validar({**por_id[1], "schema_v": 99})[0] is False


def test_transformar_v1_v2_con_linaje():
    por_id = {r["id"]: r for r in manifiesto_esperado()["registros"]}
    doc1 = transformar(por_id[1], "2026-10-06T00:00:00Z")
    assert doc1["bateria"] is None
    assert doc1["linaje"] == {
        "sha_origen": por_id[1]["sha256"],
        "schema_v": 1,
    }
    doc11 = transformar(por_id[11], "2026-10-06T00:00:00Z")
    assert doc11["bateria"] == por_id[11]["bateria"]
    assert doc11["linaje"]["schema_v"] == 2


def test_balance_del_caso():
    # 15 mensajes raw: 13 válidos + 1 duplicado idéntico + 1 veneno.
    # MySQL: 14 filas (PK frena el duplicado). Curated/Mongo: 13. DLQ: 1.
    assert len(IDS_V1) + len(IDS_V2) == 13
    assert ID_DUPLICADO in IDS_V1
    assert ID_VENENO not in IDS_V1 + list(IDS_V2)


def test_unknown_schema_with_correct_hash_is_not_a_poison_hash():
    record = registro(200, 3, random.Random(7))
    assert record["sha256"] == sha_de(
        {k: v for k, v in record.items() if k != "sha256"}
    )
    assert validar(record)[0] is False
    assert "schema_v" in validar(record)[1]


def test_missing_required_sensor_fields_rejected_for_dlq():
    record = registro(201, 1, random.Random(7))
    for missing in ("sensor", "temp"):
        altered = {k: v for k, v in record.items() if k not in (missing, "sha256")}
        altered["sha256"] = sha_de(altered)
        valid, reason = validar(altered)
        assert not valid and missing in reason


def test_nonfinite_temp_rejected():
    record = registro(201, 1, random.Random(7))
    record["temp"] = float("nan")
    body = {k: v for k, v in record.items() if k != "sha256"}
    record["sha256"] = sha_de(body)
    assert validar(record)[0] is False


def test_huge_integer_temperature_routes_to_rejection():
    entry = registro(301, 1, random.Random(7))
    entry["temp"] = 10**300
    body = {k: v for k, v in entry.items() if k != "sha256"}
    entry["sha256"] = sha_de(body)
    ok, reason = validar(entry)
    assert not ok and "rango" in reason
