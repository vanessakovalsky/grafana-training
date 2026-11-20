# Module 08 — Corrections

## Lab 08.1 ⭐ — Lien interne et lien externe
### Solution
Étapes de l'énoncé. Comportements relevés au banc (Grafana 13.3.1) :
- Lien externe actif : page accessible sans session (API `GET /api/public/dashboards/<TOKEN>` → HTTP 200).

Équivalent par l'API (terminal du bureau) :
```bash
cd ~/grafana-training/stack
curl -s -u "admin:$(grep ^GRAFANA_ADMIN_PASSWORD .env | cut -d= -f2)" -H 'Content-Type: application/json' \
  -X POST http://localhost:3000/grafana/api/dashboards/uid/tlc-noc-mural/public-dashboards \
  -d '{"isEnabled":true,"share":"public"}' | jq -c '{accessToken, isEnabled, share}'
```
Sortie attendue (jeton différent) :
```
{"accessToken":"60aa1408bec9483fadf14953fddbf5c7","isEnabled":true,"share":"public"}
```

### Pourquoi
- **Lock time range** : le lien transporte `from` et `to` absolus ; ouvert le lendemain, il montre toujours l'incident.
- Lien externe : lecture seule, tableau de bord ENTIER, sans authentification : jamais de données sensibles.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Destinataire voit « maintenant » au lieu de l'incident | **Lock time range** désactivé | Réactiver, recopier le lien |
| Bouton **Accept** grisé | Case de confirmation non cochée | Cocher « I understand… » |
| Écran mural demandant une connexion | Lien interne copié au lieu du lien externe | **Share externally** → **Copy external link** |
| Panel Flow vide sur le lien externe | Rendu identique attendu : sinon, plugin non installé sur l'instance | Vérifier l'installation (M07) |

## Lab 08.2 ⭐ — Snapshot d'incident
### Solution
Étapes de l'énoncé. Snapshot listé dans **Dashboards → Snapshots** avec son nom et son expiration.

### Pourquoi
- Snapshot : données et mise en forme copiées dans la base Grafana ; requêtes et références aux sources retirées.
- Expiration courte (1 jour) : le snapshot ne survit pas à l'enquête.
- Publication locale UNIQUEMENT : `snapshots.raintank.io` est un service public de Grafana Labs (données hors du SI).

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Snapshot vide pour certains panels | Panels repliés (lignes fermées) au moment de la publication | Déplier les lignes avant la publication |
| Snapshot publié hors du SI | **Publish to snapshots.raintank.io** choisi | **Dashboards → Snapshots** → supprimer, republier en local |
| Lien inaccessible pour le prestataire | Instance Grafana non joignable de l'extérieur | Lien externe (Lab 08.1) ou export PDF (Enterprise) |

## Défis facultatifs

## Défi 08.2b ⭐⭐ — Maîtriser les partages publics et les snapshots
### Solution
1. **Dashboards → Public dashboards** → écran mural → **Pause access** : fenêtre privée rechargée → message `Dashboard paused` ; réactivation → écran de nouveau visible.
2. **Dashboards → Snapshots** : snapshot listé avec son nom et sa date d'expiration (création + 1 jour).
3. **Share internally** → **Shorten link** : lien court `.../goto/<ID>`.

### Pourquoi
- Pause = coupure immédiate et réversible (jeton conservé) ; suppression = jeton détruit, nouveau lien à diffuser.
- Lien court : stocké dans la base Grafana, valable pour les utilisateurs connectés seulement.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Lien externe « introuvable » après réactivation | Accès supprimé (et non mis en pause) | Recréer le partage externe |
| Écran toujours visible pendant la pause | Fenêtre privée non rechargée | `F5` |

## Défi 08.3 ⭐⭐ — Échanger un tableau de bord avec son binôme
### Solution
1. **Export → Export as code** → activer **Share dashboard with another instance** → **Download file**.
2. **Dashboards → New → Import dashboard** → **Upload dashboard JSON file** (fichier du binôme).
3. Options d'import : **Name** `[TLC] Réseau — Détail régional (binôme <PRÉNOM>)`, **Folder** `NOC Telcéa`, **UID** modifié (ex. `tlc-reseau-regional-binome`), source **Prometheus** locale → **Import**.

Écran d'import d'un fichier en schéma v2 (Grafana 13.3.1) : **Name**, **Folder**, **Unique identifier (UID)** (bouton **Change uid**), un sélecteur de source par source à résoudre (erreur « Please select a data source » si vide), puis **Import** (ou **Import (Overwrite)** si l'uid existe déjà). Pas de rubrique library panels en v2.

### Pourquoi
- Sources d'une autre instance = uid inconnus localement : l'option d'export les remplace par des paramètres choisis à l'import.
- uid unique par instance : conserver l'uid d'origine écraserait son propre tableau de bord régional.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Panels « Datasource … was not found » | Export sans **Share dashboard with another instance** | Réexporter avec l'option, ou choisir la source dans chaque panel |
| « A dashboard with the same uid already exists » | uid d'origine conservé | Changer l'uid (ou le titre) à l'import |
| Variables vides | Source de la variable `region` non résolue | Vérifier la source dans Settings → Variables |

### Variantes acceptables
- JSON collé dans la zone de texte de l'import au lieu du fichier.
- Export classique sans l'option, puis remplacement manuel de l'uid de source : fonctionne, plus long.

## Défi 08.4 ⭐⭐⭐ — Un panel de consignes partagé
### Solution
1. Tableau de bord national, mode édition → menu du panel `Consignes du NOC` → **More...** → **New library panel** → dossier `NOC Telcéa` → enregistrer.
2. Écran mural → nouveau panel → **Use library panel** → `Consignes du NOC`.
3. Modification du texte depuis l'un des tableaux de bord → **Save** (confirmation de la mise à jour du library panel) → l'autre affiche `1011`.

### Pourquoi
- Library panel = un seul objet stocké, référencé par plusieurs tableaux de bord.
- **Unlink library panel** : redevenir une copie locale (modifications non propagées).

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Modification non propagée | Panel copié-collé au lieu d'être ajouté comme library panel | Remplacer la copie par **Use library panel** |
| Library panel introuvable dans l'autre tableau de bord | Dossier du library panel non accessible (droits, M10) | Ranger le library panel dans `NOC Telcéa` |

## QCM — Réponses
1. **A** — Lien externe : en direct, sans compte.
2. **D** — **Lock time range** convertit la plage relative en plage absolue.
3. **C** — Snapshot : données affichées et mise en forme, sans requêtes ni sources.
4. **B** — Publication sur un service public de Grafana Labs : sortie des données.
5. **D** — Sources remplacées par des paramètres d'import.
6. **A** — Un library panel est partagé : toute modification est visible partout.
