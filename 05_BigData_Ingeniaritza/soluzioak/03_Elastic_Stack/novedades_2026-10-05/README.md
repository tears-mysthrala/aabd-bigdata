# Elastic P13, P15 (aldaerak), P16 eta P17

Iturria: [PDF eguneratua](../../../materialak/02_elastic_stack.pdf), 75 orri,
2026-10-05ean irakurrita. P13: 51–60; P14: 63; P15: 65–66;
P16: 70; P17: 71–72. P13 zaharra orain P14 da (stdin); P14 zaharra
orain P15 da (Grok). Aurreko ebidentziak bere data eta numerazio historikoa
mantentzen ditu. Gida hau bertsio berriaren arabera dago.

## Prestaketa eta laborategiaren mugak

Linux-en `C:\elastic\ariketak\beats-kasua` karpetaren baliokidea karpeta hau
da. Bash, Python 3 (liburutegi estandarra), curl, Docker eta Compose behar dira.
Ez da pakete Python gehigarririk instalatzen. Irakurri [compose.yaml](compose.yaml)
eta [filebeat.yml](filebeat.yml) abiarazi aurretik.

```bash
cd 05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack/novedades_2026-10-05
free -h
df -h .
docker ps
ss -ltn 'sport = :19200 or sport = :15601 or sport = :18080'
docker compose config --quiet
```

Proiektu propioa: `aabd-elastic-novedades-20261005`. Portuak `127.0.0.1`-en
soilik: ES **19200**, Kibana **15601**, Apache **18080**. PDFan 9200/5601/8080
dira; barneko 9200/5601/80 portuak berdinak dira. Ez da lehengo Compose-a
erabiltzen, ezta beste zerbitzuen datuak/bolumenak ukitzen ere.
Elastic irudiak **9.5.4** dira (lehendik eskuragarri zegoen bertsioa; PDFa
9.1.4), Apache `httpd:2.4` digest zehatzarekin finkatuta (**2.4.69** exekuzioan).
Exekuzio-erregistroak benetako irudien digest-ak
gordetzen ditu. ES heap 512MiB, Kibana 1024MiB; edukiontzien mugak
1100/1500/128/256MiB (ES/Kibana/Apache/Filebeat). Laborategi lokal honen
ES autentifikazioa PDFko moduan dago: isolamendua loopback bidez egiten da.
Ezin da konfigurazio hau zerbitzari publiko batean kopiatu.

RAM gutxirekin exekutatu faseka. `docker compose stop`-ek gure zerbitzuak
gelditzen ditu eta bolumenak mantentzen ditu. Ez erabili `down -v`.

## P13 — Apache → Filebeat → Elasticsearch → Kibana

**Helburua.** Web-eskaera bakoitzaren jatorrizko lerroa Apache-n sortu,
bolumen partekatuan Filebeat-ek irakurri, ES-en biltegiratu eta Discover-en
aztertu. Hemen ez dugu Apache modulurik edo Grok prozesadorerik gehitzen:
log-lerro osoa `message` eremuan dago, enuntziatuak eskatzen duen bezala.

### Abiarazi, eskaerak sortu eta datuak egiaztatu

```bash
docker compose up -d elasticsearch apache filebeat
curl -fsS http://127.0.0.1:19200
curl -fsS http://127.0.0.1:18080
python3 verificar_p13.py
docker compose exec -T apache cat /usr/local/apache2/logs/access_log
docker compose exec -T filebeat cat /var/log/apache/access_log
docker compose logs --tail 50 filebeat
docker compose exec -T filebeat filebeat test output -e --strict.perms=false
curl -fsS 'http://127.0.0.1:19200/_cat/indices?v'
curl -fsS 'http://127.0.0.1:19200/_resolve/index/filebeat*?pretty'
curl -fsS 'http://127.0.0.1:19200/filebeat-*/_search?pretty'
```

`verificar_p13.py`-k **15 eskaera berri** egiten ditu: 8 baliabide zuzenera
(200), 6 `/proba`, `/ikasleak`, `/ez-dago` bideetara (404) eta azken bat
`If-None-Match` goiburuarekin, lehen erantzunaren ETag-a erabiliz (304). Exekuzio bakoitzean marka bakarra
sortzen du; ez du aurreko dokumentuen kopurua egiaztapen berritzat hartzen.
Bi edukiontzietan logaren edukia bera dela frogatzen du eta ES-en 15 lerro
horiek **hitzez hitz** `message` direla egiaztatzen du.
Emaitza: [p13_resultado.json](evidencias/p13_resultado.json); lerro osoak:
[Apache](evidencias/p13_apache_access.log), [Filebeat](evidencias/p13_filebeat_access.log).

Filebeat-en `filestream` sarrera lehenespenez 1024 byteko fingerprint-a
erabiltzen duen bertsioetan fitxategi txikien irakurketa atzeratu daiteke;
15 eskaerek muga hori gainditzen dute. Ikusi [Elastic filestream dokumentazioa](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-filestream).
Ez aldatu fingerprint ezarpenak erregistroa berriro irakurtzera behartu nahian.

Lerro baten interpretazioa (IPa Docker sarearen arabera aldatzen da):

```text
172.x.x.x - - [05/Oct/2026:... +0000] "GET /proba?run=... HTTP/1.1" 404 ...
```

`172.x.x.x`: bezeroaren IPa; `GET`: metodoa; `/proba?...`: baliabidea;
`HTTP/1.1`: protokolo bertsioa; `404`: erantzunaren egoera. `message` ez da
`status_code` eremu egituratu bat: Grok/ingest pipeline/module bat beharko da
eremu bereizietan analizatzeko. `@timestamp` Filebeat-ek sortutako unea da
hemen, ez Apache-ren testuko data automatikoki parseatutako balioa.

### Kibana eta Discover

```bash
docker compose --profile gui up -d kibana
curl -fsS http://127.0.0.1:15601/api/status
```

Ireki `http://127.0.0.1:15601`, joan Discover-era, sortu Data View
`filebeat-*` eta aukeratu `@timestamp`. Denbora-tartea datuen egunera edo
azken orduetara egokitu. Gehitu `message` zutabea eta zabaldu dokumentu bat.
KQL adibideak: `message: "404"`, `message: "200"`, `message: "304"`.
Balio horiek testuaren edozein tokitan ere ager daitezke: zabaldu lerroa eta
ziurtatu kodea komatxo arteko eskaeraren **ondoren** dagoela.
Karpeta honetako [exekuzio-erregistroak](exekuzioa_2026-10-05.md) bereizten ditu
REST eta GUI frogak. Data View-a eta tanda zehatzaren Discover URLa
`python3 preparar_kibana.py` bidez presta daitezke; horrek **ez** du GUI
verifikazioa egiten. Benetako pantailak [evidencias/](evidencias/) karpetan daude.

### Compose-aren sei galderak

1. Lau zerbitzuak: **elasticsearch, kibana, apache, filebeat**.
2. PDFko kanpoko portuak 9200/5601/8080 dira; laborategikoak
   **19200/15601/18080**. Compose sare barruan 9200/5601/80 dira.
3. `apache-logs` bolumenak Apache-k idatzitako logak gordetzen eta
   Filebeat-ekin partekatzen ditu.
4. Eduki bera bi path-etan muntatzen da: Apache-ren berezko
   `/usr/local/apache2/logs` eta Filebeat-en irakurketa-konfigurazioaren
   `/var/log/apache`. Edukiontzi bakoitzak bere fitxategi-sistema dauka.
5. `:ro` = read-only; Filebeat-ek ezin du Apache-ren loga aldatu.
6. Apache-ren `command` blokeak `CustomLog ... common` gehitzen du,
   loga benetako fitxategian idazteko, eta `exec httpd-foreground` bidez
   Apache lehen planora eramaten du. Irudiaren log lehenetsiak terminalera
   joan daitezke; `CustomLog` honek fitxategi partekatua bermatzen du.
   Gure blokeak aurretik existitzen den egiaztatzen du: restart batek ez du
   bigarren direktiba gehitzen eta eskaera beraren loga bikoizten.

### Azken bederatzi galderak

1. Datuen jatorria **Apache-ren HTTP access loga** da, gure eskaerek sortua.
2. **Filebeat-ek lerro berriak irakurri eta ES-era bidaltzen ditu**;
   registry-ak irakurritako posizioa gordetzen du.
3. **Elasticsearch-en Filebeat data stream/indizean** geratzen dira.
4. **Kibana-k kontsultatu eta bistaratu** egiten ditu; ez da logen biltegia.
5. Docker volume-ak **fitxategi bera partekatu eta edukia mantentzeko** balio du.
6. Eskaera bezeroak bidaltzen du (metodoa/bidea/goiburuak);
   erantzuna zerbitzariak itzultzen du (kodea/goiburuak/gorputza).
7. **200**: arrakasta; **304**: baldintzapeko eskaeran baliabidea ez da
   aldatu, bezeroaren cachea erabil daiteke; **404**: baliabidea ez da aurkitu.
8. `elasticsearch:9200` Compose DNSaren zerbitzu-izena da;
   Filebeat barruko `localhost:9200` Filebeat edukiontzia litzateke.
9. **Apache → Filebeat → Elasticsearch → Kibana**.

## P15 — Grok Debugger: bi aldaera berriak

**Helburua.** Bi lehen logetako bost eremuak eta bi formatu berriak atera.
`pipelines/p15.conf`-ek lau lagin onak eta IP okerreko lagina prozesatzen ditu
Logstash errealean. Kibana Grok Debugger-en lagin/patroi bakoitza banaka sartu
eta **Simulate** sakatu; Logstash-ek eta Debugger-ek errore-formatu desberdina
erakusten dute (tag vs errore mezua).

Oinarrizko laginak:

```text
192.168.1.105 GET /api 500 1234
10.0.0.25 POST /login 200 856
^%{IP:bezero_ip} %{WORD:metodoa} %{URIPATH:request} %{NUMBER:status_code} %{NUMBER:bytes}$
```

Erabiltzailea amaieran:

```text
10.0.0.25 POST /login 401 856 erabiltzailea 1
^%{IP:bezero_ip} %{WORD:metodoa} %{URIPATH:request} %{NUMBER:status_code} %{NUMBER:bytes} %{GREEDYDATA:erabiltzailea}$
```

Emaitza: `bezero_ip="10.0.0.25"`, `metodoa="POST"`, `request="/login"`,
`status_code="401"`, `bytes="856"`, **`erabiltzailea="erabiltzailea 1"`**.
`WORD` soilik erabiliz ez genuke azken espazioa eta `1` harrapatuko.

Data aurrizkian:

```text
2026-10-04 10.0.0.25 POST /login 401 856
^(?<data>%{YEAR}-%{MONTHNUM}-%{MONTHDAY}) %{IP:bezero_ip} %{WORD:metodoa} %{URIPATH:request} %{NUMBER:status_code} %{NUMBER:bytes}$
```

Emaitza: aurreko bost eremuak eta **`data="2026-10-04"`**.
Oraindik ez du `@timestamp` aldatzen. Grok-ek egitura harrapatzen du;
Date filter-ak egutegiaren balioa eta denbora interpretatzen ditu.

**Galderak.** Patroiak goian daude. Lehen bi laginetan patroi bera balio du
egitura bera dutelako. Egitura aldatzean patroia egokitu behar da;
`invalid-ip ...` laginak `_grokparsefailure` ematen du Logstash-en.
`^`/`$`-k lerro osoa hartzen dute. `NUMBER`-ek hemen string-ak sortzen ditu,
P17k erakusten du nola zenbaki bihurtu. [Benetako event-ak](evidencias/p15.events.json).

## P16 — Grok + Date

**Helburua.** Logaren `timestamp`, `bezero_ip`, `metodoa`, `request`,
`status_code` atera eta jatorrizko gertaera-unea `@timestamp` bihurtu.
[p16.conf](pipelines/p16.conf)-eko filter osoa:

```logstash
filter {
  grok {
    match => { "message" => "^(?<timestamp>%{MONTHDAY}/%{MONTH}/%{YEAR}:%{TIME}) %{IP:bezero_ip} %{WORD:metodoa} %{URIPATH:request} %{NUMBER:status_code}$" }
  }
  if "_grokparsefailure" not in [tags] {
    date {
      match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss" ]
      locale => "en"
      timezone => "Europe/Madrid"
      target => "@timestamp"
    }
  }
}
```

Sarrera: `30/Sep/2026:10:30:45 192.168.1.105 GET /api 500`.
Irteera: `timestamp="30/Sep/2026:10:30:45"`,
`@timestamp="2026-09-30T08:30:45.000Z"`; IP/metodoa/bidea/kodea
`192.168.1.105/GET//api/"500"`. Irailean Madril UTC+02 da.
PDFak ez du zonarik zehazten: hemen **Europe/Madrid hipotesi esplizitua** da.
Jatorrizko loga UTC balitz `timezone => "UTC"` jarri eta 10:30:45Z espero
beharko litzateke. `locale => "en"`-ek `Sep` hilabetea determinista egiten du.
Ikusi [Date filter dokumentazioa](https://www.elastic.co/docs/reference/logstash/plugins/plugins-filters-date).

**Interpretazioa/galderak.** Date gabe `@timestamp` prozesatze-unea da;
Date-rekin gertaeraren unea, Kibana-ko histograma denboran zuzen kokatzeko.
`31/Sep/2026...` egitura zuzena baina data ezinezkoa da: `_dateparsefailure`.
`BAD DATE ...` egitura okerra: `_grokparsefailure`, Date ez da exekutatzen.
Erroreko event-aren prozesatze-timestamp-a ez da jatorrizko data zuzena dela
frogatzat hartu behar. [Benetako event-ak](evidencias/p16.events.json).

## P17 — Mutate: mota, izena eta eremuak

**Helburua.** **JSON event-a → Logstash (mutate) → terminala**.
[p17.conf](pipelines/p17.conf)-ek `stdin { codec => json }` erabiltzen du.
Eraldaketak:

```logstash
mutate {
  convert => { "status_code" => "integer" "bytes" => "integer" }
  rename => { "request" => "uri" }
  remove_field => [ "message" ]
}
```

Sarrera [p17.jsonl](fixtures/p17.jsonl)-n dago, PDFko JSON bera lerro bakarrean.
Benetako irteeraren negozio-eremuak:

```json
{"bezero_ip":"192.168.1.105","metodoa":"GET","uri":"/api","status_code":500,"bytes":1234}
```

Logstash-ek `@timestamp`, `@version`, host/event metadatuak ere gehitu ditzake;
PDFko objektua event osoaren laburpena da. `status_code` eta `bytes` JSON
zenbakiak dira, komatxorik gabe. `request` eta `message` ez daude;
`uri` dago. Ez da `replace`: `rename`-k izena mugitzen du.
Ikusi [Mutate dokumentazioa](https://www.elastic.co/docs/reference/logstash/plugins/plugins-filters-mutate).
Balio ez numerikoen garbiketa ez du enuntziatu honek definitzen;
`convert` ez da sarrera balidazio osoa. [Benetako event-a](evidencias/p17.events.json).

### P15/P16/P17 exekutatu eta irteerak konparatu

RAM askatzeko lehenik P13ko zerbitzuak gelditu, bolumenak mantenduz:

```bash
docker compose --profile gui stop
./ejecutar_logstash.sh
python3 verificar_logstash.py
```

Scriptak hiru Logstash edukiontzi **sekuentzial** exekutatzen ditu, sarerik
gabe, 512MiB heap eta 1100MiB muga, fitxategi propioak read-only muntatuta.
Edukiontzi geldituak gordetzen dira, ez dira automatikoki ezabatzen.
Terminalaren codec-a `json_lines` da `rubydebug`-ren ordez, benetako motak
assert bidez egiaztatzeko; filter-ak eta stdin fluxua berberak dira.
Interaktiboki PDFko `rubydebug` nahi bada, output-eko codec-a aldatu eta
`docker run -it` erabili, sarrera terminaletik idazteko.

[logstash_verificacion.json](evidencias/logstash_verificacion.json)-ek lau
lagin on, Grok akats bat, data zuzena, data ezinezkoa, egitura akatsa eta
Mutate-ren mota/izena/ezabaketa frogatzen ditu. `*.stdout.log` fitxategiak
programaren irteera osoak dira; `*.events.json` fitxategiak horietatik
ateratako event-ak. Ez dira eskuz asmatu edo ingest simulate bidez ordezkatu.

GUIko snapshot gordeen barne-koherentzia egiaztatzeko:
`python3 verificar_gui_evidencias.py`. Honek dokumentuko `message` eremua eta
Grok-en **Structured Data** JSONak berrirakurtzen ditu; ez du nabigatzailea
berriro exekutatzen. Denbora berrian GUIa egiaztatzeko, goiko Discover eta
Grok urratsak errepikatu behar dira.

La marca `request_batch_id` del JSON de P13 es un UUID público añadido al query string `run` de las peticiones sintéticas. Sirve para aislar una tanda en Discover; no autentica ni autoriza ningún acceso.
