# Exercice 5 - Utilisation des plugins

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


### Via le CLI de grafana (si vous avez accès en SSH à la machine)
- Se connecter en SSH sur la machine de grafana
- Pour lister les plugins disponibles :
```
grafana-cli plugins list-remote
```
- Pour installer un plugin utiliser la commande : 
```
plugins install <plugin-id>
```


## Utilisation du plugin Boom Table

### Création du panel et des requêtes
- Ajouter un panel à votre tableau de bord qui permet d'afficher dans un tableau : 
  - Une colonne par conteneur
  - Une ligne pour CPU Usage
  - Une ligne pour Memory Usage
  - Une ligne pour le réseau entrant
  - Une ligne pour pour le réseau sortant

Ce qui donne un tableau récapitulatif comme celui-ci dessous: 

![](img/exo3/boom_table_result.png)

- Pour cela créer un nouveau Panel
- Puis créer les deux requêtes ci dessous :
```
sum(100 - ((container_spec_memory_limit_bytes - container_memory_usage_bytes)  * 100 / container_spec_memory_limit_bytes) ) by (name) 
```
- Avec les options :
  - Legend : `{{name}} | MemoireRestante`
  - Laisser les autres options par défaut

- Puis la seconde :
```
100 - (avg by (name) (irate(container_cpu_usage_seconds_total[5m])) *100)
```
- Avec les options :
  - Legend : `{{name}} | CPU`
  - Laisser les autres options par défaut


### Mise en forme du tableau
- En haut à droite, choisir le type de graph `Boom Table`
- Pour le titre, définir  `Etat des lieux de chaque conteneur` (ou le titre de votre choix)
- Ensuite pour définir ce qui est affiché nous allons utilisés les patterns
- Cliquer sur `Add Pattern` puis renseigner les options suivantes :
  Dans le bloc Pattern
  - Name of the Pattern : `CPU Pattern`
  - Pattern : `CPU`
  - Delimiter : `|`
  - Row Name : `_1_`
  - Col Name : `_0_`
  Dans le bloc Stats :
  - Stat: `Current`
  - Format : `Percent(0-100)`
  - Decimals: 0
  Dans le bloc Thresholds : 
  - Thresholds : `50,70`
  - Cocher `Change display value based on thresholds?`
  - Puis dans Transform Value for thresholds : `_fa-battery-full,green_ _value_|_fa-battery-quarter,yellow_ _value_|_fa-battery-empty,red_ _value_`
-> vous devriez alors obtenir des petite batterie qui indique le niveau d'utilisation du CPU

- On va ajouter un deuxième pattern pour la mémoire cette fois-ci avec les options suivantes :
Dans le bloc Pattern
  - Name of the Pattern : `MemoireRestante Pattern`
  - Pattern : `MemoireRestante`
  - Delimiter : `|`
  - Row Name : `_1_`
  - Col Name : `_0_`
  Dans le bloc Stats :
  - Stat: `Current`
  - Format : `Percent(0-100)`
  - Decimals: 0
  Dans le bloc Thresholds : 
  - Thresholds : `10,20,30,40,50,60,70,80,90`
  - Cocher `Change display value based on thresholds?`
  - Puis dans Transform Value for thresholds : `_fa-square,green,1_ _fa-square,gray,9_|_fa-square,green,2_ _fa-square,gray,8_|_fa-square,green,3_ _fa-square,gray,7_|_fa-square,green,4_ _fa-square,gray,6_|_fa-square,yellow,5_ _fa-square,gray,5_|_fa-square,yellow,6_ _fa-square,gray,4_|_fa-square,yellow,7_ _fa-square,gray,3_|_fa-square,red,8_ _fa-square,gray,2_|_fa-square,red,9_ _fa-square,gray,1_|_fa-square,red,10_ _fa-square,gray,0_`

-> Et voila vous avez obtenu les deux lignes prévues. Ce plugin est très puissant et permet d'afficher avec des transformations graphiques de nombreuses informations

N'hésitez pas à aller consulter sa documentation pour connaître ses autres possibilités et options : https://github.com/yesoreyeram/yesoreyeram-boomtable-panel 

## Aller plus loin -  Sélection de plugins

- Trouver un ou plusieurs plugins qui seraient utiles à ajouter dans Grafana pour répondre à votre problèmatique de monitoring
- Quels sont, selon vous les critères à prendre en compte pour le choix d'un plugin ?
