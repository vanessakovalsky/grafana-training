# Module 02 — Corrections

## Lab 02.1 ⭐ — Nommer l'organisation Telcéa
### Solution
Étapes de l'énoncé. Vérification par l'API (terminal du bureau) :
```bash
cd ~/grafana-training/stack
curl -s -u "admin:$(grep ^GRAFANA_ADMIN_PASSWORD .env | cut -d= -f2)" \
  http://localhost:3000/grafana/api/org
```
Sortie attendue (extrait) :
```
{"id":1,"name":"Telcéa","address":{"address1":"","address2":"","city":"","zipCode":"","state":"","country":""}}
```

### Pourquoi
- Fuseau `Europe/Paris` au niveau de l'organisation : tous les tableaux de bord affichent l'heure du NOC, quel que soit le navigateur.
- Langue laissée en anglais : libellés identiques à la documentation officielle et aux énoncés.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Nom non modifié | Bouton **Save preferences** utilisé à la place de **Update organization name** | Deux boutons distincts : un pour le nom, un pour les préférences |
| Palette sans effet | Raccourci capté par le navigateur ou Guacamole | Utiliser la loupe de la barre du haut |

## Défi 02.2 ⭐ — Lire la configuration effective et l'état de l'instance
### Solution
Valeurs relevées sur la VM (banc : `http://localhost:3000/grafana/`) :

| Section | Clé | Valeur |
|---|---|---|
| `server` | `root_url` | `https://stagiaireNN.<SESSION>.kovalibre-labs.com/grafana/` |
| `database` | `type` | `sqlite3` |
| `smtp` | `enabled` | `true` |
| `paths` | `provisioning` | `/etc/grafana/provisioning` |

Stats : `0` tableau de bord, `1` utilisateur, `1` organisation.
Plugins de sources installés : Prometheus, InfluxDB, Loki, Elasticsearch, CloudWatch, Zipkin (au choix).

### Pourquoi
- **Settings** affiche la valeur EFFECTIVE (fusion `defaults.ini` + `grafana.ini` + `GF_*`) : seule référence fiable.
- Les mots de passe y sont masqués (`*************`).

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Menu **Administration** absent | Session avec un utilisateur non administrateur | Se reconnecter en `admin` |

## Défi 02.3 ⭐⭐ — Surcharger un paramètre par variable `GF_*`
### Solution
```bash
cd ~/grafana-training/stack
cat > compose.override.yaml <<'EOF'
services:
  grafana:
    environment:
      GF_DASHBOARDS_MIN_REFRESH_INTERVAL: 10s
EOF
docker compose up -d grafana
```
Sortie attendue (dernière ligne) :
```
Container telcea-grafana-1  Started
```
Contrôle (banc, 18/11/2026) :
```bash
curl -s -u "admin:$(grep ^GRAFANA_ADMIN_PASSWORD .env | cut -d= -f2)" \
  http://localhost:3000/grafana/api/admin/settings | jq -c '.dashboards.min_refresh_interval'
```
```
"10s"
```

### Pourquoi
- `compose.override.yaml` : fusionné automatiquement par Docker Compose, sans toucher au fichier de référence.
- Section `[dashboards]` + clé `min_refresh_interval` → `GF_DASHBOARDS_MIN_REFRESH_INTERVAL`.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Valeur inchangée dans **Settings** | `docker compose restart` (ne relit pas l'environnement) | `docker compose up -d grafana` (recrée le conteneur) |
| `yaml: line 3: mapping values are not allowed` | Indentation par tabulations | Indentation par 2 espaces |
| Valeur inchangée | Faute dans le nom (`GF_DASHBOARD_...` sans S) | Nom exact de la section : `dashboards` |

### Variantes acceptables
- Ajout de la variable dans `compose.yaml` : fonctionne, mais modifie le fichier de référence (conflit lors d'une mise à jour du dépôt).

## Défi 02.4 ⭐⭐⭐ — Provisionner le tableau de bord d'accueil du NOC
### Solution
Fichier `stack/grafana/provisioning/dashboards/noc.yaml` :
```yaml
apiVersion: 1
providers:
  - name: noc
    folder: NOC
    type: file
    allowUiUpdates: false
    options:
      path: /etc/grafana/provisioning/dashboards/noc
```
Fichier `stack/grafana/provisioning/dashboards/noc/lisez-moi.json` :
```json
{
  "uid": "noc-lisez-moi",
  "title": "[TLC] NOC — Lisez-moi",
  "tags": ["telcea", "noc"],
  "panels": [
    {
      "type": "text",
      "title": "Consignes du NOC",
      "gridPos": {"x": 0, "y": 0, "w": 12, "h": 6},
      "options": {"mode": "markdown",
        "content": "## NOC Telcéa\n- Astreinte radio : poste 1001\n- Astreinte transport : poste 1002"}
    }
  ],
  "schemaVersion": 41
}
```
```bash
docker compose restart grafana
```
Contrôle relevé au banc :
```bash
curl -s -u "admin:$(grep ^GRAFANA_ADMIN_PASSWORD .env | cut -d= -f2)" \
  http://localhost:3000/grafana/api/dashboards/uid/noc-lisez-moi | jq -c '.meta | {provisioned, provisionedExternalId}'
```
```
{"provisioned":true,"provisionedExternalId":"lisez-moi.json"}
```

### Pourquoi
- Dossier de provisioning monté dans le conteneur (`./grafana/provisioning:/etc/grafana/provisioning`) : fichier visible sans reconstruction.
- `allowUiUpdates: false` : le fichier reste la seule source de vérité.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Tableau de bord absent | JSON invalide (virgule finale) | `docker compose logs grafana \| grep -i provisioning` ; valider avec `jq . lisez-moi.json` |
| Dossier créé mais vide | `path` différent du dossier monté | Chemin VU PAR LE CONTENEUR (`/etc/grafana/...`) |

### Variantes acceptables
- `foldersFromFilesStructure: true` (sans `folder`) : dossier déduit de l'arborescence des fichiers.

### Nettoyage
Supprimer `noc.yaml` et `noc/` puis `docker compose restart grafana` : le tableau de bord disparaît ; le dossier `NOC` vide reste (suppression dans **Dashboards**).

## QCM — Réponses
1. **C** — La base interne contient la configuration (utilisateurs, tableaux de bord, alertes), jamais les mesures.
2. **B** — `GF_<SECTION>_<CLÉ>` en majuscules : `GF_SERVER_ROOT_URL`.
3. **D** — Les variables d'environnement l'emportent sur les fichiers `.ini`.
4. **A** — **Settings** affiche la configuration effective, fusion de toutes les sources.
5. **C** — Ressource provisionnée : le fichier fait foi, l'enregistrement depuis l'interface est refusé.
6. **B** — Grafana 13 a supprimé `grafana-cli` ; commande : `grafana cli plugins install <ID>`.
