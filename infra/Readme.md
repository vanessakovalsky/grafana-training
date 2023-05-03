# Infrastructure pour formation Grafana / Prometheus / InfluxDB / Loki


## Sur AWS 
- Lancer VM sur AWS avec image Prom...
- Se connecter en ssh (login ubuntu)
- se mettre dans /home/ubuntu/laravel-kingoludo-master/src
- docker-compose up -d
- (influx db et telegraph sont installé et tournent) : sudo systemctl status influxdb
- dans le groupe de securité ouvrir les ports : 3000 (grafana), 8090 (app), 9090 (prometheus) 8086(influxdb)
- Aller dans l'UI de influxdb 
- Load Data > Telegraph, puis créer une nouvelle config
- /!\ Telegraph doit tourner pour que les données soient envoyées dans InfluxDB

# En local

- cloner le dépôt laravel-kingoludo dans le dossier courant puis lancer :
- docker-compose up -d


## Todo :
- Add influxDB et telegraph sur le compose
- Ajouter le provisionning de loki et de influx db à Grafana