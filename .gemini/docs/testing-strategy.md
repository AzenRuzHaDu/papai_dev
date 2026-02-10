# Stratégie de tests

## Principe

Chaque couche a ses propres tests. On teste le comportement, pas l'implémentation. Les outils de test sont définis par la stack du projet — ce document définit **quoi** tester et **comment**, pas avec quoi.

---

## Back-end

### Business classes / Models

- **Type** : Tests unitaires
- **Quoi** : Constructeurs, getters, setters, valeurs par défaut, contraintes de type
- **Pas de mock** : Ce sont des objets purs, testés directement

### Repositories

- **Type** : Tests d'intégration
- **Quoi** : CRUD complet, cas limites (ID inexistant, doublons, liste vide)
- **Base de test** : Base réelle ou in-memory selon la stack

### Services

- **Type** : Tests unitaires avec mocks des repositories
- **Quoi** : Un test par cas d'usage nominal, un test par cas d'erreur documenté dans la story
- **Mock** : Les repositories sont mockés, les business classes sont réelles

### Controllers

- **Type** : Tests d'intégration (HTTP)
- **Quoi** : Status codes, format de réponse, validation des entrées (inputs invalides, champs manquants)
- **Pas de mock des services** si possible — tester la chaîne complète

---

## Front-end

### Components

- **Type** : Tests unitaires / snapshot
- **Quoi** : Rendu avec différentes props, interactions (click, input, submit), états visuels (loading, error, empty)

### Hooks / Composables

- **Type** : Tests unitaires
- **Quoi** : Transitions d'état (loading → success, loading → error), appels à l'API layer
- **Mock** : L'API layer est mockée

### API layer

- **Type** : Tests unitaires
- **Quoi** : Sérialisation des requêtes, désérialisation des réponses, gestion des erreurs HTTP
- **Mock** : Les appels HTTP sont mockés

---

## Règles générales

- **Pas de tests pour la config** — Ce sont des valeurs statiques.
- **Un test = un comportement** — Nommer par comportement : "should return 404 when user not found", pas "test getUserById".
- **Indépendance** — Chaque test tourne seul, sans ordre, sans état partagé.
- **Cas d'erreur obligatoires** — Si la story liste des cas d'erreur, ils doivent être testés.
- **Emplacement** — Les tests vivent à côté du fichier testé ou dans un dossier `__tests__/` parallèle, selon la convention du projet.
