# Module 04 — Exercices

Parcours essentiel = Labs 04.1 et 04.2 (tout le groupe). Défis = facultatifs, en cas d'avance.
Toutes les requêtes sont fournies : copier-coller, sans retaper.

## Lab 04.1 ⭐ — Créer le tableau de bord du NOC (guidé)
**Durée** : 15 min · **Objectif** : créer « [TLC] Réseau — Vue nationale » dans le dossier « NOC Telcéa », avec un premier panel
**Contexte** : le NOC de Telcéa remplace ses indicateurs dispersés par un écran unique.
**Prérequis** : source `Prometheus` (M03)

### Étapes
1. Menu ☰ → **Dashboards** → bouton **New** → **New folder** : nom `NOC Telcéa` → **Create**.
2. Dans le dossier : **New** → **New dashboard**.
3. Sous **Select layout**, choisir **Custom grid**.
4. Panneau **Add** (à droite) : cliquer sur **Panel**, puis sur **Configure visualization** dans le panel créé.
5. À droite de la zone de requête : **Code**, puis copier-coller :
   ```promql
   sum by (region) (telcea_cell_users)
   ```
   Cliquer en dehors de la zone de requête. Résultat attendu : 4 courbes.
6. Options à droite, champ **Title** : `Abonnés par région`. Bouton **Back** (en haut à droite).
7. Bouton **Save** (en haut à droite) : **Title** `[TLC] Réseau — Vue nationale`, **Folder** `NOC Telcéa` → **Save**.

### Si bloqué
Tableau de bord importé par la formatrice (rattrapage, 5 s) : **Dashboards → NOC Telcéa**.

### Critères de réussite
- [ ] Tableau de bord visible dans **Dashboards → NOC Telcéa**, avec 4 courbes

---

## Lab 04.2 ⭐ — Ajouter 3 panels (guidé)
**Durée** : 20 min · **Objectif** : compléter le tableau de bord avec un chiffre clé et deux graphiques
**Contexte** : l'équipe *radio* et l'équipe *transport* consultent le même écran.
**Prérequis** : Lab 04.1

Méthode, identique pour chaque panel : bouton **Edit** (si besoin) → panneau **Add** → **Panel** → **Configure visualization** → **Code** → copier-coller la requête → **Title** → **Back**.

### Étapes
1. Panel `Sites en service` :
   ```promql
   sum(telcea_site_up)
   ```
   Visualisation : bouton **Change** (en haut des options, à droite) → **Stat**.
   Résultat attendu : grand chiffre `12`.
2. Panel `Débit descendant par région` (Time series, visualisation par défaut) :
   ```promql
   sum by (region) (rate(telcea_cell_traffic_bytes_total{direction="down"}[5m])) * 8
   ```
3. Panel `Utilisation des liens de collecte` (Time series) :
   ```promql
   sum by (link) (rate(telcea_link_bytes_total[5m])) * 8 / sum by (link) (telcea_link_capacity_bits_per_second)
   ```
   Résultat attendu : 3 courbes entre 0,2 et 0,5 en journée.
4. Agrandir ou déplacer les panels à la souris (coin inférieur droit, titre), puis **Save** → **Exit edit**.

Unités brutes à ce stade (grands nombres, ratios) : réglées au M05.

### Critères de réussite
- [ ] 4 panels avec des données, dont le chiffre `12`

---

## Défis facultatifs (en cas d'avance)

## Défi 04.2b ⭐⭐ — Finitions : légendes, lignes, réglages
**Durée** : 15 min · **Objectif** : rendre le tableau de bord lisible et organisé
**Contexte** : l'écran est partagé par les équipes *radio* et *transport*.

**Énoncé** :
1. Légendes lisibles : `Bretagne` au lieu de `{region="Bretagne"}` sur les panels par région, nom du lien sur le panel des liens.
2. Trois lignes (rows) dans l'ordre `Synthèse` (Stat), `Radio` (abonnés, débit), `Transport` (liens).
3. Réglages du tableau de bord : description, tags `telcea`, `reseau`, `noc` ; plage `Last 6 hours` et rafraîchissement `30s` conservés après `F5`.

**Indices** :
- Légende : **Options** de la requête → **Legend** → **Custom** → `{{region}}` ou `{{link}}`
- Lignes : panneau **Add** → **Add row**, puis glisser les panels par leur titre
- Réglages : engrenage (barre latérale droite, mode édition) → **Settings**

**Critères de réussite** :
- [ ] 3 lignes, légendes sans accolades, 3 tags

---

## Défi 04.3 ⭐⭐ — Choisir les widgets du NOC (semi-autonome)
**Durée** : 15 min · **Objectif** : choisir et ajouter le widget adapté à 3 besoins exprimés par le NOC
**Contexte** : le responsable du NOC formule trois demandes pour la ligne `Synthèse`.

**Énoncé** :
1. « Les consignes d'astreinte doivent rester affichées » : astreinte radio poste 1001, astreinte transport poste 1002, coupure de site à signaler dans les 15 min.
2. « Je veux l'état de chaque site, ligne par ligne » (requête `telcea_site_up`).
3. « Je veux accéder en un clic aux autres tableaux de bord étiquetés `telcea` ».

Pour chaque besoin : choisir la visualisation, l'ajouter dans `Synthèse`, la titrer.

**Indices** :
- Texte mis en forme : visualisation acceptant le Markdown
- Une ligne par site, valeur actuelle : requête en **Instant**, **Format** `Table`
- Liste de tableaux de bord filtrée par tag : widget de la famille « Widgets »

**Critères de réussite** :
- [ ] 3 panels supplémentaires dans `Synthèse`, titrés
- [ ] Tableau des sites : 12 lignes
- [ ] Liste : au moins le tableau de bord « [TLC] Réseau — Vue nationale »

---

## Défi 04.4 ⭐⭐⭐ — Onglets et règle d'affichage (autonome)
**Durée** : 10 min · **Objectif** : exploiter les tableaux de bord dynamiques de Grafana 13
**Contexte** : sur l'écran mural du NOC, la ligne `Transport` doit disparaître tant qu'aucun lien ne dépasse 80 % d'utilisation.

**Énoncé** :
- Créer une copie du tableau de bord (**Save as copy**, titre `[TLC] Réseau — Vue nationale (TEST onglets)`).
- Dans la copie, regrouper les lignes en deux onglets : `Vue nationale` (Synthèse, Radio) et `Transport`.
- Ajouter au panel d'utilisation des liens une règle d'affichage qui le masque quand la requête ne renvoie rien, et modifier la requête pour ne renvoyer que les liens au-dessus de 0,8.

**Critères de réussite** :
- [ ] Deux onglets, un seul visible à la fois
- [ ] Panel masqué hors incident (il réapparaîtra pendant la tempête du M09)
