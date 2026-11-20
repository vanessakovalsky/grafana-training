# Module 09 — Corrections

État final de référence : `scripts/m09/catch-up/alerting.sh` (points de contact, politique, 3 règles du groupe `telcea-1m`).

## Lab 09.1 ⭐ — Première règle : site radio hors service
### Solution
| Section | Valeur |
|---|---|
| 1. Name | `Site radio hors service` |
| 2. Requête / condition | `telcea_site_up` (Instant) ; WHEN QUERY IS BELOW `1` |
| 3. Folder / labels | `NOC Telcéa` ; `equipe=radio` |
| 4. Évaluation | Groupe `telcea-1m` (1 min) ; Pending period `1m` |
| 5. Notifications | Routage par politique de notification (Lab 09.2) |

Contrôle par l'API :
```bash
curl -s -u "admin:$(grep ^GRAFANA_ADMIN_PASSWORD ~/grafana-training/stack/.env | cut -d= -f2)" \
  http://localhost:3000/grafana/api/prometheus/grafana/api/v1/rules | jq -c '.data.groups[].rules[] | {name, state, health}'
```
Sortie attendue hors incident :
```
{"name":"Site radio hors service","state":"inactive","health":"ok"}
```
(`inactive` = toutes les instances à Normal.)

### Pourquoi
- Requête sans agrégation : une instance par site, donc une notification qui nomme les sites coupés.
- Pending 1 min : une coupure de quelques secondes (redémarrage) ne réveille personne.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Une seule instance | Requête agrégée (`sum(telcea_site_up)`) | Requête sans `sum` pour une instance par site |
| Règle en `Error` | Requête en Range avec condition simple, ou source absente | **Type** `Instant` ; **Preview** |
| Groupe absent de la liste | Dossier non choisi avant le groupe | Section 3 d'abord, puis section 4 |

## Lab 09.2 ⭐ — Points de contact et routage par équipe
### Solution
Politique relevée au banc (**Notification policies**) :
```
Default policy · 2 routes          Delivered to NOC Telcea
 ├─ equipe = radio                 Delivered to Equipe radio
 └─ equipe = transport             Delivered to Equipe transport
```
(Le rattrapage ajoute un regroupement `alertname, region` sur la politique par défaut.)

### Pourquoi
- Politique par défaut = filet de sécurité : toute alerte sans label `equipe` arrive au NOC.
- Routes testées dans l'ordre : la première route dont le matcher correspond reçoit l'alerte.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Route absente sous **Default policy** | **Add route** non enregistré | Refaire, puis enregistrer |
| Alerte radio reçue par le NOC | Matcher `equipe = Radio` (majuscule) | Valeur identique au label de la règle |
| Ressources marquées **Provisioned** | Créées par fichier ou API de provisioning | Modifier la source (fichier) ; le rattrapage crée des ressources modifiables |

## Lab 09.3 ⭐ — La tempête en Bretagne (observation)
### Solution
Chronologie type (règle `Site radio hors service`, minutes après le lancement de la tempête) :

| Délai | Événement |
|---|---|
| 1 à 2 min | Sites bretons coupés (BRE-01, QUI-01) : `Normal` → `Pending` |
| 2 à 3 min | `Pending` → `Firing` |
| 3 à 4 min | Courriel « Site radio hors service » → `radio@telcea.example` (Mailpit) |

Relevé au banc (18/11/2026, tempête à 12 h 22 min 18 s) : `Pending` à 12 h 23 min 43 s, courriel `[FIRING:2] Site radio hors service Bretagne` à 12 h 24 min 36 s. Tableau `État des sites` : `Hors service` sur fond rouge pour BRE-01 et QUI-01.

### Pourquoi
- Délai ≈ évaluation (≤ 1 min) + pending (1 min) + `group_wait` (30 s) avant le courriel.
- Label `equipe=radio` → route `equipe = radio` → point de contact `Equipe radio` : rien chez `transport@`.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Aucune alerte | Tempête non lancée sur la VM | `tempete.sh <CONFIG> etat stagiaireNN` |
| Courriel reçu par `noc@` au lieu de `radio@` | Route `equipe=radio` absente ou valeur différente du label | Corriger la route (Lab 09.2) |
| Courriel absent alors que l'alerte est `Firing` | Délai `group_wait` non écoulé | Attendre 30 s à 1 min |

## Défis facultatifs

## Défi 09.2b ⭐⭐ — Tester et documenter les alertes
### Solution
- **Test → Send test notification** sur chaque point de contact : 3 courriels de test dans Mailpit, expéditeur `grafana@telcea.example`, un par adresse.
- Règle `Site radio hors service` : label `severite=critique` ; section 6, **Summary** : `Site {{ $labels.site }} ({{ $labels.region }}) hors service`.

### Pourquoi
- Test avant l'incident : une adresse ou un SMTP erroné se découvre à froid, pas pendant la tempête.
- `{{ $labels.site }}` : une instance par site → le message nomme le site coupé.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Test en échec | SMTP de Grafana non configuré | Stack : `GF_SMTP_HOST=mailpit:1025` (vérifier Settings) |
| Résumé affichant `<no value>` | Nom de label mal orthographié | `$labels.site`, `$labels.region` |

## Défi 09.3 ⭐⭐ — La tempête en Bretagne : deux règles de plus
### Solution
Règles complémentaires (en plus de `Site radio hors service`) :

| Règle | Requête | Condition | Pending | Labels |
|---|---|---|---|---|
| Lien de collecte sature | `sum by (link, region) (rate(telcea_link_bytes_total[5m])) * 8 / sum by (link, region) (telcea_link_capacity_bits_per_second)` | IS ABOVE `0.8` | `2m` | `equipe=transport`, `severite=majeure` |
| Site sur batterie | `telcea_site_on_battery` | IS ABOVE `0` | `1m` | `equipe=radio`, `severite=mineure` |

Chronologie relevée au banc (18/11/2026, tempête à 12 h 22 min 18 s) :

| Heure | Événement |
|---|---|
| 12 h 23 min 43 s | Site radio hors service : BRE-01, QUI-01 `Pending` ; Site sur batterie : BRE-01, QUI-01, REN-01 `Pending` |
| 12 h 24 min 33 s | Courriel `[FIRING:3] Site sur batterie Bretagne` → `radio@telcea.example` |
| 12 h 24 min 36 s | Courriel `[FIRING:2] Site radio hors service Bretagne` → `radio@telcea.example` |
| 12 h 26 | Lien REN-PAR à 89 % : `Pending` |
| 12 h 28 min 30 s | Courriel `[FIRING:1] Lien de collecte sature Bretagne` → `transport@telcea.example` |

### Pourquoi
- Délai sites ≈ évaluation (≤ 1 min) + pending (1 min) + `group_wait` (30 s).
- Délai lien plus long : moyenne glissante sur 5 min (`rate(...[5m])`) + pending 2 min.
- `by (link, region)` : labels conservés dans l'instance, réutilisables dans le message et le routage.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Lien jamais en alerte | Seuil `80` au lieu de `0.8` (ratio) | Seuil `0.8` |
| Courriel de lien chez `radio@` | Label `equipe=radio` copié de la première règle | `equipe=transport` |
| Aucune alerte | Tempête non lancée sur la VM | `tempete.sh <CONFIG> etat stagiaireNN` |

## Défi 09.4 ⭐⭐⭐ — Silence et Alertmanager externe
### Solution
- **Silences → Create silence** : matcher `site = BRE-01`, durée `2h`, commentaire `Intervention alimentation` → **Save silence**.
- **Connections → Data sources → Add new data source → Alertmanager** : URL `http://alertmanager:9093`, **Implementation** `Prometheus` → **Save & test** ; dans **Alerting**, sélecteur de source Alertmanager → alerte `SiteRadioHorsService`.
- Mailpit : `alertmanager@telcea.example` (règle Prometheus, objet `[FIRING:2] SiteRadioHorsService Bretagne ...`) et `grafana@telcea.example` (règles Grafana).

### Pourquoi
- Silence par label : BRE-01 seul, QUI-01 continue de notifier.
- Deux moteurs d'alerte coexistent (Prometheus + Alertmanager, Grafana) : choisir un seul propriétaire par alerte pour éviter les doublons (ici, la coupure de site est notifiée deux fois).

## QCM — Réponses
1. **B** — La politique dont les matchers correspondent aux labels choisit le point de contact.
2. **D** — Condition vraie pendant toute la période avant le passage en Alerting.
3. **A** — Une instance par série en anomalie.
4. **C** — Silence sur `site = BRE-01` pour la durée de l'intervention.
5. **B** — Politique par défaut.
6. **D** — Valeur du label de l'instance insérée dans le message.
