# Module 04 — Exercices

## Lab 04.1 ⭐ — Créer le tableau de bord du NOC (guidé)
**Durée** : 15 min · **Objectif** : créer « [TLC] Réseau — Vue nationale » dans le dossier « NOC Telcéa », avec un premier panel
**Contexte** : le NOC de Telcéa remplace ses indicateurs dispersés par un écran unique.
**Prérequis** : M03 (source `Prometheus` par défaut)

### Étapes
1. Menu **Dashboards → New → New folder** : nom `NOC Telcéa` → **Create**.
2. Dans le dossier, **New → New dashboard**.
3. Sous **Select layout**, choisir **Custom grid**.
4. Panneau **Add** (à droite) : cliquer sur la vignette **Panel**, puis **Configure visualization** dans le panel créé.
5. Requête (mode **Code**) :
   ```promql
   sum by (region) (telcea_cell_users)
   ```
   **Options** de la requête → **Legend** : **Custom**, saisir `{{region}}`.
   Résultat attendu : 4 courbes nommées `Bretagne`, `Hauts-de-France`, `Ile-de-France`, `Provence`.
6. Options à droite : **Title** = `Abonnés par région`. Cliquer sur **Back** (en haut à droite).
7. **Save** : **Title** = `[TLC] Réseau — Vue nationale`, **Folder** = `NOC Telcéa` → **Save**.
8. Icône d'engrenage (barre latérale droite, mode édition) → **Settings**, onglet **General** :
   - **Description** : `Supervision nationale du réseau radio et transport de Telcéa (NOC).`
   - **Tags** : `telcea`, `reseau`, `noc` (touche Entrée après chaque tag)
   Puis **Save** (message : `Description et tags`).
9. Barre du haut : plage `Last 6 hours`, rafraîchissement `30s` (liste à droite de **Refresh**), **Save**, **Exit edit**.

### Critères de réussite
- [ ] Tableau de bord visible dans **Dashboards → NOC Telcéa**, 3 tags affichés
- [ ] Rechargement de la page (`F5`) : plage `Last 6 hours` et rafraîchissement `30s` conservés

---

## Lab 04.2 ⭐ — Organiser en lignes et ajouter 4 panels (guidé)
**Durée** : 20 min · **Objectif** : obtenir 3 lignes (Synthèse, Radio, Transport) et 5 panels
**Contexte** : l'équipe *radio* et l'équipe *transport* consultent le même écran, chacune sa ligne.
**Prérequis** : Lab 04.1

### Étapes
1. **Edit** → panneau **Add** → **Add row** trois fois. Renommer les lignes (clic sur le titre de la ligne, champ **Title** à droite) : `Synthèse`, `Radio`, `Transport`.
2. Glisser le panel `Abonnés par région` dans la ligne `Radio` (poignée du titre du panel).
3. Ajouter dans `Synthèse` un panel **Stat** :
   - Requête : `sum(telcea_site_up)` ; **Options** → **Type** : `Instant`
   - Visualisation : bouton **Change** (en haut des options) → **Stat**
   - **Title** : `Sites en service`
   Résultat attendu : grand chiffre `12`.
4. Ajouter dans `Radio` un panel **Time series** `Débit descendant par région` :
   ```promql
   sum by (region) (rate(telcea_cell_traffic_bytes_total{direction="down"}[5m])) * 8
   ```
   Légende `{{region}}`.
5. Ajouter dans `Transport` un panel **Time series** `Utilisation des liens de collecte` :
   ```promql
   sum by (link) (rate(telcea_link_bytes_total[5m])) * 8 / sum by (link) (telcea_link_capacity_bits_per_second)
   ```
   Légende `{{link}}`. Résultat attendu : 3 courbes entre 0,2 et 0,5 en journée.
6. Ajuster tailles et positions (coin inférieur droit des panels), puis **Save** et **Exit edit**.
7. Replier la ligne `Transport` (clic sur son titre) puis la déplier.

### Critères de réussite
- [ ] 3 lignes dans l'ordre Synthèse, Radio, Transport
- [ ] 4 panels affichant des données (`12` pour le Stat)
- [ ] Unités brutes à ce stade (octets, ratios) : réglées au M05

---

## Exercice 04.3 ⭐⭐ — Choisir les widgets du NOC (semi-autonome)
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
