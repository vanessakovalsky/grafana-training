# Exercice 4 - Industrialiser l'export / import des dashboard de Grafana dans un pipeline Gitlab CI

## Export des dashboards et ajout dans un depôt git

- Sur Gitlab, forker le projet GrafanaDashboard, laisser le groupe GrafanaTraining (pour des questions d'accès)
- Aller dans votre compte Edit Profile > Access Token et générer un token avec le scope : read_repository et write_repository
- Copier le token généré
- Aller dans Settings / CI/CD, ouvrer le panneau Variables, ajouter une variable avec la clé ACCESS_TOKEN et pour value, coller le token généré à l'étape précédente, cocher mask variables et ajouter la variables
- Ajouter les trois variables suivantes :
    - GRAFANA_IMPORT_URL : URL de votre grafana à partir duquel vous voulez exporter les dashboards
    - GRAFANA_IMPORT_TOKEN : Token d'API de votre Grafana (à générer dans l'UI de Grafana)
- Lancer un build, vous devriez avoir les fichiers ajouter à votre depot dans le dossier exports
