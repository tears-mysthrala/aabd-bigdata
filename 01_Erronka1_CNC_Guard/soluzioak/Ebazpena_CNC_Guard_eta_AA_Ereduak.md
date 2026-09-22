# Erronka 1 (CNC Guard) eta AA Ereduak (5071) - Laburpen eta Ebazpen Teknikoa

Moduluak: **Adimen Artifizialaren Ereduak (5071)** eta **Erronka 1: CNC Guard**  
Kokatuta: `04_Erronka1_CNC_Guard_eta_AA_Ereduak`

---

## 1. Erronkaren Testuingurua: CNC Guard (Mantentze Prediktiboa)

### Helburua
Fabrika bateko zenbakizko kontrol bidezko (CNC) frexatzeko makinetan sentsoreen datuak (tenperatura, bibrazioa, erremintaren higadura, momentua) monitorizatzea eta **matxurak gertatu baino lehen** detektatzea, ekoizpen-geldialdi garestiak saihesteko.

---

## 2. AAren Paradigmen Aplikazioa CNC Guard proiektuan

Teorian ikusitako hiru paradigmen arabera:

| Paradigma | Nola aplikatzen da CNC Guard-en? | Algoritmo/Tresna Adibidea |
|---|---|---|
| **1. Paradigma Sinbolikoa (Arau-sistemak & Logika Lausoa)** | Esperientziaz ezagutzen diren muga finkoak eta arrazoibide kualitatiboa: *"Bibrazioa ALTUA bada eta Tenperatura OSO BEROA bada, orduan Arrisku Kritikoa"* | **Logika Lausoa (Fuzzy Logic - scikit-fuzzy)** |
| **2. Paradigma Konexonista (Machine Learning & Deep Learning)** | Datu historikoetatik matxura-eredu konplexuak ikastea (adib. AI4I dataset-a erabiliz) | **Random Forest, XGBoost, LSTM (denbora-serieak)** |
| **3. AA Sortzailea (Generative AI & LLMs)** | Operadorearentzako diagnostiko naturaleko txostenak idaztea eta gomendioak sortzea | **LLM Laguntzaile Lokala (RAG bidez)** |

---

## 3. Logika Lausoaren (Fuzzy Logic) Diseinua: Sentsoreen Fusioa

Balio boolear zorrotzak erabili beharrean (adib. $T > 75^\circ C \to \text{Matxura}$), Logika Lausoak giza aditu baten moduan arrazoitzen du pertenentzia-funtzioen (*membership functions*) bidez:

1. **Sarrera-aldagaiak (Inputs):**
   - **Tenperatura (°C):** `[Hotza, Normala, Beroa, Gehiegizkoa]`
   - **Bibrazioa (mm/s):** `[Baxua, Onargarria, Arriskutsua]`
   - **Higadura (minutuak):** `[Berria, Erabilia, Zaharra]`
2. **Irteera-aldagaia (Output):**
   - **Makina-Osasuna / Arrisku-Maila (%):** `[Normala (0-30%), Kautela (30-70%), Gelditu Berehala (70-100%)]`
3. **Arau-basea (Fuzzy Rules):**
   - *IF Tenperatura Beroa AND Bibrazioa Arriskutsua THEN Arrisku-Maila Gelditu Berehala.*
   - *IF Higadura Zaharra AND Bibrazioa Onargarria THEN Arrisku-Maila Kautela.*

---

## 4. Datu-Multzoen Garbiketa eta Prestaketa (Data Science integrazioa)

`5073_2_Datu_Zientzia_Ariketak` koadernoan ebatzitako estrategiak CNC Guard-en aplikatuz:
1. **Outlier-ak ezabatzea:** Sentsoreen deskonexioek sortutako datu anomaloak (adib. 999 °C edo balio negatiboak) medianarekin edo zeroarekin ordezkatzea.
2. **Datu galduak (NaN):** Neurketa hutsak ezabatzea (`.dropna()`) edo aldameneko balioekin interpolatzea.
3. **Ezaugarri berriak (Feature Engineering):**
   - Batez besteko mugikorra (*rolling mean*) azken 5 minutuko leihoan.
   - Bibrazioaren desbiderapen estandarra (makinaren ezegonkortasun-adierazle nagusia).

---

## 5. Entregagaien Egitura eta Dokumentazioa (Anexoak)

- **ANEXO 1 (Talde Kontratua):** Taldekideen arteko konpromisoak, rol banaketa (Data Engineer, Data Scientist, Sysadmin) eta barne-arauak.
- **ANEXO 4 (Behin Betiko Proposamena):** Proposatutako arkitektura teknikoa (Sentsoreak -> MQTT/NiFi -> InfluxDB/MongoDB -> Streamlit/Grafana UI -> ML Modeloa) eta proiektuaren bideragarritasun-analisia.
