# 5071-IE1-Logika_Lausoa



3. ATALA

Logika Lausoa

EGILEA



ZENTROA

Laneki — FP Euskadi

EDIZIOA

v1.0

IKASTAROA

2026 — 2027



Logika Lausoa

Logika Lausoaren (Fuzzy Logic) oinarriak

Aurreko atalean ikusi dugun bezala, Sistema Adituek ezagutza arau zurrunen bidez kodetzen dute. Sistema horietan, baldintza bat betetzen da edo ez da betetzen: "Sukarra 38ºC-tik gorakoa bada, gaixo dago". Baina zer gertatzen da pazienteak 37,9ºC baditu? Logika klasikoan oinarritutako SA batek "osasuntsu" dagoela esango luke, muga gogor horrek (0 edo 1) ez duelako ñabardurarik onartzen. Honek sistema oso sentikorrak eta, batzuetan, hauskorrak sortzen ditu.

Hain zuzen ere, muga horiek gainditzeko sortu zen Logika Lausoa. Bere helburua ez da SAen egitura aldatzea, baizik eta egitura horri malgutasun matematikoa ematea. Sistema aditu bat "lausoa" denean, ez du erabakitzen zerbait egia den ala ez; zerbait neurri batean egia den kalkulatzen du.



03.1  Aldagai Linguistikoak eta Multzo Lausoen Teoria

Logika lausoaren oinarrian aldagai linguistikoak daude. Guk, gizakiok, ez dugu esaten "gela hau 24,5 gradutan dago"; esaten dugu "gela bero dago" edo "giro ona dago". "Bero" hori multzo lauso bat da.



Logika Lausoaren funtzionamendu-eskema: lausotzea, inferentzia eta lausotasun-kentzea



MULTZO KLASIKOAK VS. MULTZO LAUSOAK



Logika Klasikoa

Logika Lausoa

Kidekotasuna

0 edo 1 (barruan edo kanpoan)

0 eta 1 arteko edozein balio

Adibidea

"37ºC < 38ºC → osasuntsu"

"37.9ºC → osasuntsu 0.1, gaixo 0.9"

Trantsizio

Bat-batekoa (aldaketa zakarra)

Leuna (gradualki aldatzen da)



Adibidea: tenperatura-multzoak

24ºC-ko tenperatura:

• "Giro ona" multzoan → 0,8 (ia bete-betean sartzen da)

• "Bero" multzoan → 0,2 (pixka bat)

• "Hotz" multzoan → 0,0 (ez da sartzen)

Honek ahalbidetzen du SAen arauak modu leunean gainjartzea, aldaketa zakarrak ekidinez.



03.2  Kontrolatzaile Lauso baten Barne-Logika: Hiru Faseak

Sistema hauek nola funtzionatzen duten ulertzeko, hiru faseko prozesu bat irudikatu behar dugu — SA inferentzia-motorraren bilakaera dena:



FASE 1: LAUSOTZEA (FUZZIFICATION)

Sentsore baten datu zehatza (balio numerikoa) hartu eta balio linguistiko bihurtzen dugu.

Sarrera: 26ºC (zenbaki zehatza)        ↓Lausotzea:  "Fresko"  → 0.1  "Giro ona" → 0.6  "Bero"     → 0.4

Une honetan, makinak "ulertzen" du tenperatura ez dela balio puntual bat, baizik eta egoera desberdinen konbinazio bat.



FASE 2: INFERENTZIA (FUZZY INFERENCE)

Behin datuak lausotuta, inferentzia-motorrak arauak aplikatzen ditu. Hemen dago Sistema Adituekin lotura zuzenena: arauak oraindik "IF... THEN..." formatukoak dira. Hala ere, aurrebaldintza guztiak neurri batean betetzen direnez, ondorioak ere neurri batean aplikatzen dira.

ARAUA 1: BALDIN (tenperatura = "Bero") [0.4]         ORDUAN (haizagailua = "Azkarra") [× 0.4]ARAUA 2: BALDIN (tenperatura = "Giro ona") [0.6]         ORDUAN (haizagailua = "Ertaina") [× 0.6]

Ez da arau bakar bat exekutatzen; arau asko aktibatzen dira aldi berean, bakoitza bere indarrarekin.



FASE 3: LAUSOTASUN-KENTZEA (DEFUZZIFICATION)

Arau guztien ondorioak konbinatu egiten dira. Prozesu matematiko honen bidez (grabitate-zentroaren metodoa ohikoena da), sistemak agindu zehatz bat kalkulatzen du.

Ondorioak konbinatu:"Haizagailua Azkarra" [0.4] + "Haizagailua Ertain" [0.6]        ↓Defuzzification (grabitate-zentroa)        ↓Irteera zehatza: motorra 1.350 rpm-ra jarri



03.3  Adibide Praktikoa: Aire Kondizionatua

Uler dezagun hiru fase hauek kasu erreal batekin: gela baten aire kondizionatuaren kontrol-sistema. Gure helburua da gela 22ºC-tan mantentzea, aldaketa bortitzak gabe.

EGOERA: GELA 28ºC-TAN DAGO, 60% HEZETASUNAREKIN



1. Urratsa — Lausotzea:



Aldagaia

Balioa

Multzo lausoak

Tenperatura

28ºC

"Bero": 0.7 / "Oso bero": 0.3

Hezetasuna

60%

"Ertaina": 0.4 / "Altua": 0.6



2. Urratsa — Arauak aplikatu:

ARAUA 1: BALDIN (tenp = "Bero") ETA (hezet = "Altua")         ORDUAN (hozketa = "Indartsua") [min(0.7, 0.6) = 0.6]ARAUA 2: BALDIN (tenp = "Oso bero") ETA (hezet = "Ertaina")         ORDUAN (hozketa = "Oso indartsua") [min(0.3, 0.4) = 0.3]ARAUA 3: BALDIN (tenp = "Bero") ETA (hezet = "Ertaina")         ORDUAN (hozketa = "Ertaina") [min(0.7, 0.4) = 0.4]



3. Urratsa — Lausotasun-kentzea (Defuzzification):

Grabitate-zentroaren metodoarekin, hiru arauak pisuarekin konbinatuta:

Emaitza: Kompresorea 78%-ean jarri (ez %100ean, ez %50ean)



KONPARAKETA: SISTEMA KLASIKOA VS. SISTEMA LAUSOA

Egoera

Sistema Klasikoa

Sistema Lausoa

Tenp. 28ºC → 27.9ºC

PIZTU/ITZALI etengabe

Abiadura graduala murriztu

Energia-kontsumoa

Altu (on/off zikloak)

Baxu (trantsizioak leunagoak)

Erosotasuna

Aldaketa zakarrak

Trantsizioak nabaritu gabe

Erabiltzailearen sentsazioa

Hotza/beroa alternatu

Tenperatura egonkor



Sistema klasikoan: Tenperatura 24ºC heltzean, sistema ITZALI egiten da. Segundu batzuetan 25ºC igotzean, PIZTU egiten da. Etengabeko on/off zikloak sortzen ditu.

Sistema lausoan: Tenperatura helburutik aldentzen denean, kompresorea pixkanaka egokitzen da. Ez da sekula erabat ITZALI edo PIZTU; beti tarteko moduren batean dago.



03.4  Sistema Hibridoak: SA + Logika Lausoa

Logika lausoak SAei eman dien abantaila handiena errendimendua eta erosotasuna da. Gaur egun sistema hibridoetan ikusten duguna honakoa da:

• SAk → goi-mailako erabakiak hartzeko (estrategia): "Eraikina bero dago, behar du hoztea".

• Logika lausoa → behe-mailako kontrolerako (ekintza zehatzak): "Zenbateko potentziatan jarri kompresorea".

Mundua errealaren ziurgabetasuna eta ñabardurak hobeto kudeatzen dituelako, logika lausoa bereziki erabilia da:

Aplikazioa

Deskribapena

Gidatze autonomoa

Boltea, abiadura eta balaztada leuntasunez kudeatu

Industria-kontrola

PID kontroladore lausoak: tenperatura, presio, fluxua

Medikuntza

Sendagaien dosifikazio gradualeko sistemak

Finantza

Arrisku-kalkulua maila anitzeko aldagaiekin

Robotika

Esku-mugimenduak giza naturalitatearekin egitea



Ondorioa: Logika lausoa ez da sistema aditu baten "ordezkoa"; bere osagarria da. Bi munduen onena hartzen du: SAen arau-egitura azalgarria eta giza arrazonamenduaren malgutasun graduala. Ikaskuntza sakonaren aurrean, logika lausoak mantentzen du abantaila bat: azalgarritasuna. Arauak ulergarriak dira gizakiarentzat, eta hori ezinbestekoa da segurtasun-kritikoak diren sistemetan.