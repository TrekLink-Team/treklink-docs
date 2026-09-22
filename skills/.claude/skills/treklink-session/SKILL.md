---
name: treklink-session
description: Drive the mandatory TrekLink session workflow end to end, context ingestion, clarification gate, approval gate, implementation, doc sync, wrap-up. Trigger at the start of ANY work session on treklink-docs, treklink-web, or treklink-firmware, or when the user says "start a session", "let's work on TK-nn", or names a TrekLink module.
argument-hint: <what you want to work on, e.g. "TK-45 device registration" or "audit the gateway queue">
---

# /treklink-session

Runs the nine-step session workflow mandated by
`_docs/01-conventions/11-ai-first-doctrine-and-toolchain.md` §5. Follow it in order. Do not skip
steps 2, 3 or 5, those are the gates, and skipping them is what wastes tokens.

## Usage

```
/treklink-session $ARGUMENTS
```

---

## Step 1: Introduction

State back, in two lines: the goal, the repo and module you believe you are working in, and the
Jira key if one was given. If any of those is unclear, ask now rather than guessing.

## Step 2: Context ingestion (do this before anything else)

Run these in parallel where possible:

1. **Resolve the docs root** (`treklink-docs/_docs/`, `_docs/`, or `../treklink-docs/_docs/`
   depending on where you were opened). If it does not resolve, **stop and say so**, do not fall
   back to generic best practice.
2. Read `_docs/01-conventions/00-index.md`, then **07** (git), **10** (Jira), **11** (AI-first).
3. Read `_docs/00-project-context/03-decisions-and-risk-register.md`. Report any `OPEN` decision
   that blocks this task.
4. Glob `docs/sessions/` and `ignore/*/docs/sessions/` for files from the last ~24h touching this
   area. **Read them.** Do not re-derive what a recent session already found.
5. Locate today on `_docs/00-project-context/02-roadmap-and-milestones.md`, sprint, roadmap week,
   what is due.
6. If the task touches a device or wire format, read
   `_docs/00-project-context/04-firmware-ground-truth.md`. Charter claims about the firmware have
   already been disproven by it.
7. Grep the actual code for the symbols/modules involved. Read targeted line ranges, not whole
   large files.

Then report a short **epistemic anchor**: what is KNOWN (verified this session), INFERRED (with
confidence), UNKNOWN (flagged).

## Step 3: Questions: HARD STOP

Ask a **batch** of clarifying questions. Cover at minimum:

- Domain edge cases and failure modes
- Authorization: which of Admin/Staff/Guide/Customer, and what ownership checks apply
- Error conditions, and what the system should do for each
- Anything in the spec that is ambiguous, contradictory, or absent
- **Every assumption you are about to make**, stated explicitly so it can be corrected

**Stop. Wait for answers. Write no code, no specs, no files.**

If the user tells you to skip this step, say once that skipping it is the main cause of rework on
this project, then comply.

## Step 4: Answers

The user answers. Engage with the answers, if one contradicts a spec, a decision, or something you
read in step 2, **say so** rather than silently accepting it. You are co-authoring, not taking
dictation.

## Step 5: Pre-check: approval gate

Before touching any file, state:

1. Every file you will create or modify, and why.
2. **Blast radius**, what depends on these, what could break. Remember module isolation: a change
   to a shared service can ripple across `devices`/`rentals`/`incidents` at once.
3. What you are deliberately **not** doing.
4. Anything you are under ~80% confident about.
5. Whether the spec-before-code gate is satisfied, if `specs/{module}/requirements.md`,
   `design.md`, `tasks.md` do not cover this, **the spec is the work**, not the code.

**Wait for explicit approval. Silence is not approval.**

## Step 6: Implement

- Read before write. Never edit a file not opened this session.
- Minimal sufficient change. No speculative abstractions.
- Follow `tasks.md` phase by phase; check items off as you go.
- Conventional Commits with the Jira key as scope: `feat(TK-45): ...`.
- **Do not commit or push unless explicitly asked.**

Circuit breakers, stop and ask rather than continuing:
- Same command run >2× with no change in result
- Same file edited >2× without passing tests
- About to touch files outside the approved scope

## Step 7: Report

- What changed, file by file.
- Test results, **actual output**, not "tests pass".
- Decisions made and why.
- **What was NOT done** and why.

## Step 8: Documentation sync: same pass, not deferred

For every finding or change, update the authoritative document **now**:

| Touched | Update |
|---|---|
| A verified firmware/wire-format fact | `_docs/00-project-context/04-firmware-ground-truth.md` |
| A new/resolved risk or decision | `_docs/00-project-context/03-decisions-and-risk-register.md` |
| A requirement, design assumption, or task | `specs/{module}/{requirements,design,tasks}.md` |
| An endpoint | `specs/{module}/api-design/*.md`, same PR |
| A comment asserting something false | Fix the comment now |

Then write the session file:
`ignore/{name}/docs/sessions/YYYY-MM-DD-HHMM-{topic}.md`, and update
`ignore/{name}/docs/current-progress.md` to point at it.

**"I'll document this at the end" is a banned pattern.** Deferred documentation is deferred
verification wearing a to-do list.

## Step 9: Wrap up

- Confirm working-tree state and test status.
- If context is past **80%**, run `/summarization` and hand off to a fresh session.
- **End the session.** Do not extend it for anything except finishing the current task.

---

## Loop-back

Whenever something new becomes ambiguous mid-implementation, return to **Step 3**. Do not resolve
an ambiguity by guessing and continuing.
