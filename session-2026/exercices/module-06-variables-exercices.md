# Module 06 — Exercices

## Lab 06.1 ⭐ — Le tableau de bord régional et sa variable Région (guidé)
**Durée** : 15 min · **Objectif** : créer « [TLC] Réseau — Détail régional » filtré par une variable `region` multi-valeur
**Contexte** : l'équipe *radio* veut le détail d'une ou plusieurs régions sans dupliquer l'écran national.
**Prérequis** : M05 (tableau de bord national, source `Prometheus`)

### Étapes
1. **Dashboards → NOC Telcéa → New → New dashboard**, mise en page **Custom grid**.
2. Engrenage (barre de droite) → **Settings** → onglet **Variables** → **New variable** :
   - **Variable type** : `Query` ; **Name** : `region` ; **Label** : `Région`
   - **Data source** : `Prometheus` ; **Query type** : `Label values` ; **Label** : `region` ; **Metric** : `telcea_site_info`
   - **Selection options** : **Multi-value** activé, **Include All value** activé
   Résultat attendu (aperçu des valeurs, bas de l'éditeur) : `Bretagne`, `Hauts-de-France`, `Ile-de-France`, `Provence`.
   → **Back to list**, **Back to dashboard**.
3. Ajouter un panel Time series `Abonnés par site` :
   ```promql
   sum by (site) (telcea_cell_users{region=~"$region"})
   ```
   Légende `{{site}}`, unité `None`.
4. **Save** : titre `[TLC] Réseau — Détail régional`, dossier `NOC Telcéa`, tags `telcea`, `reseau`, `radio`.
5. Liste **Région** en haut : choisir `Bretagne`, puis ajouter `Provence`.
   Résultat attendu : 3 courbes (REN-01, BRE-01, QUI-01), puis 6 ; URL contenant `var-region=Bretagne&var-region=Provence`.

### Critères de réussite
- [ ] Variable `region` à 4 valeurs + `All`
- [ ] Le panel suit la sélection (3 courbes pour la Bretagne seule)

---

## Lab 06.2 ⭐ — Variables chaînées, custom et interval (guidé)
**Durée** : 15 min · **Objectif** : ajouter `site` (dépend de `region`), `techno` (liste fixe) et `fenetre` (durée)
**Contexte** : le technicien veut isoler un site 4G précis et lisser plus ou moins les débits.
**Prérequis** : Lab 06.1

### Étapes
1. **New variable** `site`, label `Site` : type `Query`, **Query type** `Classic query`, requête :
   ```promql
   label_values(telcea_site_info{region=~"$region"}, site)
   ```
   Multi-value et Include All value activés.
2. **New variable** `techno`, label `Techno` : type `Custom`, valeurs `4G,5G`, Multi-value et Include All value activés.
3. **New variable** `fenetre`, label `Fenêtre de calcul` : type `Interval`, valeurs `1m,5m,15m,1h`.
4. Vérifier l'ordre de la liste : `region`, `site`, `techno`, `fenetre` (glisser si besoin).
5. Modifier `Abonnés par site` :
   ```promql
   sum by (site) (telcea_cell_users{region=~"$region", site=~"$site", techno=~"$techno"})
   ```
6. Ajouter un Time series `Débit descendant par site ($fenetre)`, unité `bits/sec(SI)` :
   ```promql
   sum by (site) (rate(telcea_cell_traffic_bytes_total{direction="down", region=~"$region", site=~"$site", techno=~"$techno"}[$fenetre])) * 8
   ```
7. **Save**. Tester : Région `Bretagne` → liste Site limitée à REN-01, BRE-01, QUI-01 ; Techno `4G` → BRE-01 et QUI-01 seulement ; Fenêtre `1h` → courbes plus lisses, titre « (1h) ».

### Critères de réussite
- [ ] Liste Site filtrée par la région
- [ ] Titre du panel de débit mis à jour avec la fenêtre choisie

---

## Exercice 06.3 ⭐⭐ — Panels répétés et frise de disponibilité (semi-autonome)
**Durée** : 15 min · **Objectif** : un Stat par région sélectionnée, et 2 panels filtrés par les variables
**Contexte** : le responsable *radio* veut voir d'un coup d'œil le nombre de sites en service de chaque région choisie.

**Énoncé** :
- En haut du tableau de bord : un Stat `Sites en service — $region` répété pour chaque région sélectionnée (4 par ligne), fond vert à 3 sites, rouge en dessous.
- Une State timeline `Disponibilité des sites` filtrée par les 3 variables (`En service` / `Hors service`).
- Un Time series `Latence au 95e centile ($fenetre)` par site, en secondes, ligne pointillée rouge à 100 ms.

**Indices** :
- **Repeat options → Repeat by variable** ; la requête du Stat ne filtre que sur `$region`
- Latence : requête du défi 03.4, regroupée `by (le, site)`, avec la fenêtre `$fenetre`
- Une requête renvoie « No data » ? Vérifier que la métrique porte bien chaque étiquette filtrée (Explore)

**Critères de réussite** :
- [ ] Région `All` → 4 Stats ; Région `Bretagne` → 1 Stat
- [ ] La latence s'affiche quelle que soit la sélection Techno

---

## Défi 06.4 ⭐⭐⭐ — Ranger, relier, restaurer (autonome)
**Durée** : 10 min · **Objectif** : organiser l'espace du NOC et éprouver la corbeille
**Contexte** : l'espace grossit ; il faut des sous-dossiers par équipe, une navigation entre écrans et une procédure en cas de suppression.

**Énoncé** :
1. Créer dans `NOC Telcéa` les sous-dossiers `Radio` et `Transport` ; déplacer `[TLC] Réseau — Détail régional` dans `Radio`.
2. Ajouter aux deux tableaux de bord un lien (Settings → **Links**) affichant en liste déroulante tous les tableaux de bord tagués `telcea`, en conservant la plage de temps.
3. Supprimer `[TLC] Réseau — Détail régional`, puis le restaurer dans `Radio`.

**Critères de réussite** :
- [ ] Arborescence `NOC Telcéa / Radio`, `NOC Telcéa / Transport`
- [ ] Menu de liens fonctionnel dans les deux sens
- [ ] Tableau de bord restauré, variables intactes
