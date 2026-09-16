# TrekLink Engineering Conventions — Index

> **This folder is the TrekLink Developer Handbook.** It is the authoritative, machine-readable
> source. [`TrekLink_Developer_Handbook_v1.0.pdf`](../TrekLink_Developer_Handbook_v1.0.pdf) is a
> **generated render** of these files — never hand-edited, rebuilt automatically by CI whenever
> anything here changes. If the PDF and these files ever disagree, **these files win** and the PDF
> is stale; rebuild it.

**Conventions v2** (2026-09-13). Originally ported from a session-driven + spec-driven (Kiro-style)
framework used on a .NET project, then adapted to TrekLink's real stack: **NestJS/TypeScript
backend, Node.js/TypeScript gateway, React/TypeScript frontend, PostgreSQL, GitHub, Jira**.

---

## Read in this order

| # | File | Domain |
|---|---|---|
| **01** | [`01-session-based-development-and-ssot.md`](01-session-based-development-and-ssot.md) | Core philosophy: docs as SSOT, session-based development, crash-safe checkpointing |
| **02** | [`02-spec-driven-development-workflow.md`](02-spec-driven-development-workflow.md) | EARS requirements → design → tasks. The spec-before-code gate. |
| **03** | [`03-operational-workflows.md`](03-operational-workflows.md) | The four lifecycles: feature dev, debugging, code review, review resolution |
| **04** | [`04-architecture-conventions.md`](04-architecture-conventions.md) | Module boundaries, entity conventions, Feature-Sliced frontend |
| **05** | [`05-backend-conventions.md`](05-backend-conventions.md) | NestJS modules, DTOs, the response envelope, error handling |
| **06** | [`06-frontend-conventions.md`](06-frontend-conventions.md) | FSD, state management, forms/UX, WCAG, Leaflet, WebSocket |
| **07** | [`07-github-workflow-git-conventions.md`](07-github-workflow-git-conventions.md) | **Branching, commits, PRs, review, merge.** The most-referenced chapter. |
| **08** | [`08-ai-agent-steering-and-discipline.md`](08-ai-agent-steering-and-discipline.md) | AI agent behaviour: thinking discipline, blast radius, circuit breakers, doc-sync |
| **09** | [`09-doc-driven-scaffold-and-ssot-conventions.md`](09-doc-driven-scaffold-and-ssot-conventions.md) | The `ignore/` personal garden scaffold and how it reconciles with tracked `specs/` |
| **10** | [`10-jira-tracking-and-workflow.md`](10-jira-tracking-and-workflow.md) | **Jira board, statuses, the development loop, backlog↔Jira mapping** |
| **11** | [`11-ai-first-doctrine-and-toolchain.md`](11-ai-first-doctrine-and-toolchain.md) | **Model policy, required toolchain, session workflow, prompting standard** |
| **12** | [`12-communication-and-daily-reports.md`](12-communication-and-daily-reports.md) | Channels, daily reports, merge announcements, schedule countdown |

**If you read only three**: 07 (git), 10 (Jira), 11 (AI-first). Those three cover everything you
touch daily.

---

## What changed in v2 (2026-09-13)

Logged as **Decision D-009**, which supersedes D-003. Every one of these was a live contradiction
in v1 — the documented commands did not work.

| Was | Now |
|---|---|
| `develop` integration branch | **`dev`** — no repo ever had a `develop` branch |
| `[Feature]` bracket-tag commits | **Conventional Commits** — `feat(TK-45): add device FSM guard` |
| Dual `features/Design_X` + `features/Implementation_X` branches | **One branch per unit of work**, spec commits first |
| `release/sprint_x` branches | **Dropped** — `main` is the release |
| Squash-merge always | **Rebase & merge** default; squash only when multi-commit; merge commits **prohibited** |
| GitHub Issues + Milestones as the tracker | **Jira** is the single tracker; GitHub Issues = daily reports + bugs |
| `points:*` labels | Jira story points, base-5 scale (1/2/3/5/10/15/20/25/30) |
| Two PR templates | **One** `pull_request_template.md`, Design DoD optional |
| AI agent guidance scattered | Chapters **11** and **12**, plus a mandatory session workflow |

---

## Adopting these conventions in a repo

All three TrekLink repos use **identical** conventions. There is no per-repo exception.

1. Point the repo's `AGENTS.md` and `CLAUDE.md` at this folder — one canonical file, copied
   verbatim into `capstone/`, `treklink-docs/`, `treklink-web/`, and `treklink-firmware/`.
2. Copy [`../.github/`](../.github/) into the repo root as-is (PR template, issue templates, labels).
3. Run the label setup script in [`../.github/labels-and-milestones.md`](../.github/labels-and-milestones.md) §3.
4. Apply branch protection per [`07-github-workflow-git-conventions.md`](07-github-workflow-git-conventions.md) §7.
5. Create a tracked `specs/{module}/` folder per module — layout in
   [`02-spec-driven-development-workflow.md`](02-spec-driven-development-workflow.md) §2.
6. **Never write production code before the requirements → design → tasks gate has been passed.**

> [!IMPORTANT]
> Do **not** vendor a second copy of these files into another repo. A duplicated convention set
> drifts and then actively teaches the wrong rules — that is exactly what happened with
> `treklink-web/docs/conventions/`, which has been deleted for this reason. Link to this folder;
> don't copy it.

---

## Authority

When two documents conflict, the higher tier wins until an ADR in
[`../00-project-context/03-decisions-and-risk-register.md`](../00-project-context/03-decisions-and-risk-register.md)
supersedes it:

1. **Tier 1** — Project Charter & capstone registration form
2. **Tier 2** — Module specs (`treklink-web/specs/{module}/`) and the backlog (`../03-backlog/`)
3. **Tier 3** — These conventions
4. **Tier 4** — Templates (`../02-templates/`) — starting points, not binding once filled in
5. **Tier 5** — Source code & tests
