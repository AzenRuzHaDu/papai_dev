# Orchestration

## Chaîne principale

```
Idée → /prd → PRD → /stack → Stack → /architect → Architecture + Stories
         ↓            ↓                    ↓
    docs/prd.md   docs/stack.md    docs/architecture.md
                                   docs/stories/*.md
                                          ↓
                                   /review stories → Rapport
                                          ↓
                                   feu vert → /dev
                                   bloquants → /architect (corrections)

         ↕ (lecture/écriture)
      docs/backlog.md
```

`/stack` est optionnel si la stack est déjà connue. `/architect` vérifie que `docs/stack.md` existe avant de commencer. `/review stories` est **obligatoire** entre l'architecte et le dev — les stories ne passent en dev qu'après feu vert du reviewer.

### Backlog inter-versions

`docs/backlog.md` est un fichier transverse alimenté par tous les agents (PRD, architecte, dev) quand un élément est reporté. Le PRD le lit à chaque activation et propose les éléments pertinents par rapport à la demande courante.

## Boucle de développement

```
          ┌─────────────────────────────────────────────────┐
          │                                                 │
/dev story N → Code + Tests → Commit → Dev Notes ──┐       │
                                                    │       │
                                   dev notes vides? │       │
                                    ├── oui → story N+1 ───┘
                                    └── non → /architect (réconciliation)
                                                    │
                                              mise à jour archi
                                              + stories impactées
                                                    │
                                              story N+1 ──────┘
```

Le dev implémente une story, écrit ses dev notes, et passe la main à l'architecte si des imprévus impactent la suite. L'architecte met à jour l'architecture et les stories concernées. Puis le dev reprend la story suivante.

## Agents

| Agent | Commande | Mode | Input | Output | Livrable |
|-------|----------|------|-------|--------|----------|
| PRD | `/prd` | — | Idée ou demande de feature | PRD | `docs/prd.md` |
| Stack | `/stack` | — | PRD | Stack technique validée | `docs/stack.md` |
| Architecte | `/architect` | initial | PRD + stack | Architecture + stories | `docs/architecture.md` + `docs/stories/*.md` |
| Architecte | `/architect` | corrections | Rapport review stories | Stories corrigées | Stories + archi mis à jour |
| Architecte | `/architect` | réconciliation | Story terminée + dev notes | Archi et stories mises à jour | Fichiers mis à jour |
| Dev | `/dev` | — | Une story | Code, tests, commit, dev notes | Code + story mise à jour |
| Review | `/review` | code | Code à reviewer | Problèmes + corrections | Code corrigé |
| Review | `/review` | stories | Stories de l'architecte | Rapport de validation | Feu vert ou corrections |

## Règles de passage

- Chaque agent attend la **validation utilisateur** avant que son output soit considéré comme terminé.
- Chaque agent **persiste** son livrable dans `docs/` après validation.
- L'output d'un agent est directement consommable par le suivant, sans transformation.
- Les agents suivants **lisent** les livrables des agents précédents depuis `docs/`.
- Le dev agent reçoit **une story à la fois**, pas le document d'architecture complet.
- Entre deux stories, le dev **rapporte** à l'architecte via les dev notes. L'architecte réconcilie si nécessaire avant que le dev continue.
- Le passage `/architect` → `/dev` exige un `/review stories` avec feu vert. Pas de dev sans review stories validé.

## Escalade

- Si le dev identifie un manque dans la story → il demande à l'utilisateur ou demande à solliciter l'architecte.
- Si l'architecte identifie un manque dans le PRD → il demande à l'utilisateur ou demande à solliciter le PRD.

## Documents transverses

Tous les agents lisent `.gemini/docs/agent-rules.md` avant de commencer. Chaque agent a ses propres références listées dans sa section "Activation".

`docs/backlog.md` est alimenté par tous les agents. Lecture : `/prd` à chaque activation, `/architect` en mode initial uniquement. Le dev y écrit mais ne le lit pas.

## Personnalisation projet

`.gemini/project/` contient les instructions projet :
- `context.md` — contexte partagé (tous les agents)
- `<agent>.md` — instructions additionnelles par agent

Complète le framework sans le remplacer. Contradiction explicite → projet prend le pas.
