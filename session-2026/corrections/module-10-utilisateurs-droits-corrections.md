# Module 10 — Corrections

État final de référence : `scripts/m10/catch-up/droits.sh` (sous-dossiers, comptes de test, équipes, permissions).

## Lab 10.1 ⭐ — Comptes et équipes
### Solution
Étapes de l'énoncé. Contrôle par l'API (terminal du bureau, facultatif) :
```bash
cd ~/grafana-training/stack
curl -s -u "admin:$(grep ^GRAFANA_ADMIN_PASSWORD .env | cut -d= -f2)" \
  http://localhost:3000/grafana/api/org/users | jq -r '.[] | .login + " " + .role'
```
Sortie attendue :
```
admin Admin
tech.radio Viewer
tech.transport Viewer
```
Équipes : `Radio` (membre `tech.radio`), `Transport` (membre `tech.transport`).

### Pourquoi
- Rôle Viewer par défaut : les droits de modification viennent UNIQUEMENT des permissions de dossier (Lab 10.2).
- Équipe = groupe de comptes : un droit donné une fois à l'équipe vaut pour tous ses membres.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| `User with same email or login already exists` | Compte déjà créé (rattrapage) | Utiliser le compte existant |
| Membre absent de l'équipe | **Add member** non validé | Rouvrir l'équipe → **Add member** |
| Nouveau compte au rôle Editor | Rôle modifié à la création | **Users** → rôle `Viewer` |

## Lab 10.2 ⭐ — Droits sur un dossier : test positif, test négatif
### Solution
Permission ajoutée sur `NOC Telcéa` : équipe `Radio` → **Edit**.

| Profil | Action | Attendu |
|---|---|---|
| `tech.radio` | Modifier et enregistrer le tableau de bord régional | Autorisé (test positif) |
| `tech.transport` | Même action | Refusé : **Edit** absent ou enregistrement refusé (test négatif) |

### Pourquoi
- Viewer + permission Edit sur un dossier = modification limitée à ce dossier (et à ses sous-dossiers).
- Permissions par défaut du dossier (Viewer View, Editor Edit) conservées : lecture pour tous, écriture ciblée.
- Test négatif aussi important que le positif : il prouve que le droit ne s'étend pas aux autres comptes.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| `tech.transport` peut modifier | Rôle d'organisation Editor (Edit sur tous les dossiers par défaut) | Rôle Viewer |
| `tech.radio` ne peut pas enregistrer | Permission donnée à un utilisateur au lieu de l'équipe, ou non enregistrée | Vérifier **Manage permissions** |
| Connexion `admin` perdue | Test fait dans la fenêtre principale | Fenêtre de navigation privée pour les comptes de test |

## Défis facultatifs

## Défi 10.2b ⭐⭐ — Invitation, direction et dossier Transport
### Solution
Courriel d'invitation relevé dans Mailpit (banc) :
```
astreinte@telcea.example | admin has invited you to join Grafana
```
Comptes (API `GET /api/org/users`) : `admin Admin`, `tech.radio Viewer`, `tech.transport Viewer`, `directeur Viewer`.

| Profil | Action | Attendu | Obtenu au banc (API) |
|---|---|---|---|
| `tech.radio` | Enregistrer le tableau de bord régional (dossier Radio) | Autorisé | HTTP 200 |
| `tech.transport` | Même action | Refusé | HTTP 403 |
| `directeur` | Lire le tableau de bord régional | Autorisé | HTTP 200 |
| `directeur` | L'enregistrer | Refusé | HTTP 403 |

Permissions du dossier `Radio` (API `GET /api/access-control/folders/noc-radio`) : rôle `Viewer` View, rôle `Editor` Edit, équipe `Radio` Edit, rôle `Admin` Admin.

### Pourquoi
- Invitation : l'utilisateur choisit lui-même son mot de passe (aucun secret transmis).
- Droit retiré sur `NOC Telcéa` : sinon l'équipe `Radio` hériterait de Edit sur `Transport` (sous-dossier).

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Invitation non reçue | **Send invite email** décoché | Renvoyer depuis **Pending invites** |
| `tech.radio` peut modifier `Transport` | Droit Edit de `Radio` conservé sur le dossier parent | Le retirer sur `NOC Telcéa` |
| Tableau de bord régional absent de `Radio` | Déplacement non fait (ou Défi 06.4 non réalisé) | **Move** vers `NOC Telcéa / Radio` |

## Défi 10.3 ⭐⭐ — Une alerte et un écran pour chaque équipe
### Solution
Règle « Lien de collecte sature » → **Edit** → section 3 **Folder** `Transport` → section 4 **New evaluation group** `transport-1m` (1m) → **Save**.
Test : `tech.transport` modifie le seuil (0.8 → 0.85) ; sur « Site radio hors service », bouton de modification absent.

### Pourquoi
- Règles Grafana rangées dans un dossier : mêmes permissions que les tableaux de bord de ce dossier.
- Groupe d'évaluation propre au dossier : un groupe appartient à un seul dossier.

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| Groupe `telcea-1m` non proposé | Groupe lié au dossier `NOC Telcéa` | Créer `transport-1m` |
| Routage cassé après déplacement | Label `equipe` supprimé par erreur | Labels conservés : `equipe=transport` |

## Défi 10.4 ⭐⭐⭐ — Compte de service pour la sauvegarde
### Solution
**Service accounts → Add service account** : `sauvegarde-noc`, rôle `Viewer` → **Add service account token** (expiration 30 jours) → copier le jeton.
```bash
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer <JETON>" \
  http://localhost:3000/grafana/api/search
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer <JETON>" \
  -H 'Content-Type: application/json' -X POST \
  http://localhost:3000/grafana/api/dashboards/db -d '{"dashboard":{"title":"test"}}'
```
Sortie relevée au banc :
```
200
403
```
Jeton au format `glsa_...`.

### Pourquoi
- Viewer suffit pour exporter : le jeton volé ne permet aucune modification.
- Jeton révocable et daté, indépendant des mots de passe des personnes.

## QCM — Réponses
1. **C** — Viewer : consultation seule.
2. **B** — Permission Edit de l'équipe sur le dossier Radio.
3. **D** — Membre de l'équipe : hérite de ses permissions.
4. **C** — Le refus attendu est vérifié.
5. **A** — Compte de service + jeton à droits limités.
6. **B** — Admin sur un dossier : gestion de ses permissions.
