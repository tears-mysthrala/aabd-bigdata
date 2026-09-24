# IE6 · Proiektu integratzailea

## Ikasleentzako laguntza goiztiarra iragartzeko sistema baten ebaluazio teknikoa

**Adibide didaktiko fikziozkoa.** Txosten honek ez du benetako ikastetxe baten tratamendua aztertzen, ez du lege-aholkularitza ematen eta ez du araudia betetzen dela ziurtatzen. Erakunde, rol eta sistema guztiak hipotetikoak dira. Tokiko lege-oinarria, kontratuak, datu-fluxuak eta AI Acteko sailkapena benetako proiektu batean egiaztatu beharko lirateke, datuak erabili edo sistema erosi aurretik.

**Kontsulta-data:** 2026-09-24.
**Hartzaileak:** fikziozko ikastetxeko zuzendaritza eta proiektuko arduradunak.
**Erabaki-esparrua:** aukera tekniko eta antolakuntzazkoak aztertu; ez ezarri sistema automatikoki.

## Laburpen exekutiboa

Tokiko ikastetxe publiko hipotetiko batek ikasleei laguntza pedagogikoa garaiz eskaintzeko tresna aztertzen du. Tresnak aurreko noten joerak eta asistentzia-datu mugatuak erabil ditzake, hurrengo ikasturteko laguntza-premiaren adierazle bat kalkulatu eta behin-behineko ikasketa-talde baten proposamena egin. Irakasle kualifikatuak ikaslearekin hitz egin, beste ebidentzia batzuk aztertu eta erabaki guztiak hartuko lituzke. Puntuazioak ez luke nota, matrikula, mailaz igotzea, diziplina, zerbitzuetarako sarbidea edo laguntza jasotzeko eskubidea erabakiko.

**Gomendioa: aldatu eta baldintzapean berriz ebaluatu.** Oraingoz ez erosi, ez aktibatu eta ez egin ikasleen datuekin piloturik. Lehenik eskuzko laguntza-prozesua eta haren emaitzak deskribatu, erabilera-helburua eta lege-oinarria egiaztatu, beharrezkoak ez diren datuak baztertu, datu-fluxu osoa eta hornitzailearen eginkizunak argitu, eta GDPRko EIPD behar den erabaki. Xedeak ikasleen ikaskuntza-emaitzak ebaluatu edo ikasketa-prozesua bideratzen badu, AI Acteko III. eranskineko hezkuntza-erabileragatik arrisku handikoa dela hartu behar da hasierako lan-hipotesitzat. Sailkapen zehatza xede eta erabilera errealaren arabera dokumentatuko da. Ez da AI Acteko arrisku-sailkapena GDPRko lege-oinarriaren ordezkoa.[1][2][6]

Arriskurik handienak honako hauek dira: ereduak ikasle ahulak gaizki sailkatzea; ordezko adierazleek pobrezia, desgaitasuna edo hizkuntza-beharrak zeharka kodetzea; irakasleek puntuazioan gehiegi fidatzea; etiketa batek ikaslearen autoirudia eta aukerak kaltetzea; eta hornitzaileak datuak helburu berrietarako erabiltzea. Arrisku horiek ez dira ohar batekin konpontzen. Datu-minimizazioa, giza berrikuspen erreala, taldeka egindako errore-azterketa, kexa-bidea, mugatutako atxikipena eta gelditzeko ahalmena behar dira.[1][2]

Pilotua soilik planteatu liteke proiektuko kontrol guztiak aurrez bete, dokumentatu eta zuzendaritzak onartu ondoren; hala ere, txosten honek ez du pilotu baimenik ematen. Proba tekniko bat egiteko nahikoa izan daiteke datu sintetiko edo behar bezala anonimizatuak erabiltzea. Ikasleen datu pertsonalekin proba egiteak tratamendu juridiko osoa eskatuko luke.

## 1. Proiektuaren deskribapena eta mugak

### 1.1 Hipotesi operatiboak

| Elementua | Proiektuko hipotesia | Egiaztatu beharrekoa erabilera errealean |
|---|---|---|
| Erakundea | Tokiko ikastetxe publiko bat | Zein administraziok kudeatzen duen eta zein hezkuntza-eskumen dituen |
| Xedea | Laguntza pedagogikoa garaiz eskaintzeko seinale bat ematea | Xedea hezkuntza-lege eta eskumenekin bateragarria den |
| Erabiltzaileak | Baimendutako irakasleak eta laguntza-taldea | Sarbide-zerrenda, baimenak eta trebakuntza |
| Pertsonak | Ikasle adingabeak izan daitezke | Adina, ordezkaritza eta ikasleen informazio irisgarria |
| Sarrerak | Ikasturteko kalifikazio agregatuak eta asistentzia-kopuruak | Iturria, zuzentasuna, beharrezkotasuna, datu berezien presentzia |
| Irteera | Laguntza-premia aztertzeko seinale eta talde-proposamen malgua | Ereduaren logika, ziurgabetasuna eta benetako eragina |
| Giza rola | Irakasleak banaka berrikusi eta erabakitzen du | Benetako denbora, informazioa, trebakuntza eta veto-ahalmena |
| Hornitzailea | Kanpoko software-hornitzaile hipotetikoa | Arduradun/prozesadore rola, azpi-prozesadoreak, ostatua, transferentziak |
| Emaitza | Laguntza-eskaintza edo elkarrizketa pedagogikoa | Ez erabiltzea kalifikazio, sarbide, zigorr edo baliabide ukapenerako |

Tresnak ez luke ikasleen nortasuna, emozioa, etxeko ingurunea edo aurpegi/ahotsa aztertuko. Ez luke gurasoen enplegua, herritartasuna edo liburutegi-erabilera baliatuko. Talde-proposamena behin-behinekoa, laburra eta berrikusgarria izango litzateke, eta ikasleak laguntza jasotzeko aukera mantenduko luke puntuazioa edozein izanik ere.

### 1.2 Sistemaren bizi-zikloa

1. Ikastetxeak laguntza-prozesua eta arazo pedagogikoa definitzen ditu, eredua erosi aurretik.
2. Datuen arduradunek iturri eta eremu bakoitzaren jatorria, zuzentasuna eta erabilera-baimena egiaztatzen dituzte.
3. Hornitzaileak, hala badagokio, datuak prozesatzen ditu kontratuan eta argibide idatzietan jasotako xederako soilik.
4. Sistemak laguntza-seinale bat sortzen du, azaldu beharreko muga eta ziurgabetasunekin.
5. Irakasleak datuak eta testuingurua berrikusten ditu, ikasleari entzuten dio, eta gomendioa onartu, aldatu edo baztertzen du.
6. Ikastetxeak eskaintza, jarraipenaren epea eta berrikuspena dokumentatzen ditu, behar adinako datuekin soilik.
7. Akats, desberdintasun edo kexa batek berrikuspena edo erabilera etetea eragin dezake.

### 1.3 Irismenetik kanpo

Txosten honek ez du eredu komertzial jakin bat, zehaztasun-maila, prezio, benetako datu multzo edo emaitza estatistikorik suposatzen. Ez dago egiaztatutako errendimendu-daturik, taldeko errorerik edo hornitzaile-kontraturik. Beraz, ez dira asmatuko. Ez da ereduaren baliozkotze teknikorik egin, ez da ikasleen daturik eskuratu, ez da erakunde erreal baten legezko oinarria ebaluatu, eta ez da DPOaren edo lege-aholkulariaren iritzirik ordezkatzen.

## 2. GDPR azterketa

GDPR 5. artikuluko zazpi printzipioek diseinua gidatzen dute; 6. artikuluko lege-oinarriak benetako hezkuntza-eginkizun eta lege aplikagarriarekin bat etorri behar du. Ikastetxe publikoa izateak ez du lege-oinarria automatikoki ebazten. Azterketa hau diseinu-hipotesia da, eta ez erabilera hasteko baimena.[1]

### 2.1 Arduraduna, prozesadorea eta datu-fluxua

Ikastetxea edo dagokion administrazio publikoa izango litzateke, printzipioz, helburua eta funtsezko bitartekoak zehazten dituen tratamenduaren arduraduna. Hornitzaileak ikastetxearen argibideen arabera jarduten badu, GDPR 28. artikuluko prozesadore izan liteke. Hornitzaileak bere helburuetarako erabiltzen baditu datuak edo funtsezko helburuak baterako erabakitzen baditu, rola berriz aztertu behar da. Kontratu batek ezin du benetako rola izendapen bidez aldatu.[1]

Prozesuaren hasieran datu-fluxu-diagrama egin behar da: ikaslearen erregistro-sistema, asistentzia-iturria, prestaketa/konbinazioa, eredua, erabiltzaile-interfazea, txostenak, esportazioak, hornitzailearen euskarria eta ezabaketa. Fluxu horretan jaso beharko dira datu bakoitzaren hartzailea, biltegiratzea, kokapen geografikoa, transferentzia, kopia eta atxikipen-epea. Sistemak lineaz kanpo edo hodeian lan egiteak ez ditu printzipio horiek aldatzen.

### 2.2 Legezkotasuna, leialtasuna eta gardentasuna

Ikastetxe publiko batek bere hezkuntza-eginkizunaren barruan eta legeak emandako eskumenaren arabera tratatzen baditu datuak, GDPR 6(1)(e) artikuluko interes publikoko eginkizuna aukera izan liteke. Hori ezin da suposatu: eskumen eta arau zehatza, tratamenduaren beharrezkotasuna eta proportzionaltasuna identifikatu behar dira. Ikasleari aukera-berdintasuna edo zerbitzu bat galtzeko arriskua sortzen duen egoeran, adostasuna ez da automatikoki libreki emandakotzat hartuko. Ikastetxe publikoak ezin du 6(1)(f) artikuluko interes legitimoa bere eginkizun publikoaren tratamenduetarako oinarri orokor gisa hartu.[1]

GDPR 13–14. artikuluetako informazioak helburua, datu-kategoriak, oinarria, hartzaileak, atxikipena, eskubideak eta erabilgarri denean automatizazioaren inguruko informazioa estali behar ditu. Ikasleentzat eta, dagokionean, legezko ordezkarientzat ulergarria izango da. Gardentasun-orriaren zirriborroak helburu bera erabiltzen du, baina benetako ikastetxeak bere kontaktuak, arau-oinarria eta epeak jarri beharko lituzke.[1]

### 2.3 Helburua mugatzea eta datu-minimizazioa

Helburua estua da: ikaslearekin elkarrizketa edo laguntza pedagogiko egokia aztertzea. Helburua ez da ikasleak sailkatzea, diziplina-neurriak hartzea, ikasleen maila edo etorkizun profesionala finkatzea, irakaslea ebaluatzea, edo publizitate/produktu-garapenerako datuak ematea. Bigarren erabilera bakoitzak bateragarritasuna, lege-oinarria, gardentasuna eta, beharrezkoa bada, beste inpaktu-ebaluazio bat eskatzen ditu.[1]

Hasierako datu-proposamena txikia da. Kalifikazio guztiak, asistentzia-historia osoa edo familia-datuak hartu beharrean, ikastetxeak justifikatu behar du zein adierazle agregatu den beharrezkoa eta zergatik. Datu gordinak gordetzeak ez du esan nahi ereduak erabili behar dituenik. Herritartasuna, gurasoen enplegua, liburutegiaren erabilera, diziplina-oharrak, osasun-informazioa eta portaera digitalaren jarraipena kanpoan uzten dira. Desgaitasunari, osasunari edo bestelako GDPR 9. artikuluko kategoria bereziei buruzko daturik balego, proiektuaren diseinua berriz aztertu behar da, eta 9. artikuluko salbuespen egoki bat egon beharko litzateke.[1]

| Datu edo aktibo mota | Hasierako tratamendua | Beharrezko kontrola |
|---|---|---|
| Ikaslearen identifikatzailea | Pseudonimoa erabili ahal bada analisi-fasean | Lotura-gakoa bananduta eta sarbide murriztua |
| Ikasturteko kalifikazio agregatuak | Erabili beharrezkotasuna frogatuz gero | Iturri, data, hutsune eta zuzenketa kontrolatu |
| Asistentzia-neurri agregatua | Erabili testuinguruan eta proportzionalki | Justifikatutako/justifikatu gabeko absentziak nahastu ez |
| Talde-proposamena eta seinalea | Baimendutako langileek soilik ikus dezakete | Ez gehitu ikasle-espediente iraunkorrari beharrik gabe |
| Irakaslearen berrikuspena | Erabakiari lotutako gutxieneko oharra | Giza arrazoiak eta ikaslearen ikuspegia erregistratu |
| Auditoretza-erregistroa | Sarbide, erabaki, zuzenketa eta bertsioaren metadatuak | Edukia minimizatu, epea ezarri eta osotasuna babestu |

### 2.4 Zehaztasuna, gordetzea eta segurtasuna

Ikastetxeak iturri bakoitzaren eguneratze-data eta eremuaren esanahia ezagutuko lituzke. Ikasleek edo ordezkariek okerreko asistentzia edo nota zuzentzeko bide erraza behar dute. Justifikatutako absentzia, datu-hutsunea edo irakasle-aldaketa ezin dira automatikoki gaitasun edo ahalegin eskas gisa interpretatu. Seinalea probabilitate edo jarduteko proposamen gisa aurkeztuko da, eta datuetan oinarritzen den azalpen laburra izango du; ez da egia objektibo gisa erakutsiko.[1]

Atxikipen-epea helburu eta eskola-egutegiaren arabera zehaztuko da: datu operatiboak laguntza erabaki eta jarraitzeko behar diren bitartean baino ez; auditoretza-arrastoak berriz, froga eta kontu-ematearen beharra betetzeko gutxieneko epe justifikatuan. Epe zehatzik ez dagoenez, ez da hilabete-kopururik asmatuko. Proiektua gelditzean, hornitzailearen kopiak, babeskopiak eta esportazioak ere ezabatzeko edo anonimatzeko plana beharko da. Artxibo publikoen arau bereiziak aplikatzen badira, dokumentatu beharko dira.[1]

Segurtasun-kontrolak: erabiltzaile bakoitzaren identitatea, rol bakoitzeko gutxieneko baimena, autentifikazio sendoa, garraioan eta biltegian zifratzea, segurtasun-eguneraketak, erregistroen osotasuna, segurtasun-kopien babesa, hornitzailearen urruneko sarbide mugatua eta kontratu bidezko ezabatzea. Ez lirateke puntuazioak ikasle edo guraso guztiei ikusgai jarriko. Erabiltzaile-interfazeak laguntza-egoera eta beharrezko hurrengo urratsa baino ez lituzke erakutsiko.

### 2.5 Erantzukizun proaktiboa eta datu-babesaren diseinua

Arduradunak betetzea frogatzeko erregistroak, helburuak, datu-fluxua, oinarri juridikoa, prozesadore-kontratua, segurtasun-neurriak, informazio-orriak, eskubideak kudeatzeko prozesua eta aldaketen kontrola dokumentatuko lituzke. Datu-babeserako ordezkaria badago edo GDPR 37. artikuluak eskatzen badu, hasieratik kontsultatu behar da. Erosketa-erabakiak ez luke hornitzailearen marketin-adierazpen hutsean oinarritu behar.[1]

GDPR 35. artikuluko EIPD egin behar da tratamenduak, bereziki teknologia berriak erabiltzeagatik, pertsona fisikoen eskubide eta askatasunetarako arrisku handia sor badezake. Ikasle adingabeen ebaluazio sistematikoa, datu-puntu anitzen lotura eta laguntza/ikasketa aukeretan eragina izatea arrisku handiko adierazleak dira. Beraz, kasu honetan EIPDren beharra baheketa formal batez dokumentatu behar da; datu errealak tratatu aurretik EIPD osoa egitea aurreikusten da, salbu eta ebaluazio arrazoituak bestela frogatzen badu. Arrisku handiak kontrol gehigarriekin ere ezin badu jarraitu, GDPR 36. artikuluko aurretiazko kontsultaren beharra aztertu behar da. EEE etikoak ez du EIPD ordezkatzen.[1][6]

## 3. Azalpena, eskubideak eta giza erabakia

Ikastetxeak azaldu behar du zertarako erabiltzen den seinalea, zein datu motari erreparatzen dion, irakasleak zer egin behar duen eta zer erabakitzen ez duen. Ikasleak ulertu behar du seinaleak elkarrizketa bat abiaraz dezakeela baina ez duela bere ahalmena, nota edo etorkizuna definitzen. Erabilera errealaren arabera, GDPR 13(2)(f), 14(2)(g) eta 15(1)(h) artikuluetako informazio automatizatuaren eskakizunak berrikusi behar dira.[1]

GDPR 22. artikulua erabaki bat soilik tratamendu automatizatuan oinarritzen denean eta ondorio juridikoak edo antzeko garrantzi handiko ondorioak dituenean aztertu behar da. Langile batek puntuazioa onartu besterik ez badu egiten, itxurazko esku-hartzeak ez du erabakia benetan giza bihurtzen. Ikaslearekin elkarrizketa, datu-iturriak egiaztatzea, bestelako testuingurua kontuan hartzea eta gomendioa baztertzeko benetako ahalmena dira erabakiaren giza izaera erakusteko kontrolak. Puntuazioa eskola-baliabidea edo talde baterako aukera esanguratsua erabakitzeko erabiltzen bada, Article 22ren aplikagarritasuna eta oinarri/berme salbuespenak berriz aztertu behar dira.[1]

AI Act 86. artikuluko azalpen-eskubidea ez da AI sistema guztien eskubide orokorra. III. eranskineko arrisku handiko sistemaren irteeran oinarrituta deployer-ak hartutako erabaki batek pertsona baten eskubide edo antzeko garrantzi handiko ondorioetan eragina badu, artikuluak ematen dituen baldintza eta mugen arabera azalpen argi eta esanguratsua eska daiteke. Proiektuak arrisku handiko sailkapen-hipotesia duelako, ikasleari emango zaion azalpen-prozesua diseinatzen da, baina ez zaio bermatzen legeak ematen ez duen eskubide-mailarik.[2]

### Eskubide-eskaerak kudeatzeko bidea

1. Eskaera ikasleak, ordezkariak edo baimendutako pertsonak aurkezten du kanal ulergarri eta irisgarri batean.
2. Ikastetxeak identitatea modu proportzionalean egiaztatzen du; ez du beharrezkoa ez den dokumentazio sentikorrik eskatzen.
3. Datuen arduradunak eskaera mota sailkatzen du: sarbidea, zuzenketa, ezabaketa, tratamenduaren murrizketa, aurkaratzea, azalpena edo giza berrikuspena.
4. Datuen iturria, dagokion bertsioa eta giza erabakiaren oinarriak berreskuratzen dira.
5. Irakasle egoki batek ikaslearen azalpena entzun eta gomendioa berrikusten du; berrikusleak ez du aurreko erabakia itsu-itsuan berresten.
6. Ikastetxeak epe juridiko aplikagarria betetzen du, erantzuna modu ulergarrian ematen du eta erabilitako datuak zuzendu edo erabakia aldatzen badu, hori erregistratzen du.
7. Pertsonak erantzunarekin ados ez badago, barneko eskalatze-bidea eta datu-babeserako agintaritzara jotzeko eskubidearen informazioa jasotzen du, aplikagarri den neurrian.[1]

## 4. AI Acteko sailkapena eta rolak

Sailkapenaren abiapuntua erabilera-helburua da, ez ereduaren tamaina edo etiketa komertziala. AI Acteko III. eranskinak 3(b) puntuan hezkuntzarako eta lanbide-heziketarako erabiltzen diren sistema jakin batzuk arrisku handiko gisa jasotzen ditu: ikaskuntza-emaitzak ebaluatzea, ikaskuntza-prozesua zuzentzea, edo hezkuntza-maila egokia ebaluatzea, adibidez. Irizpide zehatza sistemaren intended purpose eta erabilera errealean aplikatzen da.[2]

Ikasle baten errendimendua aurresan eta ikasle-taldea proposatzeko tresnak ikaskuntza-emaitzen ebaluazio edo ikaskuntza-prozesua bideratzeko funtzioa bete lezake. Horregatik, **hasierako kontserbaziozko hipotesia: arrisku handiko sistema, III. eranskineko hezkuntza-kategoria dela eta**, salbu eta eskumen juridiko egokiak dokumentatutako sailkapen-azterketak erakusten badu erabilera ez dela zerrendatutako kasua edo 6. artikuluko salbuespen bat osorik betetzen duela. Salbuespenak ez dira erosleak automatikoki aplika ditzakeen aringarriak; erabilera, eragin-maila eta baldintza juridiko guztiak egiaztatu behar dira. Hartutako ondorioa eta arrazoia idatziz utziko dira.[2]

Arrisku handiko hipotesiak hornitzaileari eta deployer-ari dagozkien betebeharrak identifikatzea eskatzen du. Hornitzaileak, dagokionean, arrisku-kudeaketa, datu-gobernantza, dokumentazio teknikoa, erregistro-gaitasuna, argibideak, zehaztasun/robustotasun/zibersegurtasunaren kontrolak eta adostasun-ebaluazioa egin behar ditu. Deployerrak erabilera argibideen barruan egin, giza gainbegiratzea antolatu, monitorizatu, erregistro esanguratsuak gorde, datuen sarrerako kontrola egin eta gertakari edo arriskuak behar bezala eskalatu behar ditu. Betebehar zehatzak rolaren, sistemaren kategoriaren, aplikazio-dataren eta 2026/1744 aldaketaren araberakoak dira.[2][3][7]

AI Acteko 14. artikuluak arrisku handiko sistemetarako giza gainbegiratzea aurreikusten du. Langileak output-a interpretatzeko gaitasuna, erabilera-mugak ezagutzea eta sistema baztertzeko, eteteko edo esku-hartzea eskatzeko aginpidea izan behar ditu. Proiektu honetan HITL aukeratzen da laguntza erabakitzeko puntu bakoitzean. HOTL egokia litzateke seinaleen jarraipen operatiboan, baina ezin du ordezkatu kasu zehatzaren berrikuspena. HICk erabaki instituzionala giza arduradunari uzten dio eta sistemaren irteera informazio lagungarri hutsa da.[2]

AI Acteko 113. artikuluaren egutegia kontuan hartu behar da. Task 2 iturri-erregistroak 2026/1744 Erregelamenduaren ondorengo testu ofiziala jasotzen du: III. eranskineko sistemetan III. kapituluko 1–3 atalak 2027-12-02tik aplikatuko dira, eta I. eranskineko produktu-sistemetan dagokion atzeratutako data 2028-08-02 da. Horrek ez du AI Act osoa data horietara arte atzeratzen eta ez du GDPRren aplikazioa aldatzen. Erakundeak erosketa edo erabilera bakoitzean data indarrean dagoen testuarekin berriro egiaztatuko du.[2][3][7]

### Hornitzaileari egin beharreko galderak

- Zein da sistemaren intended purpose idatzia? Zein hezkuntza-erabaki laguntzen ditu, eta zein ez ditu egin behar?
- Zein III. eranskineko puntu eta 6. artikuluko irizpideren arabera sailkatu da? Eman arrazoia eta adostasun-ebaluazioaren dokumentazioa.[2]
- Zer ezaugarri, datu eta etiketa erabili dira? Zein iturri, ordezkaritza, denboraldi eta hutsune dituzte datuek?
- Nola baliozkotu dira faltsu-negatiboak, faltsu-positiboak eta azpitaldeetako errendimendua? Zer gutxieneko lagin eta ziurgabetasun-tarte erabiltzen dira?
- Nola adierazten dira ziurgabetasuna, datu eskasa eta erabilera-eremuetatik kanpoko kasuak?
- Zer egin behar du irakasleak gomendioa desadosteko edo baztertzeko? Zer informazio behar du automatizazio-alborapena saihesteko?
- Zein datu mantentzen du hornitzaileak, non, zenbat denboraz eta zein azpi-prozesadorek prozesatzen dute? Nola ezabatzen dira kopiak eta segurtasun-kopiak?
- Erabiliko al ditu datuak eredu orokorra entrenatzeko, produktuaren analitika egiteko edo beste bezero batzuekin alderatzeko? Nola desgaitu eta egiaztatu erabilera hori?
- Nola jasoko ditugu segurtasun-gertakariak, eredu-aldaketak, eguneratzeak eta errendimenduaren narriadura? Zein zerbitzu-maila eta eten-prozedura dago?
- Zein dokumentu, proba, auditoretza-arrasto eta kontratu-berme eskainiko dizkio hornitzaileak ikastetxeari bere betebeharrak betetzeko?

## 5. Eragin etikoaren ebaluazioa (EEE)

EEE hau diseinu- eta eztabaida-tresna da, ez GDPRko EIPD. Eragin juridikoa, soziala eta hezkuntza-ondorioak bereizita aztertzen dira. Ebaluazioa behin-behinekoa da; ez da proba edo emaitza enpirikoen ordezkoa.

### 5.1 Proportzionaltasuna eta onura/kaltetzearen balantzea

Onura posiblea da ikasle batzuek behar duten laguntza lehenago jasotzea eta irakasleek seinaleak koherentzia handiagoz aztertzea. Onura hori frogatu gabe dago. Lehenik, AA gabeko oinarrizko prozesua deskribatu: irakasleen ohiko jarraipena, ikaslearen autoeskaera, tutoretza eta familiarekin elkarrizketa. Tresna batek ez luke arazo pedagogiko edo langile-gabezia sistemiko bat datu gehiago bilduz estali behar.

Kalte posibleak: ikasleari arrisku-etiketa jartzea, irakasleen itxaropenak jaistea, laguntzaren ordez kontrola handitzea, datu-erroreak ikaslearen aurka iraunaraztea, baliabideak seinalatutako ikasleengana gehiegi bideratzea edo seinalerik gabekoei laguntza ukatzea. Balantzeak ikasleen ahotsa eta irisgarritasuna jaso behar ditu. Seinaleak ez luke laguntza ukatzeko edo lehentasuna kentzeko balio behar. Talde-proposamena malgua izango da eta irakasleak ikaslearekin egiaztatuko du.

Proportzionaltasun-proba hauek gainditu behar dira: xedea legitimoa eta argia al da; AA gabeko alternatiba ez hain intrusibo batek xede bera lor al dezake; datu eta denbora-tarte bakoitza beharrezkoa al da; erabilera txikienean ere ikaslearen kaltea murrizten al da; emaitza eta akatsak berrikusteko baliabide nahikorik al dago? Galdera bati ezin bazaio ebidentzian oinarritutako erantzunik eman, aurrera ez egitea da aukera zuhurra.

### 5.2 Alborapenaren eta kalitatearen auditoretza

Lehenengo fasean ez da datu sentikor berririk bilduko. Eskuragarri dauden datu legitimoekin aztertu daiteke eredua norengan okertzen den, baina talde konparazioak ez dira egingo datu horiek legez eta etikoki erabiltzeko oinarririk, babesik eta nahikoa laginik gabe. Talde-adierazleak erabilgarri ez badaude, muga hori dokumentatu behar da eta arriskua ezin dela baztertu esan.

Azterketa-plana:

1. **Datuen jatorria:** epe, ikastetxe eta programa bakoitzeko estaldura; erregistro falta, kode-aldaketa eta onarpen/irteera-alborapena.
2. **Helburua eta etiketa:** zer da “laguntza behar izatea”; nork eta noiz erabaki zuen; irakasleek emandako zerbitzua eskuragarri zegoelako bakarrik agertzen al da etiketa.
3. **Errore motak:** faltsu-negatiboa, laguntza behar duen ikaslea ez seinalatzea; faltsu-positiboa, laguntza premia faltsuki seinalatzea. Biak ikaslearengan eta irakasleengan dituzten ondorioekin aztertu.
4. **Taldeka:** beharrezkoa eta baimendua bada, adin/ikasturte, hizkuntza, genero edo desgaitasunaren araberako akatsak konparatu, gutxieneko zelula-tamaina eta pribatutasuna babestuta.
5. **Egonkortasuna:** ikasturte, irakasle, ebaluazio-metodo edo eskolako egoera aldatzean errendimenduaren aldaketa neurtu.
6. **Giza konparazioa:** irakasle arruntaren bidearekin alderatu, irakasleek gomendioak noiz onartu edo baztertzen dituzten eta zergatik jasota.
7. **Ekintza:** onarpen-irizpideak aurrez zehaztu. Mugak gainditzen badira, sarrerako datu bat kendu, xedea estutu, eredua eten edo ohiko prozesura itzuli.

Ez da bidezkoa “zehaztasun orokorra” emaitza bakar gisa aurkeztea; klaseen desoreka ezkutatu lezake. Aurrez zehaztutako neurri eta mugak aditu independenteekin aukeratuko dira, hezkuntza-helburuarekin bat etorrita. Ez da parekotasun metriko bakarra onartuko ekitatearen definizio oso gisa. Zenbakiak ez dira argitaratuko benetako datu eta metodologia gabe.

### 5.3 Pribatutasuna eta eskubideak diseinuan

Atal honetako kontrolak hiru momentutan egiaztatuko dira: datuak iturritik ateratzean; hornitzaileari bidaltzean; eta emaitza irakaslearen pantailan agertzean. Datuak pseudonimizatzeak ez ditu datu pertsonal izateari uzten, berriz identifikatzeko aukera badago. Anonimizazio aldarrikapenak berridentifikazio-arriskua aztertuta egiaztatu behar dira. Datuen kopiak, erabiltzaileen esportazioak, cacheak eta laguntza-txartelak ere fluxuaren parte dira.[1]

Diseinu-erabaki nagusiak: datu gutxienekoak; aurrez zehaztutako xedea; ikasturteko epe mugatua; sarbide rol bidezkoa; kontrolatutako esportazioa; hornitzailearen erabilera sekundarioaren debekua; ikasleen informazioa plain language bidez; eta aztertzeko/zuzenketa eskatzeko kanal argia. Kexa aurkezteak ez dio ikasleari laguntza eskuratzea oztopatuko.

### 5.4 Erreklamazio eta erremedio mekanismoa

Ikasleak edo legezko ordezkariak puntuazioari edo proposamenari buruz galdetu, datu-errorea zuzendu edo giza berrikuspena eska dezake. Kexa hartzen duen langileak eskaeraren data, gaia eta premia erregistratuko lituzke, baina ez luke kexa-izapideko daturik ereduan sartuko. Zuzendaritzak kexak jasotzeko langile arduraduna izendatuko luke; kasu pedagogikoa irakasle egoki batek berrikusiko luke. Kexa puntuala bada, laguntza arruntaren prozesua erabiliko da berehala, ereduaren eztabaida bukatu arte itxaron gabe.

Lehen erantzun eta ebazpen epeak benetako zerbitzu-ahalmena eta GDPR epe aplikagarriak egiaztatuta ezarriko lirateke. Dokumentu honetan ez da epe operatiborik edo lege-eperik asmatzen. Ikastetxeak erantzunaren aurrerapena jakinarazi, ikaslearen ikuspegia entzun, datu eta erabakia behar izanez gero zuzendu, eta emaitza modu ulergarrian azalduko luke. Errepikatutako kexak, ikasle talde batek sortutako kexak edo kalte-arrastoak arduradun nagusiari eta DPOari eskalatuko litzaizkieke.

### 5.5 Ingurumen eta gizarte kostuak

Helburu txikiko ikastetxe baterako ere aztertu behar dira datu-hodeiaren hornitzailea, eredua exekutatzeko baliabideak eta datuen mugimendua. Proiektu honetan ez dago energia edo ingurumen-datu fidagarririk; ezin da inpaktu kuantitatiborik ondorioztatu. Hornitzaileari sistemaren baliabide-kontsumoari eta datu-kokapenari buruz galdetzea gomendatzen da, baina neurriok hezkuntza-balioa eta pribatutasun-arriskua ebazten ez badute, eraginkortasun-adierazpenak ez dira nahikoa.

### 5.6 EEEren behin-behineko ondorioa

Onura pedagogikoa sinesgarria baina frogatu gabea da; kalteak banaketa desorekatuaren eta etiketatzearen bidez gerta daitezke. Irakasle-erabakiak benetakoak izango balira ere, automatizazio-alborapena eta puntuazioen eragin zeharkakoa kontrolatu behar dira. Horregatik gomendioak “aldatu eta berriz ebaluatu” izaten jarraitzen du. Diseinu-kontrolak ezartzen ez badira edo banaketa desorekatu frogatua agertzen bada, erabilera gelditu.

## 6. Arrisku-erregistroa eta kontrolak

| Arriskua | Eragin posiblea | Kontrol prebentiboa | Detekzioa eta erantzuna | Arduradun-rola |
|---|---|---|---|---|
| Datu oker edo zaharkituak | Ikaslea behar bezala ez laguntzea edo oker etiketatzea | Iturrien jatorria, zuzenketa-prozesua, eguneratze-data | Zuzenketa-eskaerak eta errore-laginak berrikusi | Datuen arduraduna |
| Ordezko adierazleek desberdintasuna kodetzea | Ikasle ahulenen kalte sistematikoa | Beharrezko datuak soilik; alborapen-analisia | Taldeko errorea eta kexa-ereduak aztertu; eredua eten | Ekitate/kalitate arduraduna |
| Automation bias | Irakasleak gomendioa egiaztatu gabe onartzea | Trebakuntza, kontrako ebidentzia ikustea, veto erreala | Onarpen/bazterketa arrazoiak auditatu | Irakasle gainbegiratzailea |
| Laguntza-etiketak iraunkor bihurtzea | Estigma edo aukeren murrizketa | Epe laburra, etiketa ez iraunkorra, ikusgarritasun txikia | Espediente eta esportazioen auditoretza | Zuzendaritza |
| Baimenik gabeko bigarren erabilera | Helburu desbideraketa | Kontratu, baimen eta interfaze-kontrolak | Hornitzailearen auditoria eta sarbide-erregistroak | Arduradun juridiko/datuak |
| Datu pertsonalen urraketa | Konfidentzialtasun edo eskubide-galera | Gutxieneko sarbidea, zifratzea eta segurtasun-kontrolak | Gertakari-prozedura, isolamendua, ebaluazioa | Segurtasun-arduraduna |
| Hornitzailearen eredua aldatzea | Aurreko emaitzak ez errepikatzea | Bertsio-aldaketen jakinarazpena eta onarpena | Erregresio-proba eta berrikuspena | Sistema-jabea |
| Kexarik edo azalpenik ez | Ikasleak ezin du datu edo erabakia zalantzan jarri | Kanal irisgarria eta rol argia | Erantzun-denbora eta eskalatze egoera berrikusi | Ikasleen babes arduraduna |

Arrisku-erregistroa erabili aurretik berrikusiko da, eta gutxienez ikasturte bakoitzean, hornitzaile/eredu aldaketa bakoitzean, helburu-aldaketa batean, datu-urraketa baten ondoren eta kexa/kalte-seinale garrantzitsu baten ondoren. Kontrol baten arduraduna eta ebidentzia zehaztu ezean, arriskua ez da itxitzat joko.

## 7. Giza gainbegiratzea eta eguneroko erabilera

### 7.1 HITL diseinu hautatua

HITL da gomendatutako eredua, ikasle bakoitzaren laguntza-eskaintza edo talde-proposamenak bere hezkuntza-esperientzian eragin dezakeelako. Giza parte-hartzea eraginkorra izateko, irakasleak aukera bakoitzean: ikusi zein datu sartu diren; ulertu seinalearen mugak; datu okerrak zuzendu edo prozesua gelditu; ikaslearen azalpena entzun; bestelako ebidentzia pedagogikoa aztertu; emaitza baztertu, aldatu edo onartu; eta arrazoia erregistratu behar du. Hori egin ezin bada lan-kargagatik edo sistemaren opakutasunagatik, tresna ez da erabiliko.[2]

### 7.2 Prozesuaren pausoak

1. Irakasleak sistema erabili aurretik ikasleari eta dagokion ordezkariari informazioa ematen dio.
2. Seinaleak laguntza-aukera bat planteatzen du; ez du automatikoki komunikazio edo zigorrik eragiten.
3. Irakasleak iturriak eta datuen zuzentasuna begiratzen ditu eta ikaslearen egoera entzuten du.
4. Irakasleak ohiko esku-hartze pedagogikoarekin alderatzen du eta AI gabeko aukera ere ebaluatzen du.
5. Irakasleak bere erabakia hartzen du, talde-proposamena aldatu ahal du eta arrazoia proportzionalki erregistratzen du.
6. Laguntza eskaintzen da seinalea edozein dela ere; ikasleak uko edo bestelako laguntza eskatzeko bidea du, aplikagarri diren eskubideak kontuan hartuta.
7. Jarraipenaren ondoren, datu operatiboak eta seinalea epe justifikatuan ezabatzen edo anonimizatzen dira.

### 7.3 Gainbegiratzailearen prestakuntza

Irakasle eta administratzaileek honako gaiak ezagutu behar dituzte: seinaleak zer adierazten duen eta zer ez; datuen jatorria eta ohiko erroreak; giza berrikuspenaren pausoak; taldeko alborapenaren adibideak; automatizazioarekiko gehiegizko konfiantzaren arriskua; datu-zuzenketaren eta kexaren bideak; informazio sentikorra babesteko neurriak; eta sistema eten behar den egoera. Prestakuntza erregistratu eta materiala eredu/bertsio aldaketekin eguneratuko da.

### 7.4 Eten irizpideak

Sistema eten edo datu-sarrera berriak blokeatuko dira baldin eta: oinarri juridikoa edo rolak zalantzan badaude; datu-isuria gertatzen bada; hornitzaileak eredu edo helburua jakinarazi gabe aldatzen badu; sarbide baimenik gabea aurkitzen bada; taldeen arteko errorerik ezin bada behar bezala aztertu; ikasle-kalte errepikatuak agertzen badira; irakasleek gomendioa ezin badute benetan gainditu; edo lege-eskakizun bat bete gabe dagoela ikusten bada. Etenaldiak ez du ohiko laguntza pedagogikoa gelditu behar.

## 8. Alternatibak eta ezarpen-aukera

| Aukera | Onura | Muga/arriskua | Gomendioa |
|---|---|---|---|
| A. Ohiko tutoretza eta irakasle-protokolo estandarra | Datu gutxiago; elkarrizketa pedagogiko zuzena | Langileentzako denbora eta koherentzia behar ditu | Lehen konparazio-oinarria |
| B. Ikaslearen autoeskaera eta laguntza irekia | Ikaslearen agentzia; ez dago seinale bidezko bazterketarik | Ikasleak laguntza eskatzera iritsi behar du | A aukerarekin batera probatu |
| C. Irakasleentzako kontrol-zerrenda ez-automatikoa | Arrisku/seinaleak sistematizatzen ditu eredu prediktiborik gabe | Adierazleak oraindik bidegabe erabil daitezke | Datu-proportzionaltasuna eta berrikuspena behar |
| D. Predikzio-tresna | Laguntza-kasu posibleak lehenago identifikatzeko lagungarria izan daiteke | Datu, alborapen, azalpen eta hornitzaile-arrisku handiagoak | Aukera baldintzapean bakarrik aztertu |

Proiektuak A, B edo C aukeren bidez helburu bera lor badezake, D aukeraren datu-babes eta ekitate-kostua ez da justifikatzen. Konparazioa diseinatu beharko litzateke datu errealak bildu aurretik, eta ikasleen hezkuntza-emaitzak ez lirateke ereduaren “arrakasta” gisa automatikoki atribuituko.

## 9. Hornitzailearen, arduradunaren eta deployer-aren betebeharren matrizea

AI Acteko rolen eta GDPRko datu-babes rolen artean lotura dago baina ez dira gauza bera. Ikastetxea GDPRko arduraduna eta AI Acteko deployer izan liteke; software-egilea AI Acteko provider eta GDPRko processor izan liteke, baina benetako kontratu eta jardueraren arabera aztertuko da.[1][2]

| Lan-lerroa | Hornitzailea | Ikastetxea / deployer-a | Froga beharrezkoa |
|---|---|---|---|
| Xedea eta erabilera | Erabilera-argibide zehatzak | Xedea eta erabilera mugatu | Xede-adierazpena eta tokiko baimena |
| AI Act sailkapena | Sistemaren dokumentazioa | Erabilera-testuingurua egiaztatu | Arrazoitutako sailkapen-oharra |
| Arriskuen kudeaketa | Sistemaren arrisku-kontrolak | Tokiko arriskuak eta erabilera-ingurunea | Arrisku-erregistro bateratua |
| Datuak | Prestakuntza/egiaztapeneko datu-gobernantza | Sarrera-datuen iturri, kalitate eta zuzentasuna | Datu-mapa eta QA txostenak |
| Giza gainbegiratzea | Erabiltzaile-argibide eta kontrol-gaitasunak | Langile trebatuak, denbora eta veto-ahalmena | Prozedura eta prestakuntza-erregistroa |
| Monitorizazioa | Akats/aldaketen jakinarazpena | Benetako erabilera, kexak eta emaitzak | Bertsio-kontrola eta aldizkako berrikuspena |
| Pribatutasuna | Prozesadore-zerbitzua mugatzea, dagokionean | Lege-oinarria, gardentasuna, EIPD eta eskubideak | GDPR erregistroak eta kontratua |
| Segurtasuna | Hornitzailearen kontrol eta gertakari-oharra | Sarbide/segurtasun neurriak eta gertakari-erantzuna | Kontratu, log eta incident report |
| Datuen amaiera | Ezabatzea/itzultzea egiaztatu | Amaiera eta kopia lokalak kudeatu | Ezabaketa-ziurtagiria eta egiaztapena |

Erosketa-kontratuan helburua, prozesadorearen argibideak, azpi-prozesadoreak, datuen kokapena, transferentzia, atxikipena, erabilera sekundarioa, segurtasun-urraketa, auditoretza, datuak ezabatzea eta eredu-aldaketen jakinarazpena estali behar dira. Hornitzailearen ziurtagiri edo produktu-ohar batek ez ditu ikastetxearen tokiko ardurak ordezkatzen.

## 10. Gertakari, kexa eta jarraipen prozesua

### 10.1 Gertakari motak

Prozedurak bereizi egingo ditu datu pertsonalen urraketa; gomendio nabarmen okerra; azpitalde jakin baten emaitzen narriadura; erabilera desegokia; ereduaren edo datuen hornitzaile-aldaketa; eta kexa edo kalte-aldarrikapena. Gertakari bat susmatzen duen langileak ez du bere kabuz logikak ezabatuko edo ikaslearen espedientea aldatuko. Erabilera segurua berehala eten, dagokion barne-kanalera jakinarazi eta ebidentzia mugatuan gorde behar da.

### 10.2 Erantzuneko pausoak

1. Gertakariaren hasierako seinalea jaso eta data/iturri minimoa erregistratu.
2. Kalte gehiago saihesteko sistema edo funtzioa eten; eskuzko laguntza-prozesua mantendu.
3. Eraginpeko datu/ikasle, sistemaren bertsio, sarbide-erregistro eta hornitzaile-jakinarazpenak identifikatu.
4. Segurtasun-arduradunak eta DPOak gertakariaren izaera eta jakinarazpen-betebeharrak aztertu.
5. Ikastetxeko zuzendaritzak eta, behar denean, eskumena duen erakundeak hurrengo urratsa erabakitzen dute.
6. Eraginpeko pertsonei informazioa ematen zaie legeak eskatzen duen eran; behar den laguntza eskaintzen da.
7. Erroaren kausa aztertu, kontrola zuzendu, itzulera-irizpideak ezarri eta ikasleei eragindako erabakiak berrikusi.
8. Erabilera berriro hastea soilik kontrolaren eraginkortasuna egiaztatu eta baimen-maila egokiak dokumentatu ondoren.

GDPRko jakinarazpen-epeak gertakariaren motaren eta arriskuaren arabera aplikatzen dira; dokumentu honek ez du egutegi juridikoaren ordez prozedura operatiborik ezartzen. Arau aplikagarriak eta erakunde barruko eskalatze-epeak segurtasun-plan errealarekin bat zehaztu behar dira.[1]

### 10.3 Erregistroa eta datu-minimizazioa

Gertakari-erregistroan identifikatzaile osoak edo ikasleen xehetasunak ez dira behar baino gehiago kopiatuko. Erregistroak honakoak jasoko lituzke: gertakari IDa, data, arduradun-rola, arriskua, eten/konponketa neurriak, beharrezko jakinarazpenen egoera, ikasitakoa eta berrirekitzeko irizpidea. Sarbidea mugatua izango da. Txosten publiko edo didaktikoetan datuak anonimizatu edo sintetikoak erabiliko dira.

## 11. Aukerak eta erabaki-ateak

Proiektuak hiru egoera garbi ditu:

| Egoera | Baldintzak | Erabakia |
|---|---|---|
| Aurrera | Helburu eta oinarri juridikoa egiaztatuta; EIPD eta kontrolak osatuta; hornitzaile froga egokia; diseinu-probak gaindituta; kexa/eten prozesua martxan | Erabilera mugatua aztertu, dagokion baimen instituzionalarekin |
| Aldatu | Xedea baliagarria baina datu, interfaze, rol, azalpen edo proba hutsune zuzentagarriak | Diseinua aldatu; ez erabili ikasleen datuetan hutsuneak itxi arte |
| Gelditu | Oinarri juridikorik ez; alternatiba ez hain intrusiboa nahikoa; kalte edo desberdintasun nabarmenak; giza gainbegiratzea ez da eraginkorra; hornitzaileak ez du frogatzen | Sistema ez erosi edo erabilera eten |

Erabaki-ate bakoitzak idatzizko ebidentzia eta rol egoki baten onarpena behar du. Ez da “aurrera” egoerara pasatuko iturri nagusi bat falta delako edo epe komertzial batek presioa egiten duelako.

## 12. Gomendioa eta hurrengo urratsak

### 12.1 Gomendio nagusia: ALDATU

Proiektua kontzeptu gisa aztertzen jarraitzea posible da, baina ikasle-datuekin erabilera ez da baimentzen gaurko ebidentziarekin. Proiektuaren kasua hipotetikoa da eta ez du benetako legezko/tekniko ebaluaziorik. Lehen urratsa helburu pedagogikoa eta ohiko alternatibak deskribatzea da. Horren ondoren soilik ebaluatu beharko lirateke datu-iturriak, oinarri juridikoa, EIPD, AI Acteko sailkapena, hornitzaile eta giza gainbegiratzea. Bide horretan arriskua onargarria dela frogatu ezin bada, gelditu.

### 12.2 Abiarazte aurreko ate-zerrenda

- [ ] Benetako arduraduna, xedea eta eskumen/lege-oinarria identifikatuta.
- [ ] Laguntza-prozesu ez-automatizatua eta aukerak alderatuta.
- [ ] Datu-mapa, datu-eremu bakoitzaren beharrezkotasuna eta gordetze-epea arrazoituta.
- [ ] Hornitzaile-rolak, kontratua, azpi-prozesadoreak, transferentziak eta erabilera sekundarioa egiaztatuta.
- [ ] AI Acteko sailkapena, erabilera-argibideak eta aplikazio-egutegia idatziz berrikusita.[2][3]
- [ ] DPOa/lege-aditua kontsultatuta, hala dagokionean.
- [ ] EIPDren beharra baheketaz ebatzita; beharrezkoa bada, tratamendua hasi aurretik amaituta.[1][6]
- [ ] Informazio-orria eta datu/erabaki zuzenketa eskatzeko kanala probatuta.
- [ ] Giza gainbegiraketa, trebakuntza, denbora eta eten-botoia egiaztatuta.
- [ ] Datu sintetiko edo anonimotuetako proba eta taldeko kalitate-azterketa aurrez zehaztuta.
- [ ] Erantzun-protokoloa, gertakari-eskalatzea eta ohiko laguntza-prozesuaren jarraipena prestatuta.
- [ ] Zuzendaritzak erabaki arrazoitua hartu eta ebidentzia erregistratuta.

Zerrenda hau proiektu hipotetikoaren diseinu-kontrola da. Ez du erakunde erreal baten lege-ziurtagiriaren edo erabaki formalaren ordez balio.

## 13. Muga eta ziurgabetasunak

- Erakunde eta sistema hipotetikoak dira; ez da ikastetxe erreal baten araudi autonomikoa, eskumen edo kontratu aztertu.
- Ikasle-datu edo eredu-irteerarik ez dago; zehaztasun, errore, ekitate edo onura kuantitatiborik ez da frogatu.
- AI Acteko xedearen eta erabileraren definizio zehatza hornitzaile-dokumentazioaren eta deployment-aren araberakoa da. Hezkuntza-erabileraren arrisku handiko hipotesia zuhurtziazko abiapuntua da, ez behin betiko iritzi juridikoa.[2]
- Datuen lege-oinarria eta adingabeen informazio/ordezkaritza kasu bakoitzean arau eta eskumen egokiekin ebazten dira.[1]
- 2026/1744 Erregelamenduak AI Acteko aplikazio-egutegia aldatu du. Erabilera-data hurbildu ahala, EUR-Lexeko bertsio indarduna berriz egiaztatu beharko da.[2][3]
- EEEko gomendio etikoak ez dira legezko betebeharren ordez; EIPD eta beste arauzko ebaluazioak bereiz egin behar dira.[1][6]

## 14. Erabilitako iturriak

Iturri-zenbaki hauek Task 2ko erantzun-ereduko erregistro berari dagozkio. Kontsulta-data 2026-09-24 da; 2026ko testu kontsolidatua eta lege aldaketa loteslea kontuan hartu dira.

1. [Datuak Babesteko Erregelamendu Orokorra (EB) 2016/679, EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj/spa), bereziki 4–6, 9, 12–15, 22, 25, 28, 32 eta 35–36. artikuluak.
2. [Adimen Artifizialari buruzko Erregelamendua (EB) 2024/1689, 2026-07-27ko testu kontsolidatua, EUR-Lex](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:02024R1689-20260727), bereziki 3, 6, 9–15, 26, 50, 86 eta 113. artikuluak, III. eranskina (3. eremua) eta I. eranskina.
3. [2026/1744 Erregelamendua, AI Acteko 113. artikuluaren aplikazio-egutegia aldatu zuena](https://eur-lex.europa.eu/eli/reg/2026/1744/oj).
4. [AEPD, AI-00009-2026, CV hautaketa-tresnari buruzko ohartarazpena](https://www.aepd.es/documento/ai-00009-2026-advertencia.pdf). Txostenean ez da hezkuntza-kasuaren iturri juridiko gisa erabiltzen.
5. [AEPD, EXP202305233, UIV urrutiko azterketetako biometria eta AA erabileraren kasuaren laburpena](https://www.aepd.es/informes-y-resoluciones/criterios-juridicos-aepd/aepd-sanciona-tratamiento-datos-biometricos-ia), eta [AEPDren 2025 memoria](https://www.aepd.es/memorias/memoria-aepd-2025.pdf), 57. or. Txostenean ez da hezkuntza-kasuaren iturri juridiko gisa erabiltzen.
6. [AEPD, datu-babesaren inpaktu-ebaluazioa (EIPD) noiz egin](https://www.aepd.es/derechos-y-deberes/cumple-tus-deberes/medidas-de-cumplimiento/realizacion-de-evaluaciones-de).
7. [AI Acteko 113. artikulua, EUR-Lexeko testu kontsolidatuan](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:02024R1689-20260727#d1e10368-1-1).

---

*Dokumentua ikasgelako erantzun-eredu hipotetikoa da. Erakunde erreal batek bere testuinguruko legea, eskumenak, datu-fluxua eta egungo araudia aztertu behar ditu erabili aurretik.*
