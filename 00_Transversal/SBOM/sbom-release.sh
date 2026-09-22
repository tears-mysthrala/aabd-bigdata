#!/usr/bin/env bash
# SBOM versionada por release. Todo local: no publica ni registra nada fuera.
# Uso:
#   ./sbom-release.sh 0.1.0            # SBOM/releases/0.1.0/
#   ./sbom-release.sh 0.1.0 /ruta/mod  # alcance limitado a un módulo
# Regla: una release = una SBOM nueva. Nunca se sobrescribe una existente.
set -euo pipefail
cd "$(dirname "$0")/.."

VERSION="${1:?Uso: sbom-release.sh <version> [ruta-alcance]}"
if [[ "$VERSION" == "-h" || "$VERSION" == "--help" ]]; then
  echo "Uso: sbom-release.sh <version> [ruta-alcance]"
  echo "Ej:  sbom-release.sh 0.1.0   |   sbom-release.sh 0.1.0 /home/tears/bigdata/erronka1/cnc_guard_setup"
  exit 0
fi
SCOPE="${2:-/home/tears/bigdata}"
DEST="SBOM/releases/$VERSION"

if [[ -e "$DEST" ]]; then
  echo "Ya existe $DEST: asigna una versión nueva, no se sobrescribe." >&2
  exit 1
fi
command -v syft >/dev/null || { echo "falta syft" >&2; exit 1; }

mkdir -p "$DEST"
syft "$SCOPE" \
  -o "cyclonedx-json=$DEST/sbom.cyclonedx.json" \
  -o "spdx-json=$DEST/sbom.spdx.json" 2>"$DEST/syft-warnings.log" || {
  echo "syft falló, ver $DEST/syft-warnings.log" >&2; exit 1; }

# Índice acumulativo (versión, fecha, alcance, nº componentes).
FECHA=$(date -u +%Y-%m-%dT%H:%M:%SZ)
NCOMP=$(python3 -c "import json;print(len(json.load(open('$DEST/sbom.cyclonedx.json')).get('components',[])))")
[[ -f SBOM/INDICE.csv ]] || echo "version,fecha_utc,alcance,componentes" > SBOM/INDICE.csv
echo "$VERSION,$FECHA,$SCOPE,$NCOMP" >> SBOM/INDICE.csv

echo "OK: $DEST ($NCOMP componentes). Recuerda fijar esta versión en SOPORTE.md si se reutiliza."
