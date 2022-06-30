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
* Partager un lien par mail de votre dashboard avec tous en mettant le lien sur Teams (on ne pourra pas accéder à ce lien, tant que nous ne pourrons pas nous connecter avec un compte utilisateur sur votre Grafana)
* Récupérer un tableau de bord partagé par un autre stagiaire et importé le dans votre propre Grafana

## Définition d'une variable

* Ajouter à votre tableau de bord une variable permettant de filtrer les données pour un ou plusieurs conteneurs parmi les différents conteneurs disponibles.
* Pour cela déclarer votre variable dans les paramètres du Dasboard, menu Variables.
* Cliquer sur New 
* Choisir un nom de variable, puis le type de variable (ici nous choisissons Query pour récupérer une liste dynamique de nom de container)
* Ensuite vous définissez le filtre à appliquer 

![](../img/exo4/add_variable.png)
* Puis utiliser cette variable dans vos requêtes pour chacun de vos panels afin de filtrer les données

![](../img/exo4/variable_query.png)
