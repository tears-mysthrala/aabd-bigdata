#!/usr/bin/env python3
"""
Apache NiFi Fluxuen Diseinu eta Antolaketa Ederra (01etik 06ra).
Fluxu guztiak 07 laborategiaren maila berean lerrokatu, etiketatu eta
antolatzen ditu (Master Banner, Stage Banners, y: 180.0 baseline,
tarte uniformeak eta kolore harmonikoak).
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def update_flow(rel_path, master_title, master_desc, master_bg, stages, procs_layout):
    full_path = os.path.join(BASE_DIR, rel_path)
    if not os.path.isfile(full_path):
        print(f"⚠️ Ez da aurkitu: {full_path}")
        return

    with open(full_path, "r", encoding="utf-8") as f:
        flow = json.load(f)

    fc = flow["flowContents"]

    # 1. Update processor positions & comments
    p_map = {p["name"]: p for p in fc["processors"]}
    for name, (x, y, comments) in procs_layout.items():
        if name in p_map:
            p_map[name]["position"] = {"x": float(x), "y": float(y)}
            if comments:
                p_map[name]["comments"] = comments
        else:
            print(f"   ⚠️ Abisua: '{name}' prozesadorea ez da aurkitu hemen: {rel_path}")

    # 2. Reset connection bends to empty list (straight, beautiful lines)
    for c in fc["connections"]:
        c["bends"] = []

    # 3. Compute master banner width
    all_x = [pos[0] for pos in procs_layout.values()]
    max_x = max(all_x) + 380.0
    master_width = max(max_x - 60.0, 1350.0)

    # 4. Generate Master Banner + Stage Banners
    labels = []
    master_text = (
        f"╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗\n"
        f"║                                {master_title:<103} ║\n"
        f"╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝\n"
        f"• {master_desc}"
    )
    labels.append({
        "identifier": f"master-{os.path.basename(rel_path)}",
        "label": master_text,
        "position": {"x": 60.0, "y": 15.0},
        "width": float(master_width),
        "height": 75.0,
        "style": {"background-color": master_bg, "font-size": "12pt"}
    })

    for i, s in enumerate(stages):
        labels.append({
            "identifier": f"stage-{i}-{os.path.basename(rel_path)}",
            "label": s["title"],
            "position": {"x": float(s["x"]), "y": float(s["y"])},
            "width": float(s["width"]),
            "height": float(s.get("height", 45.0)),
            "style": {"background-color": s["bg"], "font-size": "11pt"}
        })

    fc["labels"] = labels

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(flow, f, indent=2)

    print(f"✅ Ederki eguneratua: {rel_path}")


def main():
    print("🎨 Fluxu guztiak 07 mailako diseinuarekin eguneratzen...")

    # =========================================================================
    # 01. FITXATEGIAK MUGITU & GATAZKAK
    # =========================================================================
    update_flow(
        rel_path="01_Fitxategiak_Mugitu_Gatazkak/flow_01_fitxategiak_mugitu.json",
        master_title="📁 LABORATEGIA 01: FITXATEGIEN TRANSFERENTZIA ETA GATAZKA KUDEAKETA",
        master_desc="Arkitektura: /sarrera monitorizatu ➔ /irteera karpetara eraman ➔ Bikoiztua bada, timestamp gehituz /gatazkak karpetan gorde",
        master_bg="#eaf2f8",
        stages=[
            {"title": "🟢 1. BIDERATZE ARRUNTA (SARRERA ➔ IRTEERA ZUZENA)", "x": 80.0, "y": 105.0, "width": 840.0, "bg": "#d5f5e3"},
            {"title": "⚠️ 2. GATAZKA ADARRA (FITXATEGI BIKOIZTUAK BERRIZENDATU & GORDE)", "x": 530.0, "y": 390.0, "width": 840.0, "bg": "#fcf3cf"}
        ],
        procs_layout={
            "FitxategiaEskuratu": (100.0, 180.0, "1. Sarrerako fitxategiak irakurri (/sarrera). Keep Source File=false."),
            "FitxategiaJarri": (550.0, 180.0, "2. Helmugan idatzi (/irteera). Izena badago -> failure bideratu."),
            "UpdateAttribute": (550.0, 460.0, "3. Gatazketan izen unikoa sortu timestamp erantsiz: ${now():toNumber()}-${filename}"),
            "GatazkaFitxategiaMugitu": (1000.0, 460.0, "4. Berrizendatutako fitxategia gatazkak karpetan gorde (/irteera/gatazkak).")
        }
    )

    # =========================================================================
    # 02. CSV DATUAK IRAGAZI (3 ALDAERA)
    # =========================================================================
    # Aldaera 1: SplitText (1 lerro)
    update_flow(
        rel_path="02_CSV_Datuak_Iragazi/flow_02_csv_datuak_iragazi_aldaera1.json",
        master_title="⚡ LABORATEGIA 02: CSV DATUAK IRAGAZI - ALDAERA 1: SPLITRECORD (1 LERRO/FLOWFILE)",
        master_desc="Arkitektura Klasikoa: CSV osoa lerroz lerro zatitu FlowFile indibidualetan ➔ SQL bidez adina >= 18 iragazi ➔ Diskoan gorde",
        master_bg="#fcf3cf",
        stages=[
            {"title": "📥 1. INGESTA", "x": 80.0, "y": 105.0, "width": 390.0, "bg": "#d6eaf8"},
            {"title": "✂️ 2. ZATIKETA (1 LERRO / FF)", "x": 530.0, "y": 105.0, "width": 390.0, "bg": "#fadbd8"},
            {"title": "🔍 3. SQL IRAGAZKETA", "x": 980.0, "y": 105.0, "width": 390.0, "bg": "#fcf3cf"},
            {"title": "🏷️ 4. METADATUAK", "x": 1430.0, "y": 105.0, "width": 390.0, "bg": "#eaeded"},
            {"title": "💾 5. BILTEGIRATZEA", "x": 1880.0, "y": 105.0, "width": 390.0, "bg": "#d5f5e3"}
        ],
        procs_layout={
            "CSVFitxategiaEskuratu": (100.0, 180.0, "1. Sarrerako CSV fitxategia irakurri (/sarrera karpeta)."),
            "CSVtikFFra": (550.0, 180.0, "2. Lerro bakoitzeko FlowFile bana sortu (Records Per Split = 1)."),
            "SQLkontsulta": (1000.0, 180.0, "3. Calcite SQL kontsulta: SELECT * FROM FLOWFILE WHERE CAST(adina AS INT) >= 18."),
            "FitxategiaBerrizendatu": (1450.0, 180.0, "4. Metadatuak ezarri: fitxategi izena ${filename:substringBeforeLast('.')}_nagusiak.csv."),
            "FitxategiaJarri": (1900.0, 180.0, "5. Iragazitako FlowFile-ak /irteera/aldaera1 karpetan gorde.")
        }
    )

    # Aldaera 2: SplitText (10 lerro)
    update_flow(
        rel_path="02_CSV_Datuak_Iragazi/flow_02_csv_datuak_iragazi_aldaera2.json",
        master_title="⚡ LABORATEGIA 02: CSV DATUAK IRAGAZI - ALDAERA 2: SPLITRECORD (10 LERROKO LOTEAK)",
        master_desc="Lote Txikiak: CSV fitxategia 10 lerroko mikroloteetan zatitu ➔ FlowFile kopurua %90 murriztu ➔ I/O eraginkortasuna",
        master_bg="#fcf3cf",
        stages=[
            {"title": "📥 1. INGESTA", "x": 80.0, "y": 105.0, "width": 390.0, "bg": "#d6eaf8"},
            {"title": "✂️ 2. ZATIKETA (10 LERRO / FF)", "x": 530.0, "y": 105.0, "width": 390.0, "bg": "#fdebd0"},
            {"title": "🔍 3. SQL IRAGAZKETA", "x": 980.0, "y": 105.0, "width": 390.0, "bg": "#fcf3cf"},
            {"title": "🏷️ 4. METADATUAK", "x": 1430.0, "y": 105.0, "width": 390.0, "bg": "#eaeded"},
            {"title": "💾 5. BILTEGIRATZEA", "x": 1880.0, "y": 105.0, "width": 390.0, "bg": "#d5f5e3"}
        ],
        procs_layout={
            "CSVFitxategiaEskuratu": (100.0, 180.0, "1. Sarrerako CSV fitxategia irakurri (/sarrera karpeta)."),
            "CSVtikFFra": (550.0, 180.0, "2. 10 lerroko loteak sortu FlowFile bakoitzean (Records Per Split = 10)."),
            "SQLkontsulta": (1000.0, 180.0, "3. Calcite SQL kontsulta: SELECT * FROM FLOWFILE WHERE CAST(adina AS INT) >= 18."),
            "FitxategiaBerrizendatu": (1450.0, 180.0, "4. Metadatuak ezarri: fitxategi izena ${filename:substringBeforeLast('.')}_loteak.csv."),
            "FitxategiaJarri": (1900.0, 180.0, "5. Iragazitako FlowFile-ak /irteera/aldaera2 karpetan gorde.")
        }
    )

    # Aldaera 3: Optimizatua (PartitionRecord / QueryRecord direct)
    update_flow(
        rel_path="02_CSV_Datuak_Iragazi/flow_02_csv_datuak_iragazi_aldaera3_optimizazioa.json",
        master_title="⚡ LABORATEGIA 02: CSV DATUAK IRAGAZI - ALDAERA 3: RECORD-ORIENTED OPTIMIZATUA",
        master_desc="Arkitektura Aurreratua: Fitxategia ZATITU GABE streamingean prozesatu ➔ RAM eta CPU eraginkortasun gorena (FlowFile bakarra!)",
        master_bg="#e8f8f5",
        stages=[
            {"title": "📥 1. INGESTA", "x": 80.0, "y": 105.0, "width": 390.0, "bg": "#d6eaf8"},
            {"title": "⚡ 2. STREAMING RECORD IRAGAZKETA", "x": 530.0, "y": 105.0, "width": 390.0, "bg": "#a3e4d7"},
            {"title": "🏷️ 3. METADATUAK", "x": 980.0, "y": 105.0, "width": 390.0, "bg": "#eaeded"},
            {"title": "💾 4. BILTEGIRATZEA", "x": 1430.0, "y": 105.0, "width": 390.0, "bg": "#d5f5e3"}
        ],
        procs_layout={
            "CSVFitxategiaEskuratu": (100.0, 180.0, "1. Sarrerako CSV fitxategia irakurri (/sarrera karpeta)."),
            "SQLkontsulta": (550.0, 180.0, "2. QueryRecord streaming zuzena (fitxategia zatitu gabe): SELECT * WHERE adina >= 18."),
            "FitxategiaBerrizendatu": (1000.0, 180.0, "3. Metadatuak ezarri: fitxategi izena ${filename:substringBeforeLast('.')}_optimizatua.csv."),
            "FitxategiaJarri": (1450.0, 180.0, "4. Emaitza /irteera/aldaera3 karpetan gorde FlowFile bakar batean.")
        }
    )

    # =========================================================================
    # 03. ATRIBUTUAK & DATU-LINAJEA (2 ALDAERA)
    # =========================================================================
    # Aldaera 1: Oinarrizkoa (Fitxategi-sistema)
    update_flow(
        rel_path="03_Atributuak_eta_Linajea/flow_03_atributuak_linajea.json",
        master_title="🏷️ LABORATEGIA 03: ATRIBUTUAK, PROVENANCE ETA DATU-LINAJEA (OINARRIZKOA)",
        master_desc="Arkitektura: FlowFile sortu ➔ Regex bidez atributuak atera ➔ Fitxategi-sisteman gorde ➔ Provenance auditatu (LogAttribute)",
        master_bg="#d5f5e3",
        stages=[
            {"title": "🚀 1. SORKUNTZA", "x": 80.0, "y": 105.0, "width": 390.0, "bg": "#d6eaf8"},
            {"title": "✏️ 2. TESTU ERALDAKETA", "x": 530.0, "y": 105.0, "width": 390.0, "bg": "#eaeded"},
            {"title": "🔍 3. ATRIBUTUAK ERAUZI", "x": 980.0, "y": 105.0, "width": 390.0, "bg": "#fcf3cf"},
            {"title": "💾 4. DISKOAN GORDE", "x": 1430.0, "y": 105.0, "width": 390.0, "bg": "#d5f5e3"},
            {"title": "📋 5. AUDITORIA & PROVENANCE (LOG ATTRIBUTE)", "x": 980.0, "y": 390.0, "width": 390.0, "bg": "#f9ebea"}
        ],
        procs_layout={
            "GenerateFlowFile": (100.0, 180.0, "1. Datu-korrontea simulatu 10 segundoro mezu testuarekin."),
            "ReplaceText": (550.0, 180.0, "2. Erabiltzailearen informazio egituratua gehitu testuan (izena, adina, hiria)."),
            "ExtractText": (1000.0, 180.0, "3. Regex erabiliz edukiko balioak FlowFile atributuetan gorde."),
            "PutFile": (1450.0, 180.0, "4. Eraldatutako fitxategia /irteera/lab03 karpetan gorde."),
            "LogAttribute": (1000.0, 460.0, "5. Atributuak eta Provenance metadatuak NiFi aplikazioaren log-ean idatzi.")
        }
    )

    # Aldaera 2: MongoDB NoSQL
    update_flow(
        rel_path="03_Atributuak_eta_Linajea/flow_03_atributuak_linajea_aldaera2_mongodb.json",
        master_title="🏷️ LABORATEGIA 03: ATRIBUTUAK ETA MONGODB NOSQL BILTEGIA (ALDAERA 2)",
        master_desc="Arkitektura: FlowFile sortu ➔ Regex erauzketa ➔ Atributuak JSON bihurtu ➔ MongoDB NoSQL bilduman txertatu",
        master_bg="#d5f5e3",
        stages=[
            {"title": "🚀 1. SORKUNTZA", "x": 80.0, "y": 105.0, "width": 390.0, "bg": "#d6eaf8"},
            {"title": "✏️ 2. TESTU ERALDAKETA", "x": 530.0, "y": 105.0, "width": 390.0, "bg": "#eaeded"},
            {"title": "🔍 3. ATRIBUTUAK ERAUZI", "x": 980.0, "y": 105.0, "width": 390.0, "bg": "#fcf3cf"},
            {"title": "🔄 4. ATRIBUTUAK -> JSON", "x": 1430.0, "y": 105.0, "width": 390.0, "bg": "#d5f5e3"},
            {"title": "🍃 5. MONGODB BILTEGIA", "x": 1880.0, "y": 105.0, "width": 390.0, "bg": "#a9dfbf"}
        ],
        procs_layout={
            "GenerateFlowFile": (100.0, 180.0, "1. Datu-korrontea simulatu 10 segundoro mezu testuarekin."),
            "ReplaceText": (550.0, 180.0, "2. Informazio egituratua testuan gehitu."),
            "ExtractText": (1000.0, 180.0, "3. Regex erabiliz balioak FlowFile atributu bihurtu."),
            "AttributesToJSON": (1450.0, 180.0, "4. Atributu hautatuak JSON dokumentu garbi bihurtu edukian."),
            "PutMongo": (1900.0, 180.0, "5. JSON dokumentua MongoDB 3kasua bilduman zuzenean txertatu.")
        }
    )

    # =========================================================================
    # 04. HTTP INGESTA & MONGODB
    # =========================================================================
    update_flow(
        rel_path="04_HTTP_Ingesta_eta_MongoDB/flow_04_mongodb_http.json",
        master_title="🌐 LABORATEGIA 04: HTTP REST INGESTA, ERRORE BIDERAKETA ETA MONGODB NOSQL",
        master_desc="Arkitektura: HTTP POST entzun (8081) ➔ Regex errore detekzioa ➔ Loteak batu (MergeContent) ➔ Parsing & MongoDB biltegiratzea",
        master_bg="#e8f8f5",
        stages=[
            {"title": "🌐 1. FASEA: HTTP REST INGESTA, ERRORE DETEKZIOA & BATCHING (PORT: 8081 /sarrera)", "x": 80.0, "y": 105.0, "width": 1290.0, "bg": "#d6eaf8"},
            {"title": "🍃 2. FASEA: PARSING, METADATUAK, JSON ERALDAKETA & MONGODB BILTEGIRATZEA", "x": 980.0, "y": 390.0, "width": 1740.0, "bg": "#d5f5e3"}
        ],
        procs_layout={
            "ListenHTTP": (100.0, 180.0, "1. Kanpoko HTTP POST eskaerak jaso /sarrera helbidean (Portua: 8081)."),
            "RouteOnContent": (550.0, 180.0, "2. Edukian .*ERROR.* regex bilatu. Errore mezuak bakarrik bideratu hurrengo fasera."),
            "MergeContent": (1000.0, 180.0, "3. Errore mezuak lote txikietan multzokatu Bin-Packing algoritmoarekin."),
            "ExtractText": (1000.0, 460.0, "4. Lotearen edukia atributuetara erauzi parsing errazagoa egiteko."),
            "UpdateAttribute": (1450.0, 460.0, "5. Metadatuak erantsi: ingesta_data eta larritasuna = 'KRITIKOA'."),
            "AttributesToJSON": (1900.0, 460.0, "6. Atributuekin MongoDB-rako JSON dokumentua prestatu."),
            "PutMongo": (2350.0, 460.0, "7. Errore dokumentua MongoDB iabd.4kasua bilduman gorde.")
        }
    )

    # =========================================================================
    # 05. CSV -> JSON CONVERTRECORD (DF 2.1)
    # =========================================================================
    update_flow(
        rel_path="05_CSV_JSON_ConvertRecord_DF2.1/flow_05_csv_json_df2.1.json",
        master_title="🔄 LABORATEGIA 05: CSV ➔ JSON CONVERTRECORD (RECORD-ORIENTED STREAMING - DF 2.1)",
        master_desc="Arkitektura: CSV sarrera irakurri ➔ Kontrolagailu-zerbitzuak erabiliz streaming formatu bihurketa (CSVReader ➔ JsonRecordSetWriter)",
        master_bg="#eaf2f8",
        stages=[
            {"title": "📥 1. CSV FITXATEGIA (GETFILE)", "x": 80.0, "y": 105.0, "width": 390.0, "bg": "#d6eaf8"},
            {"title": "🔄 2. CONVERTRECORD (STREAMING RECORD API)", "x": 530.0, "y": 105.0, "width": 390.0, "bg": "#aed6f1"},
            {"title": "🏷️ 3. METADATUAK (.json BARRIA)", "x": 980.0, "y": 105.0, "width": 390.0, "bg": "#eaeded"},
            {"title": "💾 4. JSON BILTEGIRATZEA (PUTFILE)", "x": 1430.0, "y": 105.0, "width": 390.0, "bg": "#d5f5e3"}
        ],
        procs_layout={
            "GetFile": (100.0, 180.0, "1. Sarrerako bezeroen CSV fitxategia irakurri (/sarrera karpeta)."),
            "ConvertRecord": (550.0, 180.0, "2. CSVReader -> JsonRecordSetWriter bihurketa azkarra memoriako streamingean."),
            "UpdateAttribute": (1000.0, 180.0, "3. Luzapena aldatu: ${filename:substringBeforeLast('.')}.json."),
            "PutFile": (1450.0, 180.0, "4. Sortutako JSON fitxategia /irteera/json karpetan gorde.")
        }
    )

    # =========================================================================
    # 06. MARIADB & MONGODB LAB (DF 2.2) (2 KASU)
    # =========================================================================
    # Kasu 6: Klasikoa (SplitText / ExtractText)
    update_flow(
        rel_path="06_MariaDB_MongoDB_Laborategia_DF2.2/flow_06_mariadb_mongodb_classic.json",
        master_title="🗄️ LABORATEGIA 06: MARIADB (SQL) ➔ MONGODB (NOSQL) - KASU 6: KLASIKOA (DF 2.2)",
        master_desc="Arkitektura Klasikoa: SQL kontsulta ➔ 12.435 FlowFile sortu SplitText bidez ➔ Banan-banan MongoDB-n txertatu (I/O eta CPU astuna)",
        master_bg="#fadbd8",
        stages=[
            {"title": "🐬 1. MARIADB SQL (DBCP POOL)", "x": 80.0, "y": 105.0, "width": 390.0, "bg": "#d6eaf8"},
            {"title": "✂️ 2. TESTU ZATIKETA (12.435 FLOWFILE ILARAN)", "x": 530.0, "y": 105.0, "width": 390.0, "bg": "#fadbd8"},
            {"title": "🍃 3. MONGODB TXERTAKETA BANAN-BANAN", "x": 980.0, "y": 105.0, "width": 390.0, "bg": "#f9ebea"}
        ],
        procs_layout={
            "ExecuteSQLRecord_Customers": (100.0, 180.0, "1. MariaDB datu-basetik 12.435 bezero atera SQL bidez."),
            "SplitText_Lines": (550.0, 180.0, "2. Fitxategia lerroz lerro zatitu (12.435 FlowFile sortzen dira ilaran!)."),
            "PutMongo_Classic": (1000.0, 180.0, "3. FlowFile bakoitza banan-banan MongoDB customers_classic bilduman txertatu.")
        }
    )

    # Kasu 6: Record-Oriented (PutMongoRecord)
    update_flow(
        rel_path="06_MariaDB_MongoDB_Laborategia_DF2.2/flow_06_mariadb_mongodb_record.json",
        master_title="🗄️ LABORATEGIA 06: MARIADB (SQL) ➔ MONGODB (NOSQL) - KASU 6: RECORD-ORIENTED (DF 2.2)",
        master_desc="Arkitektura Aurreratua: SQL kontsulta ➔ FlowFile BAKARRA ➔ PutMongoRecord bidez bulk streaming zuzena (%90 azkarragoa!)",
        master_bg="#d5f5e3",
        stages=[
            {"title": "🐬 1. MARIADB SQL (DBCP POOL)", "x": 80.0, "y": 105.0, "width": 390.0, "bg": "#d6eaf8"},
            {"title": "🍃 2. MONGODB RECORD STREAMING (FLOWFILE BAKARRA)", "x": 630.0, "y": 105.0, "width": 450.0, "bg": "#a9dfbf"}
        ],
        procs_layout={
            "ExecuteSQLRecord_Customers": (100.0, 180.0, "1. MariaDB datu-basetik bezeroak atera DBCP konexio-igerilekuaren bidez."),
            "PutMongoRecord_Direct": (650.0, 180.0, "2. FlowFile bakarrean 12.435 erregistroak zuzenean MongoDB-ra kargatu Record API bidez.")
        }
    )

    print("\n🎉 FLUXU GUZTIAK EDERKI EGUNERATU DIRA!")

if __name__ == "__main__":
    main()
