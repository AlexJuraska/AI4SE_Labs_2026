# Task 3 Report: Architecture Work With and Without the Skill

**Project:** Teamify
**Date:** 2026-10-29

## Summary

The skill made the whole job much faster. The first run (Tasks 1 and 2 without the skill) took about an hour and needed many prompts and several ADR revision rounds. The second run with the skill took about 10–15 minutes and produced an ADR of essentially the same quality. In several technical areas it was more detailed. The few remaining gaps in the second ADR come mostly from decisions I did not state during the shorter session, not from the skill itself.

## How the two runs were done

| | Without the skill (Tasks 1 + 2) | With the skill (Task 3) |
|---|---|---|
| Approach | I steered every step with my own prompts | The skill guided the conversation step by step |
| Note-taking | I had to ask for it explicitly | Notes file created and updated automatically |
| Requirements analysis | Requested separately | Done automatically, with open questions listed |
| Three options | Requested; I had to check they were different enough | Proposed automatically, each with dissadvantages listed |
| Discussion | Free-form questions I wrote myself | Clickable choices plus an optional write-in answer at every step |
| ADR revision rounds | About 5 | About 1, but can be more depending on the user |
| Approximate time | 1 hour | About 10–15 minutes |

## What made the skill faster

- **Clickable choices.** After every step, Copilot offered numbered options, for example "Challenge or explore the three options", "Answer the open requirements questions first", or "Proceed to the comparison table". There was always an optional write-in field for my own answer. I rarely had to write prompts from scratch, so each decision were made quicker.
- **No repeated instructions.** In the first run I had to keep asking for the same things: notes, a comparison table, a diagram, simpler language, and keeping preferences separate from requirements. The skill contains these rules, so they were handled from the start.
- **A clear order of work.** The skill walks through understanding the requirements, choosing what to compare, proposing three options, discussing, comparing, deciding, writing the ADR, and reviewing. The assistant stopped at the right points and waited for my input instead of jumping straight to a finished answer.

## Quality comparison of the two ADRs

Both ADRs choose the same architecture, a modular monolith. Both reject distributed services and a managed platform for similar reasons. Overall quality is essentially the same.

**Where the ADR made with the skill is stronger:**
- Comparison criteria that fit Teamify better: shared-data consistency, real-time behavior, operations, and changeability.
- More detailed open questions, and an explicit statement that no numeric targets were invented.

**Where the original ADR is stronger:**
- A concrete technology usage (PostgreSQL, Redis, NestJS, React) with reasons.
- The rejection of the managed platform states the preference for control over data.
- A clearer architecture diagram that shows the modules inside one deployable application.

## Why the remaining gaps are mostly not the skill's fault

The tech stack and the team's preference for data control ended up in the first ADR because I stated them during long discussions and revision rounds. In the shorter skill based session I did not give these decisions. The skill correctly avoided inventing a stack or a preference I had not stated. It recorded them as open choices instead of making them up, which matches the skill's own rule.

The only gap clearly related to the skill is the diagram layout. The skill tells the assistant to keep components of one deployable application inside one boundary, but the diagram still drew the modules outside it. This could be fixed with one more correction prompt, or by making the diagram rule more prominent in the skill.

## Conclusion

With the skill, the task went from about an hour of manual steering to about 10–15 minutes of guided decisions, and the result was essentially as good. The clickable choices with a write-in option were the biggest time saver, as the conversation became a series of quick decisions instead of writing every prompt myself. Improvements to the second ADR would mainly come from me stating more decisions (tech, preferences), not from changes to the skill.

**Possible improvements to the skill:**
- Make the diagram rule stricter, or add a diagram check to the review step.
- Before writing the ADR, ask the user directly about technology preferences and team preferences, so these decisions are not lost in shorter sessions.