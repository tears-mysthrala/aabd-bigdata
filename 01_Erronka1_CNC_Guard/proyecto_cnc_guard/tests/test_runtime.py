from pathlib import Path

import pytest

from cnc_guard.runtime import configure_resources, project_root


def test_root_is_project() -> None:
    root = project_root()
    assert (root / "pyproject.toml").is_file()


def test_missing_root(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        project_root(tmp_path)


def test_resources(monkeypatch: pytest.MonkeyPatch) -> None:
    # Restaurar variables al finalizar la prueba.
    for variable in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
    ):
        monkeypatch.setenv(variable, "8")
    settings = configure_resources()
    assert settings["resources"]["model_jobs"] == 2
    assert settings["resources"]["batch_rows"] > 0
