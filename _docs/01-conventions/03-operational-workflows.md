# Engineering Lifecycle & Operational Workflows

> Four canonical, repeatable workflows for feature development, defect diagnosis, code review, and review-comment resolution. Applies equally whether the acting party is a teammate or an AI coding agent.

---

## 1. Executive Workflow Matrix

See **Figure 1**.

```mermaid
flowchart TD
    subgraph Flow1["1. Normal Feature Development Flow"]
        D1["Fetch origin & sync dev"] --> D2["Discovery & Clarification Interview"]
        D2 --> D3["Author requirements.md, design.md, tasks.md"]
        D3 --> D4["Create isolated feature branch"]
        D4 --> D5["Phased implementation & unit tests"]
        D5 --> D6["Automated quality & verification gate"]
        D6 --> D7["Rebase on origin/dev & push"]
        D7 --> D8["Open PR & return to dev"]
    end

    subgraph Flow2["2. Diagnostic & Debugging Flow"]
        B1["Checkout defect/hotfix branch"] --> B2["State falsifiable hypothesis"]
        B2 --> B3["Inspect primary log & code evidence"]
        B3 --> B4["Execute minimal surgical fix"]
        B4 --> B5["Add dedicated regression test"]
        B5 --> B6["Verify zero regressions across suite"]
        B6 --> B7["Push with fix: tag & return to dev"]
    end

    subgraph Flow3["3. Code Review (PR) Flow"]
        R1["Fetch remote & inspect diff"] --> R2["Audit architecture, coupling & security"]
        R2 --> R3["Evaluate Definition of Done"]
        R3 --> R4["Run automated tests / CI"]
        R4 --> R5["Decision: Approve / Request Changes"]
    end

    subgraph Flow4["4. Review Issue Resolution Flow"]
        S1["Extract review comments (GitHub PR API/UI)"] --> S2["Severity triage: Critical / Medium / Low"]
        S2 --> S3["Implement targeted surgical fixes"]
        S3 --> S4["Run verification suite & type checks"]
        S4 --> S5["Commit fix: & push to branch"]
        S5 --> S6["Deliver structured resolution table"]
    end
```

***Figure 1***: The four operational workflows, normal feature development, defect handling, spec revision, and session handoff, and the points at which they hand off to one another. Placement: rotated plate, 182.0 x 199.7 mm, labels at 8.23 pt.

---

## 2. Lifecycle 1: Normal Feature Development Flow (Spec-First)

### Step 1: Baseline Synchronization
```bash
git fetch origin
git checkout dev
git pull origin dev
```

### Step 2: Discovery, Clarification & Spec Authoring
Review the target module's charter section, existing entities, and dependent modules. Run the **Phase 1A Mandatory Gate** clarification interview (see `02-spec-driven-development-workflow.md`), hard stop until answered. Author `specs/{module}/requirements.md` → `design.md` → `tasks.md` → `api-design/`.

### Step 3: Branch Creation & Isolation
```bash
git checkout -b feat/TK-45-device-registration
```

One branch per unit of work. Spec commits and implementation commits live on the **same** branch,
spec first, see `07-github-workflow-git-conventions.md` §2.3. Branch type is `feat/`, `fix/`,
`docs/`, or `chore/` as appropriate.

### Step 4: Phased Clean Implementation
Follow `tasks.md` phase-by-phase. Commit small, atomic units using Conventional Commits with the Jira key as scope, `feat(TK-45): ...`, `fix(TK-45): ...`, `test(TK-45): ...` (see `07-github-workflow-git-conventions.md` §3).

### Step 5: Quality Gate & Verification
```bash
# Backend (NestJS) — from the backend package root
npm run lint && npm run typecheck && npm test && npm run test:e2e

# Gateway (Node/TS)
npm run lint && npm test

# Frontend (React)
npm run lint && npm run build && npm test
```
Confirm **100% test pass rate**, 0 lint errors, clean build. Backend endpoint behavior must match `specs/{module}/api-design/*.md` exactly (same response envelope, see `05-backend-conventions.md`).

### Step 6: Upstream Rebase & Push
```bash
git fetch origin
git rebase origin/dev
# re-run Step 5 after resolving any conflicts
git push --force-with-lease origin feat/TK-45-device-registration
```

### Step 7: PR Assembly & Return to Base
Open the PR with `.github/pull_request_template.md`, fill the DoD, and **ping the reviewer in Zalo**. Move the Jira card to `IN REVIEW`. Checkout back to `dev`.

---

## 3. Lifecycle 2: Diagnostic & Debugging Flow (Hypothesis-Driven)

### Step 1: Checkout Target Branch
```bash
git checkout feat/TK-45-device-registration
# OR for an urgent defect — see 07-github-workflow-git-conventions.md §2.4
# for which branch to cut from (dev vs main):
git checkout -b hotfix/TK-99-jwt-expiry-crash
```

### Step 2: Hypothesis Formulation & Investigation
State a single falsifiable hypothesis. Inspect logs/stack traces/source lines with real tool calls, not guesses. Assess blast radius, e.g. a fix to the idempotency key logic touches every consumer of `eventId` across gateway + backend.

### Step 3: Minimal Surgical Fix
Address the root cause only. No unrelated refactors or formatting changes bundled in.

### Step 4: Dedicated Regression Test
Add a test that reproduces the failure without the fix and passes with it. Run the full suite, zero downstream regressions.

### Step 5: Push & Return to Base
```bash
git commit -m "fix(TK-99): precise description of the resolved defect"
git push --force-with-lease origin hotfix/TK-99-jwt-expiry-crash
git checkout dev
```
Output a diagnostic summary: root cause, fix mechanics, regression-test proof.

---

## 4. Lifecycle 3: Pull Request & Code Review Flow

### Step 1: Branch Fetch & Diff Inspection
```bash
git fetch origin
git log --oneline origin/dev..origin/{target_branch}
git diff origin/dev...origin/{target_branch}
```
Or via GitHub CLI: `gh pr diff {number}`, `gh pr checks {number}`.

### Step 2: Architectural & Code Quality Audit
- [ ] Module boundaries respected (no cross-module repository access, see `04-architecture-conventions.md` §4)
- [ ] DTOs strictly typed with `class-validator`, matching `api-design/*.md`
- [ ] Errors use the standard envelope (`result`/`isSuccess`/`statusCode`/`message`), not ad-hoc shapes
- [ ] Security: mutating endpoints have both a JWT guard and a role/CASL policy check, e.g. `@UseGuards(JwtAuthGuard, PoliciesGuard)` on any endpoint that mutates device/rental/incident state
- [ ] Performance: no N+1 queries, indexed lookups on `eventId`/device ID/trip ID
- [ ] Hygiene: no debug logs, dead code, hardcoded secrets, or `.env` values committed

### Step 3: Definition of Done Verification
Confirm DoD checklist in the PR description is honestly checked and CI is green.

### Step 4: Structured Review Output
- **Decision**: `[APPROVED]` | `[CHANGES REQUESTED]` | `[NEEDS FIXES]`
- **Findings**: exact file + line references, drop-in diff suggestions.

---

## 5. Lifecycle 4: Review Issue Resolution Flow

### Step 1: Retrieve Review Notes
Pull comments from the GitHub PR conversation thread (`gh pr view {number} --comments` or the UI).

### Step 2: Severity Triage
- 🔴 **Critical**: missing auth/RBAC guard, data corruption risk, broken CI, idempotency/priority-ordering violation.
- 🟡 **Medium**: performance issue, missing transaction rollback, unhandled edge case.
- 🟠 **Low/Hygiene**: formatting, naming, doc updates.

### Step 3: Implement Targeted Fixes
Address each comment directly, on the same branch, without unrelated scope changes.

### Step 4: Verification & Handoff
```bash
npm test && npm run lint
git commit -m "fix: Address review feedback on {topic}"
git push
```

Output a resolution table:

| # | Reviewer Comment | Severity | Applied Fix | Status |
|:---:|---|:---:|---|:---:|
| 1 | Missing role guard on device retire endpoint | 🔴 Critical | Added `@Roles('Admin')` + CASL `can('retire','Device')` check | Resolved |
| 2 | Duplicate-SOS test only covers 2 retries, NFR needs 10 | 🟡 Medium | Extended test to 10× replay of same `eventId` | Resolved |
