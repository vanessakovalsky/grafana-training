# Module 09 — Exercices

Parcours essentiel = Labs 09.1, 09.2 et 09.3 (tout le groupe). Défis = facultatifs, en cas d'avance.
Courriels : boîte de test Mailpit de la VM, `https://stagiaire<NN>.<SESSION>.kovalibre-labs.com/mail/` (aucun courriel ne sort de la VM).

## Lab 09.1 ⭐ — Première règle : site radio hors service (guidé)
**Durée** : 20 min · **Objectif** : créer la règle « Site radio hors service »
**Contexte** : la nuit, personne ne regarde l'écran du NOC ; une coupure de site doit être signalée automatiquement à l'équipe *radio*.
**Prérequis** : source `prometheus`, dossier `NOC Telcéa`

### Étapes
1. **Alerting → Alert rules → New alert rule**.
2. Section 1 : **Name** `Site radio hors service`.
3. Section 2 : source `prometheus`, mode **Code**, copier-coller la requête :
   ```promql
   telcea_site_up
   ```
   **Options → Type** : `Instant`.
4. **Alert condition** : WHEN QUERY **IS BELOW** `1` → bouton **Preview alert rule condition**.
   Résultat attendu : 12 instances `Normal` (une par site).
5. Section 3 : **Folder** `NOC Telcéa` ; **Add labels** : `equipe` = `radio`.
6. Section 4 : **New evaluation group** `telcea-1m`, intervalle `1m` ; **Pending period** `1m`.
7. Section 5 : laisser le routage par politique de notification (configuré au Lab 09.2).
8. **Save** (bas de page).
   Résultat attendu : règle dans **Alert rules**, état `Normal`.

### Si bloqué
Règles, points de contact et routage créés par la formatrice (rattrapage, 5 s) : reprise au Lab 09.3.

### Critères de réussite
- [ ] Règle enregistrée, 12 instances `Normal`, label `equipe=radio`

---

## Lab 09.2 ⭐ — Points de contact et routage par équipe (guidé)
**Durée** : 20 min · **Objectif** : chaque équipe reçoit uniquement ses alertes, le NOC reçoit le reste
**Contexte** : l'équipe *radio* ne veut pas les alertes de liens, l'équipe *transport* pas celles des sites.
**Prérequis** : Lab 09.1

### Étapes
1. **Alerting → Notification configuration** → onglet **Contact points** → **New contact point** :
   **Name** `Equipe radio`, intégration **Email**, adresse `radio@telcea.example` → **Save contact point**.
2. Idem : `Equipe transport` → `transport@telcea.example` ; `NOC Telcea` → `noc@telcea.example`.
3. Onglet **Notification policies** : ligne **Default policy** → **More → Edit** → **Default contact point** `NOC Telcea` → enregistrer.
4. Ligne **Default policy** → **Add route** : matcher `equipe` `=` `radio` → **Contact point** `Equipe radio` → enregistrer.
5. Idem : `equipe` `=` `transport` → `Equipe transport`.
   Résultat attendu : **Default policy · 2 routes**.

### Critères de réussite
- [ ] 3 points de contact
- [ ] Deux routes, matchers `equipe=radio` et `equipe=transport`

---

## Lab 09.3 ⭐ — La tempête en Bretagne (observation)
**Durée** : 15 min · **Objectif** : voir une alerte se déclencher et arriver chez la bonne équipe
**Contexte** : une tempête frappe la Bretagne (déclenchée par la formatrice) : sites coupés, bascule sur batterie, lien de collecte saturé.
**Prérequis** : Labs 09.1 et 09.2 (ou rattrapage)

### Étapes
1. Au signal de la formatrice : **Alerting → Alert rules**, règle `Site radio hors service`.
   Résultat attendu : états `Normal` → `Pending` (1 à 2 min) → `Firing` (2 à 3 min) pour les sites bretons coupés ; courriel en 3 à 4 min.
2. Ouvrir Mailpit (`/mail/`).
   Résultat attendu : courriel « Site radio hors service » adressé à `radio@telcea.example`.
3. Ouvrir `[TLC] Réseau — Vue nationale` : repérer les sites `Hors service` dans le tableau `État des sites`.

### Critères de réussite
- [ ] Alerte `Firing` observée
- [ ] Courriel reçu par `radio@`, aucun par `transport@`

---

## Défis facultatifs (en cas d'avance)

## Défi 09.2b ⭐⭐ — Tester et documenter les alertes
**Durée** : 10 min
**Énoncé** :
1. Sur chaque point de contact : **Test** → **Send test notification** ; 3 courriels de test dans Mailpit.
2. Règle `Site radio hors service` : ajouter le label `severite` = `critique` et le résumé (section 6, **Summary**) : `Site {{ $labels.site }} ({{ $labels.region }}) hors service`.

**Critères de réussite** :
- [ ] 3 courriels de test, chacun à la bonne adresse
- [ ] Courriel de la tempête citant le site et la région

---

## Défi 09.3 ⭐⭐ — La tempête en Bretagne : deux règles de plus
**Durée** : 25 min · **Objectif** : créer les 2 règles manquantes, vivre l'incident, vérifier le routage
**Contexte** : 14 h 20, une tempête frappe la Bretagne (déclenchée par la formatrice) : sites coupés, bascule sur batterie, lien de collecte saturé.

**Énoncé** :
1. Avant 14 h 20, créer dans le groupe `telcea-1m` :
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
