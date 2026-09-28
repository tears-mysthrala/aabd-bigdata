DATUEN INGENIARITZA

ARIKETAK

Datuen bizi-zikloa identifikatu

Adierazi egoera bakoitza zein faserekin lotzen den: Sorrera, Ingesta, Biltegiratzea, Eraldaketa edo Zerbitzatzea/Kontsumoa.

Tenperatura-sentsore batek 5 segundoan behin neurketa bat egiten du.

Apache NiFi-k CSV fitxategiak zerbitzari batetik Data Lake batera eramaten ditu.

Datuak MongoDB batean gordetzen dira.

"Eibar " balioa "Eibar" bihurtzen da.

Power BI-k salmenten dashboard bat erakusten du.

Web zerbitzari batek erabiltzaile baten eskaera log batean erregistratzen du.

Bi CSV fitxategitako bezeroen informazioa bateratzen da.

Machine Learning eredu batek prestatutako datuak erabiltzen ditu.

Datu baten bidaia

Online denda batean bezero batek produktu bat erosten du.

Azaldu datu horrek egin dezakeen ibilbidea honako kontzeptuak erabiliz:

Sorrera  Ingesta  Biltegiratzea  Eraldaketa  Zerbitzatzea

Adibidez, erantzun honelako galderak:

Non sortzen da datua? Nola eramaten da? Non gordetzen da? Zer transformazio egin dakioke? Nork erabiliko du azkenean?

Hardware fisikoa: zer aukeratuko zenuke?

Aukeratu HDD, SSD edo RAM eta justifikatu.

Duela 5 urteko backup-ak, ia inoiz erabiltzen ez direnak.

Une honetan aplikazio batek etengabe erabiltzen dituen datuak cachean gordetzea.

Ordenagailu bateko sistema eragilea eta egunero erabiltzen diren aplikazioak.

10 TB-ko artxibo historikoa, urtean behin kontsultatzen dena.

Segundo bakoitzean milaka aldiz kontsultatzen den aldi baterako informazioa.

Biltegiratze-abstrakzio egokia aukeratu

Aukeratu Data Warehouse, Data Lake, Data Lakehouse edo Cache.

Enpresa batek azken 10 urteetako salmenta egituratuak aztertu nahi ditu OLAP kontsultekin.

Enpresa batek PDF, JSON, CSV, bideo, audio eta log gordinak gorde nahi ditu.

Industria batek IoT datu gordinak gorde nahi ditu, baina aldi berean analitika aurreratua egin eta datuak modu kontrolatuan kudeatu. DATA

Web-aplikazio batek erabiltzaileek etengabe kontsultatzen duten informazioa milisegundotan itzuli behar du.

Kasu praktikoa: “Smart Factory”

Fabrika batek 500 IoT sentsore ditu. Sentsoreek tenperatura, bibrazioa eta energia-kontsumoa neurtzen dituzte. Datu berriak segundo gutxian behin sortzen dira. Uneko datuak oso azkar kontsultatu behar dira makinen egoera monitorizatzeko. Datu guztiak ere gorde nahi dira, azken 5 urteetako joerak aztertzeko.

Erantzun:

Non sortzen dira datuak?

Identifikatu Sorrera, Ingesta, Biltegiratzea, Eraldaketa eta Zerbitzatzea faseetako adibide bana.

Datu historiko guztietarako zer biltegiratze-abstrakzio proposatuko zenuke?

Zer transformazio egin dakieke sentsoreen datuei?

Nork edo zerk kontsumituko lituzke datuak?

Datuen irenstea eta ETL

Erantzun justifikatuz:

Datuen pipeline bat diseinatzerakoan, zein da kontuan hartu beharreko lehen urratsa?

Zer erlazio dago datu-pipeline eta ETL artean?

ETL eta ELT gauza bera al dira? Noiz egiten da bakoitza?

Big Data testuinguruan, zein dira nagusi (ETL ala ELT)? Zergatik?

ETL ala ELT?

Adierazi kasu bakoitzean ETL edo ELT erabiltzen den eta justifikatu erantzuna.

CSV fitxategi bat irakurri, datu okerrak zuzendu eta ondoren Data Warehouse batean gordetzen da.

IoT sentsoreen datu gordinak zuzenean Data Lake batean gordetzen dira. Gero, Spark erabiliz garbitu eta agregatzen dira.

MariaDB-ko datuak atera, NiFi-n eraldatu eta MongoDB-n gordetzen dira.

JSON eta CSV fitxategiak aldaketarik gabe Data Lake batera eramaten dira. Ondoren, SQL bidez analisirako prestatzen dira.

Salmenten datuak Pythoon bidez garbitu, bezeroen datuekin elkartu eta azken emaitza Parquet formatuan gordetzen da.

Non daude E, T eta L?

Honako prozesua aztertu:

Identifikatu:

Zein urrats dagokio Extract faseari?

Zein urrats dagozkio Transform faseari?

Zein urrats dagokio Load faseari?

Zer aldatuko litzateke prozesua ELT izango balitz?

ETL prozesua diseinatu

Online denda batek bi fitxategi ditu:

salmentak.csv

bezeroak.csv

Enpresak Eibarko bezeroen salmenta guztien zenbatekoa kalkulatu nahi du.

Azaldu zer egingo zenukeen fase bakoitzean (pipeline-a pentsatu):

E – Extract

T – Transform

L – Load

Zein formatu aukeratuko zenuke?

Kasu bakoitzean aukeratu formatu egokiena: CSV, JSON, JSONL edo Parquet, eta erantzuna justifikatu.

Excel/Calc-en ireki behar den 500 erregistroko bezero-zerrenda.

API batek erabiltzaile baten informazioa bidaltzen du.

Zerbitzari batek etengabe log-erregistroak sortzen ditu eta banan-banan prozesatu nahi ditugu.

500 milioi salmentako Data Lake bat Spark-ekin analizatu behar dugu.

Beste enpresa bati taula sinple bat bidali behar diogu, edozein tresnarekin ireki ahal izateko.

200 GB-ko dataset batean prezioa eta produktua zutabeak bakarrik analizatuko ditugu.

Errenkadaka ala zutabeka?

Enpresa batek honako dataset-a dauka:

id, data, produktua, kategoria, hiria, prezioa, unitateak, bezero_id

Adierazi kasu bakoitzean errenkadetara orientatutako edo zutabeetara orientatutako formatua interesgarriagoa den.

bezero_id=4387 bezeroaren erosketa baten informazio osoa eskuratu.

Salmenta guztien batez besteko prezioa kalkulatu.

Produktu jakin baten erregistro osoa irakurri.

Hiri bakoitzeko salmenta kopurua kalkulatu.

Milioika erregistrotatik hiria eta prezioa soilik analizatu.

Faker-ekin lehen dataset-a

Sortu bezeroak.csv fitxategia 100 bezero sintetikorekin.

Gutxienez:

id

izena

emaila

hiria

adina

Baldintzak:

Faker(‘es_ES’) erabili.

Adina 18-80 artean.

Goiburua izan behar du.

100 erregistro izan behar ditu.

Fitxategia ireki eta emaitza egiaztatu.

Ondoren, aldatu kodea 10.000 bezero sortzeko.

Zer aldatu behar duzu 100 erregistrotik 10.000ra pasatzeko?

Zer egiten du seed-ak?

Faker-ek normalean datu desberdinak sortzen ditu programa exekutatzen dugun bakoitzean. Ariketa honetan seed erabiltzeak zer eragin duen egiaztatuko dugu.

A kasua: Seed gabe

Exekutatu bi aldiz aurreko programa.

fake = Faker('es_ES')

Bi exekuzioetako lehenengo bost pertsonak alderatu.

B kasua: Seed-ekin

Faker.seed(42)

fake = Faker('es_ES')

Berriro bi aldiz exekutatu.

Erantzun:

Zer gertatu da lehenengo kasuan?

Zer gertatu da bigarrenean?

Zertarako izan daiteke erabilgarria seed bat test automatizatuetan?

Irakasleak eta ikasle guztiek seed=42 erabiltzen badute, zer abantaila dauka?

CSV  JSON

Aurreko bezeroak.csv hartu eta bezeroak.json sortu.

Egitura:

{

"bezeroak": [

{

"id": 1,

"izena": "...",

"emaila": "...",

"hiria": "...",

"adina": 34

}

]

}

Erantzun:

Zein fitxategi da gizakiarentzat irakurterrazagoa?

Zeinek dauka egitura esplizituagoa?

JSON-en non gordetzen dira zutabe-izenak?

10 milioi erregistro balira, egokia litzateke JSON osoa memoria batean eraikitzea?

Erronka: salmenta-dataset sintetikoa

Sortu Faker erabiliz 10.000 salmentako dataset sintetikoa:

id

data

bezeroa

hiria

produktua

kategoria

prezioa

unitateak

Baldintzak:

Faker(‘es_ES’)

Faker.seed(42)

Prezioa: 5-2000€

Unitatea: 1-10

Kategoriak: Ordenagailuak, Osagaiak, Periferikoak, Sareak

Gutxienez 10.000 erregistro

Programa exekutatzean bi fitxategi sortu behar dira:

Salmentak.csv

Salmentak.json

Hausnarketa: Dataset honek 10.000 erregistro izan beharrean 500 milioi izango balitu eta Spark-ekin kategoria eta prezioa bakarrik analizatu nahi bagenitu, zein formatu erabiliko zenuke? Zergatik?
