# AI Agent Steering, Governance & Thinking Discipline

> Any AI coding agent working on TrekLink (Claude Code, Cursor, Copilot, etc.) must operate with the precision, epistemic humility, and safety rigor expected of a teammate whose commits get graded. Internal reasoning is scratchwork for reaching correct conclusions, not a performance. Link this file (plus `07-github-workflow-git-conventions.md`) into whatever your tool reads as its rules file (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, Copilot custom instructions).

---

## 1. Operating Principles & Decision Hierarchy

1. **Knowledgeable, not instructive** — speak at engineer level, exact file/line references, no filler or lectures.
2. **Show, don't tell** — don't narrate compliance; execute the tool call.
3. **Truthful & transparent** — report failing tests and missing context with exact evidence, never fabricate state.
4. **Search & grounding first** — ground non-trivial claims (API usage, architecture choices, NFR interpretation) in the actual spec/code, not memory.

**Decision hierarchy** (highest wins on conflict): Safety & Security → System Integrity (module boundaries, DB constraints, audit trails) → Evidence Completeness → Task Correctness (satisfies the EARS requirement) → Resource Efficiency.

---

## 2. The Universal Pre-Action Protocol

```mermaid
flowchart TD
    S0["Stage 0: Anti-Looping / Anti-Yapping"] --> S1["Stage 1: Epistemic Categorization"]
    S1 --> S1_5["Stage 1.5: Blast Radius & Impact"]
    S1_5 --> S2["Stage 2: Sanity Gate"]
    S2 --> S2_5["Stage 2.5: Crash-Safe Checkpoint"]
    S2_5 --> S3["Stage 3: Verified Execution"]
```

### Stage 0 — Thinking discipline
Banned: stalling interjections ("Wait, actually…"), rhetorical loops without a tool call to resolve them, narrating an action right before doing it, theatrical reactions, absolutist claims before empirical verification, faking a tool run in prose.
Required loop: state one falsifiable hypothesis → name the exact check → run it → state the finding once → proceed (or test the next hypothesis without re-litigating).

### Stage 1 — Epistemic Reality Anchor
- **Read-before-write**: never edit a file not opened this session.
- **Check for concurrent/recent session files first** (Session 4 addition): before deep-diving a module or repeating research, glob `docs/sessions/` and `ignore/[you]/docs/sessions/` for anything from the last ~24h in the same area. Another session (yours or a teammate's agent) may have already found and recorded exactly what you're about to re-derive — reading a 20-line session file is far cheaper than re-running the investigation.
- **KNOWN** (verified this session) / **INFERRED** (pattern-based, state confidence) / **UNKNOWN** (flag before proceeding — check `00-project-context/03-decisions-and-risk-register.md` first; an "unknown" is often already an OPEN decision there).
- **Kalama Proof Standard**: reject "seems right" — require file evidence or test output.

### Stage 1.5 — Blast Radius (before migrations, deletions, dependency bumps, cross-module refactors)
1. List every caller/module affected — remember TrekLink's module-isolation rule (`04-architecture-conventions.md` §1.1): a change to a shared service can ripple across `devices`/`rentals`/`incidents` simultaneously.
2. Argue the alternative approach with equal rigor; if genuinely close, cap confidence ≤70% and ask.
3. Check rollback feasibility (`git checkout`/migration-down); if hard to revert (e.g. a destructive Postgres migration on shared dev data), get explicit confirmation first.

### Stage 2 — Sanity Gate
Minimal change only · imports/DI wiring satisfied · builds immediately · addresses the root cause · matches `specs/{module}/design.md`.

### Stage 2.5 — Crash-Safe Checkpoint & Doc Sync

Two distinct actions, both mandatory, both **at the moment of finding — never batched to session end**:

**(a) Session-file entry** (`01-session-based-development-and-ssot.md` §4). Write to your
namespaced session file the moment you find something a future session would otherwise have to
re-derive. This is an index/pointer, not the fix itself — see (b).

**(b) Authoritative doc sync — same pass, no exceptions.** A session-file entry is not a
substitute for updating the real document a finding or change actually affects. The instant you
confirm a fact, rule out a risk, discover a contradiction, or make a change that a document
governs, **open and edit that document in the same tool-call sequence** — before starting the
next finding, and certainly before the session ends. Concretely, per finding, ask "which of these
does this touch?" and fix all that apply immediately:
- `00-project-context/04-firmware-ground-truth.md` — any verified firmware/wire-format fact
- `00-project-context/03-decisions-and-risk-register.md` — any new/resolved risk, or anything
  that changes a `D-xxx` decision's status or a firmware-fix candidate list
- `specs/{module}/{requirements,design,tasks}.md` and `api-design/*.md` — any requirement, design
  assumption, or task whose real-world basis just changed (this generalizes
  `01-session-based-development-and-ssot.md` §2.2's "atomic spec-code merges" rule beyond API
  endpoints to every spec artifact)
- Schema/code comments asserting something as fact (e.g. an idempotency-key formula) — if it's
  wrong, fix the comment now, don't leave a landmine for the next reader
- The backlog (`03-backlog/`) — if a gap in story coverage was found, add the story via
  `build_backlog.py` and regenerate, don't just note that one should exist someday

**Why same-pass, not end-of-session**: this is the Evidence Completeness tier of the Decision
Hierarchy in §1 outranking Resource Efficiency — batching "documentation" as a cleanup step at
the end trades completeness for cheapness, and it's a false economy. Long sessions compact and
paraphrase context; a finding written up from memory at hour 3 is measurably less precise (looser
file:line citations, dropped caveats, drifted wording) than one written the moment it's confirmed.
**"I'll document this at the end" is a banned pattern for the same reason Stage 0 bans narrating
an action before doing it** — it's deferred verification dressed up as a to-do list. If you
catch yourself accumulating a mental list of "docs to update later," stop and do them now instead.

### Stage 3 — Execution
Only after Stages 0–2.5 pass.

---

## 3. Power Modes & Token Budget

| Mode | Target | Use for |
|---|---|---|
| **Eco** | <10K | Doc typo, one-line config change |
| **Balanced** (default) | 10K–40K | Typical story implementation |
| **Deep** | 40K–150K | New module scaffolding, gateway-sync's priority-queue design, cross-module refactor |
| **Critical** | constrained | Near session/context limit — close out and checkpoint, don't start new work |

---

## 4. Hallucination & Loop Circuit Breakers

- **Loop detection**: same command/tool run >2× with no change in result → stop, report the exact error, ask for guidance.
- **File-edit oscillation**: same file edited >2× without passing tests → stop, diff the attempts, summarize, pause for review.
- **Scope creep**: touching files/entities outside the approved `tasks.md` → stop and ask: *"This is outside the approved spec — proceed or stick to the spec?"*

---

## 5. Tool Discipline (adapt to whatever tool names your actual agent exposes)

Prefer structured tools over raw shell equivalents where both exist: dedicated read/search/edit tools over `cat`/`grep`/`sed`; a dedicated test-runner invocation over ad-hoc shell chains. Reserve raw terminal commands for compilers, test runners, and git operations. Never rename a shared symbol via blind find-and-replace — use the language server / IDE refactor, since TrekLink's cross-module DI wiring (see `04-architecture-conventions.md`) is easy to break with a naive text replace.

## 6. Multi-Agent / Subagent Dispatch (if your tool supports it)

For a large module (e.g. all of TP2's Gateway Bridge), divide into: a **research/code-indexer** pass (map existing gateway code, no mutation), a **QA verifier** pass (run the test suite, report pass/fail with evidence), and the **implementation** pass itself. Each hands back a short structured summary (what changed, test results, open questions) rather than a full transcript — keeps the lead session's context budget for actual decisions.
