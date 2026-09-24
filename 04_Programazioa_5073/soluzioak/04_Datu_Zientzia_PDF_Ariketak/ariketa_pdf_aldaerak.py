"""PDFko 5073-2 ariketa-aldaera osagarriak, lehendik dauden datuak ukitu gabe.

Erabilera: python ariketa_pdf_aldaerak.py

Zenbait datu ez dira PDFan ematen (Z-score matrizea eta tutorearen CSV zehatzak).
Horietarako, hemen zehaztutako adibide sintetikoak erabiltzen dira eta hala
etiketatzen dira; ez dira gelako benetako emaitzak.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


try:
    OINARRI = Path(__file__).resolve().parent
except NameError:  # Koadernoan itsatsitako kode-gelaxkak ez du __file__-rik.
    OINARRI = Path.cwd()
    if not (OINARRI / "data" / "pdf_ariketa_2_2_fixtures").is_dir():
        OINARRI = (
            OINARRI
            / "04_Programazioa_5073"
            / "soluzioak"
            / "04_Datu_Zientzia_PDF_Ariketak"
        )
FIXTURE_DIR = OINARRI / "data" / "pdf_ariketa_2_2_fixtures"
HILABETEAK = ("urtarrila", "otsaila", "martxoa")


def ariketa_1_2_matrizea() -> np.ndarray:
    """Sortu PDFko seed=42 (6, 4) ausazko nota-matrizea.

    5x5 aldaketa ez da itzultzen; ezin da 24 elementu 25 gelaxkatan banatu.
    """
    # RandomState-ek PDFko np.random.seed(42) + randint sekuentzia bera ematen du,
    # baina ez du NumPy-ren ausazko egoera globala aldatzen.
    return np.random.RandomState(42).randint(0, 11, size=(6, 4))


def ariketa_1_3_prezioak(
    prezioak: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Kalkulatu PDFko BEZa/deskontua eta adibideko zutabe-Z-score-a.

    Prezio bektoreak lau balio izan behar ditu; PDFko balioak [10, 25, 8, 50]
    dira. Normalizazioaren 5x4 matrizea ariketa honetarako datu sintetiko
    esplizitua da, ez benetako saltokien behaketa.
    """
    if prezioak.shape != (4,):
        raise ValueError("prezioak array-ak lau elementuko forma (4,) izan behar du")
    if not np.issubdtype(prezioak.dtype, np.number):
        raise TypeError("prezioak zenbakizkoak izan behar dira")

    beza = prezioak.astype(float) * 1.21
    deskontu_faktoreak = np.array([1.0, 0.9, 1.0, 0.9])
    azken_prezioak = beza * deskontu_faktoreak

    dendak_sintetikoak = np.array(
        [
            [10.0, 25.0, 8.0, 50.0],
            [12.0, 20.0, 9.0, 45.0],
            [8.0, 30.0, 7.0, 55.0],
            [11.0, 27.0, 10.0, 48.0],
            [9.0, 23.0, 6.0, 52.0],
        ],
        dtype=float,
    )
    batezbestekoa = dendak_sintetikoak.mean(axis=0)
    desbideratzeak = dendak_sintetikoak.std(axis=0, ddof=0)
    if np.any(desbideratzeak == 0):
        raise ValueError("Z-score-rako zutabe guztiek bariantza izan behar dute")
    z_score = (dendak_sintetikoak - batezbestekoa) / desbideratzeak
    return azken_prezioak, z_score


def ariketa_1_4_stock(stock: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Itzuli agortutakoen maskara eta PDFko stock-aren birhornitze-emaitza."""
    if stock.shape != (10,):
        raise ValueError("stock array-ak PDFko hamar produktuak izan behar ditu")
    agortuta = stock == 0
    stock_birhornitua = stock.copy()
    stock_birhornitua[stock_birhornitua < 5] = 10
    return agortuta, stock_birhornitua


def ariketa_2_2_csvak(
    bideak: list[Path],
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Kargatu hiru hilabeteko CSVak, iturria gehitu eta errenkadak zenbatu.

    Funtzioa esplizituki hiru fitxategirako da, PDFan eskatutakoaren arabera.
    ``bideak``-en ordenak hilabeteen izenarekin parekatzen dira.
    """
    if len(bideak) != len(HILABETEAK):
        raise ValueError("Hiru CSV bide eman behar dira: urtarrila, otsaila, martxoa")

    beharrezkoak = {"data", "produktua", "kopurua", "prezioa"}
    zatiak: list[pd.DataFrame] = []
    for hilabetea, bidea in zip(HILABETEAK, bideak, strict=True):
        try:
            taula = pd.read_csv(bidea, sep=";", encoding="utf-8")
            if not beharrezkoak.issubset(taula.columns):
                taula = pd.read_csv(bidea, encoding="utf-8")
        except Exception:
            taula = pd.read_csv(bidea, encoding="utf-8")

        falta = beharrezkoak.difference(taula.columns)
        if falta:
            raise ValueError(f"{bidea}: zutabe hauek falta dira: {sorted(falta)}")
        taula = taula.copy()
        taula["iturria"] = hilabetea
        zatiak.append(taula)

    bateratua = pd.concat(zatiak, ignore_index=True)
    kopuruak = {h: int((bateratua["iturria"] == h).sum()) for h in HILABETEAK}
    return bateratua, kopuruak


def ariketa_2_5_concat(
    urtarrila: pd.DataFrame, otsaila: pd.DataFrame
) -> pd.DataFrame:
    """Pilatu urtarrileko eta otsaileko salmenta-taulak errenkadaz errenkada."""
    return pd.concat(
        [urtarrila.assign(iturria="urtarrila"), otsaila.assign(iturria="otsaila")],
        ignore_index=True,
    )


def main() -> None:
    """Exekutatu adibide guztiak eta erakutsi irteera erreproduzigarriak."""
    notak = ariketa_1_2_matrizea()
    notak_reshape = notak.reshape(4, 6)
    notak_laua = notak.flatten()
    print("1.2 — PDFko ausazko notak (seed=42):")
    print(notak)
    print(f"shape={notak.shape}, ndim={notak.ndim}, size={notak.size}")
    print(f"reshape(4, 6)={notak_reshape.shape}; flatten={notak_laua.shape}")
    try:
        notak.reshape(5, 5)
    except ValueError as errorea:
        print(f"reshape(5, 5) ezinezkoa: {errorea}")

    prezioak = np.array([10.0, 25.0, 8.0, 50.0])
    prezio_amaierakoak, z_score = ariketa_1_3_prezioak(prezioak)
    print("\n1.3 — PDFko prezioak: BEZa eta deskontua:")
    print(prezio_amaierakoak.round(3))
    print("Z-score (5x4 datu sintetikoak; ddof=0):")
    print(z_score.round(3))

    stock = np.array([12, 0, 45, 3, 0, 78, 5, 0, 23, 1])
    agortuta, stock_berria = ariketa_1_4_stock(stock)
    print("\n1.4 — agortutako produktu kopurua:", int(agortuta.sum()))
    print("stock baxua (0 < stock < 5):", stock[(stock > 0) & (stock < 5)].tolist())
    print("stock < 5 balio guztiak 10era:", stock_berria.tolist())

    csv_bideak = [FIXTURE_DIR / f"{h}.csv" for h in HILABETEAK]
    salmentak, errenkadak_hilabeteka = ariketa_2_2_csvak(csv_bideak)
    print("\n2.2 — fixture sintetikoak (ez dira tutorearen CSVak):")
    print(salmentak.to_string(index=False))
    print(f"guztira={len(salmentak)}; hilabeteka={errenkadak_hilabeteka}")

    # 2.2 — Tutorearen CSV ofizialak (Moodle mock datuak)
    tutore_dir = Path("/home/tears/bigdata/04_Programazioa_5073/data/mock_datuak/Ariketa 2.2")
    if tutore_dir.is_dir():
        tutore_bideak = [tutore_dir / f"{h}.csv" for h in HILABETEAK]
        if all(p.is_file() for p in tutore_bideak):
            salmentak_tutorea, hilabeteka_tutorea = ariketa_2_2_csvak(tutore_bideak)
            print("\n2.2 — Tutorearen CSV ofizialak (mock datuak / Ariketa 2.2):")
            print(f"guztira={len(salmentak_tutorea)}; hilabeteka={hilabeteka_tutorea}")
            print(salmentak_tutorea.head(3).to_string(index=False))

    bi_hilabete = ariketa_2_5_concat(
        salmentak.loc[salmentak["iturria"] == "urtarrila"].drop(columns="iturria"),
        salmentak.loc[salmentak["iturria"] == "otsaila"].drop(columns="iturria"),
    )
    print("\n2.5 — urtarrila eta otsaila concat bidez:")
    print(bi_hilabete.to_string(index=False))
    print(
        f"shape={bi_hilabete.shape}; merge=JOIN gako baten bidez; "
        "concat=errenkadak pilatu"
    )


if __name__ == "__main__":
    main()
