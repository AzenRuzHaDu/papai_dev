# Gemini CLI — Project Instructions

Ce fichier définit les règles et l'orchestration pour le développement du projet **PAI_DEV** avec Gemini.

## Rôles et Orchestration

Le projet suit un workflow structuré défini dans [.gemini/docs/orchestration.md](.gemini/docs/orchestration.md).
Chaque agent (PRD, Stack, Architecte, Dev, Review) a des responsabilités spécifiques et produit des livrables persistés dans `docs/`.

### Commandes (Modes de fonctionnement)

Lorsque l'utilisateur utilise l'une des commandes suivantes, active le mode correspondant en suivant les instructions du fichier associé :

- **/prd** : [Product Manager](.gemini/commands/prd.md) — Transforme une idée en PRD dans `docs/prd.md`.
- **/stack** : [Stack Expert](.gemini/commands/stack.md) — Définit la stack technique.
- **/architect** : [Architecte](.gemini/commands/architect.md) — Crée l'architecture et les stories.
- **/dev** : [Developer](.gemini/commands/dev.md) — Implémente une story spécifique.
- **/review** : [Reviewer](.gemini/commands/review.md) — Analyse et corrige le code.

## Règles Transverses

Applique strictement les règles définies dans [.gemini/docs/agent-rules.md](.gemini/docs/agent-rules.md) :

1. **Rédaction progressive** : Ne pas rédiger le livrable d'un bloc. Construire incrémentalement.
2. **Élicitation conversationnelle** : Poser les questions **une par une**, expliquer pourquoi, et proposer des options.
3. **Persistance** : Tous les livrables finaux DOIVENT être écrits dans des fichiers sous `docs/`.
4. **Validation** : Toujours attendre la validation utilisateur avant de persister ou de passer à l'étape suivante.

## Workflows Techniques

- **Git** : Suit [.gemini/docs/git-workflow.md](.gemini/docs/git-workflow.md). Utilise les Conventional Commits avec le tag `[gemini/nom-agent]`.
- **Tests** : Suit [.gemini/docs/testing-strategy.md](.gemini/docs/testing-strategy.md).
- **Stack** : Suit [.gemini/docs/stack-selection.md](.gemini/docs/stack-selection.md).

## Localisation des documents

- Documents de conception : `docs/`
- Stories : `docs/stories/*.md`
- Instructions Gemini : `.gemini/`
