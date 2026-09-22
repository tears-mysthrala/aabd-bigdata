# Ariketak_01_02_datuen_ingeniaritza

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

