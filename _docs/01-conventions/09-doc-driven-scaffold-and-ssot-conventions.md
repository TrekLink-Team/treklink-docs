# Doc-Driven Scaffold & SSOT Conventions

> Source: uploaded as `11-doc_driven_scaffold_and_ssot_conventions.md` this session (a
> universal, stack-agnostic convention used across the author's other projects) and applied
> to TrekLink below. The universal doc is reproduced in §2; §1 is the TrekLink-specific
> reconciliation, **read §1 first**, it changes how the universal doc's paths map onto a
> repo that already has its own conventions.

## 1. TrekLink Application Note (read this first)

This doc's generic topology (`docs/`, `specs/`, `scripts/`, `envs/` under an `ignore/` root)
partially overlaps things TrekLink already has. To avoid two competing SSOTs, here's exactly
what changed and what didn't:

- **`specs/{module}/` is NOT moved.** `treklink-web/specs/{module}/{requirements,design,tasks}.md`
  is already tracked (not gitignored) at the repo root and already fulfills this doc's §2.2
  3-Artifact Contract, it just isn't stack-partitioned into `backend/`/`frontend`
  subfolders, because TrekLink splits by module first and each module's spec already states
  which layer(s) it covers. **Leave it where it is.** Nothing in `ignore/` duplicates it.
- **`ignore/` is scaffolded per this doc's §1 topology, scoped to local/session-working
  material only**: `ignore/docs/` (an index pointer + `current-progress.md` + `diagrams/` +
  `flows/`), `ignore/scripts/`, `ignore/envs/`. Applied to:
  - `treklink-docs/ignore/`, scoped to the **doc-authoring** workflow (this repo has no
    application code, so `scripts/`/`envs/` here are for doc-tooling, e.g. a future
    Markdown-lint script, not app config).
  - `treklink-web/ignore/`, scoped to the **code** workflow.
  - `treklink-firmware/` and any hardware repo are **out of scope this session**, handled
    directly by the team.
- **Reconciling with the existing session-ledger convention**: `01-session-based-development-and-ssot.md`
  §4 and `08-ai-agent-steering-and-discipline.md`'s Stage 2.5 define the ledger. **(Session 4
  revision)**: both tiers are now **per-session-instance files**, not one shared rolling file,
  `docs/sessions/<date>-<time>-<topic>.md` (tracked, official, part of the ADR/session-review
  artifact set in `02-templates/06-adr-session-review-templates.md`) and
  `ignore/[name]/docs/sessions/<date>-<time>-<topic>.md` (untracked, low-ceremony, one per
  concurrent session). `current-progress.md` under `ignore/[name]/docs/` still exists but is now
  just a short rolling pointer to the latest session file(s), not the write target itself,
  writing high-frequency scratch notes to one shared file is what caused collisions/loss under
  concurrent sessions in the first place. Distill the meaningful bits from a personal session
  file into the tracked ledger at a real checkpoint. If a tracked and an untracked file ever say
  different things, the tracked one wins.
- **The Dual-Branch GitFlow pattern (§2.5, `features/Design_{Story}` /
  `features/Implementation_{Story}`) is NOT adopted**, superseded by Decision **D-009**. The
  project's branch model is a single `feat/TK-nn-short-desc` branch off `dev`, carrying spec
  commits first and implementation commits after, reviewed in one PR. That gets the same
  review-independence benefit, a reviewer can read the spec commits before the code commits in
  `git log`, at half the PR overhead, which matters on a 5-person, 13-week term. See
  `07-github-workflow-git-conventions.md` §2.3.
- Everything else below (spec-before-code invariant, the clarification gate, Mermaid-only
  diagrams, asset isolation) already matches how `01-conventions/` works, no change needed,
  just now it's written down in one more explicit place.

---

## 2. Universal Documentation-Driven Scaffold & SSOT Architecture

> **Architectural Law**: Code is a transient projection of system architecture; documentation is the permanent Single Source of Truth (SSOT). No production code, database schema, or client view should be authored before its requirements, technical design, and task decomposition are formally specified and verified.

### 2.1 Master Scaffold Topology

```text
ignore/ (or workspace doc-root)
├── docs/                                  # Master Architecture, System Context & Living Ledger
│   ├── 00-system-context.md                # System boundaries, domain models, and high-level glossary
│   ├── current-progress.md                 # Living progress ledger, active tasks, and milestone state
│   ├── diagrams/                           # System entity relationship and architecture diagrams (.mmd)
│   └── flows/                              # End-to-end business interaction and user flows (.mmd)
├── scripts/                                # Local Tooling & Data Automation
│   └── README.md                           # Tooling execution guides and CLI usage
└── envs/                                   # Sensitive Configuration Templates & Credentials Matrix
    └── .env.example                        # Environment variable template
```

(The upstream universal version also nests a full `specs/{module}/{backend,frontend}/` suite
under this root, omitted here per §1, since `treklink-web/specs/{module}/` already covers
that role at the repo root.)

### 2.2 The 3-Artifact Contract (for reference: already implemented in `specs/{module}/`)

| Artifact | Responsibility | Format / Standard |
|---|---|---|
| `requirements.md` | Business rules, user stories, acceptance criteria | **EARS Syntax** (Ubiquitous, Event-Driven, State-Driven, Unwanted Behavior, Optional) |
| `design.md` | Data schemas, domain models, sequence diagrams | Architecture descriptions + Mermaid sequence/activity flows |
| `tasks.md` | Granular work breakdown across 5–6 logical phases | Checklists with checkboxes (`- [ ]`) |
| `api-design/` | Granular HTTP/RPC interface documentation | Individual endpoint specs + verification guide |

### 2.3 Core Operational Conventions

**Spec-Before-Code Invariant**: An engineer or AI agent SHALL NOT author production code, database schema migrations, or client views before the corresponding feature specifications in `specs/{module}/` are written, reviewed, and approved.

$$\text{Clarification Gate} \longrightarrow \text{requirements.md} \longrightarrow \text{design.md} \longrightarrow \text{tasks.md} \longrightarrow \text{Implementation}$$

**Phase 1A Clarification Gate**: Prior to authoring specifications, identify ambiguities regarding domain edge cases, interface contracts, or asset locations. **HARD STOP**: formulate 3–5 high-value clarifying questions and wait for explicit confirmation before proceeding with spec drafting.

**Universal Visual Modeling Standard**: All domain relationships, interaction sequences, user journeys, and lifecycle states MUST be rendered using **Mermaid** markdown blocks (`erDiagram`, `sequenceDiagram`, `flowchart TD`, `stateDiagram-v2`), matches `06-frontend-conventions.md`/`04-architecture-conventions.md`'s existing Mermaid-only rule.

**Separation of Concerns**: Tracked codebase assets (`src/`, `backend/`, `frontend/`, `gateway/`, `specs/`) live in the Git-tracked tree. `ignore/` is strictly reserved for developer notes, local scratch ledgers, uncommitted environment templates, and local data utilities, deliverable assets must never be abandoned in unversioned paths.

**Living Progress Ledger**: Maintain `ignore/docs/current-progress.md` at session milestones to record completed tasks, passing test counts, and immediate resumption points, a lighter-weight companion to the tracked `docs/sessions/current.md` (see §1).
