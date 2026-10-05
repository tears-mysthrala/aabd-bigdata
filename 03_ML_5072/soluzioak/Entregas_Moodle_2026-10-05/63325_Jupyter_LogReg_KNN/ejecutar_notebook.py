"""Ejecutar la práctica desde un kernel limpio y verificar las salidas guardadas."""

import json
import sys
from pathlib import Path

import nbformat
from jupyter_client.manager import KernelManager
from nbclient import NotebookClient

BASE = Path(__file__).resolve().parent


def main():
    path = BASE / "iris_logreg_knn.ipynb"
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    manager = KernelManager(kernel_name="python3")
    manager.kernel_spec.argv = [
        sys.executable,
        "-m",
        "ipykernel_launcher",
        "-f",
        "{connection_file}",
    ]
    NotebookClient(
        notebook, km=manager, timeout=120, resources={"metadata": {"path": str(BASE)}}
    ).execute()
    code = [cell for cell in notebook.cells if cell.cell_type == "code"]
    assert len(code) == 6 and all(cell.execution_count is not None for cell in code)
    assert not any(
        output.output_type == "error" for cell in code for output in cell.outputs
    )
    results = json.loads((BASE / "resultados.json").read_text())
    assert results["n"] == 150
    for key, correct in [("logreg", 123), ("knn", 128)]:
        matrix = results[key]["confusion_matrix"]
        assert sum(sum(row) for row in matrix) == 150
        assert sum(matrix[i][i] for i in range(3)) == correct
        assert results[key]["correct"] == correct
        assert results[key]["accuracy"] == correct / 150
    nbformat.write(notebook, path)
    print(
        "Notebook: seis celdas ejecutadas, sin errores; matrices y 123/128 aciertos verificados."
    )


if __name__ == "__main__":
    main()
