# IE1 — Sarrera: ariketa eta eztabaida

> **Erantzun-eredua, 2026-09-24.** Gelako taldeak bere sektorea eta iritziak aukeratu behar ditu; beheko adibideak ez du ikasleen lana ordezten. 5., 21., 23. eta 24. diapositibetako jarduerei dagokie. Ez da beste jarduerarik gehitu.

## 1. AAren historian kokatzea — 5. diapositiba

Diapositibak 1956ko Dartmouth, «negu artifizialak», 2012ko ikaskuntza sakona eta 2022ko AA sortzailea aipatzen ditu, eta Deep Blue, AlphaGo eta ChatGPT tartean kokatzea eskatzen du. Lerro hau **irakaskuntza-laburpena** da, ez AAren historia osoa edo etapa zehatz eta unibertsalki adostuen zerrenda.

| Urtea | Gertaera | Ikasgairako lotura |
|---|---|---|
| 1997 | IBMren Deep Blue-k Garry Kasparov egungo munduko xake-txapelduna garaitu zuen sei partidako neurketan. | Bilaketa eta xake-posizioen ebaluazio konputazional bizkorra. |
| 2016 | DeepMind-en AlphaGo-k Lee Sedol garaitu zuen 4–1, Go partida-seriean. | Sare neuronal sakonak eta bilaketa konbinatzen dituen sistema. |
| 2022-11-30 | OpenAI-k ChatGPT aurkeztu zuen ikerketa-aurrebista gisa. | Elkarrizketan erabiltzeko AA sortzailea; diapositibaren 2022ko mugarriari dagokio. |

Hiru mugarriak hurrenkera kronologikoan: **Deep Blue (1997) → AlphaGo (2016) → ChatGPT (2022)**. Ez dute AA eredu bera adierazten: xakeko sistema espezializatua, Go-rako sare neuronalak eta bilaketa erabiltzen dituen sistema, eta elkarrizketarako hizkuntza-eredua dira, hurrenez hurren.

Iturri ofizialak, kontsulta-data: 2026-09-24: [IBM — Deep Blue](https://www.ibm.com/history/deep-blue); [Google DeepMind — AlphaGo](https://deepmind.google/research/alphago/); [OpenAI — Introducing ChatGPT](https://openai.com/index/chatgpt/).

## 2. Inferentzia-zuhaitza — 21. diapositiba

Diapositibak adibide hau ematen du: «motorra ez da pizten» → bateria? → «argiak pizten dira?». Honako zuhaitza adibide hori galdera kateatu bihurtzeko erantzun-eredua da; adar bakoitza ez da matxuraren ziurtasun-diagnostikoa.

```text
Motorra ez da pizten
└─ Erregai-usain handia?
   ├─ bai → Ez piztu; eten eta laguntza eskatu
   └─ ez → Arbel/argiak pizten dira?
      ├─ ez → Elikadura edo bateria aztertu
      └─ bai → Argiak ahul daude?
         ├─ bai → Bateria aztertu
         └─ ez (normal) → Klik-hotsa dago?
            ├─ bai → Abiagailua/konexioa aztertu
            └─ ez → Erregai-neurgailuak hutsik markatzen du?
               ├─ bai → Erregaia egiaztatu
               └─ ez → Immobilizadorearen argia keinuka?
                  ├─ bai → Giltza/immobilizadore-sistema aztertu
                  └─ ez → Pizte- edo erregai-sistema aztertu
```

Adarrak eskuz jarraitzeko, erantzun ezezagunak ez dira «ez» gisa hartzen: galdera egin edo «ondoriorik ez» adarrean geratu. Usaina edo erregai-ihesa sumatuz gero, segurtasun-ekintza lehenesten da, ez diagnostiko-saioa.

## 3. Paperean exekutatzeko sistema aditua — 23. diapositiba

Diapositibako eskakizuna betetzeko, hemen sektore-adibide bat dago: **pizten ez den auto baten hasierako diagnostikoa**. Sistema didaktikoa da, ez ibilgailuak konpontzeko jarraibide profesionala.

### Ezagutza-basea: 9 IF–THEN erregela

Gertaera bakoitzak hiru egoera izan ditzake: egia, gezurra edo ezezaguna. «Ez dakigu» ez da «gezurra».

| ID | IF — baldintza guztiak | THEN — ondorioa |
|---|---|---|
| R1 | Erregai-usain handia edo ihesa antzematen da | Ez saiatu motorra pizten; urrundu eta laguntza eskatu (segurtasun-geldialdia). |
| R2 | Motorra ez da pizten eta argiak ez dira pizten | Elikadura elektrikoa/bateria aztertu. |
| R3 | Motorra ez da pizten eta argiak ahul daude | Bateria ahula izan daiteke; bateria/terminalak egiaztatu. |
| R4 | Motorra ez da pizten, argiak normal daude eta klik azkarrak entzuten dira | Bateria-konexioa edo abiagailua aztertu. |
| R5 | Motorra ez da pizten, argiak normal daude eta klik bakarra entzuten da | Abiagailua edo solenoidea aztertu. |
| R6 | Motorra ez da pizten, argiak normal daude, klikik ez dago eta erregai-neurgailuak hutsik dio | Erregai-maila egiaztatu eta, behar bada, hornitu. |
| R7 | Motorra ez da pizten, argiak normal daude, klikik ez dago, erregaia badago eta immobilizadorearen argia keinuka dago | Giltza/immobilizadorearen sistema aztertu. |
| R8 | Motorra ez da pizten, argiak normal daude, klikik ez dago, erregaia badago eta immobilizadorearen argia ez dago piztuta | Pizte- edo erregai-sistemaren azterketa eskatu. |
| R9 | R2 edo R3k bateria/elikadura egiaztatzea ondorioztatu du | Neurtu bateria eta begiratu konexioak; ez ordezkatu pieza proba egin gabe. |

### Lehentasuna eta gatazka-konponbidea

1. R1 segurtasun-araua da eta beti gailentzen da: aktibatuz gero, diagnostikoa gelditu eta ez da beste jarduera arriskutsurik gomendatzen.
2. Segurtasun-arauak aktibatu ezean, egiaztatu gainerako arauak eta aktibatu baldintzak betetzen dituztenak; ondorio berriak gehitu, eta errepikatu ondorio berririk ez dagoen arte (aurreranzko kateatzea). Baldintza zehatzagoa duen arauak lehenesten du baldintza orokorrago baten aurrean.
3. Zehaztasun bera badute, ID txikiena lehenesten da. Araua behin bakarrik exekutatzen da; ondorio bera berriro ez gehitzeko.
4. Kontraesanezko sarrerak edo sarrera ezezagunak badaude, ez asmatu: emaitza «ezin da ondorioztatu» da, eta falta den galdera egin behar da.

Kasu honetan R2 eta R3 elkarren baztertzaile dira (`argiak ez dira pizten` vs `ahul daude`); R4–R5–R6–R7–R8 adarretan klik-mota eta baldintzak bereizten dira. R9k R2/R3ren ondorioa findu egiten du, ez du haren aurka egiten.

### Eskuzko exekuzioaren adibidea

Hasierako gertakariak: (1) motorra ez da pizten; (2) argiak ahul daude; (3) ez da erregai-usainik edo ihesik antzeman; (4) argien egoera «ahul» da, beraz ez da «itzalita»; (5) ez dago klik azkarrari edo bakarrari buruzko daturik.

1. R1: ez da betetzen, ez baita erregai-usainik/ihesik jakinarazi.
2. R2: ez da betetzen; argiak ez daude itzalita, ahul baizik.
3. R3: betetzen da → **bateria ahula izan daiteke; bateria/terminalak egiaztatu** ondorioa gehitzen da.
4. R9: R3k elikadura egiaztatzea ondorioztatu duenez, betetzen da → **bateria neurtu eta konexioak begiratu; ez ordezkatu proba egin gabe**.
5. R4–R8: ez dira ebaluazio honetan aplikatzen, argiak normal daudelako baldintza faltsua baita; ez dira klik, erregai-neurgailu edo immobilizadoreari buruzko datuak asmatzen.

Azken emaitza: **bateria/terminalak egiaztatzea lehen urrats arrazoitua da; ez da behin betiko diagnostikoa**. Eskuzko exekuzioan bi erregela aktibatu dira (R3 eta R9).

### Noiz ez dira nahikoak erregelak? — 5072rako sarrera

Erregelak erabilgarriak dira adituek baldintza argi eta nahiko egonkorrak eman ditzaketenean, baina ez dute berez huts egindako sentsorea antzematen, salbuespen guztiak estaltzen edo egoera berrietara ikasten. Sintoma konbinazio asko, neurketa zaratatsuak edo ezagutzen ez diren matxurak badaude, datu adierazgarriak dituen ikaskuntza automatikoko eredua azter liteke. Eredu horrek ere baliozkotzea, azalpena eta gizakiaren egiaztapena behar ditu; ez da automatikoki arauen ordezko segurua.

## 4. MYCINen ardura — 24. diapositiba

> **Eztabaidarako erantzun-ereduak dira; ez dira taldearen iritzi bakarra edo lege-irizpena.** Diapositibak MYCINen historia eta «nork erantzun behar du» galdera planteatzen ditu, eta bi galdera hauek eztabaidatzea eskatzen du.

### «Medikuak baino hobea den sistema erabiliko zenukete? Zergatik (ez)?»

Erabiltzea aztertuko nuke, baina ez diagnostiko autonomo gisa eta ez «testetan hobea» izatea nahikoa delako. Lehenik, zein paziente-talderi, zein egoeratan eta zer emaitza neurtu den argitu behar da; ondoren, erabilera aurreikusian kanpo-baliozkotzea, kalte-arriskuak, hutsegite motak, datu-aldaketekiko sendotasuna eta alternatibak ebaluatu. Proba mugatu eta kontrolatu batean, medikuak gomendioa berrikusi eta bazter dezake, eta sistemarik ezean ere arreta emateko bidea egon behar da. Ebidentzia nahikorik edo ikuskapen eraginkorrik gabe, ez nuke pazientearen tratamendu-erabakiaren ordez erabiliko.

Kontrako argudio arrazoizkoa da proba on batek espezialistaren hutsune batzuk estal ditzakeela eta, segurtasun-neurriak badaude, laguntza-tresna gisa baliagarria izan daitekeela. Eztabaidak errendimenduaren eta erabilera-baldintzen ebidentzia eskatu behar du; diapositibako «testetan hobea» esaldia ez da nahikoa ondorio kliniko orokor bat ateratzeko.

### «Nork erantzun behar du sistema batek huts egiten duenean: garatzaileak, medikuak, ospitaleak?»

Erantzukizuna ez litzateke automatikoki pertsona edo erakunde bakar bati egotzi behar. **Garatzaileak** diseinu, entrenamendu/arau, dokumentazio, abisu eta ezagutzen diren akatsen berri emateaz erantzun beharko luke; **osasun-profesionalak** bere eskumenaren barruan gomendioa kritikoki aztertu eta pazientearen testuingurua kontuan hartzeaz; **ospitaleak** hautaketa, integrazioa, langileen prestakuntza, erabilera-protokoloa, gainbegiratzea eta intzidenteen kudeaketaz. Ebidentziak erakuts lezake ekarpena dutela hainbat aldeek, edo baten batek ez duela dagokion zeregina bete.

Benetako erantzukizun juridikoa ez da etikako eztabaida honetatik bakarrik erabakitzen: jurisdikzioaren lege aplikagarria, kontratuak, sistemaren xedea, kaltea, erabakiaren kontrola eta froga zehatzak aztertu behar dira. Horregatik, erantzun eredu orekatuak ardura operatiboak banatzen ditu, baina ez du aldez aurretik erantzukizun juridikoaren emaitza adierazten.
