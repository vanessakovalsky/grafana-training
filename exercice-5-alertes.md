# Exercice 5 - Alertes

## Pré-requis

* Avoir un tableau de bord configuré dans Grafana

## Création d'une alerte

### Définir le seuil
* Sur votre dashboard, choisir le panel qui affiche le trafic réseau entrant
* Ouvrir votre Panel en modification, puis sélectionner l'onglet `Alert`
* Puis cliquer sur `Create Alert`

![](https://static.les-enovateurs.com/uploads/2019/02/Grafana-nouvelle-alerte.png)

* Choisir maintenant la valeur `count` dans la liste déroulante `When`
* Définir une valeur à 5
* Dans La section `If no data or all values are null` choisir `Ok`

### Définir la notification

* Cliquer à gauche sur `Notifications`
* Puis choisir d'envoyer un mail à votre propre adresse email
![](https://static.les-enovateurs.com/uploads/2019/02/Grafana-Liaison-de-service-avec-une-alerte.png)

* Vous pouvez ajouter d'autres notifications en appuyant sur le bouton `+`

### Tester votre alerte

* Ouvrir dans plusieurs onglets l'application web en moins de 5 minutes
* Cela devrait alors déclencher l'alerte et vous envoyer un email.

## Définir ses propres alertes

* Pour chacun des éléments que vous avez choisi de monitorer, définir les seuils qui doivent déclencher des alertes
* Une fois les seuils définis, créer les alertes et les notifications associées