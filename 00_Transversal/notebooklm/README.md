# AABD Big Data & IA - NotebookLM Konfigurazioa eta Materialak

Repositorio honetan Google NotebookLM zerbitzuarekin sinkronizatutako baliabide guztiak, iturriak eta sortutako ikasketa-artefaktuak biltzen dira.

---

## 🌐 NotebookLM Koaderno Nagusia
- **Izena:** `AABD Big Data & IA - Kurtsoa eta Erronkak`
- **Notebook ID:** `3db48c6c-0f7a-43c6-b9d0-0ae3b88be9d2`
- **Sarbide Zuzena (Web):** [NotebookLM - AABD Big Data & IA](https://notebooklm.google.com/notebook/3db48c6c-0f7a-43c6-b9d0-0ae3b88be9d2)
- **Google Kontua:** (privado — no se publica)

---

## 📦 Sortutako eta Deskargatutako Ikasketa-Modulu Guztiak (100% Osatuta)

Guztiak NotebookLM bidez sortu dira eta lokalean gordeta daude:

| Módulo / Artefacto | Archivo Local | Tamaño | Descripción |
| :--- | :--- | :--- | :--- |
| 🎧 **Audio Podcast** | [`Podcast_AABD_IA_Averias_Industriales.m4a`](Podcast_AABD_IA_Averias_Industriales.m4a) | 46 MB | *"IA para predecir averías industriales silenciosas"*. Conversación completa en español sobre mantenimiento predictivo y ML. |
| 🎬 **Vídeo Overview** | [`Video_AABD_BigData_MachineLearning.mp4`](Video_AABD_BigData_MachineLearning.mp4) | 34 MB | *"Big Data y Machine Learning"*. Vídeo explicativo y estructurado de los módulos del curso. |
| 📄 **Guía de Estudio** | [`Guia_Estudio_AABD.md`](Guia_Estudio_AABD.md) | 6.1 KB | Síntesis de conceptos fundamentales: NiFi, Medallion, paradigmas de IA y CNC Guard. |
| 🃏 **Flashcards** | [`Flashcards_AABD.md`](Flashcards_AABD.md) | 9.1 KB | +480 líneas con tarjetas de preguntas/respuestas de memorización activa. |
| 📝 **Quiz de Autoevaluación**| [`Quiz_AABD.md`](Quiz_AABD.md) | 4.3 KB | Test de autoevaluación con respuestas justificadas (DAGs, 7V, ELT vs ETL, etc.). |
| 🧠 **Mapa Mental** | [`MindMap_AABD.json`](MindMap_AABD.json) | 2.8 KB | Nodos conceptuales interconectados de las asignaturas y retos. |

---

## 📚 Koadernoan Kargatutako Iturriak (32 Iturri Guztira)

### 1. 00 - Orokorra eta Programazioa
- `00 - Programazio Didaktikoa AA 2026-2027` (PDF)
- `00 - AABD Materialen Aurkibidea` (Markdown)

### 2. 01 - Erronka 1: CNC Guard
- `1Erronka_ikaslearen_txostena.docx.pdf` (Erronkaren gida nagusia)
- `patata tortila - planifikazioa eta kostuak lantzekoAA 2026-2027.md` (PERT eta Gantt)
- `ANEXO1-Eus.md` (Talde konpromisoak eta rolak)
- `Ebazpena_CNC_Guard_eta_AA_Ereduak.md` (CNC Guard erronkaren ebazpen integrala)

### 3. 02 - AA Ereduak (5071)
- `5071-IE1-Sarrera_Kontzeptuala.md` (AAren paradigmak: Sinbolikoa, Konexonista, Sortzailea)
- `5071-IE1-Logika_Lausoa.md` (Fuzzy Logic: kide-funtzioak, arau-baseak eta defuzzification)
- `E1-Ereduak-Aurkezpena.pdf` (Diapositibak)
- `E1-Ereduak-Sarrera.pdf` (Sarrera teorikoa)

### 4. 03 - Machine Learning / Ikaskuntza Automatikoa (5072)
- `5072_00_Sarrera.pdf` (ML oinarriak)
- `5072_1_Datua_eta_Aurreprozesamenua.pdf` & `ppt` (Datuen garbiketa, outliereak, imputazioa)
- `5072_2_Ikasketa_Gainbegiratua.pdf` & `ppt` (Erregresioa, sailkapena, metriken ebaluazioa)

### 5. 04 - Lengoaiak eta Datu Zientzia (5073)
- `5073_1_Lengoaiak.pdf` (Python anatomia, Git, venv, JSON/YAML/XML)
- `5073_2_Datu_Zientzia.pdf` (NumPy bektorializazioa, Pandas, Seaborn bistaratzea)
- `Ariketa Ebatzien Aurkibidea` (`soluzioak/README.md`)
- `AGENTS.md` (Agente eta Prompt Ingeniaritza arauak)

### 6. 05 - Big Data eta Datuen Ingeniaritza
- `01_01_big_data_sarrera.pdf` & Ariketak (Big Data 7 V-ak, OLAP vs OLTP, Data Lake)
- `01_02_datuen_ingeniaritza.pdf` & Ariketak (Datuen bizi-zikloa, Lakehouse, ETL vs ELT)
- Ebazpen dokumentu osoak (7V Spotify kasua, E-commerce arkitektura, Smart Factory 500 sentsore)

### 7. 06 - Apache NiFi eta DataFlow Ingesta
- `Software instalazioak.pdf` (Docker, NiFi, MariaDB, MongoDB)
- `01_01_ApacheNifi.pdf` & `01_02_ApacheNifi_aurreratua.pdf`
- `GIDA Apache NiFi instalazioa eta kasu praktikoak 1-2-3-4.pdf`
- Ariketa ebatzien txostenak (FlowFiles, QueryRecord, ConvertRecord, Linajea, AEMET Medallion Lakehouse)

---

## 🛠️ Nola kudeatu NotebookLM terminaletik (CLI)

`notebooklm-py` tresna konfiguratuta dago eta zuzenean erabil daiteke terminalean:

```bash
# Galdera bat egin koadernoko material guztiak oinarri hartuta:
notebooklm ask "¿Cómo se implementa la lógica difusa en el reto de monitorización de CNC Guard?"

# Koadernoaren egoera ikusi:
notebooklm status

# Artefaktu berriak sortu edo deskargatu:
notebooklm generate audio "Enfócate en la comparación entre ETL y ELT"
notebooklm download audio --latest ./audio_nuevo.m4a
```
