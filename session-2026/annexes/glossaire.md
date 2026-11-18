# Glossaire

## A
- **Alert rule (règle d'alerte)** : requête + condition + évaluation ; produit une instance d'alerte par série en anomalie (M09).
- **Alertmanager** : composant de l'écosystème Prometheus qui regroupe, route et envoie les notifications ; utilisable comme point de contact ou comme source dans Grafana (M09).
- **Alloy (Grafana Alloy)** : collecteur de Grafana Labs (métriques, journaux, traces) ; dans la stack, collecte les journaux des conteneurs vers Loki.
- **Angular (AngularJS)** : ancien cadre des plugins ; plugins Angular retirés en Grafana 12 (Boom Table, Worldmap).
- **Annotation (règle d'alerte)** : texte informatif d'une alerte (résumé, procédure), sans effet sur le routage.

## C
- **Compte de service (service account)** : identité technique pour les scripts et outils, avec jetons révocables (M10).
- **Contact point (point de contact)** : destination d'une notification (courriel, Teams, Slack, webhook, Alertmanager) (M09).
- **Counter (compteur)** : métrique qui ne fait que croître (`_total`) ; s'exploite avec `rate()` (M03).

## D
- **Dashboard (tableau de bord)** : ensemble de panels, lignes, onglets et variables partageant une plage de temps (M04).
- **Data frame** : format tabulaire commun (champ temps + champs de valeurs) échangé entre sources et visualisations.
- **Data source (source de données)** : configuration permettant à Grafana d'interroger une base (plugin + URL + authentification) (M03).
- **Dossier (folder)** : regroupement de tableaux de bord et de règles ; porte les permissions (M06, M10).

## G
- **Gauge (jauge)** : métrique qui monte et descend (ex. abonnés connectés) ; aussi visualisation en cadran (M05).
- **Geomap** : visualisation cartographique (marqueurs placés par latitude / longitude) (M05).

## H
- **Histogram (histogramme)** : métrique répartie en tranches (`_bucket`, étiquette `le`) ; centiles avec `histogram_quantile()`.

## I
- **InfluxDB 3 Core** : base de séries temporelles interrogée en SQL (InfluxQL possible) ; données système de la VM dans la stack.
- **Instance (d'alerte)** : occurrence d'une règle pour une série donnée (ex. `site=BRE-01`).

## L
- **Label (étiquette)** : couple clé = valeur qui qualifie une série (`region="Bretagne"`) ou une alerte (`equipe="radio"`).
- **Library panel** : panel partagé entre plusieurs tableaux de bord, maintenu une seule fois (M08).
- **Lien externe (share externally)** : accès en lecture seule à un tableau de bord sans compte Grafana (ex-« public dashboard ») (M08).
- **Loki** : base de journaux de Grafana Labs, interrogée en LogQL.

## M
- **Mixed (source)** : pseudo-source permettant plusieurs sources dans un même panel (M11).
- **Mute timing** : plage horaire récurrente sans notification (nuit, week-end).

## N
- **NOC (Network Operations Center)** : centre de supervision du réseau, 24 h / 24.
- **Notification policy (politique de notification)** : arbre de routage des alertes selon leurs labels (M09).

## O
- **Organisation** : espace cloisonné d'une instance Grafana (utilisateurs, sources, tableaux de bord).
- **Override** : réglage d'affichage appliqué à un champ précis d'un panel (M05).

## P
- **Panel** : bloc d'un tableau de bord = requêtes + transformations + visualisation.
- **Pending period (période d'attente)** : durée pendant laquelle la condition doit rester vraie avant l'alerte.
- **Plugin** : extension de Grafana (panel, source de données, application) (M07).
- **PromQL** : langage de requête de Prometheus.
- **Prometheus** : base de métriques à collecte *pull* (lecture périodique des cibles `/metrics`).
- **Provisioning** : configuration de Grafana par fichiers YAML lus au démarrage (M02).
- **Pull / push** : la base lit les cibles (*pull*, Prometheus) ou les agents écrivent dans la base (*push*, Telegraf).

## R
- **Repeat (panel répété)** : copie automatique d'un panel pour chaque valeur d'une variable (M06).
- **Rôle d'organisation** : Viewer, Editor, Admin (ou aucun rôle de base) (M10).

## S
- **Seuil (threshold)** : valeur qui fait changer la couleur ou l'état d'une donnée (M05).
- **Signature (plugin)** : garantie de l'éditeur et de l'intégrité du code d'un plugin (M07).
- **Silence** : suspension ponctuelle des notifications d'alertes correspondant à des labels (M09).
- **Snapshot** : copie figée d'un tableau de bord (données affichées, sans requêtes) (M08).

## T
- **Telegraf** : agent de collecte d'InfluxData (*push*) ; mesures système de la VM vers InfluxDB.
- **Transformation** : traitement des résultats de requêtes avant affichage (jointure, calcul, renommage) (M11).

## V
- **Value mapping** : remplacement d'une valeur par un texte et une couleur (`1` → « En service ») (M05).
- **Variable** : liste de valeurs en haut du tableau de bord, insérée dans les requêtes par `$nom` (M06).
