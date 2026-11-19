# Module 03 — Exercices

Parcours essentiel = Labs 03.1 et 03.2 (tout le groupe). Défis = facultatifs, en cas d'avance.
Toutes les requêtes sont fournies : copier-coller, sans retaper.

## Lab 03.1 ⭐ — Raccorder Prometheus et voir le réseau (guidé)
**Durée** : 15 min · **Objectif** : brancher Grafana sur Prometheus et afficher les sites du réseau
**Contexte** : le NOC de Telcéa raccorde la base de métriques du réseau à Grafana.
**Prérequis** : session `admin` ouverte

### Étapes
1. Menu ☰ → **Connections** → **Data sources** → **Add new data source** → **Prometheus**.
2. **Name** : `prometheus` (minuscules : nom compatible DNS exigé par Grafana 13) ; **Prometheus server URL** : copier-coller `http://prometheus:9090`. Ne rien changer d'autre.
3. Bouton **Save & test** (tout en bas de la page).
   Résultat attendu : `Successfully queried the Prometheus API.`
4. Bouton **Explore data** (en haut de la page).
5. À droite de la zone de requête, cliquer sur **Code**, puis copier-coller :
   ```promql
   telcea_site_up
   ```
   Bouton **Run query** (en haut à droite).
   Résultat attendu : courbes à `1` = sites en service.
6. Remplacer la requête par :
   ```promql
   sum by (region) (telcea_cell_users)
   ```
   **Run query**. Résultat attendu : 4 courbes, une par région (nombre d'abonnés connectés).

### Si bloqué
Source créée par la formatrice (rattrapage, 5 s) → reprise à l'étape 4 : menu ☰ → **Explore**, source `prometheus`.

### Critères de réussite
- [ ] Message `Successfully queried the Prometheus API.`
- [ ] 4 courbes pour la somme par région

---

## Lab 03.2 ⭐ — Interroger InfluxDB en SQL (guidé)
**Durée** : 10 min · **Objectif** : afficher l'utilisation processeur de la VM depuis InfluxDB
**Contexte** : l'équipe *systeme* stocke les mesures de la VM de supervision dans InfluxDB.
**Prérequis** : source `InfluxDB` déjà créée par la formatrice (jeton secret, présent seulement sur la VM)

### Étapes
1. Menu ☰ → **Explore**.
2. Liste des sources (en haut à gauche) : choisir `InfluxDB`.
3. Copier-coller la requête :
   ```sql
   SELECT $__dateBin(time) AS time, avg(usage_user) AS cpu_utilisateur
   FROM cpu
   WHERE $__timeFilter(time)
   GROUP BY 1
   ORDER BY 1
   ```
4. **Format** (sous la requête) : `Time series`. Bouton **Run query**.
   Résultat attendu : une courbe `cpu_utilisateur` entre 2 et 20 (% du temps processeur).

### Critères de réussite
- [ ] Courbe CPU affichée

---

## Défis facultatifs (en cas d'avance)

## Défi 03.2b ⭐⭐ — Créer soi-même une source InfluxDB
**Durée** : 10 min · **Objectif** : raccorder InfluxDB 3 en SQL, jeton compris
**Contexte** : le jeton d'accès n'est disponible que sur la VM (bureau Linux requis).

**Énoncé** : créer une source `influxdb-test` identique à `InfluxDB`, puis l'utiliser dans Explore avec la requête du Lab 03.2.

**Indices** :
- Jeton, dans un terminal du bureau : `grep INFLUX_TOKEN ~/grafana-training/stack/.env` (valeur après `=`)
- **Query language** `SQL` ; **URL** `http://influxdb:8181` ; **Database** `systeme` ; **Insecure Connection** activé

**Critères de réussite** :
- [ ] **Save & test** : `OK`

---

## Défi 03.3 ⭐⭐ — Retrouver ses données (semi-autonome)
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
