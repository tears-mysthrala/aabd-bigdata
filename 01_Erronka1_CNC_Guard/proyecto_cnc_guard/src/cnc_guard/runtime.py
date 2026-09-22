"""Configuración y rutas comunes para scripts y notebooks."""

from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any


def project_root(start: Path | None = None) -> Path:
    """Buscar el proyecto desde el directorio actual sin rutas personales fijas."""
    origin = (start or Path.cwd()).resolve()
    if origin.is_file():
        origin = origin.parent
    for candidate in (origin, *origin.parents):
        manifest = candidate / "pyproject.toml"
        if manifest.is_file():
            with manifest.open("rb") as handle:
                metadata = tomllib.load(handle)
            if metadata.get("project", {}).get("name") == "cnc-guard":
                return candidate
    raise FileNotFoundError("Ejecuta desde la raíz de CNC Guard o una de sus subcarpetas.")


def configure_resources(root: Path | None = None) -> dict[str, Any]:
    """Ejecutar ANTES de importar NumPy/scikit-learn en un kernel nuevo.

    Estos límites no son cuotas duras de CPU/RAM del proceso. La configuración
    model_jobs debe pasarse a cada estimador; DuckDB se configura por conexión.
    """
    root = root or project_root()
    with (root / "config" / "resources.toml").open("rb") as handle:
        settings = tomllib.load(handle)
    threads = int(settings["resources"]["blas_threads"])
    if threads < 1:
        raise ValueError("blas_threads debe ser positivo")
    for variable in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
    ):
        os.environ[variable] = str(threads)
    return settings
