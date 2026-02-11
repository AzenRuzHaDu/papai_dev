# Format du backlog inter-versions

## Rôle

`docs/backlog.md` est la mémoire des évolutions futures. Il capture tout ce qui est consciemment reporté pour ne pas le perdre.

## Qui écrit

- **PRD** — quand l'utilisateur classe une feature en "Vision (vN+1+)" ou "Hors scope"
- **Architecte** — quand il simplifie une story ou reporte une feature pendant la conception
- **Dev** — quand il découvre un besoin hors scope pendant l'implémentation

## Qui lit

- **PRD** — à chaque activation. S'il existe, il propose les éléments pertinents par rapport à la demande courante.
- **Architecte** — en mode initial uniquement, comme contexte pour anticiper les points d'extension. Pas en réconciliation.
- **Dev** — lit le backlog uniquement au moment d'y écrire, pour vérifier les doublons. Pas de lecture au démarrage.

## Format du fichier `docs/backlog.md`

```markdown
# Backlog — Évolutions futures

## Reporté depuis vN

### [Depuis PRD] Titre de l'élément
- **Origine** : PRD vN — décision utilisateur
- **Raison du report** : pourquoi ce n'est pas dans cette version
- **Contexte** : détails utiles pour reprendre le sujet plus tard

### [Depuis Architecture] Titre de l'élément
- **Origine** : Architecture vN — story X
- **Raison du report** : complexité, dépendance, hors scope MVP
- **Contexte** : impact anticipé, points d'attention

### [Depuis Dev] Titre de l'élément
- **Origine** : Dev — story N, dev notes
- **Raison du report** : découvert en implémentation, hors scope
- **Contexte** : détails techniques, suggestion d'approche
```

## Règles

- Chaque entrée a une **origine** (quel agent, quelle version, quel moment)
- Chaque entrée a une **raison du report** (pas juste "hors scope" — pourquoi)
- Chaque entrée a un **contexte** suffisant pour reprendre le sujet sans devoir relire toute l'historique
- Quand un élément est intégré dans une nouvelle version, il est **retiré** du backlog par le PRD
- Le backlog ne remplace pas le PRD — c'est un input pour le PRD, pas un livrable autonome
