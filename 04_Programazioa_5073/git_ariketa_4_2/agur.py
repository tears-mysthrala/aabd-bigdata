"""Agur pertsonalizatua (ariketa 4.2 + feature branch 4.4: --izena arg)."""

from __future__ import annotations

import argparse


def agurtu(izena: str) -> str:
    """Emandako izenarekin agur pertsonalizatua sortzen du."""
    izena = izena.strip()
    if not izena:
        raise ValueError("Izena ezin da hutsik egon.")
    return f"Kaixo, {izena}!"


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="Agur pertsonalizatua")
    ap.add_argument("--izena", default=None, help="Izena zuzenean (bestela galdetu)")
    args = ap.parse_args(argv)
    izena = args.izena.strip() if args.izena else input("Sartu zure izena: ").strip()

    if not izena:
        print("Izena ezin da hutsik egon.")
        return

    print(agurtu(izena))


if __name__ == "__main__":
    main()
