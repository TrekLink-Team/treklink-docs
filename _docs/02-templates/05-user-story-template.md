# User Story / Backlog Item Template

> This documents the columns used in [`User_Story_Backlog_TEMPLATE.xlsx`](User_Story_Backlog_TEMPLATE.xlsx) (in this same folder) and in the GitHub Issue form `.github/ISSUE_TEMPLATE/user_story.md`. It extends the team's existing `User_Story_Agile.xlsx` schema, same core columns, kept Jira/GitHub-CSV-import-compatible, with three additions (`Epic/Module`, `Sprint/Milestone`, `GitHub Issue #`) needed to tie the backlog to the actual roadmap and repo.
>
> **This is a template only, no real backlog rows are filled in here.** Start populating the xlsx (or GitHub Issues directly) once TP1's requirements pass are underway.

## Columns

| Column | Required | Notes |
|---|---|---|
| **Issue Type** | Yes | `Epic` \| `Story` \| `Task` \| `Bug` \| `Spec` \| `Chore` |
| **Epic/Module** | Yes | One of: Identity & RBAC · Device Fleet & Maintenance · Trip & Rental Management · Gateway & Offline Sync · Real-Time Monitoring & SOS Incidents · Billing & Reporting · DevOps/CI-CD |
| **Summary** | Yes | For `Story`: `"As a <role>, I want to <action>, so that <benefit>"`. For `Epic`: a one-line capability description. |
| **Description (incl. Acceptance Criteria)** | Yes for Story/Bug | Numbered `AC-01`, `AC-02`, …, same convention as the original `User_Story_Agile.xlsx`. Prefer EARS phrasing (`WHEN…THEN the system SHALL…`) where it fits, matching `01-requirements-template.md`. |
| **Issue Id** | Yes | Internal short ID (`T1`, `T2`, …) for cross-referencing before a GitHub Issue number exists |
| **Parent** | For Story/Task | The Epic's Issue Id |
| **Priority** | Yes | `High` \| `Medium` \| `Low` |
| **Story Point Estimate** | Yes for Story/Task | Fibonacci-like: `1, 2, 3, 5, 8, 13` only |
| **Sprint / Milestone** | Yes once scheduled | Must match a GitHub Milestone name from `00-project-context/02-roadmap-and-milestones.md` §2/§3, e.g. `Sprint 2 (Wk3-4)` |
| **Status** | Yes | `Backlog` \| `Ready` \| `In Progress` \| `In Review` \| `Done` |
| **GitHub Issue #** | Once created | Backfill after `gh issue create`/UI creation, keeps the spreadsheet and the repo in sync |

## Example (illustrative only: not a real backlog entry)

| Issue Type | Epic/Module | Summary | Description | Issue Id | Parent | Priority | Points |
|---|---|---|---|---|---|---|---|
| Epic | Gateway & Offline Sync | The Gateway reliably delivers field events to the cloud under intermittent connectivity | — | E-GW | — | High | — |
| Story | Gateway & Offline Sync | As a Gateway operator, I want SOS events to sync before GPS/telemetry on reconnect, so that safety-critical data isn't delayed | AC-01: WHEN connectivity is restored, THEN the Gateway SHALL flush all P0 events before P2/P3.\nAC-02: The system SHALL log retry count and queue depth per tier. | T-EX01 | E-GW | High | 8 |

## Converting a backlog row into a GitHub Issue

1. Copy **Summary** → Issue title.
2. Copy **Description** (with AC-xx list) → Issue body, using `.github/ISSUE_TEMPLATE/user_story.md`.
3. Apply labels: one `type:*`, one `module:*`, one `points: N` (see `01-conventions/07-github-workflow-git-conventions.md` §2.1).
4. Set Milestone = the Sprint/Milestone column value.
5. If the Story decomposes into Tasks, create them as **sub-issues** (§2.4 of the same doc) and set **Parent** in the sheet to the Story's Issue Id for traceability, even though GitHub tracks the real parent-child link natively.
