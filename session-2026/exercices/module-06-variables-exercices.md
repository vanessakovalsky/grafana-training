# Module 06 — Exercices

Parcours essentiel = Labs 06.1 et 06.2 (tout le groupe). Défis = facultatifs, en cas d'avance.
Toutes les requêtes sont fournies : copier-coller, sans retaper.

## Lab 06.1 ⭐ — Le tableau de bord régional et sa variable Région (guidé)
**Durée** : 15 min · **Objectif** : créer « [TLC] Réseau — Détail régional » filtré par une variable `region`
**Contexte** : l'équipe *radio* veut le détail d'une ou plusieurs régions sans dupliquer l'écran national.
**Prérequis** : source `prometheus`, dossier `NOC Telcéa`

### Étapes
1. **Dashboards → NOC Telcéa → New → New dashboard**, mise en page **Custom grid**.
2. Engrenage (barre de droite) → **Settings** → onglet **Variables** → **New variable**.
3. Renseigner :
   - **Variable type** : `Query` ; **Name** : `region` ; **Label** : `Région`
   - **Data source** : `prometheus` ; **Query type** : `Label values` ; **Label** : `region` ; **Metric** : `telcea_site_info`
   - **Selection options** : **Multi-value** activé, **Include All value** activé
   Résultat attendu (aperçu, bas de l'éditeur) : `Bretagne`, `Hauts-de-France`, `Ile-de-France`, `Provence`.
4. **Back to list** → **Back to dashboard**.
5. Panneau **Add** → **Panel** → **Configure visualization** → **Code**, copier-coller :
   ```promql
   sum by (site) (telcea_cell_users{region=~"$region"})
   ```
   **Title** : `Abonnés par site` → **Back**.
6. **Save** : titre `[TLC] Réseau — Détail régional`, dossier `NOC Telcéa` → **Save** → **Exit edit**.
7. Liste **Région** (en haut) : choisir `Bretagne`.
   Résultat attendu : 3 courbes (REN-01, BRE-01, QUI-01).

### Si bloqué
Tableau de bord importé par la formatrice (rattrapage, 5 s) : **Dashboards → NOC Telcéa**.

### Critères de réussite
- [ ] Variable `region` à 4 valeurs + `All`
- [ ] 3 courbes pour la Bretagne seule

---

## Lab 06.2 ⭐ — Une variable Site qui dépend de la région (guidé)
**Durée** : 10 min · **Objectif** : ajouter la variable `site`, limitée aux sites de la région choisie
**Contexte** : le technicien veut isoler un site précis.
**Prérequis** : Lab 06.1

### Étapes
1. **Edit** → engrenage → **Settings** → **Variables** → **New variable** :
   - **Variable type** : `Query` ; **Name** : `site` ; **Label** : `Site`
   - **Data source** : `prometheus` ; **Query type** : `Classic query`, requête :
   ```promql
   label_values(telcea_site_info{region=~"$region"}, site)
   ```
   - **Multi-value** et **Include All value** activés
2. **Back to list** → **Back to dashboard**.
3. Panel `Abonnés par site` → **Edit** → remplacer la requête par :
   ```promql
   sum by (site) (telcea_cell_users{region=~"$region", site=~"$site"})
   ```
   **Back** → **Save** → **Exit edit**.
4. Tester : Région `Bretagne` → liste **Site** limitée à REN-01, BRE-01, QUI-01 ; Site `BRE-01` → 1 courbe.

### Critères de réussite
- [ ] Liste Site filtrée par la région
- [ ] Le panel suit la sélection du site

---

## Défis facultatifs (en cas d'avance)

## Défi 06.2b ⭐⭐ — Variables Techno et Fenêtre de calcul
**Durée** : 15 min · **Objectif** : ajouter une liste fixe et une variable de durée
**Contexte** : le technicien veut filtrer par technologie et lisser plus ou moins les débits.

**Énoncé** :
1. Variable `techno` (label `Techno`) : type `Custom`, valeurs `4G,5G`, multi-valeur, `All`.
2. Variable `fenetre` (label `Fenêtre de calcul`) : type `Interval`, valeurs `1m,5m,15m,1h`.
3. Ordre des variables : `region`, `site`, `techno`, `fenetre`.
4. `Abonnés par site` filtré aussi par `techno` ; nouveau panel `Débit descendant par site ($fenetre)`, unité `bits/sec(SI)` :
   ```promql
   sum by (site) (rate(telcea_cell_traffic_bytes_total{direction="down", region=~"$region", site=~"$site", techno=~"$techno"}[$fenetre])) * 8
   ```
5. Tags du tableau de bord : `telcea`, `reseau`, `radio`.

**Critères de réussite** :
- [ ] Techno `4G` en Bretagne → BRE-01 et QUI-01 seulement
- [ ] Fenêtre `1h` → courbes plus lisses, titre « (1h) »

---

## Défi 06.3 ⭐⭐ — Panels répétés et frise de disponibilité (semi-autonome)
**Durée** : 15 min · **Objectif** : un Stat par région sélectionnée, et 2 panels filtrés par les variables
**Prérequis** : défi 06.2b (variables `techno` et `fenetre`)
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
