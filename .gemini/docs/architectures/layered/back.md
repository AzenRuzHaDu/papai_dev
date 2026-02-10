# Architecture en couches — Back-end

## Principes fondamentaux

Chaque couche a une responsabilité unique et ne communique qu'avec les couches adjacentes. Les dépendances vont toujours dans le même sens : de l'extérieur (point d'entrée) vers l'intérieur (métier).

---

## Couches

### Controllers

**Rôle** : Point d'entrée de l'application. Reçoit les requêtes (HTTP, WebSocket, événements), valide les entrées, délègue aux services et retourne une réponse.

**Règle SRP** : Un controller ne contient aucune logique métier. Il ne fait que router, valider et répondre. Un controller par ressource ou domaine fonctionnel.

**Interdit** : Accès direct à la base de données, logique conditionnelle métier, transformation complexe de données.

### Services

**Rôle** : Logique applicative. Orchestre les appels aux repositories et aux business classes pour répondre à un cas d'usage. Gère les transactions, la coordination entre domaines et les règles applicatives.

**Règle SRP** : Un service correspond à un domaine fonctionnel. Il ne connaît pas le transport (HTTP, CLI...) et n'accède pas directement aux données — il passe par les repositories.

**Interdit** : Référence au contexte HTTP (request, response), requêtes SQL/ORM directes, logique de présentation.

### Repositories

**Rôle** : Accès aux données. Abstrait la source (BDD, API externe, fichiers). Expose des méthodes claires (findById, save, delete) qui retournent des business classes.

**Règle SRP** : Un repository par entité ou agrégat. Il ne contient pas de logique métier — uniquement de la lecture/écriture de données.

**Interdit** : Logique conditionnelle métier, appels à d'autres repositories, connaissance du format de réponse HTTP.

### Business classes (Models)

**Rôle** : Représentation du domaine métier. Entités, value objects, DTOs. Portent les règles métier intrinsèques (validation, calculs, états).

**Règle SRP** : Une classe par concept métier. Les règles qu'elle porte ne concernent qu'elle-même — pas d'orchestration, pas d'effets de bord.

**Interdit** : Import de services, accès aux données, logique applicative.

### Config

**Rôle** : Centralise toute la configuration de l'application. Variables d'environnement, constantes métier, paramètres de connexion, feature flags, valeurs par défaut.

**Règle SRP** : Un fichier par domaine de configuration (database, auth, mail, app...). Ne contient que des valeurs et leur lecture — aucune logique.

**Interdit** : Logique métier, import de services/repositories, effets de bord. Aucun code exécutable autre que la lecture de variables d'environnement.

---

## Patterns optionnels

### DTOs (Data Transfer Objects)

**Rôle** : Objet de transport entre les couches, distinct des business classes. Définit un contrat explicite pour ce qui entre (RequestDTO) et ce qui sort (ResponseDTO) d'un service.

**Où il s'insère** : Entre controllers et services. Le controller reçoit un DTO en entrée, le service retourne un DTO en sortie. Les business classes restent internes au domaine.

**Quand l'utiliser** : Ce n'est pas systématique. L'agent architect doit évaluer les critères suivants pour chaque ressource/endpoint :

- L'entité métier expose-t-elle des champs sensibles ou internes (hash, IDs techniques, timestamps internes) ?
- La forme de la requête ou de la réponse diffère-t-elle du modèle interne ?
- A-t-on besoin de versionner l'API sans toucher au domaine ?
- Plusieurs consumers (front, mobile, API publique) consomment-ils la même ressource avec des besoins différents ?

Si au moins un critère est vrai → DTO à cette frontière. Si aucun → le modèle peut passer directement.

**Règle SRP** : Un DTO ne contient aucune logique. C'est une structure de données pure avec éventuellement de la validation d'entrée (annotations, décorateurs).

**Interdit** : Logique métier, accès aux données, import de services.

---

## Flux

```
Request → Controller → Service → Repository → DB
                         ↕
                   Business Class

Config → accessible par toutes les couches (injection/import)
```
