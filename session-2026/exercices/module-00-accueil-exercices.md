# Module 00 — Exercices

## Lab 00.1 ⭐ — Accéder à Grafana et au bureau de sa VM (guidé)
**Durée** : 5 min · **Objectif** : se connecter à Grafana et au bureau Linux avec les identifiants fournis
**Contexte** : chaque technicien du NOC de *Telcéa* dispose d'une VM qui héberge Grafana et les outils de supervision.
**Prérequis** : identifiants reçus (URL, mot de passe), navigateur récent (Firefox, Chrome, Edge)

Variables : `<NN>` = numéro de VM sur 2 chiffres ; `<SESSION>` = nom de la session ; `<MOT_DE_PASSE>` = mot de passe fourni.

### Étapes
1. Ouvrir Grafana : `https://stagiaire<NN>.<SESSION>.kovalibre-labs.com/grafana/`.
   Résultat attendu : page de connexion Grafana, cadenas HTTPS valide.
2. Se connecter avec `admin` / `<MOT_DE_PASSE>`.
   Résultat attendu : page d'accueil *Welcome to Grafana*.
3. Ouvrir le menu d'aide (icône `?` en haut à droite).
   Résultat attendu : `Grafana v13.3.1 (da3aa3ff57)` en tête du menu.
4. Ouvrir le menu principal (icône ☰ en haut à gauche) → **Connections** → **Data sources**.
   Résultat attendu : aucune source de données (raccordement au M03).
5. Dans un second onglet, ouvrir le bureau : `https://stagiaire<NN>.<SESSION>.kovalibre-labs.com/`, se connecter avec `stagiaire` / `<MOT_DE_PASSE>`.
   Résultat attendu : bureau Linux ouvert automatiquement.

### Critères de réussite
- [ ] Grafana affiché en HTTPS, session `admin` ouverte, version 13.3.1
- [ ] Bureau Linux ouvert dans le second onglet

---

## Exercice 00.2 ⭐⭐ — Découvrir les données brutes du réseau Telcéa (semi-autonome)
**Durée** : 5 min · **Objectif** : voir à quoi ressemblent les métriques avant de les afficher dans Grafana
**Contexte** : le simulateur du réseau Telcéa publie ses mesures au format texte Prometheus, lu toutes les 15 s.

**Énoncé** :
- Depuis le navigateur du bureau Linux, afficher la page des métriques du simulateur.
- Trouver la valeur actuelle de `telcea_cell_users` pour le site `PAR-01`.
- Compter les sites déclarés dans `telcea_site_info`.

**Indices** :
- Adresse du simulateur, depuis la VM uniquement : `http://localhost:9200/metrics`
- Recherche dans la page : `Ctrl + F`
- Une ligne = un nom de métrique + des étiquettes entre accolades + une valeur

**Critères de réussite** :
- [ ] Valeur du nombre d'abonnés de `PAR-01` notée
- [ ] 12 sites comptés

---

## Défi 00.3 ⭐⭐⭐ — Vérifier l'état de la stack en ligne de commande (autonome)
**Durée** : 5 min (ou pendant la première pause) · **Objectif** : contrôler soi-même l'environnement de travail
**Contexte** : avant la prise de poste, le technicien du NOC vérifie ses outils.

**Énoncé** : dans un terminal du bureau, lancer le contrôle de la stack fournie dans `~/grafana-training/stack`, puis identifier quel service conserve les journaux d'alarmes du réseau.

**Critères de réussite** :
- [ ] Contrôle terminé par `Result: stack ready`
- [ ] Service des journaux identifié et justifié
