#!/usr/bin/env bash
set -euo pipefail
base_dir=$(cd -- "$(dirname -- "$0")" && pwd)
orange_python=${ORANGE_PYTHON:-/home/tears/.local/share/uv/tools/orange3/bin/python}
python3 "$base_dir/scripts/estadisticas.py"
flock /tmp/aabd-orange-entregas-20261005.lock env \
  AI4I_ORANGE_LOCK_HELD=1 XDG_RUNTIME_DIR="/run/user/$(id -u)" \
  WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}" QT_QPA_PLATFORM=wayland \
  "$orange_python" "$base_dir/scripts/capturar_orange.py"
flock /tmp/aabd-orange-entregas-20261005.lock env \
  AI4I_ORANGE_LOCK_HELD=1 XDG_RUNTIME_DIR="/run/user/$(id -u)" \
  WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}" QT_QPA_PLATFORM=wayland \
  "$orange_python" "$base_dir/scripts/verificar_flujo_orange.py"
uv run --with reportlab==5.0.1 python "$base_dir/scripts/generar_pdf.py"
python3 "$base_dir/scripts/verificar.py" --actualizar-hashes
