# Module 01 — Corrections

## Lab 01.1 ⭐ — Compléter la chaîne de supervision de Telcéa
### Solution
| Composant | Rôle | Mode |
|---|---|---|
| Simulateur Telcéa | Collecte (exportateur : publie `/metrics` sur le port 9200) | *Pull* (lu par Prometheus) |
| node-exporter | Collecte (mesures système de la VM, port 9100) | *Pull* |
| Telegraf | Collecte (agent : CPU, mémoire, disque, réseau de la VM) | *Push* (vers InfluxDB) |
| Prometheus | Stockage des métriques + évaluation de règles d'alerte | Lit les cibles (*pull*) |
| InfluxDB | Stockage des métriques système (base `systeme`) | Reçoit (*push*) |
| Alloy | Collecte des journaux des conteneurs | *Push* (vers Loki) |
| Loki | Stockage des journaux (alarmes du simulateur) | Reçoit (*push*) |
| Grafana | Visualisation, exploration, alertes | — (interroge les bases à l'affichage) |
| Alertmanager | Routage et envoi des notifications d'alerte de Prometheus | — |

Flèches attendues :
```
Simulateur, node-exporter, cAdvisor  <- lus par -  Prometheus  -> Grafana
Telegraf  -> InfluxDB  -> Grafana
Alloy     -> Loki      -> Grafana
Prometheus -> Alertmanager -> courriel (Mailpit)
```

### Pourquoi
- Grafana ne stocke pas les mesures : aucune flèche des collecteurs vers Grafana.
- Prometheus collecte ET stocke : il initie la lecture (*pull*).

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Flèche Telegraf → Grafana | Confusion collecte / visualisation | Rappel : Grafana interroge les bases, jamais les agents |
| Prometheus classé « visualisation » | Interface web de Prometheus (graphe simple) | Interface de test ; la visualisation partagée = Grafana |

## Exercice 01.2 ⭐⭐ — Classer les indicateurs du NOC
### Solution
| # | Famille | Type | Unité | Équipe |
|---|---|---|---|---|
| 1 | Disponibilité | Métrique (`telcea_site_up`) | 0 / 1 | radio |
| 2 | Capacité | Métrique (`telcea_cell_users`) | abonnés | radio |
| 3 | Capacité | Métrique (`telcea_link_bytes_total`) | % de la capacité | transport |
| 4 | Disponibilité | Journal (code `PWR-003`) | texte | radio |
| 5 | Qualité | Métrique (`telcea_call_failures_total` / `telcea_call_attempts_total`) | % | radio |
| 6 | Environnement | Métrique (`telcea_site_temperature_celsius`) | °C | radio |
| 7 | Capacité | Métrique (`telcea_router_cpu_ratio`) | % | transport |
| 8 | Capacité | Métrique (Telegraf, mesure `disk`) | octets, % | systeme |

### Pourquoi
- Un même événement peut exister sous deux formes : la coupure de BRE-01 = métrique (`telcea_site_up` à 0) ET journal (`PWR-003`).
- L'équipe destinataire détermine le routage des alertes (M09).

### Variantes acceptables
- Indicateur 4 classé « environnement » (cause : alimentation) : accepté si justifié.
- Indicateur 7 classé « qualité » (un routeur saturé dégrade la latence) : accepté si justifié.

## Défi 01.3 ⭐⭐⭐ — Choisir le mode de collecte
### Solution
| Cas | Choix | Justification | Limite |
|---|---|---|---|
| Boîtiers fibre derrière un routeur | *Push* | Aucun port entrant : seul l'envoi sortant traverse le routeur | Boîtier muet = absence de données à détecter (alerte « No Data ») |
| Script nocturne de 4 min | *Push* | Le script se termine avant d'être lu (Pushgateway pour Prometheus) | Dernière valeur conservée après la fin du script |
| 40 conteneurs éphémères | *Pull* + découverte automatique | Prometheus découvre les cibles (Docker, Kubernetes) et détecte une cible muette (`up == 0`) | Découverte à configurer ; conteneurs de moins de 15 s invisibles |

### Pourquoi
- *Pull* : détection immédiate d'une cible muette, configuration centralisée.
- *Push* : traversée des pare-feu, sources de courte durée.

### Variantes acceptables
- Cas 3 en *push* via OpenTelemetry (Alloy) : valide, choix fréquent pour les applications instrumentées.

## Bonus — Lire une page de métriques
Sortie relevée au banc :
```
# HELP telcea_site_up Radio site availability (1 up, 0 down)
# TYPE telcea_site_up gauge
telcea_site_up{region="Bretagne",site="REN-01",techno="5G"} 1.0
```
Page `http://localhost:9090/targets` : 4 cibles `UP` (`cadvisor`, `node`, `prometheus`, `telcea-reseau`).

## QCM — Réponses
1. **B** — Superviser ferme la boucle DevOps : les mesures orientent la planification suivante.
2. **A** — Ligne de texte horodatée = journal (log).
3. **D** — Prometheus lit périodiquement l'adresse `/metrics` des cibles (*pull*).
4. **C** — Grafana interroge les sources à chaque affichage ; sa base interne ne contient que la configuration.
5. **B** — Nagios : contrôles actifs aux états OK / WARNING / CRITICAL / UNKNOWN.
6. **D** — Latence et perte de paquets mesurent la qualité du service rendu.
