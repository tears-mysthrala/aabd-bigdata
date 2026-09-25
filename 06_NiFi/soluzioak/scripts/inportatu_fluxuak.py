#!/usr/bin/env python3
"""Listar los flows del laboratorio o delegar su importación segura."""

import os
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]


def main() -> None:
    flows = sorted(BASE_DIR.rglob("flow_*.json"))
    print(f"Fluxuak ({len(flows)}):")
    for flow in flows:
        print(f"  {flow.relative_to(BASE_DIR)}")

    if sys.argv[1:] == ["--list"]:
        return
    if sys.argv[1:]:
        raise SystemExit("Uso: inportatu_fluxuak.py [--list]")

    importer = Path(__file__).with_name("kargatu_fluxu_guztiak.py")
    os.execv(sys.executable, [sys.executable, str(importer)])


if __name__ == "__main__":
    main()
