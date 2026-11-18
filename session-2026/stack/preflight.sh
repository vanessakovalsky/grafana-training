#!/usr/bin/env bash
# Controle de la stack Telcea sur une VM (ou en local). Sortie OK / KO, code retour 0 si tout est OK.
# Usage : ./preflight.sh
set -u
cd "$(dirname "$0")"
KO=0
ok() { echo "OK    $*"; }
ko() { echo "KO    $*"; KO=1; }

SERVICES="grafana prometheus alertmanager simulateur node-exporter cadvisor influxdb telegraf loki alloy mailpit"
RUNNING="$(docker compose ps --status running --services 2>/dev/null)"
for S in $SERVICES; do
  echo "$RUNNING" | grep -qx "$S" && ok "Service $S running" || ko "Service $S not running"
done

curl -fsS http://localhost:${GRAFANA_PORT:-3000}/grafana/api/health 2>/dev/null | grep -q '"database": *"ok"' \
  && ok "Grafana health" || ko "Grafana health"

UP="$(curl -fsS 'http://localhost:9090/api/v1/query?query=sum(telcea_site_up)' 2>/dev/null \
  | sed -n 's/.*"value":\[[^,]*,"\([0-9.]*\)".*/\1/p')"
[ "${UP:-0}" = "12" ] && ok "Telcea: 12 sites up" || ko "Telcea: sites up = ${UP:-none} (expected 12, storm running?)"

DOWN="$(curl -fsS 'http://localhost:9090/api/v1/query?query=count(up==0)' 2>/dev/null | grep -c '"value"')"
[ "$DOWN" = "0" ] && ok "Prometheus: all targets up" || ko "Prometheus: some targets down (Status > Targets)"

curl -fsS 'http://localhost:3100/loki/api/v1/label/service/values' 2>/dev/null | grep -q simulateur \
  && ok "Loki: simulator logs received" || ko "Loki: no simulator logs yet (wait 1 min)"

TOKEN="$(grep '^INFLUX_TOKEN=' .env 2>/dev/null | cut -d= -f2)"
curl -fsS -H "Authorization: Bearer ${TOKEN}" \
  'http://localhost:8181/api/v3/query_sql?db=systeme&q=SELECT%20count(*)%20FROM%20cpu' >/dev/null 2>&1 \
  && ok "InfluxDB: database systeme queried" || ko "InfluxDB: database systeme not queryable"

curl -fsS http://localhost:8025/mail/api/v1/info >/dev/null 2>&1 && ok "Mailpit" || ko "Mailpit"

AVAIL="$(free -m | awk '/^Mem:/ {print $7}')"
[ "$AVAIL" -ge 800 ] && ok "Memory available: ${AVAIL} MB (min 800)" || ko "Memory available: ${AVAIL} MB (min 800)"

curl -fsS -o /dev/null https://grafana.com/api/plugins/grafana-clock-panel && ok "Network: grafana.com plugin catalog" \
  || ko "Network: grafana.com plugin catalog unreachable"

curl -fsS -o /dev/null https://basemaps.cartocdn.com/gl/ 2>/dev/null || curl -sI https://basemaps.cartocdn.com/gl/ 2>/dev/null | grep -q "^HTTP" \
  && ok "Network: map tiles (CARTO)" || ko "Network: map tiles (CARTO) unreachable (Geomap without background)"

echo "----"
[ "$KO" = 0 ] && echo "Result: stack ready" || echo "Result: fix the KO lines"
exit "$KO"
