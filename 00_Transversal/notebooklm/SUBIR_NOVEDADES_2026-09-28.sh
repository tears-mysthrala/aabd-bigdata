#!/usr/bin/env bash
# Subir novedades 2026-09-28 al NotebookLM "AABD Big Data & IA".
# Requisito previo (interactivo, una vez):  notebooklm login
# Uso: ./SUBIR_NOVEDADES_2026-09-28.sh
# Ya ejecutado el 2026-09-28 (verificado con `notebooklm ask` + citas).
# Nota: el PDF viejo 01_03_ApacheKafka.pdf (fuente 17dcc62d-8348-4cc7-8058-04183654d03c)
# se borró a mano (`source delete -y <id>`) para no duplicar con la versión nueva.
set -euo pipefail
cd "$(dirname "$0")/../.."

NB="3db48c6c-0f7a-43c6-b9d0-0ae3b88be9d2"

add() { notebooklm source add -n "$NB" --type file "$1"; }

# replace <titulo-exacto>: PDF baten bertsio zaharra badago, ezabatu eta
# berria igo (berrerabilgarria: 0 edo 1 bat-etortzean ondo; 2+ bada, eskuz).
replace() { # replace <titulo-exacto> <fitxategia>
  echo y | notebooklm source delete-by-title -n "$NB" "$1" > /dev/null 2>&1 || true
  notebooklm source add -n "$NB" --type file "$2"
}

add 05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack/Ebazpena_Elastic_Praktikak.md
add 07_Kafka/soluzioak/ariketa_kontsola_5_11_erreplika_gako_taldeak_offset.md
add 04_Programazioa_5073/soluzioak/egiaztapena_2026-09-28.md
add 02_AA_Ereduak_5071/soluzioak/etikako_ariketa_osagarriak.md
add INDICE.md
replace '01_03_ApacheKafka.pdf' 07_Kafka/materialak/01_03_ApacheKafka.pdf
replace '02_elastic_stack.pdf' 05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf

echo "OK: 7 fuentes enviadas. Revisa duplicados con: notebooklm source list"
