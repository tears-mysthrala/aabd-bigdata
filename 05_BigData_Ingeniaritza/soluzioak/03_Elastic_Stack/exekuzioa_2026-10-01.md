# Kibana: exekuzio eta egiaztapen erreala — 2026-10-01

Iturria: `05_BigData_Ingeniaritza/materialak/02_elastic_stack.pdf`, 61 orrialde.
P5: 35; P6: 38; P7: 39–40; P8: 44; P14: 56.
Aurreko dokumentazioak PDF zaharraren 43 orrialdeak erabiltzen zituen.
`06_NiFi/materialak/02_elastic_stack.pdf` ere kontrastatu da: testuko aldeak
P12/Beats inguruan daude; Kibana P5–P8/P14 enuntziatuak berdinak dira.
Ez dira entrega bikoitzak sortu.

## Ingurunea

Aurretik martxan zeuden labeko contenedoreak berrerabili dira:
`codex-aabd-es-gui` (`127.0.0.1:19200`) eta `codex-aabd-kibana-gui`
(`127.0.0.1:15601`), biak 9.5.4. ES root endpoint-ak 9.5.4 eman du;
Kibana `/api/status`-ek `status.overall.level: available` eman du.
Kibana-ren package.json ere 9.5.4 da. Ez da stack-a berrabiarazi.

## Egiaztapenak

| Praktika | Egiaztatutako emaitza |
|---|---|
| P5 | Data View denbora-eremurik gabe; 3 zutabeak; bilaketa guztiak Discover GUIan: 4 guztira, lau KQLekin 2/0/2/2 |
| P6 | Bi Lens panelen Inspector: 2/2 produktu, 39.99/6.50 €; Informatika barran klik eginda beste panela iragazten da; iragazkia kenduta biak berriz |
| P7 datuak | 500 dokumentuen `_source` guztiak CSVko 500 errenkadekin alderatuta; `data` mapping date da |
| P7 panelak | Bost Lens: sum unitateak, sum diru_sarrera, count kanala donut, hileko sum diru_sarrera lerroa, 12 produktuen average prezioa barrak |
| P7 interaktibitatea | Ermua barran klik → hiria.keyword iragazkia → kategoriak 155/131/79/73, kanalak 50/46; kenduta kanalak 256/244. Web KQL → 256 soilik; Osagaiak KQL → 594 soilik |
| P8 | Politika 0ms/7d/30d/90d, web-logs-template, data stream gabe; `_simulate_index/web-logs-2026.10.02` → index.lifecycle.name web-logs-policy |
| P8 GUI | Politika editorean Warm 7, Cold 30, Delete 90 eta lotutako template 1; irakurketa ondoren Cancel/Leave page, aldaketarik gorde gabe |
| P14 | Grok Debugger Simulate, bi logetako bost eremuak; EXTRA gehitzeak Provided Grok patterns do not match data in the input errorea |
| Errepikapena | Script-ak hainbat aldiz exekutatuta, 4/500 dokumentu mantenduta, ids egonkorrekin |
| Esportazio/importazioa | 16 objektu: 7 Lens, 2 dashboards, 5 search, 2 index-pattern; `aabd-egiaztapena` espazioan azken esportazioa importatuta: successCount 16, success true, warnings [] |
| Sintaxia | Bi Python script-en py_compile eta shell wrapper-aren bash -n, exit 0 |

Exekutatutako komando nagusia:

```bash
ES=http://127.0.0.1:19200 KB=http://127.0.0.1:15601 \
  bash 05_BigData_Ingeniaritza/soluzioak/03_Elastic_Stack/elastic_praktika_5_8.sh
```

Azken irteera: `P5–P8: objetos, dataset completo e ILM/template verificados`.
[GUIaren erregistroa](dashboards/gui_verification.json),
[azken importazioaren erantzuna](dashboards/import_verification.json),
[entregaren gida](dashboards/README.md).

## Zuzendutako akatsak

- REST agregazioak soilik edukitzea ez zen Discover/Lens/dashboard entrega.
- Lens datasource `formBased` da bertsio honetan, ez `indexpattern`.
- Lens batez bestekoa `average` da, ez Elasticsearch-en `avg`;
  okerreko izenak GUIan panel hutsak/TypeError sortzen zituen.
- Count-ek `sourceField: ___records___` behar du; falta zenean
  `aggValueCount requires the field argument` agertzen zen.
- Donut-a `lnsPie` da, ez `lnsXY`-ko `seriesType: pie`.
- Denbora-tartea urtarrila–ekaina 2026 da, ez azken 15 minutuak.
- 12 produktuak erakutsi behar dira; aurreko Top 10-ak bi ezkutatzen zituen.
- P7ren 5. analisi-galdera Ermua-ren zenbakiekin erantzun da.
- P8ren izen zehatzak, template-a eta automatikoki esleitzeko azalpena falta ziren.
  Eguneko indizeek ez dute PDFan rolloverrik eskatzen.
- Script berriak ez du indizerik edo objektu globalik ezabatzen.

## Ebidentziaren mugak

CSV inportazioa API bidez egin da; ez dira Data Visualizer-en upload klikak
exekutatu. Saved Objects-ek ez dituzte ES dokumentuak edo ILM konfigurazioa
esportatzen; horiek scriptak eta JSONek erreproduzitzen dituzte.

Browser egiaztapenak T3 Code preview bidez egin dira. Snapshot tresnak huts
 egin du; ez dago orri osoko screenshotik. Zazpi PNGak Kibana-ren benetako
canvas-etatik esportatutako grafikoak dira. Klik interaktiboetarako
preview_evaluate bidez MouseEvent-ak sintetizatu dira; emaitza Inspector-en
eta sortutako iragazkietan egiaztatu da.

ILMren konfigurazioa eta template-aren aplikazioa frogatu dira. Ez da 90
 eguneko denbora igaro, ez dira logak ezabatu, eta nodo bakarreko labak ez du
warm/cold hardware desberdinen arteko migrazioa frogatzen.
P1–P4ren exekuzio historikoa ez da oraingo exekuzio berri gisa aurkeztu.
