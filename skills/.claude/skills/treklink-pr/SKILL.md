---
name: treklink-pr
description: Open, review, fix, or merge a TrekLink pull request per Conventions v2. Trigger with "open a PR", "review PR #n", "address the review comments", "ready to merge", or when work on a feat/fix/docs/chore branch is complete.
argument-hint: <open | review <N> | fix <N> | merge <N>>
---

# /treklink-pr

Implements the PR lifecycle in `_docs/01-conventions/07-github-workflow-git-conventions.md` §5.

## Usage

```
/treklink-pr open          # open a PR from the current branch
/treklink-pr review 42     # review PR #42
/treklink-pr fix 42        # address review comments on PR #42
/treklink-pr merge 42      # merge PR #42
```

---

## `open`

1. **Verify the branch.** Must be `{type}/{TK-KEY}-{desc}` off `dev`. Never open a PR from `dev` or
   `main`.
2. **Run the gates locally, they must pass before the PR exists:**
   ```bash
   npm --prefix backend  run lint && npm --prefix backend  run typecheck && npm --prefix backend  test
   npm --prefix gateway  run lint && npm --prefix gateway  run typecheck && npm --prefix gateway  test
   npm --prefix frontend run lint && npm --prefix frontend run typecheck && npm --prefix frontend run build
   ```
   If tests fail, **stop**. Do not open the PR. A feature with failing or absent tests is not done.
3. **Rebase on `dev`:**
   ```bash
   git fetch origin && git rebase origin/dev
   ```
   Re-run the gates after resolving any conflict.
4. **Push** with `--force-with-lease` (never bare `--force`).
5. **Open the PR** against `dev`, title `type(TK-nn): short description`. Fill the template
   honestly, including **`Model used:`**, which is mandatory. Paste real test output.
6. Fill the **Design DoD** block only if this branch introduced or changed a spec.
7. Tell the user to: move the Jira card to `IN REVIEW`, and **ping the reviewer in Zalo**. The Zalo
   ping is what starts the review clock; GitHub notifications are not reliably read.

## `review <N>`

**Pull the branch and run it. Reading the diff in the browser is not a review.**

```bash
gh pr checkout <N>
npm ci
npm test        # run the suites yourself — do not trust the author's claim
```

Then audit:

- [ ] EARS criteria in `specs/{module}/requirements.md` actually satisfied
- [ ] Module boundaries respected, no cross-module repository/entity access
- [ ] Response envelope `{ result, isSuccess, statusCode, message }` on every new/changed endpoint
- [ ] JWT guard **and** role/CASL policy on every mutating endpoint
- [ ] Centralized error codes, not ad-hoc strings
- [ ] No N+1 queries; indexes match idempotency/uniqueness requirements
- [ ] **Tests exist and are meaningful**, not written to pass
- [ ] No secrets, `.env` values, debug logs, dead code, unresolved `TODO`s
- [ ] `api-design/*.md` updated in this same PR if an endpoint changed
- [ ] `Model used:` declared; if a restricted model touched a critical module, flag it

Output a decision, `[APPROVED]` / `[CHANGES REQUESTED]` / `[NEEDS FIXES]`, with findings at exact
`file:line` and drop-in diff suggestions. Severity-tag each: **Blocking / Suggestion / Nit /
Praise**.

> A **failing test is evidence of a flaw** until the author proves otherwise. "It's flaky" is a
> claim needing evidence, not a dismissal.
>
> **"LGTM" is for genuinely small changes you actually read and ran.** On a 400-line diff, a
> four-character review is a signature, not a review.

## `fix <N>`

1. Read **all** review comments in full before touching anything.
2. `git checkout` the PR's branch, **confirm you are on it.** Fixing a review on `dev` is a
   classic and painful mistake.
3. Make targeted fixes. No drive-by refactors.
4. Re-run the gates. Rebase if `dev` moved.
5. `git push --force-with-lease`.
6. **Comment on the PR** stating what you changed and what you deliberately did not, and why.
   Pushing silently does not re-request review.

If you are *stuck* on a comment rather than disagreeing with it: move the Jira card to
`NEEDS HELP`, say so in the PR, and tell the leader specifically what is blocking you.

## `merge <N>`

1. **Check approval.** Self-approval is permitted **only** for <50 lines, no behavioural impact,
   pure housekeeping. Otherwise a second party must approve, **including for the leader's own
   PRs**, which additionally require an independent AI review pass.
2. **Check CI.** Red CI does not block merge, but: the leader may merge red at their discretion; a
   non-leader reviewer needs the leader's explicit go-ahead; and the reason it is red goes in the
   PR before merging.
3. **Choose the method:**
   - Single commit → **Rebase and merge**
   - Multiple commits → **Squash and merge**
   - **Never "Create a merge commit"**, prohibited on this project.
4. **Delete the source branch**, except `dev` → `main`, where `dev` is never deleted.
5. Remind the user to **announce the merge in Zalo** so everyone pulls and rebases, and to verify
   the Jira card reached `DONE`.
