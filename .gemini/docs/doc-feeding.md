# Doc Feeding — Vérification documentaire des technos

## Problème

Les LLM ont une date de coupure de données d'entraînement. Les technologies évoluent vite, surtout dans l'écosystème JavaScript/TypeScript, les SDK d'IA, et les frameworks frontend. Un agent qui code avec des API obsolètes produit du code qui ne compile pas ou qui utilise des patterns dépréciés.

## Solution

Avant de coder, vérifier les API dans la documentation officielle et consigner les patterns confirmés dans un fichier de contexte projet. Le dev lit ce fichier et dispose des liens de doc pour lever ses doutes en cours d'implémentation.

## Quand exécuter

- **Systématiquement** après le `/review stories` et avant le premier `/dev` — c'est une étape obligatoire de la chaîne.
- **À la demande** pendant le dev si une techno non couverte pose problème.
- **En mise à jour** quand une nouvelle techno est ajoutée au stack ou qu'une version change.

## Technos à risque

Une techno est "à risque" si :
- Sa version dans le stack est récente (< 1-2 ans)
- Elle évolue rapidement (releases fréquentes, breaking changes entre mineures)
- Elle est en pre-1.0 ou en beta
- Son API est complexe et spécifique (pas juste du CRUD)
- Le projet en dépend lourdement

Une techno est "stable" si :
- Son API est mature et n'a pas changé significativement depuis des années
- Elle est largement documentée et connue (Express, PostgreSQL, React de base, etc.)

## Format du contexte

Le fichier `.gemini/project/context.md` contient :
- Pour chaque techno vérifiée : un lien doc officielle, les patterns confirmés, les points d'attention
- Uniquement des informations vérifiées dans la doc — pas de suppositions
- La date de dernière mise à jour

Ce fichier est lu par le dev agent à chaque activation. Les liens permettent au dev de vérifier directement en cas de doute pendant l'implémentation.

## Règles

- Ne documenter que ce qui est pertinent pour le projet (pas toute l'API d'une techno)
- Préférer un exemple de code court à une explication longue
- Signaler explicitement les breaking changes par rapport aux versions antérieures populaires
- Le fichier est incrémental : on ajoute, on ne repart pas de zéro
