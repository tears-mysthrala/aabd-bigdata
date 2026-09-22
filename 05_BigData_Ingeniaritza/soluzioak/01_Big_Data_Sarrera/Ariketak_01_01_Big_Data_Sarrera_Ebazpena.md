# Ariketak 01_01: Big Data Sarrera - Ebazpen Osoa

Modulua: **Big Data Sistemak eta Sarrera**  
Fitxategi iturria: `Ariketak_01_01_big_data_sarrera.docx`

---

## 1. Big Data-ren 7 V-ak. Hausnarketa

### Galdera 1: Big Data-ren 7V-etatik zein dela garrantzitsuena uste duzu? Zergatik?
**Erantzuna:**
Dudarik gabe, **Balioa (Value)** eta **Egiazkotasuna (Veracity)** dira garrantzitsuenak:
- **Balioa (Value):** Big Data proiektu baten helburua ez da datuak metatzea, negozioari edo gizarteari erabaki hobeak hartzen laguntzea baizik. Petabyte asko eduki ditzakegu, baina informazio hori erabilgarria ez bada, kostu huts bat besterik ez da.
- **Egiazkotasuna (Veracity):** *“Garbage in, garbage out”* printzipioa aplikatzen da. Datuak faltsuak, zikinak edo fidagarritasun gabeak badira, horien gainean eraikitako Machine Learning ereduak edo txostenak kaltegarriak izango dira.
- **Ondorioa:** Bolumena, Abiadura eta Barietatea erronka teknologikoak dira; baina Balioa eta Egiazkotasuna dira proiektuaren arrakasta bermatzen dutenak.

---

### Galdera 2: Big Data-n oinarritutako zer tresna/zerbitzu/teknologiak errazten du zure eguneroko bizitza?
**Erantzuna:**
Hainbat adibide daude gure egunerokoan:
1. **Google Maps / Waze (Mugikortasuna):** Milioika gailuren kokapen-datuak eta abiadura denbora errealean aztertzen ditu pilaketak aurreikusteko eta ibilbiderik azkarrena kalkulatzeko.
2. **Spotify / YouTube (Gomendio-sistemak):** Entzuleen portaera-datu masiboak aztertuz, gure gustuetara egokitutako abestiak eta edukiak proposatzen dizkigu (Collaborative Filtering eta Deep Learning bidez).
3. **Kreditu-txartelen iruzur-detekzioa (Bankuak):** Transakzio bat egiten dugun milisegundoetan, iruzur-arriskua neurtzen du gure ohiko erosketa-ereduekin alderatuta.

---

## 2. 7 V-ak kasu errealetan (Spotify)

Spotify-ren antzeko streaming-plataforma batean, identifikatu zein V agertzen den egoera bakoitzean:

| Egoera | 7V-etako zein? | Arrazoibidea |
|---|---|---|
| **Milioika erabiltzailek aldi berean abestiak entzuten dituzte.** | **Bolumena (Volume)** eta **Abiadura (Velocity)** | Datu-fluxuaren tamaina izugarria da eta aldi bereko konkurrentzia handia kudeatu behar da. |
| **Erabiltzaile bakoitzak milaka erreprodukzio sortzen ditu.** | **Bolumena (Volume)** | Denboran zehar sortzen den erregistro kopuru total masiboa adierazten du. |
| **Erabiltzaileen datuak CSV, JSON, audio, irudi eta testu formatuetan daude.** | **Barietatea (Variety)** | Datu egituratuak (CSV), erdi-egituratuak (JSON) eta egituratu gabeak (Audio, Irudiak, Azalak) elkarrekin kudeatzen dira. |
| **Erreprodukzio-datuak segunduro jasotzen dira.** | **Abiadura (Velocity)** | Datuen sorkuntza eta irenste (ingestion) abiadura handia denbora errealean. |
| **Datu batzuetan erabiltzailearen adina 17, beste batzuetan 170 agertzen da.** | **Egiazkotasuna (Veracity)** | Datuen kalitate-arazoa, erroreak, anomaliak edo inkongruentziak (outliers). |
| **Datuak aztertuz, erabiltzaile bakoitzarentzat abesti interesgarriak proposatzen dira.** | **Balioa (Value)** | Datuak negozio-onura eta erabiltzaile-esperientzia hobetzeko bihurtzen dira (Gomendio Eredua). |
| **Zuzendaritzak dashboard batean KPI-ak ikusten ditu.** | **Bistaratzea (Visualization)** / **Bideragarritasuna (Viability)** | Informazio konplexua panel bisual ulergarrietan aurkeztea erabaki estrategikoak hartzeko. |

---

## 3. Analitika motak

Online denda baten salmenten datuak aztertuz:

1. *"Joan den hilean 125.000 € saldu genituen."*  
   👉 **Deskribatzailea (Descriptive):** Iraganean zer gertatu den azaltzen du (Datu historikoak laburbildu).
2. *"Zergatik jaitsi ziren salmentak %15 martxoan?"*  
   👉 **Diagnostikoa (Diagnostic):** Gertatutakoaren arrazoiak eta zergatiak bilatzen ditu (Kausa-efektua).
3. *"Datorren hilabetean 140.000 €-ko salmentak izango ditugula aurreikusten dugu."*  
   👉 **Prediktiboa (Predictive):** Etorkizunean zer gertatuko den aurreikusten du eredu estatistikoen bidez.
4. *"Stocka %20 handitu beharko genuke eskaera handia duten produktuetan."*  
   👉 **Preskriptiboa (Prescriptive):** Ekintza zehatz bat proposatzen du emaitza optimizatzeko (Erabaki-hartzea bideratu).
5. *"Eibarrek izan du salmenta-kopuru handiena."*  
   👉 **Deskribatzailea (Descriptive):** Datu historikoen banaketa geografikoa erakusten du.
6. *"Astelehenetan salmentak beste egunetan baino txikiagoak dira."*  
   👉 **Deskribatzailea / Diagnostikoa:** Patroi historiko bat identifikatzen du.
7. *"Eguraldi txarra egiten duenean online eskaerak handitzen dira."*  
   👉 **Diagnostikoa (eta oinarri Prediktiboa):** Kanpoko faktore baten eta salmenten arteko korrelazioa azaltzen du.

---

## 4. Data Science prozesua ordenatu

### Faseen ordena zuzena:
1. **Helburuak ezarri** *(Business / Problem Understanding)*
2. **Datuak eskuratu** *(Data Acquisition / Ingestion)*
3. **Datuak esploratu** *(Exploratory Data Analysis - EDA)*
4. **Datuak prestatu** *(Data Cleaning, Transformation & Feature Engineering)*
5. **Modeloak sortu** *(Model Training & Evaluation)*
6. **Emaitzak aurkeztu eta automatizatu** *(Deployment, Dashboarding & Monitoring)*

---

### Aplikazioa ikastetxeko absentismo-kasuan:
> *“Ikastetxe batek ikasleen absentismoa aztertu nahi du, eta hurrengo hilabetean absentismo-arriskua duten ikasleak identifikatu.”*

1. **Helburuak ezarri:**  
   Definitu zer den arrisku-maila (adib. hurrengo hilabetean klaseen %15 baino gehiago galtzeko arriskua duten ikasleak goiz detektatzea), tutoreek garaiz esku har dezaten.
2. **Datuak eskuratu:**  
   Ikastetxeko kudeaketa-sistematik (adib. Moodle, Inika, Alexia) aurreko ikasturteetako falta-erregistroak, ikasleen garraio-datuak, kalifikazio partzialak eta asteko ordutegiak erauzi.
3. **Datuak esploratu:**  
   Estatistika deskribatzailea eta grafikoak egin: faltak astelehenetan edo ostiraletan gehiago al dira? Lehenengo orduan al dira? Absentismoaren eta noten artean korrelaziorik ba al dago?
4. **Datuak prestatu:**  
   Datu galduak (NaN) kudeatu, falta justifikatuak eta ez-justifikatuak bereizi, eta aldagai prediktiboak sortu (adibidez: *azken 15 egunetako falta-kopurua*, *aurreko ebaluazioko batez besteko nota*).
5. **Modeloak sortu:**  
   Gainbegiratutako sailkapen-eredu bat entrenatu (adibidez, *Random Forest* edo *XGBoost*) ikasle bakoitzari arrisku-probabilitate bat (0tik 1era) esleitzeko. Zehaztasuna balioztatu (Precision/Recall).
6. **Emaitzak aurkeztu eta automatizatu:**  
   Zuzendaritza eta orientatzaileentzat Power BI / Web panel bat prestatu, eta astero automatikoki datu berriak kargatu eta arrisku-zerrenda eguneratzen duen pipeline-a martxan jarri.

---

## 5. OLTP ala OLAP?

| Egoera | Sistema Mota | Arrazoibidea |
|---|---|---|
| **Bezero batek ordainketa egiten du** | **OLTP** | Transakzio azkarra, ACID ezaugarriak behar ditu lerro bakar baten gainean. |
| **5 urteko salmentak aztertzea** | **OLAP** | Datu historikoen bolumen handia agregatu eta zutabeka kontsultatzen da. |
| **Produktu baten stocka eguneratzea** | **OLTP** | Inbentarioko errenkada baten balioa denbora errealean aldatzea. |
| **Zein hilabetetan saldu da gehien?** | **OLAP** | Hileko salmenta guztiak batu eta taldekatu (GROUP BY) behar dira. |
| **Bezero baten helbidea aldatzea** | **OLTP** | Erregistro espezifiko baten eguneratzea (UPDATE). |
| **Produktu bakoitzaren urteko batez besteko salmentak** | **OLAP** | Kalkulu estatistiko agregatuak datu-multzo handi batean. |
| **Eskari berri bat sortzea** | **OLTP** | Transakzio operatiboa (INSERT) bezeroaren erosketa erregistratzeko. |
| **Herrialde bakoitzeko salmentak konparatzea** | **OLAP** | Dimentsio geografikoaren araberako kontsulta analitiko konparatiboa. |

### Proposatutako 4 egoera berri:
1. **Kutxazain automatikotik 50 € ateratzea:** 👉 **OLTP** (Banku-kontuaren saldoa berehala zordundu eta eguneratu behar da).
2. **Azken 3 urteetako bezeroen galera-tasa (churn-rate) adinaren arabera kalkulatzea:** 👉 **OLAP** (Portaera-analisia milioika erregistrotan).
3. **Erabiltzaileak bere profileko pasahitza eguneratzea:** 👉 **OLTP** (Erabiltzaile baten erregistroa bakarrik ukitzen da).
4. **Gabonetako kanpainarako gehien batera erositako produktuen azterketa (Market Basket Analysis):** 👉 **OLAP** (Transakzio historiko guztien arteko loturak bilatzea).

---

## 6. E-commerce arkitektura. Proposamena

E-commerce enpresa baten beharrak:
- Txartel bidezko ordainketak denbora errealean.
- Azken 5 urteko salmenta-joerak aztertu.
- Hileko portaera-txostenak sortu.
- Inbentarioa denbora errealean kudeatu.

### Identifikazioa:
- **OLTP eragiketak:** Ordainketak denbora errealean kudeatzea eta inbentarioaren stock-aldaketak erregistratzea.
- **OLAP eragiketak:** 5 urteko joeren analisia eta hileko txosten analitikoak sortzea.

### Biltegiratze-soluzio proposamena:
**Arkitektura Hibridoa (Dual Engine / DWH geruza banatua):**
1. **Transakzio-geruza (OLTP):** PostgreSQL edo MariaDB cluster bat, erantzun-denbora baxuarekin eta transakzio-segurtasun osoarekin (ACID).
2. **Analitika-geruza (OLAP):** Data Warehouse zutabekaria (adibidez ClickHouse, Snowflake edo BigQuery), non datuak erregularki (ETL bidez) erreplikatzen diren.

### Zergatik ez litzateke sistema bakar bat nahikoa?
1. **Baliabideen lehia (Resource Contention):** OLAP kontsulta batek milioika lerro eskaneatzen dituenean, CPU eta I/O guztia erabil dezake. Datu-base bakarra balego, analista batek txosten bat ateratzerakoan bezeroen erosketak blokeatu edo moteldu egingo lirateke.
2. **Datuen egituraketa desberdina:** OLTP sistemek lerrokako egitura normalizatua behar dute (idazketa azkarretarako eta erredundantzia saihesteko); OLAP sistemek, berriz, zutabekako egitura desnormalizatua behar dute (irakurketa masibo eta agregazio azkarretarako).

---

## 7. Data Warehouse, Data Lake ala Data Lakehouse?

### A enpresa – Bankua
- **Hautatutako sistema:** **Data Warehouse (DWH)**
- **Justifikazioa:** Bankuek datu oso egituratuak dituzte (kontuak, transakzioak), araudi zorrotza bete behar dute, eta finantza-txostenetan zehaztasun osoa (ACID) behar dute.
- **Abantaila:** Datu-kalitate maximoa, segurtasun bikaina eta SQL kontsulta azkarrak.
- **Desabantaila:** Eskalatze garestia eta ez du onartzen audio/bideo edo formatu gordinik.

### B enpresa – Sare Soziala
- **Hautatutako sistema:** **Data Lake**
- **Justifikazioa:** Milaka milioi datu heterogeneo eta egituratu gabeak ditu (bideoak, argazkiak, testuak, JSON log-ak). Ezinbestekoa da fitxategiak beren jatorrizko formatuan merke gordetzea (adib. AWS S3 edo MinIO).
- **Abantaila:** Biltegiratze kostu oso txikia eta formatu aniztasun osoa onartzea.
- **Desabantaila:** Datuak antolatu gabe badaude oso zaila da kontsultak egitea eta ez dago eskema-kontrolik.

### C enpresa – Industria (IoT)
- **Hautatutako sistema:** **Data Lakehouse** (adibidez Delta Lake edo Apache Iceberg)
- **Justifikazioa:** Datu gordin masiboak (IoT sentsoreak) merke gorde behar ditu, baina aldi berean datuak eguneratu/ezabatu (ACID) eta analitika aurreratua zein Machine Learning egin nahi ditu plataforma berean.
- **Abantaila:** Data Lake-aren kostu baxua eta Data Warehouse-aren fidagarritasuna, ACID transakzioak eta eskema-kudeaketa uztartzen ditu.
- **Desabantaila:** Teknologia konplexuagoa da ezartzeko eta konfiguratzeko.

---

## 8. Data Lake -> Data Swamp (Datu-zingira)

### Zein arazo dago?
Enpresak **Data Swamp (Datu-zingira)** bat sortu du. Datuak kontrolik gabe, dokumentaziorik gabe eta metadaturik gabe bota dira. Horren ondorioz, inork ez daki zer datu dauden erabilgarri, datuak bikoiztuta daude, ezin dira aurkitu, eta ez dago jakiterik informazioa eguneratuta dagoen ala ez.

### Zer neurri proposatuko zenituzke?
1. **Datuen Gobernantza (Data Governance) ezarri:** Fitxategiak gordetzeko arautegia (izendapen-arauak, direktorio-egitura logikoa adib. *Bronze/Silver/Gold* arkitektura).
2. **Datu-katalogoa (Data Catalog):** Metadatuen biltegi bat txertatzea (adibidez Apache Atlas edo OpenMetadata) datuen jatorria (data lineage) eta esanahia indexatzeko.
3. **Eskema-erregistroa eta baliozkotzea:** Fitxategiak irenstean formatuak eta eskemak balioztatzea, datu hondatuak automatikoki baztertzeko.

### Zer informazio gorde beharko litzateke metadatuetan?
- **Teknikoak:** Fitxategi-izena, tamaina, formatua (JSON/CSV/Parquet), sorrera eta karga data/ordua, enkriptazio-mota.
- **Jatorria (Lineage):** Zein sentsore, zerbitzari edo aplikaziotatik datorren.
- **Negozioa:** Datu-jabea (Data Owner), erabilera-helburua, negozio-eremua.
- **Segurtasuna eta Pribatutasuna:** Datu pertsonalak (GDPR/LOPD) dituen ala ez, sailkapen-maila (Konfidentziala, Barnekoa, Publikoa).

---

## 9. Datu-rolak

| Egoera | Dagokion Rola |
|---|---|
| “Dashboard bat sortu du.” | **Datu-analista (Data Analyst)** |
| “ETL pipeline bat garatu du.” | **Datu-ingeniaria (Data Engineer)** |
| “Machine Learning modelo bat entrenatu du.” | **Datu-zientzialaria (Data Scientist)** |
| “Datuen arkitektura diseinatu du.” | **Datu-arkitektoa (Data Architect)** |
| “SQL erabiliz salmenten txostena prestatu du.” | **Datu-analista (Data Analyst)** |
| “Kafka eta cloud zerbitzuak integratu ditu.” | **Datu-ingeniaria (Data Engineer)** |
| “Datuen gobernantza eta segurtasun-politikak definitu ditu.” | **Datu-arkitektoa (Data Architect)** |
| “Salmenten aurreikuspen-modelo bat sortu du.” | **Datu-zientzialaria (Data Scientist)** |
