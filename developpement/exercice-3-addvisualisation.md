# Exercice 3 - Visualiser des données dans notre Panel

## Récupérer et manipuler les données

* Dans notre Plugins nous récupérons data qui contient les données de notre requête
* Cet objet data contient une collection series sur laquel nous pouvons utiliser la fonction map qui nous permet de répéter un traitement pour chaque élément d'une collection :
```
  const valueField = data.series[0].fields.find((field) => field.type === 'number');
```
* Ici nous avons mis dans la constante valueField les valeurs des champs de type numbers de la première serie
* Si nous ajoutons cela à l'affichage de notre module :
```
        <div>
          {valueField.values}
        </div>
```
* Visualiser dans le navigateur

## Continuer avec les données

* A partir de data, afficher un tableau contenant les données
