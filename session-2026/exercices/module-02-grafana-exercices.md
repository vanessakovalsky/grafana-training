# Module 02 — Exercices

Interface de Grafana en anglais (libellés des énoncés). Passage en français possible au Lab 02.1 (profil) : les libellés diffèrent alors des énoncés.

## Lab 02.1 ⭐ — Prendre en main l'interface et nommer l'organisation (guidé)
**Durée** : 10 min · **Objectif** : naviguer dans Grafana et régler les préférences de l'organisation Telcéa
**Contexte** : le NOC de Telcéa partage une instance Grafana ; l'organisation doit porter le nom de l'opérateur et afficher l'heure de Paris.
**Prérequis** : Lab 00.1 (session `admin` ouverte)

### Étapes
1. Ouvrir le menu principal (icône ☰ en haut à gauche) et repérer les entrées **Home**, **Dashboards**, **Explore**, **Drilldown**, **Alerting**, **Connections**, **Administration**.
2. Ouvrir la palette de commandes avec `Ctrl + K`, taper `preferences`, sélectionner **Default preferences**.
   Résultat attendu : page **Administration → General → Default preferences**.
3. Renseigner :
   - **Organization name** : `Telcéa` → **Update organization name**
   - **Timezone** : `Europe/Paris`
   - **Week start** : `Monday` → **Save preferences**
   Résultat attendu : nom `Telcéa` affiché en haut de la page.
4. Ouvrir le profil (menu ☰ → **admin** → **Profile**) et repérer le champ **Language** (ne pas le modifier pendant la formation).

### Critères de réussite
- [ ] **Default preferences** affiche `Telcéa`, `Europe/Paris`, `Monday`
- [ ] Palette de commandes (`Ctrl + K`) utilisée au moins une fois

---

## Lab 02.2 ⭐ — Lire la configuration effective et l'état de l'instance (guidé)
**Durée** : 10 min · **Objectif** : retrouver la valeur réellement appliquée de 4 paramètres et l'état de santé de l'instance
**Contexte** : avant de raccorder les sources, le NOC vérifie que l'instance est correctement configurée.
**Prérequis** : Lab 02.1

### Étapes
1. Menu **Administration → General → Settings**. Utiliser `Ctrl + F` dans la page pour trouver chaque valeur et la noter :

   | Section | Clé | Valeur relevée |
   |---|---|---|
   | `server` | `root_url` | |
   | `database` | `type` | |
   | `smtp` | `enabled` | |
   | `paths` | `provisioning` | |

   Résultat attendu : `root_url` se termine par `/grafana/` ; `type` = `sqlite3` ; `enabled` = `true`.
2. Menu **Administration → General → Stats and license** : noter le nombre de tableaux de bord et d'utilisateurs.
   Résultat attendu : `0` tableau de bord, `1` utilisateur.
3. Menu **Administration → Plugins and data → Plugins**, filtre **Installed** : noter 3 plugins de type *Data source* déjà présents.
4. Menu **Administration → Advisor** : relancer les contrôles (bouton **Refresh**) et lire le résultat.
   Résultat attendu : `No issues found.` ou une liste de points à corriger (ex. `Updates available for 1 plugin`).

### Critères de réussite
- [ ] 4 valeurs relevées dans **Settings**
- [ ] Compteurs **Stats** relevés
- [ ] Contrôles **Advisor** lancés

---

## Exercice 02.3 ⭐⭐ — Surcharger un paramètre par variable `GF_*` (semi-autonome)
**Durée** : 10 min · **Objectif** : modifier la configuration sans éditer de fichier `.ini` et prouver la prise en compte
**Contexte** : pour protéger les sources de données, le NOC interdit les rafraîchissements de tableau de bord plus fréquents que toutes les 10 s.

**Énoncé** :
- Dans le bureau Linux, dossier `~/grafana-training/stack`, créer un fichier `compose.override.yaml` qui ajoute au service `grafana` la variable correspondant à la clé `min_refresh_interval` de la section `[dashboards]`, valeur `10s`.
- Recréer le conteneur Grafana.
- Prouver la nouvelle valeur dans **Administration → General → Settings**.

**Indices** :
- Nom de variable : `GF_<SECTION>_<CLÉ>` en majuscules
- Un fichier `compose.override.yaml` est fusionné automatiquement avec `compose.yaml`
- Recréation d'un seul service : `docker compose up -d <SERVICE>`

**Critères de réussite** :
- [ ] `dashboards` → `min_refresh_interval` = `10s` dans **Settings**
- [ ] Aucune modification de `compose.yaml` (`git -C ~/grafana-training status` : seul `compose.override.yaml` est nouveau, ignoré par Git)

---

## Défi 02.4 ⭐⭐⭐ — Provisionner le tableau de bord d'accueil du NOC (autonome)
**Durée** : 10 min · **Objectif** : créer par fichier un dossier et un tableau de bord verrouillés
**Contexte** : le responsable du NOC veut un tableau de bord « [TLC] NOC — Lisez-moi » (numéros d'astreinte) que personne ne peut modifier dans l'interface.

**Énoncé** : à l'aide du provisioning (`stack/grafana/provisioning/dashboards/`), créer le dossier `NOC` contenant le tableau de bord `[TLC] NOC — Lisez-moi` (uid `noc-lisez-moi`) avec un panel texte en Markdown : « Astreinte radio : poste 1001 » et « Astreinte transport : poste 1002 ».

Contraintes : aucune action dans l'interface ; l'enregistrement d'une modification dans l'interface doit être refusé.

**Critères de réussite** :
- [ ] Dossier `NOC` et tableau de bord visibles dans **Dashboards**
- [ ] Bandeau ou message indiquant un tableau de bord provisionné lors d'une tentative d'enregistrement
