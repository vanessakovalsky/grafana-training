# Installation de l'environnement

## Pré-requis

* Avoir docker-compose installé et docker lancé

* Récupérer les fichiers de ce dossier timescale
* Lancer un  \docker-compose up -d
* Copier les fichiers create_table.sql et nyc_data_rides.csv dans le conteneur : docker cp myfile timescale:/
* Se connecter au conteneur : docker exec -it timescale /bin/bash
* Dans le conteneur se connecter à Postgres : psql --username=timescale 
* Créer une BDD : data
* importer les fichiers : \COPY create_table.sql
* \COPY rides FROM nyc_data_rides.csv CSV;
* Vérifier que les données sont importées : SELECT * FROM rides LIMIT 5;
* Sortir de psql
* sortir du conteneur

* Aller sur http://localhost:3030
* Se connecter à Grafana (admin/admin la premières fois)