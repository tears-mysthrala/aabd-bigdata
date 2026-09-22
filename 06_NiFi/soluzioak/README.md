# AABD - 03 DataFlow: Apache NiFi Ariketa eta Ebazpen Nagusia

> **Modulua:** Big Data Aplikatua (5073 / DataFlow)  
> **Ingurunea:** Apache NiFi 2.0.0, Docker Compose, MySQL 8.4, MongoDB 7.0, Nginx SSL  
> **UI Sarbidea:** `https://nifi.bigdata.local/nifi` (edo erreserban: `https://localhost:8443/nifi`)

Dokumentu honek Apache NiFi moduluko ariketa, fluxu eta laborategi guztiak biltzen ditu, modu modular, garbi eta profesionalean antolatuta.

---

## 📂 Direktorioen Egitura Estandarizatua

```
soluzioak/03_DataFlow_Apache_NiFi/
├── 📁 01_Fitxategiak_Mugitu_Gatazkak/             # 1. Kasua: Sarrera -> Irteera + Gatazkak kudeatu
│   ├── flow_01_fitxategiak_mugitu.json
│   ├── README.md
│   └── sarrera/ (proba fitxategiak)
├── 📁 02_CSV_Datuak_Iragazi/                      # 2. Kasua: salmentak.csv iragazketa (3 aldaera)
│   ├── flow_02_csv_datuak_iragazi_aldaera1.json   #   Aldaera 1: SplitRecord 1 errenkada
│   ├── flow_02_csv_datuak_iragazi_aldaera2.json   #   Aldaera 2: SplitRecord 10 errenkada
│   ├── flow_02_csv_datuak_iragazi_aldaera3_optimizazioa.json # Aldaera 3: Optimizatua (Split gabe)
│   ├── simulatu_kasu_2_salmentak.py
│   ├── README.md
│   ├── sarrera/salmentak.csv
│   └── irteera/salmentak_iragaziak.csv
├── 📁 03_Atributuak_eta_Linajea/                  # 3. Kasua: Edukia vs Atributuak, Lineage & Mongo
│   ├── flow_03_atributuak_linajea.json            #   Aldaera 1: LogAttribute + Provenance
│   ├── flow_03_atributuak_linajea_aldaera2_mongodb.json # Aldaera 2: AttributesToJSON + PutMongo
│   └── README.md
├── 📁 04_HTTP_Ingesta_eta_MongoDB/                 # 4. Kasua: Webhook ListenHTTP + Error routing
│   ├── flow_04_mongodb_http.json
│   └── README.md
├── 📁 05_CSV_JSON_ConvertRecord_DF2.1/            # 5. Kasua / DF2.1: Prozesu-talde modularra
│   ├── flow_05_csv_json_df2.1.json
│   ├── README.md
│   └── sarrera/datuak.csv
├── 📁 06_MariaDB_MongoDB_Laborategia_DF2.2/       # 6. Kasua / DF2.2: RDBMS -> NoSQL (Bi aldaera)
│   ├── flow_06_mariadb_mongodb_classic.json       #   Aldaera 1: SplitText + PutMongo
│   ├── flow_06_mariadb_mongodb_record.json        #   Aldaera 2: PutMongoRecord (Direct Bulk)
│   ├── DF2.2_konparaketa_oharra.md                #   Errendimendu txostena (>64x azkarrago)
│   ├── docker-compose.yml, Dockerfile.nifi, create_db.sql, redeploy.sh...
│   └── README.md
├── 📁 07_AEMET_Datu_Lakua_Medallion_DF2.3/        # 7. Kasua / DF2.3: Medallion Data Lake
│   ├── flow_07_aemet_datalake_medallion.json      #   Bronze -> Silver -> Gold (FS + Mongo)
│   └── README.md
└── 📁 scripts/                                    # Automatizazio eta laguntza script-ak
    ├── inportatu_fluxuak.py                       #   REST API bidezko inportatzailea
    ├── nifi_api_helper.sh                         #   CLI laguntzailea (token, start, stop)
    ├── reset_samples.sh                           #   Lagin fitxategiak berrezartzeko scripta
    └── test_environment.sh                       #   Ingurunearen auto-egiaztapen osoa
```

---

## 📊 Kasu eta Fluxuen Taula Nagusia

| Kasua | Izena eta Fitxategia | Ariketa Kodea | Helburua | Prozesadore Nagusiak | Kontroladore Zerbitzuak |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **1** | [**01_Fitxategiak_Mugitu_Gatazkak**](file:///home/tears/bigdata/soluzioak/03_DataFlow_Apache_NiFi/01_Fitxategiak_Mugitu_Gatazkak/README.md) | Kasu 1 | Fitxategiak mugitu eta gatazkak timestamp bidez kudeatu | `GetFile`, `PutFile`, `UpdateAttribute` | - |
| **2** | [**02_CSV_Datuak_Iragazi**](file:///home/tears/bigdata/soluzioak/03_DataFlow_Apache_NiFi/02_CSV_Datuak_Iragazi/README.md) | Kasu 2 | Salmentak iragazi (`France` eta `Units > 1`) 3 arkitekturatan | `GetFile`, `SplitRecord`, `QueryRecord`, `UpdateAttribute`, `PutFile` | `CSVReader`, `CSVRecordSetWriter` |
| **3** | [**03_Atributuak_eta_Linajea**](file:///home/tears/bigdata/soluzioak/03_DataFlow_Apache_NiFi/03_Atributuak_eta_Linajea/README.md) | Kasu 3 | Edukitik atributuak erauztea, log-ak, datuen linajea eta MongoDB karga | `GenerateFlowFile`, `ReplaceText`, `ExtractText`, `LogAttribute`, `AttributesToJSON`, `PutMongo` | `MongoDBControllerService` |
| **4** | [**04_HTTP_Ingesta_eta_MongoDB**](file:///home/tears/bigdata/soluzioak/03_DataFlow_Apache_NiFi/04_HTTP_Ingesta_eta_MongoDB/README.md) | Kasu 4 | Webhook HTTP bidezko sarrera, errore-bideraketa eta lote-karga | `ListenHTTP`, `RouteOnContent`, `MergeContent`, `ExtractText`, `AttributesToJSON`, `PutMongo` | `MongoDBControllerService` |
| **5** | [**05_CSV_JSON_ConvertRecord**](file:///home/tears/bigdata/soluzioak/03_DataFlow_Apache_NiFi/05_CSV_JSON_ConvertRecord_DF2.1/README.md) | **DF2.1** | CSV JSON bihurtzea prozesu-talde modular batean (`Input/Output Port`) | `GetFile`, `ConvertRecord`, `UpdateAttribute`, `PutFile` | `CSVReader`, `JsonRecordSetWriter` |
| **6** | [**06_MariaDB_MongoDB_Laborategia**](file:///home/tears/bigdata/soluzioak/03_DataFlow_Apache_NiFi/06_MariaDB_MongoDB_Laborategia_DF2.2/README.md) | **DF2.2** | RDBMS-tik NoSQL-ra: Klasikoa (`SplitText`) vs Modernoa (`Record API`) | `ExecuteSQLRecord`, `SplitText`, `PutMongo`, `PutMongoRecord` | `DBCPConnectionPool`, `JsonRecordSetWriter`, `JsonTreeReader`, `MongoDBControllerService` |
| **7** | [**07_AEMET_Datu_Lakua_Medallion**](file:///home/tears/bigdata/soluzioak/03_DataFlow_Apache_NiFi/07_AEMET_Datu_Lakua_Medallion_DF2.3/README.md) | **DF2.3** | AEMET telemetria datu-lakua (Bronze $\rightarrow$ Silver $\rightarrow$ Gold) | `GenerateFlowFile`, `UpdateAttribute`, `EvaluateJsonPath`, `AttributesToJSON`, `MergeContent`, `QueryRecord`, `PutFile`, `PutMongo`, `PutMongoRecord` | `MongoDBControllerService`, `ParquetReader`, `ParquetRecordSetWriter` |

---

## 🛠️ Diseinu Estandarrak eta Hobekuntzak

1. **Koordenatu Ortogonal Garbiak:**
   - Prozesadore guztiak ezkerretik eskuinera (`dx = 400px`) edo goitik behera ordenatu dira.
   - Gezi atzerakoiak (*backwards loops*) eta marra gurutzatuak ezabatu dira.
   - Koordenatu negatiboak guztiz zuzendu dira.
2. **Prozesadoreen Iruzkinak (Comments):**
   - Prozesadore bakoitzak bere funtzioa deskribatzen duen testu argigarria du NiFi-ren barruan.
3. **Prozesu-taldeen Kapsulazioa:**
   - NiFi 2.0 formatuko JSON fitxategietan Controller Service guztiak txertatuta daude, inportazioa 100% autonomoa izan dadin.
4. **Scripts eta Automatizazioa:**
   - `scripts/inportatu_fluxuak.py` tresnarekin NiFi REST API-ra konektatu eta edozein fluxu aztertu edo inportatu daiteke komando bidez.
