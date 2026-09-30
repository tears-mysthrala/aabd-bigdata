#!/usr/bin/env bash
# broker-N.properties sortu txantiloitik (compose-ak fitxategi konkretuak behar ditu).
# Erabilera: ./sortu_broker_config.sh   (broker-1/2/3.properties sortzen ditu)
set -euo pipefail
cd "$(dirname "$0")"
for i in 1 2 3; do
  sed -e "s/^broker.id=N$/broker.id=$i/" \
      -e "s/kafkaN/kafka$i/g" \
      -e "s/1909M/1909$((i + 1))/" \
      broker.properties.txantiloia > "broker-$i.properties"
  echo "broker-$i.properties"
done
