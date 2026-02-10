# Règles transverses — Agents

Ce document s'applique à **tous les agents** du framework. Chaque agent doit le lire avant de commencer.

## Rédaction progressive

L'agent ne rédige **pas** son livrable d'un bloc à la fin. Il rédige au fur et à mesure de la conversation :

- Dès qu'une section est clarifiée, l'agent la rédige et la présente.
- L'utilisateur peut corriger immédiatement, avant de passer à la suite.
- Le livrable se construit incrémentalement pendant l'échange.
- À la fin, l'agent présente le document complet pour validation finale.

## Élicitation conversationnelle

- Les questions sont posées **une par une**, pas en bloc.
- Chaque question explique **pourquoi** elle est posée (quel impact sur le livrable).
- L'agent propose **2-3 options** concrètes quand c'est possible.
- L'agent ne pose pas de questions dont la réponse est déjà dans le contexte.
- L'agent ne devine pas. Si c'est flou, il demande.

## Output directement consommable

- Le livrable de chaque agent est **directement exploitable** par l'agent suivant dans la chaîne.
- Pas de brouillon, pas de document qui nécessite une transformation.

## Persistance des livrables

- Chaque agent **écrit** son livrable final dans un fichier projet (dans `docs/`).
- Ce qui n'est pas persisté n'existe pas — la conversation ne suffit pas.
- L'agent écrit le fichier **après validation** par l'utilisateur, pas avant.
- Les agents suivants dans la chaîne **lisent** les livrables des agents précédents depuis `docs/`.

## Boucle de feedback dev → architecte

- Après chaque story, le dev rédige ses **dev notes** directement dans le fichier de la story (section `## Dev Notes`).
- Les dev notes capturent les écarts, imprévus et impacts potentiels sur les stories suivantes.
- Si les dev notes signalent un impact, l'architecte est sollicité en **mode réconciliation** pour mettre à jour l'architecture et les stories concernées.
- L'architecte ne réécrit que ce qui est impacté — pas de refonte globale.

## Ce que tout agent ne fait pas

- Sortir de son scope (défini dans son propre fichier).
- Contredire les documents de référence.
- Poser toutes les questions d'un coup.
- Inventer des informations non fournies par l'utilisateur.
- Produire un livrable sans le persister dans un fichier.
