# PAI DEV

Framework de développement agent-driven pour Claude Code et Gemini CLI.

Transforme une idée en code implémenté via une chaîne d'agents spécialisés, chacun produisant un livrable validé avant le passage suivant.

## Workflow

```
Idée → /prd → /stack → /architect → /dev (story par story) → /review
```

```
                                              ┌── /dev story N → Dev Notes ──┐
                                              │                              │
                                              │   si impact: /architect      │
                                              │       (réconciliation)       │
                                              │                              │
                                              └──────── story N+1 ←──────────┘
```

## Commandes

| Commande | Rôle | Livrable |
|----------|------|----------|
| `/prd` | Product Manager — transforme une idée en PRD structuré | `docs/prd.md` |
| `/stack` | Sélection de stack technique | `docs/stack.md` |
| `/architect` | Architecture + découpage en stories | `docs/architecture.md` + `docs/stories/*.md` |
| `/dev` | Implémentation d'une story (code, tests, commit) | Code + story mise à jour |
| `/review` | Revue de code et corrections | Code corrigé |

## Utilisation

### Nouveau projet depuis ce template

```bash
gh repo create mon-projet --template=AzenRuzHaDu/papai_dev --clone
cd mon-projet
```

Ou via GitHub : bouton **"Use this template"** sur la page du repo.

### Lancer le workflow

```bash
# 1. Décrire l'idée
/prd

# 2. Choisir la stack (optionnel si déjà décidé)
/stack

# 3. Générer l'architecture et les stories
/architect

# 4. Implémenter story par story
/dev

# 5. Reviewer le code
/review
```

Chaque commande pose ses questions une par une, construit le livrable progressivement, et écrit le résultat dans `docs/`.

## Structure

```
.claude/
├── commands/          # Agents Claude Code (/prd, /architect, /dev, /review, /stack)
├── docs/              # Documentation de référence (framework)
└── project/           # Personnalisations projet (context.md, <agent>.md)
    ├── agent-rules.md
    ├── architectures/layered/
    ├── models/anemic.md
    ├── git-workflow.md
    ├── orchestration.md
    ├── stack-selection.md
    └── testing-strategy.md

.gemini/
├── commands/          # Agents Gemini CLI (mêmes commandes)
└── docs/              # Même documentation de référence

docs/                  # Livrables projet (générés par les agents)
```

## Principes

- **Rédaction progressive** — le livrable se construit au fil de la conversation
- **Élicitation une par une** — jamais de bloc de questions
- **Persistance** — ce qui n'est pas écrit dans `docs/` n'existe pas
- **Feedback loop** — dev notes après chaque story, réconciliation architecte si besoin
- **Pas de devinette** — si c'est flou, l'agent demande
