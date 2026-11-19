# Module 08 — Exercices

Parcours essentiel = Labs 08.1 et 08.2 (tout le groupe). Défis = facultatifs, en cas d'avance.
Canal d'échange des liens et fichiers : messagerie de la session (Teams ou équivalent).

## Lab 08.1 ⭐ — Lien interne et lien externe (guidé)
**Durée** : 10 min · **Objectif** : partager une vue figée avec un collègue, puis l'écran mural sans compte
**Contexte** : l'équipe *radio* signale un incident en Bretagne ; la direction veut suivre l'écran mural depuis son bureau, sans compte Grafana.
**Prérequis** : tableau de bord régional (M06), écran mural (M07) — sinon rattrapage par la formatrice

### Étapes
1. Ouvrir `[TLC] Réseau — Détail régional`, Région `Bretagne`.
2. Bouton **Share** (barre du haut) → **Share internally** : activer **Lock time range** → **Copy link**.
3. Coller le lien dans un nouvel onglet.
   Résultat attendu : région `Bretagne`, dates et heures fixes à la place de `Last ...`.
4. Ouvrir `[TLC] NOC — Écran mural` → **Share** → **Share externally** : cocher « I understand that this entire dashboard will be public. » → **Accept** → **Copy external link**.
5. Ouvrir le lien externe dans une fenêtre de navigation privée (`Ctrl + Maj + N` ou `Ctrl + Maj + P`).
   Résultat attendu : écran mural affiché sans connexion, en lecture seule.

### Critères de réussite
- [ ] Lien interne à plage figée et région conservée
- [ ] Écran mural visible sans compte

---

## Lab 08.2 ⭐ — Snapshot d'incident (guidé)
**Durée** : 10 min · **Objectif** : figer l'état du tableau de bord national et transmettre le lien
**Contexte** : le prestataire de maintenance radio doit voir l'état du réseau à l'instant du signalement, sans accès aux requêtes ni aux sources.
**Prérequis** : tableau de bord national (M05)

### Étapes
1. `[TLC] Réseau — Vue nationale` → **Share** → **Share snapshot**.
2. **Snapshot name** : `[TLC] Réseau — état <HEURE>` ; **Expires in** : `1 Day`.
3. Bouton **Publish snapshot** (et SURTOUT PAS **Publish to snapshots.raintank.io**) → **Copy link**.
4. Envoyer le lien à la formatrice par la messagerie de la session.
5. Ouvrir le snapshot, modifier la plage de temps.
   Résultat attendu : données figées.

### Critères de réussite
- [ ] Snapshot local publié, lien transmis

---

## Défis facultatifs (en cas d'avance)

## Défi 08.2b ⭐⭐ — Maîtriser les partages publics et les snapshots
**Durée** : 5 min · **Objectif** : couper un accès public et retrouver un snapshot
**Énoncé** :
1. **Dashboards → Public dashboards** : écran mural → **Pause access**, recharger la fenêtre privée (accès refusé), puis réactiver.
2. **Dashboards → Snapshots** : retrouver son snapshot, noter sa date d'expiration.
3. Lien interne raccourci : option **Shorten link** de **Share internally**.

**Critères de réussite** :
- [ ] Accès bloqué pendant la pause, rétabli ensuite
- [ ] Date d'expiration relevée

---

## Défi 08.3 ⭐⭐ — Échanger un tableau de bord avec son binôme (semi-autonome)
**Durée** : 15 min · **Objectif** : exporter son tableau de bord régional et importer celui du binôme dans sa propre instance
**Contexte** : deux NOC régionaux de Telcéa veulent comparer leurs écrans ; chaque NOC a sa propre instance Grafana.

**Énoncé** :
- Exporter `[TLC] Réseau — Détail régional` dans un fichier, en préparant le fichier pour une AUTRE instance.
- Transmettre le fichier au binôme ; importer le sien dans le dossier `NOC Telcéa`, sous le titre `[TLC] Réseau — Détail régional (binôme <PRÉNOM>)`, avec sa propre source Prometheus.
- Vérifier que les variables et les panels fonctionnent.

Variables : `<PRÉNOM>` = prénom du binôme.

**Indices** :
- Export : **Export** (barre du haut) → **Export as code**, option **Share dashboard with another instance**, puis **Download file**
- Import : **Dashboards → New → Import dashboard** → **Upload dashboard JSON file** → choix du dossier, de la source, titre et uid différents
- Conflit d'uid (tableaux de bord issus du rattrapage : même uid `tlc-reseau-regional` dans les deux instances) → en changer à l'import

**Critères de réussite** :
- [ ] Deux tableaux de bord régionaux dans `NOC Telcéa` (le sien, celui du binôme)
- [ ] Panels du tableau de bord importé avec des données (source locale choisie)

---

## Défi 08.4 ⭐⭐⭐ — Un panel de consignes partagé (autonome)
**Durée** : 10 min · **Objectif** : maintenir une seule fois un panel utilisé par plusieurs écrans
**Prérequis** : panel `Consignes du NOC` (défi 04.3) ; sinon, le créer (visualisation **Text**, astreinte radio poste 1001)
**Contexte** : les numéros d'astreinte changent chaque semaine ; ils sont affichés sur l'écran national ET sur l'écran mural.

**Énoncé** :
- Transformer le panel `Consignes du NOC` du tableau de bord national en library panel (dossier `NOC Telcéa`).
- L'ajouter à l'écran mural.
- Modifier le numéro d'astreinte radio (`1001` → `1011`) depuis un seul des deux tableaux de bord et vérifier l'autre.

**Critères de réussite** :
- [ ] Library panel listé dans **Dashboards → Library panels**, utilisé par 2 tableaux de bord
- [ ] Numéro `1011` affiché sur les deux écrans après une seule modification
