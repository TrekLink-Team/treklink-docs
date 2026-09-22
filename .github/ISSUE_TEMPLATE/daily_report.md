---
name: Daily Report
about: Manual fallback, the daily report issue is normally opened automatically at 08:00 ICT
title: "DAILY REPORT DD/MM/YYYY"
labels: "type:daily-report"
assignees: ""
---

<!--
NORMAL FLOW: CI opens this issue automatically at 08:00 ICT, Monday-Friday, and closes it at
12:00 ICT. Use this template ONLY when you need one manually, a weekend, a holiday, or if CI
failed to fire.

Convention: 01-conventions/12-communication-and-daily-reports.md §3
-->

Every member comments their report on **this** issue, **before 12:00 ICT**.

**Format, exactly three fields:**

```markdown
YourCode

Yesterday: what you did (link the PR / issue)
Today: what you will do

Issues: blocker, or None
```

English is required. Vietnamese is tolerated by exception here, and **only** here, when
English would cost you clarity about a blocker.

---

## Reported

- [ ] @KhoaDD
- [ ] @LongLP
- [ ] @HoangTK
- [ ] @LongNN
- [ ] @TanNB

---

> **The 12:00 cutoff is hard.** CI closes this issue at midday whether or not everyone has
> reported. Missed it? **Reopen** the issue, post your report, close it again. The reopen is
> deliberately visible, the timeline is the lateness log.
