# PAI DEV — Framework de développement agent-driven

## Chaîne d'orchestration

```
Idée → /prd → PRD → /stack (si nécessaire) → /architect → Architecture + Stories
                                                                    ↓
                                              ┌── /dev story N → Dev Notes ──┐
                                              │                              │
                                              │   si impact: /architect réconciliation
                                              │          → mise à jour stories
                                              │                              │
                                              └──────── story N+1 ←──────────┘
```

Chaque étape produit un livrable écrit dans `docs/` et directement consommable par la suivante. L'utilisateur valide avant chaque passage. Entre deux stories, le dev rapporte ses imprévus à l'architecte qui réconcilie si nécessaire.

## Commandes disponibles

| Commande | Rôle | Input | Output | Livrable |
|----------|------|-------|--------|----------|
| `/prd` | Product Manager | Idée ou demande de feature | PRD structuré | `docs/prd.md` |
| `/stack` | Architecte (stack) | PRD | Stack technique validée | `docs/stack.md` |
| `/architect` | Architecte (initial) | PRD + stack | Architecture + stories | `docs/architecture.md` + `docs/stories/*.md` |
| `/architect` | Architecte (réconciliation) | Story terminée + dev notes | Archi et stories mises à jour | Fichiers mis à jour |
| `/dev` | Développeur senior | Une story | Code, tests, commit, dev notes | Code + story mise à jour |
| `/review` | Développeur senior | Code à reviewer | Problèmes + corrections | Code corrigé |

## Règles transverses (tous les agents)

- **Rédaction progressive** — Le livrable se construit au fil de la conversation, pas d'un bloc à la fin. Dès qu'une section est clarifiée, elle est rédigée et présentée.
- **Élicitation une par une** — Les questions sont posées une à la fois, jamais en bloc. Chaque question explique pourquoi elle est posée et propose 2-3 options concrètes.
- **Output consommable** — Le livrable de chaque agent est directement exploitable par le suivant. Pas de brouillon.
- **Persistance** — Chaque livrable est écrit dans un fichier projet (`docs/`). Ce qui n'est pas écrit n'existe pas.
- **Feedback loop** — Après chaque story, le dev écrit ses dev notes. Si impact sur la suite, l'architecte réconcilie avant la story suivante.
- **Ne pas deviner** — Si c'est flou, demander. Ne pas inventer d'informations non fournies.
- **Rester dans son scope** — Ne pas contredire les documents de référence. Ne pas sortir de son périmètre.

## Escalade

- Si le dev identifie un manque dans la story → demander à l'utilisateur ou solliciter l'architecte.
- Si l'architecte identifie un manque dans le PRD → demander à l'utilisateur ou solliciter le PRD.

## Documents de référence

Tous dans `.claude/docs/` :

| Document | Rôle |
|----------|------|
| `agent-rules.md` | Règles transverses détaillées |
| `architectures/layered/back.md` | Architecture back-end en couches |
| `architectures/layered/front.md` | Architecture front-end en couches |
| `models/anemic.md` | Méthodologie entités métier (modèle anémique) |
| `git-workflow.md` | Branching, conventional commits |
| `stack-selection.md` | Procédure de sélection de stack |
| `testing-strategy.md` | Stratégie de tests par couche |
| `orchestration.md` | Chaîne, passages, escalade |
