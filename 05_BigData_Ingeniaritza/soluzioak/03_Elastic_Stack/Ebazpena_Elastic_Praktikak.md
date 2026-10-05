# Elastic Stack praktikak: ebazpena (P1–P17)

Iturria: [`02_elastic_stack.pdf`](../../materialak/02_elastic_stack.pdf)
(75 or., uneko PDFa 2026-10-05ean irakurrita; 2026-10-01ekoak 61 zituen).
Numerazio berria: stdin P13 zaharra → **P14**; Grok P14 zaharra → **P15**.
[Nobedadeen gida eta exekuzioak](novedades_2026-10-05/README.md)
P13 berriaren, P15 aldaeren, P16 Date-ren eta P17 Mutate-ren ebazpen osoa dira.
P1–P4 aurreko exekuzioa:
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
dakar interfaze guztietan) eta heap minimoak esplizituak (ES `-Xms512m -Xmx512m`,
Kibana `NODE_OPTIONS=--max-old-space-size=1024`).

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

P5–P8 eta P15eko Grok oinarria (orduan P14) **Kibana 9.5.4 errealean egiaztatuta, 2026-10-01**:
[exekuzioa_2026-10-01.md](exekuzioa_2026-10-01.md).
[Entregaren gida](dashboards/README.md),
[16 saved object-en esportazioa](dashboards/kibana_praktikak.ndjson),
[GUIaren erregistroa](dashboards/gui_verification.json).
P1–P4ren aurreko emaitzak 2026-09-28ko erregistroan daude.

## 5. praktika — Discover eta KQL

PDF: 35. orria. `produktuak` Data View-ak ez du denbora-eremurik.
Discover-en `izena`, `kategoria`, `prezioa` zutabeak prestatuta daude;
dokumentu guztien bilaketa eta lau KQL bilaketak gordeta daude.
GUIan ireki eta egiaztatu dira, ez soilik REST baliokideak.

| KQL | Discover-en emaitza |
|---|---|
| (hutsik) | 4 dokumentuak |
| `kategoria: "Informatika"` | 2: Sagu optikoa (19.99), Teklatu mekanikoa (59.99) |
| `prezioa > 100` | 0: No results; maximoa 59.99 da |
| `kategoria: "Informatika" AND prezioa < 500` | 2: Sagu optikoa, Teklatu mekanikoa |
| `NOT kategoria: "Papergintza"` | 2: Sagu optikoa, Teklatu mekanikoa |

KQL eta Query DSL: baldintza baliokideekin dokumentu multzo bera lortzen da.
KQL iragazteko hizkuntza da; Kibana-k Query DSL bihurtzen du. DSLk, gainera,
agregazioak eta garrantziaren araberako bilaketak adieraz ditzake.
`kategoria.keyword` erabil daiteke balio oso zehatza iragazteko;
`kategoria` text eremua analizatuta dago.

## 6. praktika — Lens + Dashboard

PDF: 38. orria. **Produktuen Dashboard-a**, bi Lens barra-grafikorekin:

| Kategoria | Produktu kopurua (Count) | Batez besteko prezioa (Average) |
|---|---:|---:|
| Informatika | 2 | 39.99 € |
| Papergintza | 2 | 6.50 € |

Taldekatzea: `kategoria.keyword`; prezioaren metrika: `Average(prezioa)`.
Grafikoko Informatika barran klik egitean `kategoria.keyword: Informatika`
iragazkia sortzen da: beste panelak Informatika soilik erakusten du (39.99 €).
Iragazkia kenduta bi kategoriak berreskuratzen dira. GUIan probatuta.

[Dashboard-a ireki](http://localhost:15601/app/dashboards#/view/aabd-28ab1f59255f6d99).
Grafikoak: [kopuruak](dashboards/irudiak/p6_1.png),
[prezioak](dashboards/irudiak/p6_2.png).

## 7. praktika — Salmenten Dashboard-a

PDF: 39–40. orriak. CSVaren **500 errenkadak** Elasticsearch-eko dokumentu
GUZTIEKIN alderatu dira. `salmentak` Data View-ak `data` date eremua darabil.
Inportazioa API bidez egin da; ez da Data Visualizer-eko upload klik gisa
aurkezten. Emaitza: indizea, eremu zuzenak eta Data View iraunkorra.

**Salmenten Dashboard-a**: bost Lens panel, bi zutabetan; azken panelak
12 produktu guztiak erakusten ditu, barra horizontalekin eta zabalera
osoan produktuen izenak irakurtzeko. Denbora-tartea gordeta dago:
2026-01-01 → 2026-07-01, urtarrila–ekaina barne. `now-15m`-k ez luke
CSV honetako dokumenturik erakutsiko.

| Panela | Taldekatzea | Metrika | Mota |
|---|---|---|---|
| Salmentak kategoriaren arabera | `kategoria.keyword` | Sum(`unitateak`) | Barrak |
| Diru-sarrerak hirika | `hiria.keyword` | Sum(`diru_sarrera`) | Barrak |
| Salmenta-kanalen banaketa | `kanala.keyword` | Count of records | Donut |
| Diru-sarreren bilakaera denboran | `data`, hileko | Sum(`diru_sarrera`) | Lerroa |
| Produktuen batez besteko prezioa | `produktua.keyword`, 12 balio | Average(`prezioa`) | Barrak |

### Azken analisia: bost erantzunak

1. **Osagaiak**: 594 unitate; Periferikoak 566, Sareak 552, Ordenagailuak 547.
2. **Ermua**: 143389.45 €; Eibar 137141.19 €, Gasteiz 128419.96 €,
   Bilbo 102690.59 €, Donostia 75440.31 €.
3. **Web**: 256 eragiketa (51.2%); Denda 244 (48.8%). Hemen salmentak
   eragiketak dira (Count), ez unitateak.
4. **PC mahaigainekoa**: 914.15 € batez beste.
5. **Ermua iragazkiarekin**: 96 eragiketa, 438 unitate, 143389.45 €;
   Web 50 eta Denda 46. Kategoria nagusia **Ordenagailuak** da (155 unitate),
   ondoren Sareak 131, Periferikoak 79, Osagaiak 73. Beraz, orokorrean
   Osagaiak nagusi diren arren, Ermuan Ordenagailuak dira nagusi.
   Diru-sarreren %24.42 sortzen du Ermua-k, eragiketen %19.2rekin:
   eragiketa bakoitzeko sarrera handiagoa du batez besteko orokorrak baino.

Grafikoko Ermua barran klik → `hiria.keyword: Ermua` → gainerako panelak
iragazten dira. Inspector-en Ordenagailuak 155 eta Web/Denda 50/46 egiaztatu
 dira; iragazkia kenduta kanalak 256/244 izatera itzultzen dira.
Kanalaren `kanala.keyword: "Web"` KQL iragazkia ere probatu da (256
eragiketa soilik), baita `kategoria.keyword: "Osagaiak"` ere (594 unitate
soilik). Biak kendu ondoren ikuspegi orokorra berreskuratu da.

| Hilabetea | Diru-sarrerak (€) |
|---|---:|
| 2026-01 | 76823.36 |
| 2026-02 | 93558.29 |
| 2026-03 | 117997.61 |
| 2026-04 | 80261.98 |
| 2026-05 | 125469.61 |
| 2026-06 | 92970.65 |

[Dashboard-a ireki](http://localhost:15601/app/dashboards#/view/aabd-1fab5517b75a73ff).
[Grafikoen PNGak](dashboards/irudiak/), [zenbakiak](dashboards/emaitzak.json).

## 8. praktika — ILM politika eta Index Template-a

PDF: 44. orria. Politika: **web-logs-policy**.

| Fasea | Gutxieneko adina | Ekintzak |
|---|---|---|
| Hot | 0ms | Lehentasuna 100 |
| Warm | 7d | Lehentasuna 50; ILMren migrazio lehenetsia |
| Cold | 30d | Lehentasuna 0; ILMren migrazio lehenetsia |
| Delete | 90d | Indizea ezabatu |

[Politika JSON](dashboards/ilm_policy.json).
**web-logs-template**: `index_patterns: ["web-logs-*"]`,
`index.lifecycle.name: web-logs-policy`, **data stream gabe**.
[Template JSON](dashboards/ilm_template.json).

`POST /_index_template/_simulate_index/web-logs-2026.10.02` bidez politika
berriari automatikoki lotuko zaiola egiaztatu da, indizea sortu gabe.
Kibana-n politika ireki da: Warm 7, Cold 30, Delete 90 eta lotutako template 1.

4. **Ez**, biharko indizeari ez zaio politika eskuz esleitu behar:
   `web-logs-*` eredua betetzen du eta template-ak ezarpena aplikatzen dio.
   Aurretik sortutako indizeei template berriak ez die atzeraeraginez eragiten.
5. **Ez dena Hot**: datu zaharren irakurketa gutxiago da; hardware azkarra eta
   garestia datu berrientzat uzten da, Warm/Cold merkeagoak erabiliz.
6. **Delete gabe**, datuak eta disko-kostua mugagabe haziko lirateke.

Eguneko izena duten indizeentzat ez da rollover ekintzarik gehitu:
PDFak ez du alias/data stream bidezko rolloverrik eskatzen. Adina indizea
sortu denetik neurtzen da. Benetako warm/cold hardware-migrazioa tier horien
nodoen araberakoa da; nodo bakarreko labak ez du hiru hardware-maila frogatzen.
90 eguneko ezabaketa ez da denbora azkartuz exekutatu.

## 9. praktika — Beat egokia aukeratu

| Kasua | Beat | Zergatik |
|---|---|---|
| 1. NGINX access.log (Linux) | Filebeat | Log-fitxategiak biltzeko agente arina |
| 2. CPU/RAM monitorizazioa | Metricbeat | Sistema-metrikak (CPU, memoria, diskoa, sarea) |
| 3. Windows Event Viewer | Winlogbeat | Windows gertaera-erregistroetarako |
| 4. Webgunea erabilgarri (kanpotik) | Heartbeat | Uptime/probe aktiboak (ICMP/TCP/HTTP) |
| 5. Sareko trafikoa | Packetbeat | Pakete-analisia (protokoloak, fluxuak) |
| 6. Segurtasun-auditoretza (Linux) | Auditbeat | Audit framework-eko gertaerak (fitxategi-osotasuna, prozesuak) |

## 10. praktika — ingesta diseinatu (20 web + NGINX + CPU/RAM + uptime)

1. Web zerbitzarietan (logak): **Filebeat** (filestream, `/var/log/nginx/*.log`).
2. CPU/RAM: **Metricbeat** (system modulua).
3. Erabilgarritasuna kanpotik: **Heartbeat** (monitor HTTP monitore-nodo batetik).
4. Helmugak: Beats-ek **Elasticsearch-era zuzenean** edo **Logstash-era**
   (eraldaketa behar bada) bidal dezakete; handik ES-era.

## 11. praktika — filebeat.yml interpretatu

```yaml
filebeat.inputs:
  - type: filestream
    id: nginx-logs
    paths:
      - /var/log/nginx/*.log
output.elasticsearch:
  hosts: ["http://elasticsearch:9200"]
```

1. NGINX web-logak (testu-lerroak). 2. `/var/log/nginx/` karpetatik.
3. `*.log`: extensio hori duten fitxategi guztiak (wildcard).
4. Elasticsearch-era zuzenean (`http://elasticsearch:9200`).
5. Ez — `output.elasticsearch` dago, ez `output.logstash`.

## 12. praktika — output-a Logstash-era aldatu

```yaml
output.logstash:
  hosts: ["logstash:5044"]
```

- Aldatutako zatia: `output.*` blokea (`output.elasticsearch` → `output.logstash`).
- Filebeat-ek EZ ditu datuak zuzenean ES-era bidaltzen; hurrengo osagaia Logstash da (Beats input, 5044 portuan entzuten).

## 13. praktika — Apache + Filebeat kasu praktikoa

PDF eguneratua: 51–60. orriak. Helburua Apache → Filebeat → Elasticsearch →
Kibana fluxua da. [Gida autoazaldua](novedades_2026-10-05/README.md#p13--apache--filebeat--elasticsearch--kibana)
prestaketa, Compose isolatua, 15 HTTP eskaera, log partekatuaren egiaztapena,
REST eta Discover urratsak, emaitzak eta hamabost galderen erantzunak ditu.

## 14. praktika — lehen Logstash pipeline-a (exekutatuta)

```bash
echo "Kaixo Logstash" | docker run --rm -i \
  -e LS_JAVA_OPTS='-Xms256m -Xmx512m' \
  docker.elastic.co/logstash/logstash:9.5.4 \
  -e 'input { stdin { } } output { stdout { codec => rubydebug } }'
```

Behatutako eventua:

```text
{
       "message" => "Kaixo Logstash",
          "host" => { "hostname" => "4abdec77cc50" },
    "@timestamp" => 2026-10-01T06:43:30.502673754Z,
         "event" => { "original" => "Kaixo Logstash" },
      "@version" => "1"
}
```

- Input-a: `stdin` (teklatua). Output-a: `stdout` (`rubydebug`).
- Ez dago filter blokerik: ez da derrigorrezkoa; eraldaketarik gabe pasatzen da.
- `message` = `Kaixo Logstash`; `@timestamp` Logstash-ek sartutako uneko ordua.

## 15. praktika — Grok Debugger

PDF eguneratua: 65–66. orriak (aurreko PDFan 56). **Kibana → Dev Tools → Grok Debugger → Simulate** bidez
bi laginak exekutatu eta bost eremuak egiaztatu dira (2026-10-01).

```text
^%{IP:bezero_ip} %{WORD:metodoa} %{URIPATH:request} %{NUMBER:status_code} %{NUMBER:bytes}$
```

| Lagina | bezero_ip | metodoa | request | status_code | bytes |
|---|---|---|---|---|---|
| `192.168.1.105 GET /api 500 1234` | 192.168.1.105 | GET | /api | "500" | "1234" |
| `10.0.0.25 POST /login 200 856` | 10.0.0.25 | POST | /login | "200" | "856" |

1. Goiko patroia: `^` eta `$` aingurek lerro osoa egiaztatzen dute.
2. Bai, patroi bera balio du: IP + metodoa + bidea + bi zenbaki egitura bera.
3. Egitura aldatuta, patroia egokitu behar da. Bigarren laginari `EXTRA`
   gehituta, GUIak **Provided Grok patterns do not match data in the input**
   eman du. Grok Debugger-en hau da errorea; Logstash grok filter-ean
   `_grokparsefailure` etiketa gehitzen da lehenespenez.

Motak: NUMBER-ek hemen kateak sortzen ditu. Zenbakizko motak nahi badira,
`%{NUMBER:status_code:int}` eta `%{NUMBER:bytes:int}` erabil daitezke.

2026-10-05eko bi aldaera berriak (erabiltzailea amaieran eta data hasieran)
[nobedadeen gidan](novedades_2026-10-05/README.md#p15--grok-debugger-bi-aldaera-berriak)
daude: patroi osoak, lau lagin on, IP okerreko kontrola eta Logstash benetako
irteerak. Erabiltzailea `erabiltzailea 1` osoa da; data `2026-10-04`.

## 16. praktika — Grok + Date

PDF: 70. orria. [Ebazpena eta pipeline osoa](novedades_2026-10-05/README.md#p16--grok--date).
Grok-ek bost eremuak ateratzen ditu; Date-k `dd/MMM/yyyy:HH:mm:ss`, `locale=en`
eta `timezone=Europe/Madrid` erabiliz gertaeraren data `@timestamp` bihurtzen du.
Zona PDFan zehaztu gabe dago eta hipotesia dokumentatuta dago.

## 17. praktika — Mutate

PDF: 71–72. orriak. [Ebazpena eta JSON pipeline-a](novedades_2026-10-05/README.md#p17--mutate-mota-izena-eta-eremuak).
`status_code` eta `bytes` integer bihurtu, `request` → `uri` berrizendatu eta
`message` ezabatu. Verifikadoreak Logstash benetako irteeraren motak eta
eremuen presentzia/ausentzia egiaztatzen ditu.
