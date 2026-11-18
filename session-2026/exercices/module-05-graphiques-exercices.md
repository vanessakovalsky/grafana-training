# Module 05 — Exercices

Point de départ : tableau de bord « [TLC] Réseau — Vue nationale » de fin de M04 (rattrapage possible, voir le guide formateur).

## Lab 05.1 ⭐ — Unités, calculs et seuils (guidé)
**Durée** : 20 min · **Objectif** : rendre lisibles les 4 panels existants (unités, couleurs d'état)
**Contexte** : sur l'écran mural du NOC, `776475341` ne veut rien dire ; `776 Mb/s` si.
**Prérequis** : Lab 04.2

### Étapes
1. **Edit**, puis survoler le panel `Sites en service` → **Edit** (menu du panel, ou touche `e`).
2. Options à droite (champ de recherche en haut des options) :
   - **Value options → Calculation** : `Last *`
   - **Stat styles → Color mode** : `Background Solid` ; **Graph mode** : `None`
   - **Thresholds** : base `Red`, `+ Add threshold` → `10` en `Orange`, `+ Add threshold` → `12` en `Green`
   Résultat attendu : `12` sur fond vert. **Back**.
3. Panel `Débit descendant par région` : **Standard options → Unit** → `Data rate / bits/sec(SI)`.
   Résultat attendu : axe en `Mb/s` (ex. `800 Mb/s`).
4. Panel `Abonnés par région` : **Unit** → `Misc / None`.
5. Panel `Utilisation des liens de collecte` :
   - **Unit** : `Misc / Percent (0.0-1.0)` ; **Min** : `0` ; **Max** : `1`
   - **Thresholds** : base `Green`, `0.8` `Orange`, `0.9` `Red`
   - **Thresholds → Show thresholds** : `As lines (dashed)`
   Résultat attendu : axe de 0 % à 100 %, lignes pointillées à 80 % et 90 %.
6. **Save** (message : `Unités et seuils`), **Exit edit**.

### Critères de réussite
- [ ] `12` sur fond vert
- [ ] Débit en `Mb/s`, liens en `%` avec 2 lignes pointillées

---

## Lab 05.2 ⭐ — Un tableau d'état lisible (guidé)
**Durée** : 15 min · **Objectif** : réduire le tableau `État des sites` à 4 colonnes, état en clair et en couleur
**Contexte** : le technicien d'astreinte doit voir d'un coup d'œil quel site est hors service.
**Prérequis** : exercice 04.3 (tableau `État des sites`)

### Étapes
1. Éditer le panel `État des sites`. Vérifier la requête : `telcea_site_up`, **Options** → **Type** `Instant`, **Format** `Table`.
2. Onglet **Transformations** → **Add transformation** → **Organize fields by name** :
   - masquer (icône œil) `Time`, `__name__`, `instance`, `job`
   - renommer `site` → `Site`, `region` → `Région`, `techno` → `Techno`, `Value` → `État`
   - ordre : Site, Région, Techno, État (glisser-déposer)
3. Options → **Value mappings** → **Add value mappings** :
   - **Value** `1` → texte `En service`, couleur verte
   - **Value** `0` → texte `Hors service`, couleur rouge
   → **Update**.
4. **+ Add field override** → **Fields with name** → `État` → **Add override property** → **Cell options > Cell type** → `Colored background`.
5. Si la colonne `État` est masquée (défilement) : **Standard options** non concernées → **Table → Column width** : `100`.
6. **Back**, **Save** (message : `Tableau des sites`).

### Critères de réussite
- [ ] 4 colonnes : Site, Région, Techno, État
- [ ] 12 cellules `En service` sur fond vert

---

## Exercice 05.3 ⭐⭐ — Carte, disponibilité, jauges (semi-autonome)
**Durée** : 25 min · **Objectif** : ajouter 2 lignes et 5 panels aux visualisations adaptées
**Contexte** : le responsable du NOC veut voir OÙ sont les sites, DEPUIS QUAND ils sont en service, et l'état de la VM de supervision.

**Énoncé** :
1. Nouvelle ligne `Carte` (entre Synthèse et Radio) :
   - Geomap `Carte des sites` : un marqueur par site, vert en service, rouge hors service, nom du site affiché.
   - State timeline `Disponibilité des sites` : une bande par site, `En service` / `Hors service`.
2. Ligne `Radio` : Bar gauge horizontal `Réussite des appels (5 min)` par région, échelle de 95 % à 100 %, rouge sous 98 %, orange sous 99 %.
3. Nouvelle ligne `Système de la VM` : deux Gauge, `CPU de la VM` et `Mémoire utilisée de la VM` (0 à 100 %, orange à 65, rouge à 90).

**Indices** :
- Carte : requête de la slide « Coordonnées pour la Geomap » (Instant, Format Table) + transformation **Convert field type** (`latitude`, `longitude` → `Number`) ; couche **Markers**, **Location** `Coords` ; **Color** : champ `Value` ; **Text label** : champ `site`
- Réussite des appels : `1 - sum by (region) (rate(telcea_call_failures_total[5m])) / sum by (region) (rate(telcea_call_attempts_total[5m]))`
- CPU : requête de l'exercice 03.3 (question 6) ; mémoire : `node_memory_MemAvailable_bytes` et `node_memory_MemTotal_bytes`
- Même value mapping que le tableau d'état pour la State timeline et la carte

**Critères de réussite** :
- [ ] 12 marqueurs verts, positionnés sur la France (Brest à l'ouest, Dunkerque au nord, Toulon au sud)
- [ ] 12 bandes vertes dans la frise de disponibilité
- [ ] Bar gauge en `%` avec 2 décimales, 2 jauges en `%`

---

## Défi 05.4 ⭐⭐⭐ — Trafic réseau de la VM en miroir (autonome)
**Durée** : 15 min · **Objectif** : maîtriser les overrides sur plusieurs requêtes d'un même panel
**Contexte** : exigence reprise de l'ancien tableau de bord d'exploitation : réception au-dessus de l'axe, émission en dessous.

**Énoncé** : dans la ligne `Système de la VM`, créer le panel Time series `Trafic réseau de la VM` :
- deux requêtes (réception, émission) en bits/s, toutes interfaces sauf `lo`, légendes `RECEIVE` et `TRANSMIT` ;
- `RECEIVE` en bleu, `TRANSMIT` en orange et SOUS l'axe ;
- bonus : sur `Utilisation des liens de collecte`, colorer `REN-PAR` (lien breton) en violet.

Contraintes : aucune modification de la requête pour obtenir l'affichage négatif.

**Critères de réussite** :
- [ ] Deux courbes de part et d'autre de 0, unité `b/s`
- [ ] Overrides visibles dans les options du panel (2 ou 3)
