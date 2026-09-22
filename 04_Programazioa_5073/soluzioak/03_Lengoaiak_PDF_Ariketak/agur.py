"""Agur pertsonalizatuaren gidoia.

Moduloa: 5073 - Lengoaiak eta Datu Zientzia
Atala: Ariketa 4.2 Git Lehen Urratsak
"""


def agurtu(izena: str) -> str:
    """Emandako izenarekin agur pertsonalizatua sortzen du."""
    garbia = izena.strip()
    if not garbia:
        return "Kaixo, ezezaguna!"
    return f"Kaixo, {garbia}! Ongi etorri Big Data ikastarora."


def main() -> None:
    izena = input("Sartu zure izena: ")
    print(agurtu(izena))


if __name__ == "__main__":
    main()
