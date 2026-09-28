# Elastic Stack praktikak: ebazpena (P1–P4 + gehigarriak)

Iturria: [`02_elastic_stack.pdf`](../../materialak/02_elastic_stack.pdf)
(43 or., 9.5.4). Exekuzio erreala:
[exekuzioa_2026-09-28.md](exekuzioa_2026-09-28.md). Script berrerabilgarria:
[elastic_praktikak.sh](elastic_praktikak.sh) (`ES=... ./elastic_praktikak.sh`;
assert-ak ditu, `DENAK OK` ematen du). Dev Tools kontsulta bakoitza REST
baliokidearekin egiaztatuta dago (Dev Tools REST bezero bat da).

> **Kibana verificado 2026-09-28** (container efimero, `NODE_OPTIONS=
> --max-old-space-size=1024`): `GET /api/status` → `overall: available`;
> `:9200` JSON (`9.5.4`, `You Know, for Search`) vs Kibana GUI en `:5601`
> (login, Discover, Dashboard, Dev Tools, Stack Management) — ES datu-motora
> da, Kibana bistaratze-geruza. Minimo neurtua: ES heap 512m (~770 MB RSS) +
> Kibana heap 1g (~750 MB RSS). Kibana 512m heap-ekin abortatzen du
> (exit 134, V8), beraz 1g da minimoa 9.5.4-n.

## 1. praktika — ES + Kibana martxan

[`compose.yaml`](compose.yaml) PDFkoaren baliokidea da, bi egokitzapenekin:
portuak `127.0.0.1`-ra atxikita (repoaren SECURITY araua; PDFak `9200:9200`
dakar interfaze guztietan) eta ES heap-a esplizitua (`-Xms1g -Xmx1g`).

```bash
docker compose up -d
curl http://127.0.0.1:9200   # JSON: cluster info
# Nabigatzailean: http://localhost:5601 (Kibana GUI)
```

## 2. praktika — lehen indizea eta dokumentuak

`POST produktuak/_doc` x4 (Dev Tools) — curl baliokideak scriptean.
`GET produktuak/_search` → 4 dokumentu (`_count.count = 4`).

- Zenbat dokumentu? **4.**
- Non daude benetako datuak? **`hits.hits[].​_source`**-n (ez `_id`, `_score`
  edo metadatuetan).
- Zer da `produktuak`? **Indizea** (≈ taula).
- Zer da `{ "izena": …, "prezioa": … }` bakoitza? **Dokumentu JSON bat**
  (≈ errenkada).

## 3. praktika — cluster health eta mapping

- `GET _cluster/health` → **`status: yellow`**, `number_of_nodes: 1`,
  `active_primary_shards: 3`, `active_shards: 3`, `unassigned_shards: 1`.
- `GET _cat/shards/produktuak?v` → `produktuak 0 p STARTED` + `0 r UNASSIGNED`.
- `GET produktuak/_mapping` → `izena: text (+keyword)`, `kategoria: text
  (+keyword)`, `prezioa: float`, `stock: long`.

a. **Egoera yellow, zergatik?** Nodo bakarra (`single-node`): primary-ak
   aktibo baina erreplika ezin esleitu — ez da gorria, datuak eskuragarri.
b. **Erreplika UNASSIGNED, zergatik?** Erreplika shard-ak nodo DESBERDINA
   behar du; bakarrarekin ez dago non kopiatu (Kafka 5. ariketako
   erreplika-arazo bera).
c. **Motak:** `izena/kategoria → text` (kateak), `prezioa → float`
   (hamartarra), `stock → long` (osoa) — mapaketa dinamiko automatikoa.
d. **Zergatik `text` + `keyword`?** Dynamic mapping-ek string bakoitzari bi
   aurpegi ematen dizkio: `text` (tokenizatua, `match` bilaketarako) eta
   `keyword` azpieremua (osorik, `term`/agregazio/ordenarako).

## 4. praktika — Query DSL

| # | Kontsulta | Emaitza behatua |
|---|---|---|
| 1 | `match izena: koaderno` | 2: Koaderno urdina, Koaderno handia (`_score` 0.693 biei — garrantzi bera, biak baldintza bera betetzen) |
| 2 | `range prezioa lte 10` | 2: Koaderno urdina (4.5), Koaderno handia (8.5) |
| 3 | `bool must[match] + filter[range gte 1 lte 10]` | 2: berak (hemen ebakiak ez du ezer kentzen) |
| 5 (erronka) | `range prezioa gte 10 lte 50` | 1: Sagu optikoa (19.99) |

a/b/c goiko taulan. d. **`must`**: bete BEHAR da eta `_score`-an eragiten du
(garrantzia); **`filter`**: bete behar da baina score-a ez du aldatzen,
cacheatzen da — zenbaki/data/balio zehatzetarako (iragazketa).

## Ariketa gehigarriak (26. or.)

| # | Kontsulta | Emaitza behatua |
|---|---|---|
| 1 | `range prezioa gt 20` | 1: Teklatu mekanikoa (59.99) |
| 2 | `match izena: mekanikoa` | 1: Teklatu mekanikoa |
| 3 | `range prezioa gte 5 lte 25` | 2: Koaderno handia (8.5), Sagu optikoa (19.99) |
| 4 | `bool must[match koaderno] + filter[prezioa gt 5]` | 1: Koaderno handia |
| 5 | `term kategoria: Informatika` | **0** — `text` tokenizatuta dago (`informatika` minuskulaz); `Informatika` maiuskulaz ez dator bat |
| 5 | `term kategoria.keyword: Informatika` | **2**: Sagu optikoa, Teklatu mekanikoa — `keyword` osorik gordetzen du jatorrizko balioa |

## Egiaztapen-erregistroa

| Egiaztapena | Egoera |
|---|---|
| P2–P4 + 5 gehigarriak (assert-ekin, `DENAK OK`) | ES 9.5.4 errealean exekutatuta 2026-09-28 |
| Yellow/unassigned, mapping, term-vs-keyword portaera | Irteera erreala transkribatuta |
| Kibana `:5601` | Bigarren exekuzioan egiaztatuta (ikus goiko ohartxo eta erregistroa): `/api/status overall: available`; GUIa nabigatzailean irekitzen da ikaslearen makinarako |
| Beats/Logstash (34–41. or.) | Teoria + grok pipeline azalpena; ez dago eskuzko ariketa zenbakidunik PDFan — ez da lan berririk |
| Kibana Discover/Dashboard/ILM/Alerting (28–33. or.) | Teoria; ez dago urrats exekutagarririk PDFan — ez da lan berririk |
