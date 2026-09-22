"""Smoke test del setup, sin Internet ni datos de una fábrica.

No mide capacidad predictiva. Usa datos de juguete para probar interoperabilidad.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import platform
import subprocess
import sys
import tempfile
import time
from importlib import metadata
from pathlib import Path

from cnc_guard.runtime import configure_resources, project_root


def main() -> None:
    root = project_root()
    settings = configure_resources(root)
    start = time.perf_counter()
    pin_path = root / ".python-version"
    lock = root / "uv.lock"
    if not pin_path.is_file() or not lock.is_file():
        raise RuntimeError("Falta .python-version o uv.lock: completa primero la inicialización")
    if pin_path.read_text(encoding="utf-8").strip() != platform.python_version():
        raise RuntimeError("El parche de Python no coincide con .python-version")
    if sys.prefix == sys.base_prefix:
        raise RuntimeError("Ejecuta esta comprobación dentro del proyecto con uv run --locked")
    packages = {
        "numpy": "numpy",
        "pandas": "pandas",
        "scipy": "scipy",
        "scikit-learn": "sklearn",
        "duckdb": "duckdb",
        "pyarrow": "pyarrow",
        "joblib": "joblib",
        "matplotlib": "matplotlib",
        "jupyterlab": "jupyterlab",
        "ipykernel": "ipykernel",
        "nbconvert": "nbconvert",
        "nbformat": "nbformat",
        "pytest": "pytest",
        "psutil": "psutil",
    }
    versions = {}
    for distribution, module in packages.items():
        importlib.import_module(module)
        versions[distribution] = metadata.version(distribution)
    versions["ruff"] = metadata.version("ruff")

    import duckdb
    import joblib
    import matplotlib
    import numpy as np
    import pandas as pd
    import psutil
    from sklearn.ensemble import IsolationForest, RandomForestClassifier

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Datos de juguete: no son telemetría industrial ni una evaluación de ML.
    rng = np.random.default_rng(settings["resources"]["random_seed"])
    features = rng.normal(size=(200, 4)).astype("float32")
    target = (features[:, 0] + features[:, 1] > 0).astype("int8")
    frame = pd.DataFrame(features, columns=["a", "b", "c", "d"])
    frame["label"] = target
    with tempfile.TemporaryDirectory(prefix="cnc-guard-check-") as temporary:
        folder = Path(temporary)
        parquet = folder / "check.parquet"
        frame.to_parquet(parquet, index=False, compression="zstd")
        pd.testing.assert_frame_equal(frame, pd.read_parquet(parquet))
        with duckdb.connect(
            config={
                "threads": settings["resources"]["duckdb_threads"],
                "memory_limit": settings["resources"]["duckdb_memory_limit"],
                "temp_directory": str(folder / "duckdb-temp"),
            }
        ) as connection:
            result = connection.execute(
                "SELECT count(*) FROM read_parquet(?)", [str(parquet)]
            ).fetchone()
        if result is None or result[0] != len(frame):
            raise RuntimeError("DuckDB no devuelve el número esperado de filas")
        model = RandomForestClassifier(n_estimators=8, max_depth=3, random_state=42, n_jobs=1)
        model.fit(features, target)
        predictions = model.predict(features[:5])
        stored = folder / "self-generated.joblib"
        joblib.dump(model, stored)
        # Se carga EXCLUSIVAMENTE el modelo recién generado por este mismo script.
        restored = joblib.load(stored)
        np.testing.assert_array_equal(predictions, restored.predict(features[:5]))
        anomaly = IsolationForest(n_estimators=8, max_samples=64, random_state=42, n_jobs=1)
        anomaly.fit(features)
        if not np.isfinite(anomaly.decision_function(features[:5])).all():
            raise RuntimeError("Puntuaciones de anomalía no finitas")
        fig, ax = plt.subplots()
        ax.plot([0, 1, 2], [0, 1, 0])
        fig.savefig(folder / "check.png")
        plt.close(fig)
    uv_version = subprocess.run(["uv", "--version"], check=True, capture_output=True, text=True)
    report = {
        "purpose": "Prueba de instalación; no validación predictiva ni industrial",
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "os": platform.system(),
        "machine": platform.machine(),
        "uv": uv_version.stdout.strip(),
        "versions": versions,
        "uv_lock_sha256": hashlib.sha256(lock.read_bytes()).hexdigest(),
        "smoke_seconds": round(time.perf_counter() - start, 3),
        "rss_end_mib_not_peak": round(psutil.Process().memory_info().rss / 1024**2, 2),
        "status": "passed",
    }
    destination = root / "reports" / "environment.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
