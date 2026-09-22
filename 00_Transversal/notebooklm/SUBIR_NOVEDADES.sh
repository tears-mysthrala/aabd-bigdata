#!/usr/bin/env bash
# Subir novedades 2026-09-22 al NotebookLM "AABD Big Data & IA".
# Requisito previo (interactivo, una vez):  notebooklm login
# Uso: ./SUBIR_NOVEDADES.sh
set -euo pipefail
cd "$(dirname "$0")/../.."

NB="3db48c6c-0f7a-43c6-b9d0-0ae3b88be9d2"

add() { notebooklm source add -n "$NB" --type file "$1"; }

add 03_ML_5072/soluzioak/5072_ML_praktika.py
add 03_ML_5072/soluzioak/README.md
add 07_Kafka/soluzioak/README.md
add 07_Kafka/soluzioak/kafka_producer.py
add 07_Kafka/soluzioak/kafka_consumer.py
add 06_NiFi/soluzioak/07_AEMET_Datu_Lakua_Medallion_DF2.3/README.md
add 04_Programazioa_5073/git_ariketa_4_2/PR_DESC.md
add 04_Programazioa_5073/data/README_10M.md
add 01_Erronka1_CNC_Guard/proyecto_cnc_guard/CNC_Guard.py
add INDICE.md

echo "OK: 8 fuentes enviadas. Revisa duplicados con: notebooklm source list"
