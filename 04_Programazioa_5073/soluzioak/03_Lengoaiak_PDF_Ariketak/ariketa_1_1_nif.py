"""NIF (NAN / IFZ) Balioztatzaile Profesionala.

Moduloa: 5073 - Lengoaiak eta Datu Zientzia
Atala: 1.1 Python script-aren anatomia
Egilea: Big Data & AI Ikaslea

Deskribapena:
Script honek Python script estandar baten egitura osoa erakusten du:
- Modulu mailako docstring-a
- Inportazio estandarrak eta tipo-oharpenak (typing)
- Konstante globalak (HITZ_LARRIAK)
- Funtzio modularrak docstring eta salbuespenekin
- Sarrerako datuen balioztatzea (modulo 23 kalkulua)
- if __name__ == "__main__" sarrera-puntua eta errore-kudeaketa
"""

from __future__ import annotations

import re
import sys
from typing import Final

# Konstanteak (PEP 8 konbentzioa)
NIF_LETRAK: Final[str] = "TRWAGMYFPDXBNJZSQVHLCKE"
NIF_PATROIA: Final[re.Pattern[str]] = re.compile(r"^(\d{8})([A-Z])$")


def kontrol_letra_kalkulatu(zenbakiak: int) -> str:
    """NIF zenbakiei dagokien kontrol-letra kalkulatzen du modulo 23 erabiliz.

    Args:
        zenbakiak: 8 digituko zenbaki osoa (adib. 12345678).

    Returns:
        Kalkulatutako kontrol-letra maiuskulaz.

    Raises:
        ValueError: zenbakiak negatiboa bada edo 8 digitu baino gehiago baditu.
    """
    if zenbakiak < 0 or zenbakiak > 99_999_999:
        raise ValueError(f"Zenbakiak 0 eta 99999999 artean egon behar du: {zenbakiak}")
    indizea = zenbakiak % 23
    return NIF_LETRAK[indizea]


def nif_balioztatu(nif: str) -> tuple[bool, str]:
    """Emandako NIF katea balioztatzen du.

    Args:
        nif: Egiaztatu beharreko NIF katea (adib. '12345678Z' edo '12345678-Z').

    Returns:
        (Baliozkoa_da, Mezu_azalpena) bikotea.
    """
    garbia = nif.strip().upper().replace("-", "").replace(" ", "")

    bat_dator = NIF_PATROIA.match(garbia)
    if not bat_dator:
        return False, f"Formatu baliogabea ('{nif}'). 8 digitu eta letra bat izan behar ditu."

    zenbaki_str, emandako_letra = bat_dator.groups()
    zenbakiak = int(zenbaki_str)
    espero_letra = kontrol_letra_kalkulatu(zenbakiak)

    if emandako_letra != espero_letra:
        return False, (
            f"Kontrol-letra okerra: '{emandako_letra}' eman da, "
            f"baina '{espero_letra}' izan beharko luke ({zenbaki_str} % 23)."
        )

    return True, f"NIF baliozkoa da: {zenbaki_str}{emandako_letra}."


def main() -> int:
    """Script-aren exekuzio printzipala."""
    print("=" * 60)
    print("   NIF (NAN) BALIOZTATZAILE AUTOMATIKOA - 5073 ARIKETA 1.1")
    print("=" * 60)

    adibideak = [
        "12345678Z",  # Posibleki okerra letra
        "00000000T",  # 0 % 23 = 0 -> T (Zuzena)
        "72849102D",  # Ausazkoa
        "12345-A",    # Formatu motza
        "44332211Y",
    ]

    print("\n[1] Aurrez definitutako adibideen egiaztapena:")
    for adibidea in adibideak:
        baliozkoa, mezua = nif_balioztatu(adibidea)
        ikurra = "✅" if baliozkoa else "❌"
        print(f"  {ikurra} {adibidea:12} -> {mezua}")

    print("\n[2] Modu interaktiboa (utzi hutsik irteteko):")
    try:
        erabiltzaile_nif = input("Sartu NIF bat egiaztatzeko: ").strip()
        if erabiltzaile_nif:
            baliozkoa, mezua = nif_balioztatu(erabiltzaile_nif)
            ikurra = "✅" if baliozkoa else "❌"
            print(f"  {ikurra} Emaitza: {mezua}")
            return 0 if baliozkoa else 1
    except (EOFError, KeyboardInterrupt):
        print("\nSaioa amaituta.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
