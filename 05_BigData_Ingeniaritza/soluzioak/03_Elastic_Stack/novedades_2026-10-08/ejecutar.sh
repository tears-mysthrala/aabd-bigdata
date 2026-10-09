#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
mkdir -p evidencias
image=docker.elastic.co/logstash/logstash:9.5.4
for practice in p18 p20 p21 p22 p22_invalid; do
  pipeline="$practice"
  fixture=web.log
  if [[ "$practice" == p21 ]]; then pipeline=p20; fixture=web_ampliado.log; fi
  if [[ "$practice" == p22 ]]; then fixture=web_ampliado.log; fi
  if [[ "$practice" == p22_invalid ]]; then pipeline=p22; fixture=invalid.log; fi
  args=(docker run --pull never -i --network none --memory 1100m --cpus 2
    --label aabd.practice=elastic-20261008
    -e LS_JAVA_OPTS=-Xms256m\ -Xmx512m
    -v "$PWD/pipelines/$pipeline.conf:/usr/share/logstash/pipeline/praktika.conf:ro")
  if [[ "$practice" != p18 ]]; then args+=(-v "$PWD/fixtures/$fixture:/datos/web.log:ro"); fi
  echo "Ejecutando $practice"
  # Se conservan los contenedores finalizados como evidencia; no se usa --rm.
  if [[ "$practice" == p18 ]]; then
    "${args[@]}" "$image" logstash -f /usr/share/logstash/pipeline/praktika.conf --pipeline.workers 1 --pipeline.batch.size 10 --log.level warn < fixtures/p18.log > "evidencias/$practice.stdout.log" 2>&1
  else
    "${args[@]}" "$image" logstash -f /usr/share/logstash/pipeline/praktika.conf --pipeline.workers 1 --pipeline.batch.size 10 --log.level warn < /dev/null > "evidencias/$practice.stdout.log" 2>&1
  fi
done
python3 verificar.py
