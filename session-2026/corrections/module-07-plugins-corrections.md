# Module 07 — Corrections

État final de référence : `scripts/m07/catch-up/ecran-mural.json` (uid `tlc-noc-mural`) ; schéma et configuration Flow : `ateliers/m07/reseau-telcea.svg`, `ateliers/m07/flow-config.yaml`.

## Lab 07.1 ⭐ — Installer quatre plugins depuis le catalogue
### Solution
Étapes de l'énoncé : **Administration → Plugins and data → Plugins**, recherche, **Install** (×4), puis **State** `Installed`.

Relevé au banc (18/11/2026, API `GET /api/plugins/<ID>/settings`) :

| Plugin | ID | Version |
|---|---|---|
| Status Panel | `vonage-status-panel` | 2.0.4 |
| Polystat | `grafana-polystat-panel` | 2.1.16 |
| D3 Gauge | `briangann-gauge-panel` | 2.2.0 |
| Flow | `andrewbmchugh-flow-panel` | 1.20.1 |

### Pourquoi
- Installation par l'interface : plugin téléchargé depuis le catalogue grafana.com, disponible sans redémarrage.
- Volume `grafana_data` : les plugins survivent à la recréation du conteneur.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Plugin introuvable | Filtre **Type** ou **State** trop restrictif | **Type** `Panels`, **State** `All` |
| Mauvais « Status Panel » installé | Plusieurs plugins du même nom (Vonage, Tech Ben) | **Status Panel — By Vonage** |
| Bouton **Install** absent | Utilisateur non administrateur du serveur | Session `admin` |
| Installation en échec | Accès à `grafana.com` bloqué | Signaler à la formatrice (rattrapage) |

## Lab 07.2 ⭐ — Écran mural : Status Panel et D3 Gauge
### Solution
Status Panel `Statut — Bretagne` (extrait du modèle JSON) :
```json
"fieldConfig": {"defaults": {"custom": {"aggregation": "last",
  "thresholds": {"valueHandler": "Number Threshold", "warn": "2", "crit": "1"}}}}
```
D3 Gauge `Utilisation REN-PAR` : requête de l'énoncé, unité `percent`, min `0`, max `100`.

Affichage relevé au banc : pavé vert (3 sites), jauge REN-PAR à 31,8 %.

### Pourquoi
- `Critical` (1) < `Warning` (2) : le plugin en déduit que les GRANDES valeurs sont bonnes (sites en service).
- Jauge en `Percent (0-100)` : la requête multiplie déjà le ratio par 100.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| `A - Invalid Number` | Agrégation absente ou invalide | **Aggregation** : `Last` |
| Pavé vert pendant une panne | Seuils par défaut (warn 70, crit 90) conservés | **Warning** `2`, **Critical** `1` |
| Status Panel absent de **Change** | Lab 07.1 non terminé, ou page non rechargée | Recharger la page |
| Aiguille bloquée en butée | **Max** laissé à la valeur par défaut, ou unité `Percent (0.0-1.0)` | **Max** `100`, unité `Percent (0-100)` |

## Défis facultatifs

## Défi 07.1b ⭐⭐ — Signatures et installation en ligne de commande
### Solution
| Plugin | Signature | Éditeur signataire |
|---|---|---|
| Status Panel | grafana | Grafana Labs |
| Polystat | grafana | Grafana Labs |
| D3 Gauge | community | Brian Gann |
| Flow | community | andrewbmchugh |

Contrôle en ligne de commande, après réinstallation et redémarrage :
```bash
docker compose exec grafana grafana cli plugins ls
```
Sortie (extrait) :
```
installed plugins:
grafana-polystat-panel @ 2.1.16
briangann-gauge-panel @ 2.2.0
andrewbmchugh-flow-panel @ 1.20.1
```

### Pourquoi
- Signature `grafana` : plugin vérifié par Grafana Labs ; `community` : signé par l'éditeur, non audité.
- Par la CLI : fichier déposé dans `/var/lib/grafana/plugins`, chargé au démarrage suivant.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| `grafana-cli: not found` | Commande supprimée en Grafana 13 | `grafana cli` (espace) |
| Plugin absent après installation CLI | Grafana non redémarré | `docker compose restart grafana` |

## Défi 07.2b ⭐⭐ — Second indicateur du Status Panel
### Solution
Extrait du modèle JSON du Status Panel :
```json
"fieldConfig": {
  "defaults": {"custom": {"aggregation": "last", "displayAliasType": "Always",
    "displayValueWithAlias": "When Alias Displayed",
    "thresholds": {"valueHandler": "Number Threshold", "warn": "2", "crit": "1"}}},
  "overrides": [
    {"matcher": {"id": "byFrameRefID", "options": "A"},
     "properties": [{"id": "displayName", "value": "Sites en service"}]},
    {"matcher": {"id": "byFrameRefID", "options": "B"},
     "properties": [{"id": "displayName", "value": "Perte de paquets"},
       {"id": "custom.thresholds", "value": {"valueHandler": "Number Threshold", "warn": "0.01", "crit": "0.02"}},
       {"id": "unit", "value": "percentunit"}]}]
}
```
Affichage relevé au banc : `Sites en service - 3`, `Perte de paquets - 0.0190%`.

### Pourquoi
- Perte de paquets : `Warning` 0.01 < `Critical` 0.02 → les petites valeurs sont bonnes.
- Pavé = état le plus grave des indicateurs : un seul indicateur critique suffit à le passer au rouge.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Noms `A`, `B` au lieu des libellés | Légende ignorée par le plugin | Override **Display name** par requête |
| Perte de paquets toujours critique | Seuils de la requête A appliqués à B | Seuils propres dans l'override B |

## Défi 07.3 ⭐⭐ — Le schéma du réseau avec Flow
### Solution
| Requête | Expression | Légende |
|---|---|---|
| A | `sum by (link) (rate(telcea_link_bytes_total[5m])) * 8 / sum by (link) (telcea_link_capacity_bits_per_second)` | `{{link}}` |
| B | `sum by (region) (telcea_site_up)` | `{{region}}` |

Options du panel : **SVG** = `reseau-telcea.svg`, **Panel Config** = `flow-config.yaml`, **Time Slider** désactivé. Relevé au banc : `REN-PAR 29%`, `LIL-PAR 32%`, `MRS-PAR 43%`, 4 régions vertes.

### Pourquoi
- `cellIdPreamble: "cell-"` : l'identifiant SVG `cell-REN-PAR` est référencé `REN-PAR` dans le YAML.
- `dataRef` = nom de la série tel que Grafana le transmet (ici la légende).
- Ancres YAML (`&seuils-liens`, `*seuils-liens`) : seuils définis une fois, réutilisés pour chaque lien.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Tout reste gris | Légendes absentes : séries nommées `{link="REN-PAR"}` | Légendes `{{link}}` et `{{region}}` |
| Erreur YAML dans le panel | Indentation par tabulations lors du copier-coller | Coller tel quel ; indentation par espaces |
| SVG non affiché | Fichier tronqué au copier-coller | Recopier tout le fichier, de `<svg` à `</svg>` |

## Défi 07.4 ⭐⭐⭐ — Atelier « Chasse au plugin »
### Exemple de grille (besoin : carte de couverture radio)
| Critère | Valeur relevée |
|---|---|
| Plugin | Geomap (visualisation interne) + couche **Heatmap** |
| Signature | Core (livré avec Grafana) |
| Dernière mise à jour | Suit les versions de Grafana |
| Compatibilité 13 | Oui |
| Licence | AGPLv3 (Grafana) |
| Dépôt, tickets | Dépôt `grafana/grafana` |
| Apport | Densité d'abonnés par zone, sans plugin tiers |
| Vigilance | Fond de carte téléchargé depuis Internet |

Décision : visualisation native préférée à un plugin tiers (aucune dépendance supplémentaire).

### Pourquoi
- Première question de la grille : une visualisation NATIVE répond-elle déjà au besoin ?
- Plugin communautaire sans mise à jour depuis plus de 12 mois : risque d'incompatibilité à la prochaine version majeure.

## QCM — Réponses
1. **A** — Signature : éditeur identifié et code identique à la version publiée.
2. **D** — `grafana-cli` supprimé en Grafana 13.
3. **B** — Plugins Angular retirés en Grafana 12.
4. **A** — Plugins installés par la CLI chargés au démarrage.
5. **D** — `dataRef` doit correspondre au nom d'une série.
6. **C** — L'icône n'indique ni la qualité ni la maintenance.
