# Module 00 — Exercices

Parcours essentiel = Lab 00.1 (tout le groupe). Défis = facultatifs, en cas d'avance.

## Lab 00.1 ⭐ — Ouvrir Grafana (guidé)
**Durée** : 5 min · **Objectif** : afficher Grafana et s'y connecter
**Contexte** : chaque technicien du NOC de *Telcéa* dispose de sa propre instance Grafana.
**Prérequis** : courriel d'accès (adresse, mot de passe), navigateur récent (Firefox, Chrome, Edge)

### Étapes
1. Copier-coller l'adresse **Grafana** du courriel dans la barre d'adresse du navigateur (pas dans un moteur de recherche) :
   `https://stagiaire<NN>.<SESSION>.kovalibre-labs.com/grafana/`
   Résultat attendu : page de connexion Grafana.
2. Identifiant `admin`, mot de passe du courriel → **Log in**.
   Résultat attendu : page d'accueil *Welcome to Grafana*.

### Si la page ne s'ouvre pas
- Adresse complète : `https://` au début, `/grafana/` à la fin, numéro `<NN>` sur 2 chiffres (`03`, pas `3`)
- Lien du courriel bloqué → adresse copiée-collée à la main
- Autre navigateur, ou fenêtre de navigation privée
- Toujours bloqué → signaler à la formatrice, travail en binôme avec le voisin en attendant

### Critères de réussite
- [ ] Page *Welcome to Grafana* affichée

Bureau Linux de la VM (`https://stagiaire<NN>.<SESSION>.kovalibre-labs.com/`, `stagiaire` / même mot de passe) : utile uniquement pour les défis.

---

## Défis facultatifs (en cas d'avance)

## Défi 00.2 ⭐⭐ — Découvrir les données brutes du réseau Telcéa
**Durée** : 5 min · **Objectif** : voir à quoi ressemblent les métriques avant de les afficher dans Grafana
**Contexte** : le simulateur du réseau Telcéa publie ses mesures au format texte Prometheus, lu toutes les 15 s.

**Énoncé** :
- Ouvrir le bureau Linux (adresse ci-dessus), puis, dans son navigateur, la page des métriques du simulateur.
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

## Défi 00.3 ⭐⭐⭐ — Vérifier l'état de la stack en ligne de commande
**Durée** : 5 min (ou pendant la première pause) · **Objectif** : contrôler soi-même l'environnement de travail
**Contexte** : avant la prise de poste, le technicien du NOC vérifie ses outils.

**Énoncé** : dans un terminal du bureau, lancer le contrôle de la stack fournie dans `~/grafana-training/stack`, puis identifier quel service conserve les journaux d'alarmes du réseau. Bonus : retrouver la version de Grafana (menu d'aide `?`).

**Critères de réussite** :
- [ ] Contrôle terminé par `Result: stack ready`
- [ ] Service des journaux identifié et justifié
