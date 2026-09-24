10. ATALA

Adimen Artifizialaren Marko Legala

# GDPR + AI Act marko legala

## 10.1 0. Sarrera: Zergatik du garrantzia legeak lan-munduan?

OHARRA

Aurreko moduluetan jada ikusi duzu

- NLP-an: US v. Heppner kasua (2026), Shadow AI eta API+DPA arkitekturak.
- Ikusmen artifiziala-n: aurpegi-aitortza eta GDPR 9. art. (datu biometriko sentibera), Mercadona kasua (2,5 M€-ko isuna).
- Robotika-n: ISO 10218 eta ISO/TS 15066 (segurtasun fisikoa).

Modulu honetan, GDPR oinarrizko 7 printzipioak, 22. artikulua (erabaki automatizatuak) eta EU AI Act-en arrisku-sailkapen osoa sakonki landuko dituzu.

Imajina ezazu egoera hau: informatika-teknikari gisa lan egiten duzu enpresa batean eta zure nagusiak esaten dizu AA sistema bat instalatu behar duzula langile-aukeraketa automatizatzeko. Edo administrazioko teknikari gisa, udaletxe batean lan egiten duzu eta AA tresna bat erabiltzen ari zara herritarren prestazioak kudeatzeko. Edo osasun-teknikari bat zara eta pazienteen datuak AA sistema batek tratatzen ditu.

Kasu guztietan galdera bera dago: lege-betebeharrak betetzen al dira?

Europako Batasunak (EB) arau-multzo bat garatu du erantzuna ematen duena. Hiru arau dira nagusiak:

1. Irudia: Europako AA Marko Legalaren Hiru Zutabeak — GDPR, Azalpenaren Eskubidea eta EU AI Act

Hiru arau hauek ez dira independienteak: elkarren osagarri dira. GDPR-k esaten du: "datu pertsonalak nola tratatu". AI Act-ek esaten du: "AA sistemak nola diseinatu eta erabili". Azkenik, azalpenaren eskubideak lotzen ditu biak: "pertsonek azalpen bat jasotzeko eskubidea dute".

### ZER IKASIKO DUZU MODULU HONETAN

OHARRA

Sarrerako ariketa. Hartu hiru minutu eta zerrendatu paperean 3 AA tresna azken astean erabili dituzunak (ChatGPT, Gemini, Copilot, Spotify gomendioak, Instagram-eko aurpegi-iragazkiak…). Zenbat aldiz galdetu zenuen "non doaz nire datuak?" edo "ari naiz adostasuna ematen?".

Konparatu ondokoarekin: zenbat zerbitzuren adostasun-laukitxoetan sartu zara begiratu gabe? Hori da legeak konpondu nahi duen arazoaren oinarria.

### 1.1. ZER DA GDPR?

GDPR siglak General Data Protection Regulation-en laburpena dira. Euskaraz: Datuak Babesteko Erregelamendu Orokorra. EB osoan aplikatzen den legea da, eta edozein enpresa, erakunde edo administrazioari aplikatzen zaio pertsonei buruzko datuak erabiltzen dituztenean.

ADIBIDEA

"Datu pertsonalak" zer dira?

Edozein informazio pertsona bat identifikatzeko balio duena:

- Izena, NAN, helbidea, telefonoa, emaila
- IP helbidea, cookie-ak, kokapena
- Osasun-datuak, biometria (hatz-marka, aurpegia)
- Laneko errendimenduaren datuak
- Sare sozialetako argitalpenak

GDPR aplikatzen zaio edozein motatako pertsonari buruzko datu-tratamenduari, bai paperean bai digitalki. Adimen Artifizialarekin lotura zuzena dauka, AAk datu-kopuru izugarriak tratatzen dituelako.

### 1.2. GDPR-REN PRINTZIPIO NAGUSIAK (SINPLEKI AZALDUTA)

ADIBIDEA

Curriculum-ak FP zentroan.

FP zentro batek enpresentzako lan-bitartekari lana egiten du. Ikasleen curriculum-ak ditu. GDPR-ren arabera:

- Ikasleei esan behar die curriculum-ak zertarako erabiliko diren
- Ikasleek baimena eman behar dute
- Zenbat denboran gordeko diren zehaztu behar da
- Datu-ihesa gertatuz gero, 72 ordutan jakinarazi behar da

### 1.3. 22. ARTIKULUA: ERABAKI AUTOMATIZATUEN ARAUDIA

Hau da GDPR-ren artikulurik garrantzitsuena AA-rentzat. Honela dio:

"Pertsonak eskubidea du soilik tratamendu automatizatuan oinarritutako erabaki baten xede ez izateko, baldin eta erabaki horrek ondorio juridikoak sortzen badizkio edo nabarmenki eragiten badio."

Hitz errazagoetan: pertsonak eskubidea du ez egoteko soilik makina batek hartutako erabaki garrantzitsu baten menpe — baina ez da debeku absolutua: salbuespenak daude (adostasun esplizitua, kontratu-betearazpena edo legezko baimena), eta horietan ere giza esku-hartzea bermatu behar da.

2. Irudia: GDPR 22. Artikuluaren Erabaki-Fluxua — noiz aplikatzen den eta zer bermeak dauden

Zer da "erabaki garrantzitsu" bat?

Salbuespenak — Noiz da zilegi erabaki automatizatua?

Erabaki automatizatu bat zilegi da hiru kasutan:

1.  Kontratua betetzeko: adib. sarrera-prezio automatikoa hegazkin-txartelan (yield management)

2.  Legeak baimenduta: adib. zerga-administrazioak iruzur automatikoki detektatzea

3.  Adostasunarekin: pertsonak berariaz onartu badu

Baina salbuespen horiek ez dituzte ezabatzen beste eskubide batzuk:

• Giza esku-hartze bat eskatzeko eskubidea (pertsona batek berrikustea)

• Ikuspegia adierazteko eskubidea

• Erabakia aurkaratzeko eskubidea

ADIBIDEA

Banku bateko kreditu-eskaera.

Mikel-ek 10.000€ko mailegu bat eskatu dio bankuari. AA sistema batek automatikoki "UKATUA" erantzuten du.

GDPR 22. artikuluaren arabera:

- Mikelek eskubidea du giza langile batek kasua berrikusteko eskaera egiteko
- Bankuak azaldu behar dio zergatik ukatu den (zer faktore erabili diren)
- Mikelek bere ikuspegia aurkeztu dezake ("nire diru-sarrerak igoko dira lan-kontratuarekin")

Enpresak ezin du esan: "algoritmoak erabaki du eta kitto"

### 1.4. GARDENTASUN-BETEBEHARRAK (12-15 ART.)

AA sistema batek pertsonei buruzko datuak tratatzen dituenean, informazioa eman behar da aldez aurretik:

• Zer datu bildu: zergatik eta zenbat denboran

• Erabaki automatizatuen existentzia: "AA sistema batek hartuko du erabakiaren parte"

• Logikari buruzko informazioa: nola funtzionatzen duen azalpen bat

• Eskubideak: nola eskatu informazioa, nola aurkaratu

ADIBIDEA

Lan-elkarrizketa bideokonferentzia bidez.

Enpresa batek AA sistema bat erabiltzen du lan-elkarrizketak analizatzeko (hizketa, jarrera, hitzen erabilera). GDPR-ren arabera:

- Aldez aurretik esan behar zaio hautagaiari AA sistema bat erabiliko dela
- Azaldu behar zaio zer analizatzen duen sistemak
- Hautagaiak aukera du bere eskubideak baliatzen

ARIKETA 1.1   ·   30 min  taldeka (3 ikasle)

Egoera. FP-ko ikastetxe bat ikasleen errendimendua aurresateko algoritmo bat ezartzea pentsatzen ari da. Algoritmoak ondoko datuak erabiliko lituzke: aurreko notak, asistentzia, jaiotze-data, herritartasuna, gurasoen lan-egoera, zenbat aldiz ikasi duen liburutegian.

Eginkizuna. GDPR-aren 7 printzipioak banaka aplikatu kasuari:

1.  Legezkotasuna: zer oinarri legal egoki da (adostasuna, kontratua, lege-eskakizuna, intereseko zilegitasuna)?

2.  Helburua: helburua zein da, eta nola justifikatu?

3.  Minimizazioa: zein datu kendu beharko lirateke zerrendatik?

4.  Zehaztasuna: nola eguneratuko dira datuak?

5.  Muga-denbora: zenbat denboran gorde behar dira?

6.  Segurtasuna: zer neurri tekniko hartuko zenituzke?

7.  Erantzukizuna: nork frogatuko du araudia betetzen dela?

Eztabaidatzeko. Sistema hau legezkoa al da, nahiz eta printzipio guztiak bete? Zer bestelako arazo etiko ikusten dituzu?

### 2.1. KONTZEPTUA: HIRU OSAGAIAK

Imajina ezazu makina batek esaten dizula: "Ezin duzu etxea alokatu", "Ukatuta duzu master horretara sartzea" edo "Lanetik bota zaitugu". Zergatik? Ez badakizu zergatik hartu den erabakia, ezin duzu ezer egin. Hori da azalpenaren eskubidearen oinarria: jakin behar duzu zergatik.

Azalpenaren eskubideak hiru osagai ditu elkarren osagarri:

Lege-testu askotan ez da modu horretan agertzen, baina ondorengo arau-multzoek batera sortzen dute:

### 2.2. ARAZO TEKNIKOA: AA ASKOK EZIN DUTE AZALPENIK EMAN

Hemen dago arazoa: AA sistema moderno askok oso emaitza onak ematen dituzte, baina inork ere ez daki zehatki zergatik. Honi deitzen zaio "kutxa beltza" arazoa (black box problem).

Adibide sinple batekin:

Erabaki-zuhaitz sinplea (azalgarria):
   ┌─ Diru-sarrerak > 2.000€/hil?
   │   ├─ BAI → ┌─ Zorra < 30%? → BAI: ONARTUA
   │   │         └─ EZ: UKATUA
   │   └─ EZ: UKATUA

Sare neuronal sakona (azalkaitza):
   [Sarrera: 500 datu] → [1.000 neurona] → [500 neurona]
   → [250 neurona] → [UKATUA]
   (Zergatik? Inork ez daki zehatki)

3. Irudia: XAI Metodoen Konparazioa — irismena, zehaztasuna eta konputazio-kostua

Azalpena emateko metodoak

Sistema konplexuetan azalpen bat emateko hainbat metodo daude. FP mailan hauek ezagutzea nahikoa da:

ADIBIDEA

Kontrafaktuala eguneroko bizitzan.

AA sistemak esaten dizu: "Zure sarrera akademikoa UKATUA da."

Kontrafaktual azalpena: "Bataz besteko nota 6,5 bada, onartua izango zinateke. Zure nota 5,8 da."

Hau lagungarriagoa da "sistema honek zure profila ez du aukeratzen" baino.

### 2.3. GDPR VS AI ACT: AZALPENAREN ESKUBIDEAREN BILAKAERA

4. Irudia: Azalpen-eskubidearen bilakaera 2018tik 2026ra — irismenaren zabaltzea eta betebehardunaren aldaketa

GDPR (2018)                         AI Act (2026)
────────────────────────            ────────────────────────
NOR?: Datu-arduraduna               NOR?: Hedatzailea (sistema
      (enpresa/erakundea)                 erabiltzen duena)

NOIZ?: Erabakia SOILIK              NOIZ?: AA sistemak EDOZEIN
       automatizatua denean                paper esanguratsu duenean

ZER?: "Logikari buruzko             ZER?: "Azalpen ARGI eta
       informazio esanguratsua"            ESANGURATSUAK"

ONDORIOA: Mugatua, zaila            ONDORIOA: Zabalagoa, praktikoagoa
          aplikatzea                          eta sendoagoa
────────────────────────            ────────────────────────

Zein da aldea praktikan?

GDPR-rekin: "Gure sistema honetako eta horretako algoritmoa erabiltzen du eta zure datu-profilean oinarritzen da." (orokorra, ez oso lagungarria)

AI Act-ekin (86. art.): "Zure kasu zehatzean, sistemak hauek aztertu ditu: lan-esperientzia (oso garrantzitsua), hezkuntza-maila (garrantzitsua), ibilbide geografikoa (txikia). Erabakiak faktore hauetan oinarritu da." (zehatza, ekintza-orientatua)

OHARRA

Hausnartzeko. Zein kasutan behar duzu gehiago azalpen bat?

a) Netflix-ek pelikula bat ez gomendatzean
b) Unibertsitateak sarrera ukatzen dizunean
c) Spam-iragazkiak mezu bat blokeatzean
d) Bankuak mailegu bat ukatzen dizunean

Erantzuna: b) eta d) dira garrantzitsuenak, ondorio juridikoak eta bizi-aldaketak eragiten dituztelako.

### 2.4. GARDENTASUNAREN 3 DIMENTSIOAK

Gardentasuna ez da kontzeptu bakar bat — hiru dimentsio ditu, eta guztiak beharrezkoak dira AA sistema baten konfiantza lortzeko:

12. Irudia: Gardentasunaren 3 dimentsioak — Trazabilitatea, Azalpen Teknikoa eta Komunikazioa

1. Trazabilitatea (Traceability)

Entrenamendu-datu guztien, etiketatzeko prozesuen eta erabaki algoritmikoen dokumentazio zorrotz eta jarraia, akats bat gertatuz gero etorkizuneko auditoretza posible egiteko.

ADIBIDEA

Osasun-diagnostiko sistema batek akats bat egiten du eta pazientea kaltetzen da. Trazabilitateak ahalbidetzen du ikerketa egitea: zein daturekin entrenatu zen? Zein errore-tasak zituen emakumeekin? Noiz eguneratu zen azkeneko aldiz? Zein medikuk erabiltzen zuen?

AI Act-en lotura: 12. art. — erregistro automatikoa derrigorrezko da arrisku altuko sistemetan. Enpresak ezin du esan "ez dakigu nola hartu duen erabakia sistemak" — trazabilitate-erregistroa egon behar da.

Trazabilitate-katea:

14. Irudia: Trazabilitate Algoritmikoaren Katea — entrenamendu-datuetatik azalpen-interfazera arteko erregistroa, kontroleko esku-hartzeekin

Entrenamendu-datuak → Ereduaren logika → Erabakia/Output → Azalpen-interfazea
      ↕                      ↕                   ↕                  ↕
  Datuak kalitate-   Diseinu           Aldakortasun-        Azalpena
  kontrola eta       interpretagarria  jarraipen eta        pertsonalizatua +
  sesgo-kontrola     eta dokumentazioa erregistroa          giza berrikuspena

2. Azalpen Teknikoa (Explainability)

Matematika-logika konplexua pertsona ulergarriak diren erabakietan itzultzeko gaitasuna — auditoreetarako, erabiltzaileentzat eta arautzaileentzat.

Garrantzitsua: Azalpen teknikoa ez da soilik erabiltzaileei esan zer erabaki hartu den — baita sistema osatzen duten eragile teknikoek ulertua egotea ere.

3. Komunikazioa (Communication)

AA sistemek beren burua modu argian identifikatu behar dute makina gisa erabiltzaileen aurrean, eta beren gaitasun eta muga errealak modu irekian komunikatu.

ADIBIDEA

- Chatbot bat → "Laguntzaile automatikoa naiz" (AI Act 50. art., gardentasun-betebehar orokorra erabiltzaileari)
- Irudi sortuak → Watermark edo metadatuen bidez identifikatua (AI Act 50.2 art. + GPAI betebeharrak 53. art.)
- Diagnostiko-sistema → Medikuntzari jakinarazi sistema honek zer ezin dezakeen egin ondo

Hiru dimentsioen arteko desberdintasuna garrantzitsua da:

FUNTSEZKO IDEIA

Trazabilitateak ez du esan nahi jabetza intelektuala agertu behar denik. Enpresak ez du bere kode-iturria erakutsi behar — baina bai erabakien inguruko dokumentazioa, datu-jatorria eta prozesuak.

### 2.5. KUTXA BELTZA VS AA AZALGARRIA (XAI): ALDERAKETA

Hemen dago galdera praktikoa: sistema opako bat edo sistema azalgarri bat? Biak ez dituzte emaitza berdinak erabaki eta konfiantza aldetik.

17. Irudia: Kutxa Beltza vs XAI — konfiantza, lege-betetzea, sesgo-detekzioa eta trazabilitatea

ADIBIDEA

Kasu errela. 2020an, Herbehereetako gobernuaren SyRI iruzur-detekzio sistema batek milaka herritar iruzurgiletzat jo zituen automatikoki, azalpen gabe. Epaileak sistema GELDITU zuen GDPR urratzeagatik: sistema kutxa beltz bat zen, eta herritarrek ezin zuten jakin zergatik izan ziren sailkatuak iruzurgile gisa.

Akats-motaren desberdintasuna kutxa beltz eta XAI artean:

• Kutxa beltz akats sistematikoa: ezin da detektatu kaltea gertatzen den arte

• XAI akats proaktiboa: aldagaien interpretazioak erakusten du aldez aurretik zein taldetan akatsak gertatzen ari diren

### 3.1. ZER DA AI ACT?

EU AI Act (Adimen Artificialaren Erregelamendua) 2024ko ekainean onartu zen eta munduko lehen AA lege integratua da. Ideia nagusia sinplea da:

FUNTSEZKO IDEIA

"AA sistema guztiak ez dira arrisku berdinekoak. Arrisku handiagoa → betebehar gehiago."

Hau da arriskuan oinarritutako ikuspegia: ez da teknologia bera arautzen, baizik eta erabilera-testuingurua.

5. Irudia: AI Act-en Arrisku-Piramidea — onartezina, arrisku altua, GPAI, gardentasuna eta arrisku minimoa

1. maila: Arrisku Onartezina — DEBEKATUTA

Hauek guztiz debekatuak daude Europan. Ez dago salbuespenik erabilera zibiletarako. Aplikazio-data: 2025eko otsailaren 2tik indarrean.

Zigorra: 35 milioi euro edo negozio-bolumenaren %7 — AI Act-eko zigorrik altuena.

ADIBIDEA

FP zentroan debekatutako sistema.

FP zentro batek software bat erosi nahi du ikasleek ordenagailuan zer egiten duten analizatzeko, barne argazkiak aterata (emozio-ezagutza). DEBEKATUTA dago: ikasleen emozioak ezin dira automatikoki aztertu hezkuntza-ingurunean. Saltzaileak ziurtatuko balu ere teknikoki ona dela — legea hautsi egiten da.

Zer egin behar da: Ikasleen jarduera-erregistroa erabili daiteke (zein aplikazio erabili duten), baina inoiz ez emozio-analisia. Giza irakasle baten behaketak balio du "jarduera-monitorizaziorako".

ADIBIDEA

Kasu errela: ClearView AI.

ClearView AI enpresa amerikarrak 30.000 milioi aurpegi-argazki baino gehiago bildu zituen Internetetik (Instagram, Facebook, LinkedIn...) baimenik gabe. Sistema polizia-departamentuei saldu zien. Europako hainbat herrialdek isun handiak jarri dizkiote eta EB-n erabat debekatua dago. Ikaspen nagusia: "aurpegien scraping" edozein arrazoirekin debekatua dago AI Act-en arabera.

2. maila: Arrisku Altua — Betebehar Zorrotzak

Arrisku altuko sistemek ez dute debekurik, baina betebehar zorrotz asko dituzte bete behar. Aplikazio-data: 2026ko abuztuaren 2tik.

Zein sektoretan daude arrisku altuko sistemak?

6. Irudia: Arrisku Altuko Sistemen Betebehar-Zikloa — 9-15. artikuluen betebehar etengabeak

Zer bete behar dute arrisku altuko sistemek?

ADIBIDEA

Osasun-zentro bateko triaje sistema.

Osasun-zentro batek AA sistema bat erosi du urgentzietan pazienteak lehentasunez ordenatzeko. Sistema honek 9-15 art. bete behar ditu:

- Datuen kalitatea (10. art.): entrenamendu-datuak emakumeekin eta gizonekin oreka egin behar du (bestela diagnostikoak okerrak izango dira genero batean)
- Erregistroa (12. art.): sistema honek zer erabaki hartu duen eta zergatik gorde behar da
- Giza gainbegiraketa (14. art.): mediku/erizainak erabakia ALDATU dezake sistemaren gomendioaren aurka

Aplikazio-data: 2026ko abuztuaren 2tik aurrera.

ADIBIDEA

Hezkuntzan — ikasleen nota-iragarpen sistema.

Unibertsitate batek AA sistema bat erabiltzen du lehen urteko ikasleek nota onena lortuko duten iragartzeko eta laguntza gehigarria zuzentzeko. Arrisku altuko sistema da (hezkuntza-emaitzak).

- Sistemak ez du ikaslearen jatorri sozioekonomikoa zuzenean erabili behar faktore bezala (diskriminazioa). Baina kode postala edo ikastetxe-mota → jatorri sozioekonomikoarekin korrelazioa → zeharkako diskriminazioa
- Irakasleak eskubidea du sistemaren gomendioaren aurka joateko
- Ikasleei jakinarazi behar zaie sistema bat erabiltzen ari dela

Zigorra: 15 milioi euro edo negozio-bolumenaren %3 (ez betetzeagatik).

3. maila: Arrisku Mugatua — Gardentasun-betebeharrak

Arrisku mugatuko sistemek ez dute betebehar teknikorik, baina erabiltzaileei esan behar diete AA sistema batekin ari direla. Inplikazioa nagusia: engainua debekatua.

ADIBIDEA

Bezero-arreta chatbot bat.

Dendak chatbot bat du bere webgunean. Bezeroek uste badute pertsona batekin ari direla eta chatbot bat dela jakiten dutenean engainatuta sentitzen dira. AI Act-en arabera: chatbot-ak beti esan behar du makina dela. Nahikoa da testu txiki bat: "Laguntzaile automatikoa naiz. Pertsona batekin hitz egin nahi baduzu, idatzi 'laguntza'."

ADIBIDEA

Deepfake biralak.

2023an, politikari baten deepfake bideoa zabaldu zen sare sozialetan, benetakoa zela uste zelarik. AI Act-en arabera: bideo hori sortu duen enpresak edo pertsonak bideo sortu bezala identifikatu behar du. Marka ikusgai bat behar da — ez "letra txikia".

4. maila: Arrisku Minimoa — Libre

AA sistemen gehiengoa betebehar berezirik gabe funtziona dezake. Adibideak:

• Spam-iragazkia — sarrerako mezua filtratzen du, ez dauka giza bizitzan ondorio zuzenik

• Netflix edo Spotify gomendio-sistema — entretenimendua, aukeran oinarritua

• Bideojoko-AI — jolaserako erabilera

• Google Translate — hizkuntz laguntza, ez erabaki kritikoak hartzen

KONTUZ

Sistema berak arrisku-maila desberdina izan dezake testuinguru desberdinetan. Adibidez:

- Chatbot bat bezero-arretarako → Arrisku Mugatua (gardentasun-betebeharra)
- Chatbot bera terapia psikologikorako → Arrisku Altua (osasun-arloa)

### 3.3. GPAI EREDUAK: CHATGPT EDO GEMINI BEZALAKOAK

AI Act-ek kategoria berezi bat sortu du Helburu Orokorreko AA Ereduentzat (General Purpose AI / GPAI): ChatGPT, Gemini, Claude... bezalako oinarrizko ereduak.

Zergatik berezia? Eredu hauek milaka aplikaziotan erabil daitezke eta arrisku berezi bat sortzen dute: eredu-sortzaileak ez daki nola erabiliko den gero.

ADIBIDEA

Enpresa batek ChatGPT-ren API-a erabiltzen du.

Enpresa batek bezero-arretarako sistema bat eraiki du ChatGPT-n oinarrituta. Ondorioak:

- GPAI betebeharrak (ChatGPT sortu duen OpenAI-k): dokumentazioa, copyright egiaztapena, arrisku-ebaluaketa
- Hedatzailearen betebeharrak (enpresak): chatbot-ak bere burua makina gisa identifikatu, erabiltzaileei gardentasuna
- GDPR (enpresak): erabiltzaileen datu pertsonalak tratatzen badira, baimen-prozesua eta datu-babesa

### 3.4. APLIKAZIO-KRONOLOGIA: NOIZ BETE BEHAR DA ZER?

AI Act-ek aplikazio graduala du. Garrantzitsua da jakitea, zeren betebehar batzuk indarrean daude eta beste batzuk ez oraindik:

7. Irudia: AI Act Aplikazio-Kronologia — 2024tik 2027ra gradualki

2024ko abuztuaren 1a
   └─ AI Act indarrean sartu zen

2025eko otsailaren 2a  ← INDARREAN DAGO JADA
   └─ Debekuak aktibatu (emozio-ezagutza lanean, social scoring...)
   └─ AA alfabetatze-betebeharrak

2025eko abuztuaren 2a  ← INDARREAN DAGO JADA
   └─ GPAI ereduen arauak (ChatGPT, Claude, Gemini...)
   └─ Europako AA Bulegoa martxan

2026ko abuztuaren 2a  ← HURRENGO MUGARRI NAGUSIA
   └─ Arrisku altuko sistemak bete behar dute
   └─ Gobernantza osoa aktibatu

2027ko abuztuaren 2a
   └─ Produktu erregulatuetan integratutako sistemak
      (mediku-gailuak, autoak...)

OHARRA

Hausnartzeko. FP zentro bateko irakasle gisa, ikasleen errendimendua ebaluatzeko AA sistema bat erosten baduzu, 2026ko abuztuaren 2tik aurrera arrisku altuko sistema bat izango da. Zer betebehar ditu?

Erantzuna: datuak kalitatezkoak izan behar dira (segasurik gabe), sistemak dokumentazioa behar du, irakasleak erabakia aldatu dezake, eta ikasleei esan behar zaie sistemak ebaluatzen duela.

### 3.5. ATE-SISTEMA: PIRAMIDEA BAINO ZEHATZAGOA

Praktikan, AA sistema batek aldi berean hainbat betebehar izan ditzake. Piramidearen ordez, pentsatu "iragazki-sistema" moduan:

8. Irudia: AI Act Ate-Sistema — lau iragazki sekuentzialak betebehar akumulatiboekin

Kontua da: irteera batek ez du geldiarazten gainerako ateetako azterketa. Sistema berberak ate guztiak pasa ditzake eta betebehar pilaketa sortzen da.

ADIBIDEA

HR plataforma bat LLM batekin (oso-osoa).

Enpresa batek CV-ak automatikoki sailkatzeko plataforma bat erosi du eta ChatGPT-n oinarrituta dago.

- 1. atea: Elkarrizketan emozioak analizatzen al ditu? → BAI → DEBEKATUTA

Onartu dezagun emozioak ez dituela aztertzen:

- 1. atea: Ez → pasa
- 2. atea: Langile-hautaketa → arrisku altua → 9-15 art. bete behar
- 3. atea: Hautagaiei esan behar zaie AA batek datuak tratatzen dituela → gardentasun-betebeharra
- 4. atea: ChatGPT erabiltzen du backend-ean → GPAI betebeharrak ere

Ondorioa: sistema honek lau maila bete behar ditu aldi berean.

### 3.6. AA FIDAGARRIAREN 4 PRINTZIPIO ETIKOAK

AI Act-ek lege-betebeharra arautzen du, baina bere oinarrian printzipio etikoak daude. Europako Batzordeak "AA Fidagarria" (Trustworthy AI) kontzeptua garatu du lau zutabetan:

13. Irudia: AA Fidagarriaren 4 printzipio — Autonomia, Kalterik Ez, Ekitatea eta Azalgarritasuna

1. Giza Autonomiaren Errespetua

AAk ez du menpekotasuna, hertsapena edo manipulazioa sortu behar. Alderantziz: giza gaitasun kognitiboak indartu behar ditu.

Praktikan zer esan nahi du?

• AAk gomendio bat eman dezake baina pertsona librea da ez jarraitzeko

• Sistema manipulatzaileak (dark patterns, emozio-ustiapena) printzipio honen kontra doaz

• "Addictive design" deritzonari (scroll infinitua, "auto-play"...) kritika etikoa egiten zaio

2. Kaltearen Prebentzioa (Do Not Harm)

Sendotasun teknikoa, datuen segurtasuna eta talde zaurgarrien babesa botere-asimetrietatik.

Praktikan zer esan nahi du?

• Sistemak robustua izan behar du: atake adbertsarialen eta akats teknologikoen aurrean

• Talde zaurgarriek (adindakoak, haurrak, ezintasun kognitiboak dituztenak) babes gehigarria behar dute

• Datu pertsonalen ihesa kalte zuzena da — teknikari bezala erantzukizun aktiboa duzu

3. Ekitatea (Fairness)

Onuren banaketa justua, alborapen injustuen prebentzioa eta ez-diskriminazioa.

Praktikan zer esan nahi du?

• Talde demografiko guztientzako emaitza parekoa lortu behar da

• Datu historikoak injustuak badira, sistema entrenatzeak injustiziak "ikasi" eta hedatzen ditu

• Ekitatea ez da lorpen automatikoa — esfortzua eskatzen du: sesgo-auditoria, datu-aniztasuna, metrika-aukera

ADIBIDEA

Ekitate-arazoa osasunean.

2019an, AEBetako ospitale baterako sistema batek etengabe emakumeak gutxiagoko arriskuan sailkatzen zituen gizonezkoek bezalako sintomak zeuzkatenean. Arrazoia: entrenamendurako datu historikoak erabili zituen eta historikoki gizonek osasun-arreta gehiago eskatzen zuten (egiturako bereizkeria), ez zuelako gaixotasun gutxiago. Sistema "equitable" zirudiena injustua zen.

4. Azalgarritasuna (Explicability)

Prozesuak gardenak izan behar dira eta erabakiak ulergarriak. Azalgarritasunik gabe, erabakiak ezin dira legez ez etikoki aurkaratu.

Praktikan zer esan nahi du?

• Erabaki garrantzitsu batek azalpen bat eduki behar du (GDPR 22. art. + AI Act 86. art.)

• Giza gainbegiraketa ezinezkoa da sistemak zergatik erabaki duen ulertzen ez bada

• Teknikariek XAI metodoak erabili behar dituzte arrisku altuko sistemetan

FUNTSEZKO IDEIA

Lau printzipioak eta legea. Printzipio hauek ez dira soilik etikoak — legean gauzatzen dira:

- Autonomia → AI Act 5. art. (debekuak: manipulazioa, social scoring)
- Kalterik Ez → AI Act 15. art. (zehaztasuna, sendotasuna, zibersegurtasuna)
- Ekitatea → GDPR 9. art. + AI Act 10. art. (datu-kalitatea, sesgo-prebentzioa)
- Azalgarritasuna → GDPR 22. art. + AI Act 86. art.

ARIKETA 2.1   ·   25 min  banaka edo bikoteka

Egoera. AI Act-ek lau arrisku-maila bereizten ditu: ezinezkoa, altua, mugatua eta minimoa. Sailkatu zuk hurrengo sistema bakoitza maila egokian eta justifikatu.

Sailkatu beharrekoak:

1.  ChatGPT-ren chatbot orokor bat enpresa baten web-orrian.

2.  Aurpegi-aitortza zentro komertzial batean ostuen aurka, denbora errealean.

3.  CV iragazki automatikoa, RR.HH. departamentuan.

4.  Spam-iragazki bat e-mail-zerbitzu batean.

5.  Sistemaren bat herritarrei "puntuazio sozial" bat ematen diena.

6.  Mediku-irudiak prozesatzen dituen sistema, oinarrizko diagnostiko-laguntzarako.

7.  Argazki-aplikazioko "edertasun-iragazkiak".

8.  Auto-konduzio autonomo (Tesla Autopilot moduko).

Eginkizuna. Bakoitzari maila bat esleitu, eta justifikatu hiru lerrotan zergatik. Ariketaren ondoren kontrastatu ondokoaren erantzunekin: bat datoz?

Eztabaidatzeko. Zerk egiten du sistema bat arrisku altu? Eredua sofistikatua delako? Erabakiek pertsonengan eragina dutelako? Bata ala bestea?

### 4.1. NOLA LOTZEN DIRA GDPR ETA AI ACT?

GDPR eta AI Act sarritan nahasten dira. Hauek dira desberdintasun nagusiak (eskuliburu didaktikoa, ez definizio legala: praktikan bi arauak elkar gainjartzen dira):

GDPR + AI Act: Ekosistema Fidagarria

Bi lege hauek batera funtzionatzen dute "Ekosistema Fidagarria" sortzeko:

ADIBIDEA

Bi arauak batera.

Osasun-zentro batek diagnostiko-sistema bat erabiltzen du:

GDPR-k esaten du:

- Pazienteen datuak (osasun-datuak = kategoria berezia) babes handia behar dute
- Pazienteei esan behar zaie sistema batek datuak tratatzen dituela
- Ezin da datu gehiagorik bildu behar dena baino

AI Act-ek esaten du:

- Sistema honek (osasun-arrisku altua) dokumentazioa behar du
- Medikuak gainbegiratu eta erabakia aldatu dezake
- Sistemak zehatza, sendoa eta segurua izan behar du

Bi arauak aldi berean bete behar dira.

### 4.2. OINARRIZKO ESKUBIDEEN GUTUNA: GUZTIEN OINARRIA

Bi arau hauek ez dira hutsetik sortu. EB-ko Oinarrizko Eskubideen Gutunak (2009) oinarri juridikoa ematen die:

9. Irudia: Marko Legalaren Geruza-Diagrama — kanpoko geruzak barnekoari oinarri juridikoa ematen dio

### 5.1. EUROPAKO MAILAKO ERAKUNDEAK

10. Irudia: Europako AA Gobernantza Instituzionala — AI Bulegoa, AI Batzordea, Panel Zientifikoa eta Agentzia Nazionalak

### 5.2. ESPAINIAN: AEPD ETA AESIA

Espainian bi erakunde nagusik egiten dute lan:

DEFINIZIOA

Datuak Babesteko Espainiako Agentzia (izen ofiziala: Agencia Española de Protección de Datos). GDPR-ren betearazpena Espainian: perfilatzea, biometria, erabaki automatizatuak. Isun-ahalmen handia.

DEFINIZIOA

Adimen Artifizialaren Gainbegiraketarako Espainiako Agentzia (izen ofiziala: Agencia Española de Supervisión de la Inteligencia Artificial). AI Act-en betearazpena Espainian eta AA sistemen kontrola. Europako lehen agentzia mota honetan.

ADIBIDEA

Isun erreala.

2023an Espainian, enpresa batek langile-aukeraketarako AA sistema bat erabili zuen generoa kontuan hartuz. AEPD-k 200.000€ko isuna jarri zuen GDPR 9. artikulua urratzeagatik (generoa kategoria bereziko datua da diskriminazio-potentzial altuan).

### 5.3. SANDBOX ERREGULATZAILEAK: PROBATZEKO INGURUNE SEGURUAK

AI Act-ek agintzen du estatu kide guztiek sandbox erregulatzaileak sortzea: ingurune kontrolatuak non enpresek AA sistemak isun-arriskurik gabe probatu ditzaketen, araudia betetzen duten egiaztatzeko.

Espainiak Europako lehen sandbox pilotua abiarazi zuen eta eredugarria da beste herrialdeentzat.

OHARRA

FP-rako garrantzia. Sandbox-ak aukera ematen die startup eta enpresa txikiei (FP ikasleek sortutakoak barne) produktu berritzaileak probatzeko legearen barnean, kosturik gabe. Aukera bikaina lehenengo enpresa-proiektuetarako.

## 10.2 6. Kasu Praktikoak: Zure Sektorearen Arabera

11. Irudia: Kasu Praktikoen Fluxu-Diagrama — GDPR eta AI Act-en eskubideak hiru egoera errealetan

### 6.1. INFORMATIKA ETA TELEKOMUNIKAZIO IKASLEENTZAT

Egoera. Teknikari gisa enpresa batean lan egiten duzu eta AA sistema bat instalatu behar duzu langile-aukeraketarako.

Zer galdetu behar diozu zure nagusiari:

• Sistema hau arrisku altukoa al da? (Bai: langile-hautaketa)

• Entrenamendu-datuak alborapenik gabe al daude?

• Erregistroak (logs) gordetzen al ditu?

• Kandidatuei jakinarazi al zaie?

• Giza gainbegiraketa-protokoloa dago?

Zure erantzukizuna teknikari gisa. Sistema instalatzean, eutsi dokumentazio guztiari eta ziurtatu gainbegiraketa-mekanismoek funtzionatzen dutela. Instalatzaileak ere badu erantzukizuna.

Egoera. Enpresa batek chatbot bat eraiki nahi du bezero-arretarako.

Egiaztatu behar duzuna:

• Chatbot-ak beti adierazi behar du makina dela

• Datu pertsonalak jasotzen baditu, GDPR bete behar da

• Bezeroei esan behar zaie euren datuak gordetzen diren

• LLM bat erabiltzen badu (Claude, Gemini...), GPAI betebeharrak ere bete behar dira

### 6.2. ADMINISTRAZIO ETA KUDEAKETA IKASLEENTZAT

Egoera. Udaletxe batean lan egiten duzu eta AA sistema bat erabiltzen da herritarren prestazioak kudeatzeko (diru-laguntzak, etxebizitza-eskariak...).

Arau nagusiak:

• Sistema hau arrisku altuko sistema da (zerbitzu publiko esentzialak)

• Herritarrek eskubidea dute giza langile batek beren kasua berrikusteko

• Erabaki guztiak dokumentatu behar dira (trazabilitatea)

• Herritarrek azalpena eskatu dezakete zergatik ukatu zaien prestazio bat

ADIBIDEA

Kasu errela: SyRI sistema Herbehereetan.

2020an, Herbehereetako gobernuak SyRI sistema bat erabili zuen iruzur sozialeko arriskua analizatzeko. Epaileak sistema GELDIARAZI zuen GDPR urratzeagatik: ez zuen gardentasunik, ez zuen azalpenik ematen, eta herri xeheari kalte gehiago egiten zien. Ondorio nagusia: teknologia ona izatea ez da nahikoa; legea ere bete behar da.

Egoera. AA sistema bat erabiltzen da enpresako langile-errendimendua ebaluatzeko.

Zer egin behar du HR teknikariak:

• Langileei jakinarazi sistema bat erabiltzen dela

• Aldizka aztertu sistemak alborapenik duen (genero, adin, jatorria...)

• Langileak eskubidea du erabakia giza langile batek berrikusteko

• Enpresa-batzordea informatu (Espainiako ET 64.4.d art.)

### 6.3. OSASUN ETA GIZARTE ZERBITZUETAKO IKASLEENTZAT

Egoera. Ospitale batean teknikari gisa lan egiten duzu. AA sistema bat erabiltzen da hiltzeko zorian dauden pazienteak identifikatzeko.

Zer bete behar da:

• Osasun-datuak = kategoria berezia → babes areagotua (GDPR 9. art.)

• EIPD (Eraginaren Ebaluazioa) derrigorrezkoa

• Medikuak edozein momentutan gelditu eta aldatu dezake sistemaren iritzia

• Sistemak ondo dokumentatua egon behar dira

• Pazienteei eskubideak azaldu behar zaizkie

ADIBIDEA

Sistemarik onenak ere akatsekin.

2019an, AEBetako ospitale bateko sistema batek etengabe emakumeak gutxiagoko arriskuan sailkatzen zituen gizonezkoek bezalako sintomak zeuzkatenean. Arrazoia: entrenamendurako datu historikoak erabili zituen eta historikoki gizonek osasun-arreta gehiago eskatzen zuten (egiturako bereizkeria), ez gaixotasun gutxiago zituztelako. Ondorio nagusia: datuetako alborapen historikoak sistemara pasatzen dira.

### 6.4. MERKATARITZA ETA MARKETING IKASLEENTZAT

Egoera. Enpresa batek bezeroei publizitate pertsonalizatua bidaltzen die AA bidez.

Zer galdetu:

• Bezeroak profilatu egiten al dira? → GDPR betebeharrak

• Ezaugarri sentikorrak erabiltzen al dira? (osasuna, arraza...) → Debekatuta gehienetan

• Bezeroak jakitun al dira? → Transparentzia-betebeharra

• Adingabeak inplikatuta al daude? → Babes gehigarria

ADIBIDEA

"Dark patterns" eta AA.

Moda-enpresa batek AA sistema bat erabili zuen bezeroak deskontua erabiltzen ez bazuten sentimendu-presioa sortzeko ("5 pertsonak ikusi dute orain produktu hau", "3 unitate gelditzen dira"). Hau teknika manipulatzaile bat da eta AI Act-ek debekatu dezake sistema honek pertsonaren portaera nabarmen alda badezake. Marra fina dago: presio legitimoa vs. manipulazioa.

## 10.3 7. Giza Gainbegiraketa Ereduak: HITL, HOTL eta HIC

AI Act-ek giza gainbegiraketa derrigorrezkotzat jotzen du arrisku altuko sistemetan (14. art.). Baina "giza gainbegiraketa" batek hiru forma desberdin hartzen ditu:

16. Irudia: Giza gainbegiraketa ereduak — autonomia-maila, interbentzio-unea eta AI Act-en lotura

### 7.1. HITL — HUMAN-IN-THE-LOOP (PERTSONA BEGIZTAN)

DEFINIZIOA

Giza esku-hartzea beharrezkoa da erabaki-ziklo bakoitzean. AAk proposatzen du, baina gizakiak berretsi edo aldatu behar du bakoitza.

AA-SISTEMA PROPOSATZEN DU
         ↓
   GIZA BERRIKUSPENA  ← derrigorrezko urratsa
         ↓
   BERRETSI / ALDATU / BAZTERTU
         ↓
    ERABAKIA HARTUA

Adibideak:

Abantailak:

• Emaitzen kalitate altua (akats larrien % murrizten du)

• Legalki sendoena: GDPR 22. art. + AI Act 14. art. betetzen du modu zabalean

• Pertsona bakoitzak kasua ikusi duenez, erantzukizuna argia da

Arriskuak:

AI Act-en lotura: Arrisku altuko sistema guztietarako derrigorrez giza berrikuspena posible izatea eskatzen da. HITL da betebehar hau betetzeko modurik zorrotzenena.

### 7.2. HOTL — HUMAN-ON-THE-LOOP (PERTSONA BEGIZTATIK KANPO)

DEFINIZIOA

AAk erabakiak autonomoki hartzen ditu, baina gizakiak sistemaren funtzionamendua monitorizatzen du eta behar denean interbenitu dezake.

AA-SISTEMAK ERABAKITZEN DU (autonomoki)
         ↓
   AUTOMATIKOKI EXEKUTATU
         ↓
   GIZA MONITORIZAZIOA  ← normalean ez du interrumpitzen
         ↓
   ANOMALIA DETEKTATU? → GIZA INTERBENTZIOA

Adibideak:

Abantailak:

• Abiaduraren onura gordetzen da

• Arrisku-eszenatoki garrantzitsuetan giza bermea dago

• Eskalagarria da erabaki-bolumen altuan

Arriskuak:

AI Act-en lotura: AI Act 14. art.: erabiltzaileak "esku hartu, gainbegiratu edo gainezarri ahal izatea". HOTL onargarria da arrisku erdi-altuko egoeretan, baina giza kontrola egiazki posible dela egiaztatu behar da.

### 7.3. HIC — HUMAN-IN-COMMAND (PERTSONA AGINTEAN)

DEFINIZIOA

Gizakiak beti du kontrol osoa AAren gainean — noiz erabili, nola erabili eta noiz desaktibatu. AAk ez du autonomia maila garrantzitsurik hartzen.

GIZA ERABAKIA: "AA sistema erabiliko dut"
         ↓
   AA-SISTEMA INFORMAZIOA ESKAINTZEN DU
         ↓
   GIZAKIAK INFORMAZIOA AZTERTU
         ↓
   GIZA ERABAKIA: onartze / aldatze / baztertzea
         ↓
    ERABAKIA EXEKUTATU

Adibideak:

Abantailak:

• Erantzukizuna oso argia: gizakiak erabakitzen du beti

• Erabilgarria helburu estrategiko, etiko edo salbuespenezko egoeretan

• "Beti itzali daitekeen botoia" bermatuta

Arriskuak:

### 7.4. HIRU EREDUEN KONPARAKETA ETA AI ACT-EN LOTURA

OHARRA

Hausnartzeko. Udal baten prestazioak kudeatzen dituen AA sistema bat: herritarrek diru-laguntza eskatu eta AAk ukatzen du automatikoki. Zein eredu da egokiena?

Erantzuna: HITL derrigorrezkoa da — ondorio juridikoak eta bizi-aldaketa dakar. AI Act Anexo III.5: "zerbitzu eta onura publikoak" arrisku altuko kategoria da. Herritarrak eskubidea du giza berrikuspena eskatzeko (GDPR 22. art.).

## 10.4 8. Zehaztasun vs Azalgarritasun Oreka: Teknikarientzako Dilema

AA sistema diseinatzerakoan, garrantzizko erabaki tekniko bat dago: zenbateko zehaztasuna vs zenbateko azalgarritasuna? Bi ezaugarri hauek sarritan kontrajarrita daude.

15. Irudia: Accuracy-Explainability tradeoff — eredu-mota desberdinen kokapenarekin

### 8.1. ZERGATIK AURKARITZEN DIRA?

ZEHAZTASUN ALTUA ←————————→ AZALGARRITASUN ALTUA
        ↑                              ↑
Sare Neuronal Sakonak         Erabaki-Zuhaitzak /
(Deep Learning)               Erregresio Lineal
                ↑
              Random Forest
              (erdibidean)

Sare neuronal sakonak — Altua zehaztasuna, baxua azalgarritasuna:

• Milioi bat datu eta mila milioi parametro → edozein eredu egoki deskribatu dezake

• Zergatia: parametroen arteko interakzioak oso konplexuak dira

• Legezko arazo nagusia: GDPR 22. art. eta AI Act 86. art. bete ezin duela

Erabaki-zuhaitzak / Erregresio lineala — Baxua zehaztasuna (askotan), altua azalgarritasuna:

• Pertsona batek berrikusita, erabakia algoritmoak bezala hartu du: gardena

• Azalpen erraz eta zuzena eman daiteke

• Legezko onura: GDPR eta AI Act betebeharrak errazago betetzen ditu

Random Forest — Erdibidean:

• Zuhaitz anitzen emaitzak batzen ditu → zehaztasun hobea

• Baina nola hartu den azken erabakia ez da zuhaitz bakarreko kasuan bezain garbia

### 8.2. LEGE-IMPLIKAZIOA: LEGEAK SAKRIFIZIO-AUKERA ESKATZEN DU

FUNTSEZKO IDEIA

"Eragin handiko erabakietan, legeak zehaztasun marginala sakrifikatzea eskatzen du azalgarritasuna eta prozedura-justizia bermatzeko."

Adibidea: Kreditu-eskaerak

Bankuak erregresio logistikoa hautatzen du (%12ko zehaztasun galera), zergatia: azalpen argia, auditatzea erraza, eta GDPR 22. art. betetzen duelako.

### 8.3. TEKNIKARIENTZAKO GAKO-GALDERA

Sistema bat diseinatzerakoan galdera hau egin behar da:

1.  Zer ondorio ditu erabakiak? (Bizimodua aldatzen badu → azalgarritasuna derrigorrezkoa)

2.  Zer arrisku-maila du? (Arrisku altua → AI Act 11-15 art. bete behar)

3.  Nork ikusiko ditu azalpenak? (Erabiltzailea, auditatzailea, epaileak...)

4.  Zehaztasun-galera onargarria da? (%5eko galera kreditu-sisteman vs %5eko galera diagnostiko-sisteman ≠ berdin)

ADIBIDEA

Zigor-sistema batean berrerortze-iragarpena.

COMPAS sistemak (AEBetan) sare neuronal komplexu bat erabiltzen du (zehaztasun altua). Baina ProPublica-ren azterketak erakutsi zuen arraza arteko akats-tasa desberdintasunak zeudela. Legezko arazo nagusia: sistemak ezin du azaldu zergatik sailkatzen duen pertsona bat arrisku altuan, eta azalpenik gabe, pertsonak ezin du erabakia aurkaratu. Europan sistema honek AI Act eta GDPR 22. art. urratuko lituzke.

## 10.5 9. Eragin Etikoko Ebaluazioa (EEE)

Lege-betebeharrez haratago, AA sistema baten eragin etikoa ebaluatzea praktika ona gisa gomendatzen da. UNESCO-ren oinarrietatik eratorritako galdera-zerrenda bat da tresnarik garrantzitsuenetako bat.

18. Irudia: Eragin Etikoko Ebaluazioa — 4 galdera-multzo sistema bateko erabaki etikoetarako.

OHARRA

Oharra: irudian gaztelaniaz dagoen "Sesgo-Auditoria" euskaraz "Alborapen-auditoria" da. Era berean, "pobreak" hitzaren ordez registro formalean "baliabide gutxiko pertsonak" erabili behar da.

### 9.1. ZERGATIK EEE BAT EGIN?

• Legeak "betebehar minimoak" ezartzen ditu — baina sistema etiko batek gehiago eskatzen du

• EEE-k akatsak diseinuaren fasean detektatzen ditu, sistemak kaltea egin baino lehen

• GDPR-k "Eragin Ebaluazioa" (EIPD) derrigorrean eskatzen du kategoria bereziko datuak direnean (GDPR 35. art.)

Bloke 1: Proportzionaltasuna eta "Ez Kalterik" (Do No Harm)

• AA al da irtenbide egokia? → Giza-teknikaria batez soluziorik ez al dago?

• Kalte itzulezinak al daude? → Gizarte-puntuaketa, masa-zaintza, adostasun ezinezkoa

• Talde zaurgarrienak kaltetuak izango dira? → Talde zaurgarriak (haurrak, adindakoak, baliabide gutxiko pertsonak)

ADIBIDEA

Udalak AA sistema bat erosi nahi du pobrezia-arriskua iragartzeko herritar batzuengan, laguntzak zuzentzeko. Proportzionala al da? Bai, baliabideak hobeto erabiltzeko. Kalterik al du? Bai, etiketapena kaltegarria izan daiteke pertsonen duintasunerako eta haien aukeretarako.

Bloke 2: Sesgo-Auditoria

• Entrenamendu-datuen kalitatea ebaluatu al da diskriminazio zuzena edo zeharkakoa saihesteko?

• Talde desberdintasunak neurtu al dira emaitzetan (generoa, arraza, adina, desgaitasuna)?

• Talde gutxituek adina datu al dituzte entrenamendurako?

Sesgo-auditoria nola egin (sinpleki):

1.  Hautatu adierazle bat: adibidez, "zenbatetan onartzen da taldeka"

2.  Konparatu talde artean: emakumeen onarpena vs gizonen onarpena

3.  Aztertu akats-motak: "faltsu positiboak" eta "faltsu negatiboak" taldeka berdinak al dira?

4.  Iturrian aurkitu arazoa: datuetan? ereduaren parametroetan? helburuen definizio okerrean?

Bloke 3: Diseinuz Pribatutasuna (Privacy by Design)

• Pribatutasun diferentziala erabiltzen al da? — datu pertsonalen zarata txertatzea gizabanakoa babestu eta taldeko estatistikak mantentzeko

• Pseudonimizazioa edo anonimizazioa posible al da entrenamendu-datuetan?

• Minimizazioa betetzen al da? (beharrezkoa dena baino datu gehiago ez)

Bloke 4: Erreklamazio-mekanismoak

• Kanal argi eta azkar bat al dago gizabanakoak erabakia giza talde baten aurrean aurkaratzeko?

• Denbora-mugan erantzungo al zaio erreklamazioari?

• Erreklamazio-ondorioa dokumentatuta geratuko al da sistemaren hobekuntzarako?

### 9.3. EEE VS EIPD (GDPR 35. ART.)

OHARRA

Jarduera: EEE taldeka. Hartu gai hau: Udaletxe batek AA sistema bat ezarri nahi du 911 larrialdi-deiei lehentasuna emateko (azkarrago erantzuteko zerbitzu kritikoetan). Egin EEE bat taldetan:

- Bloke 1: Proportzionala al da? Zer kalte posible?
- Bloke 2: Zein talde egon daiteke diskriminatuta? Zergatik?
- Bloke 3: Zer datu minimizatu daitezke?
- Bloke 4: Nola aurkara dezake herritarrak erabakia?

## 10.6 10. Erronkak: Oraindik Ebatzi Gabe Daudenak

Legeak existitu arren, arazo hauek oraindik konplexuak dira:

### 10.1. "NORK DU ERRUA?"

AA sistema batek kalte bat sortzen duenean, hainbat eragile daude:

Eredu-sortzailea → Integratzailea → Hedatzailea → Erabiltzailea
(adib. OpenAI)     (adib. enpresa)  (adib. ospital) (adib. medikua)

Arazo praktikoa: ospitale batek LLM bat erabiltzen du diagnostikoak egiteko eta akats bat egiten du. Nork du erantzukizuna? Legea hau argitzen saiatzen ari da, baina oraindik ere oso konplexua da.

### 10.2. EREDU ITXIAK AUDITATU

Nola auditatu milaka milioi parametroko eredu bat? Enpresa txiki batek ez du gaitasun teknikorik GPT-4 bezalako sistema bat auditatzeko. AI Act-ek aukera ematen dio Europako AI Bulegoari auditoria hauek egiteko, baina gaitasuna garatzen ari da oraindik.

### 10.3. AZALPEN "NAHIKOA" ZER DA?

GDPR-k esaten du "informazio esanguratsua" eman behar dela. AI Act-ek "azalpen argi eta esanguratsuak" eskatzen ditu. Baina zenbat eta zer nahikoa da? Oraindik tribunalen eskuetan dago erabakia.

OHARRA

Debate-gaia klaserako. "Gemini bezalako sistema batek eskubide-erabaki bat hartzen duenean (adib. kreditu-eskaera ukatzea), posible al da azalpen "nahikoa" bat ematea mila milioi parametroko eredu batentzat?"

Bi talde: batak defenda dezake baietz (método post-hoc-ak nahikoak dira); besteak ezetz (hurbilketak soilik dira, ez azalpen errealak).

### 11.1. GAUZA GARRANTZITSUENAK

### 11.2. FP IKASLE GISA ZER EGIN DEZAKEZU

Lan-munduan sartzen zarenean, galdera hauek egin itzazu AA sistema bat ikusi edo instalatzen duzunean:

1.  Zer datu tratatzen ditu? → Pertsonalik bada, GDPR aplikatzen da

2.  Zer erabakitan parte hartzen du? → Garrantzitsua bada (enplegua, osasuna...), AI Act aplikatzen da

3.  Erabiltzaileei esan al zaie? → Gardentasun-betebeharra

4.  Giza gainbegiraketa al dago? → Zein eredu da? HITL, HOTL ala HIC?

5.  Dokumentazioa al dago? → Legala bada, paperak egon behar dira

6.  Sesgo-auditoriarik egin al da? → Arrisku altuko sistemetan derrigorrezkoa

7.  Azalpen bat eman al daiteke? → Kutxa beltza bada, legalki arriskutsua da

### 11.3. IDEIA NAGUSIA

FUNTSEZKO IDEIA

Europan, AA ona ez da soilik teknologikoki aurreratua edo ekonomikoki errentagarria: ona izateko, aldi berean bete behar ditu:

- Erabilgarria izatea
- Segurua izatea
- Oinarrizko eskubideak errespetatzea
- Giza kontrola izatea (HITL/HOTL/HIC egoki hautatuta)
- Azalpen bat eman ahal izatea
- Juridikoki erantzule izatea
- Ekitatiboa izatea talde guztientzat

## 10.7 12. Amaierako proiektu integratzailea: enpresa bati GDPR + AI Act compliance-laguntza

ARIKETA 3.0   ·   4 saio  taldeka (4 ikasle)

PROIEKTU INTEGRATZAILEA: enpresarentzat compliance-azterketa

### Kasua

Tokiko enpresa batek AA sistema bat ezarri nahi du, eta zuei eskatu dizue compliance-azterketa egin dezatela legealdiko betebeharrak ulertzeko. Aukeratu enpresa-mota zuen FP-zikloaren araberakoa:

- Informatika: ChatGPT-bidezko bezero-arreta automatikoa enpresa-webgune batean.
- Administrazioa: Udaletxearen prestazio-eskaerak iragazteko AA tresna.
- Osasuna: Errezeta-historialen analisi automatikoa lehen mailako arretarako.
- Heziketa: Ikasleen errendimendua aurresan eta talde-banaketa proposatzen duen tresna.
- Merkataritza: Marketing pertsonalizatua, bezeroaren portaeran oinarritua.

### Eskakizun teknikoak

1.  GDPR analisia (1. atala)

2.  Azalpenaren eskubidea (2. atala)

3.  AI Act sailkapena (3. atala)

4.  Gainbegiraketa (5-7. atalak)

5.  EEE — Eragin Etikoko Ebaluazioa (9. atala)

### Entregablea

- Compliance-txosten teknikoa (12-15 orrialde): atalez atal.
- Enpresa-aurkezpen exekutiboa (15 min): zuzendaritzari aurkeztu, gomendio bat sartuz: aurrera egin, aldatu edo abandonatu.
- Klausulak idatzi: erabiltzailearentzako informazio-orria (gardentasun-betebeharra), barneko zuzendaritzaren protokoloa.

### Ebaluazio-irizpideak

| Atala | Pisua |
|-------|-------|
| GDPR azterketa zuzena | %20 |
| AI Act sailkapen justifikatua | %20 |
| Azalpenaren eskubidea aplikatua | %15 |
| Gainbegiraketa-eredua aukeratua | %15 |
| EEE osoa | %20 |
| Aurkezpenean defentsa argia | %10 |

### JARDUERAK

1. jarduera — Kasu-azterketa (45 min). Taldeka, aukeratu sektore bat (osasuna, enplegua, administrazioa, hezkuntza). Enpresa batek AA sistema bat erosi nahi du sektore horretan. Taldeak aztertu behar du:

• Zein arrisku-mailan dago?

• Zein betebehar ditu?

• Zein galdera egin behar dizkio enpresak hornitzaileari?

2. jarduera — Isun-simulazioa (30 min). AEPD-ren webgunean isun erreal bat bilatu eta aztertu: zergatik jarri zuten, zer urraketa gertatu zen, nola saihestu zitekeen.

3. jarduera — Azalpen-proba (20 min). Kreditu-eskaera ukatzeko AA sistema bat simulatu. Talde batek bankua jokatzen du eta beste taldeak bezero-eskubideak baliatzea simulatzen du: azalpena eskatu, giza berrikuspena eskatu, aurkaratu.

4. jarduera — Gainbegiraketa eredua aukeratu (30 min). Taldeek hiru egoera hauek aztertzen dituzte eta HITL, HOTL ala HIC zein egokiena den eztabaidatzen dute, eta zergatia argitzen:

• Udaletxeko diru-laguntza-sistema

• Bankuko iruzur-detekzio sistema

• Enpresako estrategia-aholkulari sistema

5. jarduera — EEE simulazioa (45 min). Taldeka, AA sistema bat aukeratu eta 9.2 ataleko lau galdera-blokeak erantzun: proportzionaltasuna, sesgo-auditoria, diseinuz pribatutasuna, erreklamazio-mekanismoak.

### EBALUAZIO-IRIZPIDEAK

## 10.8 14. Glosarioa

### ARAUDIA

1.  Erregelamendua (EB) 2024/1689 — EU AI Act

2.  Erregelamendua (EB) 2016/679 — GDPR

3.  Europako Oinarrizko Eskubideen Gutuna (2009)

4.  LO 3/2018 — LOPDGDD (Espainia)

5.  ET 64.4.d — Estatuto de los Trabajadores / Langileen Estatutua (algoritmoen gardentasun-betebeharra langile-ordezkarien aurrean)

### BALIABIDE DIGITALAK

1.  [AI Act Service Desk](https://ai-act-service-desk.ec.europa.eu) — Batzordearen tresna ofiziala

2.  [artificialintelligenceact.eu](https://artificialintelligenceact.eu) — Kronologia eta laburpena

3.  [AEPD Gidak](https://www.aepd.es) — Espainiako gidak eta adibideak

4.  [AESIA](https://aesia.digital.gob.es) — Espainiako AA agentzia

5.  [UNESCO AI Ethics](https://www.unesco.org/en/artificial-intelligence/recommendation-ethics) — Etika gomendio globala

Lanbide Heziketa ikasle eta irakasleentzat prestatua. Eduki hau hezkuntza-helburuetarako da eta ez du aholku juridiko profesionalik ordezkatzen.

| EGILEA |  |

| ZENTROA | Laneki — FP Euskadi |

| EDIZIOA | v1.0 |

| IKASTAROA | 2026 — 2027 |

| Araua | Zer arautzen du? | Noiz sartu zen indarrean? |

| GDPR | Datu pertsonalak nola tratatu | 2018ko maiatzaren 25a |

| Azalpenaren Eskubidea | Erabaki automatizatuen azalpena jasotzeko eskubidea | GDPR-rekin batera (2018); AI Act-ekin indartu (2026) |

| EU AI Act | AA sistema motak eta betebeharrak | 2024ko abuztuaren 1ean indarrean; gradualki aplikatzen (debekuak 2025/02, GPAI 2025/08, arrisku altua 2026/08, produktu erregulatuak 2027/08) |

| Atala | Galdera nagusia | Zer egingo duzu |

| 1. GDPR | Nola tratatu datu pertsonalak? | 7 printzipioak aplikatu |

| 2. Azalpen-eskubidea | Nork du eskubidea jakiteko zergatik? | Hiru osagaiak banatu |

| 3. EU AI Act | Zer arrisku-maila du nire AA-k? | Lau mailen sailkapena |

| 4-5. Lotura eta erakundeak | Zein dira gainbegiraleak? | AEPD, AESIA, sandbox-ak |

| 6. Sektore-kasuak | Nire FP-zikloan nola aplikatu? | Lau sektoreren adibideak |

| 7-8. Giza gainbegiraketa | HITL, HOTL, HIC zer da? | Eredua aukeratu kasuko |

| 9-10. Tradeoffak eta EEE | Zehaztasun vs azalgarritasun? | Eragin etikoko ebaluazioa |

| # | Printzipioa | Zer esan nahi du praktikan? |

| 1 | Legezkotasuna | Datu bat tratatzeko arrazoi bat behar duzu (adostasuna, kontratua, legea...) |

| 2 | Helburua | Datuak helburu zehatz baterako bakarrik erabili. Curriculum bat irakurri duzu → ezin duzu marketinerako erabili |

| 3 | Minimizazioa | Behar duzuna bakarrik bildu. Ez galdetu jaiotze-data ez bada beharrezkoa |

| 4 | Zehaztasuna | Datuak eguneratuta egon behar dira. Zaharkitutako datuak ezabatu. |

| 5 | Denbora- muga | Beharrezkoa den denboran bakarrik gorde. Gero ezabatu. |

| 6 | Segurtasuna | Datu-ihesak saihesteko neurriak hartu |

| 7 | Erantzukizuna | Enpresak frogatu behar du arauak betetzen dituela |

| Erabakia | Garrantzitsua al da? |

| Kreditu-eskaera onartua/ukatua | Bai (ondorio juridikoak) |

| CV bat lehenago hautatu edo baztertu | Bai (enplegua eragiten du) |

| Langile baten errendimendua ebaluatu | Bai (soldata, sustapena...) |

| Ikas-aholkua eman | Baliteke (hezkuntza-ibilbidea) |

| Spam-mezua iragazki batek blokeatu | Ez (ondorio txikia) |

| Netflix-ek pelikula bat gomendatu | Ez (ondorio txikia) |

| Osagaia | Zer esan nahi du? | Non dago jasota? |

| Logika ulergarria | Faktore nagusiak eta erabakiaren oinarria ezagutzeko eskubidea | GDPR 22. art. |

| Giza esku-hartzea | Pertsona erreal bati erabaki automatizatua berrikusteko eskatzeko eskubidea | GDPR 22. art. |

| Ikuspuntua adierazteko | Erabakiaren aurka argudiatzeko eta testuinguru gehiago aurkezteko aukera | GDPR 22. art. + AI Act 86. art. |

| Iturria | Artikulua | Zer esaten du? |

| GDPR | 13, 14, 15 art. | Erabaki automatizatuei buruzko informazioa eskatzeko eskubidea |

| GDPR | 22 art. | Logikari buruzko informazio "esanguratsua" jasotzeko eskubidea |

| EU AI Act | 86 art. | "Azalpen argi eta esanguratsuak" jasotzeko eskubidea (2026tik) |

| Metodoa | Nola funtzionatzen du? | Adibidea |

| SHAP | Aldagai bakoitzaren ekarpen "zehatza" kalkulatzen du | "Kreditua ukatu da: diru-sarrerak (-%40), lana (%+20), zorra (-%35)..." |

| LIME | Kasu konkretu baten azalpen sinple bat sortzen du | "Zure kasuan, lan-egonkortasuna izan da faktorerik garrantzitsuena" |

| Kontrafaktuala | Erantzuten du: "Zer aldatu beharko zenuke onarpena lortzeko?" | "500€ gehiago irabaziko bazenu, onartua izango zinateke" |

| Dimentsioa | Galdera | Eragilea |

| Trazabilitatea | "Nola hartu da erabakia?" | Auditoreak, arautzaileak |

| Azalpen teknikoa | "Zergatik hartu da erabakia?" | Erabiltzaileak, teknikariak |

| Komunikazioa | "Nork hartu du erabakia?" | Orok jakin behar du |

| Alderdiak | Kutxa Beltza | AA Azalgarria (XAI) |

| Erabiltzailearen Konfiantza | Baxua — erabiltzaileak ez daki zergatik erabaki den | Alta — erabiltzaileak logika ulertu eta onartzen du |

| Betebehar Legala | Zigorgarria GDPR 22. art. eta AI Act-en arabera | Gardentasun- eta auditoretza-betebeharrak betetzen ditu |

| Sesgo-detekzioa | Zaila kaltea sistematikoa bihurtu arte | Aldagai diskriminatzaileak era proaktiboan identifikatu |

| Trazabilitatea | Ezinezkoa "zergatia" berreraikitzea akats baten ondoren | Erregistro osoa sarreratik irteerara arte |

| Praktika debekatua | Zergatia | Inplikazioak |

| Gizarte-puntuazioa (social scoring) | Duintasuna urratzen du | Txinan bezalako sistema bat non portaerak puntuazioa ematen dion herritarrari, ondoren zerbitzuak (garraio, hezkuntza) mugatzeko. Ondorioa: pertsonak beldurrez bizi, pentsamendu librea ahultzen. |

| Teknika subliminalak | Libre-nahia kentzen du | App batek ezabatze-botoia ikusezin egitea bertan jarraitzeko; edo algoritmoak emozio-egoerak ustiatzea produktuak saltzeko kontzientzia gabe. |

| Emozio-ezagutza lan-gunean | Intimitatea urratzen du | Kameraren bidez langileen estresa edo poza neurtzen duen sistema. Ondorioa: langileek beldurrez bizi, etengabeko zaintza-sentsazioa, eztabaidarako eta sindikalizaziorako askatasuna murriztu. |

| Emozioen ezagutza hezkuntza-ingurunean | Haurren babesa | Ikasleek pantailan zer sentitzen duten analizatzen duen tresna. Ondorioa: haurren garapen normala kaltetu, etengabeko ebaluazio-sentsazioa, konfiantzazko harreman pedagogikoa suntsitu. |

| Aurpegi-ezagutzarako datu-base masiboak | Pribatutasun-urraketa | Internetetik milaka aurpegi-argazki bildu eta datu-base bat sortu baimenik gabe (ClearView AI kasu ospetsua: 30.000 milioi argazki bildu zituen). Ondorioa: pertsona orok bere irudia ustiatu dela jakitea. |

| Aurpegi-ezagutza denbora errealean espazio publikoetan | Masa-zaintza galarazten du | CCTV kamerak espazio publikotan pertsona guztiak identifikatzen dituena denbora errealean (salbuespen oso murritzak: terrorismoaren bilaketa judizialaren baitan). |

| Pertsonen profila arriskuaren arabera eratu | Aurreikuspen injustua | Aurretiko delitua egin gabe pertsonak arrisku-talde bezala sailkatzea, soilik ezaugarri demografikoekin. |

| Sektorea | Sistema adibideak | Inplikazio nagusiak |

| Osasuna | Diagnostikoa, triajea, tratamendu-aholkuak | Diagnostiko okerrak bizitzak arriskuan jarri dezake. Entrenamendu-datuak genero eta etnia artean orekatu behar dira. |

| Enplegua | Hautaketa, ebaluazioa, deskontraketa | Sesgoek gaitasun berdinak dituzten hautagaiak bazter dezake. Trazabilitateak enpresa-batzordea informatzea eskatzen du. |

| Hezkuntza | Onarpen-sistemak, azterketa-ebaluazioa, nota-iragarpenak | Ikasle batek bere etorkizuna aldatzen duen erabaki bat automatikoki jasotzen du. Jatorri sozioekonomikoak edo desgaitasunak ez dira faktore zuzen gisa erabili behar. |

| Finantza | Kreditua, asegurua, scoring-a | Mailegu bat ukatzeak etxebizitza, enpresa edo ikasketak arriskuan jarri ditzake. Azalpenak konkretuak eta ekintza-orientatuak izan behar dira. |

| Justizia | Berrerortzeko arrisku-ebaluazioa (COMPAS bezalakoak) | Askatasuna mugatu dezake. Arraza edo jatorria ez da zuzenean erabili behar — eta aldagaien arteko korrelazioak ezin ditu zeharkako diskriminazioa sortu. |

| Segurtasuna | Iruzur-detekzioa, arrisku-profilatzea | Herritar errugabeak susmagarri gisa sailkatzeak kaltea sortzen du. Emaitza okerren banaketa talde guztientzat berdin egon behar da. |

| Administrazioa | Prestazioak kudeatzea, migrazioa, asilo-eskariak | Bizitzako erabaki kritikoak: etxea, familia-batasuna, asiloa. Herritarrek eskubidea dute giza langile batek berrikusteko. |

| Betebeharra | Artikulua | Zer esan nahi du praktikan? |

| Arrisku-kudeaketa | 9. art. | Sistemak bizi-ziklo osoan arrisku-ebaluazioa behar du |

| Datuen kalitatea | 10. art. | Entrenamendu-datuak ez dira sesgadunak izan behar — desoreka eta benetako ordezkaritza egiaztatu |

| Dokumentazioa | 11. art. | Sistemak zer egiten duen eta nola dokumentatu — auditorea sistemaz jabetu dadin |

| Erregistroa (logs) | 12. art. | Erabaki guztiak gordeta egon behar dira (trazabilitatea) — ikerketarako beharrezkoa |

| Gardentasuna | 13. art. | Erabiltzaileei azaldu sistemak zer egiten duen eta mugak zeintzuk diren |

| Giza gainbegiraketa | 14. art. | Pertsona batek gainbegiratu, gelditu eta aldatu ahal izatea |

| Zehaztasuna eta segurtasuna | 15. art. | Sistemak ondo funtzionatu behar du eta erresistentea izan behar da erasoen aurrean |

| Sistema | Betebeharra | Zer gertatzen da ez bada betetzen? |

| Chatbot-a (adib. webguneko laguntza) | "Adimen artifiziala naiz, ez pertsona" | 15M€ isuna edo %3; erabiltzaileak engainatuta sentituko dira eta konfiantza galduko da |

| Deepfake bideoa | "Bideo hau artifizialki sortua da" | Informazio-manipulazioaren erantzukizuna; demandak posible |

| AA sortutako irudia | "Irudi hau AA bidez sortua da" | Copyright-arazoak + engainuaren erantzukizuna |

| Emozio-ezagutza sistema (ez debekatuak) | "Sistema honek emozioak analizatzen ditu" | Adostasun-urraketa + GDPR 9. art. |

| Betebehar mota | Zer esan nahi du praktikan? |

| Dokumentazioa | Nola entrenatu den, zertarako, zer datu erabili diren |

| Gardentasuna | Entrenamendu-datuei buruz informatu, ezagutza-mugak adierazi |

| Copyright-a | Entrenamendu-datuak lege-bidezkoak izan behar dira; egile-eskubideen jabeekin negoziatu edo erregistratu |

| Deepfake markaketa | AA sortu duen edozein irudi, audio edo bideo identifikatua egon behar da watermark edo metadatuekin |

| Arrisku sistemikoa | 10²³ FLOP baino gehiago erabili dituzten ereduak (gehien eragina izaten dutenak): arrisku-ebaluaketa eta larrialdi-protokoloak beharrezkoak |

| Atea | Galdera | Adibidea |

| 1. atea | Debekatuta al dago? | Ikasleek emozioak aztertzea → BAI → DEBEKATUTA |

| 2. atea | Arrisku altukoa al da? | CV-iragazkia → BAI → Betebehar areagutuak |

| 3. atea | Gardentasun-betebeharra? | Chatbot bat → BAI → Erabiltzailea informatu |

| 4. atea | GPAI eredua erabiltzen du? | ChatGPT backend-ean → BAI → GPAI betebeharrak ere |

|  | GDPR | AI Act |

| Zer arautzen du? (didaktikoki) | Sarrerako datuak (pertsonei buruzko informazioa) | Irteera-sistema (AA produktua bera) |

| Nork bete behar du? | Datu-arduradunak eta tratatzaileak | Hornitzaileak eta hedatzaileak |

| Noiz aplikatzen da? | Datu pertsonalak daudenean beti | AA sistema bat erabiltzen denean |

| Zigorra | 20M€ edo negozio-bolumenaren %4 | 35M€ edo negozio-bolumenaren %7 |

| GDPR bake-tik | EB biak elkar lotu | AI Act-etik |

| Datu pertsonalen babesa | AA Fidagarria | AA sistemaren segurtasuna |

| Profil ez konsentituak saihestea | Azalgarritasun derrigorrezkoa | Arrisku-ebaluaketa eta mitigazioa |

| 100% erabaki automatizaturik ez | Giza gainbegiraketa bermatua | GPAI ereduen gobernantza |

| Artikulua | Eskubidea | AA-rekin lotura |

| 1. art. | Giza duintasuna | Pertsonak tratu degradagarria jasan ezin du AA bidez |

| 7. art. | Bizitza pribatua | Datu pertsonalak babestea |

| 8. art. | Datu pertsonalen babesa | GDPR-ren oinarria |

| 21. art. | Diskriminaziorik eza | AA sistemek ezin dute bereizkeria egin |

| 47. art. | Tutela judiziala | Erabaki automatizatua aurkaratu dezakezu epaitegietan |

| Erakundea | Zer egiten du? |

| Europako AA Bulegoa (AI Office) | Koordinazioa eta GPAI ereduen zuzeneko gainbegiraketa |

| Europako AA Batzordea (AI Board) | 27 estatu kideen ordezkariak. Aplikazioa koordinatu |

| Batzorde Zientifikoa | Aditu independenteak. Aholkularitza teknikoa |

| Foro Aholkularia | Enpresak, sindikatuak, unibertsitateak, gizarte zibila |

| Sektorea | Nola funtzionatzen du? |

| Osasun-diagnostikoa | AAk CT irudi batean tumore posible bat identifikatzen du → Erradiologoak berrikusi eta ziurtatzen du baino lehen diagnostikoa ematen da |

| Langile-aukeraketa | AAk CVak iragazten ditu eta zerrenda bat proposatzen du → HR teknikariak zerrendatik hautagaiak aukeratzen ditu elkarrizketarako |

| Kreditua onartzea | AAk arrisku-puntuazioa kalkulatzen du → Analista finantziero batek puntuazioa aztertu eta onartzen edo ukatzen du |

| Eduki moderazioa | AAk arau-hausle posible bat markatzen du → Moderatzaileak kasua aztertu eta erabakia hartzen du |

| Arriskua | Azalpena | Konponbidea |

| "Automation bias" | Gizakiek joeraz AAren proposamena jarraitzen dute kritikoki aztertu gabe | Prestakuntza + erregistroa proposamena aldatu den ala ez ikusteko |

| Denbora-kostua | Erabaki bakoitzak giza denbora behar du | Berrikuntzarako unitate txikitan probatu; presioa argi identifikatu |

| Eskala arazoa | Mila erabaki eguneko: ezinezkoa dena berrikustea sakon | HITL erabaki garrantzitsuenetan soilik; gainerakoak HOTL |

| Sektorea | Nola funtzionatzen du? |

| Iruzur-detekzioa bankuan | AAk susmopeko transakzioak automatikoki blokeatzen ditu → Analistek eguneko kasuen pila aztertzen dute eta behar izanez gero aldatzen dituzte erabakiak |

| Sare elektrikoa | AAk karga oreka automatikoki mantentzen du → Operadoreak dashboardean anomaliak ikusiz gero eskuz aldatzen du |

| Trafiko-kontrola | AAk semaforo-denborak optimizatzen ditu → Udaleko teknikariak monitorizatzen du eta larrialdiak eskuz kudeatzen ditu |

| Aktibo finantzarioen trading-a | Algoritmoak autonomoki erosi eta saltzen du → Dendak limiteak eta alarmak ditu eta operadoreak arriskua monitorizatzen du |

| Arriskua | Azalpena | Konponbidea |

| "Alert fatigue" | Alerta gehiegi badira, garrantzitsuenak ez ikusteko arriskua | Alerta-leihoak moldatu eta optimizatu; ez guztia alerta egitea |

| Kontrol-itxura | Teorian pertsonak kontrolatzen du, baina azkarregi gertatzen dena ezin da kontrolatu praktikan | Argi definitu zer erabaki-motetan den HOTL nahikoa |

| Erantzukizun-nahasketaa | Sistemak autonomoki erabaki du, baina pertsona monitorizatzen ari zen → Nork du errua akats batean? | AI Act-ek rol-banaketa argi eskatzen du |

| Sektorea | Nola funtzionatzen du? |

| Enpresako estrategia | AAk merkatuko txostenak eta iragarpenak presta ditzake → Zuzendaritza-taldeak txostenak aztertu eta estrategia erabakitzen du |

| Osasun paliatiboa | AAk mina kontrolatzeko protokoloak iradoki ditzake → Mediku-taldeak erabakitzen du arretaren norabidea |

| Gerra-erabakiak | Estatuak ados daude AAk inoiz ez dituela autonomoki armak erabiltzeko baimenak eduki behar (debate aktiboan oraindik) |

| Lege-aholkularitza | AAk jurisprudentzia eta kasu antzekoak aurkitzen ditu → Abokatu batek kasua aztertu eta estrategia juridikoa erabakitzen du |

| Arriskua | Azalpena | Konponbidea |

| Inertzia-presioa | "Sistemak beti gomendatzen du X eta guk beti baietz ematen diogu" → HITL/HOTL bihurtzen da praktikan | Aldizka erabakiak berrikusi gomendioaren kontrakoak hartu diren ala ez ikusteko |

| Eskalagarritasun mugatua | Erabaki bolumen handirako ezinezkoa da HIC erabiltzea | HIC erabaki kritiko eta gutxi batzuetarako; beste kasu batzuetarako HITL/HOTL |

| Independentzia-sentsazio faltsua | Gizakiak uste du kontrolatzen duela baina AAren outputa bere iritzia aldatzen ari da | Transparentzia AA sistemak duen eraginaren inguruan |

| Alderdiak | HITL | HOTL | HIC |

| AA autonomia-maila | Baxua — soilik proposatu | Ertaina — exekutatu eta monitorizatu | Ia nulua — soilik informatu |

| Giza esku-hartzea | Erabaki bakoitzean | Anomalia edo arazoetan | Estrategia-mailako erabakietan |

| Abiaduraren onura | Galtzen da | Mantentzen da | Mantentzen da (maila estrategikoan) |

| AI Act betegarritasuna | Zorrotza | Egoera batzuetan onartgarria | Ez nahikoa arrisku altuko sistemetan |

| Adibidea tipikoa | Osasun-diagnostikoa | Bankuko iruzur-detekzioa | Enpresako estrategia |

| Arrisku nagusia | Automation bias | Alert fatigue | Inertzia-presioa |

| Eredua | Zehaztasuna | Azalgarritasuna | Legalki? |

| Sare neuronal sakona | %94 | Oso baxua | AI Act betebeharrik ez du betetzen |

| Random Forest | %89 | Ertaina | Post-hoc XAI metodoekin posible (SHAP) |

| Erregresio logistikoa | %82 | Altua | Azalpen zuzena eman daiteke |

|  | EEE (Eragin Etikoko Ebaluazioa) | EIPD (GDPR 35. art.) |

| Derrigorrezkoa al da? | Gomendatua (ez legez) | Legez derrigorrezkoa kategoria bereziko datuetan |

| Zer aztertzen du? | Inpaktu sozial eta etikoa | Datu-babesa eta pribatutasuna soilik |

| Noiz egin? | Diseinu-fasean | Tratamendua hasi baino lehen |

| Nork egin? | Talde interdisziplinarra | Datu-babeseko ordezkaria (DPO) |

| Araua | Ideia nagusia | Artikulu gakoa |

| GDPR | Datu pertsonalak babesteko | 22. art.: erabaki automatizatuak |

| Azalpenaren eskubidea | Jakiteko eskubidea zergatik | GDPR 13-15 + AI Act 86. art. |

| EU AI Act | Arrisku-mailaren araberako betebeharrak | 5. art. (debekuak), 14. art. (gainbegiraketa) |

| Gaitasuna | Gutxienekoa | Ongi | Bikain |

| GDPR 22. art. identifikatu | Zer den jakin | Kasu batean aplikatu | Salbuespenekin lan egin |

| AI Act arrisku-mailak | Lau mailak izendatu | Adibideak eman | Sistema zehatz bat sailkatu |

| Azalpenaren eskubidea | Existitzen dela jakin | Egoera batean eskatu | GDPR vs AI Act alderantzikatu |

| Praktika debekatuak | Bat azaldu | Hiru adibide eman | Muga-kasua argudiatu |

| HITL/HOTL/HIC bereizi | Hiru kontzeptuak izendatu | Egoera batean egokiena aukeratu | Arriskuak eta abantailak azaldu |

| EEE egin | Zer den jakin | Galdera-bloke bat bete | EEE osoa sistema errealean egin |

| Terminoa | Definizioa |

| AEPD | Datuak Babesteko Espainiako Agentzia (izen ofiziala: Agencia Española de Protección de Datos). GDPR betetzea Espainian gainbegiratzen duen erakunde publiko independentea. |

| AESIA | Adimen Artifizialaren Gainbegiraketarako Espainiako Agentzia (izen ofiziala: Agencia Española de Supervisión de la Inteligencia Artificial). AI Act-en betetzea Espainian gainbegiratzen duen erakundea; Europako lehen agentzia mota honetan. |

| AI Act | EB 2024/1689 Erregelamendua, AAren Europako lege nagusia. |

| Arrisku altua | AI Act-en hirugarren maila — lan-aukera, hauteskunde, justizia, mediku-diagnostiko bezalako sistemak. |

| Arrisku ezinezkoa | AI Act-en goren maila — debekatutako praktikak (puntuazio sozial, manipulazio, espazio publikoan biometria). |

| DPA | Data Processing Agreement — datu-tratamenduaren akordioa hornitzaile eta enpresaren artean. |

| DPIA / EIPD | Data Protection Impact Assessment / Datu Babesaren Eraginaren Ebaluazioa. GDPR 35. art.-en arabera derrigorrezko ebaluazioa arrisku altuko tratamenduetarako. |

| EEE | Eragin Etikoko Ebaluazioa. Praktika gomendatua AA sistema baten eragin sozial eta etikoa neurtzeko. |

| GDPR / RGPD / DBEO | General Data Protection Regulation / Reglamento General de Protección de Datos / Datuak Babesteko Erregelamendu Orokorra. EB 2016/679. |

| GPAI | General-Purpose AI. Helburu orokorreko AA ereduak (ChatGPT, Claude, Gemini bezalakoak). |

| HIC | Human-in-Command. Pertsonek erabateko agintea AA sistemaren gainean. |

| HITL | Human-in-the-Loop. Pertsonak erabaki bakoitzean parte hartzen du. |

| HOTL | Human-on-the-Loop. Pertsonak gainbegiratzen du baina ez du erabaki bakoitzean parte hartzen. |

| LOPDGDD | Ley Orgánica 3/2018 de Protección de Datos Personales y garantía de los derechos digitales — Datu Pertsonalak Babesteko eta Eskubide Digitalak Bermatzeko Lege Organikoa. GDPR-aren Espainiako egokitzapena. |

| NMS | Erabaki automatizatu oro; GDPR 22. art.-en bidez arautua. |

| Sandbox erregulatzailea | Probatzeko ingurune kontrolatu eta segurua, AA berriak merkatura sartu aurretik araudia betetzen dutela egiaztatzeko. |

| XAI | Explainable AI — AA azalgarria; erabakiak azaltzen dituen AA. |

| Langileen Estatutua (ET) | Estatuto de los Trabajadores (izen ofiziala). Espainiako lan-harremanen oinarrizko legea; 64.4.d art.-ek algoritmoen gardentasun-betebeharra ezartzen die enpresei langile-ordezkarien aurrean. |

| Zehaztasun vs Azalgarritasun | Bi balio aurkari: eredu zehatzenak askotan kutxa beltzak dira; azalgarritasunak ehuneko gutxi sakrifikatu dezake zehaztasunean. |
