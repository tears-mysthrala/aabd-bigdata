#!/usr/bin/env python3
"""2. kasua - NiFi consumer (ConsumeKafka -> PutFile), talde desberdinarekin."""

import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

NIFI_URL = os.environ.get("NIFI_URL", "https://localhost:8443")
if urllib.parse.urlparse(NIFI_URL).scheme != "https":
    raise SystemExit("NIFI_URL HTTPS izan behar da (kredentzialak argi ez bidaltzeko)")


def make_ctx():
    insecure = os.environ.get("NIFI_INSECURE", "")
    if insecure == "1":
        print(
            "OHARRA: NIFI_INSECURE=1 — ziurtagiria ez da egiaztatzen (lab soilik)",
            file=sys.stderr,
        )
        c = ssl.create_default_context()
        c.check_hostname = False
        c.verify_mode = ssl.CERT_NONE
        return c
    cafile = os.environ.get("NIFI_CA_CERT") or None
    return ssl.create_default_context(cafile=cafile)


ctx = make_ctx()

HERE = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.normpath(
    os.path.join(
        HERE,
        "..",
        "..",
        "..",
        "06_NiFi",
        "soluzioak",
        "06_MariaDB_MongoDB_Laborategia_DF2.2",
        ".env",
    )
)


def load_env(path):
    creds = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                creds[k.strip()] = v.strip().strip('"').strip("'")
    return creds


def api(endpoint, method="GET", data=None, tok=None):
    url = NIFI_URL + "/nifi-api" + endpoint
    headers = {"Content-Type": "application/json"}
    if tok:
        headers["Authorization"] = "Bearer " + tok
    body = json.dumps(data).encode() if isinstance(data, (dict, list)) else data
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as res:
            raw = res.read().decode()
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:500]
        raise RuntimeError("NiFi %s %s: %s" % (method, endpoint, detail))
    try:
        return json.loads(raw)
    except ValueError:
        return raw


def get_token(creds):
    payload = urllib.parse.urlencode(
        {"username": creds["NIFI_USER"], "password": creds["NIFI_PASSWORD"]}
    )
    req = urllib.request.Request(
        NIFI_URL + "/nifi-api/access/token",
        data=payload.encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, context=ctx, timeout=30) as res:
        return res.read().decode()


def find_processor(tok, kind):
    d = api("/flow/processor-types", tok=tok)
    pts = d.get("processorTypes", d if isinstance(d, list) else [])
    for p in pts:
        if p.get("type", "").endswith(kind):
            b = p.get("bundle", {})
            return (
                p["type"],
                b.get("group", ""),
                b.get("artifact", ""),
                b.get("version", ""),
            )
    raise RuntimeError("processor mota ez da aurkitu: " + kind)


def mk_processor(tok, pg, ptype, bundle, name, props, x, y, autoterm=()):
    payload = {
        "revision": {"version": 0},
        "component": {
            "type": ptype,
            "bundle": {"group": bundle[0], "artifact": bundle[1], "version": bundle[2]},
            "name": name,
            "position": {"x": x, "y": y},
            "config": {
                "properties": props,
                "autoTerminatedRelationships": list(autoterm),
            },
        },
    }
    r = api("/process-groups/%s/processors" % pg, "POST", payload, tok)
    return r["id"]


def connect(tok, pg, src, dst, rel):
    payload = {
        "revision": {"version": 0},
        "component": {
            "source": {"id": src, "groupId": pg, "type": "PROCESSOR"},
            "destination": {"id": dst, "groupId": pg, "type": "PROCESSOR"},
            "selectedRelationships": [rel],
        },
    }
    api("/process-groups/%s/connections" % pg, "POST", payload, tok)


def set_state(tok, pid, state):
    cur = api("/processors/%s" % pid, tok=tok)
    payload = {"revision": {"version": cur["revision"]["version"]}, "state": state}
    api("/processors/%s/run-status" % pid, "PUT", payload, tok)


def find_cs(tok, kind):
    d = api("/flow/controller-service-types", tok=tok)
    for p in d.get("controllerServiceTypes", []):
        if p.get("type", "").endswith(kind):
            b = p.get("bundle", {})
            return (
                p["type"],
                b.get("group", ""),
                b.get("artifact", ""),
                b.get("version", ""),
            )
    raise RuntimeError("controller service ez da aurkitu: " + kind)


def mk_cs(tok, pg, cst, bundle, name, props):
    payload = {
        "revision": {"version": 0},
        "component": {
            "type": cst,
            "bundle": {"group": bundle[0], "artifact": bundle[1], "version": bundle[2]},
            "name": name,
            "properties": props,
        },
    }
    r = api("/process-groups/%s/controller-services" % pg, "POST", payload, tok)
    return r["id"]


def enable_cs(tok, csid):
    cur = api("/controller-services/%s" % csid, tok=tok)
    payload = {"revision": {"version": cur["revision"]["version"]}, "state": "ENABLED"}
    api("/controller-services/%s/run-status" % csid, "PUT", payload, tok)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brokers", required=True)
    ap.add_argument("--topic", default="codex-personas")
    ap.add_argument("--group", default="codex-personas-nifi")
    ap.add_argument("--pg-name", default="2KASUA-Kafka-Personas")
    ap.add_argument("--outdir", default="/tmp/nifi-personas")
    ap.add_argument("--cleanup", action="store_true")
    a = ap.parse_args()

    creds = load_env(ENV_FILE)
    tok = get_token(creds)
    root = api("/flow/process-groups/root", tok=tok)["processGroupFlow"]["id"]

    if a.cleanup:
        kids = api("/process-groups/%s/process-groups" % root, tok=tok)
        n = 0
        for pg in kids.get("processGroups", []):
            if pg.get("component", {}).get("name", "") != a.pg_name:
                continue  # izen zehatza: "-backup" moduko PGak ez ukitu
            pid = pg["id"]
            for p in api("/process-groups/%s/processors" % pid, tok=tok).get(
                "processors", []
            ):
                dd = api("/processors/%s" % p["id"], tok=tok)
                if dd["component"].get("state") == "RUNNING":
                    set_state(tok, p["id"], "STOPPED")
            import time as _t

            for _ in range(12):
                states = []
                for p in api("/process-groups/%s/processors" % pid, tok=tok).get(
                    "processors", []
                ):
                    dd = api("/processors/%s" % p["id"], tok=tok)
                    states.append(dd["component"].get("state"))
                if all(s in ("STOPPED", "DISABLED") for s in states):
                    break
                _t.sleep(5)
            for c in api("/process-groups/%s/connections" % pid, tok=tok).get(
                "connections", []
            ):
                drop = api(
                    "/flowfile-queues/%s/drop-requests" % c["id"],
                    "POST",
                    {"revision": {"version": 0}},
                    tok,
                )
                for _ in range(12):
                    st = api(
                        "/flowfile-queues/%s/drop-requests/%s"
                        % (c["id"], drop["dropRequest"]["id"]),
                        tok=tok,
                    )["dropRequest"]
                    if st.get("finished", False):
                        break
                    _t.sleep(5)
                ver = api("/connections/%s" % c["id"], tok=tok)["revision"]["version"]
                api("/connections/%s?version=%d" % (c["id"], ver), "DELETE", tok=tok)
                for p in api("/process-groups/%s/processors" % pid, tok=tok).get(
                    "processors", []
                ):
                    ver = api("/processors/%s" % p["id"], tok=tok)["revision"][
                        "version"
                    ]
                    api("/processors/%s?version=%d" % (p["id"], ver), "DELETE", tok=tok)
                for cs in api(
                    "/flow/process-groups/%s/controller-services" % pid, tok=tok
                ).get("controllerServices", []):
                    if cs.get("parentGroupId") != pid:
                        continue  # root-eko partekatuak (MariaDB/Mongo) ez ukitu
                    dd = api("/controller-services/%s" % cs["id"], tok=tok)
                    if dd["component"].get("state") == "ENABLED":
                        cur = dd
                        api(
                            "/controller-services/%s/run-status" % cs["id"],
                            "PUT",
                            {
                                "revision": {"version": cur["revision"]["version"]},
                                "state": "DISABLED",
                            },
                            tok,
                        )
                ver = api("/process-groups/%s" % pid, tok=tok)["revision"]["version"]
                api("/process-groups/%s?version=%d" % (pid, ver), "DELETE", tok=tok)
                n += 1
        print("ezabatuta: %d" % n)
        return 0

    pg = api(
        "/process-groups/%s/process-groups" % root,
        "POST",
        {
            "revision": {"version": 0},
            "component": {"name": a.pg_name, "position": {"x": 1200.0, "y": 200.0}},
        },
        tok,
    )["id"]
    kt = find_processor(tok, "kafka.processors.ConsumeKafka")
    ua = find_processor(tok, "UpdateAttribute")
    pf = find_processor(tok, "PutFile")
    kcs = find_cs(tok, "Kafka3ConnectionService")
    jtr = find_cs(tok, "JsonTreeReader")
    jrw = find_cs(tok, "JsonRecordSetWriter")
    cs = mk_cs(
        tok,
        pg,
        kcs[0],
        kcs[1:],
        "k-conn",
        {"bootstrap.servers": a.brokers, "security.protocol": "PLAINTEXT"},
    )
    rr = mk_cs(tok, pg, jtr[0], jtr[1:], "k-reader", {})
    rw = mk_cs(tok, pg, jrw[0], jrw[1:], "k-writer", {})
    for csid in (cs, rr, rw):
        enable_cs(tok, csid)
    k = mk_processor(
        tok,
        pg,
        kt[0],
        kt[1:],
        "k-consume",
        {
            "Kafka Connection Service": cs,
            "Topics": a.topic,
            "Group ID": a.group,
            "auto.offset.reset": "earliest",
            "Record Reader": rr,
            "Record Writer": rw,
            "Output Strategy": "USE_VALUE",
            "Key Format": "string",
        },
        400.0,
        200.0,
        ["parse failure"],
    )
    u = mk_processor(
        tok, pg, ua[0], ua[1:], "k-filename", {"filename": "${kafka.key}"}, 700.0, 200.0
    )
    f = mk_processor(
        tok,
        pg,
        pf[0],
        pf[1:],
        "k-putfile",
        {"Directory": a.outdir, "Conflict Resolution Strategy": "replace"},
        1000.0,
        200.0,
        ["success", "failure"],
    )
    connect(tok, pg, k, u, "success")
    connect(tok, pg, u, f, "success")
    for pid in (k, u, f):
        set_state(tok, pid, "RUNNING")
    print("PG=%s run" % pg)
    for _ in range(12):
        time.sleep(10)
    print("prest (10 mezu badaude, /tmp/nifi-personas aztertu)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
