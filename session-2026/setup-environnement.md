# Préparation de l'environnement

Formation « Monitorer avec Grafana » (Grafana 13.3.1). Une VM par stagiaire, accessible depuis un navigateur ; aucun logiciel à installer sur le poste.

## 1. Côté stagiaire

| Besoin | Détail |
|---|---|
| Navigateur | Firefox, Chrome ou Edge récent |
| Réseau | Accès HTTPS (443) à `*.kovalibre-labs.com` (validé sur le réseau Orange) |
| Identifiants | URL de la VM et mot de passe, transmis le matin du J1 |

Accès :
- Grafana : `https://stagiaireNN.<SESSION>.kovalibre-labs.com/grafana/` (compte `admin`)
- Bureau Linux (terminal, Firefox local) : `https://stagiaireNN.<SESSION>.kovalibre-labs.com/` (compte `stagiaire`)
- Courriels de test : `https://stagiaireNN.<SESSION>.kovalibre-labs.com/mail/`

Contrôle (terminal du bureau) :
```bash
~/grafana-training/stack/preflight.sh
```
Sortie attendue (dernière ligne) :
```
Result: stack ready
```

## 2. Côté formatrice : provisionnement des VM

Outils : AWS CLI v2 configuré (EC2, VPC, Route53, SSM, IAM), `jq`, `curl`, `ssh`, dépôt `../vm-stagiaire`.

### 2.1 Configuration de la session
```bash
cp scripts/setup/config-grafana.env.example scripts/setup/config-grafana.env
# adapter SESSION (ex. grafana-2027-01) et NB_STAGIAIRES (stagiaires + 1 VM formatrice)
```
Variables : `<CONFIG>` = chemin absolu de `scripts/setup/config-grafana.env`.

### 2.2 Contraintes à vérifier (J-7)
| Contrainte | Commande | Attendu |
|---|---|---|
| Quota vCPU EC2 standard | `aws service-quotas get-service-quota --service-code ec2 --quota-code L-1216C47A --region eu-west-3` | ≥ 2 × NB_STAGIAIRES |
| Type d'instance | `aws ec2 describe-instance-type-offerings --filters Name=instance-type,Values=t3.medium --region eu-west-3` | Présent |
| Paquet stagiaire publié | Dépôt `vanessakovalsky/grafana-training`, sous-dossier de session contenant `stack/` | Présent |

### 2.3 Création (J-1, 14 h 00)
```bash
cd ../vm-stagiaire
./00-provision.sh <CONFIG>                      # ~10 min (XFCE, Guacamole, Nginx, Let's Encrypt)
./status.sh <CONFIG>                            # bootstrap=OK, https=200 pour chaque VM
./run-on-vms.sh <CONFIG> 'cd ~/grafana-training/<SOUS_DOSSIER>/stack && ./setup.sh'
./run-on-vms.sh <CONFIG> '~/grafana-training/stack/preflight.sh'
```
Variables : `<SOUS_DOSSIER>` = sous-dossier de la session dans le dépôt public (variable `ATELIERS_DIR` de la publication).

`setup.sh` (idempotent) : jeton InfluxDB, `.env` (mot de passe Grafana = mot de passe de la VM), images Docker, stack démarrée, publication de `/grafana/` et `/mail/` dans Nginx, Firefox (dépôt APT Mozilla), lien `~/grafana-training/stack`.

Distribution : `state/<SESSION>/stagiaires.csv` (URL, identifiant, mot de passe par VM).

### 2.4 Pendant la session
| Action | Commande (depuis le dépôt de la formation) |
|---|---|
| Rattrapage d'un module | `scripts/setup/sur-vms.sh <CONFIG> scripts/mXX/catch-up/<SCRIPT> [--data <FICHIER>] stagiaireNN` |
| Tempête (M09) | `scripts/m09/labs/tempete.sh <CONFIG> start` / `stop` / `etat` |
| VM supplémentaire | `../vm-stagiaire/add-vm.sh <CONFIG>` puis `setup.sh` sur la nouvelle VM |
| Après un redémarrage des VM | `../vm-stagiaire/dns-sync.sh <CONFIG>` |

Rattrapages disponibles : `m02/catch-up/organisation.sh`, `m03/catch-up/sources.sh`, `m04` et `m05/catch-up/dashboard.sh` (`--data tableau-de-bord.json`), `m06/catch-up/dashboard.sh` (`--data detail-regional.json`), `m07/catch-up/plugins-et-ecran.sh` (`--data ecran-mural.json`), `m09/catch-up/alerting.sh`, `m10/catch-up/droits.sh`, `m11/catch-up/dashboard.sh` (`--data croisement.json`).

## 3. Banc de test local (formatrice)

Poste avec Docker et Docker Compose v2 :
```bash
cd stack
GRAFANA_PORT=13000 ./setup.sh --local          # Grafana sur http://localhost:13000/grafana/
GRAFANA_PORT=13000 ./preflight.sh
GRAFANA_PORT=13000 ../scripts/setup/local.sh ../scripts/m05/catch-up/dashboard.sh \
  --data ../scripts/m05/catch-up/tableau-de-bord.json
```
Empreinte mémoire relevée : ≈ 1,1 Gio pour les 11 services.

## 4. Nettoyage (fin du J2, après récupération des exports)

| Ressource | Commande | Délai incompressible |
|---|---|---|
| VM, VPC, DNS, rôles IAM, planifications | `../vm-stagiaire/99-teardown.sh <CONFIG>` (confirmation « oui ») | Aucun |
| Banc local | `cd stack && docker compose down -v` | Aucun |
| Liens externes et snapshots | Supprimés avec les VM | — |

Coût indicatif : `t3.medium` ≈ 0,05 $/h `[À VÉRIFIER]` par VM, soit environ 40 $ pour 11 VM sur 3 jours sans arrêt nocturne.
