# %%
"""Ariketa 2.3: CSV berriko bezero-datu zikinak garbitu.

Exekutatu modulu honen direktoriotik edo edonondik:
    python ariketa_2_3_datu_berria.py
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

# %%
BEHARREZKO_ZUTABEAK = ["izena", "adina", "hiria", "soldata"]
SOLUTION_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
IRTEERA_DIR = SOLUTION_DIR / "data"
SARRERA = (
    SOLUTION_DIR.parents[1]
    / "data"
    / "mock_datuak"
    / "Ariketa 2.3"
    / "datu_zikinak.csv"
)
CSV_GARBIA = IRTEERA_DIR / "datu_zikinak_garbia.csv"
LABURPENA_JSON = IRTEERA_DIR / "datu_zikinak_laburpena.json"


def garbitu_datuak(entrada: Path) -> tuple[pd.DataFrame, dict[str, object]]:
    """Kargatu eta garbitu bezeroen CSVa; sarrera-fitxategia irakurtzeko soilik da."""
    jatorrizkoa = pd.read_csv(entrada, sep=";")
    assert set(BEHARREZKO_ZUTABEAK).issubset(jatorrizkoa.columns), (
        f"Beharrezko zutabeak: {BEHARREZKO_ZUTABEAK}; jasotakoak: {list(jatorrizkoa.columns)}"
    )
    assert len(jatorrizkoa) > 0, "Sarrera CSVak gutxienez errenkada bat izan behar du."
    for zutabea in ("izena", "hiria", "soldata"):
        jatorrizkoa[zutabea] = jatorrizkoa[zutabea].astype("string")

    missing = jatorrizkoa[BEHARREZKO_ZUTABEAK].isna().sum()
    missing_percentages = (
        jatorrizkoa[BEHARREZKO_ZUTABEAK].isna().mean().mul(100).round(2)
    )
    rows_before = int(len(jatorrizkoa))

    garbia = jatorrizkoa.copy()
    izen_zuriuneak_kenduta = garbia["izena"].str.strip()
    garbia["izena"] = izen_zuriuneak_kenduta.str.title()
    garbia["hiria"] = garbia["hiria"].str.strip().str.title()

    # Casefold-ek maiuskula/minuskula eta Unicode kasu-aldaerak bateratzen ditu.
    izen_gakoa = izen_zuriuneak_kenduta.str.casefold()
    bikoiztua = izen_gakoa.duplicated(keep="first")
    duplicate_rows = int(bikoiztua.sum())
    garbia = garbia.loc[~bikoiztua].copy()

    adinak = pd.to_numeric(garbia["adina"], errors="raise")
    adin_hutsak = int(adinak.isna().sum())
    if adinak.notna().any():
        adin_batezbestekoa = float(adinak.mean())
        garbia["adina"] = adinak.fillna(adin_batezbestekoa)
        if float(garbia["adina"].mod(1).abs().max()) == 0:
            garbia["adina"] = garbia["adina"].astype("int64")
    else:
        adin_batezbestekoa = None

    hiri_hutsak = int(garbia["hiria"].isna().sum())
    garbia["hiria"] = garbia["hiria"].fillna("Ezezaguna")

    soldata_jatorrizkoa = garbia["soldata"]
    soldata_testua = (
        soldata_jatorrizkoa.str.replace("€", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )
    soldata_zenbakia = pd.to_numeric(soldata_testua, errors="coerce")
    soldata_okerra = (
        soldata_jatorrizkoa.notna()
        & soldata_testua.ne("")
        & soldata_zenbakia.isna()
    )
    if soldata_okerra.any():
        balioak = soldata_jatorrizkoa.loc[soldata_okerra].tolist()
        raise ValueError(f"Ezin izan dira soldata-balio hauek zenbaki bihurtu: {balioak}")
    garbia["soldata"] = soldata_zenbakia

    summary: dict[str, object] = {
        "sarrera_fitxategia": Path(entrada).name,
        "zutabeak": BEHARREZKO_ZUTABEAK,
        "hasierako_errenkadak": rows_before,
        "amaierako_errenkadak": int(len(garbia)),
        "ezabatutako_izen_bikoiztuak": duplicate_rows,
        "hasierako_balio_galduak": {str(k): int(v) for k, v in missing.items()},
        "hasierako_balio_galduen_ehunekoak": {
            str(k): float(v) for k, v in missing_percentages.items()
        },
        "adina_bete_da_batezbestekoarekin": adin_hutsak,
        "adina_batezbestekoa_bikoiztuak_kendu_ondoren": adin_batezbestekoa,
        "hiria_bete_da_ezezaguna": hiri_hutsak,
        "soldata_hutsak_gordeta": int(garbia["soldata"].isna().sum()),
        "soldata_zenbakitan": True,
        "soldata_formatuaren_hipotesia": "Puntua milako-banatzailea da; € ikurra kendu da; koma hamartarrak puntu bihurtu dira.",
        "bikoiztu_hipotesia": "Lehen errenkada mantendu da izena zuriuneak kendu ondoren casefold bidez parekatuta.",
        "adina_hutsaren_hipotesia": "Batezbestekoa bikoiztuak kendutako errenkadetako adin ez-hutsekin kalkulatu da.",
    }
    assert list(garbia.columns) == BEHARREZKO_ZUTABEAK
    return garbia.reset_index(drop=True), summary

# %%
def main() -> None:
    """Sortu garbitutako CSVa eta haren laburpen erreproduzigarria."""
    datuak, laburpena = garbitu_datuak(SARRERA)
    IRTEERA_DIR.mkdir(parents=True, exist_ok=True)
    datuak.to_csv(CSV_GARBIA, index=False, na_rep="")
    LABURPENA_JSON.write_text(
        json.dumps(laburpena, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(datuak.to_string(index=False))
    print(f"\nLaburpena: {LABURPENA_JSON}")
    print(f"CSV garbia: {CSV_GARBIA}")


if __name__ == "__main__":
    main()
