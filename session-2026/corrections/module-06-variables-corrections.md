# Module 06 — Corrections

État final de référence : `scripts/m06/catch-up/detail-regional.json` (uid `tlc-reseau-regional`, généré par `scripts/m06/catch-up/generer.py`).

## Lab 06.1 ⭐ — Le tableau de bord régional et sa variable Région
### Solution
Variable `region` dans le modèle JSON (Settings → **JSON Model**, extrait) :
```json
{"type": "query", "name": "region", "label": "Région",
 "definition": "label_values(telcea_site_info, region)",
 "multi": true, "includeAll": true, "refresh": 1}
```
`refresh: 1` = **On dashboard load**.

### Pourquoi
- `telcea_site_info` : une série par site avec toutes les étiquettes descriptives ; source idéale pour les listes.
- Multi-valeur : Grafana remplace `$region` par `(Bretagne|Provence)`, d'où `=~` dans la requête.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Liste vide | Métrique mal orthographiée ou **Data source** non choisie | Vérifier dans Explore → **Metrics browser** |
| « No data » avec 2 régions | `region="$region"` | `region=~"$region"` |
| Panel inchangé quand la région change | Requête sans `$region` | Ajouter le filtre dans la requête |

## Lab 06.2 ⭐ — Une variable Site qui dépend de la région
### Solution
| Variable | Type | Définition |
|---|---|---|
| `site` | Query (Classic query) | `label_values(telcea_site_info{region=~"$region"}, site)`, multi-valeur, `All` |

Requête du panel `Abonnés par site` :
```promql
sum by (site) (telcea_cell_users{region=~"$region", site=~"$site"})
```
Région `Bretagne` → liste Site : `BRE-01`, `QUI-01`, `REN-01` ; Site `BRE-01` → 1 courbe.

### Pourquoi
- Variable fille placée APRÈS la mère : Grafana évalue les variables dans l'ordre de la liste.
- `{region=~"$region"}` dans la définition de `site` : liste limitée aux sites de la région choisie.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Liste Site non mise à jour | `site` placée avant `region` | Réordonner la liste des variables |
| Sites d'autres régions dans la liste | Requête de `site` sans filtre | `{region=~"$region"}` |
| Panel inchangé quand le site change | Requête du panel sans `site=~"$site"` | Remplacer la requête (étape 3) |

### Variantes acceptables
- Variable `site` en **Query type** `Label values` avec filtre d'étiquette `region =~ $region` : équivalent.

## Défis facultatifs

## Défi 06.2b ⭐⭐ — Variables Techno et Fenêtre de calcul
### Solution
| Variable | Type | Définition |
|---|---|---|
| `techno` | Custom | `4G,5G`, multi-valeur, `All` |
| `fenetre` | Interval | `1m,5m,15m,1h`, valeur par défaut `5m` |

Ordre : `region`, `site`, `techno`, `fenetre`. Requête de `Abonnés par site` : ajout de `techno=~"$techno"`. Panel `Débit descendant par site ($fenetre)`, unité `bits/sec(SI)`, requête de l'énoncé. Tags `telcea`, `reseau`, `radio`.

Sélection Région `Bretagne` + Techno `4G` (banc) : courbes `BRE-01` et `QUI-01`.

### Pourquoi
- `fenetre` dans `rate(...[$fenetre])` : lissage réglable par l'utilisateur sans éditer le panel.
- `$fenetre` dans le titre : fenêtre de calcul visible sur le panel.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Erreur `bad_data: 1:...: parse error` | Variable Interval utilisée hors crochets (`$fenetre` seule) | Uniquement dans `[$fenetre]` |
| Techno sans effet | Filtre `techno=~"$techno"` absent de la requête | L'ajouter |

### Variantes acceptables
- Variable `fenetre` de type Custom : fonctionne, mais sans l'option `Auto` des variables Interval.

## Défi 06.3 ⭐⭐ — Panels répétés et frise de disponibilité
### Solution
| Panel | Requête | Réglages |
|---|---|---|
| Sites en service — `$region` | `sum(telcea_site_up{region=~"$region"})` (Instant) | **Repeat by variable** `region`, **Repeat direction** horizontale, **Max per row** 4 ; seuils rouge / 3 vert ; fond coloré |
| Disponibilité des sites | `telcea_site_up{region=~"$region", site=~"$site", techno=~"$techno"}`, légende `{{site}}` | State timeline + value mapping En service / Hors service |
| Latence au 95e centile (`$fenetre`) | `histogram_quantile(0.95, sum by (le, site) (rate(telcea_site_latency_seconds_bucket{region=~"$region", site=~"$site"}[$fenetre])))` | Unité `seconds (s)`, seuil rouge `0.1` en pointillés |

### Pourquoi
- Panel répété : dans chaque copie, `$region` vaut UNE région (d'où `Sites en service — Bretagne`).
- Latence SANS filtre `techno` : `telcea_site_latency_seconds_bucket` ne porte que `region` et `site` ; le filtre `techno=~"(4G|5G)"` exclut toutes les séries.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Latence « No data » | Filtre `techno` sur une métrique sans étiquette `techno` | Retirer le filtre (vérifier les étiquettes dans Explore) |
| Un seul Stat malgré 4 régions | **Repeat by variable** non réglé, ou variable non multi-valeur | Régler la répétition ; `region` en Multi-value |
| Stats répétés tous identiques | Requête du Stat sans `$region` | `{region=~"$region"}` |

## Défi 06.4 ⭐⭐⭐ — Ranger, relier, restaurer
### Solution
1. **Dashboards** → dossier `NOC Telcéa` → **New → New folder** : `Radio`, puis `Transport`. Tableau de bord régional : **Move** (case à cocher dans la liste) → `NOC Telcéa / Radio`.
2. Settings → **Links** → **Add dashboard link** : **Type** `Dashboards`, **With tags** `telcea`, **Show as dropdown** activé, **Include current time range** activé, titre `Telcéa`.
3. Tableau de bord → Settings → **Delete dashboard** ; **Dashboards → Recently deleted** → cocher → **Restore** → dossier `Radio`.

### Pourquoi
- Sous-dossiers par équipe : droits posés une fois au niveau du dossier (M10).
- Liens par tag : tout nouveau tableau de bord tagué `telcea` apparaît sans modifier les autres.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Lien vide | Tag différent (`Telcea` majuscule) | Tags en minuscules, identiques |
| Tableau de bord absent de la corbeille | Suppression définitive depuis la corbeille | Restauration impossible : réimport (rattrapage M06) |

## QCM — Réponses
1. **C** — Query : valeurs lues dans la source.
2. **B** — `=~` : la sélection multiple devient une expression régulière `(A|B)`.
3. **C** — La requête de la fille filtre sur la valeur de la mère.
4. **A** — Un filtre sur une étiquette absente exclut toutes les séries.
5. **D** — **Repeat by variable** : une copie du panel par valeur sélectionnée.
6. **B** — Grafana 13 : Dashboards → Recently deleted → Restore.
