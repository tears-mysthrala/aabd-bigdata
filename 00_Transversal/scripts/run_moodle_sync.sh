#!/usr/bin/env bash
set -euo pipefail

export PATH="/usr/local/bin:/usr/bin:/bin:/home/tears/.local/bin:$PATH"

# DBUS eta Wayland mahaigaineko jakinarazpenetarako (notify-send)
if [ -z "${DBUS_SESSION_BUS_ADDRESS:-}" ]; then
    export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"
fi

# Aldiberekotasun-zaintza: orduko zikloak ez dira gainjartzen.
# Blokeoa exec bidez heredatzen da (fd 9, CLOEXEC gabe), uv amaitu arte.
LOCK_FILE="/tmp/moodle-sync.lock"
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
    echo "moodle-sync ya en ejecución, se omite este ciclo"
    exit 0
fi

exec /usr/bin/uv run --with playwright --with requests --with beautifulsoup4 --with python-docx /home/tears/bigdata/00_Transversal/scripts/moodle_sync.py
