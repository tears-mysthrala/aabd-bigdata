# Seguridad

Repositorio de **material de estudio**. La política operativa del laboratorio
está en [`00_Transversal/SECURITY.md`](00_Transversal/SECURITY.md); aquí el
resumen aplicable a quien lo clone o contribuya.

## Avisar de un problema

**No publiques** vulnerabilidades, credenciales, tokens ni datos sensibles en
issues o PRs. Aviso privado a quien mantenga el repositorio (ver
[README](README.md)), incluyendo: descripción reproducible, impacto, pasos
mínimos sin datos reales y mitigación si la hay.

## Reglas para reutilizar este material

- Los `.env` con contraseñas **no se versionan** (ver `.gitignore`); copia
  `.env.example` y cambia todos los valores antes de `docker compose up`.
- MongoDB y Kafka van **sin autenticación y solo en `127.0.0.1`**: correcto
  para el lab, inseguro fuera de él. Activa auth/TLS si lo expones.
- Jupyter solo en `127.0.0.1` **con token**; nunca `0.0.0.0` ni sin autenticación.
- Dependencias solo vía `uv` + lock versionado; revisa el diff de `uv.lock` y
  pasa `pip-audit` antes de entregar o reutilizar un módulo.
- `pickle`/`joblib` solo de procedencia propia y verificada.
- Docker: sin `chmod 666` al socket; cada persona en el grupo `docker`.

## Alcance

La SBOM (`00_Transversal/SBOM/`) documenta dependencias, **no certifica** la
seguridad del host, red ni integraciones industriales. Al reutilizar un módulo
fuera del lab, declara soporte y contacto de vulnerabilidades (plantilla en
`00_Transversal/SBOM/SOPORTE.md`).
