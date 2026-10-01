#!/usr/bin/env python3
"""P6/P7: visualizaciones clasicas (aggregation based) + Dashboards por API.

Lens por API falla con 'Could not find datasource' (9.5.4 valida el state
de forma estricta); las clasicas dan el mismo grafico visible y son
reproducibles por API. Dashboard real en Kibana, verificable con captura.
Erabilera: KB=http://127.0.0.1:15601 ./sortu_dashboardak_classic.py [--delete]
"""
import argparse
import json
import os
import sys
import urllib.request

KB = os.environ.get("KB", "http://127.0.0.1:15601")
DV = {"produktuak": "997fb2ec-60b1-4fb9-80dd-ff19ce92fbb3",
      "salmentak": "16e909d6-b026-4c06-a453-a463286ee956"}


def api(method, path, data=None):
    req = urllib.request.Request(
        KB + path,
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Content-Type": "application/json", "kbn-xsrf": "true"},
        method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            raw = res.read().decode()
            return json.loads(raw) if raw else {}
    except Exception as e:
        body = ""
        try:
            body = e.read().decode()[:600]
        except Exception:
            pass
        raise RuntimeError("%s %s: %s | %s" % (method, path, e, body))


def metric(mid, op, field=None):
    m = {"id": mid, "enabled": True, "type": op, "schema": "metric",
         "params": {}}
    if field:
        m["params"]["field"] = field
    return m


def terms_bucket(bid, field, size=5):
    return {"id": bid, "enabled": True, "type": "terms", "schema": "segment",
            "params": {"field": field, "orderBy": "1", "order": "desc",
                       "size": size, "otherBucket": False,
                       "otherBucketLabel": "Other", "missingBucket": False,
                       "missingBucketLabel": "Missing"}}


def date_bucket(bid):
    return {"id": bid, "enabled": True, "type": "date_histogram",
            "schema": "segment",
            "params": {"field": "data", "timeRange": {"from": "now-1y",
                                                      "to": "now"},
                       "useNormalizedEsInterval": True, "interval": "auto",
                       "drop_partials": False, "min_doc_count": 1,
                       "extended_bounds": {}}}


HIST_PARAMS = {
    "type": "histogram", "grid": {"categoryLines": False},
    "categoryAxes": [{"id": "CategoryAxis-1", "type": "category",
                      "position": "bottom", "show": True}],
    "valueAxes": [{"id": "ValueAxis-1", "name": "LeftAxis-1", "type": "value",
                   "position": "left", "show": True,
                   "scale": {"type": "linear", "mode": "normal"},
                   "labels": {"show": True, "rotate": 0, "truncate": 100},
                   "title": {"text": "Count"}}],
    "seriesParams": [{"show": "true", "type": "histogram", "mode": "stacked",
                      "data": {"label": "Count", "id": "1"},
                      "valueAxis": "ValueAxis-1", "drawLinesBetweenPoints": True,
                      "showCircles": True}],
    "addTooltip": True, "addLegend": True, "legendPosition": "right",
    "times": [], "addTimeMarker": False, "thresholdLine": {
        "show": False, "value": 10, "width": 1, "style": "full",
        "color": "#E7664C"}}


def vis(vtype, title, dv, aggs, params=None):
    import copy
    p = copy.deepcopy(HIST_PARAMS)
    if params:
        p.update(params)
    attrs = {"title": title,
             "visState": {"title": title, "type": vtype, "params": p,
                          "aggs": aggs},
             "kibanaSavedObjectMeta": {
                 "searchSourceJSON": json.dumps(
                     {"index": DV[dv],
                      "query": {"query": "", "language": "kuery"},
                      "filter": []})}}
    refs = [{"name": "kibanaSavedObjectMeta.searchSourceJSON.index",
             "id": DV[dv], "type": "index-pattern"}]
    if vtype == "pie":
        attrs["visState"]["params"] = {
            "type": "pie", "addTooltip": True, "addLegend": True,
            "legendPosition": "right", "isDonut": True, "labels": {
                "show": False, "values": True, "last_level": True,
                "truncate": 100}}
    r = api("POST", "/api/saved_objects/visualization",
            {"attributes": attrs, "references": refs})
    print("vis:", title, "->", r.get("id"))
    return r["id"]


def dashboard(title, viz_ids):
    panels, refs = [], []
    for i, vid in enumerate(viz_ids):
        panels.append({"version": "9.5.4",
                       "gridData": {"x": (i % 2) * 24, "y": (i // 2) * 15,
                                    "w": 24, "h": 15},
                       "panelIndex": str(i),
                       "embeddableConfig": {},
                       "panelRefName": "panel_%d" % i})
        refs.append({"id": vid, "name": "panel_%d" % i,
                     "type": "visualization"})
    attrs = {"title": title,
             "panelsJSON": json.dumps(panels),
             "optionsJSON": json.dumps(
                 {"hidePanelTitles": False, "useMargins": True}),
             "version": 3, "timeRestore": False}
    r = api("POST", "/api/saved_objects/dashboard",
            {"attributes": attrs, "references": refs})
    print("dashboard:", title, "->", r.get("id"))
    return r.get("id")


def wipe():
    for t in ("lens", "visualization", "dashboard"):
        d = api("GET", "/api/saved_objects/_find?type=%s&per_page=100" % t)
        for o in d.get("saved_objects", []):
            api("DELETE", "/api/saved_objects/%s/%s" % (t, o["id"]))
            print("deleted", t, o.get("attributes", {}).get("title"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--delete", action="store_true")
    a = ap.parse_args()
    if a.delete:
        return wipe() or 0
    out = {}
    out["p6_v1"] = vis("histogram", "Produktuak kategoriaren arabera",
                       "produktuak",
                       [metric("1", "count"),
                        terms_bucket("2", "kategoria.keyword")])
    out["p6_v2"] = vis("histogram",
                       "Batez besteko prezioa kategoriaren arabera",
                       "produktuak",
                       [metric("1", "avg", "prezioa"),
                        terms_bucket("2", "kategoria.keyword")])
    out["p6_dash"] = dashboard("Produktuen Dashboard-a",
                               [out["p6_v1"], out["p6_v2"]])
    out["p7_a"] = vis("histogram", "Salmentak kategoriaren arabera",
                      "salmentak",
                      [metric("1", "sum", "unitateak"),
                       terms_bucket("2", "kategoria.keyword")])
    out["p7_b"] = vis("histogram", "Diru-sarrerak hirika", "salmentak",
                      [metric("1", "sum", "diru_sarrera"),
                       terms_bucket("2", "hiria.keyword", size=10)])
    out["p7_c"] = vis("pie", "Salmenta-kanalen banaketa", "salmentak",
                      [metric("1", "count"),
                       terms_bucket("2", "kanala.keyword")])
    out["p7_d"] = vis("histogram", "Diru-sarreren bilakaera denboran",
                      "salmentak",
                      [metric("1", "sum", "diru_sarrera"), date_bucket("2")])
    out["p7_e"] = vis("histogram", "Produktuen batez besteko prezioa",
                      "salmentak",
                      [metric("1", "avg", "prezioa"),
                       terms_bucket("2", "produktua.keyword", size=10)])
    out["p7_dash"] = dashboard(
        "Salmenten Dashboard-a",
        [out["p7_a"], out["p7_b"], out["p7_c"], out["p7_d"], out["p7_e"]])
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "dashboards_ids.json"), "w"), indent=1)
    print("ids -> dashboards/dashboards_ids.json")
    return 0


if __name__ == "__main__":
    sys.exit("Intento anterior conservado para referencia. Usa completar_kibana.py: la entrega requiere Lens y evita borrados globales.")
