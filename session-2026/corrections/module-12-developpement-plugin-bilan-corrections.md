# Module 12 — Corrections

## Lab 12.1 ⭐ — Lire un plugin généré
### Solution
| Élément | Valeur | Fichier |
|---|---|---|
| Type | `panel` | `src/plugin.json` |
| Identifiant | `telcea-nocstatus-panel` | `src/plugin.json` |
| Compatibilité | `"grafanaDependency": ">=13.2.0"` | `src/plugin.json` |
| Options de l'éditeur | `text` (Simple text option), `showSeriesCount` (Show series counter), `seriesCountSize` (Series counter size) | `src/module.ts` |
| Rendu React | `src/components/SimplePanel.tsx` | `arborescence.txt` |
| Grafana de développement | `docker-compose.yaml` (+ `.config/docker-compose-base.yaml`) | `arborescence.txt` |

### Pourquoi
- `grafanaDependency` : Grafana refuse de charger le plugin sur une version plus ancienne (critère de la grille d'évaluation du M07).
- Options déclarées dans `module.ts` : ce sont celles affichées à droite de l'éditeur de panel (même mécanique que les plugins installés au M07).

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| `%VERSION%` lu comme version | Valeur remplacée à la construction (`npm run build`) | Version réelle dans `package.json` |

## Exercice 12.2 ⭐⭐ — QCM final
Réponses et barème : `evaluation-finale.md` (document formatrice, non distribué avant l'évaluation).

## Défi 12.3 ⭐⭐⭐ — Générer et lancer son premier panel
### Solution
```bash
npx @grafana/create-plugin@latest \
  --plugin-type=panel --plugin-name=noc-status --org-name=telcea --no-backend
cd telcea-nocstatus-panel
npm install
npm run dev            # terminal 1
docker compose up      # terminal 2
```
Sortie de la génération (banc, 18/11/2026, Node.js 22.16) :
```
 ✓ Scaffolded telcea-nocstatus-panel panel plugin
 ✓ Added basic E2E test (Playwright)
 ✓ Set up provisioning for basic dashboard and TestData data source instance
 ✓ Configured development environment (Docker)
 ✓ Added default GitHub actions for CI, releases and Grafana compatibility
```
`npm install` et `docker compose up` non exécutés au banc : sorties à relever lors du premier essai.

### Pourquoi
- Squelette complet (tests, CI GitHub, environnement Docker) : seul le code du panel reste à écrire.
- Le squelette 9.x contient aussi des fichiers de consignes pour assistants de code (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`).

### Erreurs fréquentes
| Symptôme | Cause | Déblocage |
|---|---|---|
| `EBADENGINE Unsupported engine` | Node.js trop ancien (constaté au banc avec 22.16 : avertissement non bloquant) | Node.js 22 récent ou 24 LTS |
| Panel absent de Grafana | `npm run dev` non lancé (`dist/` vide) | Lancer la compilation avant `docker compose up` |
| Port 3000 occupé | Autre Grafana sur le poste | Arrêter l'autre instance ou changer le port dans `docker-compose.yaml` |

## QCM — Réponses
1. **A** — `npx @grafana/create-plugin@latest`.
2. **D** — `src/plugin.json`, champ `grafanaDependency`.
3. **C** — React et TypeScript (Angular retiré en Grafana 12).
4. **B** — `<organisation>-<nom>-<type>`.
5. **C** — Compilation continue en développement.
6. **A** — `allow_loading_unsigned_plugins` (section `[plugins]`), en développement uniquement.
