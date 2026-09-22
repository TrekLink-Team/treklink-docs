# Contributing to TrekLink

The 2-minute version. Full detail lives in [`01-conventions/`](01-conventions/), which is also the
source of the [Developer Handbook PDF](TrekLink_Developer_Handbook_v1.0.pdf).

## 1. Orient yourself
- What are we building: [`00-project-context/01-project-charter.md`](00-project-context/01-project-charter.md)
- What week/sprint is it: [`00-project-context/02-roadmap-and-milestones.md`](00-project-context/02-roadmap-and-milestones.md)
- Anything blocking you: [`00-project-context/03-decisions-and-risk-register.md`](00-project-context/03-decisions-and-risk-register.md)

## 2. Where work lives
**Jira** is the single tracker ([TK project](https://treklink-capstone.atlassian.net/jira/software/projects/TK/summary)).
**GitHub Issues** hold daily reports and standalone bugs only. The **backlog**
([`03-backlog/`](03-backlog/)) is read-only to members, it holds the EARS criteria you implement
against. See [`01-conventions/10-jira-tracking-and-workflow.md`](01-conventions/10-jira-tracking-and-workflow.md).

## 3. Before writing code
Every module goes through `specs/{module}/requirements.md` → `design.md` → `tasks.md` **before**
implementation, see [`01-conventions/02-spec-driven-development-workflow.md`](01-conventions/02-spec-driven-development-workflow.md).
Blank templates in [`02-templates/`](02-templates/).

## 4. Branch, commit, PR
```bash
git fetch origin && git checkout dev && git pull origin dev
git checkout -b feat/TK-45-device-registration        # Jira key in the branch name

# ... work, per 01-conventions/03-operational-workflows.md ...
git commit -m "feat(TK-45): add device FSM transition guard"

npm test                                              # must be green BEFORE the PR
git fetch origin && git rebase origin/dev
git push -u origin feat/TK-45-device-registration --force-with-lease
gh pr create --base dev --title "feat(TK-45): device registration" --label "module:devices"
```
Then **move the Jira card to `IN REVIEW`** and **ping your reviewer in Zalo**.
Full convention: [`01-conventions/07-github-workflow-git-conventions.md`](01-conventions/07-github-workflow-git-conventions.md).

**No direct pushes to any branch, ever, including the leader's.**

## 5. Merging
Rebase & merge (single commit) or Squash & merge (multiple). **Merge commits are prohibited.**
Delete the source branch, except `dev` → `main`. **Announce every merge to `dev` in Zalo** so
everyone pulls and rebases.

## 6. Backend response contract (non-negotiable)
Every endpoint returns `{ result, isSuccess, statusCode, message }`, see
[`01-conventions/05-backend-conventions.md`](01-conventions/05-backend-conventions.md) §3.

## 7. Language
**English only**, code, commits, PRs, specs, docs, Jira cards. You may prompt your AI agent in
Vietnamese; what it writes to the repo is English regardless.

## 8. Using an AI coding agent
Read [`01-conventions/11-ai-first-doctrine-and-toolchain.md`](01-conventions/11-ai-first-doctrine-and-toolchain.md)
once, fully. Install `prompt-orchestrator` and the TrekLink skills, open the `capstone/` parent
folder (not a single repo), and run `/treklink-session`. The agent reads the conventions itself,
you should never have to tell it to.

## 9. Definition of Done, every PR
- [ ] EARS criteria in `requirements.md` satisfied
- [ ] **Unit tests written and passing**, before the PR is opened
- [ ] Module boundaries respected (no cross-module repository access)
- [ ] Lint/typecheck clean
- [ ] `api-design/*.md` updated in the same PR if any endpoint changed
- [ ] Rebased on `dev`; Jira card linked and moved to `IN REVIEW`
- [ ] `Model used:` declared in the PR
