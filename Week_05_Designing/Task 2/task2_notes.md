# Task 2 Notes

Date: 2026-10-29

## Work completed

- Read `task1_notes.md` to use the documented Teamify requirements,
  architecture drivers, alternatives, and final preference.
- Created `ADR-architecture.md` describing the context, three considered
  options, the decision to use a modular monolith, the reasons for that
  decision, and its consequences.
- Chose the modular monolith because it supports Teamify's current real-time
  and collaboration requirements with less operational and distributed-system
  complexity than service-oriented architecture, while preserving a path to
  extract modules later. Managed serverless was rejected because control over
  login, user data, chat, and notifications was prioritized over provider
  convenience.
- Added a comparison table to `ADR-architecture.md` covering development
  speed, complexity, scaling, real-time support, cost, and control over data
  for all three architecture options.
- Added a Mermaid diagram showing the chosen architecture: client channels,
  the modular monolith and its bounded modules, PostgreSQL, Redis, background
  workers, and notification delivery.
- Revised the Option 3 rejection in `ADR-architecture.md` so that direct
  control over data is explicitly described as the team's preference and
  planning assumption, rather than a stated Teamify requirement.
- Redrew the Mermaid diagram so the HTTPS API, WebSocket gateway, and all
  bounded modules are inside the `Teamify backend (one deployable application)`
  subgraph, while PostgreSQL, Redis, workers, and email/push delivery remain
  outside it.
- Added the selected technology stack: TypeScript/NestJS for the backend and
  React for the web client, with React Native as a future mobile option.
- Replaced the generic architecture-reconsideration sentence with concrete
  signals involving targets, independent scaling, deployment coupling, team
  ownership, and operational cost or incident impact.
- Added an `Assumptions and open questions` section covering scale,
  infrastructure responsibilities, domain rules, real-time behavior, polls,
  deletion, security, and conflict resolution.
- Read the whole ADR and simplified the language by shortening sentences,
  replacing abstract wording with direct wording, and removing repeated
  points.
- Added one sentence explaining that NestJS was chosen over Spring Boot so the
  backend and React client can use the same language.
- Clarified that the latency and availability targets in the reconsideration
  signals have not yet been defined.
