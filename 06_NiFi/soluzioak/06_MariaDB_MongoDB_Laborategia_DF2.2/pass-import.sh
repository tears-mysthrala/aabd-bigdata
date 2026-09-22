#!/usr/bin/env bash
# Guarda las credenciales del lab en Proton Pass. Nada se muestra por pantalla.
# Requisito previo (una vez): pass-cli login
# Uso: ./pass-import.sh [--vault NOMBRE]   (defecto: clase)
set -euo pipefail
cd "$(dirname "$0")"

VAULT="clase"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --vault|-v)
      VAULT="$2"
      shift 2
      ;;
    *)
      VAULT="$1"
      shift
      ;;
  esac
done

[[ -f .env ]] || { echo "No hay .env" >&2; exit 1; }
command -v pass-cli >/dev/null || { echo "falta pass-cli en PATH" >&2; exit 1; }
pass-cli vault list >/dev/null 2>&1 || { echo "Haz primero: pass-cli login" >&2; exit 1; }

# shellcheck disable=SC1091
set -a; source .env; set +a

pass-cli vault create --name "$VAULT" >/dev/null 2>&1 || true

put_login() { # titulo usuario clave [url1] [url2]
  local t="$1" u="$2" p="$3"
  shift 3
  local existing_id
  existing_id=$(pass-cli item list --vault-name "$VAULT" 2>/dev/null | grep -F "]: $t (" | head -n1 | sed -E 's/^- \[([^]]+)\].*/\1/' || true)

  if [[ -n "$existing_id" ]]; then
    pass-cli item update --vault-name "$VAULT" --item-id "$existing_id" \
      --field "username=$u" --field "password=$p" >/dev/null 2>&1
    echo "actualizado: $t"
  else
    local args=(item create login --vault-name "$VAULT" --title "$t" --username "$u" --password "$p")
    for u_arg in "$@"; do
      [[ -n "$u_arg" ]] && args+=(--url "$u_arg")
    done
    pass-cli "${args[@]}" >/dev/null 2>&1
    echo "creado: $t"
  fi
}

put_note() { # titulo contenido
  local t="$1" c="$2"
  local existing_id
  existing_id=$(pass-cli item list --vault-name "$VAULT" 2>/dev/null | grep -F "]: $t (" | head -n1 | sed -E 's/^- \[([^]]+)\].*/\1/' || true)

  if [[ -n "$existing_id" ]]; then
    pass-cli item update --vault-name "$VAULT" --item-id "$existing_id" \
      --field "note=$c" >/dev/null 2>&1 || true
    echo "actualizado: $t"
  else
    local args=(item create note --vault-name "$VAULT" --title "$t" --note "$c")
    pass-cli "${args[@]}" >/dev/null 2>&1
    echo "creado: $t"
  fi
}

put_login "NiFi (nifi.bigdata.local)" "${NIFI_USER:-nifi}" "$NIFI_PASSWORD" "https://nifi.bigdata.local/nifi" "https://localhost:8443/nifi"
put_login "MySQL retail_db (lab)" "${MYSQL_USER:-iabd}" "$MYSQL_PASSWORD" "localhost:3306"
put_login "MySQL root (lab)" "root" "$MYSQL_ROOT_PASSWORD" "localhost:3306"

if [[ -n "${NIFI_SENSITIVE_PROPS_KEY:-}" ]]; then
  put_note "NiFi Sensitive Props Key (lab)" "$NIFI_SENSITIVE_PROPS_KEY"
fi

echo "OK en vault '$VAULT'. Comprueba con: pass-cli item list --vault-name '$VAULT'"
