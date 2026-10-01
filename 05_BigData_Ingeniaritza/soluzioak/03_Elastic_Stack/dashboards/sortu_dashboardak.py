#!/usr/bin/env python3
"""P6/P7: Lens bistaratzeak + Dashboard-ak Saved Objects API bidez.

Erabilera: KB=http://127.0.0.1:15601 python3 sortu_dashboardak.py
GUI bidezko kliken baliokidea: objektu berak sortzen dira, Dashboard
aplikazioan ikusgai eta interaktiboak.
"""
import argparse
import json
import os
import sys
import urllib.request
import uuid
import hashlib
from urllib.parse import urlparse



KB = os.environ.get("KB", "http://127.0.0.1:15601")
DV = {}
if urlparse(KB).hostname not in ("localhost", "127.0.0.1", "::1"):
    raise SystemExit("Loopback laborategia behar da.")


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


def layer_id():
    return uuid.uuid4().hex[:8]


def terms_col(cid, field, label, size=5, order_col=None):
    col = {"customLabel": True, "dataType": "string", "isBucketed": True,
           "label": label, "operationType": "terms",
           "params": {"include": [], "exclude": [],
                      "orderDirection": "desc",
                      "otherBucket": False,
                      "parentFormat": {"id": "terms"}, "size": size,
                      "missingBucket": False},
           "scale": "ordinal", "sourceField": field}
    if order_col:
        col["params"]["orderBy"] = {"type": "column", "columnId": order_col}
    return col


def metric_col(cid, op, label, field=None):
    op = "average" if op == "avg" else op
    col = {"customLabel": True, "dataType": "number", "isBucketed": False,
           "label": label, "operationType": op, "scale": "ratio"}
    if op == "count":
        col["sourceField"] = "___records___"
    elif field:
        col["sourceField"] = field
    if op in ("average", "sum"):
        col["params"] = {"emptyAsNull": True}
        if field in ("prezioa", "diru_sarrera"):
            col["params"]["format"] = {"id": "number", "params": {"pattern": "0,0.00"}}
    return col


def date_col(cid, label="data"):
    return {"customLabel": True, "dataType": "date", "isBucketed": True,
            "label": label, "operationType": "date_histogram",
            "params": {"interval": "1M"}, "scale": "interval",
            "sourceField": "data"}


def lens_xy(title, dv, xcol, ycol, series="bar_stacked"):
    lid = layer_id()
    state = {
        "datasourceStates": {
            "formBased": {
                "layers": {
                    lid: {"columnOrder": ["cx", "cy"],
                          "columns": {"cx": xcol, "cy": ycol},
                          "sampling": 1}}}},
        "filters": [],
        "query": {"language": "kuery", "query": ""},
        "visualization": {
            "axisTitlesVisibilitySettings": {"x": True, "y": True},
            "fittingFunction": "None",
            "gridlinesVisibilitySettings": {"x": True, "y": True},
            "layers": [{"accessors": ["cy"], "layerId": lid,
                        "layerType": "data",
                        "palette": {"type": "palette", "name": "default"},
                        "position": "top", "seriesType": series,
                        "showGridlines": False, "xAccessor": "cx"}],
            "legend": {"isVisible": True, "position": "right",
                       "showSingleSeries": False},
            "preferredSeriesType": series,
            "tickLabelsVisibilitySettings": {"x": True, "y": True},
            "valueLabels": "hide"}}
    refs = [{"id": DV[dv], "name": "indexpattern-datasource-current-indexpattern",
             "type": "index-pattern"},
            {"id": DV[dv], "name": "indexpattern-datasource-layer-" + lid,
             "type": "index-pattern"}]
    if series == "pie":
        state["visualization"] = {"shape": "donut", "layers": [{"layerId": lid, "layerType": "data", "primaryGroups": ["cx"], "secondaryGroups": [], "metrics": ["cy"], "numberDisplay": "percent", "categoryDisplay": "default", "legendDisplay": "default"}]}
    oid = "aabd-" + hashlib.sha256(title.encode()).hexdigest()[:16]
    r = api("POST", "/api/saved_objects/lens/" + oid + "?overwrite=true",
            {"attributes": {"title": title, "visualizationType": "lnsPie" if series == "pie" else "lnsXY",
                            "state": state},
             "references": refs})
    print("lens:", title, "->", r.get("id"))
    return r["id"]


def dashboard(title, viz_ids):
    panels, refs = [], []
    for i, vid in enumerate(viz_ids):
        panels.append({"version": "9.5.4",
                       "gridData": {"x": (i % 2) * 24, "y": (i // 2) * 15,
                                    "w": 48 if len(viz_ids) == 5 and i == 4 else 24,
                                    "h": 20 if len(viz_ids) == 5 and i == 4 else 15},
                       "panelIndex": str(i),
                       "embeddableConfig": {"enhancements": {}},
                       "panelRefName": "panel_%d" % i})
        refs.append({"id": vid, "name": "panel_%d" % i, "type": "lens"})
    attrs = {"title": title,
             "description": "AABD — Elastic Stack praktikak",
             "panelsJSON": json.dumps(panels),
             "optionsJSON": json.dumps(
                 {"hidePanelTitles": False, "useMargins": True}),
             "version": 3,
             "timeRestore": True,
             "timeFrom": "2026-01-01T00:00:00.000Z",
             "timeTo": "2026-07-01T00:00:00.000Z"}
    oid = "aabd-" + hashlib.sha256(title.encode()).hexdigest()[:16]
    r = api("POST", "/api/saved_objects/dashboard/" + oid + "?overwrite=true",
            {"attributes": attrs, "references": refs})
    print("dashboard:", title, "->", r.get("id"))
    return r.get("id")




def main():
    ap = argparse.ArgumentParser()
    ap.parse_args()
    DV.update({v["title"]:v["id"] for v in api("GET", "/api/data_views")["data_view"]})
    out = {}
    out["p6_v1"] = lens_xy("Produktuak kategoriaren arabera", "produktuak",
                           terms_col("cx", "kategoria.keyword",
                                     "Kategoria", order_col="cy"),
                           metric_col("cy", "count", "Produktu kopurua"))
    out["p6_v2"] = lens_xy("Batez besteko prezioa kategoriaren arabera",
                           "produktuak",
                           terms_col("cx", "kategoria.keyword",
                                     "Kategoria", order_col="cy"),
                           metric_col("cy", "avg",
                                      "Batez besteko prezioa (€)", "prezioa"))
    out["p6_dash"] = dashboard("Produktuen Dashboard-a",
                               [out["p6_v1"], out["p6_v2"]])
    out["p7_a"] = lens_xy("Salmentak kategoriaren arabera", "salmentak",
                          terms_col("cx", "kategoria.keyword",
                                    "Kategoria", order_col="cy"),
                          metric_col("cy", "sum",
                                     "Saldutako unitateak", "unitateak"))
    out["p7_b"] = lens_xy("Diru-sarrerak hirika", "salmentak",
                          terms_col("cx", "hiria.keyword",
                                    "Hiria", order_col="cy"),
                          metric_col("cy", "sum",
                                     "Diru-sarrerak (€)", "diru_sarrera"))
    out["p7_c"] = lens_xy("Salmenta-kanalen banaketa", "salmentak",
                          terms_col("cx", "kanala.keyword",
                                    "Kanala", order_col="cy"),
                          metric_col("cy", "count", "Eragiketa kopurua"),
                          series="pie")
    out["p7_d"] = lens_xy("Diru-sarreren bilakaera denboran", "salmentak",
                          date_col("cx"),
                          metric_col("cy", "sum",
                                     "Diru-sarrerak (€)", "diru_sarrera"),
                          series="line")
    out["p7_e"] = lens_xy("Produktuen batez besteko prezioa", "salmentak",
                          terms_col("cx", "produktua.keyword",
                                    "Produktua",
                                    size=12, order_col="cy"),
                          metric_col("cy", "avg",
                                     "Batez besteko prezioa (€)", "prezioa"),
                          series="bar_horizontal")
    out["p7_dash"] = dashboard(
        "Salmenten Dashboard-a",
        [out["p7_a"], out["p7_b"], out["p7_c"], out["p7_d"], out["p7_e"]])
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "dashboards_ids.json"), "w"), indent=1)
    print("ids -> dashboards/dashboards_ids.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
