# Module 09 — Exercices

Courriels : boîte de test Mailpit de la VM, `https://stagiaireNN.<SESSION>.kovalibre-labs.com/mail/` (aucun courriel ne sort de la VM).

## Lab 09.1 ⭐ — Première règle : site radio hors service (guidé)
**Durée** : 20 min · **Objectif** : créer la règle « Site radio hors service » et observer ses instances
**Contexte** : la nuit, personne ne regarde l'écran du NOC ; une coupure de site doit être signalée automatiquement à l'équipe *radio*.
**Prérequis** : source `Prometheus`, dossier `NOC Telcéa`

### Étapes
1. **Alerting → Alert rules → New alert rule**.
2. Section 1 : **Name** `Site radio hors service`.
3. Section 2 : source `Prometheus`, mode **Code**, requête `telcea_site_up`, **Options → Type** `Instant`.
   **Alert condition** : WHEN QUERY **IS BELOW** `1`. Cliquer sur **Preview alert rule condition**.
   Résultat attendu : 12 instances `Normal` (une par site).
4. Section 3 : **Folder** `NOC Telcéa` ; **Add labels** : `equipe` = `radio`, `severite` = `critique`.
5. Section 4 : **New evaluation group** `telcea-1m`, intervalle `1m` ; **Pending period** `1m` ; **Keep firing for** `None`.
6. Section 5 : laisser le routage par politique de notification (configuré au Lab 09.2) ; si un choix direct est proposé, sélectionner le point de contact par défaut.
7. Section 6 : **Summary** `Site {{ $labels.site }} ({{ $labels.region }}) hors service`.
8. **Save** (bas de page).
   Résultat attendu : règle dans **Alert rules**, dossier `NOC Telcéa`, groupe `telcea-1m`, état `Normal`.

### Critères de réussite
- [ ] Règle enregistrée, 12 instances `Normal`
- [ ] Labels `equipe=radio`, `severite=critique` visibles dans le détail de la règle

---

## Lab 09.2 ⭐ — Points de contact et routage par équipe (guidé)
**Durée** : 20 min · **Objectif** : chaque équipe reçoit uniquement ses alertes, le NOC reçoit le reste
**Contexte** : l'équipe *radio* ne veut pas les alertes de liens, l'équipe *transport* pas celles des sites.
**Prérequis** : Lab 09.1

### Étapes
1. **Alerting → Notification configuration** → onglet **Contact points** → **New contact point** :
   - `Equipe radio`, intégration **Email**, adresse `radio@telcea.example` → **Test** → **Send test notification** → **Save contact point**
   - `Equipe transport` → `transport@telcea.example`
   - `NOC Telcea` → `noc@telcea.example`
2. Ouvrir Mailpit (`/mail/`) : 3 courriels de test reçus.
3. Onglet **Notification policies** : ligne **Default policy** → **More → Edit** → **Default contact point** `NOC Telcea` → enregistrer.
4. Ligne **Default policy** → **Add route** : matcher `equipe` `=` `radio` → **Contact point** `Equipe radio`. Idem `equipe = transport` → `Equipe transport`.
   Résultat attendu : **Default policy · 2 routes**, branches `equipe = radio` (*Delivered to Equipe radio*) et `equipe = transport`.

### Critères de réussite
- [ ] 3 courriels de test dans Mailpit, chacun à la bonne adresse
- [ ] Deux politiques enfants, matchers `equipe=radio` et `equipe=transport`

---

## Exercice 09.3 ⭐⭐ — La tempête en Bretagne (semi-autonome)
**Durée** : 25 min · **Objectif** : créer les 2 règles manquantes, vivre l'incident, vérifier le routage
**Contexte** : 13 h 45, une tempête frappe la Bretagne (déclenchée par la formatrice) : sites coupés, bascule sur batterie, lien de collecte saturé.

**Énoncé** :
1. Avant 13 h 45, créer dans le groupe `telcea-1m` :
   - `Lien de collecte sature` : utilisation d'un lien > 80 % pendant 2 min, labels `equipe=transport`, `severite=majeure`, résumé citant le lien ;
   - `Site sur batterie` : `telcea_site_on_battery` > 0 pendant 1 min, labels `equipe=radio`, `severite=mineure`.
2. Pendant la tempête : suivre les états dans **Alert rules** (Normal → Pending → Firing) et noter l'heure de chaque passage.
3. Relever dans Mailpit : destinataire et objet de chaque notification ; vérifier qu'aucun courriel de liens n'est arrivé à `radio@` (et inversement).
4. Observer l'écran national : State timeline, carte, Status Panel.

**Indices** :
- Utilisation des liens : requête de l'exercice 03.3 (question 5), à regrouper `by (link, region)` pour garder les labels utiles dans le message
- Délais : intervalle d'évaluation + pending + `group_wait` (30 s) avant le courriel
- Le lien sature en quelques minutes (moyenne sur 5 min)

**Critères de réussite** :
- [ ] Tableau horodaté des états des 3 règles
- [ ] Courriels « Site radio hors service » et « Site sur batterie » chez `radio@`, « Lien de collecte sature » chez `transport@`

---

## Défi 09.4 ⭐⭐⭐ — Silence et Alertmanager externe (autonome)
**Durée** : 15 min · **Objectif** : suspendre une notification et relier Grafana à l'Alertmanager de Prometheus
**Contexte** : une équipe d'intervention part sur BRE-01 ; par ailleurs, Prometheus porte déjà une règle `SiteRadioHorsService` routée par son propre Alertmanager.

**Énoncé** :
- Créer un silence de 2 h sur `site=BRE-01` avec le commentaire `Intervention alimentation`, et vérifier que BRE-01 ne génère plus de courriel alors que QUI-01 continue.
- Ajouter une source de données **Alertmanager** (`http://alertmanager:9093`, implémentation Prometheus) et retrouver, dans Grafana, l'alerte `SiteRadioHorsService` émise par Prometheus.
- Comparer dans Mailpit les courriels envoyés par Grafana et par Alertmanager (expéditeur, objet).

**Critères de réussite** :
- [ ] Silence actif, visible dans **Silences**, alerte BRE-01 marquée suspendue
- [ ] Alertes de l'Alertmanager visibles dans Grafana
- [ ] Deux expéditeurs identifiés : `grafana@telcea.example` et `alertmanager@telcea.example`

---

## Pour aller plus loin — Définir ses propres alertes
Reprise de l'atelier historique (« liste des alertes pertinentes ») : pour 3 indicateurs de son propre périmètre, définir seuil, durée, équipe destinataire et justification (ex. CPU d'ESX > 70 % → administrateurs vCenter ; trafic sortant anormal → équipe sécurité).
