# Module 02 — Exercices

Parcours essentiel = Lab 02.1 (tout le groupe). Défis = facultatifs, en cas d'avance.
Interface de Grafana en anglais (libellés des énoncés) : ne pas changer la langue du profil.

## Lab 02.1 ⭐ — Nommer l'organisation Telcéa (guidé)
**Durée** : 5 min · **Objectif** : régler le nom et le fuseau horaire de l'organisation
**Contexte** : l'instance Grafana du NOC doit porter le nom de l'opérateur et afficher l'heure de Paris.
**Prérequis** : Lab 00.1 (session `admin` ouverte)

### Étapes
1. Menu principal (icône ☰ en haut à gauche) → **Administration** → **General** → **Default preferences**.
2. **Organization name** : `Telcéa` → bouton **Update organization name**.
   Résultat attendu : `Telcéa` affiché en haut de la page.
3. **Timezone** : `Europe/Paris` → bouton **Save preferences** (bas de page).

### Si bloqué
Rattrapage par la formatrice (5 s) : sans impact sur la suite.

### Critères de réussite
- [ ] **Default preferences** affiche `Telcéa` et `Europe/Paris`

---

## Défis facultatifs (en cas d'avance)

## Défi 02.2 ⭐ — Lire la configuration effective et l'état de l'instance
**Durée** : 10 min · **Objectif** : retrouver la valeur réellement appliquée de 4 paramètres et l'état de santé de l'instance
**Contexte** : avant de raccorder les sources, le NOC vérifie que l'instance est correctement configurée.

**Énoncé** :
1. **Administration → General → Settings** (`Ctrl + F` dans la page) : relever `server` → `root_url`, `database` → `type`, `smtp` → `enabled`, `paths` → `provisioning`.
2. **Administration → General → Stats and license** : nombre de tableaux de bord et d'utilisateurs.
3. **Administration → Plugins and data → Plugins**, filtre **Installed** : 3 plugins de type *Data source* déjà présents.
4. **Administration → Advisor** : bouton **Refresh**, lire le résultat.
5. Palette de commandes : `Ctrl + K`, taper `preferences`.

**Critères de réussite** :
- [ ] `root_url` terminé par `/grafana/`, `type` = `sqlite3`, `enabled` = `true`
- [ ] `0` tableau de bord, `1` utilisateur (avant le M04)

---

## Défi 02.3 ⭐⭐ — Surcharger un paramètre par variable `GF_*`
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

## Défi 02.4 ⭐⭐⭐ — Provisionner le tableau de bord d'accueil du NOC
**Durée** : 10 min · **Objectif** : créer par fichier un dossier et un tableau de bord verrouillés
**Contexte** : le responsable du NOC veut un tableau de bord « [TLC] NOC — Lisez-moi » (numéros d'astreinte) que personne ne peut modifier dans l'interface.

**Énoncé** : à l'aide du provisioning (`stack/grafana/provisioning/dashboards/`), créer le dossier `NOC` contenant le tableau de bord `[TLC] NOC — Lisez-moi` (uid `noc-lisez-moi`) avec un panel texte en Markdown : « Astreinte radio : poste 1001 » et « Astreinte transport : poste 1002 ».

Contraintes : aucune action dans l'interface ; l'enregistrement d'une modification dans l'interface doit être refusé.

**Critères de réussite** :
- [ ] Dossier `NOC` et tableau de bord visibles dans **Dashboards**
- [ ] Bandeau ou message indiquant un tableau de bord provisionné lors d'une tentative d'enregistrement
