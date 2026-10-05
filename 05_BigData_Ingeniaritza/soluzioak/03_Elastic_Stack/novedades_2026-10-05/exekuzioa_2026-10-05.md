# Exekuzio erreala — 2026-10-05

Laborategia: `aabd-elastic-novedades-20261005`, soilik loopback,
ES19200/Kibana15601/Apache18080. Hasierako behaketa: Docker edukiontzi aktiborik
ez, 1.9GiB memoria erabilgarri, 11GiB swap libre, 45GiB disko libre; hiru
portuak libre. Ez dira lehengo zerbitzuak, datuak edo bolumenak ukitu.
Faseka exekutatu da, heap/edukiontzi mugak Compose-an esplizituak direla.
[Bertsioak eta irudien digest-ak](evidencias/laboratorio_versiones.json):
Elastic9.5.4, Apache2.4.69, Compose5.6.0; PDFko Elastic9.1.4-ren ordez9.5.4
erabili da. Apache irudia probatutako digest-arekin finkatuta dago.

## Aginduak eta frogatutako emaitzak

Karpeta honetatik:

```bash
docker compose config --quiet
docker compose up -d elasticsearch apache filebeat
python3 verificar_p13.py
docker compose exec -T filebeat filebeat test output -e --strict.perms=false
docker compose --profile gui up -d kibana
python3 preparar_kibana.py
docker compose --profile gui stop
./ejecutar_logstash.sh
```

| Egiaztapena | Benetako emaitza | Ebidentzia |
|---|---|---|
| Compose | `config --quiet`: exit0; laborategi propioa osorik sortu | [compose.yaml](compose.yaml), [bertsioak](evidencias/laboratorio_versiones.json) |
| P13 HTTP+Filebeat+ES | 2026-10-05 08:11:55UTC: **15 dokumentu berri;200×8,404×6,304×1**. Apache/Filebeat fitxategiak berdinak eta ES `message`-ak lerro originalen kopia zehatzak | [p13_resultado.json](evidencias/p13_resultado.json), bi `access.log` |
| Filebeat output | `dns lookup...OK`, `dial up...OK`, `talk to server...OK`, `version:9.5.4` | [filebeat_test_output.txt](evidencias/filebeat_test_output.txt) |
| ES destino | `filebeat-9.5.4` data stream-a; backing index `.ds-filebeat-9.5.4-2026.10.05-000001`, denbora-eremua `@timestamp` | [filebeat_resolve.json](evidencias/filebeat_resolve.json) |
| Kibana readiness+Data View | `overall.level=available`; `filebeat-*`, `@timestamp`, id=`aabd-novedades-filebeat` | [kibana_status.json](evidencias/kibana_status.json), [kibana_data_view.json](evidencias/kibana_data_view.json) |
| P13 Discover GUI | Tanda bakarraren KQLarekin **Documents(15)**; `message` zutabean200/304/404 kodeak ikusita | [snapshot](evidencias/p13_discover_snapshot.txt), [pantaila](evidencias/p13_discover.png) |
| P13 dokumentu zabaldua | Document elkarrizketan `Text message` eremua: jatorrizko `GET /?... HTTP/1.1` lerroa eta304 kodea | [snapshot](evidencias/p13_documento_message_snapshot.txt), [pantaila](evidencias/p13_documento_message.png) |
| P15 Grok Debugger GUI | Simulate: `erabiltzailea="erabiltzailea 1"`; beste aldaeran `data="2026-10-04"`; bakoitzean sei eremu zuzen | [usuario snapshot](evidencias/p15_usuario_grok_snapshot.txt), [fecha snapshot](evidencias/p15_fecha_grok_snapshot.txt), PNGak karpeta berean |
| P15 Logstash | Lau lagin onetako bost/sei eremuak; IP okerrekoa `_grokparsefailure` | [p15.events.json](evidencias/p15.events.json) |
| P16 Logstash | `30/Sep/2026:10:30:45` → **2026-09-30T08:30:45.000Z**; `31/Sep` → `_dateparsefailure`; egitura okerra → `_grokparsefailure` | [p16.events.json](evidencias/p16.events.json) |
| P17 Logstash | `status_code=500` eta `bytes=1234` **integer**; `uri=/api`; `request`/`message` ez daude; IP eta metodoa mantenduta | [p17.events.json](evidencias/p17.events.json) |
| Logstash verifikadorea | Lehen exekuzioa08:26:50UTC; ondoren gordetako irteerak reverifikatu dira, exit0; event kopuruak P15=5,P16=3,P17=1; mota/izena/ezabaketa eta kontrol negatiboak OK | [logstash_verificacion.json](evidencias/logstash_verificacion.json) |
| GUI ebidentzien verifikadorea | `python3 verificar_gui_evidencias.py`: exit0; Discover15, hiru kodeak, dokumentuaren message eta Grok Structured Data JSON zehatzak | [gui_verificacion.json](evidencias/gui_verificacion.json) |
| Apache restart | CustomLog bloke idempotentearekin restart erreala: fitxategiko direktiba kopurua **1**, ez2 | [apache_customlog_restart.txt](evidencias/apache_customlog_restart.txt) |

GUIa benetan ireki da agent-browser bidez, `aabd-elastic-novedades-20261005`
saio propioan eta `/tmp/aabd-elastic-novedades-browser-profile` profil bereizian.
Ez da Moodle-ren saioa edo erabiltzailearen nabigatzailea erabili.
Logstash probak **stdin→filter→stdout**, benetako prozesuak dira, `--network none`
eta edukiontzi sekuentzialak erabiliz. JSON output codec-ak mota zehatzak
egiaztatzea ahalbidetzen du; ez da ingest simulation baten ordezkapena.

Lau Python scriptak `ruff format` bidez formateatu dira. Ondoren
`ruff check .`, `ruff format --check .`, `python3 -m py_compile ...` eta
`bash -n ejecutar_logstash.sh` gainditu dira. Formateatze ondorengo
`verificar_logstash.py` eta `verificar_gui_evidencias.py` exekuzioak
**gordetako stdout/snapshot-en reverifikazioak** dira, ez zerbitzuen proba berriak:
[Logstash](evidencias/reverificacion_logstash_guardado.txt),
[GUI](evidencias/reverificacion_gui_guardado.txt). Apache-ren azken restart
aldiz benetako zerbitzu-zikloa izan da, ES/Kibana geldituta zeudela.

## Exekuzioan aurkitutako xehetasunak

Lehen HTTP tandak `If-Modified-Since` etorkizuneko datarekin ez zuen304
sortu (15 eskaera:200×9,404×6). Ez da tanda hori gainditutako egiaztapen
bezala aurkeztu. Scriptak lehen200 erantzunaren **ETag erreala** berrerabiltzen
du `If-None-Match`-en; bigarren tanda zuzena da eta bere marka bakarraren
arabera zenbatzen da. Lehen tandako datuak ez dira ezabatu; horregatik
data stream osoak15 baino dokumentu gehiago ditu. `p13_resultado.json`-eko
markak eta [Discover URLak](evidencias/discover_url.txt) tanda zuzena isolatzen dute.

Chromium automatizazioaren hasierako komando batek profil-konfigurazio
esplizitua behar izan zuen (Wayland saiorik ez); komando guztiek gero
konfigurazio propioa eta headless modua erabili dute. Grok-en Simulate
botoia hasierako leihoaren azpitik zegoen; leihoa1280×1200era egokitu eta
**Structured Data** emaitza egiaztatu da. Azken PNGek emaitza zuzena dute.

Kibana-ko Fleet/AI/workflows plugin batzuek abisu/errore osagarriak eman
dituzte autentifikaziorik gabeko laborategian; irteera laburra
[kibana_logs.txt](evidencias/kibana_logs.txt)-en mantendu da. Readiness,
Discover eta Grok emaitzak bereizita egiaztatu dira; ez da plugin guztien
funtzionamendua aldarrikatzen.

## Interpretazioa eta mugak

- P13ko `message` testu gordina da; ez da Apache module-a erabili eta ez da
  `status_code` eremu egituratuaren ingestarik frogatzen.
- P16ko timezone **Europe/Madrid hipotesia** da, PDFak ez baitu zehazten.
  UTC izango balitz, emaitza10:30:45Z izango litzateke; gida bi aukerak argitzen du.
- P17k `message` goiko eremua kentzen du. ECSko `event.original` metadatuak
  JSON originala mantentzen du; ez da jatorrizko datuen ezabaketa osoa.
- Heap minimoak eta swapak laborategia moteldu dute. Honek funtzionaltasuna
  frogatzen du, ez ekoizpeneko gaitasuna edo errendimendu-helburua.
- Ez da Windows/PowerShell aginduen exekuzioa, Moodle entregarik edo
  argitalpen/commit/push egoerarik frogatzen. Gida Linux/Bash baliokidea da.
- Amaieran gure zerbitzuak soilik `stop` bidez gelditzen dira; hiru bolumenak
  eta Logstash edukiontzi geldituak mantentzen dira. Ez da `down -v` exekutatu.
  [Amaierako egoera](evidencias/estado_final.txt) bereizita dago.
