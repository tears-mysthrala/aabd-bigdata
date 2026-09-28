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

### Comprobaciones de secretos y datos personales

El workflow de PR ejecuta Gitleaks sobre el historial alcanzable del checkout
y TruffleHog sobre los SHA de base y cabecera de la PR. Una ejecución que falla
antes de escanear no constituye una comprobación limpia.

Para repetir Gitleaks localmente sin imprimir secretos:

```bash
gitleaks git --log-opts=HEAD --config .gitleaks.toml --redact=100
```

La configuración conserva las reglas predeterminadas y exceptúa únicamente
un UUID verificado de Controller Service, en una propiedad y un archivo de NiFi
concretos. No se excluyen flujos completos ni la detección de claves AWS.

Los CSV docentes se conservan intencionalmente. En particular, COMPAS contiene
identificadores personales e información judicial del dataset público original;
no es un dataset anonimizado. Los ejemplos de clientes de ingeniería de datos
proceden de Faker. Los escáneres de secretos no verifican anonimización ni
revisan el contenido visual de PDFs, capturas y vídeos.

La SBOM (`00_Transversal/SBOM/`) documenta dependencias, **no certifica** la
seguridad del host, red ni integraciones industriales. Al reutilizar un módulo
fuera del lab, declara soporte y contacto de vulnerabilidades (plantilla en
`00_Transversal/SBOM/SOPORTE.md`).
