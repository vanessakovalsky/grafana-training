# Module 07 — Exercices

Parcours essentiel = Labs 07.1 et 07.2 (tout le groupe). Défis = facultatifs, en cas d'avance.
Toutes les requêtes sont fournies : copier-coller, sans retaper.

## Lab 07.1 ⭐ — Installer quatre plugins depuis le catalogue (guidé)
**Durée** : 15 min · **Objectif** : installer Status Panel, Polystat, D3 Gauge et Flow par l'interface
**Contexte** : le NOC de Telcéa prépare son écran mural ; les visualisations natives ne couvrent ni le schéma du réseau ni le statut multi-indicateurs.
**Prérequis** : session `admin`

### Étapes
1. **Administration → Plugins and data → Plugins**, **Type** : `Panels`, **State** : `All`.
2. Rechercher `status` → ouvrir **Status Panel — By Vonage** → **Install**.
   Résultat attendu : bouton **Uninstall** à la place de **Install**.
3. Même démarche : rechercher `polystat` → **Polystat** → **Install**.
4. Même démarche : rechercher `D3 Gauge` → **D3 Gauge** → **Install**.
5. Même démarche : rechercher `flow` → **Flow** (éditeur andrewbmchugh) → **Install**.
6. Retour au catalogue, **State** : `Installed`.
   Résultat attendu : `Status Panel`, `Polystat`, `D3 Gauge`, `Flow` présents.

### Si bloqué
Plugins installés par la formatrice (rattrapage, ~20 s, redémarrage de Grafana) : recharger la page.

### Critères de réussite
- [ ] 4 plugins à l'état **Installed**

---

## Lab 07.2 ⭐ — Écran mural : Status Panel et D3 Gauge (guidé)
**Durée** : 15 min · **Objectif** : un pavé de statut pour la Bretagne et une jauge à aiguille pour le lien REN-PAR
**Contexte** : sur l'écran mural, l'état de la Bretagne (région la plus exposée aux tempêtes) doit sauter aux yeux.
**Prérequis** : Lab 07.1

### Étapes
1. **Dashboards → NOC Telcéa → New → New dashboard**, **Custom grid**.
2. **Save** : titre `[TLC] NOC — Écran mural`, dossier `NOC Telcéa` → **Save**.
3. Panneau **Add** → **Panel** → **Configure visualization** → bouton **Change** → rechercher `Status` → **Status Panel**.
4. **Code**, copier-coller :
   ```promql
   sum(telcea_site_up{region="Bretagne"})
   ```
   **Title** : `Statut — Bretagne`.
5. Options du Status Panel : **Thresholds** → **Number Threshold**, **Warning** `2`, **Critical** `1` ; **Aggregation** : `Last`.
   Résultat attendu : pavé vert. **Back**.
6. Nouveau panel → **Change** → **D3 Gauge** ; **Code**, copier-coller :
   ```promql
   sum(rate(telcea_link_bytes_total{link="REN-PAR"}[5m])) * 8 / sum(telcea_link_capacity_bits_per_second{link="REN-PAR"}) * 100
   ```
   **Title** : `Utilisation REN-PAR` ; **Unit** `Percent (0-100)`, **Min** `0`, **Max** `100`.
   Résultat attendu : aiguille entre 20 et 45 en journée. **Back**.
7. **Save** → **Exit edit**.

### Si bloqué
Écran mural importé par la formatrice (rattrapage, utilisé au M08).

### Critères de réussite
- [ ] Pavé de statut vert
- [ ] Jauge en %

---

## Défis facultatifs (en cas d'avance)

## Défi 07.1b ⭐⭐ — Signatures et installation en ligne de commande
**Durée** : 10 min · **Objectif** : vérifier la confiance accordée à un plugin et installer sans interface
**Énoncé** :
1. Catalogue : pour chacun des 4 plugins, onglet **Overview** → relever **Signature**, **Installed Version** / **Latest Version**, **Dependencies**.
2. Plusieurs « Status Panel » existent (Vonage, Tech Ben) : comparer éditeur et badge.
3. Dans un terminal du bureau Linux, désinstaller D3 Gauge dans l'interface puis le réinstaller en ligne de commande :
   ```bash
   cd ~/grafana-training/stack
   docker compose exec grafana grafana cli plugins install briangann-gauge-panel
   docker compose restart grafana
   ```
**Critères de réussite** :
- [ ] Signature de chacun relevée (2 « Grafana », 2 « community »)
- [ ] D3 Gauge de nouveau **Installed** après le redémarrage

---

## Défi 07.2b ⭐⭐ — Second indicateur du Status Panel
**Durée** : 10 min · **Objectif** : un pavé de statut multi-indicateurs
**Énoncé** : dans `Statut — Bretagne`, ajouter la requête B `max(telcea_link_packet_loss_ratio{region="Bretagne"})` ; nommer les indicateurs `Sites en service` et `Perte de paquets` (unité `Percent (0.0-1.0)`, seuils `0.01` / `0.02`) ; **Display Alias** : `Always`.

**Indices** : **+ Add field override → Fields returned by query** → **Display name**, **Unit**, seuils du Status Panel.

**Critères de réussite** :
- [ ] Lignes `Sites en service - 3` et `Perte de paquets - 0.0x%`

---

## Défi 07.3 ⭐⭐ — Le schéma du réseau avec Flow (semi-autonome)
**Durée** : 15 min · **Objectif** : animer le schéma du réseau Telcéa (liens et régions colorés selon les métriques)
**Contexte** : remplace le plugin Diagram de l'ancien écran mural.
**Fichiers fournis** : `~/grafana-training/ateliers/m07/` (bureau Linux) ou dépôt en ligne `grafana-training` : `reseau-telcea.svg` (schéma du réseau) et `flow-config.yaml` (configuration Flow).

**Énoncé** : ajouter un panel **Flow** `Schéma du réseau Telcéa` :
- **SVG** : contenu de `reseau-telcea.svg` ; **Panel Config** : contenu de `flow-config.yaml` (copier-coller) ;
- deux requêtes : utilisation des liens par lien, sites en service par région, avec des légendes égales aux `dataRef` du YAML.

**Indices** :
- Utilisation des liens : requête de l'exercice 03.3 (question 5), légende `{{link}}`
- Sites par région : `sum by (region) (telcea_site_up)`, légende `{{region}}`
- Élément gris = `dataRef` sans série du même nom ; bouton de débogage des options du panel (journal dans la console du navigateur, `Ctrl + Maj + J`)

**Critères de réussite** :
- [ ] 3 liens verts avec leur pourcentage, 4 régions vertes
- [ ] Désactiver la requête B (icône œil) → régions grises : comprendre le rôle de `dataRef`

---

## Défi 07.4 ⭐⭐⭐ — Atelier « Chasse au plugin » (binômes, autonome)
**Durée** : 15 min (dont 5 min de restitution) · **Objectif** : choisir un plugin pour un besoin non couvert, avec une grille d'évaluation
**Contexte** : atelier repris du support historique, adapté à Grafana 13.

**Énoncé** :
1. Choisir un besoin réel de supervision (le sien) ou l'un des suivants : carte de couverture radio, frise des interventions de maintenance, diagramme de flux de facturation, suivi d'un parc d'équipements IoT.
2. Sur `grafana.com/grafana/plugins`, trouver un plugin (panel ou source) qui y répond.
3. Remplir la grille : nom et éditeur · signature (Grafana, Commercial, Community, non signé) · date de dernière mise à jour · version minimale de Grafana (compatible 13 ?) · licence · dépôt et activité des tickets · apport par rapport à une visualisation native · un point de vigilance.
4. Décision argumentée : installer, tester d'abord, ou refuser. Restitution en 1 minute.

**Critères de réussite** :
- [ ] Grille complète (8 critères)
- [ ] Décision justifiée par au moins 2 critères
