"""JSON -> YAML eta XML Bihurgailua eta Datu-Formatuen Alderaketa.

Moduloa: 5073 - Lengoaiak eta Datu Zientzia
Atala: 1.3 Datu-formatuak (JSON, YAML, XML)
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path
import yaml

JSON_DATUAK = """{
  "bezeroak": [
    {"id": "001", "izena": "Ane", "erosketa": 89.50},
    {"id": "002", "izena": "Mikel", "erosketa": 23.10},
    {"id": "003", "izena": "Leire", "erosketa": 145.00},
    {"id": "004", "izena": "Jon", "erosketa": 12.75},
    {"id": "005", "izena": "Maite", "erosketa": 67.90}
  ]
}"""


def json_to_yaml(json_str: str) -> str:
    """JSON katea YAML formatura bihurtzen du."""
    datuak = json.loads(json_str)
    return yaml.dump(datuak, sort_keys=False, allow_unicode=True)


def json_to_xml(json_str: str) -> str:
    """JSON katea XML formatura bihurtzen du."""
    datuak = json.loads(json_str)
    root = ET.Element("datuak")
    bezeroak_elem = ET.SubElement(root, "bezeroak")
    for b in datuak["bezeroak"]:
        b_elem = ET.SubElement(bezeroak_elem, "bezeroa", id=b["id"])
        izena = ET.SubElement(b_elem, "izena")
        izena.text = b["izena"]
        erosketa = ET.SubElement(b_elem, "erosketa")
        erosketa.text = str(b["erosketa"])
    return ET.tostring(root, encoding="utf-8").decode("utf-8")


def main() -> None:
    print("--- [1] JATORRIZKO JSON ---")
    print(JSON_DATUAK)

    yaml_out = json_to_yaml(JSON_DATUAK)
    print("\n--- [2] BIHURTUTAKO YAML ---")
    print(yaml_out)

    xml_out = json_to_xml(JSON_DATUAK)
    print("--- [3] XML FORMATUA ---")
    print(xml_out)

    print("\n--- [4] ANALISIA: ZERGATIK DU JSON-EK ABANTAILA API-ETAN? ---")
    print("1. Tamaina eta arintasuna: XML-k etiketa itxiak behar ditu (<izena>Ane</izena>), byte gehiago kontsumituz.")
    print("2. Parsing abiadura eta erraztasuna: JSON zuzenean mapatzen da Python dict/list edo JS Object-etara.")
    print("3. YAML vs JSON: YAML konfigurazio fitxategietarako (adib. Docker, K8s) bikaina da (irakurgarria), baina JSON estandar unibertsala da REST APIetan.")


if __name__ == "__main__":
    main()
