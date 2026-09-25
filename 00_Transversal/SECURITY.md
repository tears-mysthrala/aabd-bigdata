# Política de seguridad del lab `~/bigdata`

Laboratorio académico. Nada de aquí se publica ni se registra fuera:
es higiene para poder reutilizar módulos sin empezar de cero.

## Informar de una vulnerabilidad

No publiques vulnerabilidades, credenciales, tokens ni datos sensibles
en issues o PRs. Aviso privado a quien mantenga el módulo afectado,
incluyendo: descripción reproducible y versión/commit, impacto,
pasos mínimos sin datos reales, logs saneados y mitigación si la hay.
Detalle por proyecto en `01_Erronka1_CNC_Guard/proyecto_cnc_guard/SECURITY.md`.

## Reglas del lab

- Jupyter solo en `127.0.0.1` con token; nunca `0.0.0.0` ni sin autenticación.
- Dependencias solo vía `uv` + lock versionado (`uv.lock`); prohibido
  `sudo pip`, `pip install --user`, `--system` e instalaciones desde celdas.
- Revisar el diff de `uv.lock` y pasar `pip-audit` antes de hitos/entregas.
- Secretos solo en `.env` (nunca en repo, notebooks, capturas ni logs).
- `pickle`/`joblib` solo de procedencia propia y verificada.
- Docker: sin `chmod 666` al socket; cada persona en el grupo `docker`.
- SBOM: `00_Transversal/SBOM/` (base) + `00_Transversal/SBOM/releases/<version>/` por release
  (`sbom-release.sh`); soporte declarado en `00_Transversal/SBOM/SOPORTE.md`;
  ficha por módulo reutilizado según `00_Transversal/SBOM/FICHA-TECNICA.md`.

## Qué NO cubre esto

La SBOM documenta dependencias, no certifica seguridad del host,
firmware, red OT ni integraciones industriales. Al reutilizar un módulo
fuera del lab, rellenar su ficha, declarar soporte y contacto de
vulnerabilidades, y aplicar el procedimiento de notificación del art. 14
(aplicable desde el 11-09-2026) si se comercializa en la UE.
