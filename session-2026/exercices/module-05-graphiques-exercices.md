# Module 05 — Exercices

Parcours essentiel = Labs 05.1 et 05.2 (tout le groupe). Défis = facultatifs, en cas d'avance.
Point de départ : tableau de bord « [TLC] Réseau — Vue nationale » du M04 (sinon rattrapage par la formatrice, 5 s).
Astuce : champ de recherche en haut des options du panel (taper `unit`, `thresholds`…).

## Lab 05.1 ⭐ — Unités et couleurs (guidé)
**Durée** : 15 min · **Objectif** : rendre lisibles 3 panels (unités, couleurs d'état)
**Contexte** : sur l'écran mural du NOC, `776475341` ne veut rien dire ; `776 Mb/s` si.
**Prérequis** : Lab 04.2

### Étapes
1. Bouton **Edit** (en haut à droite), puis survoler le panel `Sites en service` → menu du panel (⋮) → **Edit**.
2. Options à droite, rubrique **Thresholds** :
   - seuil de base (`Base`) : couleur `Red`
   - remplacer la valeur `80` par `12`, couleur `Green`
   Résultat attendu : `12` en vert. Bouton **Back**.
3. Panel `Débit descendant par région` → **Edit** → **Standard options → Unit** : taper `bits/sec`, choisir `bits/sec(SI)`.
   Résultat attendu : axe en `Mb/s`. **Back**.
4. Panel `Utilisation des liens de collecte` → **Edit** → **Unit** : taper `percent`, choisir `Percent (0.0-1.0)`.
   Résultat attendu : axe en `%`. **Back**.
5. **Save** → **Exit edit**.

### Critères de réussite
- [ ] `12` en vert ; débit en `Mb/s` ; liens en `%`

---

## Lab 05.2 ⭐ — Un tableau d'état des sites (guidé)
**Durée** : 15 min · **Objectif** : un tableau d'une ligne par site, état en clair et en couleur
**Contexte** : le technicien d'astreinte doit voir d'un coup d'œil quel site est hors service.
**Prérequis** : Lab 05.1

### Étapes
1. **Edit** → panneau **Add** → **Panel** → **Configure visualization** → **Code**, copier-coller :
   ```promql
   telcea_site_up
   ```
   Sous la requête, **Options** : **Type** `Instant`, **Format** `Table`.
2. Visualisation : bouton **Change** → **Table**. **Title** : `État des sites`.
   Résultat attendu : 12 lignes, une par site.
3. Onglet **Transformations** (sous le panel) → **Add transformation** → **Organize fields by name** : masquer (icône œil) `Time`, `__name__`, `instance`, `job`.
4. Options à droite → **Value mappings** → **Add value mappings** :
   - **Value** `1` → **Display text** `En service`, couleur verte
   - **Value** `0` → **Display text** `Hors service`, couleur rouge
   → **Update**.
   Résultat attendu : colonne `Value` affichant `En service` en vert.
5. **Back** → **Save** → **Exit edit**.

Panel `État des sites` déjà présent (rattrapage) → reprise à l'étape 3, en éditant ce panel.

### Critères de réussite
- [ ] 12 lignes `En service`, sans les colonnes `Time`, `__name__`, `instance`, `job`

---

## Défis facultatifs (en cas d'avance)

## Défi 05.2b ⭐⭐ — Finitions des panels
**Durée** : 10 min · **Objectif** : pousser le réglage des panels existants
**Énoncé** :
1. `Sites en service` : fond plein coloré, sans mini-graphique ; seuil orange à `10`.
2. `Utilisation des liens de collecte` : axe de 0 % à 100 %, seuils orange à 80 %, rouge à 90 %, affichés en lignes pointillées.
3. `État des sites` : colonnes renommées et ordonnées `Site`, `Région`, `Techno`, `État` ; cellule `État` en fond coloré.

**Indices** :
- **Stat styles → Color mode** / **Graph mode** ; **Thresholds → Show thresholds**
- **Organize fields by name** : renommage et glisser-déposer
- **+ Add field override → Fields with name** → **Cell options > Cell type** → `Colored background`

**Critères de réussite** :
- [ ] `12` sur fond vert ; lignes pointillées à 80 % et 90 % ; 4 colonnes nommées

---

## Défi 05.3 ⭐⭐ — Carte, disponibilité, jauges (semi-autonome)
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
