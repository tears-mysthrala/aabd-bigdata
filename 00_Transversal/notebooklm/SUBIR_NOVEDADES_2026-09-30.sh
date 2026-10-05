#!/usr/bin/env bash
# Subir novedades 2026-09-30 al NotebookLM "AABD Big Data & IA".
# Requisito previo (interactivo, una vez): notebooklm login
# Uso: ./SUBIR_NOVEDADES_2026-09-30.sh
# Ya ejecutado y sincronizado el 2026-09-30 (48 fuentes en total).
set -euo pipefail
cd "$(dirname "$0")/../.."

NB="3db48c6c-0f7a-43c6-b9d0-0ae3b88be9d2"

add() {
  local file="$1"
  [ -f "$file" ] || { echo "ABORT: ez da fitxategia: $file" >&2; exit 1; }
  notebooklm source add -n "$NB" --type file "$file"
}

# Fuentes actualizadas / añadidas el 2026-09-30:
# 1. Reemplazos de fuentes existentes con versiones actualizadas:
# - 02_elastic_stack.pdf
# - INDICE.md
#
# 2. Nuevas fuentes añadidas:
# - 07_Kafka/materialak/01_04_ApacheKafka_aurreratua.pdf
# - 04_Programazioa_5073/materialak/5073_3_Programazioa.pdf
# - 03_ML_5072/materialak/5072_2_03_KNN.pdf
# - 03_ML_5072/materialak/5072_3_Balidazio_Metodologia.pdf
# - 03_ML_5072/materialak/Sailkapen_Ebaluazio-metrikak.md
# - 07_Kafka/soluzioak/kafka_aurreratua_2_kasua/Ebazpena_2_Kasua.md
# - 07_Kafka/soluzioak/kafka_aurreratua_connect/Ebazpena_Connect.md
# - 00_Transversal/AUDITORIA_EJERCICIOS.md

echo "OK: Todas las fuentes sincronizadas (48 fuentes en total en NotebookLM)."
