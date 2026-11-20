# Module 11 — Corrections

État final de référence : `scripts/m11/catch-up/croisement.json` (uid `tlc-croisement`, généré par `generer.py`).

## Lab 11.1 ⭐ — Deux sources dans un panel
### Solution
Extrait du modèle JSON :
```json
"datasource": {"type": "datasource", "uid": "-- Mixed --"},
"interval": "1m",
"targets": [
  {"refId": "A", "datasource": {"type": "prometheus"}, "legendFormat": "node-exporter",
   "expr": "100 * (1 - avg(rate(node_cpu_seconds_total{mode=\"idle\"}[1m])))"},
  {"refId": "B", "datasource": {"type": "influxdb"}, "format": "time_series", "rawQuery": true,
   "rawSql": "SELECT $__dateBin(time) AS time, avg(100 - usage_idle) AS telegraf FROM cpu WHERE $__timeFilter(time) GROUP BY 1 ORDER BY 1"}
]
```
Relevé au banc : courbes entre 8 et 45 %, écart habituel de 1 à 5 points.

### Pourquoi
- `rate(...[1m])` et `$__dateBin` sur 1 min : même granularité, comparaison honnête.
- Nom de série InfluxDB = alias SQL (`telegraf`) ; nom Prometheus = légende.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Requête B en erreur `no time column found` | Alias `AS time` absent | `$__dateBin(time) AS time` |
| Une seule source proposée par requête | Panel non passé en `-- Mixed --` | Sélecteur **Data source** du panel |
| Courbe B absente | **Format** `Table` au lieu de **Time series** | **Format** `Time series` |

## Lab 11.2 ⭐ — Calculer l'écart entre les deux collecteurs
### Solution
```json
"transformations": [
  {"id": "joinByField", "options": {"mode": "outer"}},
  {"id": "calculateField", "options": {"mode": "binary", "alias": "Ecart", "replaceFields": true,
    "binary": {"left": {"matcher": {"id": "byName", "options": "node-exporter"}}, "operator": "-",
               "right": {"matcher": {"id": "byName", "options": "telegraf"}}}}}
]
```

### Pourquoi
- Jointure sans champ imposé : Grafana prend le champ temps de chaque série (`Time` côté Prometheus, `time` côté InfluxDB).
- **Min interval** `1m` : horodatages alignés sur la minute dans les deux sources ; sans lui, Prometheus produit un point toutes les 15 s et la jointure ne trouve presque aucune paire.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| « No data » après le calcul (constaté au banc) | Jointure forcée sur `Time` (absent côté InfluxDB) ou pas différents | Champ de jointure vide + **Min interval** `1m` |
| Points isolés au lieu d'une courbe | Valeurs nulles entre deux minutes | **Connect null values** : `Always` |

## Défis facultatifs

## Défi 11.3 ⭐⭐ — Synthèse par site
### Solution
| Requête | Expression (Instant, Table) |
|---|---|
| A | `sum by (site, region) (telcea_cell_users)` |
| B | `sum by (site) (rate(telcea_cell_traffic_bytes_total{direction="down"}[5m])) * 8` |
| C | `histogram_quantile(0.95, sum by (le, site) (rate(telcea_site_latency_seconds_bucket[5m])))` |
| D | `sum by (site) (telcea_site_up)` |

Transformations : **Merge series/tables** → **Add field from calculation** (`Value #B` / `Value #A`, alias `Débit par abonné`) → **Organize fields by name** (masquer `Time`, renommer, ordonner) → **Sort by** `Abonnés` décroissant.
Relevé au banc (12 h 30) : PAR-01 en tête (1 321 abonnés, 470 Mb/s, 356 kb/s par abonné, 19,8 ms) ; REN-01 à 126 ms (en rouge, fin de tempête).

### Pourquoi
- `site` présent dans les 4 requêtes : clé commune de la fusion ; `region` n'est porté que par A (une seule colonne Région).
- Calcul dans Grafana : aucune requête PromQL complexe (division par étiquettes) à écrire.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| 4 tableaux au lieu d'un (sélecteur en bas du panel) | **Merge** absent | Ajouter **Merge series/tables** en premier |
| Colonne de calcul vide | Noms `Value #A` / `#B` différents (refId modifiés) | Noms réels dans **Table view** |
| Lignes dupliquées | Requête D avec `by (site, region)` et B avec `by (site)` | Mêmes étiquettes de regroupement, ou `region` dans une seule requête |

## Défi 11.4 ⭐⭐⭐ — Totaux par région
### Solution
Copie du tableau → transformation **Group by** (après **Organize**) : `Région` → **Group by** ; `Abonnés` → **Calculate** `Total` ; `Débit descendant` → `Total` ; `Latence p95` → `Max` ; autres champs ignorés.

### Pourquoi
- Agrégation dans Grafana sur des données déjà chargées : pas de requête supplémentaire vers Prometheus.
- Latence : `Max` (pire site) plutôt que `Total` (une somme de latences n'a pas de sens).

## QCM — Réponses
1. **C** — Source Mixed : une source par requête.
2. **A** — Add field from calculation, opération binaire.
3. **B** — Horodatages non alignés : aucune paire à joindre.
4. **A** — Ordre de la liste, chaque étape sur le résultat précédent.
5. **D** — Organize fields by name (renommage).
6. **C** — Table view / Query inspector : données après transformations.
