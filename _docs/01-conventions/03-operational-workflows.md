# Engineering Lifecycle & Operational Workflows

> Four canonical, repeatable workflows for feature development, defect diagnosis, code review, and review-comment resolution. Applies equally whether the acting party is a teammate or an AI coding agent.

---

## 1. Executive Workflow Matrix

```mermaid
flowchart TD
    subgraph Flow1["1. Normal Feature Development Flow"]
        D1["Fetch origin & sync develop"] --> D2["Discovery & Clarification Interview"]
        D2 --> D3["Author requirements.md, design.md, tasks.md"]
        D3 --> D4["Create isolated feature branch"]
        D4 --> D5["Phased implementation & unit tests"]
        D5 --> D6["Automated quality & verification gate"]
        D6 --> D7["Rebase on origin/develop & push"]
        D7 --> D8["Open PR & return to develop"]
    end

    subgraph Flow2["2. Diagnostic & Debugging Flow"]
        B1["Checkout defect/hotfix branch"] --> B2["State falsifiable hypothesis"]
        B2 --> B3["Inspect primary log & code evidence"]
        B3 --> B4["Execute minimal surgical fix"]
        B4 --> B5["Add dedicated regression test"]
        B5 --> B6["Verify zero regressions across suite"]
        B6 --> B7["Push with [Fix] tag & return to develop"]
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
        S4 --> S5["Commit [Fix] & push to branch"]
        S5 --> S6["Deliver structured resolution table"]
    end
```

---

## 2. Lifecycle 1: Normal Feature Development Flow (Spec-First)

### Step 1: Baseline Synchronization
```bash
git fetch origin
git checkout develop
git pull origin develop
```

### Step 2: Discovery, Clarification & Spec Authoring
Review the target module's charter section, existing entities, and dependent modules. Run the **Phase 1A Mandatory Gate** clarification interview (see `02-spec-driven-development-workflow.md`) — hard stop until answered. Author `specs/{module}/requirements.md` → `design.md` → `tasks.md` → `api-design/`.

### Step 3: Branch Creation & Isolation
```bash
git checkout -b features/Implementation_{UserStoryName}
# If the story needs a documented API/UI design first:
git checkout -b features/Design_{UserStoryName}
```

### Step 4: Phased Clean Implementation
Follow `tasks.md` phase-by-phase. Commit small, atomic units with bracket tags (`[Feature]`, `[Fix]`, `[Refactor]`, `[Test]`, `[Spec]`).

### Step 5: Quality Gate & Verification
```bash
# Backend (NestJS) — from the backend package root
npm run lint && npm run typecheck && npm test && npm run test:e2e

# Gateway (Node/TS)
npm run lint && npm test

# Frontend (React)
npm run lint && npm run build && npm test
```
Confirm **100% test pass rate**, 0 lint errors, clean build. Backend endpoint behavior must match `specs/{module}/api-design/*.md` exactly (same response envelope — see `05-backend-conventions.md`).

### Step 6: Upstream Rebase & Push
```bash
git fetch origin
git rebase origin/develop
# re-run Step 5 after resolving any conflicts
git push origin features/Implementation_{UserStoryName}
```

### Step 7: PR Assembly & Return to Base
Open the PR from `.github/PULL_REQUEST_TEMPLATE/implementation.md` (or `design.md` for the sibling design branch). Checkout back to `develop`.

---

## 3. Lifecycle 2: Diagnostic & Debugging Flow (Hypothesis-Driven)

### Step 1: Checkout Target Branch
```bash
git checkout features/Implementation_{UserStoryName}
# OR for a production-critical defect:
git checkout -b hotfix/Bug_{DefectName}
```

### Step 2: Hypothesis Formulation & Investigation
State a single falsifiable hypothesis. Inspect logs/stack traces/source lines with real tool calls, not guesses. Assess blast radius — e.g. a fix to the idempotency key logic touches every consumer of `eventId` across gateway + backend.

### Step 3: Minimal Surgical Fix
Address the root cause only. No unrelated refactors or formatting changes bundled in.

### Step 4: Dedicated Regression Test
Add a test that reproduces the failure without the fix and passes with it. Run the full suite — zero downstream regressions.

### Step 5: Push & Return to Base
```bash
git commit -m "[Fix] Precise description of resolved defect (#IssueID)"
git push origin hotfix/Bug_{DefectName}
git checkout develop
```
Output a diagnostic summary: root cause, fix mechanics, regression-test proof.

---

## 4. Lifecycle 3: Pull Request & Code Review Flow

### Step 1: Branch Fetch & Diff Inspection
```bash
git fetch origin
git log --oneline origin/develop..origin/{target_branch}
git diff origin/develop...origin/{target_branch}
```
Or via GitHub CLI: `gh pr diff {number}`, `gh pr checks {number}`.

### Step 2: Architectural & Code Quality Audit
- [ ] Module boundaries respected (no cross-module repository access — see `04-architecture-conventions.md` §4)
- [ ] DTOs strictly typed with `class-validator`, matching `api-design/*.md`
- [ ] Errors use the standard envelope (`result`/`isSuccess`/`statusCode`/`message`), not ad-hoc shapes
- [ ] Security: mutating endpoints have both a JWT guard and a role/CASL policy check — e.g. `@UseGuards(JwtAuthGuard, PoliciesGuard)` on any endpoint that mutates device/rental/incident state
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
git commit -m "[Fix] Address review feedback on {topic}"
git push
```

Output a resolution table:

| # | Reviewer Comment | Severity | Applied Fix | Status |
|:---:|---|:---:|---|:---:|
| 1 | Missing role guard on device retire endpoint | 🔴 Critical | Added `@Roles('Admin')` + CASL `can('retire','Device')` check | Resolved |
| 2 | Duplicate-SOS test only covers 2 retries, NFR needs 10 | 🟡 Medium | Extended test to 10× replay of same `eventId` | Resolved |
