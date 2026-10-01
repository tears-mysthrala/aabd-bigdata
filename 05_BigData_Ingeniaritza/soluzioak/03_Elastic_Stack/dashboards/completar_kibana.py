#!/usr/bin/env python3
"""Completa P5–P8 en un laboratorio local, sin borrar índices ni objetos.
ES=http://127.0.0.1:19200 KB=http://127.0.0.1:15601 python3 completar_kibana.py
Solo biblioteca estándar. Conserva datos existentes y comprueba el CSV completo.
"""
import csv
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
import sortu_dashboardak as dashboards

HERE = Path(__file__).resolve().parent
ES = os.environ.get("ES", "http://127.0.0.1:19200").rstrip("/")
KB = dashboards.KB.rstrip("/")
for url in (ES, KB):
    if urllib.parse.urlparse(url).hostname not in ("127.0.0.1", "localhost", "::1"):
        raise SystemExit("Este script solo modifica un laboratorio en loopback.")


def api(base, method, path, data=None, raw=False):
    payload = data if isinstance(data, bytes) else json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(base + path, data=payload, method=method,
        headers={"Content-Type": "application/x-ndjson" if isinstance(data, bytes) else "application/json", "kbn-xsrf": "true"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read() if raw else json.load(r)


def ensure_index(name, docs, mapping):
    try:
        existing = api(ES, "GET", "/" + name + "/_search?size=1000")["hits"]["hits"]
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
        api(ES, "PUT", "/" + name, {"mappings": {"properties": mapping}})
        existing = []
    if not existing:
        bulk = []
        for i, doc in enumerate(docs):
            bulk.extend([json.dumps({"index": {"_index": name, "_id": str(doc.get("id", i + 1))}}), json.dumps(doc)])
        result = api(ES, "POST", "/_bulk?refresh=true", ("\n".join(bulk) + "\n").encode())
        if result["errors"]:
            raise RuntimeError(result)
        existing = api(ES, "GET", "/" + name + "/_search?size=1000")["hits"]["hits"]
    # Comparación completa, independiente del orden y de los ids internos de ES.
    normal = lambda rows: sorted(json.dumps(r, sort_keys=True) for r in rows)
    if normal([h["_source"] for h in existing]) != normal(docs):
        raise RuntimeError(name + ": los datos existentes difieren del enunciado; no se sobrescriben")
    assert api(ES, "GET", "/" + name + "/_count")["count"] == len(docs)
    print(name, len(docs), "documentos verificados")


def main():
    products = [
        {"izena": "Koaderno urdina", "kategoria": "Papergintza", "prezioa": 4.5, "stock": 25},
        {"izena": "Koaderno handia", "kategoria": "Papergintza", "prezioa": 8.5, "stock": 10},
        {"izena": "Sagu optikoa", "kategoria": "Informatika", "prezioa": 19.99, "stock": 15},
        {"izena": "Teklatu mekanikoa", "kategoria": "Informatika", "prezioa": 59.99, "stock": 5}]
    text = {"type": "text", "fields": {"keyword": {"type": "keyword"}}}
    ensure_index("produktuak", products, {"izena": text, "kategoria": text, "prezioa": {"type": "float"}, "stock": {"type": "long"}})
    with (HERE.parents[2] / "materialak/salmentak_kibana.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in ("id", "unitateak"):
            r[k] = int(r[k])
        for k in ("prezioa", "deskontua_pct", "diru_sarrera"):
            r[k] = float(r[k])
    ensure_index("salmentak", rows, {"data": {"type": "date"}, "id": {"type": "long"}, "unitateak": {"type": "long"}, **{k: {"type": "double"} for k in ("prezioa", "deskontua_pct", "diru_sarrera")}, **{k: text for k in ("hiria", "kanala", "kategoria", "produktua")}})
    assert api(ES, "GET", "/salmentak/_mapping")["salmentak"]["mappings"]["properties"]["data"]["type"] == "date"
    views = {v["title"]: v["id"] for v in api(KB, "GET", "/api/data_views")["data_view"]}
    for name in ("produktuak", "salmentak"):
        if name not in views:
            view = {"id": "aabd-" + name, "title": name, "name": name}
            if name == "salmentak":
                view["timeFieldName"] = "data"
            views[name] = api(KB, "POST", "/api/data_views/data_view", {"data_view": view})["data_view"]["id"]
        view = api(KB, "GET", "/api/data_views/data_view/" + views[name])["data_view"]
        if (view.get("timeFieldName") or None) != ("data" if name == "salmentak" else None):
            raise RuntimeError("Data View con campo temporal incorrecto: " + name)
    queries = ["", 'kategoria: "Informatika"', "prezioa > 100", 'kategoria: "Informatika" AND prezioa < 500', 'NOT kategoria: "Papergintza"']
    searches = []
    for i, query in enumerate(queries):
        oid = "aabd-p5-" + str(i)
        api(KB, "POST", "/api/saved_objects/search/" + oid + "?overwrite=true", {
            "attributes": {"title": "P5 · Produktuak · " + (query or "dokumentu guztiak"), "columns": ["izena", "kategoria", "prezioa"], "sort": [], "kibanaSavedObjectMeta": {"searchSourceJSON": json.dumps({"indexRefName": "kibanaSavedObjectMeta.searchSourceJSON.index", "query": {"language": "kuery", "query": query}, "filter": []})}},
            "references": [{"name": "kibanaSavedObjectMeta.searchSourceJSON.index", "id": views["produktuak"], "type": "index-pattern"}]})
        searches.append({"id": oid, "query": query})
    policy = {"policy": {"phases": {
        "hot": {"min_age": "0ms", "actions": {"set_priority": {"priority": 100}}},
        "warm": {"min_age": "7d", "actions": {"set_priority": {"priority": 50}}},
        "cold": {"min_age": "30d", "actions": {"set_priority": {"priority": 0}}},
        "delete": {"min_age": "90d", "actions": {"delete": {}}}}}}
    template = {"index_patterns": ["web-logs-*"], "priority": 200, "template": {"settings": {"index.lifecycle.name": "web-logs-policy"}}}
    api(ES, "PUT", "/_ilm/policy/web-logs-policy", policy)
    api(ES, "PUT", "/_index_template/web-logs-template", template)
    simulated = api(ES, "POST", "/_index_template/_simulate_index/web-logs-2026.10.02")
    assert simulated["template"]["settings"]["index"]["lifecycle"]["name"] == "web-logs-policy"
    assert "data_stream" not in api(ES, "GET", "/_index_template/web-logs-template")["index_templates"][0]["index_template"]
    phases = api(ES, "GET", "/_ilm/policy/web-logs-policy")["web-logs-policy"]["policy"]["phases"]
    assert {k: v["min_age"] for k, v in phases.items()} == {"hot": "0ms", "warm": "7d", "cold": "30d", "delete": "90d"}
    (HERE / "ilm_policy.json").write_text(json.dumps(policy, indent=2) + "\n")
    (HERE / "ilm_template.json").write_text(json.dumps(template, indent=2) + "\n")
    (HERE / "p5_searches.json").write_text(json.dumps(searches, indent=2, ensure_ascii=False) + "\n")
    # El generador también descubre las Data Views y usa ids deterministas.
    dashboards.main()
    ids = json.loads((HERE / "dashboards_ids.json").read_text())
    objects = [{"type": "dashboard", "id": ids[k]} for k in ("p6_dash", "p7_dash")] + [{"type": "search", "id": s["id"]} for s in searches]
    exported = api(KB, "POST", "/api/saved_objects/_export", {"objects": objects, "includeReferencesDeep": True, "excludeExportDetails": True}, raw=True)
    (HERE / "kibana_praktikak.ndjson").write_bytes(exported)
    ermua = [r for r in rows if r["hiria"] == "Ermua"]
    report = {"csv_rows": len(rows), "monthly_revenue": {m: round(sum(r["diru_sarrera"] for r in rows if r["data"].startswith(m)), 2) for m in sorted({r["data"][:7] for r in rows})}, "Ermua": {"operations": len(ermua), "units": sum(r["unitateak"] for r in ermua), "revenue": round(sum(r["diru_sarrera"] for r in ermua), 2), "channels": {c: sum(r["kanala"] == c for r in ermua) for c in ("Web", "Denda")}, "categories": {c: sum(r["unitateak"] for r in ermua if r["kategoria"] == c) for c in sorted({r["kategoria"] for r in ermua})}}}
    (HERE / "emaitzak.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print("P5–P8: objetos, dataset completo e ILM/template verificados; exportación", len(exported), "bytes")


if __name__ == "__main__":
    main()
