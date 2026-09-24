# Etikako ariketa osagarriak — erantzun-ereduak

> **Eredu didaktikoa, ez ikasle baten edo talde baten benetako erabakia.** Diapositibetan ageri diren jarduerei erantzuten die. Notebooken emaitza edo puntuaziorik ez da asmatu; norberaren/taldearen hautua egiteko eremuak hutsik uzten dira.

## Materialaren irismena

Erreferentziazko diapositibak `E1-Ereduak-Etika_eta_legea.pdf` dira. Diapositibek 3.1 notebooka ospitaleko fairness metrikei aplikatzeko, 6.1 notebooka ALTAI galdera-zerrendarekin eta protokolo pertsonalarekin, eta 12.0 notebooka SHAP/LIME erabiltzeko aipatzen dituzte. Hiru notebook horiek ez daude checkout-ean; beraz, ezin dira ezkutuko azpiatalak, datuak, rubrika, benetako kalkuluak edo puntuazioak berreraiki. Behekoak ikusgai dagoen diapositiba-aginduari emandako eredu-erantzunak dira. 6.1ek ALTAIren zazpi dimentsioak eta mugikorreko app bat ere aipatzen ditu; ez da 6.1en auditoretza oso gisa aurkezten.

## 02-06 · Ospitaleko fairness metrikak (3.1 aipamena)

**Eredu-kasua eta suposizioak.** Ospitale batek pazientearen datuekin hurrengo 24 orduetan zainketa intentsiboko okertzea aurreikusten du, eta puntuazioak langileei berrikuspen-zerrenda ordenatzen laguntzen die. Puntuazioak ez du berez arreta ukatzen edo ematen. Adibide hau azalpen kualitatiboa da: ez dago benetako datu, talde, neurketa edo Fairlearn exekuziorik.

| Neurria | Zertan jartzen du arreta | Ospitaleko balizko onura | Tentsioa / muga |
|---|---|---|---|
| Demographic parity (hautapen-tasa berdintasuna) | Talde bakoitzean alerta positiboen proportzioa | Alerta-eskuragarritasun desoreka handia agerian utz dezake | Gaixotasunaren oinarri-tasa desberdina bada, alarma faltsu gehiago sor ditzake eta arrisku klinikoa behar bezala ordenatzea kaltetu |
| Equal opportunity (benetako positiboen tasa berdina) | Benetan okertzen diren pazienteen artean, talde bakoitzean zenbat hautematen diren | Talde bateko gaixo larriak gutxiago galtzeko egokia izan daiteke | Taldeen artean faltsu positiboen tasa ez da nahitaez berdina; positiboen etiketen fidagarritasuna eta lagin-tamaina behar dira |
| Equalized odds | Benetako positiboen eta faltsu positiboen tasak taldeetan antzekoak izatea | Kalte klinikoaren bi aldeak aztertzen ditu: huts egindako alerta eta alarma alferrikakoa | Neurri hau eta kalibrazioa edo beste fairness-definizio batzuk ez dira beti batera lor daitezkeen baldintzak; aukeraketa ezin da estatistikatik bakarrik atera |
| Kalibrazioa | Puntuazio bereko arrisku aurreikuspenak talde guztietan antzeko maiztasunez egia izatea | Puntuazio klinikoaren interpretazioa taldeetan egonkorra izatea lagun dezake | Kalibrazio onak ez du berez talde arteko errore-tasak berdintzen edo banakako tratu bidezkoa bermatzen |

**Adibideko talde-argudioa (ez da gelako taldearen erabakia):** «Lehenetsi dezagun equal opportunity lehen ebaluazioan: egoera larrian dauden pazienteak talde jakin batean sistematikoki gutxiago ez hautematea segurtasun klinikoko arrisku handia litzateke. Aldi berean, equalized odds eta kalibrazioa ere argitaratu, lagin-tamaina eta ziurgabetasun-tarteekin; tasa bakar bat ez da bidezko arreta osoaren ordezkoa. Medikuak puntuazioa berrikusi behar du eta sistemak ez du arreta automatizoki ukatuko». Aukera kliniko eta etikoa da, ez arauak agindutako metrika unibertsala. **Gelako benetako hautua:** ____________________.

**Ebidentzia-muga:** diapositibak soilik ospitale-kasua eta Fairlearn aipatzen ditu; 3.1 notebookik gabe ez dago ereduaren emaitza edo metriken balio zehatzik egiaztatzerik.

Metriken definizio teknikoak Fairlearnen ebaluazio-gidan azaltzen dira: [Common fairness metrics](https://fairlearn.org/main/user_guide/assessment/common_fairness_metrics.html). Definizio horiek ez dute beraiek erabakitzen zein den klinikoki edo etikoki egokiena.

## 02-07 · Hiruko taldean fairness metrika bat defendatzea

Diapositibaren ariketa-agindua: hiruko talde bakoitzak fairness metrika bat defendatu. Goiko kasurako, taldeko kide batek equal opportunity defendatzeko argudio-eredua eman dezake: okertze larriak saihesteko, benetan arriskuan dauden pazienteen positiboen detekzioa azpitaldeen artean alderatzea lehenesten du. Argudioak onartu behar du faltsu positiboak eta kalibrazioa bereiz aztertu behar direla, eta ordezko babes-neurriak behar direla.

| Taldekideak / rola | Aukeratutako metrika | Argudioa eta aitortutako kostua |
|---|---|---|
| 1 | __________________ | ______________________________ |
| 2 | __________________ | ______________________________ |
| 3 | __________________ | ______________________________ |
| Taldearen ondorioa | __________________ | Zer beste neurri/berrikuspen erabiliko dugu? __________________ |

Ezintasun-teorema aipatzeak ez du esan nahi edozein datu-kasutan fairness neurri guztiak batera ezinezkoak direnik; zer definizio eta baldintza zehatz aplikatzen diren aztertu behar da. Hautua taldeak egin behar du.

## 02-08 · GDPRren 22. artikulua: erabaki-fluxu eredua

**Erabaki-zuhaitza kasu bati aplikatzeko:**

1. **Datu pertsonalen tratamendua dago?** Ez bada, 22. artikulua ez da bide honetatik aplikatzen; beste arau batzuk aplika daitezke. Bai bada, jarraitu.
2. **Norbanako bati buruzko erabakia da?** Profilatzea erabil daiteke, baina profilatzea bakarrik ez da nahikoa 22. artikulua pizteko.
3. **Erabakia tratamendu automatizatuan soilik oinarritzen da, gizakiaren esku-hartze esanguratsurik gabe?** Giza ukitu hutsak ez du “soil-soilik automatikoa” izaera kentzen: berrikusleak informazioa ulertu, zalantzan jarri eta emaitza aldatzeko benetako ahalmena behar du.
4. **Erabakiak ondorio juridikoak ditu edo antzera nabarmen eragiten dio pertsonari?** Lau baldintzak betetzen badira, 22(1) artikuluko eskubidea aktibatzen da: pertsonak eskubidea du halako erabakirik ez jasotzeko.
5. **Badago 22(2) artikuluko salbuespen zehatz bat?** (a) kontratua egiteko/betearazteko beharrezkoa izatea; (b) EBko edo estatu kideko legeak baimentzea eta babes-neurri egokiak ezartzea; edo (c) berariazko baimena. Salbuespena ez da baimen orokor bat: kasuaren lege-baldintzak frogatu behar dira.
6. **Babes-neurriak eta datu berezien baldintzak aztertu.** (a) edo (c) salbuespenetan, gutxienez giza esku-hartzea lortzeko, norberaren ikuspegia azaltzeko eta erabakia aurkaratzeko bidea bermatu behar da (22(3)). 22(4) artikuluak 9(1)eko datu-kategoria berezien erabilera mugatzen du, 9(2)(a) edo (g) oinarria eta babes egokiak behar direla ezarriz.
7. **Informazioa eta aplikagarri diren beste betebeharrak.** 13(2)(f), 14(2)(g) eta 15(1)(h) artikuluek 22(1)/(4) kasuetan erabaki automatikoaren existentziari, erabilitako logikari buruzko informazio esanguratsuari, eta garrantzi/ondorio aurreikusei buruzko informazioa aurreikusten dute. Hau ez da automatikoki iturburu-kode osoa emateko eskubide gisa ulertu behar; azalpena kasurako esanguratsua eta ulergarria izan behar da.

**Kasu-eredua:** ikasleen nota edo eskubide garrantzitsua algoritmoak bakarrik erabakitzen badu eta ondorio nabarmena badu, 22. artikuluaren azterketa sakona egin. Irakasle batek benetan aztertzen badu ebidentzia eta erabakia alda badezake, 22(1)eko “soilik automatikoa” baldintza ez da automatikoki betetzen; hala ere, GDPRko gardentasun, zehaztasun, legezko oinarri eta datuak babesteko beste betebeharrak indarrean jarraitzen dute. Kasu zehatza datu-fluxu eta erabakitzeko boterearen arabera baloratu behar da.

**Iturri juridikoak egiaztatuta: 2026-09-24.** RGPDren testu ofizialak 22. artikuluaren baldintzak eta salbuespenak ezartzen ditu [EUR-Lex, 2016/679 Erregelamendua](https://eur-lex.europa.eu/eli/reg/2016/679). EDPB/WP29 jarraibideek erabaki automatizatuaren eta profilatzearen azalpena ematen dute [EDPB, Automated decision-making and profiling (WP251 rev.01)](https://www.edpb.europa.eu/documents/guideline/automated-decision-making-and-profiling_en). AEPDren eskubide-orriak esparru bera herritarrei azaltzen die [AEPD, Derecho a no ser objeto de decisiones individuales automatizadas](https://www.aepd.es/derechos-y-deberes/conoce-tus-derechos/derecho-no-ser-objeto-de-decisiones-individuales). C-203/22 auzian, EBko Justizia Auzitegiak “logikari buruzko informazio esanguratsua” erabakiak sortzeko prozedura eta erabilitako printzipioei buruzko azalpen ulergarri gisa interpretatu zuen [EUR-Lex, C-203/22, 2025eko otsailaren 27ko epaia](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62022CJ0203).

## 02-09 · SHAP/LIME eta azalgarritasuna (12.0 aipamena)

12.0 compliance notebookaren kodea eta datuak falta dira; beraz, atal honek ez du azalpen grafikorik, SHAP balio kalkulaturik edo benetako eredu-emaitzarik aurkezten.

- **SHAP**: ezaugarri bakoitzari aurreikuspen batean duen ekarpena esleitzeko azalpen-metodoa; joko-teoriako Shapley balioekin lotuta dago. Ekarpena eredua eta atzeko planoko banaketa zehaztuta interpretatzen da, ez kausa-efektu gisa.
- **LIME**: kasu jakin baten inguruan sarrerak perturbatu eta eredu konplexuaren portaera hurbiltzen duen tokiko eredu sinple bat doitzen du. Hurbilketa tokikoa da, eta perturbazioen diseinuarekiko sentikorra izan daiteke.
- **Adibide kontzeptuala, ez exekuzio erreala:** ikasle-laguntza eredua hipotetikoki hiru sarrerarekin aurreikusten ari dela suposatuz, azalpenak “azken hilabeteko atzerapenak puntuazioa gora eraman du; aurreko probako puntuazioak behera” deskriba lezake. Ez dago horrelako emaitzarik notebookean egiaztatuta, eta azalpenak ez du frogatzen sarrera batek kausatu duenik edo eredua zuzena/bidezkoa denik.

Ikaslearen konparazio-erregistroa (benetako notebooka eskuratzen denean bete): eredua ___; banako kasua ___; SHAP behaketa ___; LIME behaketa ___; azalpenen adostasuna/desadostasuna ___; azalpenaren muga ___; auditoria independentea ___ .

## 02-10 · Ikasle-proiektu baterako EIA mini eredua

**Suposizioa:** ikastetxe bateko ikasle-proiektu batek irakasleari ikasketa-laguntza behar izan dezaketen ikasleak antzematen laguntzen dio. Benetako sistema edo daturik ez da aztertu. Behekoa arrisku-ebaluazio pedagogikoa da, **ez** arauzko DPIA bat, auditoretza edo betetze-adierazpena.

| Eremua | Ereduko erantzuna |
|---|---|
| Helburua eta onura | Laguntza-eskaera garaiz eztabaidatzeko seinale bat eman; ikasleari zigorrik edo automatikoki bazterketarik ez eragin. Alternatiba: irakaslearen behaketa eta ikaslearen/ familiaren eskaera. |
| Ukituak eta boterea | Ikasleak (adingabeak barne), familiak, irakasleak eta laguntza-langileak; erakundea erabaki-prozesuaren arduraduna da. Botere-asimetria handia da; ikaslea ez da presiopean “borondatez” datuak ematera behartu behar. |
| Datuak eta kalitatea | Hasierako diseinuan behar-beharrezko ikaskuntza-seinaleak baino ez; osasun, etnia edo familia-egoerari buruzko datu sentikorrik ez bildu beharrezko oinarri eta babesik gabe. Datuen jatorria, okerrak, hutsuneak eta ordezko proxyak egiaztatu. |
| Kalte posibleak | Faltsu negatiboek laguntza atzeratzea; faltsu positiboek estigma; aurreko desberdintasunak birsortzea; datu-ihesa; ikasleak “arrisku” etiketa barneratzea; irakasleak puntuazioan gehiegi fidatzea. |
| Neurketa eta parte-hartzea | Errore motak eta laguntza-eskuragarritasuna taldeka aztertu; lagin txikien ziurgabetasuna erakutsi; ikasle/familia/irakasleen iritzia bildu, eta kexa edo zuzenketa-bidea eskaini. Ez asmatu emaitzarik, aurretik ez badago daturik. |
| Babesak | Erabakiaren aurretik adituak kasua berrikusi; arrazoia azaldu; erabakiaren aurkako bidea; datu-minimizazioa, sarbide mugatua, atxikipen-epea, segurtasun-probak, aldizkako diskriminazio/kalitate egiaztapena, eta erabakia geldiarazteko irizpidea. |
| Hondar-arriskua eta erabakia | Hondar-arriskua ertaina edo handia izan daiteke adingabeen profilatzea eta etiketatzea badago. **Ereduko gomendioa: aldatu eta pilotu mugatu ezarri**, informazio osagarri eta benetako parte-hartzaileekin berrikusi arte; kaltearen kontrolik edo azalpen/errekurtso biderik ez badago, ez hedatu. |

Legezko oharra: benetako erakundeak tratamenduaren helburua, oinarri juridikoa, GDPR 35. artikuluaren DPIA-beharra eta kasuko AI Act sailkapena banan-banan aztertu behar ditu. EIA mini hau ez da horien ordezkoa; “ethical recommendation” gisa markatutako kontrolak gomendio dira eta ez dira denak arau-testuaren agindu literalak.

## 02-11 · Tailerreko kalitate-kameraren aurkako eraso fisikoa

**Diapositibako galdera:** tailerreko kalitate-kamera adversarial eraso fisiko batez engaina ote liteke? **Ereduzko erantzuna:** bai, posible da; benetako kameraren edo ereduaren probak ez dira egin. Argiztapenak, ikuspegiak, gainazaleko eredu errepikakorrek edo objektuan erantsitako markek sailkatzailearen sarrera alda dezakete, pertsona batek begi hutsez akats txikia ikusi arren.

**Defentsa eta erantzuna:** ereduaren erabilera-mugak eta inpaktuak zehaztu; kalitate kritikoa ezin utzi sailkatzaile bakarraren esku; kamera/argiztapen/angelu aldaketekin ebaluazio adversarial baimendua egin; anomalia eta konfiantza baxuko sarrerak baztertu edo eskuz berrikustera bidali; bi ikuspegi edo neurketa independente erabili; giza ikuskatzaileari gelditzeko ahalmena eman; eredu/datu/firmware aldaketak kontrolatu eta log-ak gorde; emaitza okerren inguruko berrikuspen-prozesua eduki. Sareko segmentazioa eta sarbide kontrola ere aplikatu. Erantzun hau defentsa- eta arrisku-kudeaketa mailakoa da; ez du eraso-prozedurarik ematen.

Etika/praktika ona: langileen segurtasuna eta kalitatearen eragina lehenetsi; probaren baimena eta hedadura dokumentatu; ez erabili produkzio-piezak edo langile-irudiak beharrezkoa ez bada. Baldintza juridiko zehatzak sistemaren testuinguruaren araberakoak dira; diapositibak ez du arau aplikagarririk zehazten.

## 02-12 · Hiru helburu, tentsio bakarra: talde-argudio adibidea

51. diapositibako hiru erpinak **zehaztasuna**, **sendotasuna (robustness)** eta **pribatutasuna** dira. Gelako taldeak kasu berean helburu bat defendatu behar du. Adibide honek **pribatutasuna** hautatzen du eta ez du taldearen benetako hautua ordezkatzen:

> «Kalitate-kamerako eredua garatzean pribatutasuna lehenetsiko dugu: ez ditugu aurpegiak edo langile-identifikatzaileak bilduko akatsen sailkapenerako beharrezkoak ez badira; irudiak makinaren eremura mugatu, atxikipena laburtu eta sarbidea mugatuko dugu. Baliteke datu gutxiagorekin zehaztasuna apur bat jaistea eta zenbait eraso fisikoren aurrean robustotasuna galtzea; hori neurtu, irudi sintetiko/anomalia tekniko baimenduekin estresatu eta zalantzazko piezak gizakiari bidaliko dizkiogu. Ez dugu segurtasun-maila edo kalitate-kontrola promesaz ordezkatuko».

Hiru helburuen arteko puntua diseinu-erabakia da: diapositibak ere ez duela segurtasun perfekturik, datu maximoekin eta erabateko gardentasunarekin batera, esaten du. Benetako talde-aukera: ____________________; erabilitako kasua: ____________________; argudioa: ____________________.

## 02-13 · Protokolo pertsonala (6.1 aipamena)

6.1 notebookaren jarraibide osoa ez dago eskuragarri. Diapositibak AI literacy eta protokolo pertsonala diseinatzea soilik adierazten du. Ondoko orri betegarria norberak bere erabilerarako osatzekoa da; ez da ikaslearen balio edo ohitura errealen ordezko.

| Nire araua | Nik beteko dudan konpromisoa |
|---|---|
| Helburua | AA erabiliko dut __________________ lanerako; ez dut erabiliko __________________ erabaki garrantzitsurako giza berrikuspenik gabe. |
| Datu pertsonalak | Tresna publikoetan ez dut sartuko __________________. Zalantzan, baimena/baimentasuna egiaztatuko dut __________________. |
| Egiaztapena | Egitateak egiaztatuko ditut __________________ iturrirekin; kodea/ kalkuluak probatuko ditut __________________. |
| Gardentasuna | AAren laguntza aitortuko dut __________________ arauen arabera, eta nire ekarpena bereiziko dut. |
| Inpartzialtasuna eta errespetua | Talde edo pertsona bati buruzko irteera berrikusiko dut __________________ ikuspegitik, eta estereotipoa edo kaltea ikusiz gero __________________. |
| Segurtasuna | Sarrera susmagarri edo fidagabe batek sistema-arauak aldatzeko eskatzen badu, __________________ egingo dut. |
| Ingurumen/erabilera neurritsua | Modelo astuna erabiliko dut soilik __________________; aukerarik txikiena/egokiena hautatuko dut __________________. |
| Berrikuspena | Protokolo hau berrikusiko dut data honetan: __________; tutorea/arduraduna (aukerakoa): __________. |

### Iturri eta muga-oharrak

- **GDPRren 22., 13., 14., 15. eta 9. artikuluak:** [EUR-Lex, Erregelamendua (EB) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679), kontsulta-data: **2026-09-24**.
- **Automatizatutako banakako erabakiak eta profilatzea:** [EDPB, WP29 Guidelines WP251 rev.01](https://www.edpb.europa.eu/documents/guideline/automated-decision-making-and-profiling_en), eta [AEPDren herritarrentzako azalpena](https://www.aepd.es/derechos-y-deberes/conoce-tus-derechos/derecho-no-ser-objeto-de-decisiones-individuales).
- **Azalpen esanguratsuaren interpretazioa:** [EBJA, C-203/22 (Dun & Bradstreet Austria), CK v Magistrat der Stadt Wien, ECLI:EU:C:2025:117](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62022CJ0203), 2025-02-27.
- **SHAP metodoaren jatorrizko lana:** Lundberg eta Lee, *A Unified Approach to Interpreting Model Predictions* (2017), [arXiv:1705.07874](https://arxiv.org/abs/1705.07874). **LIME metodoaren jatorrizko lana:** Ribeiro, Singh eta Guestrin (2016), [arXiv:1602.04938](https://arxiv.org/abs/1602.04938). Erreferentziak metodoak azaltzeko dira; ez dira falta diren 12.0 ariketaren ordezko.
- Kontsulta-data adierazi den arren, proiektu erreal batean araudiaren aplikazioa eta azken bertsioak berriro egiaztatu behar dira. Dokumentu honek ez du banakako aholkularitza juridikorik ematen.
