#!/usr/bin/env bash
# Installe et demarre la stack Telcea sur une VM stagiaire (ou en local).
#
# VM (via ../vm-stagiaire/run-on-vms.sh, qui fournit $VM_PASSWORD) :
#   ./setup.sh            -> .env, jeton InfluxDB, stack, Nginx (/grafana/, /mail/)
# Poste local (banc de test) :
#   ./setup.sh --local    -> pas de Nginx, Grafana sur http://localhost:3000/grafana/
#
# Idempotent : relancable sans perte (le .env et le jeton existants sont conserves).
# ASCII uniquement (script execute a distance).
set -euo pipefail
cd "$(dirname "$0")"
MODE="${1:-vm}"

# Paquet publie dans un sous-dossier de session (grafana-training/<SESSION>/stack) :
# lien ~/grafana-training/stack pour des chemins identiques dans tous les enonces.
if [ "$MODE" != "--local" ] && [ -d "$HOME/grafana-training" ] && [ ! -e "$HOME/grafana-training/stack" ]; then
  ln -s "$PWD" "$HOME/grafana-training/stack"
fi

log() { echo ">>> $*"; }

# 1. Adresse publique (server_name du site Nginx cree par vm-stagiaire)
if [ "$MODE" = "--local" ]; then
  ROOT_URL="http://localhost:${GRAFANA_PORT:-3000}/grafana/"
else
  FQDN="$(awk '/server_name/ {gsub(";",""); print $2; exit}' /etc/nginx/sites-available/guacamole)"
  [ -n "$FQDN" ] || { echo "server_name introuvable dans Nginx"; exit 1; }
  ROOT_URL="https://${FQDN}/grafana/"
fi

# 2. Jeton administrateur InfluxDB 3 (genere hors ligne, une seule fois)
mkdir -p influxdb
if [ ! -s influxdb/admin-token.json ]; then
  log "Generation du jeton InfluxDB"
  docker run --rm --user "$(id -u):$(id -g)" -v "$PWD/influxdb:/out" influxdb:3.12.2-core \
    influxdb3 create token --admin --offline --output-file /out/admin-token.json --format json >/dev/null
fi
chmod 644 influxdb/admin-token.json   # lu par l'utilisateur du conteneur InfluxDB
TOKEN="$(sed -n 's/.*"token": *"\([^"]*\)".*/\1/p' influxdb/admin-token.json | head -1)"

# 3. Fichier .env (mot de passe Grafana = mot de passe de la VM)
if [ ! -f .env ]; then
  log "Creation du .env"
  PASS="${VM_PASSWORD:-$(openssl rand -base64 12 | tr -d '/+=')}"
  umask 077
  printf 'GRAFANA_ADMIN_PASSWORD=%s\nGRAFANA_ROOT_URL=%s\nINFLUX_TOKEN=%s\n' \
    "$PASS" "$ROOT_URL" "$TOKEN" > .env
fi

# 4. Stack
log "Telechargement des images et demarrage de la stack"
docker compose pull --quiet --ignore-pull-failures
docker compose build --quiet
docker compose up -d

# 5. Nginx : Grafana et Mailpit publies a cote de Guacamole
if [ "$MODE" != "--local" ]; then
  log "Publication de /grafana/ et /mail/ dans Nginx"
  sudo install -m 644 nginx/telcea-locations.conf /etc/nginx/snippets/telcea-locations.conf
  for SITE in /etc/nginx/sites-available/guacamole; do
    grep -q 'telcea-locations.conf' "$SITE" || \
      sudo sed -i 's|^\(\s*\)location / {|\1include /etc/nginx/snippets/telcea-locations.conf;\n\1location / {|' "$SITE"
  done
  sudo nginx -t
  sudo systemctl reload nginx

  # Firefox (paquet .deb du depot APT Mozilla, pas de snap sous xrdp) :
  # interfaces locales Prometheus (9090), Alertmanager (9093), simulateur (9200)
  if ! dpkg -s firefox >/dev/null 2>&1 || ! grep -q packages.mozilla.org /etc/apt/sources.list.d/*.list 2>/dev/null; then
    log "Installation de Firefox (depot Mozilla)"
    sudo install -d -m 0755 /etc/apt/keyrings
    curl -fsSL https://packages.mozilla.org/apt/repo-signing-key.gpg \
      | sudo tee /etc/apt/keyrings/packages.mozilla.org.asc >/dev/null
    echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" \
      | sudo tee /etc/apt/sources.list.d/mozilla.list >/dev/null
    printf 'Package: *\nPin: origin packages.mozilla.org\nPin-Priority: 1000\n' \
      | sudo tee /etc/apt/preferences.d/mozilla >/dev/null
    sudo apt-get update -qq
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq firefox firefox-l10n-fr
  fi
fi

# 6. Attente de Grafana
log "Attente de Grafana"
for _ in $(seq 1 60); do
  curl -fsS http://localhost:${GRAFANA_PORT:-3000}/grafana/api/health >/dev/null 2>&1 && break
  sleep 5
done
curl -fsS http://localhost:${GRAFANA_PORT:-3000}/grafana/api/health
echo
log "Stack prete : ${ROOT_URL} (admin / mot de passe de la VM)"
