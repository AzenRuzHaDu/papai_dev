# Procédure — Sélection de Stack

## Objectif

Identifier **tous les besoins techniques** d'un projet à partir de son PRD, puis choisir les outils adaptés. Pas de liste à cocher — la stack est déduite du projet, pas l'inverse.

## Quand l'exécuter

Avant de commencer l'architecture. L'architecte lance cette procédure après avoir lu le PRD.

## Méthodologie

### Passe 1 — Besoins fonctionnels → Besoins techniques

Pour chaque fonctionnalité du PRD, l'architecte identifie les implications techniques.

Il pose la question : **"Pour implémenter cette fonctionnalité, de quoi ai-je besoin techniquement ?"**

Exemples :
- "Chat temps réel" → WebSocket ou SSE, gestion de connexions persistantes
- "Génération de réponses IA dans l'UI" → streaming LLM, UI générative (AssistantUI, CopilotKit, Vercel AI SDK...)
- "Prise de RDV" → gestion de créneaux, fuseaux horaires, notifications
- "Paiement en ligne" → provider de paiement, webhooks, idempotence
- "Upload de fichiers" → stockage objet, limites de taille, preview

L'architecte présente ses déductions à l'utilisateur et demande validation avant de passer à la suite.

### Passe 2 — Préoccupations transverses

Ce sont les besoins que le PRD ne mentionne jamais mais que le projet nécessite. L'architecte les passe en revue **mentalement** et ne soulève que ceux qui sont **pertinents pour ce projet**.

Catégories de préoccupations transverses (non exhaustif, à adapter au projet) :
- Authentification & autorisation
- Gestion d'erreurs & logging
- Monitoring & alerting
- Sécurité (CORS, rate limiting, validation d'inputs, injection)
- Mailing / notifications (email, push, SMS)
- Paiement
- Internationalisation (i18n)
- SEO
- Accessibilité (a11y)
- RGPD / protection des données
- Performance (cache, CDN, lazy loading)
- Jobs asynchrones / files d'attente
- Stockage fichiers
- Conteneurisation
- CI/CD
- DX (linting, formatting, tests)

L'architecte pose une question par préoccupation pertinente, **en expliquant pourquoi elle s'applique à ce projet**.

### Passe 3 — Choix d'outils

Pour chaque besoin identifié en passe 1 et 2, l'architecte :
1. Demande à l'utilisateur s'il a déjà une préférence
2. Si oui, valide le choix ou signale un risque
3. Si non, propose 2-3 options avec les trade-offs et recommande

L'architecte fait des **recherches** si nécessaire — il ne recommande pas un outil qu'il ne connaît pas bien ou qui a pu évoluer.

## Output

Un résumé structuré de la stack validée, intégré au document d'architecture dans une section "Stack technique". Chaque choix est accompagné d'une ligne de justification.
