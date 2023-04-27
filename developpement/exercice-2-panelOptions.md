# Exercice 2 - Personnaliser son panel 


## Les options de notre panel

* Nous avons besoin de définir un type TypeScript pour les options de notre panel
* Pour cela, lors de la creation du script un fichier types.ts a été géneré dans src
* Il contient l'interface 
```
type SeriesSize = 'sm' | 'md' | 'lg';

export interface SimpleOptions {
  text: string;
  showSeriesCount: boolean;
  seriesCountSize: SeriesSize;
}
```
* le type SeriesSize contient les données utilisable pour l'option seriesCountSize
* l'interface SimpleOptions contient les options utilisé par l'interface
* Vous pouvez définir d'autres données, avec les types correspondants si vous le souhaitez
* Noter que si vous mettez un `?` après le nom du paramètre, celui-ci sera optionnel, sinon il sera obligatoire lors de l'utilisation du type


## Utiliser les options

* L'utilisation des options se fait en deux étapes dans le composant :
    * Premièrement on définit une interface Props qui étend PanelsProps et prend en entrée notre type SimpleOption :
    ```
    interface Props extends PanelProps<SimpleOptions> {}
    ```
    * Puis lors de l'export de notre Panel nous typons les données avec cette interface
    ```
    export const SimplePanel: React.FC<Props> = ({ options, data, width, height }) => {
    ```
    * Nous pouvons alors appelé nos options avec {options.nomdeloption}
    ```
    <div>Text option value: {options.text}</div>
    ```
* Vérifier le résultat dans votre navigateur (en ayant laissé yarn watch tourné dans le terminal)

## Gérer le contenu du panel

* Dans le fichier SimplePanel.tsx, remplacer le contenu de `export const SimplePanel: React.FC<Props> = ({ options, data, width, height }) => { ` par le contenu suivant :
```
<div style={{ overflow: 'auto', width, height}}>
    <h1>Bienvenue dans mon panel</h1>
</div>
```
* Pour détailler un peu ces lignes :
    * la balise div contient le style qui récupère les paramètres de largeur et de hauteur du panel et active l'overflow
    * a l'intérieur du div nous choisissons le contenu à afficher
* Vérifier dans votre navigateur le résultat 
* Vous pouvez rajouter les options définies dans l'interface SimpleOption, par exemple :
```
<div>Text option value: {options.text}</div>
```

## Ajouter une option et la rendre paramètrable
* Pour commencer dans nos options nous ajoutons une nouvelle option (dans le fichier types.ts)
```
export interface SimpleOptions {
  text: string;
  showSeriesCount: boolean;
  seriesCountSize: SeriesSize;
  myNumber: number;
}
```
* L'ajout des paramètres du panel se fait dans le fichier module.ts
* Lors de l'export du plugin nous avons (create-plugin l'a fait pour vous) renvoyer la fonction builder qui permet de construire les formulaires. Elle contient déjà les champs sous forme de fonction addMyTypeFieldInput pour les options fournies par défaut
* Nous allons ajouter un champ pour notre option myNumber :
```
    .addNumberInput({
      path: 'myNumber',
      name: 'My Number',
      description: 'Number to show',
      defaultValue: 42,
    })
```
* Si nous détaillons un peux :
    * addNumberInput vient de grafana/data qui définit nos les options disponibles
    * path: il s'agit du nom de l'option qui doit être le même que dans le type
    * name: contient le nom affiché dans l'interface
    * description : contient la description
    * defaultValue : contient la valeur par défaut
* Ajoutons notre option dans l'affichage du panel (dans le fichier SimplePanel.tsx):
```
        <div>My number value {options.myNumber}</div>
```
* Il ne vous reste plus qu'à tester et à ajouter les champs dont vous avez besoin pour vos options.

