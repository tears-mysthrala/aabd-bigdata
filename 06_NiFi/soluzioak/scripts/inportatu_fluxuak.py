#!/usr/bin/env python3
"""
Apache NiFi 2.0 REST API - Fluxu Guztiak Inportatzeko Tresna Automatizatua.
Guztira 7 kasuak eta aldaerak NiFi-ra zuzenean inportatzen ditu prozesu-talde garbi gisa.
"""

import os
import sys
import glob
import json
import urllib.request
import urllib.error
import ssl

NIFI_URL = os.environ.get("NIFI_URL", "https://localhost:8443")
NIFI_USER = os.environ.get("NIFI_USER", "nifi")
# Sin contraseña por defecto: va en entorno/.env, nunca hardcodeada (SECURITY.md).
NIFI_PASS = os.environ.get("NIFI_PASS", "")
if not NIFI_PASS:
    print("Falta NIFI_PASS en entorno (cárgala desde .env).", file=sys.stderr)
    sys.exit(1)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SSL baliogabetzea tokiko garapenerako
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def api_request(endpoint, method="GET", data=None, token=None, content_type="application/json"):
    url = f"{NIFI_URL}/nifi-api{endpoint}"
    headers = {"Content-Type": content_type}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    body = None
    if data:
        if isinstance(data, (dict, list)):
            body = json.dumps(data).encode("utf-8")
        elif isinstance(data, bytes):
            body = data
        elif isinstance(data, str):
            body = data.encode("utf-8")
            
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            res_body = response.read().decode("utf-8")
            try:
                return json.loads(res_body)
            except Exception:
                return res_body
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"HTTP Errorea ({e.code}) {endpoint}: {err_msg[:300]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Konexio errorea {endpoint}: {e}", file=sys.stderr)
        return None

def get_token():
    print(f"1. NiFi-n saioa hasten ({NIFI_URL})...")
    payload = f"username={NIFI_USER}&password={NIFI_PASS}"
    res = api_request("/access/token", method="POST", data=payload, content_type="application/x-www-form-urlencoded")
    if res and isinstance(res, str) and res.startswith("ey"):
        print("   ✅ Autentifikazioa zuzena! JWT Bearer tokena eskuratu da.")
        return res
    print("   ❌ Ezin izan da autentifikatu. Egiaztatu erabiltzailea eta pasahitza.")
    return None

def get_root_id(token):
    res = api_request("/flow/process-groups/root", token=token)
    if res:
        root_id = res.get("processGroupFlow", {}).get("id")
        print(f"2. Root Process Group ID aurkitua: {root_id}")
        return root_id
    return None

def list_flows():
    pattern = os.path.join(BASE_DIR, "**", "flow_*.json")
    flows = sorted(glob.glob(pattern, recursive=True))
    return flows

def main():
    print("=== Apache NiFi: Fluxuak Kudeatu eta Inportatu ===")
    flows = list_flows()
    print(f"Diskoan aurkitutako fluxuak ({len(flows)}):")
    for i, f in enumerate(flows, 1):
        rel = os.path.relpath(f, BASE_DIR)
        print(f"  {i}. {rel}")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        return

    print("\n👉 NiFi Canvas-ean ariketak kargatzen eta antolatzen...")
    script_path = os.path.join(os.path.dirname(__file__), "kargatu_fluxu_guztiak.py")
    os.execv(sys.executable, [sys.executable, script_path])

if __name__ == "__main__":
    main()
