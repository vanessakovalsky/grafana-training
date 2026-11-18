# Module 10 — Exercices

Tests de connexion avec un autre compte : fenêtre de navigation privée (session `admin` conservée dans la fenêtre principale).

## Lab 10.1 ⭐ — Comptes et équipes (guidé)
**Durée** : 15 min · **Objectif** : créer 3 comptes au rôle Viewer et 2 équipes
**Contexte** : le NOC de Telcéa ouvre Grafana à ses techniciens et à la direction.
**Prérequis** : session `admin`

Variables : `<MOT_DE_PASSE_TEST>` = mot de passe commun des comptes de test, choisi par la formatrice (ex. `Telcea-2027!`).

### Étapes
1. **Administration → Users and access → Users → New user** :
   - **Name** `Technicien radio`, **Email** `tech.radio@telcea.example`, **Username** `tech.radio`, **Password** `<MOT_DE_PASSE_TEST>` → **Create user**
   - idem `Technicien transport` (`tech.transport`) et `Directeur NOC` (`directeur`)
   Résultat attendu : 4 utilisateurs dans la liste, les 3 nouveaux au rôle `Viewer`.
2. **Invite** : inviter `astreinte@telcea.example` (rôle Viewer, **Send invite email** coché).
   Résultat attendu : courriel d'invitation dans Mailpit (`/mail/`).
3. **Administration → Users and access → Teams → New team** : `Radio` (courriel `radio@telcea.example`) → **Create** → **Add member** : `tech.radio`.
4. Idem équipe `Transport` avec `tech.transport`.

### Critères de réussite
- [ ] 3 comptes Viewer, 1 invitation reçue dans Mailpit
- [ ] 2 équipes d'un membre chacune

---

## Lab 10.2 ⭐ — Droits par dossier (guidé)
**Durée** : 15 min · **Objectif** : chaque équipe modifie les tableaux de bord de SON dossier
**Contexte** : l'équipe *radio* maintient le tableau de bord régional ; l'équipe *transport* ne doit pas pouvoir le modifier.
**Prérequis** : Lab 10.1, défi 06.4 (sous-dossiers `Radio` et `Transport`) ou rattrapage

### Étapes
1. Vérifier l'arborescence : `NOC Telcéa / Radio` (contient `[TLC] Réseau — Détail régional`) et `NOC Telcéa / Transport`. Créer les sous-dossiers si besoin (**New → New folder** dans `NOC Telcéa`).
2. Dossier `Radio` → **Folder actions → Manage permissions** → **Add a permission** : **Team** `Radio`, **Edit** → **Save**.
3. Dossier `Transport` : **Team** `Transport`, **Edit**.
4. Fenêtre privée, connexion `tech.radio` : ouvrir le tableau de bord régional → **Edit** → modifier un titre → **Save**.
   Résultat attendu : enregistrement accepté.
5. Fenêtre privée, connexion `tech.transport` : même tableau de bord.
   Résultat attendu : bouton **Edit** absent (ou enregistrement refusé).
6. Connexion `directeur` : consultation possible, aucune modification.

### Critères de réussite
- [ ] Tableau des 4 tests (profil, action, attendu, obtenu) rempli, sans écart
- [ ] Permissions visibles dans **Manage permissions** des deux dossiers

---

## Exercice 10.3 ⭐⭐ — Une alerte et un écran pour chaque équipe (semi-autonome)
**Durée** : 10 min · **Objectif** : étendre le moindre privilège aux règles d'alerte
**Contexte** : l'équipe *transport* veut ajuster le seuil de « Lien de collecte sature » sans pouvoir toucher aux alertes radio.

**Énoncé** :
- Déplacer la règle « Lien de collecte sature » dans le dossier `Transport` (nouveau groupe d'évaluation `transport-1m`, 1 min).
- Vérifier avec `tech.transport` : modification du seuil possible sur cette règle, impossible sur « Site radio hors service ».

**Indices** :
- Les règles Grafana suivent les permissions du dossier qui les contient
- Modifier une règle → section 3 (dossier) et section 4 (groupe)

**Critères de réussite** :
- [ ] Règle dans `NOC Telcéa / Transport`
- [ ] Test positif et test négatif avec `tech.transport`

---

## Défi 10.4 ⭐⭐⭐ — Compte de service pour la sauvegarde (autonome)
**Durée** : 5 min · **Objectif** : remplacer le mot de passe `admin` d'un script par un jeton à droits limités
**Contexte** : un script nocturne exporte tous les tableaux de bord du NOC (sauvegarde) ; il ne doit rien pouvoir modifier.

**Énoncé** : créer un compte de service `sauvegarde-noc` au rôle adapté, générer un jeton valable 30 jours, puis, dans le terminal du bureau, lister les tableaux de bord avec ce jeton et prouver qu'il ne peut pas en créer.

Variables : `<JETON>` = jeton généré (affiché une seule fois).

**Critères de réussite** :
- [ ] `GET /api/search` avec le jeton : liste des tableaux de bord (HTTP 200)
- [ ] `POST /api/dashboards/db` avec le jeton : refus (HTTP 403)
