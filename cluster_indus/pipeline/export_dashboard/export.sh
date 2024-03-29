KEY="VAR_GRAFANA_IMPORT_TOKEN"
HOST="VAR_GRAFANA_IMPORT_URL"

GRAFANA_DASHBOARDS_FOLDER="exports"
echo "Exporting Grafana dashboards from $HOST"
mkdir -p "${GRAFANA_DASHBOARDS_FOLDER}"
for dash in $(curl -sSL -k -H "Authorization: Bearer ${KEY}" "${HOST}/api/search?query=&" | jq -r '.[] | select(.type == "dash-db") | .uid'); do
  curl -sSL -k -H "Authorization: Bearer ${KEY}" "${HOST}/api/dashboards/uid/$dash" | jq -r . >${GRAFANA_DASHBOARDS_FOLDER}/${dash}.json
  slug=$(cat ${GRAFANA_DASHBOARDS_FOLDER}/${dash}.json | jq -r '.meta.slug')
  folder=$(cat ${GRAFANA_DASHBOARDS_FOLDER}/${dash}.json | jq -r '.meta.folderTitle')
  mkdir -p "${GRAFANA_DASHBOARDS_FOLDER}/${folder}"
  mv ${GRAFANA_DASHBOARDS_FOLDER}/${dash}.json "${GRAFANA_DASHBOARDS_FOLDER}/${folder}/${slug}.json"
done