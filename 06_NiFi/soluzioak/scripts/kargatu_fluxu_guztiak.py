#!/usr/bin/env python3
"""
Apache NiFi 2.0 - Fluxu Guztiak Kargatzeko eta Antolatzeko Script-a.
Ariketa guztiak (01etik 07ra) NiFi-ren oihalean (canvas) profesionalki
antolatzen ditu, etiketekin, koloreekin eta azalpen argiekin.
"""

import os
import sys
import json
import uuid
import urllib.request
import urllib.error
import ssl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, "06_MariaDB_MongoDB_Laborategia_DF2.2", ".env")

# SSL testuingurua tokiko zerbitzarirako
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def load_env():
    creds = {
        "NIFI_USER": "nifi",
        "NIFI_PASSWORD": "",
        "NIFI_URL": "https://localhost:8443",
        "MYSQL_USER": "iabd",
        "MYSQL_PASSWORD": ""
    }
    if os.path.isfile(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    creds[k] = v
    return creds

CREDS = load_env()
NIFI_URL = os.environ.get("NIFI_URL", CREDS.get("NIFI_URL", "https://localhost:8443"))

def api_call(endpoint, method="GET", data=None, token=None, content_type="application/json"):
    url = f"{NIFI_URL}/nifi-api{endpoint}"
    headers = {"Content-Type": content_type}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    body = None
    if data is not None:
        if isinstance(data, (dict, list)):
            body = json.dumps(data).encode("utf-8")
        elif isinstance(data, str):
            body = data.encode("utf-8")
        elif isinstance(data, bytes):
            body = data

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx) as res:
            res_data = res.read().decode("utf-8")
            try:
                return json.loads(res_data)
            except Exception:
                return res_data
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        print(f"❌ HTTP Error ({e.code}) {endpoint}: {err[:300]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Connection Error {endpoint}: {e}", file=sys.stderr)
        return None

def get_token():
    payload = f"username={CREDS['NIFI_USER']}&password={CREDS['NIFI_PASSWORD']}"
    res = api_call("/access/token", method="POST", data=payload, content_type="application/x-www-form-urlencoded")
    if res and isinstance(res, str) and res.startswith("ey"):
        return res
    raise RuntimeError("Ezin izan da NiFi-n autentifikatu. Egiaztatu .env pasahitza.")

def get_root_id(token):
    res = api_call("/flow/process-groups/root", token=token)
    return res["processGroupFlow"]["breadcrumb"]["breadcrumb"]["id"]

def disable_services_in_group_recursive(token, gid):
    """Gelditu prozesadoreak eta desgaitu kontrolagailu-zerbitzuak talde barruan."""
    api_call(f"/flow/process-groups/{gid}", method="PUT", token=token,
             data={"id": gid, "state": "STOPPED"})
    cs_data = api_call(f"/flow/process-groups/{gid}/controller-services", token=token)
    for cs in cs_data.get("controllerServices", []):
        cid = cs["id"]
        ver = cs["revision"]["version"]
        if cs["component"].get("state") != "DISABLED":
            api_call(f"/controller-services/{cid}/run-status", method="PUT", token=token,
                     data={"revision": {"version": ver, "clientId": str(uuid.uuid4())}, "state": "DISABLED"})
    
    flow = api_call(f"/flow/process-groups/{gid}", token=token)
    for child in flow.get("processGroupFlow", {}).get("flow", {}).get("processGroups", []):
        disable_services_in_group_recursive(token, child["id"])

def clear_root_canvas(token, root_id):
    """Garbitu root-eko prozesu-taldeak eta etiketak berriz antolatzeko."""
    flow = api_call(f"/flow/process-groups/{root_id}", token=token)
    pgs = flow.get("processGroupFlow", {}).get("flow", {}).get("processGroups", [])
    labels = flow.get("processGroupFlow", {}).get("flow", {}).get("labels", [])
    
    for pg in pgs:
        disable_services_in_group_recursive(token, pg["id"])
    
    flow_fresh = api_call(f"/flow/process-groups/{root_id}", token=token)
    for pg in flow_fresh.get("processGroupFlow", {}).get("flow", {}).get("processGroups", []):
        gid = pg["id"]
        ver = pg["revision"]["version"]
        api_call(f"/process-groups/{gid}?version={ver}", method="DELETE", token=token)
    
    for lbl in labels:
        lid = lbl["id"]
        ver = lbl["revision"]["version"]
        api_call(f"/labels/{lid}?version={ver}", method="DELETE", token=token)

def create_process_group(token, parent_id, name, x, y, comments=""):
    payload = {
        "revision": {"version": 0, "clientId": str(uuid.uuid4())},
        "component": {
            "name": name,
            "position": {"x": float(x), "y": float(y)},
            "comments": comments
        }
    }
    res = api_call(f"/process-groups/{parent_id}/process-groups", method="POST", data=payload, token=token)
    return res["id"]

def enable_controller_services_in_group(token, pg_id):
    """Gaitu prozesu-taldearen barruko kontrolagailu-zerbitzu guztiak."""
    cs_data = api_call(f"/flow/process-groups/{pg_id}/controller-services", token=token)
    for cs in cs_data.get("controllerServices", []):
        c = cs["component"]
        cs_id = cs["id"]
        ver = cs["revision"]["version"]
        if c.get("state") == "DISABLED" and not c.get("validationErrors"):
            api_call(f"/controller-services/{cs_id}/run-status", method="PUT", token=token,
                     data={"revision": {"version": ver, "clientId": str(uuid.uuid4())}, "state": "ENABLED"})

def import_flow(token, parent_id, flow_rel_path, name, x, y, comments="", cs_ids=None):
    full_path = os.path.join(BASE_DIR, flow_rel_path)
    if not os.path.isfile(full_path):
        print(f"⚠️ Ez da fitxategia aurkitu: {full_path}")
        return None
    
    with open(full_path, "r", encoding="utf-8") as f:
        snapshot_str = f.read()
    
    if cs_ids:
        if cs_ids.get("mongo_id"):
            snapshot_str = snapshot_str.replace("6f352988-b5e5-3e19-882e-66fca64f6ea1", cs_ids["mongo_id"])
        if cs_ids.get("dbcp_id"):
            snapshot_str = snapshot_str.replace("74888e3f-4e6e-3a48-b543-c2162080cfa1", cs_ids["dbcp_id"])
        if cs_ids.get("writer_id"):
            snapshot_str = snapshot_str.replace("1e207816-ca56-38af-8d4f-4408c7fc579f", cs_ids["writer_id"])
        if cs_ids.get("reader_id"):
            snapshot_str = snapshot_str.replace("f0cb7f47-a0e5-3e6e-8c48-c28b0792890c", cs_ids["reader_id"])

    snapshot = json.loads(snapshot_str)
    
    if comments and "flowContents" in snapshot:
        snapshot["flowContents"]["comments"] = comments
    
    payload = {
        "revisionDTO": {"version": 0, "clientId": str(uuid.uuid4())},
        "flowSnapshot": snapshot,
        "positionDTO": {"x": float(x), "y": float(y)},
        "groupName": name,
        "disconnectedNodeAcknowledged": False
    }
    res = api_call(f"/process-groups/{parent_id}/process-groups/import", method="POST", data=payload, token=token)
    if res and "id" in res:
        new_id = res["id"]
        print(f"   ✅ Kargatua: {name} (ID: {new_id[:8]}...)")
        enable_controller_services_in_group(token, new_id)
        return new_id
    else:
        print(f"   ❌ Errorea kargatzean: {name}")
        return None

def create_label(token, parent_id, text, x, y, width, height, bg_color="#ffffff", font_size="12pt"):
    payload = {
        "revision": {"version": 0, "clientId": str(uuid.uuid4())},
        "component": {
            "label": text,
            "position": {"x": float(x), "y": float(y)},
            "width": float(width),
            "height": float(height),
            "style": {
                "background-color": bg_color,
                "font-size": font_size
            }
        }
    }
    return api_call(f"/process-groups/{parent_id}/labels", method="POST", data=payload, token=token)

def ensure_controller_services(token, root_id):
    """Ziurtatu MySQL DBCP eta MongoDB zerbitzuak Root mailan aktibatuta daudela."""
    cs_list = api_call(f"/flow/process-groups/{root_id}/controller-services", token=token)
    existing = {c["component"]["name"]: c for c in cs_list.get("controllerServices", [])}

    # 1. MongoDB Controller Service
    if "MongoDBControllerService" not in existing:
        payload = {
            "revision": {"version": 0, "clientId": str(uuid.uuid4())},
            "component": {
                "name": "MongoDBControllerService",
                "type": "org.apache.nifi.mongodb.MongoDBControllerService",
                "bundle": {"group": "org.apache.nifi", "artifact": "nifi-mongodb-services-nar", "version": "2.0.0"},
                "properties": {"mongo-uri": "mongodb://mongodb:27017"}
            }
        }
        res = api_call(f"/process-groups/{root_id}/controller-services", method="POST", data=payload, token=token)
        if res:
            api_call(f"/controller-services/{res['id']}/run-status", method="PUT", token=token,
                     data={"revision": {"version": res["revision"]["version"], "clientId": str(uuid.uuid4())}, "state": "ENABLED"})
            print("   ✅ MongoDBControllerService sortua eta aktibatua")
    else:
        print("   ℹ️ MongoDBControllerService lehendik sortua")

    # 2. DBCP MariaDB / MySQL
    if "DBCPConnectionPool_MariaDB" not in existing:
        payload = {
            "revision": {"version": 0, "clientId": str(uuid.uuid4())},
            "component": {
                "name": "DBCPConnectionPool_MariaDB",
                "type": "org.apache.nifi.dbcp.DBCPConnectionPool",
                "bundle": {"group": "org.apache.nifi", "artifact": "nifi-dbcp-service-nar", "version": "2.0.0"},
                "properties": {
                    "Database Connection URL": "jdbc:mysql://mysql:3306/retail_db",
                    "Database Driver Class Name": "com.mysql.cj.jdbc.Driver",
                    "database-driver-locations": "/opt/mysql-connector-j-8.0.31.jar",
                    "Database User": CREDS.get("MYSQL_USER", "iabd"),
                    "Password": CREDS.get("MYSQL_PASSWORD", "")
                }
            }
        }
        res = api_call(f"/process-groups/{root_id}/controller-services", method="POST", data=payload, token=token)
        if res:
            api_call(f"/controller-services/{res['id']}/run-status", method="PUT", token=token,
                     data={"revision": {"version": res["revision"]["version"], "clientId": str(uuid.uuid4())}, "state": "ENABLED"})
            print("   ✅ DBCPConnectionPool_MariaDB sortua eta aktibatua")
    else:
        print("   ℹ️ DBCPConnectionPool_MariaDB lehendik sortua")

    # 3. JsonRecordSetWriter NDJSON
    if "JsonRecordSetWriter_NDJSON" not in existing:
        payload = {
            "revision": {"version": 0, "clientId": str(uuid.uuid4())},
            "component": {
                "name": "JsonRecordSetWriter_NDJSON",
                "type": "org.apache.nifi.json.JsonRecordSetWriter",
                "bundle": {"group": "org.apache.nifi", "artifact": "nifi-record-serialization-services-nar", "version": "2.0.0"},
                "properties": {"output-grouping": "output-oneline"}
            }
        }
        res = api_call(f"/process-groups/{root_id}/controller-services", method="POST", data=payload, token=token)
    # 4. JsonTreeReader
    if "JsonTreeReader" not in existing:
        payload = {
            "revision": {"version": 0, "clientId": str(uuid.uuid4())},
            "component": {
                "name": "JsonTreeReader",
                "type": "org.apache.nifi.json.JsonTreeReader",
                "bundle": {"group": "org.apache.nifi", "artifact": "nifi-record-serialization-services-nar", "version": "2.0.0"},
                "properties": {"schema-access-strategy": "infer-schema"}
            }
        }
        res = api_call(f"/process-groups/{root_id}/controller-services", method="POST", data=payload, token=token)
        if res:
            api_call(f"/controller-services/{res['id']}/run-status", method="PUT", token=token,
                     data={"revision": {"version": res["revision"]["version"], "clientId": str(uuid.uuid4())}, "state": "ENABLED"})
            print("   ✅ JsonTreeReader sortua eta aktibatua")
    else:
        print("   ℹ️ JsonTreeReader lehendik sortua")

    # Fetch updated list to get IDs
    cs_list_updated = api_call(f"/flow/process-groups/{root_id}/controller-services", token=token)
    name_to_id = {c["component"]["name"]: c["id"] for c in cs_list_updated.get("controllerServices", [])}
    return {
        "mongo_id": name_to_id.get("MongoDBControllerService"),
        "dbcp_id": name_to_id.get("DBCPConnectionPool_MariaDB"),
        "writer_id": name_to_id.get("JsonRecordSetWriter_NDJSON"),
        "reader_id": name_to_id.get("JsonTreeReader")
    }

def main():
    print("=================================================================")
    print("🚀 Apache NiFi: Ariketa Guztiak Kargatu eta Canvas-a Antolatu")
    print("=================================================================")
    
    token = get_token()
    root_id = get_root_id(token)
    print(f"📌 Root Process Group ID: {root_id}")

    print("\n1. Kontrolagailu-zerbitzu orokorrak ziurtatzen...")
    cs_ids = ensure_controller_services(token, root_id)

    print("\n2. Canvas nagusia garbitzen...")
    clear_root_canvas(token, root_id)

    print("\n3. Master Header Label sortzen...")
    header_text = (
        "╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗\n"
        "║                                 🎓 BIG DATA & DATAFLOW - APACHE NIFI LABORATEGIAK (2025-2026)                                              ║\n"
        "║                                 📌 IABD: Ariketa eta Proiektu Guztiak (01etik 07ra) Garbi Antolatuta                                      ║\n"
        "╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝\n\n"
        "• Lab 01: Fitxategiak Mugitu & Gatazkak (GetFile, PutFile, UpdateAttribute, ignore/replace/fail)\n"
        "• Lab 02: CSV Datuak Iragazi (3 Aldaera: SplitText 1 vs SplitText 10 vs PartitionRecord optimizatua)\n"
        "• Lab 03: Atributuak & Datu-Linajea (Fitxategi-sistema lokala vs MongoDB NoSQL integrazioa)\n"
        "• Lab 04: HTTP Ingesta & MongoDB (ListenHTTP bidezko REST sarrera eta JSON dokumentu biltegiratzea)\n"
        "• Lab 05: CSV -> JSON ConvertRecord DF2.1 (Record-oriented prozesamendua: CSVReader & JsonRecordSetWriter)\n"
        "• Lab 06: MariaDB & MongoDB Lab DF2.2 (Klasikoa vs Record-Oriented arkitekturen errendimendu konparaketa)\n"
        "• Lab 07: AEMET Datu-Lakua Medallion DF2.3 (Bronze gordinak -> Silver garbitua -> Gold agregatua)"
    )
    create_label(token, root_id, header_text, x=100, y=40, width=1460, height=210, bg_color="#d6eaf8", font_size="13pt")

    print("\n4. Ariketak kargatzen...")

    # --- 01. Lab ---
    print("   -> 01. Fitxategiak Mugitu & Gatazkak...")
    import_flow(token, root_id, 
                "01_Fitxategiak_Mugitu_Gatazkak/flow_01_fitxategiak_mugitu.json",
                "📁 01. Fitxategiak Mugitu & Gatazkak",
                x=100, y=290,
                comments="Fitxategien transferentzia lokala eta gatazka kasuen (ignore/replace/fail) kudeaketa.",
                cs_ids=cs_ids)

    # --- 02. Lab (Container with 3 variants) ---
    print("   -> 02. CSV Datuak Iragazi (3 aldaera)...")
    pg02_id = create_process_group(token, root_id, 
                                   "⚡ 02. CSV Datuak Iragazi (3 Aldaera)", 
                                   x=620, y=290,
                                   comments="CSV lerroen iragazketa eta transformazioa: SplitText(1), SplitText(10) eta PartitionRecord.")
    
    lbl02_text = (
        "📊 CSV DATUAK IRAGAZTEKO ERRENDIMENDU KONPARAKETA (3 ALDAERA)\n\n"
        "• Aldaera 1: SplitText (lerro 1) -> FlowFile bat lerro bakoitzeko. I/O eta Provenance overhead handia.\n"
        "• Aldaera 2: SplitText (10 lerro) -> Lote txikiak, FlowFile kopurua %90 murrizten da.\n"
        "• Aldaera 3: Optimizatua (PartitionRecord) -> Erregistro-bidezko prozesamendua memoriako streamingean. RAM eta CPU eraginkorrena!"
    )
    create_label(token, pg02_id, lbl02_text, x=80, y=40, width=1380, height=100, bg_color="#fcf3cf", font_size="12pt")
    
    import_flow(token, pg02_id,
                "02_CSV_Datuak_Iragazi/flow_02_csv_datuak_iragazi_aldaera1.json",
                "Aldaera 1: SplitText (1 lerro)",
                x=80, y=170,
                comments="FlowFile bana sortzen du CSV lerro bakoitzeko.",
                cs_ids=cs_ids)
    import_flow(token, pg02_id,
                "02_CSV_Datuak_Iragazi/flow_02_csv_datuak_iragazi_aldaera2.json",
                "Aldaera 2: SplitText (10 lerro)",
                x=560, y=170,
                comments="10 lerroko loteak sortzen ditu FlowFile bakoitzean.",
                cs_ids=cs_ids)
    import_flow(token, pg02_id,
                "02_CSV_Datuak_Iragazi/flow_02_csv_datuak_iragazi_aldaera3_optimizazioa.json",
                "Aldaera 3: Optimizatua (PartitionRecord)",
                x=1040, y=170,
                comments="PartitionRecord erabiliz fitxategia zatitu gabe iragazten du.",
                cs_ids=cs_ids)

    # --- 03. Lab (Container with 2 variants) ---
    print("   -> 03. Atributuak & Linajea (2 aldaera)...")
    pg03_id = create_process_group(token, root_id,
                                   "🏷️ 03. Atributuak & Datu-Linajea",
                                   x=1140, y=290,
                                   comments="Datuen jatorria, atributuak erabili eta datu-linajea: Fitxategi-sistema eta MongoDB.")
    
    lbl03_text = (
        "🏷️ ATRIBUTUAK, PROVENANCE ETA DATU-LINAJEA\n\n"
        "• Aldaera 1: FlowFile atributuak erauzi eta edukia disko lokalean gorde.\n"
        "• Aldaera 2: Atributuak JSON bihurtu eta zuzenean MongoDB NoSQL bilduman txertatu."
    )
    create_label(token, pg03_id, lbl03_text, x=80, y=40, width=1000, height=90, bg_color="#d5f5e3", font_size="12pt")

    import_flow(token, pg03_id,
                "03_Atributuak_eta_Linajea/flow_03_atributuak_linajea.json",
                "Aldaera 1: Oinarrizkoa (Fitxategi-sistema)",
                x=80, y=160,
                comments="Atributuak atera eta fitxategi moduan gorde.",
                cs_ids=cs_ids)
    import_flow(token, pg03_id,
                "03_Atributuak_eta_Linajea/flow_03_atributuak_linajea_aldaera2_mongodb.json",
                "Aldaera 2: MongoDB NoSQL",
                x=580, y=160,
                comments="Atributuak JSON bihurtu eta PutMongo bidez kargatu.",
                cs_ids=cs_ids)

    # --- 04. Lab ---
    print("   -> 04. HTTP Ingesta & MongoDB...")
    import_flow(token, root_id,
                "04_HTTP_Ingesta_eta_MongoDB/flow_04_mongodb_http.json",
                "🌐 04. HTTP Ingesta & MongoDB NoSQL",
                x=100, y=540,
                comments="ListenHTTP entzulea erabiliz kanpoko REST HTTP eskaerak jaso eta MongoDB-n gorde.",
                cs_ids=cs_ids)

    # --- 05. Lab ---
    print("   -> 05. CSV -> JSON ConvertRecord (DF 2.1)...")
    import_flow(token, root_id,
                "05_CSV_JSON_ConvertRecord_DF2.1/flow_05_csv_json_df2.1.json",
                "🔄 05. CSV -> JSON ConvertRecord (DF 2.1)",
                x=620, y=540,
                comments="ConvertRecord kontrolagailu-zerbitzuak erabiliz formatu bihurketa azkarra eta arina.",
                cs_ids=cs_ids)

    # --- 06. Lab (Container with 2 variants) ---
    print("   -> 06. MariaDB & MongoDB Lab (DF 2.2)...")
    pg06_id = create_process_group(token, root_id,
                                   "🗄️ 06. MariaDB & MongoDB Lab (DF 2.2)",
                                   x=1140, y=540,
                                   comments="MariaDB (SQL) -> MongoDB (NoSQL) migrazioa: Klasikoa vs Record-Oriented.")
    
    lbl06_text = (
        "🗄️ DF 2.2: MARIADB (SQL) -> MONGODB (NOSQL) MIGRAZIOA\n\n"
        "• Klasikoa: SplitText + ExtractText -> 12.435 FlowFile sortzen dira ilaran. Baliabide asko kontsumitzen ditu.\n"
        "• Record-Oriented: PutMongoRecord zuzena -> FlowFile bakarra streamingean, %90 azkarrago eta Heap memoria askoz egonkorrago!"
    )
    create_label(token, pg06_id, lbl06_text, x=80, y=40, width=1040, height=90, bg_color="#fadbd8", font_size="12pt")

    import_flow(token, pg06_id,
                "06_MariaDB_MongoDB_Laborategia_DF2.2/flow_06_mariadb_mongodb_classic.json",
                "Kasu 6: Klasikoa (SplitText / ExtractText)",
                x=80, y=160,
                comments="Lerroz lerro zatituta eta banan-banan txertatuta.",
                cs_ids=cs_ids)
    import_flow(token, pg06_id,
                "06_MariaDB_MongoDB_Laborategia_DF2.2/flow_06_mariadb_mongodb_record.json",
                "Kasu 6: Record-Oriented (PutMongoRecord)",
                x=580, y=160,
                comments="DBCP + PutMongoRecord erabiliz streaming zuzena.",
                cs_ids=cs_ids)

    # --- 07. Lab (Medallion Data Lake) ---
    print("   -> 07. AEMET Datu-Lakua Medallion (DF 2.3)...")
    import_flow(token, root_id,
                "07_AEMET_Datu_Lakua_Medallion_DF2.3/flow_07_aemet_datalake_medallion.json",
                "🏅 07. AEMET Datu-Lakua Medallion (DF 2.3)",
                x=100, y=790,
                comments="AEMET Open Data API -> Medallion Arkitektura osoa (Bronze -> Silver -> Gold).",
                cs_ids=cs_ids)

    lbl07_text = (
        "🏅 MEDALLION DATA LAKE ARKITEKTURA (DF 2.3)\n\n"
        "• 🥉 Bronze Geruza: AEMET-etik jasotako JSON gordinak (Raw Data) fitxategi lokalean gorde jatorrizko egoeran.\n"
        "• 🥈 Silver Geruza: Datu garbituak, egituratuak eta normalizatuak MongoDB NoSQL bilduman indexatuta.\n"
        "• 🥇 Gold Geruza: Kontsulta analitikoetarako datu agregatu eta estatistikoak (QueryRecord / MergeContent)."
    )
    create_label(token, root_id, lbl07_text, x=620, y=790, width=940, height=175, bg_color="#f9ebea", font_size="12pt")

    print("\n=================================================================")
    print("🎉 GUZTIA ONGI KARGATU DA! NI-FI CANVAS-A PREST DAGO!")
    print(f"👉 Sartu hemen ikusteko: {NIFI_URL}/nifi/")
    print("=================================================================")

if __name__ == "__main__":
    main()
