# Team Communication, Daily Reports & Schedule Awareness

> How the team stays synchronised: where each kind of message belongs, the daily report ritual, the
> merge-announcement obligation, and the automated schedule countdown.

---

## 1. Channels: What Goes Where

| Channel | Use for | Do **not** use for |
|---|---|---|
| **Zalo group** | Merge announcements, reviewer pings, "I'm blocked", fast coordination | Anything that needs to survive the week. Zalo is not a record. |
| **GitHub Issues** (`treklink-docs`) | Daily reports, standalone bugs, blockers needing a written thread | Feature work, that's Jira |
| **Jira** | All work tracking: epics, stories, tasks, subtasks, sprint state | Discussion. Cards are state, not conversation. |
| **PR comments** | Code review, design debate tied to a specific change | Status updates |
| **`treklink-docs` `_docs/`** | Decisions, conventions, anything that must outlive the term | Work-in-progress notes |
| **`ignore/{your_name}/`** | Your own notes, session files, scratch | Anything a teammate needs to see |

**The rule of durability**: if losing a message would cost the team, it does not belong in Zalo.

---

## 2. The Two Mandatory Announcements

### 2.1 Merging into `dev`

> [!IMPORTANT]
> **Every merge into `dev` must be announced in the Zalo group, immediately.**

Everyone else must stop, pull, and rebase, see
[`07-github-workflow-git-conventions.md`](07-github-workflow-git-conventions.md) §4.2. That
obligation cannot be honoured if nobody knows the merge happened. Merging silently and letting four
teammates discover it via conflicts three hours later is the most expensive avoidable mistake on
this project.

```text
Merged PR #42 → dev : feat(TK-45) device registration
Everyone please pull + rebase your branches.
```

### 2.2 Pinging your reviewer

Opening a PR is not a request for review, GitHub notifications are not reliably read. **Ping the
reviewer in Zalo with the PR link.** That ping starts the SLA clock (§5.5 of the Git chapter:
same-day if opened 08:00–17:00, one day absolute ceiling).

---

## 3. Daily Reports

### 3.1 The ritual

Every working day, an automated GitHub Issue titled `DAILY REPORT DD/MM/YYYY` opens in
`treklink-docs` at **08:00 ICT**. Every member comments their report on **that day's issue**. The
issue **auto-closes at 12:00 ICT**.

### 3.2 Format: exactly three lines

```markdown
KhoaDD

Yesterday: compile docs for report1
Today: Plan main flows

Issues: None
```

- **Yesterday**, what you did. Link the PR or the issue if there is one.
- **Today**, what you will do.
- **Issues**, blockers, or `None`. Do not leave this blank.

Keep it to those three fields. The value is in everyone being able to read five reports in thirty
seconds.

### 3.3 The 12:00 cutoff and lateness

> [!IMPORTANT]
> **Reports are due before 12:00 (midday).** CI closes the issue at 12:00 sharp regardless of who
> has reported.

If you missed the cutoff:
1. **Reopen the issue.**
2. Post your report.
3. Close it again.

The reopen is deliberately visible. The issue timeline records who reported after the cutoff and
when, it doubles as the lateness log, without anyone having to police it manually. The closing
comment CI posts at 12:00 names anyone who hadn't reported yet.

This is a discipline mechanism, not a punishment one. Consistent lateness is a signal to the leader
that something needs addressing, which is exactly what a leader should be able to see.

### 3.4 Language

**English is required and strongly preferred.** Vietnamese is tolerated *by exception* in daily
reports only, when writing it in English would genuinely cost you clarity about a blocker.

This is the only place in the entire project where non-English text is acceptable. Everything else
, code, commits, PRs, specs, Jira cards, documentation, is English without exception. See
[`07-github-workflow-git-conventions.md`](07-github-workflow-git-conventions.md) §6.

### 3.5 Schedule

| | |
|---|---|
| **Opens** | 08:00 ICT (UTC+7), **Monday–Friday** |
| **Closes** | 12:00 ICT, same day |
| **Weekends** | No automatic issue |
| **Holidays / no-class days** | Skipped automatically where the CI can determine it |

Working outside business hours or at a weekend? **Create the daily report issue manually**, same
title format, and report into it.

### 3.6 Notifications

The opening issue **@-mentions all five members**, which triggers GitHub's email notification to
everyone. That is intentional, the mail is the nudge. It also posts a checklist so who has and
hasn't reported is visible at a glance:

```markdown
### Reported
- [ ] @ruskicoder (KhoaDD)
- [ ] @lamphilong2004 (LongLP)
- [ ] @wangf28 (HoangTK)
- [ ] @NgocLong216 (LongNN)
- [ ] @nguyenbatan21112003 (TanNB)
```

The roll-call carries the handle **and** the team code. The handle is what notifies. The code is
what a reader recognises, because the handles do not resemble the codes.

> [!WARNING]
> `@handle` is what sends the notification. A markdown link, `[@handle](https://github.com/handle)`,
> renders identically and notifies nobody. Never tidy the mentions into links.
>
> A handle must also be an **org member**. GitHub does not notify a mention of someone without
> access, so a wrong-but-real handle fails silently. `LongLP` pointed at a non-member account until
> 2026-09-17, and every daily report until then pinged nobody.

> [!CAUTION]
> **A scheduled workflow runs from the repository's default branch, which is `main`.** It reads the
> `.github/schedule.yml` that exists on `main`, never the one on your branch and never the one on
> `dev`. Correcting a handle on `dev` changes nothing in production until `dev` reaches `main`.
>
> This was live from the automation landing until 2026-09-22. `main` carried
> `LongLP: TODO-longlp`, `HoangTK: TODO-hoangtk`, `LongNN: TODO-longnn` and `TanNB: TODO-tannb`,
> so `mention()` took its placeholder branch and rendered `**LongLP**` rather than a mention.
> **Only `KhoaDD` was ever notified**, on every daily report the automation has produced. Issue #18
> of 21/09/2026 still shows it. The 2026-09-17 correction of `LongLP` was made on `dev` and could
> not have taken effect.
>
> After changing anything the scheduler reads, verify against `main`, not against your branch:
>
> ```bash
> git show origin/main:.github/schedule.yml
> ```

### 3.6.1 Verifying that the roll-call actually mentions people

A placeholder or missing handle renders `**CODE**` in bold. A working handle renders `@handle`.
Read the created issue, not the script:

```bash
gh issue view <n> --json body -q .body | sed -n '/### Reported/,/^---/p'
```

Every line must start with `- [ ] @`. A line showing `- [ ] **CODE**` is a member who is not being
notified.

### 3.7 The closing comment

At 12:00 the script posts one comment and closes the issue. It names both groups in the same
format as the opening roll-call:

```markdown
**Cutoff reached, 12:00 ICT 17/09/2026.**

Reported (4/5): @ruskicoder (KhoaDD), @lamphilong2004 (LongLP), @wangf28 (HoangTK), @NgocLong216 (LongNN)

**Did not report before the cutoff:** @nguyenbatan21112003

Reopen this issue, post your report, and close it again. The reopen is the record.
```

Everyone is mentioned, including the members who did report. The closing comment is the day's
record, and a record that names four people by handle and the fifth by code is not one record.

Attendance is counted from the **human** comments only. The script filters out its own comments
before scanning, because the closing comment contains every reported member's code; an unfiltered
scan on a reopen-report-reclose cycle would read its own previous roll-call back and credit
everybody. See `.github/scripts/daily_report.py`.

---

## 4. Raising Problems

### 4.1 General rules (carried over from the team's existing practice)

1. The leader opens a daily report thread each working day, now automated.
2. Members report into that day's thread.
3. **Create additional issues whenever something needs solving together.** Do not wait for
   permission.
4. When something is blocking you, open an Issue so the leader can help resolve it.
5. A finished feature needing review: ping the reviewer via the PR **and** Zalo.

### 4.2 Blocked vs broken

Mirrors the Jira distinction in [`10-jira-tracking-and-workflow.md`](10-jira-tracking-and-workflow.md) §4:

| You are… | Do |
|---|---|
| **Blocked** (you can't proceed) | Jira → `NEEDS HELP`, tell the leader **why**, specifically |
| **Given broken code** (review found a defect) | Jira → `BUG`, fix on the same branch |
| **Hitting a standalone defect** | GitHub Issue, `type:bug` label |

Raise blockers **early**. A blocker on day 1 costs someone an hour. The same blocker on day 4 costs
the sprint.

---

## 5. Schedule Awareness: Automated Countdown

`treklink-docs` CI maintains a live countdown so nobody discovers a deadline the day it lands.

### 5.1 Two independent clocks

| Clock | Source | Cadence |
|---|---|---|
| **Team sprint** | Jira / the roadmap sprint mapping | Every 2 weeks |
| **Capstone roadmap milestone** | [`../00-project-context/02-roadmap-and-milestones.md`](../00-project-context/02-roadmap-and-milestones.md) | Fixed, external, immovable |

> [!WARNING]
> **These are not the same clock and one never implies the other.** A sprint ending is internal. A
> Review 1 dossier deadline is external and graded. When both land in the same week, the CI flags
> it loudly, those weeks are where things get dropped.

### 5.2 What the countdown shows

Posted to the repo `README.md` badge area and into the daily report issue:

```text
NEXT UP
  Sprint 2 ends ............... 6 days   (Sun 20 Sep)
  Report 2 due ................ tomorrow (Sun 20 Sep)   ⚠ COLLISION
  Review 1 dossier ............ 1 week 3 days (Sun 27 Sep)
  Scope lock (form FROZEN) .... 4 weeks 2 days (Sun 18 Oct)
```

Phrasing degrades naturally as a deadline approaches: `4 weeks 2 days` → `6 days` → `tomorrow` →
`TODAY`.

---

## 6. Weekly Rhythm

| When | What |
|---|---|
| **Daily, 08:00–12:00** | Daily report in that day's GitHub Issue |
| **Daily, as it happens** | Merge announcements + reviewer pings in Zalo |
| **Daily, 08:00–17:00** | PRs opened in work hours get reviewed before 17:00 |
| **Every 2 weeks** | Sprint close + planning; leader creates the next sprint's cards |
| **Weekly** | Supervisor (GVHD) meeting, leader prepares, per the roadmap |
| **Per roadmap milestone** | Report deliverable; see the roadmap calendar |

---

## 7. Quick Reference

| Situation | Channel | Urgency |
|---|---|---|
| Merged to `dev` | Zalo, immediately | Everyone must rebase |
| Need a review | PR assignment **+** Zalo ping | Same day if before 17:00 |
| Blocked | Jira `NEEDS HELP` + tell the leader | Immediately, do not sit on it |
| Found a standalone bug | GitHub Issue, `type:bug` | Same day |
| Daily status | GitHub Issue, that day's thread | Before 12:00 |
| Made a decision that outlives today | `_docs/00-project-context/03-decisions-and-risk-register.md` | Same working pass |
| Need to change a convention | `docs:` PR to `treklink-docs` | Team consensus |
