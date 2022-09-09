# Exercice 3 - Utilisation des plugins

## Pré-requis
- Avoir accès à Grafana 
- Avoir configurer un tableau de bord

## Installation des plugins

- Pour l'exercice nous avons besoin des plugins suivant :
  - Boom Table

### Via l'interface graphique
- L'installation des plugins peut être faite directement dans l'UI de Grafana
- Dans le menu de Grafana, ouvrir `Configuration`, puis cliquer sur `Plugins`
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


## Utilisation des plugins

### Boom Table
- Ajouter un panel à votre tableau de bord qui permet d'afficher dans un tableau : 
  - Une ligne par conteneur
  - Une colonne CPU Usage
  - Une colonne Memory Usage
  - Une colonne Disk Usage






## Aller plus loin -  Sélection de plugins

- Trouver un ou plusieurs plugins qui seraient utiles à ajouter dans Grafana pour répondre à votre problèmatique de monitoring
- Quels sont, selon vous les critères à prendre en compte pour le choix d'un plugin ?
