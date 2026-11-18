# Module 03 — Exercices

## Lab 03.1 ⭐ — Raccorder Prometheus et explorer le réseau (guidé)
**Durée** : 20 min · **Objectif** : obtenir `Successfully queried the Prometheus API.` puis afficher 3 requêtes dans Explore
**Contexte** : le NOC de Telcéa raccorde la base de métriques du réseau à Grafana.
**Prérequis** : M02 (session `admin`)

### Étapes
1. Menu **Connections → Data sources → Add new data source**, choisir **Prometheus**.
2. Renseigner **Name** : `Prometheus` ; **Prometheus server URL** : `http://prometheus:9090`. Laisser les autres champs par défaut.
3. Cliquer sur **Save & test** (bas de page).
   Résultat attendu :
   ```
   Successfully queried the Prometheus API.
   ```
4. Cliquer sur **Explore data** (haut de page), passer l'éditeur en **Code** (bouton à droite de la requête), saisir puis exécuter (`Shift + Entrée` ou bouton **Run query**) :
   ```promql
   telcea_site_up
   ```
   Résultat attendu : 12 courbes à `1` (une par site), légende `telcea_site_up{instance="simulateur:9200", job="telcea-reseau", region="Bretagne", site="REN-01", techno="5G"}` pour la première.
5. Remplacer la requête par :
   ```promql
   sum by (region) (telcea_cell_users)
   ```
   Résultat attendu : 4 courbes (une par région), Île-de-France au-dessus de 2 000 abonnés en journée.
6. Ouvrir **Metrics browser**, taper `telcea_` : noter les 15 métriques du simulateur.
7. Plage de temps (en haut à droite) : choisir **Last 6 hours** et observer l'évolution des abonnés.

### Critères de réussite
- [ ] Source `Prometheus` enregistrée, test réussi, cochée par défaut (**Default**)
- [ ] 12 séries pour `telcea_site_up`, 4 séries pour la somme par région

---

## Lab 03.2 ⭐ — Raccorder InfluxDB 3 en SQL (guidé)
**Durée** : 15 min · **Objectif** : interroger en SQL les mesures système de la VM depuis Grafana
**Contexte** : l'équipe *systeme* stocke les mesures de la VM de supervision dans InfluxDB (collecteur Telegraf).
**Prérequis** : Lab 03.1

### Étapes
1. Récupérer le jeton InfluxDB : dans le bureau Linux, ouvrir un terminal et taper :
   ```bash
   grep INFLUX_TOKEN ~/grafana-training/stack/.env
   ```
   Résultat attendu : `INFLUX_TOKEN=apiv3_` suivi d'une longue chaîne. Copier la valeur après `=`.
2. Menu **Connections → Data sources → Add new data source**, choisir **InfluxDB**.
3. Renseigner dans cet ordre :
   - **Name** : `InfluxDB`
   - **Query language** : `SQL`
   - **URL** : `http://influxdb:8181`
   - **Database** : `systeme`
   - **Token** : valeur copiée à l'étape 1
   - **Insecure Connection** : activé
4. **Save & test**. Résultat attendu : message `OK`.
5. **Explore data**, éditeur en mode code SQL, saisir :
   ```sql
   SELECT $__dateBin(time) AS time, avg(usage_user) AS cpu_utilisateur
   FROM cpu
   WHERE $__timeFilter(time)
   GROUP BY 1
   ORDER BY 1
   ```
   Format : **Time series**. Exécuter.
   Résultat attendu : une courbe `cpu_utilisateur` entre 2 et 20 (% du temps processeur).

### Critères de réussite
- [ ] Source `InfluxDB` enregistrée, test `OK`
- [ ] Courbe CPU affichée sur la dernière heure

---

## Exercice 03.3 ⭐⭐ — Retrouver ses données (semi-autonome)
**Durée** : 25 min · **Objectif** : répondre à 6 questions du responsable du NOC par une requête chacune
**Contexte** : réunion de 14 h du NOC ; chaque réponse doit être justifiée par une requête (copie dans un fichier texte).

**Énoncé** :
1. Combien de sites sont en service maintenant ?
2. Quelle région compte le plus d'abonnés connectés ?
3. Quel est le débit descendant total (Mbit/s) par région ?
4. Quel est le taux de réussite des appels (%) par région sur les 5 dernières minutes ?
5. Quel est le taux d'utilisation (%) de chacun des 3 liens de collecte ?
6. Quelle est l'utilisation CPU (%) de la VM selon Prometheus ET selon InfluxDB ?

**Indices** :
- Métriques utiles : `telcea_site_up`, `telcea_cell_users`, `telcea_cell_traffic_bytes_total`, `telcea_call_attempts_total`, `telcea_call_failures_total`, `telcea_link_bytes_total`, `telcea_link_capacity_bits_per_second`, `node_cpu_seconds_total`
- Octets → bits : `* 8` ; bits/s → Mbit/s : `/ 1e6`
- Taux de réussite = `1 - échecs / tentatives`
- Split (Explore) : Prometheus à gauche, InfluxDB à droite

**Critères de réussite** :
- [ ] 6 requêtes notées, chacune avec sa valeur
- [ ] Question 5 : une série par lien (`REN-PAR`, `LIL-PAR`, `MRS-PAR`), valeurs entre 0 et 100
- [ ] Question 6 : écart entre les deux sources inférieur à 5 points

---

## Défi 03.4 ⭐⭐⭐ — Latence au 95e centile et mémoire moyenne (autonome)
**Durée** : 15 min · **Objectif** : exploiter un histogramme Prometheus et une agrégation temporelle SQL
**Contexte** : le contrat de service de Telcéa engage une latence inférieure à 100 ms pour 95 % des mesures.

**Énoncé** :
- Afficher la latence au 95e centile, en millisecondes, par région (`telcea_site_latency_seconds`).
- Afficher la mémoire disponible moyenne (%) de la VM par tranche de 5 minutes sur la dernière heure (InfluxDB, table `mem`).

Contraintes : une requête par question ; tranche de 5 minutes fixe (pas l'intervalle automatique) pour la seconde.

**Critères de réussite** :
- [ ] 4 courbes de latence, valeurs entre 20 et 100 ms hors incident
- [ ] 12 points maximum sur la courbe mémoire (1 h / 5 min)
