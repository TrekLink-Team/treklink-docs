# TrekLink: Engineering Documentation Set

> FA26SE159 · TrekLink Team · GitHub org: [`github.com/TrekLink-Team`](https://github.com/TrekLink-Team)
> Supervisor: Đặng Ngọc Minh Đức · Team: Đỗ Đăng Khoa (Leader), Trần Khải Hoàng, Lâm Phi Long, Nguyễn Bá Tân, Nguyễn Ngọc Long

> [!IMPORTANT]
> **Unified Documentation Root:** The master Single Source of Truth (SSOT), Obsidian Vault Golden Rules, and Git workflow conventions are unified at the repository root: [`../README.md`](../README.md).

This folder is meant to be copied into the product repo (or a dedicated `TrekLink-Team/docs` repo) as `docs/`. It is the **Single Source of Truth (SSOT)** for the capstone: if a decision, requirement, or convention is not written here, it does not exist for grading, review, or AI-agent-assisted development purposes.

## Repo scope & vault compatibility

This is a **docs-only** repository, it holds no application code. It's meant to be its own git-versioned repo (e.g. `TrekLink-Team/docs`) that is also directly usable as an **Obsidian vault**: open this folder in Obsidian as-is. That constrains a few authoring choices, kept consistent across every file here:
- Links are relative standard Markdown (`[text](../folder/file.md)`), not wikilinks, renders correctly in both GitHub and Obsidian.
- Diagrams are **Mermaid** (native in both GitHub's Markdown renderer and Obsidian ≥0.9), not PlantUML, except inside `02-templates/04-api-endpoint-template.md` where PlantUML is kept only because it's verbatim from the team's existing `API_Design_Template.md`, swap it for Mermaid in real endpoint docs if your Obsidian setup has no PlantUML plugin.
- Numbered folder/file prefixes (`00-`, `01-…`) control sort order identically in the GitHub file tree and Obsidian's file explorer.
- No Obsidian-only syntax (embeds, Dataview queries, plugin-specific blocks), keeps the vault readable on GitHub with zero plugins required.

Everything under `.github/` is the exception: those files are meaningless to Obsidian and exist purely to be copied into the root of `treklink-web`, the single active application repo (Gateway Bridge + NestJS backend + React frontend as workspace packages), see Decision D-004. The full 3-repo capstone layout (`treklink-docs`, `treklink-firmware`, `treklink-web`, cloned as siblings) is documented in the root `README.md` §1.

## How this doc set is organized

| Folder | Purpose | Read this when… |
|---|---|---|
| [`00-project-context/`](00-project-context/) | What we're building, why, the roadmap against capstone milestones, and open decisions | Onboarding, before Review 1/2/3 prep |
| [`01-conventions/`](01-conventions/) | How we work: session-based dev, spec-driven workflow, architecture, backend/frontend code rules, Git/GitHub flow, AI agent discipline, doc-driven scaffold/SSOT | Before writing any code or spec |
| [`02-templates/`](02-templates/) | Blank, reusable templates: requirements (EARS), design, tasks, API endpoint spec, user story backlog | Starting a new module/feature/spec |
| [`03-backlog/`](03-backlog/) | The actual epic/user-story backlog (8 epics, 87 stories) generated from `build_backlog.py`, and the source data for `User_Story_Agile_TrekLink.xlsx` | Sprint planning, picking up a story, checking who owns what |
| [`.github/`](.github/) | Drop-in GitHub repo config: PR templates, Issue templates, label taxonomy | Copy directly into the actual code repo's root |

## Quick start for a new session (human or AI agent)

1. Read [`00-project-context/01-project-charter.md`](00-project-context/01-project-charter.md) once, fully.
2. Check [`00-project-context/02-roadmap-and-milestones.md`](00-project-context/02-roadmap-and-milestones.md) to know which capstone milestone/sprint is active **today**.
3. Check [`00-project-context/03-decisions-and-risk-register.md`](00-project-context/03-decisions-and-risk-register.md) for anything marked `OPEN` that blocks your task.
4. **Touching anything that talks to a device?** Read [`00-project-context/04-firmware-ground-truth.md`](00-project-context/04-firmware-ground-truth.md) first. It records what the firmware *actually puts on the wire*, every claim cited to `file:line`. Three specification assumptions have already turned out to contradict it, do not design against the charter's description of the firmware without checking this file.
4. Follow [`01-conventions/02-spec-driven-development-workflow.md`](01-conventions/02-spec-driven-development-workflow.md): write/read `requirements.md` → `design.md` → `tasks.md` for the module under `specs/{module}/` in the code repo **before** touching code.
5. Branch, code, and open a PR per [`01-conventions/07-github-workflow-git-conventions.md`](01-conventions/07-github-workflow-git-conventions.md).
6. If you're an AI coding agent (Claude Code, Cursor, Copilot, etc.), also load [`01-conventions/08-ai-agent-steering-and-discipline.md`](01-conventions/08-ai-agent-steering-and-discipline.md) into your system/rules file.

## Document authority hierarchy

When two documents conflict, the higher tier wins until an ADR in `03-decisions-and-risk-register.md` formally supersedes it:

1. **Tier 1, Project Charter & Capstone Register** (`00-project-context/01-project-charter.md`, and the two submitted `Phieu_*.docx` register forms it reconciles)
2. **Tier 2, Module specs** (`specs/{module}/requirements.md`, `design.md` in the code repo) and **the backlog** (`03-backlog/`), a story's EARS criteria here is what gets expanded into that module's `requirements.md` once its sprint starts; if they ever disagree after that point, the code repo's `requirements.md` wins as the more detailed, reviewed artifact.
3. **Tier 3, Conventions** (`01-conventions/*`)
4. **Tier 4, Templates** (`02-templates/*`), starting points only, not binding once filled in
5. **Tier 5, Source code & tests**

## Source documents this set reconciles

- `Phieu_FA26SE159.docx`, the individually-submitted, detailed capstone register (formal RQs, NFRs, experiment protocol, TP1–TP6 task packages). Treated as the **primary/authoritative** spec.
- `Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.docx`, the team's earlier draft register (same project, 5-module framing, M1–M5). Used as a cross-check; where it differs from the FA26SE159 form, the latter wins (see `03-decisions-and-risk-register.md`, Decision D-000).
- `Git_Lab_Guide.pdf`, the school's GitLab/PR convention (v1.0, Aug 2025). Re-expressed for GitHub in `01-conventions/07-github-workflow-git-conventions.md`, same core philosophy.
- `API_Design_Template.md`, the team's existing API doc format. Adopted as-is as the canonical endpoint template (`02-templates/04-api-endpoint-template.md`); the response envelope it defines (`result` / `isSuccess` / `statusCode` / `message`) is now the **binding contract** for all TrekLink backend responses.
- `User_Story_Agile.xlsx`, the team's existing Jira-style backlog format (Issue Type / Summary / Description / Issue Id / Parent / Priority / Story Point Estimate). Extended slightly and reproduced as a blank template (`02-templates/User_Story_Backlog_TEMPLATE.xlsx`).
- `dev-flow.zip`, a session-driven + spec-driven (Kiro-style) engineering framework previously used on a .NET project. Ported to the TrekLink stack (NestJS/TypeScript backend, React frontend, Node.js gateway, PostgreSQL) in `01-conventions/`.
