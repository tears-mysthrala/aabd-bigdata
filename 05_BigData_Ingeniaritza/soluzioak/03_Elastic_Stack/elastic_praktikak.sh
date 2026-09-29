#!/usr/bin/env bash
# Elastic Stack 1–4 praktikak + ariketa gehigarriak (curl bidez).
# Kibana Dev Tools kontsulta bakoitzaren REST baliokidea da.
# Erabilera: ES=http://127.0.0.1:9200 ./elastic_praktikak.sh
# Berrerabilgarria: hasieran `produktuak` indizea ezabatzen du (ez badago,
# errorea ezabatzen da), beraz bigarren exekuzioak ez ditu dokumentuak bikoizten.
set -euo pipefail
ES="${ES:-http://127.0.0.1:9200}"

echo "== ES prest egon arte itxaron (gehienez ~2 min) =="
for _ in $(seq 1 24); do
  if curl -fsS --max-time 5 "$ES" > /dev/null 2>&1; then echo "ES prest"; break; fi
  sleep 5
done
curl -fsS --max-time 10 "$ES" > /dev/null # huts egiten badu, hemen gelditu

q() { # q <izena> <metodo> <path> [body] — curl -f: HTTP erroreak ezkutatu gabe
  local name="$1" method="$2" path="$3" body="${4:-}"
  if [ -n "$body" ]; then
    curl -fsS -X "$method" "$ES$path" -H 'Content-Type: application/json' -d "$body"
  else
    curl -fsS -X "$method" "$ES$path"
  fi
  echo
}

check() { # check <hits-espero> <json>
  local expected="$1" json="$2"
  local hits
  hits=$(echo "$json" | python3 -c "import json,sys; print(json.load(sys.stdin)['hits']['total']['value'])")
  if [ "$hits" != "$expected" ]; then
    echo "FAIL: $expected hits espero, $hits jaso" >&2
    exit 1
  fi
  echo "OK ($hits hits)"
}

echo "== 2. praktika: indizea garbitu + 4 dokumentu =="
# Segurtasuna: DELETE suntsitzailea loopback-ean bakarrik, bestela BERREZARRI=1 eskatu.
case "$ES" in
  *127.0.0.1*|*localhost*) ;;
  *) if [ "${BERREZARRI:-0}" != "1" ]; then
       echo "ABORT: $ES ez da loopback — ez dut produktuak ezabatuko. BERREZARRI=1 ezarri laborategi botagarria dela berresteko." >&2
       exit 1
     fi ;;
esac
curl -fsS -X DELETE "$ES/produktuak" > /dev/null 2>&1 || true # ez badago, berdin
q p2-1 POST /produktuak/_doc '{"izena":"Koaderno urdina","kategoria":"Papergintza","prezioa":4.50,"stock":25}' > /dev/null
q p2-2 POST /produktuak/_doc '{"izena":"Koaderno handia","kategoria":"Papergintza","prezioa":8.50,"stock":10}' > /dev/null
q p2-3 POST /produktuak/_doc '{"izena":"Sagu optikoa","kategoria":"Informatika","prezioa":19.99,"stock":15}' > /dev/null
q p2-4 POST /produktuak/_doc '{"izena":"Teklatu mekanikoa","kategoria":"Informatika","prezioa":59.99,"stock":5}' > /dev/null
q refresh POST /produktuak/_refresh > /dev/null
echo "== count =="; q count GET /produktuak/_count

echo "== 3. praktika: health / shards / mapping =="
q health GET /_cluster/health
q shards GET /_cat/shards/produktuak?v
q mapping GET /produktuak/_mapping

echo "== 4. praktika =="
r=$(q 4.1 GET /produktuak/_search '{"query":{"match":{"izena":"koaderno"}}}'); echo "$r"; check 2 "$r"
r=$(q 4.2 GET /produktuak/_search '{"query":{"range":{"prezioa":{"lte":10}}}}'); echo "$r"; check 2 "$r"
r=$(q 4.3 GET /produktuak/_search '{"query":{"bool":{"must":[{"match":{"izena":"koaderno"}}],"filter":[{"range":{"prezioa":{"gte":1,"lte":10}}}]}}}'); echo "$r"; check 2 "$r"
r=$(q 4.5 GET /produktuak/_search '{"query":{"range":{"prezioa":{"gte":10,"lte":50}}}}'); echo "$r"; check 1 "$r"

echo "== gehigarriak =="
r=$(q G1 GET /produktuak/_search '{"query":{"range":{"prezioa":{"gt":20}}}}'); check 1 "$r"
r=$(q G2 GET /produktuak/_search '{"query":{"match":{"izena":"mekanikoa"}}}'); check 1 "$r"
r=$(q G3 GET /produktuak/_search '{"query":{"range":{"prezioa":{"gte":5,"lte":25}}}}'); check 2 "$r"
r=$(q G4 GET /produktuak/_search '{"query":{"bool":{"must":[{"match":{"izena":"koaderno"}}],"filter":[{"range":{"prezioa":{"gt":5}}}]}}}'); check 1 "$r"
r=$(q G5a GET /produktuak/_search '{"query":{"term":{"kategoria":"Informatika"}}}'); check 0 "$r"
r=$(q G5b GET /produktuak/_search '{"query":{"term":{"kategoria.keyword":"Informatika"}}}'); check 2 "$r"
echo "DENAK OK"
