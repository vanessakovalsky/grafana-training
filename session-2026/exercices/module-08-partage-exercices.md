# Module 08 — Exercices

Travail en binôme pour les échanges (voisin de salle ou de visio). Canal d'échange des liens et fichiers : messagerie de la session (Teams ou équivalent).

## Lab 08.1 ⭐ — Lien interne et lien externe (guidé)
**Durée** : 10 min · **Objectif** : partager une vue filtrée et figée avec un collègue, puis l'écran mural sans compte
**Contexte** : l'équipe *radio* signale un incident en Bretagne ; la direction veut suivre l'écran mural depuis son bureau, sans compte Grafana.
**Prérequis** : M06 (tableau de bord régional), M07 (écran mural)

### Étapes
1. Ouvrir `[TLC] Réseau — Détail régional`, Région `Bretagne`, plage `Last 1 hour`.
2. Bouton **Share** (barre du haut) → **Share internally** : activer **Lock time range** et **Shorten link** → **Copy link**.
   Résultat attendu : lien `https://stagiaireNN.<SESSION>.kovalibre-labs.com/grafana/goto/...` copié.
3. Coller le lien dans un nouvel onglet : vérifier la région `Bretagne` et la plage absolue (dates et heures affichées à la place de `Last 1 hour`).
4. Ouvrir `[TLC] NOC — Écran mural` → **Share** → **Share externally** : cocher « I understand that this entire dashboard will be public. » → **Accept** → **Copy external link**.
5. Ouvrir le lien externe dans une fenêtre de navigation privée (aucune session Grafana).
   Résultat attendu : écran mural affiché en lecture seule, sans menu ni connexion.
6. **Dashboards → Public dashboards** : repérer l'écran mural, puis **Pause access**, recharger la fenêtre privée.
   Résultat attendu : accès refusé tant que la pause est active ; réactiver ensuite.

### Critères de réussite
- [ ] Lien interne à plage figée et région conservée
- [ ] Écran mural visible sans compte, puis bloqué par la pause

---

## Lab 08.2 ⭐ — Snapshot d'incident (guidé)
**Durée** : 10 min · **Objectif** : figer l'état du tableau de bord national et transmettre le lien
**Contexte** : le prestataire de maintenance radio doit voir l'état du réseau à l'instant du signalement, sans accès aux requêtes ni aux sources.
**Prérequis** : tableau de bord national (M05)

### Étapes
1. `[TLC] Réseau — Vue nationale` → **Share** → **Share snapshot**.
2. **Snapshot name** : `[TLC] Réseau — état <HEURE>` ; **Expires in** : `1 Day` → **Publish snapshot** (et SURTOUT PAS **Publish to snapshots.raintank.io**).
   Résultat attendu : lien `.../grafana/dashboard/snapshot/...` → **Copy link**.
3. Envoyer le lien à la formatrice par la messagerie de la session (rôle du courriel au prestataire).
4. Ouvrir le snapshot : modifier la plage de temps, ouvrir un panel en édition.
   Résultat attendu : données figées, aucune requête visible.
5. **Dashboards → Snapshots** : retrouver le snapshot, noter sa date d'expiration.

### Critères de réussite
- [ ] Snapshot local publié, expiration 1 jour
- [ ] Lien transmis ; données identiques quelle que soit l'heure d'ouverture

---

## Exercice 08.3 ⭐⭐ — Échanger un tableau de bord avec son binôme (semi-autonome)
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
- Conflit d'uid : même uid `tlc-reseau-regional` dans les deux instances → en changer à l'import

**Critères de réussite** :
- [ ] Deux tableaux de bord régionaux dans `NOC Telcéa` (le sien, celui du binôme)
- [ ] Panels du tableau de bord importé avec des données (source locale choisie)

---

## Défi 08.4 ⭐⭐⭐ — Un panel de consignes partagé (autonome)
**Durée** : 10 min · **Objectif** : maintenir une seule fois un panel utilisé par plusieurs écrans
**Contexte** : les numéros d'astreinte changent chaque semaine ; ils sont affichés sur l'écran national ET sur l'écran mural.

**Énoncé** :
- Transformer le panel `Consignes du NOC` du tableau de bord national en library panel (dossier `NOC Telcéa`).
- L'ajouter à l'écran mural.
- Modifier le numéro d'astreinte radio (`1001` → `1011`) depuis un seul des deux tableaux de bord et vérifier l'autre.

**Critères de réussite** :
- [ ] Library panel listé dans **Dashboards → Library panels**, utilisé par 2 tableaux de bord
- [ ] Numéro `1011` affiché sur les deux écrans après une seule modification
