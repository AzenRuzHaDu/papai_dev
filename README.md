# PAPAI_DEV

Framework de développement agent-driven pour Claude Code et Gemini CLI. On le manipule avec une **foufourche**. Le dev, c'est du sérieux.

Transforme une idée en code implémenté via une chaîne d'agents spécialisés, chacun produisant un livrable validé avant le passage suivant.

## Workflow

```
Idée → /prd → /stack → /architect → /review stories → /doc-feed → /dev (story par story) → /review code
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
| `/doc-feed` | Vérification doc des technos récentes | `.claude/project/context.md` |
| `/review` | Revue de code et corrections | Code corrigé |

## Installation

### foufourche — la fourche du dev sérieux

`foufourche` crée des projets depuis ce template et les met à jour quand le framework évolue. C'est l'outil de base de la PAPAI_DEV.

```bash
# Copier le script dans le PATH
cp bin/foufourche ~/.local/bin/
chmod +x ~/.local/bin/foufourche
```

> `~/.local/bin/` doit être dans votre `$PATH`. Sinon, ajoutez `export PATH="$HOME/.local/bin:$PATH"` dans votre `.bashrc` ou `.zshrc`.

### Prérequis

- [GitHub CLI](https://cli.github.com/) (`gh`) — authentifié
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (`claude`) et/ou [Gemini CLI](https://github.com/google-gemini/gemini-cli) (`gemini`)

## Utilisation

### Nouveau projet

```bash
foufourche mon-projet                  # crée le projet, lance Claude
foufourche -g mon-projet               # crée le projet, lance Gemini
foufourche mon-projet ~/Projects       # répertoire parent custom
```

Ou manuellement :

```bash
gh repo create mon-projet --template=AzenRuzHaDu/papai_dev --clone
cd mon-projet
```

### Mettre à jour le framework

```bash
cd mon-projet
foufourche -u                          # merge les dernières évolutions du framework
```

Les personnalisations dans `.claude/project/` ne sont jamais en conflit.

### Configuration

Par défaut, `foufourche` lance Claude. Pour changer le défaut :

```bash
mkdir -p ~/.config/foufourche
echo 'CLI=gemini' > ~/.config/foufourche/config
```

Les options `-c` (Claude) et `-g` (Gemini) surchargent la config ponctuellement.

### Lancer le workflow

```bash
# 1. Décrire l'idée
/prd

# 2. Choisir la stack (optionnel si déjà décidé)
/stack

# 3. Générer l'architecture et les stories
/architect

# 4. Valider les stories avant dev
/review stories

# 5. Vérifier les docs des technos récentes
/doc-feed

# 6. Implémenter story par story
/dev

# 7. Reviewer le code
/review
```

Chaque commande pose ses questions une par une, construit le livrable progressivement, et écrit le résultat dans `docs/`.

## Structure

```
bin/
└── foufourche         # CLI : création et mise à jour de projets

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
