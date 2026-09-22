# Prose and Wording Conventions

> **Scope**: every tracked document in every TrekLink repository, the generated handbook, module
> specs, commit messages, PR bodies, issue text, code comments, Jira card text, and the graded
> reports under `capstone/Documents/`. It also governs what an AI agent writes in chat.
>
> **Status**: binding from 2026-09-22 (Session 8). Recorded as **D-024**.

The reader is a teammate, a supervisor or a council reviewer looking for one specific thing, usually
under time pressure. Write for that reader.

---

## 1. Hard rules

| Rule | Applies to |
|---|---|
| No em dash `—` in prose | Everything written into a repository, and every chat reply |
| No en dash `–` as a clause separator | Same |
| No banned openers | Same |

**Permitted uses of an em dash**, because they are data or quoted content rather than prose:

- inside a fenced code block or an inline code span
- a table cell used as a "not applicable" placeholder
- a verbatim quotation of source text, a log line, or an upstream document

> [!NOTE]
> Documents written before 2026-09-22 are full of em dashes. They are corrected when the file is
> next edited for another reason, per §6. Do not open a repository-wide rewrite pass.

### 1.1 Replace the em dash

Join the statements with a comma. Split into two sentences where the comma produces a run-on. Use a
colon when the second clause explains the first, and parentheses for a true aside.

| Instead of | Write |
|---|---|
| `The queue is bounded — verify the shedding policy` | `The queue is bounded, verify the shedding policy` |
| `Two flows share the defect — MF-02 is worse` | `Two flows share the defect. MF-02 is worse` |
| `Stage B — the on-device queue` | `Stage B, the on-device queue` |

### 1.2 Banned openers

`Let's`, `In order to`, `It's worth noting`, `Needless to say`, `At the end of the day`,
`It goes without saying`, `Simply put`.

Delete the opener and start with the statement.

### 1.3 No aphorism formulas

Do not write a memorable line in place of an accurate one.

| Instead of | Write |
|---|---|
| `A spec that doubles as a backlog is neither` | `Requirements live in requirements.md. The backlog stays generated from build_backlog.py` |

### 1.4 No two-beat antithesis

Do not use the `not X, but Y` shape as a rhetorical device. State what is true.

| Instead of | Write |
|---|---|
| `This is not a preference, it is a requirement` | `This is a requirement` |
| `Not a parser bug, a wire-format assumption` | `The parser assumed a custom PortNum that the firmware never emits` |

`Use X rather than Y` is an instruction. It is permitted.

### 1.5 No unverified claims

State only what the repository, the firmware source or returned tool output supports. Where a claim
is carried forward but unproven, mark it inline:

```
(unverified) The v3 LittleFS partition holds 1.5 MB after the OTA slot.
```

Use `(unverified)`, `(untested)` or `(needs check)`, then the claim. Add the item to
[`../00-project-context/03-decisions-and-risk-register.md`](../00-project-context/03-decisions-and-risk-register.md)
in the same edit, per the doc-sync rule in
[`08-ai-agent-steering-and-discipline.md`](08-ai-agent-steering-and-discipline.md). Do not delete
the claim, and do not silently promote it to fact.

This is the wording-level expression of the rule that
[`../00-project-context/04-firmware-ground-truth.md`](../00-project-context/04-firmware-ground-truth.md)
already enforces with `file:line` citations.

### 1.6 No fabricated precision

Do not quote a line count, a duration, a hash, a byte size or a percentage that was not measured.
An unverified figure is worse than no figure, because it survives into a decision and then into a
graded report.

---

## 2. Structure

Headings name a feature or a fault. A heading that could sit on any document is not a heading.

| Instead of | Write |
|---|---|
| `Overview` | `Eviction order during an uplink outage` |
| `Additional notes` | `A reboot empties the RAM queue` |
| `Considerations` | `The channel PSK protects RF, not the broker hop` |

Break text into blocks a reader can scan. Prefer a table for anything comparative, sequential with
branches, or enumerable. Prefer a numbered list for anything executed in order.

Commands are literal text on their own line. Never put a command and its explanation on the same
line.

Cut generic openers, restated context, and summaries of the paragraph above.

---

## 3. Keep all context

Brevity applies to the wording, not to the content. Do not delete a procedure, an evidence
reference, a rationale, a configuration value or a correction in the name of tone. Cut the words
around the fact, keep the fact.

Where a section is long because the subject is complex, break it into sub-headings and tables. Do
not summarise it away. A spec that lost its exception scenarios is not a shorter spec, it is an
incomplete one.

---

## 4. Ledger exemption

[`../00-project-context/03-decisions-and-risk-register.md`](../00-project-context/03-decisions-and-risk-register.md)
and the session files under `docs/sessions/` and `ignore/*/docs/sessions/` are append-only records.
They keep their full narrative and reasoning, because a compressed decision gets re-litigated later.

The wording rules in §1 still apply to them. Em dashes, banned openers and aphorism formulas are
removed. Existing entries are corrected in place for wording only, never for substance.

---

## 5. AI agent obligations

Every AI assistant working in any of the four repositories runs both of the following from session
start, without being asked. This is part of the toolchain mandate in
[`11-ai-first-doctrine-and-toolchain.md`](11-ai-first-doctrine-and-toolchain.md).

| Skill | Path | Purpose |
|---|---|---|
| `prose-and-wording` | `~/.claude/skills/prose-and-wording/SKILL.md` | This chapter, as an always-on skill |
| `caveman`, level `full` | `~/.claude/skills/caveman/SKILL.md` | Compressed chat register |

Division of labour:

- **caveman** governs the register of chat replies. It compresses.
- **this chapter** governs what any written text is allowed to contain.
- Anything persisted to a repository stays normal prose under §1 to §4. Commit messages, PR bodies,
  specs, comments, issue text and Jira cards are never written in caveman register.
- On conflict, clarity wins. Caveman never authorises an em dash.

An assistant that is not Claude Code installs the equivalent rule in its own always-on
configuration file, or carries this chapter in its system prompt. A missing skill is not an excuse:
the rules in §1 are enforced by review regardless of tooling.

---

## 6. Applying this to existing documents

Bring a file to these conventions when you edit it for another reason. Do not open a separate
rewrite pass for a file you are not otherwise touching, unless the leader asks for exactly that.

The four canonical `AGENTS.md` copies and this conventions folder are the exception: they teach the
rules, so they were corrected first, on 2026-09-22.

### 6.1 Never swept

These are excluded from every mechanical wording pass, and the checker skips them:

| Path | Why |
|---|---|
| `topics/` | Course-issued and officially submitted. The registered capstone title is frozen and must match the form the school holds. |
| `ignore/` | Gitignored personal scratch, not a deliverable |
| `_docs/03-backlog/01-epics.md`, `02-user-stories.md` | Generated. Fix `build_backlog.py` and regenerate. |
| `_docs/TrekLink_Developer_Handbook_v1.0.pdf` | Generated from this folder |

> [!WARNING]
> On 2026-09-22 an exclusion filter silently failed and a sweep reworded the registered project
> title in both `topics/` forms. It was caught by sampling the diff and reverted with no net
> change. **Print the file list the sweep will touch and confirm the exclusion held**, before
> writing anything. See [`08-ai-agent-steering-and-discipline.md`](08-ai-agent-steering-and-discipline.md) Stage 2.7.

### 6.2 How a sweep is verified

Correctness, not finish. Read a representative sample of the diff rather than every line. Then:

1. `git diff --check`, for the trailing whitespace a blind em dash join leaves behind.
2. Confirm the excluded paths are absent from `git diff --name-only`.
3. Run the checker in §7.

---

## 7. Checking

```bash
python3 .github/scripts/check_prose.py
```

It runs in CI on every pull request and every push to `dev` and `main`, as
`.github/workflows/prose-check.yml`. Exit code 1 on any violation, reported as
`file:line: rule: text`.

Two rules are enforced there: the em dash in prose, and a banned opener at the start of a sentence.
Everything else in this chapter is review-enforced. A checker that guesses at aphorism formulas or
unverified claims produces false positives, and a check that cries wolf gets ignored.

Scan a single file before committing it:

```bash
python3 .github/scripts/check_prose.py _docs/01-conventions/07-github-workflow-git-conventions.md
```
