# Git Workflow

## Branches

Trois niveaux de branches, pas plus.

### `main`

- Branche de production. Toujours déployable.
- On ne commit **jamais** directement sur `main`.
- Alimentée uniquement par des merges depuis `dev`.

### `dev`

- Branche d'intégration. C'est ici que les features convergent.
- On ne commit **jamais** directement sur `dev` (sauf hotfix documentation triviale).
- Alimentée par des merges depuis les branches `feature/`.

### `feature/*`

- Une branche par fonctionnalité ou fix.
- Nommage : `feature/nom-court-en-kebab-case` ou `fix/nom-court-en-kebab-case`.
- Durée de vie courte : quelques heures à quelques jours max.
- Créée depuis `dev`, mergée dans `dev`.

```
main ← dev ← feature/mon-truc
              feature/mon-fix
```

## Releases

Rolling releases. Quand `dev` est stable et testé, on merge dans `main`.

Pas de branche `release/`. Pas de tags de version sauf si le projet distribue un package (npm, PyPI, etc.) — dans ce cas, tag `vX.Y.Z` sur `main` après merge.

## Conventional Commits

Chaque commit suit le format [Conventional Commits](https://www.conventionalcommits.org/).

```
type(scope): description courte [llm/agent]
```

Le tag `[llm/agent]` identifie quel LLM et quel agent a produit le commit. Exemples : `[claude/dev]`, `[gpt4/planner]`, `[gemini/review]`. Pas de tag = commit humain.

### Types

| Type | Usage |
|------|-------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `refactor` | Refactoring sans changement de comportement |
| `docs` | Documentation uniquement |
| `test` | Ajout ou modification de tests |
| `chore` | Maintenance (deps, config, CI) |
| `style` | Formatage, lint (pas de changement de logique) |

### Scope

Le scope est optionnel mais recommandé. Il désigne le module ou la couche concernée.

```
feat(auth): add JWT refresh token endpoint [claude/dev]
fix(booking-service): handle overlapping time slots [claude/dev]
docs(architecture): add DTO decision rationale [claude/architect]
test(user-repo): add edge case for duplicate email [claude/tester]
refactor(auth): extract token validation to service
```

Le dernier exemple n'a pas de tag — c'est un commit humain.

### Règles

- Description en **anglais**, en **minuscules**, sans point final.
- Un commit = un changement atomique. Pas de commits fourre-tout.
- Si un commit nécessite un paragraphe d'explication, ajouter un body après une ligne vide.

```
fix(payment): prevent double charge on retry [claude/dev]

The payment service was not checking idempotency keys before
processing. Added check against the transactions table.
```

## Workflow quotidien

```bash
# 1. Créer une branche feature depuis dev
git checkout dev
git pull origin dev
git checkout -b feature/ma-feature

# 2. Travailler, commiter régulièrement
git add .
git commit -m "feat(scope): description [llm/agent]"

# 3. Mettre à jour depuis dev avant de merger
git checkout dev
git pull origin dev
git checkout feature/ma-feature
git rebase dev

# 4. Merger dans dev
git checkout dev
git merge feature/ma-feature
git push origin dev

# 5. Supprimer la branche feature
git branch -d feature/ma-feature
```

## Merge dans main

```bash
git checkout main
git pull origin main
git merge dev
git push origin main
```

Pas de squash sur le merge `dev → main` — on garde l'historique lisible grâce aux conventional commits.

## Quand un autre dev intervient

- Il travaille sur sa propre branche `feature/` depuis `dev`.
- Rebase sur `dev` avant de merger.
- Pas de merge commits inutiles : `rebase` plutôt que `merge` pour synchroniser.
