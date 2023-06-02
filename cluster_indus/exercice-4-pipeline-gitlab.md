# Exercice 4 - Industrialiser l'export / import des dashboard de Grafana dans un pipeline Gitlab CI

## Ecriture d'un dashboard avec Grafyaml

### Configurer votre environnement
* En local sur votre environnement, vous devez avoir python 3 installé
* Lancer l'installation de l'outil :
```
pip install grafyaml
```
* Vous aurez besoin ensuite d'une variable d'environnement GRAFANA_API_KEY qui contient la valeur de la clé d'API du grafana sur lequel vous voulez déployer (à récupérer dans l'UI de grafana ou avec la requête API suivante)
```
curl -X POST -H "Content-Type: application/json" -d '{"name":"apikeycurl", "role": "Admin"}' http://admin:admin@ec2-3-143-234-246.us-east-2.compute.amazonaws.com:3000/api/auth/keys
```
* -> Pensez à remplacer l'URL par celle de votre grafana et admin:admin par les identifiants correspondant à votre environnement

* En environnement Linux pour définir la variable d'environnement :
```
export GRAFANA_API_KEY="API_KEY_HERE"
```
* En environnement Windows, vous pouvez utiliser les paramètres systèmes : https://www.malekal.com/variables-environnement-windows/#Modifier_les_variables_d8217environnement 

### Créer le fichier de dashboard

* Créer un dossier dashboard et à l'intérieur un fichier mondashboard.yml avec le contenu suivant:
```
dashboard:
  editable: false
  tags:
  - grafyaml
  - example
  - basic
  time:
    from: now-30m
    to: now
  timezone: browser
  title: Host metrics
  rows:
  - showTitle: true
    title: CPU and memory usage
    collapse: false
    height: 500px
    panels:
    - fill: 8
      legend:
        alignAsTable: true
        current: true
        show: true
        sort: current
        sortDesc: true
        values: true
      span: 4
      stack: true
      targets:
      - expr: 100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) * on (instance) group_left (nodename) node_uname_info
        legendFormat: '{{ nodename }}'
      title: CPU usage
      type: graph
    - fill: 8
      legend:
        alignAsTable: true
        current: true
        show: true
        sort: current
        sortDesc: true
        values: true
      span: 4
      stack: true
      targets:
      - expr: 100 * (avg by (instance) (1 - ((avg_over_time(node_memory_MemFree_bytes{}[5m]) + avg_over_time(node_memory_Cached_bytes{}[5m]) + avg_over_time(node_memory_Buffers_bytes{}[5m])) / avg_over_time(node_memory_MemTotal_bytes{}[5m])))) * on (instance) group_left (nodename) node_uname_info
        legendFormat: '{{ nodename }}'
      title: Memory usage
      type: graph
```
* Le dashboard contient une seule ligne avec deux graphique de types graphs. 
* Pour déployer votre dashboard sur votre Grafana : 
```
grafana-dashboard --grafana-url https://my-grafana-host.domain.com update dashboard/mondashboard.yml
```

* A vous de jouer : a partir des exemples présent ici : https://github.com/deliveryhero/grafyaml/tree/master/examples/advanced/templates, construire un dashboard reprenant celui fait dans l'interface

## Export des dashboards et ajout dans un depôt git

- Sur Gitlab, forker le projet GrafanaDashboard, laisser le groupe GrafanaTraining (pour des questions d'accès)
- Aller dans votre compte Edit Profile > Access Token et générer un token avec le scope : read_repository et write_repository
- Copier le token généré
- Aller dans Settings / CI/CD, ouvrer le panneau Variables, ajouter une variable avec la clé ACCESS_TOKEN et pour value, coller le token généré à l'étape précédente, cocher mask variables et ajouter la variables
- Ajouter les trois variables suivantes :
    - GRAFANA_IMPORT_URL : URL de votre grafana à partir duquel vous voulez exporter les dashboards
    - GRAFANA_IMPORT_TOKEN : Token d'API de votre Grafana (à générer dans l'UI de Grafana)
- Lancer un build, vous devriez avoir les fichiers ajouter à votre depot dans le dossier exports

