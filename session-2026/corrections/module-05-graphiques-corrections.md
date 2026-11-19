# Module 05 — Corrections

État final de référence : `scripts/m05/catch-up/tableau-de-bord.json` (généré par `scripts/m05/catch-up/generer.py` à partir de l'état M04).

## Lab 05.1 ⭐ — Unités et couleurs
### Solution
| Panel | Réglage | Valeur |
|---|---|---|
| Sites en service | **Thresholds** | Base `Red`, `12` `Green` |
| Débit descendant par région | **Unit** | `bits/sec(SI)` (`bps`) |
| Utilisation des liens de collecte | **Unit** | `Percent (0.0-1.0)` (`percentunit`) |

Extrait du modèle JSON du panel `Sites en service` :
```json
"thresholds": {"mode": "absolute", "steps": [{"color": "red", "value": null}, {"color": "green", "value": 12}]}
```

### Pourquoi
- Base rouge, `12` vert : vert seulement si les 12 sites sont en service ; un site perdu → rouge.
- `bits/sec(SI)` : la requête est déjà en bits (`* 8`) ; préfixes SI → `Mb/s`.
- `percentunit` : la requête renvoie un ratio 0-1 (division débit / capacité).

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Stat toujours vert même avec 11 sites | Base laissée verte, seuil `80` conservé | Base `Red`, seuil `12` `Green` |
| Liens affichés `0.41%` | Unité `Percent (0-100)` | `Percent (0.0-1.0)` |
| Débit `776 MB/s` au lieu de `Mb/s` | Unité `bytes/sec` (octets) alors que la requête est en bits (`* 8`) | `bits/sec(SI)` |
| Réglage appliqué au mauvais panel | Panel non ouvert en édition (**Edit** du tableau de bord seulement) | Menu du panel (⋮) → **Edit** |

## Lab 05.2 ⭐ — Un tableau d'état des sites
### Solution
Requête `telcea_site_up`, **Type** `Instant`, **Format** `Table`, visualisation **Table**, puis :
```json
"transformations": [{"id": "organize", "options": {
  "excludeByName": {"Time": true, "__name__": true, "instance": true, "job": true}}}],
"fieldConfig": {
  "defaults": {"mappings": [{"type": "value", "options": {
    "0": {"text": "Hors service", "color": "red", "index": 0},
    "1": {"text": "En service", "color": "green", "index": 1}}}]},
  "overrides": [{"matcher": {"id": "byName", "options": "Value"},
    "properties": [{"id": "custom.cellOptions", "value": {"type": "color-background"}}]}]
}
```
Tableau obtenu : 12 lignes, colonnes `region`, `site`, `techno`, `Value` (`En service` sur fond vert).

### Pourquoi
- **Instant** : une ligne par site (valeur actuelle) ; **Range** = une ligne par horodatage.
- Le mapping porte le texte ET la couleur ; dans une table, la couleur n'est appliquée qu'avec un **Cell type** coloré.
- Override sur `Value` uniquement : un fond coloré sur toutes les colonnes rendrait le tableau illisible.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Texte du mapping affiché, sans couleur | **Cell type** laissé en `Auto` (couleur du mapping ignorée dans une table) | Override `Value` → **Cell type** `Colored background` |
| Toutes les cellules colorées | **Cell type** réglé dans les options standard | Le régler dans l'override `Value` uniquement |
| Une ligne par horodatage | Requête en **Range** | **Type** : `Instant` |

## Défis facultatifs

## Défi 05.2b ⭐⭐ — Finitions des panels
### Solution
Extrait du modèle JSON (Settings → **JSON Model**) du panel `Utilisation des liens de collecte` :
```json
"fieldConfig": {
  "defaults": {
    "unit": "percentunit", "min": 0, "max": 1,
    "thresholds": {"mode": "absolute", "steps": [
      {"color": "green", "value": null}, {"color": "orange", "value": 0.8}, {"color": "red", "value": 0.9}]},
    "custom": {"thresholdsStyle": {"mode": "dashed"}}
  }
}
```
Stat `Sites en service` : `"colorMode": "background"`, `"graphMode": "none"`, calcul `lastNotNull` (`Last *`), seuils rouge / 10 orange / 12 vert.

Table `État des sites` :
```json
"transformations": [{"id": "organize", "options": {
  "excludeByName": {"Time": true, "__name__": true, "instance": true, "job": true},
  "indexByName": {"site": 0, "region": 1, "techno": 2, "Value": 3},
  "renameByName": {"site": "Site", "region": "Région", "techno": "Techno", "Value": "État"}}}],
"fieldConfig": {"overrides": [{"matcher": {"id": "byName", "options": "État"},
  "properties": [{"id": "custom.cellOptions", "value": {"type": "color-background"}}]}]}
```

### Pourquoi
- Min 0, max 1 : échelle stable (sinon l'axe s'adapte et un lien à 30 % semble saturé).
- Seuil orange à 10 : 2 sites perdus = situation dégradée mais pas critique.
- Override sur le nom FINAL de la colonne (`État`) : les overrides s'appliquent après les transformations.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Lignes de seuils absentes | **Show thresholds** sur `Off` | `As lines (dashed)` |
| Override sans effet après renommage | Override resté sur `Value` | Override sur `État` |
| Mini-graphique encore visible | **Graph mode** `Area` | **Graph mode** `None` |

## Défi 05.3 ⭐⭐ — Carte, disponibilité, jauges
### Solution
| Panel | Requête | Réglages clés |
|---|---|---|
| Carte des sites | `telcea_site_up * on(site) group_left(ville, latitude, longitude) telcea_site_info` (Instant, Table) | **Convert field type** latitude / longitude → Number ; couche Markers, **Location** `Coords` ; couleur : champ `Value`, seuils rouge / 1 vert ; **Text label** : `site` ; vue centrée sur la France (zoom ≈ 5,3) |
| Disponibilité des sites | `telcea_site_up`, légende `{{site}}` | State timeline, value mapping En service / Hors service, **Show values** `Never` |
| Réussite des appels (5 min) | `1 - sum by (region) (rate(telcea_call_failures_total[5m])) / sum by (region) (rate(telcea_call_attempts_total[5m]))` (Instant) | Bar gauge horizontal, `percentunit`, min `0.95`, max `1`, 2 décimales, seuils rouge / 0.98 orange / 0.99 vert |
| CPU de la VM | `100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])))` | Gauge, `percent`, 0-100, vert / 65 orange / 90 rouge |
| Mémoire utilisée de la VM | `100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)` | Idem CPU |

Relevé au banc (18/11/2026, 10 h 40) : CPU 13,1 %, mémoire 46,0 %, réussite des appels 99,3 à 100 %.

### Pourquoi
- `group_left(...)` : recopie des étiquettes de `telcea_site_info` (une série par site) sur `telcea_site_up`.
- Min `0.95` sur le Bar gauge : sinon toutes les barres sont pleines (99,x %) et aucun écart n'est visible.
- `MemAvailable` plutôt que `MemFree` : le cache disque est récupérable (« libre » sous-estime la mémoire disponible).

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Carte sans marqueur | Coordonnées en texte | **Convert field type** → `Number` |
| Marqueurs au large de l'Afrique (0, 0) | Champs latitude / longitude non choisis dans **Location** | **Location** `Coords` + choix des deux champs |
| Résultat vide (aucune erreur) | `on(site)` oublié : étiquettes différentes des deux côtés, aucune correspondance | `on(site) group_left(...)` |
| Fond de carte gris | Accès Internet sortant bloqué (fond par défaut : CARTO) | Vérifier `curl -sI https://basemaps.cartocdn.com/gl/` depuis la VM |

### Variantes acceptables
- Status history au lieu de State timeline : valide (cases par intervalle).
- Mémoire en Bar gauge : valide si unité et seuils identiques.

## Défi 05.4 ⭐⭐⭐ — Trafic réseau de la VM en miroir
### Solution
```promql
sum(rate(node_network_receive_bytes_total{device!="lo"}[5m])) * 8     # légende RECEIVE
sum(rate(node_network_transmit_bytes_total{device!="lo"}[5m])) * 8    # légende TRANSMIT
```
```json
"overrides": [
  {"matcher": {"id": "byName", "options": "RECEIVE"},
   "properties": [{"id": "color", "value": {"mode": "fixed", "fixedColor": "blue"}}]},
  {"matcher": {"id": "byName", "options": "TRANSMIT"},
   "properties": [{"id": "color", "value": {"mode": "fixed", "fixedColor": "orange"}},
                  {"id": "custom.transform", "value": "negative-Y"}]}
]
```
Bonus : override **Fields with name** `REN-PAR` → couleur fixe `purple` sur le panel des liens.

### Pourquoi
- **Transform → Negative Y** : affichage inversé sans modifier la donnée (l'infobulle reste positive).
- Couleurs fixes : lecture identique sur tous les écrans du NOC.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Override sans effet | Légende différente (`Transmit`) du nom sélectionné | Même casse : `TRANSMIT` |
| Valeurs négatives dans l'infobulle | Requête multipliée par `-1` | Override **Negative Y** à la place |

## QCM — Réponses
1. **B** — `rate()` transforme le compteur d'octets en débit par seconde.
2. **A** — `percentunit` attend un ratio 0-1.
3. **D** — `Mean` moyenne les valeurs de la plage ; `Last *` donne l'état actuel.
4. **C** — Un value mapping associe une valeur à un texte et une couleur.
5. **B** — Override **Fields with name** : exception pour une série.
6. **C** — La couche Markers attend des champs numériques de latitude et de longitude.
7. **A** — Settings → General (M04).
8. **D** — L'URL est résolue par le serveur Grafana dans le réseau Docker (M03).
