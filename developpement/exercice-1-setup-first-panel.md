# Exercice 1 - Mise en place de l'environnement et création du premier panel

## Pré-requis
* Il est nécessaire d'avoir un Grafana installé dans son environnement de développement : https://grafana.com/docs/grafana/latest/setup-grafana/installation/  (vous pouvez utiliser le docker_compose.yml a dispoition dans le dossier parent)
* Des connaissances de base sont recommandés sur ces sujets :
    * en TypeScript : https://vanessakovalsky.github.io/typescript-exercises 
    * en react : https://handsonreact.com/docs/

## Installation des outils nécessaires

### Environnement de développement
* NodeJS est nécessaire pour créer des plugins Grafana : https://nodejs.org/en/download/ 
* Nous allons utiliser l'utilitaire en ligne de commande yarn, pour l'installer (après avoir installé NodeJS):
``` 
npm i -g yarn
``` 
* NB : npm est un gestionnaire de paquet fournit par nodeJS, c'est avec lui que nous allons installé les différents paquets nécessaires
* i signifie install
* l'option -g permet d'installer le paquet de manière globale sur votre ordinateur (cela évite donc de reinstaller certains outils pour chaque projet). Par défaut le paquet (sans cet option) est ajouté dans un fichier package.json et installé dans un dossier node_modules dans le dossier dans lequel vous vous trouvez lorsque vous lancer la commmande
* Nous aurons également besoin d'un utilitaire qui nous facilite la vie pour créer les plugins : create-plugin. Pour l'installer
``` 
npm i @grafana/create-plugin
```
* Un editeur de code, nous vous recommandons VisualStudioCode : https://code.visualstudio.com/ avec les extensions suivantes :
    * React
    * Typescript React code snippet
    * React Extension Pack
    * Grafana

### Outils de test et de debug

* Un navigateur : Firefox ou Chrome sont recommandés 
* L'extension React Developer Tools pour votre navigateur : https://beta.reactjs.org/learn/react-developer-tools


## Création et affichage du premier panel

* On va créer un premier plugin de type panel
* Pour cela on utilise l'utilitaire de grafana create-plugin
* Ouvrir un terminal et se mettre dans le dossier des plugins que l'on a configurer

```
npx @grafana/create-plugin
```
* L'utilitaire va alors vous demander certaines informations et générer les fichiers indispensable à votre module (plugin.json + module.ts dans un dossier avec le nom de votre module)
* Nous avons besoin d'installer les dépendances de notre module pour cela dans le dossier du module faire la commande suivante :
```
yarn install 
```
* Commençons par builder notre module une première fois. Depuis le dossier du module faire la commande suivante :
```
yarn dev 
```
* Une fois le module généré, nous devons configurer notre environnement Grafana pour que ce nouveau plugin soit lu 

## Configuration de l'environnement 
* Grafana recherche les plugins par défaut dans un dossier data/plugins
* Nous devons donc mettre nos plugins dans ce dossier pour que Grafana les prenne en compte
* Sur un Grafana local :
    * Soit vous faite un lien symbolique entre le dossiers dans lequel vous travailler et le dossier plugin : 
    ```
    ln -s <plugin-path>/dist data/plugins/<plugin-name>
    ```
    * Soit vous modifier la lignes de configuration du fichier conf/custom.ini qui définit le chemin dans lequel sont stocké vos plugins
    ```
    [paths]
    plugins = <path-to-your-plugin-parent-directory>
    ```
    * Pour que grafana prenne en compte les modifications du fichier de configuration il est nécessaire de redemarrer Grafana
* En utilisant docker : 
    * un fichier docker-compose.yml est présent à la racine du dossier
    * lancer le avec la commande : docker-compose up -d
* Lorsque Grafana a redémarrer vous pouvez déjà aller vérifier que votre plugin est bien détecté dans l'UI de Grafana et activer le
* Toujours dans l'UI, créer un dashboard et un Panel à l'aide de votre Plugin. 
* Votre Panel doit maintenant apparaître :)

## Continuer à modifier son plugin
* Vous pouvez modifier votre plugin sans oublier de faire la commande
```
yarn dev
``` 
* pour que Grafana récupère la dernière version
* Ou bien si vous préferez avoir un rechargement à chaud: 
```
yarn watch
```


