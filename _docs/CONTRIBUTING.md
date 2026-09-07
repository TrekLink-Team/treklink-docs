# Contributing to TrekLink

Quick-start for a teammate (or an AI coding agent) picking up work. Full detail lives in `01-conventions/`; this page is the 2-minute version.

## 1. Orient yourself
- What are we building: [`00-project-context/01-project-charter.md`](00-project-context/01-project-charter.md)
- What week/sprint is it: [`00-project-context/02-roadmap-and-milestones.md`](00-project-context/02-roadmap-and-milestones.md)
- Anything blocking you: [`00-project-context/03-decisions-and-risk-register.md`](00-project-context/03-decisions-and-risk-register.md)

## 2. Before writing code
Every module goes through `specs/{module}/requirements.md` → `design.md` → `tasks.md` **before** implementation — see [`01-conventions/02-spec-driven-development-workflow.md`](01-conventions/02-spec-driven-development-workflow.md). Use the blank templates in [`02-templates/`](02-templates/).

## 3. Branch, commit, PR
```bash
git checkout develop && git pull origin develop
git checkout -b features/Implementation_{StoryName}   # or Design_{StoryName}
# ... work, per 01-conventions/03-operational-workflows.md ...
git commit -m "[Feature] Short imperative description (#IssueNumber)"
git fetch origin && git rebase origin/develop
git push origin features/Implementation_{StoryName}
gh pr create --base develop --label "module:X" --label "points: N" --milestone "Sprint N"
```
Full convention: [`01-conventions/07-github-workflow-git-conventions.md`](01-conventions/07-github-workflow-git-conventions.md). PR templates auto-load from [`.github/PULL_REQUEST_TEMPLATE/`](.github/PULL_REQUEST_TEMPLATE/).

## 4. Backend response contract (non-negotiable)
Every endpoint returns `{ result, isSuccess, statusCode, message }` — see [`01-conventions/05-backend-conventions.md`](01-conventions/05-backend-conventions.md) §3 and the canonical example in [`02-templates/04-api-endpoint-template.md`](02-templates/04-api-endpoint-template.md).

## 5. Using an AI coding agent
Point it at [`01-conventions/08-ai-agent-steering-and-discipline.md`](01-conventions/08-ai-agent-steering-and-discipline.md) plus the GitHub workflow doc, via your tool's rules file (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, etc.).

## 6. Definition of Done, every PR
- [ ] EARS criteria in `requirements.md` satisfied
- [ ] Module boundaries respected (no cross-module repository access)
- [ ] Tests green, lint/typecheck clean
- [ ] `api-design/*.md` updated in the same PR if any endpoint changed
- [ ] Rebased on `develop`, PR linked to its Issue
