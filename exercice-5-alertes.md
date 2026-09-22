# Exercice 5 - Alertes

## Pré-requis

* Avoir un tableau de bord configuré dans Grafana
* Avoir créer un dossier dans les dashboard

### Objectif
À la fin de l'atelier, chaque participant a créé une règle d'alerte fonctionnelle, un point de contact, et compris comment le routage des notifications se déclenche.

### Contexte technique 

Depuis Grafana 12, le **Grafana-Managed Alerting** est la méthode par défaut (les alertes gérées côté datasource — Prometheus/Loki — restent possibles mais ne sont plus le mode par défaut). La navigation Alerting a aussi été réorganisée en 4 zones : **Alert rules**, **Alert activity** (Alerts + Active notifications), **Notification Configuration** (Contact points, Notification policies, Time intervals, Templates), et **Groups**.

---

### Étape 1 — Explorer la navigation Alerting (5 min)

Ouvrir le menu **Alerting** dans la sidebar et de repérer les 4 sous-menus.
Sans cliquer encore, où vous iriez pour : voir les alertes qui se déclenchent en ce moment, configurer un canal Slack/email, et créer une nouvelle règle.

### Étape 2 — Créer une règle d'alerte (15 min)

Aller dans **Alert rules → New alert rule**.

1. **Nommer la règle** de façon explicite (ex : `cpu-high-webserver`)
2. **Définir la requête** : choisir la source de données et écrire la requête qui retourne la métrique à surveiller (ex : CPU > seuil, taux d'erreur HTTP, etc.)
3. **Définir la condition d'alerte** : seuil (`WHEN query IS ABOVE 80`), avec la fenêtre d'évaluation
4. **Configurer l'évaluation** :
   - Rattacher la règle à un *evaluation group* (fréquence d'évaluation, ex : toutes les 1 min)
   - Définir le `pending period` (durée pendant laquelle la condition doit rester vraie avant de passer à *Firing*)
5. **Ajouter des labels** (ex : `severity=critical`, `team=infra`) — c'est ce qui servira au routage à l'étape suivante
6. **Ajouter des annotations** (résumé, description, lien runbook) pour enrichir la notification

Consigne pratique à donner : "Testez votre requête et regardez l'état de la règle passer de *Normal* à *Pending* à *Firing* si vous forcez la condition."

### Étape 3 — Créer un point de contact (10 min)

Aller dans **Notification Configuration → Contact points → Add contact point**.

1. Choisir l'intégration (email, Slack, webhook, Teams...)
2. Renseigner les paramètres (adresse, webhook URL, etc.)
3. Utiliser le bouton **Test** pour envoyer une notification factice et vérifier la réception

### Étape 4 — Configurer la politique de notification (10 min)
Aller dans **Notification Configuration → Notification policies**.

1. Observer la politique par défaut (root policy)
2. Créer une politique imbriquée basée sur les labels définis à l'étape 2 (ex : si `severity=critical` → contact point Slack ; sinon → contact point email)
3. Expliquer le principe de **matching** par labels et l'héritage entre politique racine et sous-politiques

Optionnel si le temps le permet : configurer un **time interval** (ex : ne pas notifier la nuit) et le rattacher à la politique.

### Étape 5 — Déclencher et observer (10 min)
1. Forcer la condition d'alerte à devenir vraie (modifier le seuil temporairement, ou générer de la charge si l'environnement le permet)
2. Aller dans **Alert activity → Alerts** pour voir l'alerte passer par les états `Pending` → `Firing`
3. Vérifier la réception de la notification sur le canal configuré
4. Consulter **Alert activity → Active notifications** puis, si disponible dans votre version, l'historique des notifications pour voir le détail de l'envoi (contact point utilisé, succès/échec)


## Pour aller plus loin - Définir ses propres alertes

* Pour chacun des éléments que vous avez choisi de monitorer, définir les seuils qui doivent déclencher des alertes
* Une fois les seuils définis, créer les alertes et les notifications associées
