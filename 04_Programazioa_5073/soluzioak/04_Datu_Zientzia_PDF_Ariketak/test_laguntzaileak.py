"""Tranpa-fixtures: 200 fitxategi zikin vs laguntzaileak. `python test_laguntzaileak.py`."""

import tempfile
from pathlib import Path

from laguntzaileak import aurkitu, balio_erabilgarria, pilatu_csvak

ZUT = ["produktua", "unitateak", "prezioa"]


def _fixtures(d: Path) -> dict:
    """200 CSV: baliozkoak (1-2 errenkada) + latin-1 + malformituak + hutsak +
    zutabe-okerrak + koma-dezimalak + zuriune-zutabeak. Espero: 150+20+10+5 koma."""
    n_ok = 0
    for i in range(150):  # baliozkoak, errenkada erabilgarri 1-2
        (d / f"f{i:03d}.csv").write_text(
            "produktua,unitateak,prezioa\n"
            f"P{i},2,10.0\n" + ("X,1,1.0\n" if i % 2 else ""),
            encoding="utf-8",
        )
        n_ok += 2 if i % 2 else 1
    for i in range(20):  # latin-1 azentuekin
        (d / f"l{i:03d}.csv").write_bytes(
            "produktua,unitateak,prezioa\n´Tildegia,3,5.0\n".encode("latin-1")
        )
        n_ok += 1
    for i in range(10):  # lerro malformituak (saltatu)
        (d / f"m{i:03d}.csv").write_text(
            "produktua,unitateak,prezioa\nOK,1,2.0\nTXARRA,lerro,luze,egia\n",
            encoding="utf-8",
        )
        n_ok += 1
    for i in range(5):  # hutsak
        (d / f"e{i:03d}.csv").write_text("", encoding="utf-8")
    for i in range(5):  # zutabe okerrak
        (d / f"w{i:03d}.csv").write_text("a,b,c\n1,2,3\n", encoding="utf-8")
    for i in range(5):  # koma-dezimalak + €
        (d / f"k{i:03d}.csv").write_text(
            'produktua,unitateak,prezioa\nK,1,"1.234,56 €"\n', encoding="utf-8"
        )
        n_ok += 1
    for i in range(5):  # zutabe-izen zikinak
        (d / f"s{i:03d}.csv").write_text(
            " produktua , unitateak , prezioa \nS,4,2.5\n", encoding="utf-8"
        )
        n_ok += 1
    return {"ok": n_ok}  # 225 (f) + 20 (l) + 10 (m) + 5 (k) + 5 (s) = 265


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="tranpak-") as tmp:
        d = Path(tmp)
        esp = _fixtures(d)
        assert len(aurkitu("*.csv", d)) == 200, "200 fixture"

        df, tx = pilatu_csvak("*.csv", d, ZUT, ("unitateak", "prezioa"))
        assert len(df) == esp["ok"], (len(df), esp["ok"])
        assert set(tx["egoera"].unique()) >= {"ok"}, (
            tx["egoera"].value_counts().to_dict()
        )
        tx_err = tx[tx["egoera"] != "ok"]
        assert len(tx_err) == 10, f"10 txar (5 huts + 5 zutabe-oker): {len(tx_err)}"
        # koma-dezimala ondo: 1234.56
        assert (
            abs(float(df[df["produktua"] == "K"]["prezioa"].iloc[0]) - 1234.56) < 0.01
        )
        # 1-datu: lehen balio erabilgarria
        assert balio_erabilgarria(df, "prezioa") is not None
        print(
            f"tranpak: {len(df)} errenkada, {len(tx_err)} fitxategi txar detektatuta ✅"
        )

    # Q1 erreala helper berarekin (2.2-rekin bat):
    dfq, txq = pilatu_csvak(
        "*.csv",
        "data",
        None,
        (),
        etiketa_fn=lambda p: (
            p.stem.capitalize()
            if p.stem in ("urtarrila", "otsaila", "martxoa")
            else None
        ),
    )
    # etiketa None dutenak iragazi (beste CSVak)
    dfq = dfq[dfq["iturria"].isin(["Urtarrila", "Otsaila", "Martxoa"])].reset_index(
        drop=True
    )
    dfq["salmenta_osoa"] = dfq["unitateak"] * dfq["prezioa"]
    assert len(dfq) == 12 and abs(dfq["salmenta_osoa"].sum() - 25110.00) < 0.01
    print("Q1 helper: 12 errenkada, 25,110.00 € ✅ (bat 2.2-rekin)")


if __name__ == "__main__":
    main()
