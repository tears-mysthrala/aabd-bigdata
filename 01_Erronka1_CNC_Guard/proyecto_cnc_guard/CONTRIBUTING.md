# Contribuir a CNC Guard

Gracias por contribuir. Este repositorio es una plantilla académica para el reto de mantenimiento predictivo de CNC. Las contribuciones deben mantener la reproducibilidad, evitar datos industriales sensibles y respetar el alcance educativo del proyecto.

## Antes de empezar

1. Lee el [README](README.md) y la [guía de instalación](INSTALACION_CNC_GUARD_UV_JUPYTER.md).
2. Lee el [enunciado del reto](docs/1Erronka_ikaslearen_txostena.pdf).
3. Comprueba que tienes CPython 3.13 de 64 bits, `uv` y Git.
4. Trabaja en una rama descriptiva. No subas `.venv`, cachés, secretos, datasets industriales ni notebooks con credenciales.

## Entorno local

Desde la raíz del proyecto:

```bash
uv sync --locked --managed-python
uv run --locked python scripts/bootstrap.py
```

Para una dependencia nueva, declárala en `pyproject.toml` mediante `uv add` y revisa el `uv.lock` generado. No instales paquetes con `pip` dentro de Jupyter ni edites manualmente el lock.

## Cambios en notebooks y datos

- Mantén las rutas relativas al proyecto mediante `cnc_guard.runtime.project_root()`.
- No incluyas datos personales, secretos, IP de máquinas, certificados ni telemetría real sin autorización explícita.
- El notebook debe poder ejecutarse con **Restart Kernel → Run All**.
- Registra origen, licencia, versión y SHA-256 de cada dataset autorizado.
- Usa datos pequeños o sintéticos en las pruebas y en los ejemplos versionados.
- No cargues modelos `pickle` o `joblib` de procedencia desconocida.

## Comprobaciones obligatorias

Antes de abrir una pull request:

```bash
uv run --locked python scripts/verify_setup.py
uv run --locked pytest -q
uv run --locked ruff check src scripts tests
uv run --locked ruff format --check src scripts tests
uv run --locked python -c "import nbformat; nbformat.validate(nbformat.read('00_verificacion_entorno.ipynb', as_version=4))"
uv run --locked jupyter nbconvert --to notebook --execute 00_verificacion_entorno.ipynb --output 00_verificacion_entorno.ejecutado.ipynb --output-dir reports --ExecutePreprocessor.kernel_name=cnc-guard --ExecutePreprocessor.timeout=600
```

El workflow de GitHub ejecuta estas comprobaciones en Ubuntu, Windows y macOS. El estado verde del CI no sustituye la revisión del modelo, la calidad de los datos ni la autorización para conectar con una CNC.

## Pull requests

- Explica el problema, el cambio realizado y cómo lo has validado.
- Mantén los cambios pequeños y evita reformatear archivos no relacionados.
- Actualiza la documentación cuando cambies comandos, dependencias, rutas o límites de seguridad.
- Incluye una nota sobre el impacto en privacidad, trazabilidad o seguridad cuando sea relevante.
- No subas secretos para que el CI acceda a una máquina, broker o base de datos.

El proyecto no tiene todavía un mantenedor o una lista de CODEOWNERS configurados. La revisión final corresponde al equipo docente y a los responsables del repositorio.