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
* Pour cela nous commençons par extraire les données de la première séries et par les mettre dans un tableau en utilisant la fonction foreach pour récupérer chaque élément de la série et les ajouter dans notre tableau 
```
const frame = data.series[0];

  const colData = new Array(0);

  frame.fields.forEach((field) => {
    colData.push(new ColData(
      field.name,
      field.config?.displayName || field.name,
      field.type,
      field.values.toArray().map((v) => v as number),
    ));
  });
```

* Ensuite pour afficher ces éléments nous allons d'abord utiliser la fonction map pour extraire le nom des champs, puis mapper nos valeurs :
```
<table>
      <thead>
        <tr>
        { colData.map((field) => (
              <th key={field}>{field.displayName}</th>
          ))}
        </tr>
          
      </thead>
      <tbody>
        { colData.map((field) => (
            field.values.map((value: number, index: number) => 
            <tr key={index}>
              <td key={index}>{value}</td>
            </tr>

            )
          ))}
      </tbody>
    </table>
```
* Pour continuer à manipuler les valeurs, ajouter d'autres colonnes à notre première série et mettre à jour le code correspondant
* Puis ajouter une deuxième serie de données et l'afficher également