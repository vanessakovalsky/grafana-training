# Exercice 3 - Créer votre propre tableau de bord et installer un plugin

## Pré-requis
- Avoir accès à Grafana 
- Avoir configurer un tableau de bord

## Installation des plugins

- Nous allons choisir et installer un plugin de Grafana.

### Via l'interface graphique

- L'installation des plugins peut être faite directement dans l'UI de Grafana
- Dans le menu de Grafana, ouvrir `Administratipn`,puis cliquer sur `Modules complémentaires`,  puis cliquer sur `Plugins`
- Vous accédez alors à la liste des plugins (ceux installé et ceux disponibles)
- Vous pouvez choisir un plugin et l'installé


### Via le CLI de grafana
- Se connecter en SSH sur la machine de grafana
- Pour lister les plugins disponibles :
```
grafana-cli plugins list-remote
```
- Pour installer un plugin utiliser la commande : 
```
plugins install <plugin-id>
```
## Atelier — "Concevez votre tableau de bord Grafana"

Durée : 45 min | Format : binômes | Niveau : après avoir vu les bases de Grafana (sources de données, panels, requêtes)

## Déroulé

1. Cadrage du cas d'usage 
Chaque binôme choisit (ou utilise un des siens) un cas d'usage parmi la liste suivante :

* Supervision d'une flotte de VMs/conteneurs (CPU, mémoire, réseau)
* Suivi de pipelines CI/CD (durée des builds, taux d'échec)
* Monitoring applicatif métier (latence API, taux d'erreur, volumétrie)
* Suivi géographique/embarqué (positions, capteurs, IoT)
* Suivi business (ventes, commandes, KPIs)

Répondre à 3 questions :

* Qui va regarder ce dashboard, et pour quelle décision ?
* Quelles sont les 3 à 5 métriques indispensables ?
* Quelle fréquence de rafraîchissement / plage temporelle a du sens ?

2. Maquette du dashboard (10 min)
Sur papier, tableau blanc ou un outil simple (Excalidraw, Miro, ou juste une feuille), le binôme dessine la disposition envisagée : combien de panels, quel type par métrique (time series, gauge, stat, table, heatmap...), organisation en lignes/sections.

Contrainte volontaire : ils doivent identifier au moins un besoin que les panels standards de Grafana ne couvrent pas bien (carte géographique, diagramme de flux, visualisation métier spécifique, etc.) — c'est ce qui amène naturellement vers l'étape plugin.

3. Chasse au plugin (15 min)
Le binôme se rend sur le [catalogue officiel Grafana](https://grafana.com/grafana/plugins/) et cherche un plugin panel/datasource répondant au besoin identifié à l'étape 2.

Grille pour évaluer le plugin trouvé (à documenter) :

* Nom du plugin et éditeur
* Est-il "Officially released" / signé, ou communautaire ?
* Date de dernière mise à jour et compatibilité version Grafana
* Ce qu'il apporte concrètement par rapport à un panel natif
* Un point de vigilance (installation, licence, dépendance à un service externe, etc.)

4. Restitution flash (10 min)
Tour de salle rapide : 1-2 min par binôme pour présenter leur cas d'usage, leur maquette, et le plugin retenu. Les autres participants peuvent réagir ou suggérer une alternative s'ils connaissent un autre plugin pertinent.
