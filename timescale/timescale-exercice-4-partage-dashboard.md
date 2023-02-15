# Exercice 4 - Partage du tableau de bord

## Pré-requis

* Avoir fais les exercices précédents


## Partage d'un Panel

* Créer un panel qui affiche le nombre de conteneurs
* Enregistrer ce panel dans la Library 
* Créer un nouveau Dashboard et utiliser votre panel depuis la Library
* Partager un instantané du panel avec un autre stagiaire et la formatrice par mail

## Partage du tableau de bord

* Exporter votre dashboard des exercices précédents, et mettre le fichier json récupéré dans Teams
* Récupérer un tableau de bord partagé par une autre personne et importé le dans votre propre Grafana

## Définition d'une variable

* Ajouter à votre tableau de bord une variable permettant de filtrer les données pour un type de paiement.
* Pour cela déclarer votre variable dans les paramètres du Dashboard, menu Variables.
* Cliquer sur New 
* Choisir un nom de variable, puis le type de variable (ici nous choisissons Query pour récupérer une liste dynamique des moyens de paiement). Dans la requête nous utilisons la requêtes suivante pour lister les moyens de paiement : 
```
SELECT payment_type FROM payment_types;
```
* Ensuite vous définissez les options à appliquer 

![](https://assets.iobeam.com/images/docs/screenshots-for-grafana-tutorial/grafana_define_variable.png)

* La variable apparaît alors en haut du tableau de bord.

## Utiliser la variable dans ses requêtes

* Puis utiliser cette variable dans vos requêtes pour chacun de vos panels afin de filtrer les données, on ajoute entre accolade le nom du paramètre de filtre suivi de = et le nom de la variable précédé par le symbole dollar.

Exemple : 
La requête : 
```
SELECT
  --1--
  time_bucket('5m', pickup_datetime) AS time,
  --2--
  COUNT(*)
FROM rides
WHERE $__timeFilter(pickup_datetime)
GROUP BY time
ORDER BY time
```

Deviendra : 
```
SELECT
  --1--
  time_bucket('5m', pickup_datetime) AS time,
  --2--
  COUNT(*)
FROM rides
WHERE $__timeFilter(pickup_datetime)
AND rides.payment_type IN ($payment_type)
GROUP BY time
ORDER BY time
```
- Il est alors possible de répeter un panel pour chaque valeur de variable, dans les paramètres du panel, ouvrir Repeating et paramètrer comme sur l'image ci-dessous

![](https://assets.iobeam.com/images/docs/screenshots-for-grafana-tutorial/grafana_create_dynamic_panels.png)


* Reprenez les requêtes que nous avons utiliser dans les différents graphs, et ajouter l'utilisation de la variable payment_type que vous avez créé sur les graphiques

* Puis changer le type de paiement sélectionné et observé la modification des graphiques


## Pour aller plus loin - Définir ses propres variables

* Selon vous, pour votre propre problématique de monitoring, certaines variables seraient elles nécessaires ?
* Sont elles statiques ou dynamiques ? 
* Dans le cas où elles sont dynamiques, pouvez vous écrire la requêtes pour récupérer votre liste dynamique ?
