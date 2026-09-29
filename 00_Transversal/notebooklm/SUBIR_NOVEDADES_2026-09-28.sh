#!/usr/bin/env bash
# Subir novedades 2026-09-28 al NotebookLM "AABD Big Data & IA".
# Requisito previo (interactivo, una vez):  notebooklm login
# Uso: ./SUBIR_NOVEDADES_2026-09-28.sh
# Berrerabilgarria: replace() lehengo bertsioa ordezkatzen du (0/1 bat-etortze
# onartzen du; 2+ anbiguotasunean gelditzen da, eskuz konpontzeko).
# Ya ejecutado el 2026-09-28 (verificado con `notebooklm ask` + citas).
set -euo pipefail
cd "$(dirname "$0")/../.."

NB="3db48c6c-0f7a-43c6-b9d0-0ae3b88be9d2"

replace() { # replace <titulo-exacto> <fitxategia>
  local title="$1" file="$2"
  [ -f "$file" ] || { echo "ABORT: ez da fitxategia: $file" >&2; exit 1; }
  local out
  if out=$(echo y | notebooklm source delete-by-title -n "$NB" "$title" 2>&1); then
    echo "ezabatuta: $title"
  elif echo "$out" | grep -qiE 'no source found|not found|no .* match|0 sources'; then
    echo "ez zegoen: $title"
  else
    echo "$out" >&2 # anbiguotasuna edo bestelako errorea: gelditu, ez igo
    exit 1
  fi
  notebooklm source add -n "$NB" --type file "$file"
}

replace 'Ebazpena_Elastic_Praktikak.md' 05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack/Ebazpena_Elastic_Praktikak.md
replace 'ariketa_kontsola_5_11_erreplika_gako_taldeak_offset.md' 07_Kafka/soluzioak/ariketa_kontsola_5_11_erreplika_gako_taldeak_offset.md
replace 'egiaztapena_2026-09-28.md' 04_Programazioa_5073/soluzioak/egiaztapena_2026-09-28.md
replace 'etikako_ariketa_osagarriak.md' 02_AA_Ereduak_5071/soluzioak/etikako_ariketa_osagarriak.md
replace 'INDICE.md' INDICE.md
replace '01_03_ApacheKafka.pdf' 07_Kafka/materialak/01_03_ApacheKafka.pdf
replace '02_elastic_stack.pdf' 05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf

echo "OK: 7 fuentes enviadas. Revisa duplicados con: notebooklm source list"
