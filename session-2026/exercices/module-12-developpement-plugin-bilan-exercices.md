# Module 12 — Exercices

Fichiers fournis : `~/grafana-training/ateliers/m12/` (`plugin.json`, `module.ts`, `arborescence.txt`), issus d'un squelette généré par `@grafana/create-plugin` 9.0.4.

## Lab 12.1 ⭐ — Lire un plugin généré (guidé)
**Durée** : 5 min · **Objectif** : retrouver dans les fichiers d'un plugin son type, son identifiant, sa compatibilité et ses options
**Contexte** : Telcéa envisage un panel maison « NOC Status » ; le squelette vient d'être généré.
**Prérequis** : aucun (lecture de fichiers)

### Étapes
1. Ouvrir `ateliers/m12/plugin.json` (éditeur du bureau, ou dépôt en ligne) et noter :
   - **type** et **id** ;
   - version minimale de Grafana (`grafanaDependency`).
   Résultat attendu : `panel`, `telcea-nocstatus-panel`, `>=13.2.0`.
2. Ouvrir `ateliers/m12/module.ts` : lister les options proposées dans l'éditeur du panel (`path` et `name` de chaque `add...`).
   Résultat attendu : 3 options (`text`, `showSeriesCount`, `seriesCountSize`).
3. Ouvrir `ateliers/m12/arborescence.txt` : repérer le fichier de rendu React et le fichier Docker de développement.

### Critères de réussite
- [ ] Type, identifiant et compatibilité relevés
- [ ] 3 options identifiées

---

## Exercice 12.2 ⭐⭐ — QCM final (semi-autonome)
**Durée** : 15 min · **Objectif** : évaluer ses acquis sur les 2 jours
**Contexte** : clôture de la formation.

**Énoncé** : répondre au QCM final (20 questions) distribué par la formatrice (`evaluation-finale.md`), puis compléter l'auto-positionnement (slide « Objectifs du programme : atteints ? »).

**Critères de réussite** :
- [ ] 20 réponses
- [ ] Auto-positionnement de 1 à 4 sur chaque objectif

---

## Défi 12.3 ⭐⭐⭐ — Générer et lancer son premier panel (hors temps de formation)
**Durée** : 45 min · **Objectif** : générer, compiler et afficher un panel maison dans un Grafana de développement
**Contexte** : pour aller plus loin après la formation, sur un poste personnel (Node.js 22 ou plus, Docker).

**Énoncé** :
1. Générer un plugin de panel `noc-status` (organisation `telcea`, sans backend).
2. `npm install`, `npm run dev`, puis `docker compose up` dans un second terminal.
3. Ouvrir `http://localhost:3000`, ajouter le panel `Noc-Status` à un tableau de bord, modifier le texte par défaut de l'option `text` dans `module.ts` et constater la mise à jour.

Exercices historiques plus poussés (options, visualisation, bibliothèque externe) : dossier `developpement/` du dépôt `grafana-training`, à adapter à `create-plugin` 9 (`[À VÉRIFIER]` : écrits pour une version antérieure de l'outil).

**Critères de réussite** :
- [ ] Panel `Noc-Status` affiché dans le Grafana de développement
- [ ] Modification du code visible après rechargement
