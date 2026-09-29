# Elastic exekuzio-erregistroa (2026-09-28)

**Ingurunea:** `docker.elastic.co/elasticsearch/elasticsearch:9.5.4`, container efimero `codex-aabd-elastic-lab`, `discovery.type=single-node`, `xpack.security.enabled=false`, `127.0.0.1:19200:9200`. Dev Tools kontsulta guztiak REST bidez egiaztatuta (script-ak `DENAK OK`).

**Kibana bigarren exekuzioa (egun berean):** container efimeroak
`codex-aabd-es-min` (ES, heap 512m) + `codex-aabd-kibana-min`
(`docker.elastic.co/kibana/kibana:9.5.4`,
`NODE_OPTIONS=--max-old-space-size=1024`, `ELASTICSEARCH_HOSTS` ESren barne
IPra). Behatuta: `GET /api/status` → `overall: available` (ES `:9200` →
`9.5.4`, `You Know, for Search`); RSS neurtua ES ~770 MB + Kibana ~750 MB.
Oharra: Kibana 512m heap-ekin abortatzen du (exit 134, V8 — ez host OOM),
horregatik 1g da minimoa 9.5.4-n; lehen saiakeran ez zen lortu, bigarrenean bai.

## / (1. praktika)
{
  "name" : "f008348b83ee",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "d9u49jgvSJqxYvHKBR1bmw",
  "version" : {
    "number" : "9.5.4",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "9170df19cae1adb107b7b489b4d82dec66d7a337",
    "build_date" : "2026-09-09T22:42:53.976833287Z",
    "build_snapshot" : false,
    "lucene_version" : "10.5.1",
    "minimum_wire_compatibility_version" : "8.19.0",
    "minimum_index_compatibility_version" : "8.0.0"
  },
  "tagline" : "You Know, for Search"
}

## _cluster/health (3. praktika)
{
  "cluster_name" : "docker-cluster",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 3,
  "active_shards" : 3,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 1,
  "unassigned_primary_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 75.0
}
## _cat/shards/produktuak?v
index      shard prirep state      docs store dataset ip         node
produktuak 0     p      STARTED       4 7.4kb   7.4kb 172.17.0.2 f008348b83ee
produktuak 0     r      UNASSIGNED                               

## produktuak/_mapping
{
  "produktuak" : {
    "mappings" : {
      "properties" : {
        "izena" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "kategoria" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "prezioa" : {
          "type" : "float"
        },
        "stock" : {
          "type" : "long"
        }
      }
    }
  }
}
## 4.1 match koaderno (laburpena)
hits: 2
 - Koaderno urdina | score 0.693
 - Koaderno handia | score 0.693
