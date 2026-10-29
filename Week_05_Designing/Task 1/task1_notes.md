# Task 1 Notes

Date: 2026-10-29

## Requirements review

- Read `Tasks/data/Teamify.txt`.
- Teamify is a personal task-management and team-collaboration application. It combines personal and team agendas, team membership and administration, shared events, real-time chat, polls, and notifications.
- Grouped the 31 user stories into the requested areas:
  - Accounts: 1-7.
  - Personal tasks: 9, 11-14.
  - Teams: 15-20, 25-26.
  - Events: 10, 27-31.
  - Chat: 21.
  - Polls: 22-24.
  - Notifications: 8 and the notification aspect of 16.
- Cross-cutting interpretation: story 10 is the team shared agenda view; story 28 is an event invitation response; stories 27-31 define shared event lifecycle and completion.
- Detectable non-functional expectations: real-time behavior for chat and notifications, intuitive/easy-to-use interface, support for individual and collaborative work, efficiency/effectiveness, privacy/data removal when an account is deleted, and access control for administrators versus members.
- Ambiguities or missing requirements: task/event fields and recurrence/time-zone rules; whether shared events are distinct from tasks; invitation and team-join mechanisms; membership and administrator permissions/last-admin rules; poll question/options, anonymity, deadlines, and vote changes; chat history, delivery/read status, and moderation; notification types, channels, preferences, persistence, and delivery guarantees; password/security policies and session behavior; account deletion retention/anonymization; conflict handling and concurrent edits; search/filter/sort; offline behavior; accessibility/localization/device/browser support; performance, availability, scalability, backup/recovery, audit logging, and measurable acceptance criteria.
- Open design questions for later work: clarify domain terminology (“task” versus “event”), define authorization rules, and turn qualitative goals such as “real-time” and “intuitive” into measurable requirements.

## Architecture drivers

- Highest-impact driver: real-time chat and notifications. They may require persistent client connections such as WebSockets, an event-driven backend, message delivery and retry handling, presence/read state, and possibly a broker or pub/sub layer. This affects deployment, scaling, and observability.
- Shared team agendas and events are another major driver. Multiple users can view and modify shared data, so authorization, transactions, optimistic concurrency/conflict handling, event invitations, and consistent updates must be designed explicitly.
- Authentication, password reset, account deletion, and administrator/member roles strongly shape the security architecture: identity/session management, password recovery, authorization boundaries, auditability, and deletion/anonymization workflows.
- Team membership and administration influence the domain model and permission checks across events, chat, polls, and notifications. Membership changes also require defined behavior for existing content and pending invitations.
- Polls are less infrastructure-intensive but introduce cross-user consistency and authorization rules, especially for one-vote constraints, anonymity, deadlines, and result visibility.
- Privacy and account deletion can affect data ownership, shared-content retention, referential integrity, and asynchronous cleanup across all subsystems.
- Scalability, availability, latency, and data-retention targets are currently missing; once specified, they could force choices such as service decomposition, caching, database replication, queueing, and backup/recovery design.
- Personal task CRUD and basic profile viewing/editing are comparatively weak architecture drivers and can normally be supported by a conventional API and database.

## Architecture alternatives

### Option A: Modular monolith

- One deployable backend with separated modules for accounts, teams, tasks/events, chat, polls, and notifications.
- The web/mobile client communicates with the backend over REST or GraphQL; chat and live updates use WebSockets. Internal modules call each other in-process and publish domain events to an internal dispatcher or Redis.
- PostgreSQL stores transactional data; Redis can store sessions, presence, short-lived notification state, and pub/sub messages. Object storage can hold future attachments.
- Chat messages are persisted in PostgreSQL, then broadcast through WebSockets. Notification events are persisted and pushed to connected clients; a background worker handles retries and offline notifications.
- Suggested stack: TypeScript/NestJS or Java/Spring Boot, PostgreSQL, Redis, WebSockets, and React/React Native.
- Main trade-off: simple deployment and strong transactional consistency, but a large deployment unit and less independent scaling.

### Option B: Event-driven service-oriented architecture

- Independently deployable services cover identity, teams/membership, tasks/events, chat, polls, and notifications. An API gateway/BFF exposes a unified client API.
- The client uses HTTPS to the gateway and WebSockets through a real-time gateway. Services communicate asynchronously through a broker and synchronously over REST or gRPC where immediate responses are required.
- Each service owns its database: for example PostgreSQL for identity and teams, PostgreSQL or another transactional store for tasks/events and polls, and a chat-oriented store such as MongoDB/Cassandra or PostgreSQL. Kafka or RabbitMQ carries domain events; Redis supports presence and connection fan-out.
- Chat writes to the chat service/store and emits events to the real-time gateway. Notification events are consumed by the notification service, which persists them and delivers them over WebSockets, email, or push providers with retries.
- Suggested stack: Java/Spring Boot, Go, or TypeScript services; Kafka or RabbitMQ; PostgreSQL; MongoDB or Cassandra if chat scale requires it; Redis; Kubernetes; React.
- Main trade-off: independent scaling and fault isolation, but substantially more operational complexity, eventual consistency, distributed tracing, and cross-service workflow handling.

### Option C: Managed serverless/backend-as-a-service

- A browser or mobile client uses managed authentication and invokes serverless functions for accounts, teams, tasks/events, polls, and administration. Managed real-time database capabilities support collaboration.
- The client communicates with managed SDKs/HTTPS APIs and receives live updates through a provider’s WebSocket-based real-time mechanism. Functions communicate through direct database operations and managed queues/events.
- A managed relational database such as Supabase/Postgres or Firebase/Firestore stores application data. Managed authentication stores identities; a managed pub/sub or queue service handles asynchronous notifications; object storage handles attachments.
- Chat messages are written to a real-time collection/table and synchronized to subscribed clients. Notification-trigger functions create notification records and invoke web push, mobile push, or email services; clients subscribe to unread notification changes.
- Suggested stack: Supabase (Auth, Postgres, Realtime, Edge Functions, Storage) with React/React Native, or Firebase Authentication, Firestore, Cloud Functions, and Cloud Messaging.
- Main trade-off: rapid delivery and reduced infrastructure operations, but provider coupling, usage-based cost uncertainty, more constrained transaction/query patterns, and potentially less control over real-time behavior.

## Architecture comparison and preference

### Modular monolith 

- Advantages: simple deployment; fast development; easy local testing and debugging; strong transactions across related features; low operational overhead; clear path to modular internal boundaries.
- Disadvantages: all modules are deployed together; independent scaling is limited; a failure or resource spike can affect the whole backend; the codebase can become tightly coupled without discipline; real-time connection scaling still needs careful design.
### Event-driven service architecture 

- Advantages: independent scaling and deployment; strong fault and responsibility isolation; suitable for high-volume chat and notifications; teams can evolve services independently; broker-based integration supports asynchronous retries and fan-out.
- Disadvantages: highest operational and development complexity; distributed transactions and eventual consistency; harder testing and debugging; more infrastructure and observability requirements; higher cost and slower initial delivery.

### Managed serverless 

- Advantages: fastest initial implementation; managed authentication, storage, real-time transport, and notifications; low infrastructure maintenance; elastic scaling; useful for validating the product quickly.
- Disadvantages: vendor lock-in; provider-specific limitations; usage-based cost can be difficult to predict; less control over latency and failure behavior; complex workflows can become scattered across triggers and functions; migration and advanced debugging may be difficult.

### Current preference

Modular monolith, with explicit module boundaries, PostgreSQL, Redis, WebSockets, and background workers. It fits the currently known requirements without prematurely introducing distributed-system complexity, while leaving a path to extract chat or notifications later if scale requires it.


Preference assumptions: Teamify is initially a small-to-medium system, the team is not already operating Kubernetes or multiple services, and no unusually strict availability or scale target has been specified. The preference should be revisited if measurable load, availability, latency, or independent-scaling requirements emerge.

## Why not start with event-driven services?

- Starting with services can make future independent scaling easier, but it introduces distributed-system costs before there is evidence that Teamify needs them.
- The main risks are premature service boundaries, eventual consistency, distributed transactions, duplicated models, network failures, broker operations, retries and duplicate events, more complex testing, and higher deployment/observability overhead.
- A service architecture does not automatically make future change easier: incorrect early boundaries can be expensive to undo, and requirements for Teamify are still ambiguous, especially tasks versus events, membership rules, notification semantics, and deletion behavior.
- A modular monolith can preserve future options by enforcing module ownership, stable interfaces, domain events, repository boundaries, and avoiding direct cross-module database access. High-pressure components such as chat or notifications can then be extracted when justified.
- Starting with services is preferable when there are known independent scaling or availability targets, multiple teams that need independent releases, strong organizational experience with distributed systems, regulatory/isolation requirements, or a proven need for separate data stores.
- Decision principle: optimize for current evidence and reversibility rather than speculative scale; measure load and operational needs, then extract the bounded context whose benefits exceed the migration cost.

## Final decision on managed serverless (Option C)

- Arguments in favor: managed services can reduce initial implementation and operations work; Teamify could benefit from managed authentication, real-time transport, storage, and push notifications; for a small app, early usage costs may be lower than hiring or operating equivalent infrastructure; it is the better choice when speed to market, a small operations team, or uncertain product-market fit matters more than infrastructure control.
- Provider lock-in can be reduced, but not eliminated. Use standards-based OAuth/OIDC where possible, keep a separate application user/profile model, isolate provider SDK calls behind adapters, export database data regularly, use portable PostgreSQL rather than provider-specific features, store files in standard formats, and keep chat/notification domain logic in application code. A second provider or self-hosted replacement should be tested before it is needed.
- These measures do not make migration free: real-time subscriptions, authentication workflows, security rules, serverless triggers, quotas, and operational knowledge can still be provider-specific. A provider outage or policy change remains an external dependency.
- Cost assessment: managed services are not automatically expensive for an early, low-traffic Teamify. They may be cheaper initially because they avoid infrastructure and operations costs. Costs can become difficult to predict with persistent real-time connections, high message volume, notification fan-out, database reads, bandwidth, storage, backups, and sudden growth. Pricing limits and an exit plan would be required.
- Control assessment: self-hosting gives more control over data location, retention, access, upgrades, incident response, and architecture. It also transfers responsibility for security, backups, availability, scaling, and operations to the Teamify team.
- Final decision: drop Option C for Teamify. The decision is driven primarily by the explicit preference for control of login, user data, chat, and notifications, plus concern about lock-in and provider pricing. Use the modular monolith with self-managed or directly controlled infrastructure instead.
- Reconsideration condition: revisit managed services only if rapid validation becomes the overriding goal, the team lacks operational capacity, usage remains small, and a documented export/migration plan plus acceptable data-processing and pricing terms are available.

## Architecture decision

- Final choice: Option 1, the modular monolith.
- Rationale: it offers a good cost/complexity balance for Teamify now, while Option 2 is considered overkill at the current stage and Option 3 is rejected because of provider dependence, lock-in, data-control, and pricing concerns.
- Evolution requirement: keep the monolith open to later change and possible extraction into services.
- Architectural constraints for evolvability: maintain explicit bounded modules; give each module ownership of its business rules and data access; communicate through stable interfaces and domain events; avoid direct cross-module database access; keep asynchronous work behind queue/worker abstractions; isolate WebSocket, broker, storage, and authentication integrations; use portable data formats and automated tests; deploy modules with independent configuration where practical.
- Revisit criteria: extract a module only when measured scale, availability, fault-isolation, team ownership, or deployment needs justify the additional distributed-system complexity.
