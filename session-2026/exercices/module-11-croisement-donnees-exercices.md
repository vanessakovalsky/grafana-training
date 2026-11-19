# Module 11 — Exercices

Parcours essentiel = Labs 11.1 et 11.2 (tout le groupe). Défis = facultatifs, en cas d'avance.
Toutes les requêtes sont fournies : copier-coller, sans retaper.

## Lab 11.1 ⭐ — Deux sources dans un panel (guidé)
**Durée** : 10 min · **Objectif** : afficher le CPU de la VM vu par node-exporter (Prometheus) et par Telegraf (InfluxDB) sur un même graphe
**Contexte** : l'équipe *systeme* soupçonne un collecteur de mal mesurer ; il faut comparer les deux.
**Prérequis** : sources `Prometheus` et `InfluxDB` (M03)

### Étapes
1. **Dashboards → NOC Telcéa → New → New dashboard**, **Custom grid** ; **Save** : `[TLC] Croisement — Réseau et système`, dossier `NOC Telcéa`.
2. Panneau **Add** → **Panel** → **Configure visualization** ; sélecteur **Data source** : `-- Mixed --`.
3. Requête A, source `Prometheus` (mode Code), légende `node-exporter` :
   ```promql
   100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[1m])))
   ```
4. **Add query** → requête B, source `InfluxDB`, format **Time series** :
   ```sql
   SELECT $__dateBin(time) AS time, avg(100 - usage_idle) AS telegraf
   FROM cpu WHERE $__timeFilter(time) GROUP BY 1 ORDER BY 1
   ```
5. **Query options** (au-dessus des requêtes) → **Min interval** : `1m`.
6. Titre `CPU de la VM : node-exporter et Telegraf`, unité `Percent (0-100)`, min `0` → **Back**, **Save**.
   Résultat attendu : deux courbes proches (écart de quelques points), légendes `node-exporter` et `telegraf`.

### Si bloqué
Tableau de bord importé par la formatrice (rattrapage, 5 s) : lecture des panels en mode **Edit**.

### Critères de réussite
- [ ] Un panel, deux sources, deux courbes
- [ ] Unité `%` commune

---

## Lab 11.2 ⭐ — Calculer l'écart entre les deux collecteurs (guidé)
**Durée** : 10 min · **Objectif** : une seule courbe = node-exporter − Telegraf
**Contexte** : un écart durable de plus de 5 points signalerait un problème de collecte.
**Prérequis** : Lab 11.1

### Étapes
1. Menu du panel → **More...** → **Duplicate** ; titre `Écart entre les deux collecteurs`.
2. Onglet **Transformations** → **Add transformation** → **Join by field** : **Mode** `OUTER (TIME SERIES)` ; laisser le champ de jointure vide (temps de chaque série).
3. **Add another transformation** → **Add field from calculation** : **Mode** `Binary operation`, `node-exporter` `-` `telegraf`, **Alias** `Ecart`, **Replace all fields** activé.
4. **Table view** (en haut de l'éditeur) : vérifier les colonnes `Time` et `Ecart`.
   Résultat attendu : courbe autour de 0 à 5 %, pics ponctuels.
5. **Back**, **Save**.

### Critères de réussite
- [ ] Courbe unique `Ecart`
- [ ] Explication d'au moins un pic (fenêtres de calcul différentes)

---

## Défis facultatifs (en cas d'avance)

## Défi 11.3 ⭐⭐ — Synthèse par site (semi-autonome)
**Durée** : 15 min · **Objectif** : un tableau d'une ligne par site, 6 colonnes issues de 4 requêtes
**Contexte** : le responsable *radio* veut, sur une seule ligne par site, l'état, les abonnés, le débit, le débit par abonné et la latence (ancien besoin couvert par Boom Table).

**Énoncé** : panel Table `Synthèse par site` (source `Prometheus`) avec 4 requêtes en **Instant** / **Format Table** :
abonnés par site et région, débit descendant par site, latence au 95e centile par site, état par site.
Résultat : colonnes `Site`, `Région`, `État` (mapping coloré), `Abonnés`, `Débit descendant` (b/s), `Débit par abonné` (b/s), `Latence p95` (s, rouge au-dessus de 100 ms), trié par abonnés décroissants.

**Indices** :
- Fusion des 4 résultats : **Merge series/tables** (colonnes `Value #A` à `Value #D`)
- Débit par abonné : **Add field from calculation**, `Value #B` / `Value #A`
- Unités et seuils par colonne : overrides **Fields with name**
- Requêtes : exercices 03.3 et 03.4

**Critères de réussite** :
- [ ] 12 lignes, 7 colonnes nommées
- [ ] Tri par abonnés décroissants ; latence colorée

---

## Défi 11.4 ⭐⭐⭐ — Totaux par région (autonome)
**Durée** : 5 min · **Objectif** : agréger la synthèse par site en synthèse par région, sans nouvelle requête
**Contexte** : la direction veut 4 lignes, pas 12.

**Énoncé** : dupliquer le tableau de l'exercice 11.3 et obtenir, par région : somme des abonnés, somme du débit descendant, latence p95 maximale ; uniquement par transformations.

**Critères de réussite** :
- [ ] 4 lignes (une par région)
- [ ] Aucune requête modifiée
