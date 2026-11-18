# Aide-mémoire Grafana 13

## Accès (VM de formation)
| Élément | Valeur |
|---|---|
| Grafana | `https://stagiaireNN.<SESSION>.kovalibre-labs.com/grafana/` (`admin`) |
| Bureau Linux | `https://stagiaireNN.<SESSION>.kovalibre-labs.com/` (`stagiaire`) |
| Courriels de test | `https://stagiaireNN.<SESSION>.kovalibre-labs.com/mail/` |
| Prometheus, simulateur (depuis le bureau) | `http://localhost:9090`, `http://localhost:9200/metrics` |
| Contrôle de la stack | `~/grafana-training/stack/preflight.sh` |

## Menus utiles
| Besoin | Chemin |
|---|---|
| Sources de données | Connections → Data sources |
| Explorer | Explore (`Ctrl + K` : palette de commandes) |
| Nouveau tableau de bord | Dashboards → New → New dashboard |
| Importer | Dashboards → New → Import dashboard |
| Corbeille | Dashboards → Recently deleted |
| Règles, contacts, routage | Alerting → Alert rules / Notification configuration / Silences |
| Utilisateurs, équipes | Administration → Users and access |
| Plugins | Administration → Plugins and data → Plugins |
| Configuration effective | Administration → General → Settings |

## PromQL
```promql
telcea_site_up{region="Bretagne"}                       # filtre exact
telcea_cell_users{site=~"PAR-.*"}                        # expression régulière
rate(telcea_cell_traffic_bytes_total[5m]) * 8            # compteur -> débit (bit/s)
sum by (region) (telcea_cell_users)                      # total par région
histogram_quantile(0.95, sum by (le) (rate(telcea_site_latency_seconds_bucket[5m])))
telcea_site_up * on(site) group_left(latitude, longitude) telcea_site_info
```

## SQL InfluxDB 3 (dans Grafana)
```sql
SELECT $__dateBin(time) AS time, avg(usage_user) AS cpu
FROM cpu WHERE $__timeFilter(time) GROUP BY 1 ORDER BY 1
```

## Réglages des panels
| Besoin | Réglage |
|---|---|
| Ratio 0-1 en % | Unit `Percent (0.0-1.0)` |
| Débit | Unit `bits/sec(SI)` |
| Couleur selon la valeur | Thresholds (+ **Color mode**) |
| `1` → « En service » | Value mappings |
| Exception pour une série | **+ Add field override** → Fields with name |
| Valeur actuelle | Requête en **Instant** ; calcul `Last *` |
| Plusieurs sources | Data source `-- Mixed --` |

## Variables
| Type | Exemple |
|---|---|
| Query | `label_values(telcea_site_info, region)` |
| Chaînée | `label_values(telcea_site_info{region=~"$region"}, site)` |
| Utilisation | `{region=~"$region"}` (`=~` en multi-valeur) ; `[$fenetre]` |

## Alertes
`Règle = Requête + Condition + Évaluation (pending) + Labels + Annotations`
`Routage : labels de l'alerte → politique de notification → point de contact`

## Plugins (Grafana 13)
```bash
docker compose exec grafana grafana cli plugins install <ID>
docker compose restart grafana
```

## Configuration
`Valeur effective = defaults.ini < grafana.ini < variables GF_<SECTION>_<CLÉ>`
