# Méthodologie — Définition des classes métier

## Objectif

Déterminer les bonnes entités métier d'un projet, avec les bons attributs et les bonnes relations entre elles. Ce guide est à suivre **avant** toute implémentation, dès la phase d'architecture.

---

## Étape 1 — Identifier les entités

Partir du besoin (brief client, user stories, conversation de cadrage) et extraire les **substantifs récurrents** qui représentent des concepts concrets du domaine.

**Méthode** :
- Lire le besoin et surligner tous les noms/substantifs
- Filtrer : garder uniquement ceux qui ont une existence propre dans le système (on peut les créer, les lire, les modifier, les supprimer)
- Ignorer les concepts purement techniques (session, token, cache) — ce ne sont pas des entités métier

**Questions à se poser** :
- Est-ce que ce concept a un cycle de vie dans l'application (il est créé, il évolue, il peut être supprimé) ?
- Est-ce qu'un utilisateur ou le système a besoin de le référencer de façon unique ?
- Si je le supprime, est-ce que d'autres concepts sont impactés ?

**Exemple** : Pour une app de réservation de salon de coiffure, les substantifs récurrents seraient : Salon, Client, Coiffeur, Prestation, Créneau, Réservation, Avis.

**Piège courant** : Confondre un attribut avec une entité. "Adresse" est souvent un groupe d'attributs sur Salon, pas une entité à part — sauf si elle a un cycle de vie propre (ex: un carnet d'adresses).

---

## Étape 2 — Définir les attributs

Pour chaque entité identifiée, lister ses attributs en se posant : **qu'est-ce qui décrit cette entité ? Qu'est-ce qu'on a besoin de stocker sur elle ?**

**Méthode** :
- Repasser sur le besoin en cherchant les adjectifs et les informations associées à chaque entité
- Typer chaque attribut (string, number, date, boolean, enum...)
- Identifier les attributs obligatoires vs optionnels
- Identifier les attributs dérivés (calculés à partir d'autres attributs)

**Questions à se poser** :
- Cet attribut appartient-il vraiment à cette entité ou à une autre ?
- Cet attribut est-il une donnée stockée ou un calcul (ex: "âge" = dérivé de "date de naissance") ?
- Est-ce qu'un attribut cache en fait une entité (ex: si "catégorie" a un nom, une description et une icône → c'est probablement une entité)

**Exemple** :
```
Réservation
├── id: string
├── date: datetime
├── statut: enum (confirmée, annulée, terminée)
├── prix: number (dérivé de la prestation)
├── note_client: string (optionnel)
├── créée_le: datetime
└── modifiée_le: datetime
```

**Piège courant** : Mettre trop d'attributs sur une entité. Si un groupe d'attributs forme un bloc cohérent qui revient sur plusieurs entités (ex: adresse = rue + ville + code postal), envisager de le factoriser en créant une entité séparée.

---

## Étape 3 — Définir la structure de chaque entité

Une entité est un **conteneur de données pur** : un constructeur, des getters, des setters. Elle ne porte **aucune logique métier** — c'est le rôle des services.

**Méthode** :
- Définir le constructeur avec les attributs obligatoires
- Exposer les attributs via getters/setters
- Typer strictement chaque attribut

**Questions à se poser** :
- Quels attributs sont requis à la création (paramètres du constructeur) ?
- Quels attributs ont une valeur par défaut ?
- Quels attributs sont en lecture seule (getter sans setter) ?

**Exemple** :
```
Réservation
├── constructor(client, prestation, coiffeur, créneau)
├── id: string (readonly)
├── date: datetime
├── statut: enum (confirmée, annulée, terminée) — défaut: confirmée
├── prix: number
├── note_client: string (optionnel)
├── créée_le: datetime (readonly)
└── modifiée_le: datetime
```

**Rappel** : La logique comme "vérifier si la réservation est annulable" ou "calculer le prix" vit dans un `ReservationService`, pas dans l'entité. L'entité ne sait rien faire — elle se contente de stocker.

---

## Étape 4 — Tracer les relations

Définir comment les entités se connaissent et interagissent.

**Méthode** :
- Pour chaque paire d'entités, se demander : est-ce qu'elles ont un lien ?
- Qualifier le lien avec la terminologie standard
- Définir le sens de la relation et la propriété (qui porte la clé étrangère ?)

**Types de relations** :

- **OneToOne** : Une entité est liée à exactement une autre. Ex: Salon → Adresse.
- **OneToMany** : Un parent possède plusieurs enfants. Côté parent, c'est une collection. Ex: Salon → Coiffeurs (un salon a plusieurs coiffeurs).
- **ManyToOne** : L'inverse du OneToMany, vu du côté enfant. L'enfant porte la référence vers le parent. Ex: Coiffeur → Salon (un coiffeur appartient à un salon).
- **ManyToMany** : Les deux entités peuvent être liées à plusieurs instances de l'autre. Souvent matérialisée par une table/entité intermédiaire. Ex: Coiffeur ↔ Prestation (un coiffeur maîtrise plusieurs prestations, une prestation peut être réalisée par plusieurs coiffeurs).

**Questions à se poser** :
- Si je supprime l'entité A, qu'arrive-t-il à l'entité B ? (cascade ou non)
- L'entité A peut-elle exister sans l'entité B ?
- Qui porte la clé étrangère ? (c'est le côté ManyToOne)
- La relation ManyToMany porte-t-elle ses propres attributs ? Si oui → entité intermédiaire.

**Exemple** :
```
Salon       ──OneToMany──▶   Coiffeur      (un salon a plusieurs coiffeurs)
Coiffeur    ──ManyToOne──▶   Salon          (un coiffeur appartient à un salon)
Salon       ──OneToMany──▶   Prestation     (un salon propose plusieurs prestations)
Coiffeur    ──OneToMany──▶   Créneau        (un coiffeur a plusieurs créneaux)
Client      ──OneToMany──▶   Réservation    (un client a plusieurs réservations)
Réservation ──ManyToOne──▶   Créneau        (une réservation concerne un créneau)
Réservation ──ManyToOne──▶   Prestation     (une réservation concerne une prestation)
Réservation ──ManyToOne──▶   Coiffeur       (une réservation concerne un coiffeur)
Coiffeur    ──ManyToMany──▶  Prestation     (via CompétenceCoiffeur)
```

**Piège courant** : Ne pas identifier les ManyToMany. Si deux entités semblent liées en OneToMany dans les deux sens, c'est probablement un ManyToMany. Se demander si la relation elle-même porte des attributs — si oui, créer une entité intermédiaire (ex: CompétenceCoiffeur avec un attribut "niveau").

---

## Étape 5 — Valider

Passer chaque entité au crible des critères suivants :

**Checklist de validation** :

- [ ] **SRP** : L'entité a une seule raison d'exister. On peut la décrire en une phrase sans "et".
- [ ] **Pas de god class** : L'entité n'a pas plus de ~10-15 attributs. Si plus, chercher à décomposer.
- [ ] **Données pures** : L'entité ne contient aucune logique métier. Juste un constructeur, des getters et des setters.
- [ ] **Attributs au bon endroit** : Chaque attribut appartient bien à cette entité et pas à une autre.
- [ ] **Relations justifiées** : Chaque relation a une raison métier, pas juste technique. Le type (OneToMany, ManyToOne, ManyToMany, OneToOne) est explicite.
- [ ] **Nommage clair** : Le nom de l'entité est un terme du domaine métier que le client comprendrait.

**Si une entité ne passe pas la checklist** → soit la décomposer, soit la fusionner avec une autre, soit la rétrograder en simple attribut d'une autre entité.
