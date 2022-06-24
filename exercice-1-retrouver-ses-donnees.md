# Exercice 1 - Retrouver ses données

## Pré-requis

- Avoir accès à l'interface graphique de Grafana
- Avoir une base de données de métriques

## Présentation 

- Un projet web contenant une application en PHP et une base de données MariaDB sont déployées dans des conteneurs
- Des métriques sont récupérées de ces conteneurs avec le collecteur CAdvisor et stocker dans une base Prométheus

## Ajouter une source de données à Grafana

- Dans Grafana, ouvrir le menu, puis dans l'item `Configuration`, cliquer sur Data sources
- Vous arrivez alors sur la liste des sources de données
- Pour ajouter une source de données, cliquer sur `Add data source`
- Dans la catégorie `Time serie base`, Choisir `Prometheus` 
- Vous arrivez alors sur une page de paramètrage
- Le seul paramètre obligatoire est alors l'adresse de Prometheus, à renseigner avec l'adresse qui vous a été fournie pendant la formation
- Les autres paramètres permettent par exemple de configurer une authentification, dans le cas où l'accès à Prometheus est protégé (ce n'est pas le cas dans le cadre de la formation)
- Cliquer en bas de la page sur `Save and test`
- Vous devriez obtenir un message `Data source is working`, dans le cas contraire, vérifier l'adresse saisie et les paramètres que vous avez modifié (il n'est pas nécessaire dans le cadre de la formation de modifier les paramètres)
- Vos données sont maintenant accessibles depuis Grafana

## Explorer les données

- Dans le menu de Grafana, cliquer sur Explore
- Tout en haut à côté du titre `Explore` vous pouvez sélectionner votre source de données
- Puis en selectionnant votre source Prometheus, vous pouvez faire des requêtes pour afficher les données disponibles.
- Pour connaitre la liste des données vous pouvez cliquer sur la flèche en dessous de Metrics, cela vous permet de voir les métriques qui sont disponibles dans votre source de donnéess.

## Définir ses indicateurs et les requêtes associées

- Dans notre contexte, nous voulons surveiller les conteneurs qui hébergent notre application.
- Quels sont selon vous les métriques nécessaires à surveiller pour cela ?
- A l'aide de la [documentation de PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/) (le langage de requête de Prometheus) définir les requêtes qui vous permettent d'obtenir les métriques à surveiller pour nos conteneurs.
 
