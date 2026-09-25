#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$DIR/../06_MariaDB_MongoDB_Laborategia_DF2.2/.env"
[ -f "$ENV_FILE" ] && set -a && . "$ENV_FILE" && set +a

echo "=== Testing Apache NiFi Advanced (Aurreratua) Environment ==="
CURL_TLS=()
if [ -n "${NIFI_CA_CERT:-}" ]; then
    CURL_TLS=(--cacert "$NIFI_CA_CERT")
fi

echo -n "1. Checking Docker containers: "
nifi_name="iabd-nifi"
docker inspect iabd-nifi >/dev/null 2>&1 || nifi_name="nifi"
mongo_name="iabd-mongodb-nifi"
docker inspect iabd-mongodb-nifi >/dev/null 2>&1 || mongo_name="mongodb"
mysql_name="iabd-mysql-nifi"

nifi_status=$(docker inspect -f '{{.State.Status}}' "$nifi_name" 2>/dev/null || echo "not running")
mongo_status=$(docker inspect -f '{{.State.Status}}' "$mongo_name" 2>/dev/null || echo "not running")
mysql_status=$(docker inspect -f '{{.State.Status}}' "$mysql_name" 2>/dev/null || echo "not running")

if [ "$nifi_status" = "running" ] && [ "$mongo_status" = "running" ] && [ "$mysql_status" = "running" ]; then
    echo "OK ($nifi_name, $mongo_name, $mysql_name running)"
else
    echo "FAIL (nifi: $nifi_status, mongodb: $mongo_status, mysql: $mysql_status)"
    exit 1
fi

echo -n "2. Checking NiFi Web UI (https://localhost:8443/nifi/): "
http_code=$(curl --silent --show-error "${CURL_TLS[@]}" -o /dev/null -w "%{http_code}" https://localhost:8443/nifi/)
if [ "$http_code" = "200" ] || [ "$http_code" = "302" ]; then
    echo "OK (HTTP $http_code)"
else
    echo "FAIL (HTTP $http_code)"
    exit 1
fi

echo -n "3. Checking NiFi REST API authentication: "
N_USER="${NIFI_USER:-nifi}"
# Sin contraseña por defecto: NIFI_PASSWORD en entorno/.env (SECURITY.md).
if [ -z "${NIFI_PASSWORD:-}" ]; then
    echo "FAIL (falta NIFI_PASSWORD en entorno)"
    exit 1
fi
export N_USER NIFI_PASSWORD
token=$(python3 -c 'import os, urllib.parse; print(urllib.parse.urlencode({"username": os.environ["N_USER"], "password": os.environ["NIFI_PASSWORD"]}), end="")' |
    curl --fail --silent --show-error "${CURL_TLS[@]}" -X POST https://localhost:8443/nifi-api/access/token \
        -H 'Content-Type: application/x-www-form-urlencoded' --data-binary @-)
if [ -n "$token" ]; then
    echo "OK (Bearer token generated)"
else
    echo "FAIL (Authentication error)"
    exit 1
fi

echo -n "4. Checking MySQL retail_db tables and data: "
M_USER="${MYSQL_USER:-iabd}"
# Sin contraseña por defecto: MYSQL_PASSWORD en entorno/.env (SECURITY.md).
if [ -z "${MYSQL_PASSWORD:-}" ]; then
    echo "FAIL (falta MYSQL_PASSWORD en entorno)"
    exit 1
fi
cust_count=$(printf '%s\n' "$MYSQL_PASSWORD" | docker exec -i "$mysql_name" sh -c 'IFS= read -r MYSQL_PWD; export MYSQL_PWD; exec mysql -u "$1" -e "select count(*) from retail_db.customers;" -s -N' sh "$M_USER" 2>/dev/null || true)
if [ "$cust_count" -gt 0 ] 2>/dev/null; then
    echo "OK (retail_db contains $cust_count customers)"
else
    echo "FAIL (retail_db customers count: $cust_count)"
    exit 1
fi

echo -n "5. Checking MySQL connectivity from inside NiFi: "
if docker exec "$nifi_name" bash -c "timeout 2 bash -c 'cat < /dev/null > /dev/tcp/iabd-mysql-nifi/3306' 2>/dev/null || timeout 2 bash -c 'cat < /dev/null > /dev/tcp/mysql/3306' 2>/dev/null"; then
    echo "OK (mysql:3306 reachable)"
else
    echo "FAIL (Unable to reach mysql:3306)"
    exit 1
fi

echo -n "6. Checking MongoDB connectivity from inside NiFi: "
if docker exec "$nifi_name" bash -c "timeout 2 bash -c 'cat < /dev/null > /dev/tcp/iabd-mongodb-nifi/27017' 2>/dev/null || timeout 2 bash -c 'cat < /dev/null > /dev/tcp/mongodb/27017' 2>/dev/null"; then
    echo "OK (mongodb:27017 reachable)"
else
    echo "FAIL (Unable to reach mongodb:27017)"
    exit 1
fi

echo -n "7. Checking MySQL JDBC Driver inside NiFi: "
if docker exec "$nifi_name" test -f /opt/mysql-connector-j-8.0.31.jar; then
    echo "OK (/opt/mysql-connector-j-8.0.31.jar exists)"
else
    echo "FAIL (JDBC jar missing in container)"
    exit 1
fi

echo -n "8. Checking exercise directories and sample data: "
if [ -d "$DIR/../05_CSV_JSON_ConvertRecord_DF2.1/sarrera" ]; then
    echo "OK (sample input directory present)"
else
    echo "FAIL (Files missing)"
    exit 1
fi

echo ""
echo "=== Basic connectivity and sample-data checks passed; NiFi flows still require runtime validation. ==="
