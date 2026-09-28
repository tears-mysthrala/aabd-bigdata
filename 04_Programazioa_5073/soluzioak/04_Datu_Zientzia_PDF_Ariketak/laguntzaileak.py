"""Laguntzaileak azterketarako: irakasle-tranpak jasan ditzakeen CSV karga.

Tranpak: encoding okerrak, lerro malformituak, zutabe okerrak/hutsak, fitxategi
hutsak, ehunka fitxategi datu erabilgarri 1ekin, koma-dezimalak, euro-ikurrak.
Menpekotasun berririk gabe: stdlib + pandas (+ numpy zenbakietan).

Azterketan: kopiatu fitxategi hau eta `pilatu_csvak("data/*.csv", ...)` 3 lerro.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ENCODINGAK = ("utf-8", "utf-8-sig", "latin-1")


def aurkitu(pattern: str, root: str | Path = ".") -> list[Path]:
    """Glob ordenatua (determinista): `aurkitu('*.csv', 'data')`."""
    return sorted(Path(root).glob(pattern))


def _zenbakira(serie: pd.Series) -> pd.Series:
    """'1.234,56 €' -> 1234.56; '805.0' -> 805.0 (koma badago, puntua milaka da;
    komarik gabe, puntua dezimala da). Zuriuneak eta € garbitzen ditu."""
    s = serie.astype(str).str.strip().str.replace("€", "", regex=False).str.strip()
    koma = s.str.contains(",", na=False)
    kont = s.str.replace(r"\.", "", regex=True).str.replace(",", ".", regex=False)
    return pd.to_numeric(s.where(~koma, kont), errors="coerce")


def kargatu_gogorra(
    bidea: str | Path,
    zutabeak: tuple[str, ...] | list[str] | None = None,
    zenbakizkoak: tuple[str, ...] | list[str] = (),
    etiketa: str | None = None,
) -> tuple[pd.DataFrame | None, dict]:
    """CSV 1 gogor kargatu. (df | None, info) itzultzen du — ez du inoiz eztanda egiten.

    - encodingak probatzen ditu ordenan; lerro txarrak saltatzen (`on_bad_lines`).
    - `zutabeak` faltan badira -> (None, info errorearekin).
    - `zenbakizkoak` koma/euro-garbiketarekin behartzen ditu.
    - `etiketa` zutabe gisa gehitzen du (normalean fitxategi-izena).
    """
    bidea = Path(bidea)
    info: dict = {"fitxategia": bidea.name, "egoera": "ok", "errenkadak": 0}
    df = None
    for enc in ENCODINGAK:
        try:
            df = pd.read_csv(bidea, encoding=enc, on_bad_lines="skip")
            info["encoding"] = enc
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:  # fitxategi hutsa, baimenak, ...
            info.update(egoera=f"errorea: {type(e).__name__}")
            return None, info
    if df is None:
        info.update(egoera="errorea: encodingik ez")
        return None, info
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(axis=0, how="all").dropna(axis=1, how="all")
    if zutabeak:
        falta = [c for c in zutabeak if c not in df.columns]
        if falta:
            info.update(egoera=f"zutabeak falta: {falta}")
            return None, info
        df = df[list(zutabeak)]
    for col in zenbakizkoak:
        if col in df.columns:
            df[col] = _zenbakira(df[col])
    if etiketa is not None:
        df["iturria"] = etiketa
    info["errenkadak"] = len(df)
    return df, info


def pilatu_csvak(
    pattern: str,
    root: str | Path = ".",
    zutabeak: tuple[str, ...] | list[str] | None = None,
    zenbakizkoak: tuple[str, ...] | list[str] = (),
    etiketa_fn=None,
    mugatu: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Glob + karga gogorra + concat + txostena. (df_pilatua, txostena).

    - `etiketa_fn(path) -> str`: iturria (defektua: stem).
    - Fitxategi txarrak ez dira kargatzen; txostenean agertzen dira.
    - `mugatu=N`: lehen N fitxategiak (ehunka fitxategirekin probak azkar).
    """
    etiketa_fn = etiketa_fn or (lambda p: p.stem)
    bideak = aurkitu(pattern, root)
    if mugatu is not None:
        bideak = bideak[:mugatu]
    zatiak, infos = [], []
    for bidea in bideak:
        df, info = kargatu_gogorra(bidea, zutabeak, zenbakizkoak, etiketa_fn(bidea))
        infos.append(info)
        if df is not None and len(df):
            zatiak.append(df)
    txostena = pd.DataFrame(infos)
    if not zatiak:
        return pd.DataFrame(), txostena
    return pd.concat(zatiak, ignore_index=True), txostena


def balio_erabilgarria(df: pd.DataFrame, zutabea: str):
    """Fitxategi 1-datuetarako: zutabeko lehen balio baliogabe-eza (NaNak saltatuz)."""
    s = pd.to_numeric(df[zutabea], errors="coerce").dropna()
    return s.iloc[0] if len(s) else None
