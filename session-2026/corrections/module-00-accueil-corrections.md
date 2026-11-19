# Module 00 — Corrections

## Lab 00.1 ⭐ — Ouvrir Grafana
### Solution
Étapes de l'énoncé, sans variante.

### Pourquoi
- Grafana publié sous `/grafana/` par le Nginx de la VM, avec le même certificat que le bureau : un seul port ouvert (443), aucun logiciel à installer.
- Même mot de passe pour Grafana et le bureau : un seul secret par stagiaire.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Page du bureau au lieu de Grafana | `/grafana/` oublié en fin d'URL | Compléter l'URL |
| `Invalid username or password` | Espace copiée en fin de mot de passe | Retaper le mot de passe |
| Page Grafana sans style | Publication Nginx absente | Formatrice : relancer `setup.sh` sur la VM |
| Bureau gris, « connexion perdue » | Coupure réseau ou proxy | Recharger la page ; Grafana reste utilisable |

## Défi 00.2 ⭐⭐ — Découvrir les données brutes du réseau Telcéa
### Solution
- Navigateur du bureau (Firefox) → `http://localhost:9200/metrics`.
- Ligne recherchée (relevée au banc le 18/11/2026 à 10 h ; valeur variable selon l'heure : cycle jour / nuit) :
  ```
  telcea_cell_users{region="Ile-de-France",site="PAR-01",techno="5G"} 914.0
  ```
- `telcea_site_info` : 12 lignes, une par site (REN-01 à AVI-01).

### Pourquoi
- Format texte Prometheus = nom + étiquettes + valeur : la base de toutes les requêtes du M03.
- Les étiquettes (`site`, `region`, `techno`) serviront de filtres et de variables (M06).

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| `localhost:9200` refusé depuis le poste personnel | Port non publié sur Internet (volontaire) | Ouvrir l'URL dans le navigateur DU BUREAU |

## Défi 00.3 ⭐⭐⭐ — Vérifier l'état de la stack en ligne de commande
### Solution
```bash
cd ~/grafana-training/stack
./preflight.sh
```
Sortie relevée au banc (18/11/2026, poste local ; `<MO>` = mémoire disponible, variable) :
```
OK    Service grafana running
OK    Service prometheus running
OK    Service alertmanager running
OK    Service simulateur running
OK    Service node-exporter running
OK    Service cadvisor running
OK    Service influxdb running
OK    Service telegraf running
OK    Service loki running
OK    Service alloy running
OK    Service mailpit running
OK    Grafana health
OK    Telcea: 12 sites up
OK    Prometheus: all targets up
OK    Loki: simulator logs received
OK    InfluxDB: database systeme queried
OK    Mailpit
OK    Memory available: <MO> MB (min 800)
OK    Network: grafana.com plugin catalog
OK    Network: map tiles (CARTO)
----
Result: stack ready
```
Journaux d'alarmes : **Loki** (collectés par Alloy depuis la sortie du conteneur `simulateur`).

### Pourquoi
- Prometheus = valeurs numériques ; Loki = lignes de texte horodatées (alarmes) ; InfluxDB = mesures système de la VM.

### Variantes acceptables
- `docker compose ps` : liste des services, sans les contrôles de données.
- `docker compose logs simulateur` : lecture directe des alarmes, sans passer par Loki.

## QCM — Réponses
1. **C** — Grafana interroge des sources externes pour visualiser et alerter ; il ne stocke pas les mesures.
2. **A** — Série temporelle = suite de couples (horodatage, valeur) pour une même mesure et les mêmes étiquettes.
3. **D** — Prometheus collecte en mode *pull* : lecture périodique des pages `/metrics` des cibles.
4. **B** — Disponibilité = part du temps en service (ex. 99,9 % sur un mois).
5. **A** — Network Operations Center : centre de supervision du réseau.
6. **D** — Un seuil transforme une valeur en état (normal, attention, critique), affiché par une couleur ou une alerte.
