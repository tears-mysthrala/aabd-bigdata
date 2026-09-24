"""Sortu ariketa didaktikoetarako bezero eta salmenta datu sintetikoak."""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

from faker import Faker


BEZERO_ZUTABEAK = ("id", "izena", "emaila", "hiria", "adina")
SALMENTA_ZUTABEAK = (
    "id",
    "data",
    "bezeroa",
    "hiria",
    "produktua",
    "kategoria",
    "prezioa",
    "unitateak",
)
KATEGORIAK = ("Ordenagailuak", "Osagaiak", "Periferikoak", "Sareak")
SALMENTA_DATA_HASIERA = date(2024, 9, 24)
SALMENTA_DATA_AZKENA = date(2026, 9, 24)
PRODUKTUAK = {
    "Ordenagailuak": ("Ordenagailu eramangarria", "Mahaigaineko ordenagailua", "Mini PC"),
    "Osagaiak": ("Prozesadorea", "RAM memoria", "SSD diskoa", "Txartel grafikoa"),
    "Periferikoak": ("Teklatua", "Sagua", "Monitorea", "Webkamera"),
    "Sareak": ("Bideratzailea", "Switch-a", "Wi-Fi egokigailua", "Sare-kablea"),
}


def _faker(seed: int | None) -> Faker:
    fake = Faker("es_ES")
    if seed is not None:
        fake.seed_instance(seed)
    return fake


def generar_bezeroak(kopurua: int, seed: int | None = None) -> list[dict[str, object]]:
    """Sortu `kopurua` bezero sintetikoren zerrenda; seed-ak emaitza erreproduzitzen du."""
    if kopurua < 0:
        raise ValueError("kopurua ezin da negatiboa izan")

    fake = _faker(seed)
    return [
        {
            "id": i,
            "izena": fake.name(),
            "emaila": fake.email(),
            "hiria": fake.city(),
            "adina": fake.random_int(min=18, max=80),
        }
        for i in range(1, kopurua + 1)
    ]


def generar_salmentak(kopurua: int = 10_000, seed: int | None = 42) -> list[dict[str, object]]:
    """Sortu salmenta sintetikoak, eskatu denean seed berarekin errepikagarriak."""
    if kopurua < 0:
        raise ValueError("kopurua ezin da negatiboa izan")

    fake = _faker(seed)
    salmentak: list[dict[str, object]] = []
    for i in range(1, kopurua + 1):
        kategoria = fake.random_element(elements=KATEGORIAK)
        salmentak.append(
            {
                "id": i,
                "data": fake.date_between(
                    start_date=SALMENTA_DATA_HASIERA,
                    end_date=SALMENTA_DATA_AZKENA,
                ).isoformat(),
                "bezeroa": fake.name(),
                "hiria": fake.city(),
                "produktua": fake.random_element(elements=PRODUKTUAK[kategoria]),
                "kategoria": kategoria,
                "prezioa": round(fake.pyfloat(min_value=5, max_value=2000, right_digits=2), 2),
                "unitateak": fake.random_int(min=1, max=10),
            }
        )
    return salmentak


def gorde_csv(erregistroak: list[dict[str, object]], helmuga: Path) -> None:
    """Idatzi CSV goiburuarekin; zutabeen ordena lehen erregistroarena da."""
    helmuga.parent.mkdir(parents=True, exist_ok=True)
    zutabeak = list(erregistroak[0]) if erregistroak else []
    with helmuga.open("w", encoding="utf-8", newline="") as fitxategia:
        idazlea = csv.DictWriter(fitxategia, fieldnames=zutabeak)
        idazlea.writeheader()
        idazlea.writerows(erregistroak)


def gorde_json(erregistroak: list[dict[str, object]], helmuga: Path, erro_izena: str) -> None:
    """Idatzi JSON objektua erro-gako batekin (adib. `bezeroak` edo `salmentak`)."""
    helmuga.parent.mkdir(parents=True, exist_ok=True)
    with helmuga.open("w", encoding="utf-8") as fitxategia:
        json.dump({erro_izena: erregistroak}, fitxategia, ensure_ascii=False, indent=2)
        fitxategia.write("\n")


def csv_json_bihurtu(sarrera: Path, helmuga: Path) -> None:
    """Bihurtu bezeroen CSVa `{"bezeroak": [...]}` JSON formatura, mota numerikoak gordez."""
    with sarrera.open(encoding="utf-8-sig", newline="") as fitxategia:
        irakurlea = csv.DictReader(fitxategia)
        bezeroak: list[dict[str, object]] = []
        for errenkada in irakurlea:
            bezeroak.append(
                {
                    "id": int(errenkada["id"]),
                    "izena": errenkada["izena"],
                    "emaila": errenkada["emaila"],
                    "hiria": errenkada["hiria"],
                    "adina": int(errenkada["adina"]),
                }
            )
    gorde_json(bezeroak, helmuga, "bezeroak")


def erakutsi_seed_demoa() -> None:
    """Erakutsi lau exekuzio: seed gabe bi eta seed=42 erabilita beste bi."""
    seed_gabe_1 = generar_bezeroak(5)
    seed_gabe_2 = generar_bezeroak(5)
    seed_42_1 = generar_bezeroak(5, seed=42)
    seed_42_2 = generar_bezeroak(5, seed=42)

    print("Bezeroak, seed gabe (1. exekuzioa):")
    for bezeroa in seed_gabe_1:
        print(bezeroa)
    print("Bezeroak, seed gabe (2. exekuzioa):")
    for bezeroa in seed_gabe_2:
        print(bezeroa)
    print("Bezeroak, seed=42 (1. exekuzioa):")
    for bezeroa in seed_42_1:
        print(bezeroa)
    print("Bezeroak, seed=42 (2. exekuzioa):")
    for bezeroa in seed_42_2:
        print(bezeroa)
    assert seed_42_1 == seed_42_2, "Seed bereko bezero-datuek berdinak izan behar dute"


def _egiaztatu_bezeroak(bezeroak: list[dict[str, object]], espero: int) -> None:
    assert len(bezeroak) == espero
    assert all(set(BEZERO_ZUTABEAK) == set(bezeroa) for bezeroa in bezeroak)
    ids = [bezeroa["id"] for bezeroa in bezeroak]
    assert len(ids) == len(set(ids))
    assert all(bezeroa["izena"] and bezeroa["emaila"] and bezeroa["hiria"] for bezeroa in bezeroak)
    assert all(18 <= int(bezeroa["adina"]) <= 80 for bezeroa in bezeroak)


def _egiaztatu_salmentak(salmentak: list[dict[str, object]], gutxienez: int) -> None:
    assert len(salmentak) >= gutxienez
    assert all(set(SALMENTA_ZUTABEAK) == set(salmenta) for salmenta in salmentak)
    ids = [salmenta["id"] for salmenta in salmentak]
    assert len(ids) == len(set(ids))
    assert all(
        all(salmenta[zutabea] for zutabea in ("data", "bezeroa", "hiria", "produktua"))
        for salmenta in salmentak
    )
    assert all(5 <= float(salmenta["prezioa"]) <= 2000 for salmenta in salmentak)
    assert all(1 <= int(salmenta["unitateak"]) <= 10 for salmenta in salmentak)
    assert all(salmenta["kategoria"] in KATEGORIAK for salmenta in salmentak)
    assert all(
        SALMENTA_DATA_HASIERA.isoformat() <= str(salmenta["data"]) <= SALMENTA_DATA_AZKENA.isoformat()
        for salmenta in salmentak
    )


def _egiaztatu_fitxategiak(data: Path) -> None:
    for izena, zutabeak, espero in (
        ("bezeroak_100.csv", BEZERO_ZUTABEAK, 100),
        ("bezeroak_10000.csv", BEZERO_ZUTABEAK, 10_000),
        ("salmentak_10000.csv", SALMENTA_ZUTABEAK, 10_000),
    ):
        with (data / izena).open(encoding="utf-8", newline="") as fitxategia:
            reader = csv.DictReader(fitxategia)
            assert tuple(reader.fieldnames or ()) == zutabeak, f"{izena}: goiburu okerra"
            errenkadak = list(reader)
        assert len(errenkadak) == espero, f"{izena}: {len(errenkadak)} errenkada"
        ids = [errenkada["id"] for errenkada in errenkadak]
        assert len(ids) == len(set(ids)), f"{izena}: ID errepikatuak"
        assert all(all(errenkada[zutabea] for zutabea in zutabeak) for errenkada in errenkadak)
        if izena.startswith("bezeroak"):
            assert all(18 <= int(errenkada["adina"]) <= 80 for errenkada in errenkadak)
        if izena.startswith("salmentak"):
            assert all(5 <= float(errenkada["prezioa"]) <= 2_000 for errenkada in errenkadak)
            assert all(1 <= int(errenkada["unitateak"]) <= 10 for errenkada in errenkadak)
            assert all(errenkada["kategoria"] in KATEGORIAK for errenkada in errenkadak)

    bezero_json = json.loads((data / "bezeroak.json").read_text(encoding="utf-8"))
    assert set(bezero_json) == {"bezeroak"} and len(bezero_json["bezeroak"]) == 100
    assert tuple(bezero_json["bezeroak"][0]) == BEZERO_ZUTABEAK
    assert isinstance(bezero_json["bezeroak"][0]["adina"], int)

    salmenta_json = json.loads((data / "salmentak_10000.json").read_text(encoding="utf-8"))
    assert set(salmenta_json) == {"salmentak"} and len(salmenta_json["salmentak"]) == 10_000
    assert tuple(salmenta_json["salmentak"][0]) == SALMENTA_ZUTABEAK
    _egiaztatu_salmentak(salmenta_json["salmentak"], 10_000)
    with (data / "salmentak_10000.csv").open(encoding="utf-8", newline="") as fitxategia:
        salmenta_csv = list(csv.DictReader(fitxategia))
    for csv_erregistroa, json_erregistroa in zip(salmenta_csv, salmenta_json["salmentak"], strict=True):
        assert int(csv_erregistroa["id"]) == json_erregistroa["id"]
        assert csv_erregistroa["data"] == json_erregistroa["data"]
        assert csv_erregistroa["bezeroa"] == json_erregistroa["bezeroa"]
        assert csv_erregistroa["hiria"] == json_erregistroa["hiria"]
        assert csv_erregistroa["produktua"] == json_erregistroa["produktua"]
        assert csv_erregistroa["kategoria"] == json_erregistroa["kategoria"]
        assert float(csv_erregistroa["prezioa"]) == json_erregistroa["prezioa"]
        assert int(csv_erregistroa["unitateak"]) == json_erregistroa["unitateak"]


def main() -> None:
    """Sortu eskatutako datu multzo didaktikoak moduluaren `data/` karpetan."""
    data = Path(__file__).parent / "data"
    erakutsi_seed_demoa()

    bezeroak_100 = generar_bezeroak(100)
    bezeroak_10000 = generar_bezeroak(10_000)
    salmentak = generar_salmentak(10_000, seed=42)
    _egiaztatu_bezeroak(bezeroak_100, 100)
    _egiaztatu_bezeroak(bezeroak_10000, 10_000)
    _egiaztatu_salmentak(salmentak, 10_000)

    gorde_csv(bezeroak_100, data / "bezeroak_100.csv")
    gorde_csv(bezeroak_10000, data / "bezeroak_10000.csv")
    csv_json_bihurtu(data / "bezeroak_100.csv", data / "bezeroak.json")
    gorde_csv(salmentak, data / "salmentak_10000.csv")
    gorde_json(salmentak, data / "salmentak_10000.json", "salmentak")
    _egiaztatu_fitxategiak(data)
    print(f"Datu sintetikoak baliozkotu dira: {data}")


if __name__ == "__main__":
    main()
