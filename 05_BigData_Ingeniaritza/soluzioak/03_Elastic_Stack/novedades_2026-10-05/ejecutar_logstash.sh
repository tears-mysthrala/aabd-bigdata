#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
mkdir -p evidencias
for practice in p15 p16 p17; do
  fixture="fixtures/$practice.txt"
  if [[ "$practice" == p17 ]]; then fixture="fixtures/p17.jsonl"; fi
  docker run -i --name "aabd-elastic-novedades-20261005-$practice-$(date +%s)" \
    --label com.docker.compose.project=aabd-elastic-novedades-20261005 \
    --network none --memory 1100m --cpus 2 \
    -e LS_JAVA_OPTS='-Xms256m -Xmx512m' \
    -v "$PWD/pipelines/$practice.conf:/usr/share/logstash/pipeline/praktika.conf:ro" \
    docker.elastic.co/logstash/logstash:9.5.4 \
    logstash -f /usr/share/logstash/pipeline/praktika.conf \
      --pipeline.workers 1 --pipeline.batch.size 10 --log.level warn \
    < "$fixture" > "evidencias/$practice.stdout.log" 2>&1
done
python3 verificar_logstash.py
