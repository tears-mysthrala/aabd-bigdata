# Contribuir

## Dónde va cada cosa

Nueva materia → `0X_Nombre/materialak/`. Nueva solución → `0X_Nombre/soluzioak/`.
Nada suelto en la raíz salvo este índice y los symlinks de compatibilidad.
La regla completa está en [INDICE.md](INDICE.md).

## Formato de soluciones (el que ya funciona)

- **Dual `.ipynb` + `.py`** con celdas `# %%` (el `.py` debe correr con
  `python fichero.py` sin Jupyter).
- **Asserts** que fallen si el resultado es incorrecto (no `print` sin comprobar).
- **Datos**: en la carpeta `data/` de su asignatura; rutas con `pathlib`
  (`Path(__file__)`), nunca absolutas salvo fallback documentado.
- **Entorno**: `uv venv && uv sync` con `pyproject.toml` + `uv.lock` versionado.
  Prohibido `sudo pip`, `pip install --user` e instalaciones desde celdas.
- **Notebooks docentes** (`materialak/`): no convertir sus `!pip install`
  de ejemplo en costumbre; ejecútalos solo en venv desechable.

## Commits y PR

- [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`…
- Una rama `feat/nombre` por cambio, merge con `--no-ff` (ejemplo vivo en
  `04_Programazioa_5073/git_ariketa_4_2/PR_DESC.md`).
- Antes de PR: tests en verde + `pip-audit` si tocas dependencias
  (`uv sync --group security && uv run --group security pip-audit`).

## Seguridad (resumen; detalle en [SECURITY.md](SECURITY.md))

- Secretos solo en `.env` (jamás en código, notebooks, issues ni capturas).
  Hay `.env.example` como plantilla; el `.env` real está gitignoreado.
- Sin credenciales por defecto en scripts (fallo rápido si falta la variable).
- Servicios Docker atados a `127.0.0.1`; nada de `chmod 666` al socket.
- `pickle`/`joblib` solo de procedencia propia y verificada.
- Cada release reutilizable lleva su SBOM en `00_Transversal/SBOM/releases/`
  (`sbom-release.sh <version>`); una release nunca se sobrescribe.
