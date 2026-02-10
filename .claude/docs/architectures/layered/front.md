# Architecture en couches — Front-end

## Principes fondamentaux

Chaque couche a une responsabilité unique et ne communique qu'avec les couches adjacentes. Les dépendances vont toujours dans le même sens : de l'extérieur (UI) vers l'intérieur (données). Le front-end transpose le modèle en couches du back avec des équivalents adaptés au contexte navigateur.

---

## Couches

### Pages / Routes

**Rôle** : Équivalent des controllers. Point d'entrée d'une route. Compose les layouts, les composants et les hooks pour assembler un écran complet.

**Règle SRP** : Une page orchestre mais ne contient pas de logique métier inline. Elle branche les hooks aux composants. Pas de fetch direct, pas de state management complexe dans le corps de la page.

**Interdit** : Appels API directs, logique métier, styles globaux, composants UI inline de plus de quelques lignes.

### Layouts

**Rôle** : Squelettes structurels qui encadrent les pages. Gèrent la navigation globale (navbar, sidebar, footer) et la grille de mise en page.

**Règle SRP** : Un layout par contexte (auth, dashboard, public, onboarding...). Il gère la coquille visuelle, pas le contenu. S'il a besoin de données (ex: user connecté), il les reçoit via un hook — jamais en appelant l'API directement.

**Interdit** : Logique métier, appels API, state management local lié au contenu de la page.

### Components

**Rôle** : UI pure et réutilisable. Reçoit des props, émet des événements. Aucune connaissance du contexte global de l'application.

**Règle SRP** : Un composant = un élément d'interface. Props in, events out. Si un composant dépasse ~150 lignes, il doit être décomposé. Aucun fetch, aucun accès au store global.

**Interdit** : Appels API, accès direct au routeur, logique métier, effets de bord non liés à l'UI.

### Hooks / Composables

**Rôle** : Équivalent des services. Encapsulent la logique métier, la gestion d'état et l'orchestration. Pont entre l'API layer et les composants.

**Règle SRP** : Un hook par domaine fonctionnel ou cas d'usage (useAuth, useCart, useBooking...). Il appelle l'API layer pour les données, jamais fetch directement. Il expose un état et des actions aux pages/composants.

**Interdit** : Appels HTTP directs (passer par l'API layer), manipulation du DOM, logique de présentation/style.

### API layer

**Rôle** : Équivalent des repositories. Centralise tous les appels HTTP. Gère la sérialisation, la désérialisation, les headers, l'authentification, la gestion d'erreurs réseau.

**Règle SRP** : Un fichier par ressource ou domaine (authApi, bookingApi, userApi...). Retourne des données typées (models). Ne connaît rien de l'UI.

**Interdit** : Logique métier, gestion d'état, référence aux composants ou hooks.

### Models / Types

**Rôle** : Équivalent des business classes. Interfaces, types, DTOs, enums. Définissent la forme des données manipulées par l'application.

**Règle SRP** : Un fichier par entité ou domaine. Portent les types et éventuellement des fonctions utilitaires pures liées au modèle (formatage, validation).

**Interdit** : Import de hooks, de composants ou de l'API layer. Aucun effet de bord.

### Config

**Rôle** : Centralise toute la configuration front. Strings d'interface (labels, messages, placeholders), constantes (routes, breakpoints, durées d'animation), feature flags, URLs d'API, clés publiques.

**Règle SRP** : Un fichier par domaine (routes.ts, labels.ts, api.ts, theme.ts...). Ne contient que des valeurs exportées — aucune logique.

**Interdit** : Logique métier, import de hooks/composants/API layer, effets de bord. Aucun code exécutable.

### Lib / Utils

**Rôle** : Fonctions utilitaires pures, partagées entre les couches. Formatters, validators, helpers de date, constantes.

**Règle SRP** : Chaque utilitaire est une fonction pure — même entrée = même sortie, zéro effet de bord. Regroupés par domaine (format.ts, validation.ts, date.ts).

**Interdit** : Import de hooks, composants, API layer. Aucun état, aucun effet de bord.

---

## Patterns optionnels

### DTOs (Data Transfer Objects)

**Rôle** : Objet de transformation entre ce que l'API renvoie et ce que l'UI consomme. Permet de découpler le format serveur du format front.

**Où il s'insère** : Dans l'API layer. C'est lui qui mappe la réponse brute de l'API vers un type "front-friendly" utilisé par les hooks/composables.

**Quand l'utiliser** : Ce n'est pas systématique. L'agent architect doit évaluer les critères suivants :

- La structure de la réponse API diffère-t-elle significativement de ce que l'UI consomme (nommage, imbrication, champs superflus) ?
- Faut-il agréger plusieurs appels API en un seul objet côté front ?
- Le back renvoie-t-il des formats bruts qui nécessitent une transformation (dates, enums, unités) ?

Si au moins un critère est vrai → mapper via un DTO dans l'API layer. Si la réponse API correspond déjà aux types/models front → pas de DTO, les types dans `models/` suffisent.

**Règle SRP** : Un DTO est une fonction de mapping pure ou un type de transport. Aucune logique métier, aucun état.

**Interdit** : Logique métier, import de hooks/composants, effets de bord.

---

## Flux

```
Route → Page → Layout + Components
                ↕
          Hook/Composable → API Layer → HTTP
                ↕
             Model/Type

Config → accessible par toutes les couches (import)
Lib    → accessible par toutes les couches (import)
```
