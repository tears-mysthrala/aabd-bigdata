#!/usr/bin/env bash
# Subir novedades 2026-09-30 al NotebookLM "AABD Big Data & IA".
# Requisito previo (interactivo, una vez): notebooklm login
# Uso: ./SUBIR_NOVEDADES_2026-09-30.sh [--dry-run|--publish]
# Por defecto solo valida y enumera archivos. --publish añade fuentes;
# no reemplaza ni elimina las existentes y puede crear duplicados.
set -euo pipefail
cd "$(dirname "$0")/../.."

NB="3db48c6c-0f7a-43c6-b9d0-0ae3b88be9d2"
MODE="${1:---dry-run}"
if [ "$#" -gt 1 ] || [[ "$MODE" != --dry-run && "$MODE" != --publish ]]; then
  echo "Uso: $0 [--dry-run|--publish]" >&2
  exit 2
fi

add() {
  local file="$1"
  [ -f "$file" ] || { echo "ABORT: ez da fitxategia: $file" >&2; exit 1; }
  notebooklm source add -n "$NB" --type file "$file"
}

SOURCES=(
  "05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf"
  "INDICE.md"
  "07_Kafka/materialak/01_04_ApacheKafka_aurreratua.pdf"
  "04_Programazioa_5073/materialak/5073_3_Programazioa.pdf"
  "03_ML_5072/materialak/5072_2_03_KNN.pdf"
  "03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf"
  "03_ML_5072/materialak/Sailkapen_Ebaluazio-metrikak.md"
  "07_Kafka/soluzioak/kafka_aurreratua_2_kasua/Ebazpena_2_Kasua.md"
  "07_Kafka/soluzioak/kafka_aurreratua_connect/Ebazpena_Connect.md"
  "00_Transversal/AUDITORIA_EJERCICIOS.md"
)

for file in "${SOURCES[@]}"; do
  [ -f "$file" ] || { echo "ABORT: ez da fitxategia: $file" >&2; exit 1; }
done
if [[ "$MODE" == --dry-run ]]; then
  printf '%s\n' "${SOURCES[@]}"
  echo "DRY RUN: ${#SOURCES[@]} fuentes validadas; no se ha subido ninguna."
  exit 0
fi
command -v notebooklm >/dev/null || { echo "ABORT: falta notebooklm" >&2; exit 1; }
for file in "${SOURCES[@]}"; do
  add "$file"
done
echo "OK: ${#SOURCES[@]} operaciones de subida completadas."
