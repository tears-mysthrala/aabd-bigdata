# DF2.2 Ariketa: 6. Kasua — MariaDB → MongoDB Konparaketa-Oharra

## 1. Testuingurua eta Helburua
Ariketa honetan `retail_db` erlazionaleko (`customers` taula) datuak MariaDB/MySQLtik MongoDB dokumentu-datu-basera transferitu dira Apache NiFi bidez, bi arkitektura eta aldaera desberdin erabiliz:
1. **1. Aldaera (Klasikoa):** `ExecuteSQLRecord` → `SplitText` → `PutMongo` (Bilduma: `6kasua-classic`)
2. **2. Aldaera (Modernoa / Record API):** `ExecuteSQLRecord` → `PutMongoRecord` (Bilduma: `6kasua-record`)

---

## 2. Arkitektura eta Diseinuaren Konparaketa

| Ezaugarria | 1. Aldaera: Klasikoa (`SplitText` + `PutMongo`) | 2. Aldaera: Record API (`PutMongoRecord`) |
| :--- | :--- | :--- |
| **Prozesadore kopurua** | 3 (`ExecuteSQLRecord`, `SplitText`, `PutMongo`) | 2 (`ExecuteSQLRecord`, `PutMongoRecord`) |
| **Bitarteko FlowFile kopurua** | $N$ FlowFile (errenkada bakoitzeko FlowFile bat) | FlowFile **bakarra** (NDJSON formatuan) |
| **Kontroladore Zerbitzuak** | `DBCPConnectionPool`, `JsonRecordSetWriter`, `MongoDBControllerService` | `DBCPConnectionPool`, `JsonRecordSetWriter`, `JsonTreeReader`, `MongoDBControllerService` |
| **Diseinuaren konplexutasuna** | Handiagoa (banaketa-etapa gehigarria eta ilara-kudeaketa) | Txikiagoa eta garbiagoa (datu-korronte jarraitua) |
| **MongoDB eragiketa mota** | Banakako dokumentu txertaketa (`insert` per FlowFile) | Bulk / Batch txertaketa efizientea |

---

## 3. Errendimenduaren eta Baliabideen Analisia

### 1. Aldaera: SplitText bidezko eragina
* **FlowFile Gainkarga (Overhead):** Errenkada bakoitzeko FlowFile berri bat sortzen denez, FlowFile Repository eta Provenance Repository biltegietan I/O eragiketa kopuru izugarria sortzen da.
* **Memoria eta Garbiketa (GC):** Milaka FlowFile aldi berean ilaran egoteak JVM Heap memorian presio handia sortzen du eta Garbage Collector-ak denbora-tarte luzeagoak behar izaten ditu.
* **Latentzia:** MongoDB-ra doazen eskaerak indibidualki edo lote txikitan egiten direnez, sare-eragiketen latentzia handiagoa da.

### 2. Aldaera: Record API bidezko hobekuntza
* **Eraginkortasun Handia:** Datu guztiak FlowFile bakar baten barruan bidaiatzen dute errekor-egitura moduan (`JsonTreeReader`).
* **Batch Insertion:** `PutMongoRecord`-ek lote bidezko txertaketa masiboa (`bulk insert`) egiten du MongoDB-n, sare-eskaeren kopurua magnitude-ordenetan murriztuz.
* **Gure probetako emaitza enpirikoa:** 
  * `6kasua-classic`: Proba-tarte berean 2.508 dokumentu txertatu ditu banan-banan.
  * `6kasua-record`: Proba-tarte berean 160.600 dokumentu txertatu ditu lote masiboetan errore gabe.

---

## 4. Ondorioak eta Gomendioak
* **Produkzioko gomendioa:** Datu-base integrazio masiboetan (RDBMS → NoSQL / DWH), **Record API (`PutMongoRecord`)** da aukera egokiena eta profesionalena, baliabideen kontsumoa murrizten duelako eta abiadura esponentzialki handitzen duelako.
* **Noiz erabili SplitText:** Soilik errenkada bakoitzak fluxu-adar independente bat behar duenean (adibidez, bideraketa konplexuak edota kanpoko API bidezko aberaste indibiduala behar duenean).
