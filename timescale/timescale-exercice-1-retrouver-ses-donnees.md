# Exercice 1 - Retrouver ses données

## Pré-requis

- Avoir accès à l'interface graphique de Grafana
- Avoir une base de données Timescale avec des données

## Présentation 

- Une base de données qui contient les données des voyages de Taxi à New York City
- Nous allons au fur et à mesure des exercices construire un tableau de bord qui ressemblera à celui-ci :

![](img/timescale/exo1/dashboard_cible.png)

## Ajouter une source de données à Grafana

- Dans Grafana, ouvrir le menu, puis dans l'item `Configuration`, cliquer sur Data sources
- Vous arrivez alors sur la liste des sources de données
- Pour ajouter une source de données, cliquer sur `Add data source`
- Dans la catégorie `SQL`, Choisir `PostgreSQL` 
- Vous arrivez alors sur une page de paramètrage
- Nous devons alors renseigner les paramètres suivants : 
    - Name : NYC Taxi trips
    - Host : timescaledb:5432
    - Database: data
    - User: timescale
    - Password: timescaledb
    - TLS/SSL Mode : Disable
    - Tous les autres paramètres sont laissés avec leur option par défaut
- Cliquer en bas de la page sur `Save and test`
- Vous devriez obtenir un message `Database Connection OK`, dans le cas contraire, vérifier l'adresse saisie et les paramètres que vous avez modifié (il n'est pas nécessaire dans le cadre de la formation de modifier les paramètres)
- Vos données sont maintenant accessibles depuis Grafana

## Explorer les données

- Dans le menu de Grafana, cliquer sur Explore
- Tout en haut à côté du titre `Explore` vous pouvez sélectionner votre source de données
- Puis en sélectionnant votre source `NYC Taxi trips`, vous pouvez faire des requêtes pour afficher les données disponibles.
- Pour connaître la liste des données vous pouvez cliquer les éléments du constructeur de requête : table et column notamment pour connaitre la structure
- Pour exécuter une requête, cliquer sur `Run Query` à droite.


## Définir les requêtes pour suivre les déplacements de taxi

- Nous avons des données sur le déplacement et le paiement des voyages en Taxi à NYC.
- Pour chaque élément nous vous donnons la requête brute à executer, vous pouvez également construire ces requêtes à l'aide du constructeur de requête
- Nous allons donc suivre le nombre de courses par jour : 
```
SELECT
  --1--
  time_bucket('1 day', pickup_datetime) AS time,
  --2--
  COUNT(*)
FROM rides
WHERE $__timeFilter(pickup_datetime)
GROUP BY time
ORDER BY time
```
* Attention les données datant de 2016, il est nécessaire en haut à droite de choisir une plage de date en 2016
- Nous allons également suivre les courses en fonction de leur distance qui sera supérieur à 5 miles de Manhattan
```
SELECT time_bucket('5m', rides.pickup_datetime) AS time,
       rides.trip_distance AS value,
       rides.pickup_latitude AS latitude,
       rides.pickup_longitude AS longitude
FROM rides
WHERE $__timeFilter(rides.pickup_datetime) 
GROUP BY time,
         rides.trip_distance,
         rides.pickup_latitude,
         rides.pickup_longitude
ORDER BY time
LIMIT 50;
```
- Et aussi une requête pour récupérer les moyens de paiement (qui nous servira a rendre notre tableau dynamique avec une variable)
```
SELECT payment_type FROM payment_types;
```
* Chacune de ces requêtes nous permet de récupérer des informations sur les courses afin de construire notre tableau de bord.
* Lors de l'exécution de ses requêtes, vous obtiendrez des graphique de résultats regroupés par interval de temps pour chaque conteneur comme celui ci-dessous

![](img/exo1/result_explore.png)

## Pour aller plus loin - Définir ses indicateurs et les requêtes associées

- Définir dans votre contexte ce que vous souhaitez monitorer 
- Quels sont selon vous les données intéressantes à suivre ?
- Quels sont les requêtes SQL correspondantes à la récupération de ces données ?
