# Module 10 — Exercices

Parcours essentiel = Labs 10.1 et 10.2 (tout le groupe). Défis = facultatifs, en cas d'avance.
Tests de connexion avec un autre compte : fenêtre de navigation privée (session `admin` conservée dans la fenêtre principale).

Variables : `<MOT_DE_PASSE_TEST>` = mot de passe commun des comptes de test, donné par la formatrice (ex. `Telcea-2027!`).

## Lab 10.1 ⭐ — Comptes et équipes (guidé)
**Durée** : 15 min · **Objectif** : créer 2 comptes au rôle Viewer et 2 équipes
**Contexte** : le NOC de Telcéa ouvre Grafana à ses techniciens.
**Prérequis** : session `admin`

### Étapes
1. **Administration → Users and access → Users → New user** :
   **Name** `Technicien radio`, **Email** `tech.radio@telcea.example`, **Username** `tech.radio`, **Password** `<MOT_DE_PASSE_TEST>` → **Create user**.
2. Idem : **Name** `Technicien transport`, **Email** `tech.transport@telcea.example`, **Username** `tech.transport`.
   Résultat attendu : 3 utilisateurs dans la liste, les 2 nouveaux au rôle `Viewer`.
3. **Administration → Users and access → Teams → New team** : `Radio` → **Create** → **Add member** : `tech.radio`.
4. Idem : équipe `Transport` avec `tech.transport`.

### Critères de réussite
- [ ] 2 comptes Viewer
- [ ] 2 équipes d'un membre chacune

---

## Lab 10.2 ⭐ — Droits sur un dossier : test positif, test négatif (guidé)
**Durée** : 15 min · **Objectif** : l'équipe *radio* modifie les tableaux de bord du dossier `NOC Telcéa`, l'équipe *transport* non
**Contexte** : l'équipe *radio* maintient le tableau de bord régional ; l'équipe *transport* ne doit pas pouvoir le modifier.
**Prérequis** : Lab 10.1, tableau de bord `[TLC] Réseau — Détail régional` dans `NOC Telcéa` (M06)

### Étapes
1. **Dashboards** → dossier `NOC Telcéa` → **Folder actions → Manage permissions**.
2. **Add a permission** : **Team** `Radio`, **Edit** → **Save**.
3. Fenêtre privée, connexion `tech.radio` : ouvrir le tableau de bord régional → **Edit** → modifier un titre de panel → **Save**.
   Résultat attendu : enregistrement accepté (test positif).
4. Se déconnecter, connexion `tech.transport` : même tableau de bord.
   Résultat attendu : bouton **Edit** absent, ou enregistrement refusé (test négatif).

### Si bloqué
Comptes, équipes, dossiers et droits créés par la formatrice (rattrapage, 5 s).

### Critères de réussite
- [ ] Test positif avec `tech.radio`, test négatif avec `tech.transport`

---

## Défis facultatifs (en cas d'avance)

## Défi 10.2b ⭐⭐ — Invitation, direction et dossier Transport
**Durée** : 10 min
**Énoncé** :
1. **Administration → Users and access → Users → Invite** : `astreinte@telcea.example`, rôle Viewer, **Send invite email** coché ; courriel d'invitation dans Mailpit (`/mail/`).
2. Compte `Directeur NOC` (`directeur`, Viewer) : consultation possible, aucune modification.
3. Sous-dossiers `NOC Telcéa / Radio` (y déplacer le tableau de bord régional, droit **Edit** pour l'équipe `Radio`) et `NOC Telcéa / Transport` (droit **Edit** pour l'équipe `Transport`) ; retirer le droit de l'équipe `Radio` sur `NOC Telcéa`.
4. Tableau des tests (profil, action, attendu, obtenu).

**Critères de réussite** :
- [ ] Invitation reçue ; tableau de tests sans écart

---

## Défi 10.3 ⭐⭐ — Une alerte et un écran pour chaque équipe (semi-autonome)
**Durée** : 10 min · **Objectif** : étendre le moindre privilège aux règles d'alerte
**Prérequis** : défi 10.2b (dossier `Transport`), défi 09.3 (règle « Lien de collecte sature ») ou rattrapage M09
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
