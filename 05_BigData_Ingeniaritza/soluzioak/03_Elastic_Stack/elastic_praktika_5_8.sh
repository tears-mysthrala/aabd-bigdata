#!/usr/bin/env bash
# P5–P8: datos verificados, Discover, Lens, dashboards e ILM + template.
# No borra índices. Valores por defecto: compose.yaml, 9200/5601.
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export ES="${ES:-http://127.0.0.1:9200}"
export KB="${KB:-http://127.0.0.1:5601}"
exec python3 "$HERE/dashboards/completar_kibana.py"
