#!/usr/bin/env bash
# Connect properties konkretuak sortu ingurune-aldagaietatik
# (${} ez da properties barruan hedatzen — pauso hau beharrezkoa da).
# Erabilera:
#   BOOTSTRAP=... PLUGIN_PATH=... MYSQL_JDBC_URL=... MYSQL_USER=... \
#   MYSQL_PASSWORD=... MONGO_URI=... ./sortu_connect_config.sh
set -euo pipefail
cd "$(dirname "$0")"
: "${BOOTSTRAP:?BOOTSTRAP falta}"; : "${PLUGIN_PATH:?PLUGIN_PATH falta}"
: "${MYSQL_JDBC_URL:?MYSQL_JDBC_URL falta}"; : "${MYSQL_USER:?MYSQL_USER falta}"
: "${MYSQL_PASSWORD:?MYSQL_PASSWORD falta}"; : "${MONGO_URI:?MONGO_URI falta}"
mkdir -p generated
sed -e "s|\${BOOTSTRAP}|$BOOTSTRAP|" -e "s|\${PLUGIN_PATH}|$PLUGIN_PATH|" \
  connect-standalone.properties > generated/connect-standalone.properties
sed -e "s|\${MYSQL_JDBC_URL}|$MYSQL_JDBC_URL|" -e "s|\${MYSQL_USER}|$MYSQL_USER|" \
    -e "s|\${MYSQL_PASSWORD}|$MYSQL_PASSWORD|" \
  mysql-source.properties > generated/mysql-source.properties
sed -e "s|\${MONGO_URI}|$MONGO_URI|" \
  mongo-sink.properties > generated/mongo-sink.properties
echo "generated/: connect-standalone, mysql-source, mongo-sink (.properties)"
