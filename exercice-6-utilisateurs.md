# Exercice 6 - Utilisateurs

## Pré-requis

* Avoir accès à Grafana en administrateur


## Ajout d'Utilisateurs

* Pour ajouter un utilisateur, rendez-vous dans le menu `Administration > Users`
* Puis cliquer sur `+ Invite`
![](https://static.les-enovateurs.com/uploads/2019/02/Grafana-Cr%C3%A9er-un-utilisateur.png)
* Vous pouvez alors inviter une autre personne du groupe et votre formatrice en saisissant une adresse email et un nom, ainsi qu'un rôle

## Gestion des équipes

* Toujours dans l'écran de configuration, cliquer sur l'onglet `Teams`
* Vous voyez alors la liste des équipes (vide par défaut)
![](https://static.les-enovateurs.com/uploads/2019/02/Grafana-Cr%C3%A9ation-dune-%C3%A9quipe.png)
* Les équipes permettent de regrouper les utilisateurs et d'assigner des permissions à cet équipe plutôt que individuellement pour chaque utilisateur
* Créer une équipe appelé formation (l'adresse email permet d'associer un avatar à l'équipe depuis le site gravatar.com )
![](https://static.les-enovateurs.com/uploads/2019/02/Grafana-Nouvelle-%C3%A9quipe.png)
* Ajouter les utilisateurs que vous avez créé à l'étape précédente dans votre équipe Formation
![](https://static.les-enovateurs.com/uploads/2019/02/Grafana-une-nouvelle-%C3%A9quipe-cr%C3%A9e.png)

## Permissions sur un tableau de bord

* Aller sur le tableau de bord que vous avez créé
* Entrer dans les paramètres du tableau de bord (via l'icône de roue cranté en haut à droite), puis cliquer sur le menu à Gauche `Permissions`
![](https://static.les-enovateurs.com/uploads/2019/02/Grafana-Gestion-des-permissions-sur-un-tableau-de-bord.png)
* La liste des permissions par rôle s'affiche
* Vous pouvez alors via le bouton `+ Add permission`, ajouter une permission soit à une équipe soit à un utilisateur : 
![](https://static.les-enovateurs.com/uploads/2019/02/Grafana-Ajout-dune-permission.png)
* Ajouter la permission de visualiser le tableau de bord à l'équipe Formation que vous avez créé
* Demander à une autre personne de l'équipe de se connecte et de visualiser le tableau de bord

## Permissions sur un dossier

* Revenir à la page d'accueil (Home)
* Créer un dossier et mettre une copie de votre tableau de bord à l'intérieur, en lui donnant un nouveau nom
* Sur la page d'accueil, en passant sur le nom du dossier, vous verrez apparaître la roue cranté permettant d'accéder aux paramètres du dossier
![](https://static.les-enovateurs.com/uploads/2019/02/Grafana-Permissions-sur-un-Dossier.png)
* Vous retrouvez alors le menu permissions et le même fonctionnement que pour un tableau de bord.
* Ajouter cette fois-ci une permission à seul utilisateur de voir le contenu du dossier. 