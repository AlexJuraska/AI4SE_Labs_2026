# Task 1 – Requirements Refinement Network: Report

## What it does

The program reads all text documents in a provided folder (emails, meeting notes, interviews, surveys, drafts) and turns them into one requirements document. It is built with LangGraph and uses OpenAI models.

Run it with:

```
python requirements_network.py <input-folder> <output-md-file>
```

Only the folder is given. The program finds all `.txt`, `.md` and `.eml` files in it by itself.

## How it works

The network has 7 steps:

1. **Load documents** (no AI). Reads every file in the folder.
2. **Extract** (AI, `gpt-5-mini`). Goes through each document separately and pulls out the requirements. It also lists what it skipped and why, for example small talk or meeting dates.
3. **Combine** (AI, `gpt-5.6-luna`). Merges requirements that say the same thing, removes conflicts, gives each requirement an ID (R-001, R-002, …) and a priority.
4. **Validate** (no AI). Checks simple rules with code: IDs are unique, source files really exist, explanations are long enough, and the wording fits the priority.
5. **Review** (AI, `gpt-5.4-nano`). Reads the draft and looks for duplicates, contradictions, missing requirements and unclear wording.
6. **Revise** (AI, `gpt-5.6-luna`). Fixes the problems found in steps 4 and 5. After revising, the draft goes back to step 4. This loop runs at most 2 times.
7. **Finalize** (no AI). Removes duplicates from the discarded list and writes the final Markdown file.

```
load → extract → combine → validate → review → finalize
                              ↑           │
                              └─ revise ←─┘  (if problems found)
```

## Why it is built this way

- **Different models for different jobs.** A small, fast model extracts requirements from each document. The most capable of the three models used combines everything, because that step needs to see the whole picture. A third, cheap model reviews the draft, so the draft is not checked by the same model that wrote it.
- **One document at a time first.** Extracting from each file separately keeps the prompts small. It also makes tracing exact, because the program knows which file each requirement came from without asking the AI.
- **Code checks where possible.** Rules that are easy to check with code are not left to the AI. This makes the checks reliable.
- **Limited loop.** The review loop stops after 2 rounds so the program always finishes.
- **Same writing rules for all AI steps.** For example "shall" for Must requirements, no filenames inside explanations.

## Meeting the network requirements

| Requirement | How it is met |
|---|---|
| ANS1: at least 3 AI nodes | 4: extract, combine, review, revise |
| ANS2: at least 1 non-AI node | 3: load, validate, finalize |
| ANS3: feedback loop | review → revise → validate → review |
| ANS4: at least 3 models | gpt-5-mini, gpt-5.6-luna, gpt-5.4-nano |
| ANS5: LangGraph | Built with LangGraph `StateGraph` |

## Meeting the output requirements

| Requirement | How it is met |
|---|---|
| OS1: one document | One Markdown file with fixed sections |
| OS2: unique IDs | IDs R-001, R-002, …; code checks they are unique |
| OS3: no duplicates | Combine step merges them; review step checks again |
| OS4: tracing | Each requirement lists the files it came from; code checks the files exist |
| OS5: name and explanation | Every requirement has a short name and a paragraph explaining it |
| OS6: priority | Must / Should / Could / Won't, explained at the top of the document |
| OS7: consistency | Shared writing rules; review step looks for contradictions |
| OS8: completeness | Extract step must not skip anything; code checks that every document that produced requirements is traced in the output |
| OS9: blacklist | Discarded requirements are listed in their own section with a reason |

## Result

From the 20 input documents, the network produced:

- **47 requirements** (45 Must, 2 Should)
- **6 discarded requirements**, for example automatic purging, which conflicts with the rule that deleting needs confirmation
- **a list of skipped content** such as small talk, action items and meeting logistics

## Known weaknesses

- Some notes in the skipped-content list point to the wrong requirement IDs.
- Almost all requirements are marked Must.
- One real requirement (data-quality reports) was wrongly put in the skipped list.
- One discarded item appears twice with different wording.