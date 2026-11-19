# Module 04 — Corrections

État final de référence (Labs 04.1, 04.2 et défis 04.2b, 04.3) : `scripts/m04/catch-up/tableau-de-bord.json` (uid `tlc-reseau-national`, dossier `NOC Telcéa`).

## Lab 04.1 ⭐ — Créer le tableau de bord du NOC
### Solution
Étapes de l'énoncé. Contrôle par l'API (terminal du bureau, facultatif) :
```bash
cd ~/grafana-training/stack
curl -s -u "admin:$(grep ^GRAFANA_ADMIN_PASSWORD .env | cut -d= -f2)" \
  "http://localhost:3000/grafana/api/search?query=Vue%20nationale" | jq -c '.[] | {title, folderTitle}'
```
Sortie attendue :
```
{"title":"[TLC] Réseau — Vue nationale","folderTitle":"NOC Telcéa"}
```

### Pourquoi
- Dossier créé AVANT le tableau de bord : droits futurs (M10) posés au niveau du dossier.
- **Custom grid** : position et taille des panels libres (disposition d'un écran de NOC).
- Mode **Code** : requête collée telle quelle (le **Builder** reconstruit la requête champ par champ).

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Tableau de bord dans **Dashboards** (racine) | Dossier non choisi à l'enregistrement | Settings → **Folder** → `NOC Telcéa` → **Save** |
| Panel vide, `No data` | Source autre que `prometheus`, ou texte collé en mode **Builder** | Source `prometheus` ; **Code** avant de coller |
| Requête non exécutée | Curseur resté dans la zone de requête | Cliquer en dehors de la zone |
| Modifications perdues | Page quittée sans **Save** | Refaire, puis **Save** |

## Lab 04.2 ⭐ — Ajouter 3 panels
### Solution
| Panel | Visualisation | Requête |
|---|---|---|
| Abonnés par région (Lab 04.1) | Time series | `sum by (region) (telcea_cell_users)` |
| Sites en service | Stat | `sum(telcea_site_up)` |
| Débit descendant par région | Time series | `sum by (region) (rate(telcea_cell_traffic_bytes_total{direction="down"}[5m])) * 8` |
| Utilisation des liens de collecte | Time series | `sum by (link) (rate(telcea_link_bytes_total[5m])) * 8 / sum by (link) (telcea_link_capacity_bits_per_second)` |

### Pourquoi
- Stat : une valeur clé, lisible de loin (dernière valeur par défaut).
- Débit : `rate()` sur le compteur d'octets, `* 8` → bits/s (unité réglée au M05).
- Utilisation : ratio débit / capacité, `sum by (link)` des deux côtés → mêmes étiquettes, division possible.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Stat affiche une moyenne décimale (ex. `11.9`) | Calcul **Mean** au lieu de **Last** | **Value options → Calculation** : `Last *` (ou M05) |
| Graphique au lieu du grand chiffre | Visualisation non changée | **Change** → **Stat** |
| Panel des liens vide | Requête tronquée au collage | Recopier la requête entière |
| Panels perdus | **Exit edit** sans **Save** | **Save** avant **Exit edit** |

## Défis facultatifs

## Défi 04.2b ⭐⭐ — Finitions : légendes, lignes, réglages
### Solution
1. Chaque panel par région : **Options** de la requête → **Legend** → **Custom** → `{{region}}` ; panel des liens : `{{link}}`.
2. Panneau **Add** → **Add row** (×3), titres `Synthèse`, `Radio`, `Transport` ; glisser `Sites en service` sous Synthèse, abonnés et débit sous Radio, liens sous Transport.
3. **Settings** : description, tags `telcea`, `reseau`, `noc` (Entrée après chaque tag) ; plage `Last 6 hours` et rafraîchissement `30s` choisis AVANT le dernier **Save**.

Contrôle par l'API :
```bash
curl -s -u "admin:$(grep ^GRAFANA_ADMIN_PASSWORD ~/grafana-training/stack/.env | cut -d= -f2)" \
  "http://localhost:3000/grafana/api/search?tag=telcea" | jq -c '.[] | {title, folderTitle, tags}'
```
Sortie attendue :
```
{"title":"[TLC] Réseau — Vue nationale","folderTitle":"NOC Telcéa","tags":["noc","reseau","telcea"]}
```

### Pourquoi
- Légende `{{region}}` : nom lisible au lieu de `{region="Bretagne"}`.
- Lignes par équipe : chaque équipe replie ce qui ne la concerne pas (panels d'une ligne repliée non interrogés).
- Tags : base de la liste de tableaux de bord (Défi 04.3) et de la recherche.
- Plage et rafraîchissement enregistrés : écran mural identique après chaque rechargement.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Légende `{region="Bretagne"}` | **Legend** laissé en **Auto** | **Custom** + `{{region}}` |
| Tags absents après rechargement | Tags saisis sans touche Entrée, ou non enregistrés | Entrée après chaque tag, puis **Save** |
| Rafraîchissement revenu à `Off` | Choisi après le dernier **Save** | **Save** de nouveau |
| Panel hors de la ligne voulue | Glissé sous la ligne au lieu de dedans | Déposer sous le titre de la ligne, ligne dépliée |

## Défi 04.3 ⭐⭐ — Choisir les widgets du NOC
### Solution
| Besoin | Visualisation | Réglages clés |
|---|---|---|
| Consignes d'astreinte | **Text** | **Mode** : Markdown ; contenu ci-dessous |
| État de chaque site | **Table** | Requête `telcea_site_up`, **Type** `Instant`, **Format** `Table` |
| Accès aux autres tableaux de bord | **Dashboard list** | **Search** activé, **Tags** : `telcea` |

Contenu Markdown du panel texte :
```markdown
**Astreinte radio** : poste 1001

**Astreinte transport** : poste 1002

Procédure incident : signaler toute coupure de site dans les 15 min.
```
Tableau obtenu : 12 lignes, colonnes `Time`, `__name__`, `instance`, `job`, `region`, `site`, `techno`, `Value` (nettoyage des colonnes au M05).

### Pourquoi
- Text : consignes visibles sans quitter l'écran (mise à jour par simple édition).
- Table en **Instant** : une ligne par série, valeur actuelle.
- Dashboard list : navigation entre écrans sans menu.

### Variantes acceptables
- **Status history** ou **State timeline** pour l'état des sites : valides, mais montrent l'historique plutôt que l'état actuel.
- **Dashboard list** avec **Starred** au lieu des tags : dépend de chaque utilisateur (moins adapté à un écran partagé).

## Défi 04.4 ⭐⭐⭐ — Onglets et règle d'affichage
### Solution
1. **Save** (flèche à droite du bouton) → **Save as copy**, titre `[TLC] Réseau — Vue nationale (TEST onglets)`.
2. Mode édition → **Group panels** → regroupement en onglets ; renommer `Vue nationale` et `Transport` ; déplacer les lignes Synthèse et Radio dans le premier onglet.
3. Panel d'utilisation des liens : requête
   ```promql
   (sum by (link) (rate(telcea_link_bytes_total[5m])) * 8 / sum by (link) (telcea_link_capacity_bits_per_second)) > 0.8
   ```
4. Options du panel → **Show / hide rules** → **Panel visibility** : **Show** + **Add rule** → règle sur le résultat de requête (afficher si des données sont présentes).

### Pourquoi
- Comparaison `> 0.8` en PromQL : ne conserve que les séries au-dessus du seuil (vide hors incident).
- Copie marquée `TEST` : aucune modification de l'écran de référence du NOC.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Panel toujours visible | Règle sur une variable au lieu du résultat de requête | Type de règle : résultat de requête (*query result*) |
| Panel vide mais visible | Règle non enregistrée | **Save** |

## QCM — Réponses
1. **D** — Préfixe d'entité, domaine, tiret cadratin, vue.
2. **C** — Settings → General : titre, description, tags, dossier.
3. **A** — Panels d'une ligne repliée non interrogés : charge réduite sur les sources.
4. **B** — Stat : une valeur clé, lisible de loin.
5. **A** — State timeline : changements d'état dans le temps.
6. **D** — Custom grid : position et taille libres ; Auto grid : tailles uniformes automatiques.
