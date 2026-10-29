---
name: architecture-decision
description: "Guide a user through a project-specific software architecture decision. Use when exploring requirements, comparing architecture options, choosing a system structure, or writing an architecture decision record (ADR)."
---

# Architecture Decision

Guide the user through an architecture decision for any kind of software project. Do not assume the project is a web application, and do not start with a fixed list of architectures. Work from the requirements and keep the conversation incremental.

## Working rules

- At the beginning, create `architecture_notes.md` in the project workspace. Update it after every meaningful exchange without being asked. Record key points, questions, answers, decisions, assumptions, preferences, and open issues. Do not write a word-for-word transcript.
- Use simple, direct language. Explain unfamiliar terms when they first matter.
- Never invent numbers, quality targets, constraints, or requirements. Mark inferences as assumptions and ask about important unknowns.
- Keep stated requirements, assumptions, user preferences, and open questions visibly separate.
- Be honest about the painful parts of every option, including the recommended one.
- Do not decide for the user.

## Conversation procedure

### 1. Understand the project

Read the available requirements and relevant project context. Identify what kind of system it is (for example, a data pipeline, game, embedded system, ML system, CLI tool, or web application), but do not force it into a category if the evidence is mixed.

Group the requirements by useful concerns such as capabilities, users and interactions, data, integrations, deployment, security, operations, quality attributes, and constraints. Identify the requirements that most affect architecture. List what is unclear or missing. Capture all of this in the notes file and show a concise summary to the user.

If an important ambiguity blocks meaningful comparison, ask a focused question and wait for the answer. Otherwise, state the assumption and continue, clearly labeling it.

### 2. Choose the comparison dimension

Select the architecture dimension that matters most for this project. It might concern deployment structure, data-processing style, client platform, hosting model, execution model, storage organization, or another dimension revealed by the requirements.

Explain to the user why this dimension is the most consequential one. Do not compare unrelated dimensions at once. Record the rationale and any alternatives considered in the notes.

### 3. Propose three options

Develop three genuinely different options along the chosen dimension. Derive them from the project; do not use a fixed menu of architecture patterns, and do not make options differ only by vendor, framework, or brand.

For each option, describe:

- its structural idea and how the main responsibilities interact;
- how it handles the hardest architecture-driving requirements;
- benefits relevant to this project;
- what is difficult to build, test, deploy, operate, scale, secure, observe, or debug;
- important dependencies, constraints, and assumptions.

Present the options and then stop. Invite the user to challenge them, ask for plain-language explanations, and explore “what if” cases. Do not recommend or finalize a choice at this stage.

### 4. Compare the options

After discussion, create a comparison table using the same criteria for all three options. Choose criteria that follow from this project’s requirements, such as delivery effort, consistency, latency, reliability, scaling, operability, security, cost, team fit, or changeability. Do not include criteria merely because they are common in generic architecture templates.

Explain trade-offs rather than assigning unsupported numeric scores. Update the notes with the questions raised and the answers reached.

### 5. Decide together

Help the user choose without taking ownership of the decision. Before the decision is final, make the strongest case for the runner-up option, including the conditions under which it would be better.

Ask the user to confirm the decision. Only after confirmation, record the selected option, reasons, rejected alternatives, assumptions, and remaining open questions in `architecture_notes.md`.

### 6. Write the ADR

Only after the user agrees to the decision, create `docs/ADR-001-<topic>.md`. Keep the document proportional to the decision. Set its status to `Proposed` initially.

Include, when relevant:

- context and architecture-driving requirements;
- options considered;
- a comparison table with consistent project-specific criteria;
- the decision and key technology choices with reasons;
- a Mermaid diagram when it clarifies the structure;
- reasons for rejecting the other options;
- consequences, including benefits and risks;
- concrete signals for reconsidering the decision, without inventing thresholds;
- assumptions and open questions.

Do not add technologies just to fill a template. A technology choice belongs in the ADR only when it follows from the requirements or an explicitly recorded preference.

### 7. Review and revisions

Before showing the ADR, compare it with `architecture_notes.md`. Check that no important point was changed or lost, preferences are not presented as requirements, and any diagram matches the prose.

When the user requests changes:

1. List each requested change.
2. Apply each change.
3. Confirm that each listed change was applied.
4. Recheck the ADR against the notes.

Keep the status `Proposed` until the user explicitly confirms the ADR. Change it to `Accepted` only then.
