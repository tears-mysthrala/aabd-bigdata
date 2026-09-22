"""Preparar carpetas y, solo al inicializar, fijar el parche de Python.

No instala paquetes, no borra entornos y no modifica Python/Rust globales.
Ejecutar la inicialización una sola vez por proyecto; compartir .python-version.
"""

from __future__ import annotations

import argparse
import platform
import subprocess
import sys
import tomllib
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--initialize", action="store_true", help="Fijar Python y registrar uv")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    with (root / "pyproject.toml").open("rb") as handle:
        manifest = tomllib.load(handle)
    if manifest.get("project", {}).get("name") != "cnc-guard":
        raise SystemExit("El manifiesto no corresponde a CNC Guard")
    if sys.version_info[:2] != (3, 13) or platform.python_implementation() != "CPython":
        raise SystemExit("Este perfil requiere CPython 3.13 estándar de 64 bits")
    if sys.maxsize <= 2**32:
        raise SystemExit("Se requiere un intérprete de 64 bits")
    for folder in ("data/raw", "data/processed", "data/samples", "reports", "models", "docs"):
        (root / folder).mkdir(parents=True, exist_ok=True)
    if args.initialize:
        pin = root / ".python-version"
        if pin.exists() or (root / "uv.lock").exists():
            raise SystemExit(
                "Ya existe un pin o un lock. No reinicializar: usar el flujo de réplica."
            )
        result = subprocess.run(["uv", "--version"], check=True, capture_output=True, text=True)
        # Modo x: fallar si otro proceso ha creado el archivo mientras tanto.
        with pin.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(platform.python_version() + "\n")
        (root / "docs" / "uv-version.txt").write_text(
            result.stdout.strip() + "\n", encoding="utf-8"
        )
        print(f"Python fijado: {platform.python_version()}")
        print("Siguiente paso: uv lock --managed-python")
    else:
        print("Carpetas preparadas; no se ha modificado .python-version ni uv.lock")


if __name__ == "__main__":
    main()
