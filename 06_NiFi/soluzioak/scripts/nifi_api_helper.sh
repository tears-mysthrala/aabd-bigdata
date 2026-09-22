#!/usr/bin/env bash
# Apache NiFi REST API Helper Script
# Based on Section 06 of 01_02_ApacheNifi_aurreratua.pdf

set -e

NIFI_URL="${NIFI_URL:-https://localhost:8443}"
USER="${NIFI_USER:-nifi}"
# Sin contraseña por defecto: NIFI_PASS en entorno/.env (SECURITY.md).
if [ -z "${NIFI_PASS:-}" ]; then
    echo "Falta NIFI_PASS en entorno (cárgala desde .env)." >&2
    exit 1
fi
PASS="$NIFI_PASS"

usage() {
    echo "Usage: $0 {token | list-pg | start <UUID> | stop <UUID> | status <UUID>}"
    echo ""
    echo "Commands:"
    echo "  token             Obtain and display the JWT bearer token"
    echo "  list-pg           List all Process Groups with Name, ID, and State"
    echo "  start <UUID>      Start a Process Group (state -> RUNNING)"
    echo "  stop <UUID>       Stop a Process Group (state -> STOPPED)"
    echo "  status <UUID>     Show detailed status of a Process Group"
    exit 1
}

get_token() {
    curl -sk -X POST "$NIFI_URL/nifi-api/access/token" \
        -d "username=$USER&password=$PASS"
}

CMD="$1"
case "$CMD" in
    token)
        TOKEN=$(get_token)
        echo "$TOKEN"
        ;;
    list-pg)
        TOKEN=$(get_token)
        echo "Retrieving process groups..."
        curl -sk -H "Authorization: Bearer $TOKEN" "$NIFI_URL/nifi-api/flow/process-groups/root" | \
            python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    flow = data.get('processGroupFlow', {})
    flow_content = flow.get('flow', {})
    pgs = flow_content.get('processGroups', [])
    root_id = flow.get('id', 'N/A')
    print(f'Root Process Group ID: {root_id}\n')
    print(f'Found {len(pgs)} child Process Group(s):')
    for pg in pgs:
        comp = pg.get('component', {})
        status = pg.get('status', {})
        print(f\"  - Name:   {comp.get('name')}\")
        print(f\"    UUID:   {comp.get('id')}\")
        print(f\"    State:  {comp.get('runningCount', 0)} running / {comp.get('stoppedCount', 0)} stopped / {comp.get('invalidCount', 0)} invalid\")
        print(f\"    Queued: {status.get('aggregateSnapshot', {}).get('queued', '0')}\")
        print()
except Exception as e:
    print('Error parsing response:', e)
"
        ;;
    start)
        PG_UUID="$2"
        [ -z "$PG_UUID" ] && usage
        TOKEN=$(get_token)
        echo "Starting process group $PG_UUID..."
        curl --tlsv1.2 -sk \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" \
            -X PUT \
            -d "{\"id\":\"$PG_UUID\",\"state\":\"RUNNING\"}" \
            "$NIFI_URL/nifi-api/flow/process-groups/$PG_UUID" | \
            python3 -m json.tool || true
        echo ""
        ;;
    stop)
        PG_UUID="$2"
        [ -z "$PG_UUID" ] && usage
        TOKEN=$(get_token)
        echo "Stopping process group $PG_UUID..."
        curl --tlsv1.2 -sk \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" \
            -X PUT \
            -d "{\"id\":\"$PG_UUID\",\"state\":\"STOPPED\"}" \
            "$NIFI_URL/nifi-api/flow/process-groups/$PG_UUID" | \
            python3 -m json.tool || true
        echo ""
        ;;
    status)
        PG_UUID="$2"
        [ -z "$PG_UUID" ] && usage
        TOKEN=$(get_token)
        curl -sk \
            -H "Authorization: Bearer $TOKEN" \
            "$NIFI_URL/nifi-api/flow/process-groups/$PG_UUID/status" | \
            python3 -m json.tool || true
        ;;
    *)
        usage
        ;;
esac
