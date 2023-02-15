# Exercice 3 - Utilisation des plugins

## Pré-requis
- Avoir accès à Grafana 
- Avoir configurer un tableau de bord

## Installation des plugins

- Pour l'exercice nous avons besoin des plugins suivant :
  - Worldmap Panel

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


## Utilisation du plugin Worldmap Panel
### Création du panel et des requêtes
- Ajouter un panel à votre tableau de bord qui permet d'afficher dans sur une carte les courses de taxi

Ce qui donne un tableau récapitulatif comme celui-ci dessous: 

![](https://assets.iobeam.com/images/docs/screenshots-for-grafana-tutorial/grafana_worldmap_query_results.png)

- Pour cela créer un nouveau Panel
- Puis créer les deux requêtes ci dessous :
```
SELECT time_bucket('5m', rides.pickup_datetime) AS time,
       rides.trip_distance AS value,
       rides.pickup_latitude AS latitude,
       rides.pickup_longitude AS longitude
FROM rides
WHERE $__timeFilter(rides.pickup_datetime) AND
  ST_Distance(pickup_geom,
              ST_Transform(ST_SetSRID(ST_MakePoint(-73.9851,40.7589),4326),2163)
  ) < 2000
GROUP BY time,
         rides.trip_distance,
         rides.pickup_latitude,
         rides.pickup_longitude
ORDER BY time
LIMIT 500;
```

### Mise de la carte
- En haut à droite, choisir le type de graph `Worldmap Panel`
- Pour le titre, définir  `Carte des courses` (ou le titre de votre choix)
- Ensuite pour définir ce qui est affiché nous allons utilisés les options
  Dans le bloc Map Visual Option
  - Min Circle Size : `1`
  - Max Circle Size : `5`
  Dans le bloc Map Data Options :
  - Location Data: `table`
  - Aggregation : `current`
  Dans le bloc Field Mapping:
  - Table Query Format : coordinates
  - Metric Field : value
  - Lattitude field : lattitude
  - Longitude field: longitude
  Dans le bloc Thresholds : 
  - Thresholds : `2,5,10`

- Pensez à enregistrer votre Panel

N'hésitez pas à aller consulter sa documentation pour connaître ses autres possibilités et options : https://github.com/grafana/worldmap-panel

## Aller plus loin -  Sélection de plugins

- Trouver un ou plusieurs plugins qui seraient utiles à ajouter dans Grafana pour répondre à votre problèmatique de monitoring
- Quels sont, selon vous les critères à prendre en compte pour le choix d'un plugin ?
