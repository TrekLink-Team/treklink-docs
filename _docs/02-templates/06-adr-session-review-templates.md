# Misc Templates: ADR, Session Checkpoint, Code Review Scorecard

## 1. Architecture Decision Record (ADR) Template

Use for any decision not already covered in `00-project-context/03-decisions-and-risk-register.md`. Add new ADRs as additional entries in that file (`D-00N`) rather than separate files, to keep one place to check for OPEN blockers.

```markdown
### D-00N — [Short decision title]
- **Status**: 🟡 OPEN | ✅ Resolved | ❌ Superseded by D-0XX
- **Context**: [What forces this decision — conflicting sources, a tradeoff, a constraint from the register's NFRs]
- **Options considered**: [A vs B vs …]
- **Decision**: [What was chosen and why]
- **Blocks**: [What work can't start until this resolves]
- **Owner**: [who confirms/executes]
```

---

## 2. Session Checkpoint Template

Save as `docs/sessions/current.md` (rolling) or `docs/sessions/YYYY-MM-DD-{module}.md` (archival), per `01-conventions/01-session-based-development-and-ssot.md` §4.

```markdown
# Session Checkpoint: [Date] — [module]

## 1. Active Focus & Objectives
- Module / Story: [ID & title]
- Branch: [features/Implementation_... or Design_...]

## 2. Completed Milestones
- [x] Phase N: [what was finished, from tasks.md]

## 3. Immediate Next Steps
1. [next concrete action]
2. [next concrete action]

## 4. Uncommitted State / Known Blockers
- Working tree: [clean / dirty — commit hash]
- Test status: [X/Y passing]
- Open questions: [none, or link to a decisions-log entry]
```

---

## 3. Code Review Scorecard Template

Use for a structured written review (peer or AI-assisted) beyond the PR's inline comments — useful ahead of Review 1/2/3 when the supervisor may ask "walk me through how this was reviewed."

```markdown
# Code Review: [PR title / branch name]

## 1. Executive Assessment
- **Reviewer**: [name / AI agent]
- **Decision**: `[APPROVED]` | `[CHANGES REQUESTED]` | `[NEEDS FIXES]`
- **Summary**: [one paragraph]

## 2. Checklist
- [ ] Module boundaries respected (01-conventions/04-architecture-conventions.md §1.1)
- [ ] Response envelope standard followed (result/isSuccess/statusCode/message)
- [ ] Centralized error codes used, no ad-hoc strings
- [ ] Auth guard + role/CASL policy present on mutating endpoints
- [ ] Test coverage includes error paths and (if applicable) FSM transitions
- [ ] `specs/{module}/api-design/*.md` matches the actual implementation

## 3. Specific Findings
### Finding 1: [title]
- **Severity**: 🔴 Critical / 🟡 Medium / 🟠 Low
- **File**: `path/to/file.ts:L45-L52`
- **Observation**: […]
- **Recommended diff**:
\`\`\`diff
- old_code()
+ new_code()
\`\`\`
```
