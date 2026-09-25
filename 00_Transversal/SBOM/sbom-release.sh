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
  echo "Ej:  sbom-release.sh 0.1.0   |   sbom-release.sh 0.1.0 /home/tears/bigdata/01_Erronka1_CNC_Guard/proyecto_cnc_guard"
  exit 0
fi
if [[ ! "$VERSION" =~ ^[[:alnum:]][[:alnum:]._-]*$ || "$VERSION" == "." || "$VERSION" == ".." ]]; then
  echo "Versión inválida: usa letras, números, puntos, guiones o guiones bajos." >&2
  exit 1
fi
SCOPE="${2:-$(cd ../ && pwd)}"
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
NCOMP=$(python3 - "$DEST/sbom.cyclonedx.json" <<'PY'
import json
import sys
with open(sys.argv[1], encoding="utf-8") as source:
    print(len(json.load(source).get("components", [])))
PY
)
[[ -f SBOM/INDICE.csv ]] || echo "version,fecha_utc,alcance,componentes" > SBOM/INDICE.csv
echo "$VERSION,$FECHA,$SCOPE,$NCOMP" >> SBOM/INDICE.csv

echo "OK: $DEST ($NCOMP componentes). Recuerda fijar esta versión en SOPORTE.md si se reutiliza."
