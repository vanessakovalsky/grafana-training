# Module 07 — Exercices

Fichiers fournis dans le dépôt de la formation (`~/grafana-training/ateliers/m07/`) : `reseau-telcea.svg` (schéma du réseau) et `flow-config.yaml` (configuration Flow).

## Lab 07.1 ⭐ — Installer quatre plugins (guidé)
**Durée** : 15 min · **Objectif** : installer Status Panel, D3 Gauge, Flow et Polystat, par l'interface puis par la ligne de commande
**Contexte** : le NOC de Telcéa prépare son écran mural ; les visualisations natives ne couvrent ni le schéma du réseau ni le statut multi-indicateurs.
**Prérequis** : session `admin`, accès Internet depuis la VM

### Étapes
1. **Administration → Plugins and data → Plugins**, **Type** : `Panels`, **State** : `All`, rechercher `status`.
   Résultat attendu : plusieurs « Status Panel » (éditeurs Vonage et Tech Ben) : noter éditeur et badge de chacun.
2. Ouvrir **Status Panel — By Vonage** → onglet **Overview** : relever **Installed Version** / **Latest Version**, **Dependencies**, **Signature** → **Install**.
   Résultat attendu : bouton **Uninstall** à la place de **Install** ; badge **Installed** dans le catalogue.
3. Même démarche pour **Polystat** (rechercher `polystat`).
4. Dans le terminal du bureau Linux, installer les deux autres plugins :
   ```bash
   cd ~/grafana-training/stack
   docker compose exec grafana grafana cli plugins install briangann-gauge-panel
   docker compose exec grafana grafana cli plugins install andrewbmchugh-flow-panel
   docker compose restart grafana
   ```
   Résultat attendu (une ligne par plugin) :
   ```
   ✔ Downloaded and extracted briangann-gauge-panel v2.2.0 zip successfully to /var/lib/grafana/plugins/briangann-gauge-panel
   ```
5. Après 20 s, recharger le catalogue, **State** : `Installed`.
   Résultat attendu : `Status Panel`, `Polystat`, `D3 Gauge`, `Flow` présents.

### Critères de réussite
- [ ] 4 plugins à l'état **Installed**
- [ ] Signature de chacun relevée (2 « Grafana », 2 « community »)

---

## Lab 07.2 ⭐ — Écran mural : Status Panel et D3 Gauge (guidé)
**Durée** : 15 min · **Objectif** : un pavé de statut pour la Bretagne et une jauge à aiguille pour le lien REN-PAR
**Contexte** : sur l'écran mural, l'état de la Bretagne (région la plus exposée aux tempêtes) doit sauter aux yeux.
**Prérequis** : Lab 07.1

### Étapes
1. **Dashboards → NOC Telcéa → New → New dashboard**, **Custom grid** ; **Save** : `[TLC] NOC — Écran mural`, tags `telcea`, `noc`.
2. Panel **Status Panel** (bouton **Change** de l'éditeur, rechercher `Status`), titre `Statut — Bretagne` :
   - requête A : `sum(telcea_site_up{region="Bretagne"})`
   - requête B : `max(telcea_link_packet_loss_ratio{region="Bretagne"})`
   - **+ Add field override → Fields returned by query** `A` → **Display name** `Sites en service` ; idem `B` → `Perte de paquets`, et **Unit** `Percent (0.0-1.0)`
   - options du champ (**Thresholds** du Status Panel) : **Number Threshold**, **Warning** `2`, **Critical** `1` pour A ; `0.01` / `0.02` pour B (override B)
   - **Aggregation** : `Last` ; **Display Alias** : `Always`
   Résultat attendu : pavé vert, lignes `Sites en service - 3` et `Perte de paquets - 0.0x%`.
3. Panel **D3 Gauge**, titre `Utilisation REN-PAR` :
   ```promql
   sum(rate(telcea_link_bytes_total{link="REN-PAR"}[5m])) * 8 / sum(telcea_link_capacity_bits_per_second{link="REN-PAR"}) * 100
   ```
   **Unit** `Percent (0-100)`, **Min** `0`, **Max** `100`.
   Résultat attendu : aiguille entre 20 et 45 en journée.
4. **Save**.

### Critères de réussite
- [ ] Pavé de statut vert avec 2 indicateurs nommés
- [ ] Jauge en %

---

## Exercice 07.3 ⭐⭐ — Le schéma du réseau avec Flow (semi-autonome)
**Durée** : 15 min · **Objectif** : animer le schéma du réseau Telcéa (liens et régions colorés selon les métriques)
**Contexte** : remplace le plugin Diagram de l'ancien écran mural.

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

## Atelier 07.4 ⭐⭐⭐ — Chasse au plugin (binômes, autonome)
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
