# TrekLink Engineering Conventions — Index

Ported from a session-driven + spec-driven (Kiro-style) framework previously used on a .NET project (`dev-flow.zip`), adapted to TrekLink's actual stack: **NestJS/TypeScript backend, Node.js/TypeScript gateway, React/TypeScript frontend, PostgreSQL, GitHub**. The philosophy (files 01–03, 08) is framework-agnostic and carries over unchanged; the code/architecture/Git files (04–07) were rewritten for this stack.

| File | Domain | Changed from source? |
|---|---|---|
| [`01-session-based-development-and-ssot.md`](01-session-based-development-and-ssot.md) | Session-based dev, docs as SSOT, checkpointing | Light (MR→PR, path examples) |
| [`02-spec-driven-development-workflow.md`](02-spec-driven-development-workflow.md) | EARS requirements → design → tasks workflow | Light (module examples, PR references) |
| [`03-operational-workflows.md`](03-operational-workflows.md) | Feature dev / bugfix / review / review-resolution lifecycles | Light (test commands, PR references, auth example) |
| [`04-architecture-conventions.md`](04-architecture-conventions.md) | Module boundaries, entity conventions, FSD frontend | **Heavy** — Clean-Architecture/.NET rewritten as NestJS modular-monolith |
| [`05-backend-conventions.md`](05-backend-conventions.md) | NestJS module structure, DTOs, response envelope, error handling | **Heavy** — CQRS/MediatR/.NET rewritten for NestJS + the team's own response contract |
| [`06-frontend-conventions.md`](06-frontend-conventions.md) | FSD, state management triad, forms/UX, WCAG, Leaflet/WebSocket | Light (validation-mirroring example only) |
| [`07-github-workflow-git-conventions.md`](07-github-workflow-git-conventions.md) | Branching, commits, PR templates, GitHub-specific mechanics | **Heavy** — GitLab (`Git_Lab_Guide.pdf`) re-expressed for GitHub |
| [`08-ai-agent-steering-and-discipline.md`](08-ai-agent-steering-and-discipline.md) | AI coding agent behavior: thinking discipline, blast-radius checks, tool hierarchy | Light (paths, subagent roles) |
| [`09-doc-driven-scaffold-and-ssot-conventions.md`](09-doc-driven-scaffold-and-ssot-conventions.md) | `ignore/` folder scaffold (local session ledger, diagrams, scripts, envs) and how it reconciles with the existing tracked `specs/` and `docs/sessions/` | New this session — read its §1 first, it changes how the generic doc's paths map onto this repo |

## Adoption in a repo

1. Copy `01-conventions/` and `02-templates/` into the target repo as `docs/conventions/` and `docs/templates/`.
2. Copy `.github/` into the repo root as-is.
3. Create a tracked `specs/{module_name}/` folder per module (see `02-spec-driven-development-workflow.md` §2 for the exact layout).
4. Link `08-ai-agent-steering-and-discipline.md` and `07-github-workflow-git-conventions.md` into whatever file your AI coding assistant reads as its rules (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, Copilot custom instructions, etc.).
5. Never write production code before the requirements → design → tasks gate in `02-spec-driven-development-workflow.md` has been passed for that module.
