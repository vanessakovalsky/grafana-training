# Module 03 — Corrections

## Lab 03.1 ⭐ — Raccorder Prometheus et voir le réseau
### Solution
Étapes de l'énoncé. Contrôle par l'API (terminal du bureau) :
```bash
cd ~/grafana-training/stack
curl -s -u "admin:$(grep ^GRAFANA_ADMIN_PASSWORD .env | cut -d= -f2)" \
  http://localhost:3000/grafana/api/datasources | jq -r '.[] | .name + " " + .url'
```
Sortie attendue :
```
Prometheus http://prometheus:9090
```
Métriques du simulateur dans **Metrics browser** (15) : `telcea_call_attempts_total`, `telcea_call_failures_total`, `telcea_cell_traffic_bytes_total`, `telcea_cell_users`, `telcea_link_bytes_total`, `telcea_link_capacity_bits_per_second`, `telcea_link_packet_loss_ratio`, `telcea_router_cpu_ratio`, `telcea_site_info`, `telcea_site_latency_seconds_bucket`, `telcea_site_latency_seconds_count`, `telcea_site_latency_seconds_sum`, `telcea_site_on_battery`, `telcea_site_temperature_celsius`, `telcea_site_up`.

### Pourquoi
- URL résolue par le serveur Grafana (accès *Server*), dans le réseau Docker : nom du service `prometheus`.
- Source par défaut : préselectionnée dans chaque nouveau panel (gain de temps aux M04 et M05).

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| `Post "http://localhost:9090/api/v1/query": dial tcp 127.0.0.1:9090: connect: connection refused` | `localhost` = conteneur Grafana | URL `http://prometheus:9090` |
| `no such host` | Faute de frappe dans le nom du service | `prometheus` en minuscules |
| Explore vide | Plage de temps antérieure au démarrage de la stack | **Last 1 hour** |
| Erreur de syntaxe PromQL | Éditeur en mode **Builder** avec du texte collé | Basculer en **Code** avant de coller |

## Lab 03.2 ⭐ — Interroger InfluxDB en SQL
### Solution
Étapes de l'énoncé : **Explore** → source `InfluxDB` → requête collée → **Format** `Time series` → **Run query**.
```sql
SELECT $__dateBin(time) AS time, avg(usage_user) AS cpu_utilisateur
FROM cpu
WHERE $__timeFilter(time)
GROUP BY 1
ORDER BY 1
```
Résultat : une courbe `cpu_utilisateur` (2 à 20 % selon la charge).

### Pourquoi
- `$__timeFilter(time)` = plage de temps du sélecteur de Grafana ; `$__dateBin(time)` = regroupement à l'intervalle adapté à la largeur du graphe.
- Alias `AS time` + **Format** `Time series` → Grafana reconnaît la colonne de temps et trace une courbe.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Source `InfluxDB` absente de la liste | Source pas encore créée | Signaler à la formatrice (rattrapage, 5 s) |
| `no time column found` | `$__dateBin(time)` sans alias | `$__dateBin(time) AS time` |
| Tableau au lieu d'une courbe | **Format** `Table` | **Format** `Time series` |
| `Cannot retrieve database: External error: database not found` | Source mal configurée (base) | Signaler à la formatrice |

## Défis facultatifs

## Défi 03.2b ⭐⭐ — Créer soi-même une source InfluxDB
### Solution
**Connections → Data sources → Add new data source → InfluxDB**, puis :
- **Name** : `InfluxDB (test)`
- **Query language** : `SQL`
- **URL** : `http://influxdb:8181`
- **Database** : `systeme` ; **Token** : valeur après `INFLUX_TOKEN=` (`grep INFLUX_TOKEN ~/grafana-training/stack/.env`)
- **Insecure Connection** : activé → **Save & test** : `OK`

Champs enregistrés (API `GET /api/datasources/name/InfluxDB%20(test)`) :
```
"url": "http://influxdb:8181", "jsonData": {"dbName": "systeme", "insecureGrpc": true, "version": "SQL"}
```

### Pourquoi
- **Query language** choisi en premier : il détermine les champs affichés ensuite (Database / Token en SQL, User / Password en InfluxQL).
- **Insecure Connection** : InfluxDB 3 est interrogé en Flight SQL (gRPC) sans TLS dans la stack.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| `transport: authentication handshake failed: tls: first record does not look like a TLS handshake` | **Insecure Connection** désactivé | Activer, **Save & test** |
| `flightsql: rpc error: code = Unauthenticated` | Jeton incomplet (copie tronquée) | Recopier toute la valeur après `INFLUX_TOKEN=` |
| `Cannot retrieve database: External error: database not found: system` | Base `system` au lieu de `systeme` | `systeme` (base créée par Telegraf) |
| `no time column found` | `$__dateBin(time)` sans alias | `$__dateBin(time) AS time` |
| `DATE_BIN stride must be non-zero` | Requête lancée hors Grafana (intervalle absent) | Exécuter depuis Explore ou un panel |

## Défi 03.3 ⭐⭐ — Retrouver ses données
### Solution
Valeurs relevées au banc le 18/11/2026 vers 10 h 30 (variables selon l'heure).

| # | Requête | Valeur relevée |
|---|---|---|
| 1 | `sum(telcea_site_up)` | `12` |
| 2 | `topk(1, sum by (region) (telcea_cell_users))` | `Ile-de-France` : 2 581 |
| 3 | `sum by (region) (rate(telcea_cell_traffic_bytes_total{direction="down"}[5m])) * 8 / 1e6` | Bretagne 237, Île-de-France 776, Hauts-de-France 269, Provence 363 |
| 4 | `100 * (1 - sum by (region) (rate(telcea_call_failures_total[5m])) / sum by (region) (rate(telcea_call_attempts_total[5m])))` | 99,4 à 99,9 % |
| 5 | `sum by (link) (rate(telcea_link_bytes_total[5m])) * 8 / sum by (link) (telcea_link_capacity_bits_per_second) * 100` | REN-PAR 27 %, LIL-PAR 30 %, MRS-PAR 41 % |
| 6 | Prometheus : `100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])))` | 17,3 % |
| 6 | InfluxDB : `SELECT $__dateBin(time) AS time, avg(100 - usage_idle) AS cpu FROM cpu WHERE $__timeFilter(time) GROUP BY 1 ORDER BY 1` | 16,6 % |

### Pourquoi
- Q3, Q4, Q5 : `rate()` sur chaque compteur, PUIS `sum by` : débit fiable même si une cible redémarre.
- Q5 : `sum by (link)` des deux côtés de la division → mêmes étiquettes, division possible (sinon résultat vide).
- Q6 : node-exporter et Telegraf lisent les mêmes compteurs du noyau ; l'écart vient des fenêtres de calcul.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Q5 : résultat vide | Division entre séries d'étiquettes différentes (`direction` d'un côté seulement) | Agréger les deux côtés `by (link)` |
| Q3 : valeurs en milliards | Bits/s non convertis | `/ 1e6` ou unité Mbit/s dans le panel (M05) |
| Q4 : valeurs proches de 0 | Taux d'échec calculé au lieu du taux de réussite | `1 - ...` puis `* 100` |

### Variantes acceptables
- Q1 : `count(telcea_site_up == 1)`.
- Q2 : lecture du graphe `sum by (region) (telcea_cell_users)` sans `topk`.
- Q6 InfluxDB : `avg(usage_user + usage_system)` (plus faible : exclut `iowait`, `steal`).

## Défi 03.4 ⭐⭐⭐ — Latence au 95e centile et mémoire moyenne
### Solution
```promql
histogram_quantile(0.95, sum by (le, region) (rate(telcea_site_latency_seconds_bucket[5m]))) * 1000
```
Relevé au banc : Bretagne 59 ms, Île-de-France 47 ms, Hauts-de-France 54 ms, Provence 58 ms.

```sql
SELECT date_bin(INTERVAL '5 minutes', time) AS time, avg(available_percent) AS memoire_dispo
FROM mem
WHERE $__timeFilter(time)
GROUP BY 1
ORDER BY 1
```
Relevé au banc : 57,6 à 57,8 % par tranche de 5 minutes.

### Pourquoi
- `histogram_quantile` attend l'étiquette `le` (bornes des tranches) : la conserver dans le `sum by`.
- `date_bin(INTERVAL '5 minutes', time)` : tranche fixe, contrairement à `$__dateBin` (intervalle calculé par Grafana selon la largeur du graphe).

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Résultat `NaN` ou vide | `le` absent du `sum by` | `sum by (le, region)` |
| Valeurs < 1 | Secondes non converties | `* 1000` (ou unité `s` dans le panel) |

## QCM — Réponses
1. **A** — URL résolue par le serveur Grafana dans le réseau Docker : nom du service.
2. **C** — Un compteur ne fait que croître : `rate()` donne le débit par seconde.
3. **B** — `=~` applique une expression régulière : `PAR-.*`.
4. **D** — `sum by (region)` additionne en conservant une série par valeur de `region`.
5. **C** — `$__timeFilter(time)` traduit la plage de temps du tableau de bord en clause `WHERE`.
6. **A** — Flight SQL sans TLS dans la stack : **Insecure Connection** obligatoire.
