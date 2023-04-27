# Exercice 4 - Utiliser une bibliothèque externe dans notre plugins

Dans cet exercice nous allons utiliser la bibliothèque Victory-candlestick pour tracer des graphique de type candlesticke

## Installation de la bibliothèque

* Une fois le plugin créé (voir exercice 1 si nécessaire), se mettre dans le dossier du plugins
* Nous utilisons la commande yarn add pour installer les bibliothèques nécessaires à notre plugin :
```
yarn add victory victory-candlestick
```
* Une fois les dépendances installées, vous pouvez lancer un yarn dev pour vérifier que tout est OK. Vous devriez avoir un message vous indiquant différents éléments, par exemple
```
assets by status 13.4 KiB [cached] 5 assets
asset module.js 2.64 MiB [emitted] (name: module)
cached modules 1.42 MiB [cached] 647 modules
runtime modules 1.25 KiB 6 modules
cacheable modules 2.73 KiB
  ./module.ts 1.04 KiB [code generated]
  ./components/SimplePanel.tsx 1.69 KiB [built] [code generated]
webpack 5.81.0 compiled successfully in 988 ms
No errors found.
```
* En cas d'erreur vérifier l'erreur et corriger ce qui ne fonctionne pas
* N'oubliez pas de redemarrer Grafana en cas de création d'un nouveau plugin pour que celui-ci soit pris en compte


## Utilisation de la bibliothèque externe

* Pour utiliser une bibliothèque externe, nous devons l'importer. Pour cela ajouter en haut du fichier dans lequel vous souhaitez utiliser la bibliothèque les imports adequats :
```
import { VictoryCandlestick } from 'victory-candlestick';
import { VictoryChart, VictoryAxis, VictoryTheme } from 'victory';
```

* Puis vous pouvez appelez votre bibliothèque dans votre code
```
<VictoryChart
          theme={VictoryTheme.material}
          domainPadding={{ x: 25 }}
          scale={{ x: "time" }}
          width={width}
          height={height}
        >
        <VictoryAxis tickFormat={(t) => `${t.getDate()}/${t.getMonth()}`}/>
        <VictoryAxis dependentAxis/>
        <VictoryCandlestick
          candleColors={{ positive: "#5f5c5b", negative: "#c43a31" }}
          data={[
            {x: new Date(2023, 6, 1), open: 5, close: 10, high: 15, low: 0},
            {x: new Date(2023, 6, 2), open: 10, close: 15, high: 20, low: 5},
            {x: new Date(2023, 6, 3), open: 15, close: 20, high: 22, low: 10},
            {x: new Date(2023, 6, 4), open: 20, close: 10, high: 25, low: 7},
            {x: new Date(2023, 6, 5), open: 10, close: 8, high: 15, low: 5}
          ]}
        />
      </VictoryChart>
```
* Vous pouvez maintenant utiliser les bibliothèques de votre choix sur votre plugin

## A vous de jouer :
* Lors la génération du candlestick, nous avons utilsier un jeu de données fixe, remplacer ce jeu de données par des données venant des requêtes de grafana, en permettant à l'utilisateur de selectionner pour chaque élément le champs de son choix
* Vous pouvez également exploiter les autres types de graphiques de Victory : https://formidable.com/open-source/victory/docs 