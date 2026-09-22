#!/usr/bin/env bash
# Re-despliegue controlado del laboratorio NiFi + MySQL + MongoDB.
# El frontal nginx vive en infra/ (arrancarlo primero).
# Uso:
#   ./redeploy.sh          # build + up + espera a healthy + estado
#   ./redeploy.sh --clean  # además borra volúmenes (DATOS: reimporta create_db.sql)
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f .env ]]; then
  echo "No hay .env -> copio .env.example. Edítalo con tus claves y reejecuta." >&2
  cp .env.example .env
  exit 1
fi

# shellcheck disable=SC1091
set -a; source .env; set +a

if [[ "${1:-}" == "--clean" ]]; then
  echo "ATENCIÓN: --clean borra mysql-data, mongo-data y estado NiFi." >&2
  read -r -p "Escribe SI para continuar: " ok
  [[ "$ok" == "SI" ]] || { echo "Cancelado."; exit 0; }
  docker compose down -v
fi

docker compose build
docker compose up -d

echo "--- esperando servicios healthy (máx ~6 min por NiFi) ---"
declare -A cont=( [mysql]=iabd-mysql-nifi [mongodb]=iabd-mongodb-nifi [nifi]=iabd-nifi )
for svc in mysql mongodb nifi; do
  for _ in $(seq 1 72); do
    st=$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}sin-health{{end}}' "${cont[$svc]}" 2>/dev/null || echo "?")
    [[ "$st" == "healthy" ]] && { echo "$svc: healthy"; break; }
    sleep 5
  done
done

docker compose ps
echo "NiFi (vía nginx de infra): https://nifi.bigdata.local/nifi  (usuario: ${NIFI_USER:-nifi})"
echo "NiFi directo (reserva): https://127.0.0.1:${NIFI_HTTPS_PORT:-8443}/nifi"
echo "MySQL: 127.0.0.1:${MYSQL_PORT:-3306}/${MYSQL_DATABASE:-retail_db} (usuario: ${MYSQL_USER:-iabd})"
echo "Mongo: 127.0.0.1:${MONGO_PORT:-27017}"
echo "NOTA: nifi.bigdata.local requiere '127.0.0.1 nifi.bigdata.local' en /etc/hosts (una vez, con sudo)."
