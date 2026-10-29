# Architecture decision notes: Teamify

Date: 2026-10-29

## Requirements reviewed

Source: `Tasks/data/Teamify.txt`

Teamify combines personal task management with team collaboration.

### Capabilities

- Account registration, login, logout, profile viewing and editing, password
  reset, and account deletion.
- Personal task creation, editing, completion, and deletion.
- Team creation, joining, leaving, listing, and administration.
- Team administrator management.
- Shared team events with create, edit, complete, delete, and invitation
  acceptance or refusal.
- Real-time group chat.
- Team polls: administrators create them; members vote and view results.
- Notification history and real-time notifications.
- Personal and team agenda views.

### Users and authorization

- Users act on their own account and personal tasks.
- Team members access team collaboration features.
- Team administrators have additional authority over members, teams, polls,
  and shared events.
- Authorization must therefore distinguish ownership, membership, and
  administrator privileges.

### Data and consistency

- Durable records are implied for accounts, tasks, teams, memberships,
  events, invitations, polls, votes, messages, and notifications.
- Shared data can be changed by multiple users, so concurrent-edit behavior
  needs definition.
- Account deletion raises ownership, retention, and shared-content questions.

### Quality expectations and constraints

- Chat and notifications are explicitly real-time.
- The interface is expected to be intuitive and support efficient individual
  and collaborative work.
- Privacy is implied by account deletion and by role-based access.
- No measurable scale, latency, availability, recovery, retention, client
  platform, or deployment constraints are stated.
- No external calendar, email, push-notification, or identity-provider
  integration is specified.

## Architecture-driving requirements

1. Real-time chat and notifications affect connection management, fan-out,
   reconnect behavior, authorization, ordering, and missed-message recovery.
2. Shared agendas and events require transactional updates, permission
   checks, invitations, and a policy for conflicting edits.
3. Authentication, password recovery, account deletion, and role changes
   require secure identity and authorization boundaries.
4. Team membership affects access to chat, events, polls, and notifications.
5. Account deletion may require coordinated cleanup or anonymization of
   shared content.

Personal task CRUD and basic profile display are comparatively weak drivers and
can be supported by a conventional API and durable datastore.

## Important unknowns

- What fields, recurrence rules, and time-zone behavior do tasks and events
  have? Are “tasks” and “events” separate domain concepts?
- How are users invited to teams, and who can approve membership?
- What happens if a team would have no administrator?
- Are polls anonymous? Can users change votes? Do polls have deadlines?
- Must chat support history, read status, presence, attachments, or
  moderation?
- Which notifications exist, which channels deliver them, and what delivery
  guarantee is required?
- What are the password, session, and account-deletion retention policies?
- What should happen to shared content authored by a deleted account?
- What client platforms, scale, latency, availability, backup, and recovery
  targets are required?
- Should users be able to work offline, search, filter, or sort?

## Chosen comparison dimension

The most consequential early decision is the deployment and execution
structure. Real-time delivery, shared-data consistency, account deletion, and
operational complexity all change substantially depending on whether the
capabilities run together, in independently deployed services, or on a
managed backend platform. Framework and vendor choices are deferred.

## Options to compare

### Option A: Modular monolith with real-time delivery

One backend deployment contains explicit modules for identity, teams,
planning, chat, polls, and notifications. It exposes ordinary request APIs
and a WebSocket endpoint. A relational database is the transactional system
of record; a small shared state or pub/sub component may support connection
fan-out and presence. Background workers handle retries, notification
delivery, password-reset messages, and account cleanup.

Benefits relevant to Teamify:

- Straightforward transactions for membership, events, invitations, and
  permissions.
- Lower deployment and local-development complexity.
- Easier end-to-end testing and debugging.
- Internal module boundaries can preserve a path to later extraction.

Painful parts:

- A release or resource problem can affect all features.
- WebSocket connections and chat fan-out need careful multi-instance design.
- Background work still needs idempotency, retries, and failure visibility.
- Module boundaries can erode without enforced ownership rules.

### Option B: Independently deployed domain services

Separate services own identity, collaboration, planning, chat, polls, and
notifications. An API gateway and real-time gateway serve clients. Services
communicate through synchronous calls for immediate decisions and a durable
event broker for propagation. Each service owns its data.

Benefits relevant to Teamify:

- Chat, notifications, and planning can scale or fail independently.
- Separate ownership and release schedules are possible.
- Event delivery and future integrations are explicit.

Painful parts:

- Membership, invitations, notifications, and account deletion span multiple
  transactions and become distributed workflows.
- Delayed, duplicated, or reordered events require idempotency, tracing,
  reconciliation, and dead-letter handling.
- Local development, contract testing, deployment, and incident response are
  substantially more demanding.

### Option C: Managed serverless or backend-as-a-service platform

Managed identity, database, functions, and real-time subscriptions provide
most infrastructure. Functions implement domain operations and background
work; provider security rules and application checks enforce ownership and
team roles.

Benefits relevant to Teamify:

- Fast initial delivery with less infrastructure to operate.
- Managed authentication, realtime transport, scaling, and backups may
  reduce implementation effort.
- Usage can scale without managing application servers directly.

Painful parts:

- Provider-specific data, transaction, realtime, and authorization behavior
  can constrain the design.
- Cost and performance can be harder to predict from usage patterns.
- Complex deletion workflows, chat semantics, observability, and recovery
  may be limited or provider-specific.
- Moving away from the provider can be expensive.

## Current state

- Option A, a modular monolith with real-time delivery, has been selected.
- Existing project notes and a proposed ADR may contain a prior preference,
  but the selected decision here is based on the current requirements review
  and explicit user confirmation.
- The user chose to proceed directly to a comparison table rather than first
  answering the open requirements questions or challenging the options.

## Comparison

| Criterion | Modular monolith | Independently deployed services | Managed serverless/backend platform |
|---|---|---|---|
| Initial delivery | Fastest route to a coherent first release; shared code and transactions simplify implementation. | Slowest because service boundaries, contracts, broker workflows, and environments are needed early. | Potentially fast if provider primitives match the requirements; custom behavior can remove that advantage. |
| Shared-data consistency | Strongest fit for membership, permissions, events, invitations, and notifications that need coordinated writes. | Cross-service operations are eventually consistent and need workflows, retries, and reconciliation. | Depends on provider transaction and trigger semantics; simple cases are convenient, complex workflows are provider-specific. |
| Real-time chat and notifications | Feasible with a WebSocket gateway, durable records, reconnect cursors, and shared fan-out state; multi-instance scaling needs deliberate design. | Strong isolation and independent scaling for chat and notification gateways, but ordering and delivery across services are harder. | Realtime subscriptions reduce infrastructure work, but delivery semantics, history, and recovery depend on the provider. |
| Scaling and fault isolation | Scaling is coarser and one deployment or resource incident can affect all features. | Best independent scaling and fault isolation, at the cost of more components and cross-service failure modes. | Provider handles much of the infrastructure scaling, but limits and cost behavior may be less predictable. |
| Security and data control | Central authorization and a single data model make policy review and account deletion more direct. | Each service must enforce identity and authorization consistently; deletion and role changes cross boundaries. | Managed identity and security rules help, but application policy is coupled to provider capabilities and configuration. |
| Operations and debugging | Fewest operational components; module coupling and background-job reliability still need discipline. | Requires tracing, broker monitoring, contract tests, deployment automation, and distributed incident response. | Less infrastructure operation, but provider-specific logs, retries, limits, and recovery procedures can be opaque. |
| Cost predictability | Application and database costs are comparatively understandable at the stated, unknown scale. | Broker, gateways, multiple databases, and operations increase baseline cost before scale is known. | Low operational overhead can be attractive initially, while usage-based pricing and lock-in make future cost harder to predict. |
| Changeability | Internal modules provide extraction seams, but releases and schema changes remain coupled. | Independent releases are strongest, but changing contracts and workflows is expensive. | Provider coupling can accelerate early changes and make later migration or unusual behavior expensive. |

### Trade-off summary

- Option A best matches the current need for coordinated team data and
  real-time behavior while keeping delivery and operations manageable. Its
  central risk is that the single deployment becomes a bottleneck or a
  failure domain.
- Option B becomes more attractive if independent scaling, team ownership,
  fault isolation, or integration volume is more important than simple
  transactions and low operational overhead. Its distributed consistency and
  operations are substantial costs at the current level of evidence.
- Option C becomes more attractive if rapid delivery and minimal
  infrastructure ownership dominate, and the team accepts provider-specific
  behavior and migration cost. It is less suitable when Teamify needs
  unusual authorization, deletion, realtime, or data-control semantics that
  the provider does not support cleanly.

The comparison was conditional because scale, delivery targets, operational
ownership, and provider preferences are still unknown. It informed the
decision recorded below.

The user chose to discuss the trade-offs or open questions before naming a
leading option.

The user requested a plain-language explanation of the three options.

The user initially identified the modular monolith (Option A) as the leading
architecture for further consideration.

## Strongest case for the runner-up

The strongest runner-up is Option B, independently deployed domain services.
It would be better if Teamify expects independently scaling chat or
notifications, multiple teams owning separate capabilities, strict fault
isolation, or frequent releases of one capability without coordinating with
the rest of the system. It also creates clearer long-term boundaries when
different parts of the product genuinely need different storage or runtime
behavior.

Those advantages do not currently outweigh the costs shown by the
requirements. Teamify needs coordinated membership, permissions, events,
invitations, account deletion, and notifications, but provides no scale,
availability, organizational, or release-independence targets that require
distributed services. The service option would introduce eventual
consistency, distributed deletion and authorization workflows, and greater
operational burden earlier than the evidence justifies.

## Selected decision

Option A is selected: a modular monolith with real-time delivery. The choice
prioritizes coordinated shared-data behavior, simpler delivery and operations,
and a lower level of distributed-systems complexity while the requirements
contain no scale or organizational drivers for independent services.

The user explicitly accepted the ADR, so its status is now `Accepted`.
