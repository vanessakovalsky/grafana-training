# Module 01 — Exercices

## Lab 01.1 ⭐ — Compléter la chaîne de supervision de Telcéa (guidé)
**Durée** : 5 min · **Objectif** : placer chaque composant de la stack dans son rôle (collecte, stockage, visualisation)
**Contexte** : le NOC de Telcéa reçoit sa nouvelle stack de supervision ; l'équipe doit savoir qui fait quoi avant de l'utiliser.
**Prérequis** : aucun (papier, tableau blanc ou éditeur de texte)

### Étapes
1. Recopier le tableau ci-dessous.

   | Composant | Rôle (collecte / stockage / visualisation / alerte) | Mode (*pull* / *push* / —) |
   |---|---|---|
   | Simulateur Telcéa | | |
   | node-exporter | | |
   | Telegraf | | |
   | Prometheus | | |
   | InfluxDB | | |
   | Alloy | | |
   | Loki | | |
   | Grafana | | |
   | Alertmanager | | |

2. Compléter chaque ligne à l'aide des slides « La chaîne de supervision » et « Collecter : *pull* ou *push* ? ».
3. Dessiner les flèches entre composants (sens de circulation des données).
   Résultat attendu : 3 chaînes qui convergent vers Grafana (réseau, système, journaux).

### Critères de réussite
- [ ] 9 lignes complétées, sans case vide
- [ ] Grafana relié aux 3 bases (Prometheus, InfluxDB, Loki), sans flèche vers les collecteurs

---

## Exercice 01.2 ⭐⭐ — Classer les indicateurs du NOC (semi-autonome)
**Durée** : 7 min · **Objectif** : relier un indicateur à sa famille, son type de donnée et son destinataire
**Contexte** : le responsable du NOC veut savoir quelle équipe reçoit quel indicateur.

**Énoncé** : pour chacun des 8 indicateurs, indiquer la famille (disponibilité, capacité, qualité, environnement), le type de donnée (métrique, journal), l'unité, et l'équipe destinataire (`radio` : sites ; `transport` : liens et routeurs ; `systeme` : VM de supervision).
1. Site BRE-01 en service ou non
2. Nombre d'abonnés connectés sur MRS-01
3. Utilisation du lien REN-PAR
4. Message « Perte d'alimentation secteur puis arrêt du site »
5. Taux de réussite des appels en Bretagne
6. Température de la salle technique de REN-01
7. Utilisation CPU du routeur `rtr-lil-01`
8. Espace disque libre de la VM de supervision

**Indices** :
- Slide « Que superviser chez un opérateur ? »
- Un message texte horodaté = journal ; une valeur numérique = métrique

**Critères de réussite** :
- [ ] 8 lignes complètes (famille, type, unité, équipe)
- [ ] Au moins un indicateur par équipe

---

## Défi 01.3 ⭐⭐⭐ — Choisir le mode de collecte (autonome)
**Durée** : 5 min · **Objectif** : justifier le choix *pull* ou *push* selon la contrainte
**Contexte** : Telcéa raccorde trois nouvelles sources à sa supervision.

**Énoncé** : pour chaque cas, choisir *pull* ou *push* et justifier en une ligne (sécurité, détection de panne, durée de vie de la source).
1. Boîtiers fibre installés chez les clients, derrière un routeur domestique (aucun port entrant)
2. Script de facturation lancé chaque nuit, durée 4 minutes
3. 40 conteneurs applicatifs recréés plusieurs fois par jour

**Critères de réussite** :
- [ ] Un choix et une justification par cas
- [ ] Au moins une limite citée pour chaque choix

---

## Bonus 🚀 — Lire une page de métriques
Depuis le navigateur du bureau Linux, ouvrir `http://localhost:9200/metrics` (simulateur Telcéa) et repérer, pour `telcea_site_up`, la ligne `# HELP`, la ligne `# TYPE` et une valeur. Puis ouvrir `http://localhost:9090/targets` (Prometheus) : retrouver la cible du simulateur et son état.
