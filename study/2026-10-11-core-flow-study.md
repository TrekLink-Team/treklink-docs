# Core Flow Study, 2026-10-11

A guided study session that every member runs with their own AI agent. The agent teaches the
member TrekLink's core direction, the five Main Flows and the architecture, checks the member's
understanding, collects the member's agreement and suggestions, and posts one result on
[issue 59](https://github.com/TrekLink-Team/treklink-docs/issues/59).

This file is temporary study material on branch `docs/core-flow-study`. It points at the sources
and never replaces them. Where this brief and a source disagree, the source wins, and the agent
reports the disagreement in the result.

## 1. Rules for the agent

- **Model**: Claude Sonnet 5, Opus 5 or Fable 5.1, or GPT-5.6 Sol or GPT-6 Astra (conventions
  chapter 11 §2.1). The session ends with an architecture assessment, which chapter 11 reserves
  for these models. On Gemini or any other model, stop and tell the member.
- **Read only.** Change no file in any repository. The only write is the one issue comment in §5.
- **Ground every answer** in a file and section from §2. If the sources do not answer a question,
  say so and add it to the open questions in the result. Never invent an answer.
- **Language**: teach in the language the member prefers (Vietnamese is fine). The issue comment
  is written in English (AGENTS.md §2.4).
- **Prose**: no em dash in the issue comment (AGENTS.md §2.7).

## 2. Sources, in reading order

Pull both repositories first, from the `capstone/` folder (AGENTS.md §1 layout). Commit or stash
any local work in `treklink-docs` before switching branch.

```bash
git pull
```

```bash
git -C treklink-docs fetch origin && git -C treklink-docs switch docs/core-flow-study && git -C treklink-docs pull
```

| # | File | What it gives |
|---|---|---|
| 1 | `treklink-docs/_docs/00-project-context/03-decisions-and-risk-register.md`, D-033 to D-039 | The direction after Review 1, lifecycles, incident tiers, and the open hosting question |
| 2 | `treklink-docs/_docs/00-project-context/05-main-flows.md` | The five Main Flows: swimlanes, steps, exception scenarios |
| 3 | `treklink-docs/_docs/00-project-context/06-requirements-foundation.md` | Context diagram, actors, use-case map, feature tree |
| 4 | `treklink-docs/_docs/00-project-context/08-whiteboard-target-flows.md` | The leader's whiteboard target flows of 2026-10-11 |
| 5 | `capstone/Documents/reports/Report3_SRS_DRAFT.md` | The SRS: use cases, requirements, state machines, NFRs |
| 6 | `treklink-docs/_docs/00-project-context/04-firmware-ground-truth.md` | What the firmware actually sends (read when MF-02 or MF-03 comes up) |

## 3. Curriculum

Teach one block at a time. After each block, ask the member to restate it in their own words,
then ask one or two check questions. Correct a wrong restatement with the source section, and
repeat the check until the restatement is right. Answer the member's questions as they come.

| Block | Content | Main source |
|---|---|---|
| A. Direction | TrekLink is the sole provider of devices, firmware, Field Station and cloud platform, and the asset manager of every device. Renters are corporate organizations only; many organizations on one platform is what makes it a platform. No bookings, trips, trek packages or individual renters. Monthly and day plans; handover and return at the TrekLink counter; monitoring always on; payments through a third-party sandbox payment gateway or at the counter. | D-033 |
| B. MF-01 | Organization onboarding, rental contract, handover | 05 §MF-01, 08 §4 |
| C. MF-02 | Field data, Field Station, cloud synchronization; Stages A, B and C; exactly-once and priority order | 05 §MF-02, 08 §3, 04 |
| D. MF-03 | SOS, tiered alert (on duty, backup, Manager), escalation to TrekLink; one incident per SOS episode | 05 §MF-03, D-034, 08 §2 |
| E. MF-04 | Live telemetry on the web map and the organization API, scoped by organization | 05 §MF-04 |
| F. MF-05 | Term end, return, inspection, billing, maintenance | 05 §MF-05, 08 §5 |
| G. Lifecycles | Device, organization and rental-contract states; the whiteboard asset flow | D-035, SRS state machines, 08 §1 |
| H. Architecture | Devices on a LoRa mesh; the Field Station on the organization's laptop with one node on USB serial, a durable queue and upload; the NestJS modular-monolith backend on PostgreSQL; the React web platform with Leaflet over OpenStreetMap; the organization API over REST and WebSocket; the payment gateway | 06 context diagram, AGENTS.md §4, SRS §2 |
| I. Open question | D-039: one TrekLink-hosted backend, or self-hosted backends on organization infrastructure, and how the Field Station gets updates | D-039 |

Spend the most time on the member's own Main Flow (named in their prompt). For that flow, also
ask the member to walk through it step by step without help, including one exception scenario.

## 4. Agreement and suggestions

After block I, ask the member, one question at a time:

1. Do you agree with the direction (block A)? If not, what would you change, and why?
2. For your own Main Flow: is anything missing, wrong or unclear in 05 or in the whiteboard
   version (08)? The whiteboard flows lack sequence diagrams for their sub-steps; which sub-steps
   of your flow need one first?
3. Do you agree with the architecture (block H)? What would you change?
4. D-039: which option do you support, and why?
5. Anything else you want the leader to know?

Record the answers in the member's words. Do not argue the member into agreement; you may point
to a source the member missed, once.

## 5. Posting the result

Draft the comment with the template below, show it to the member, apply their corrections, and
post it only after they say it is right:

```bash
gh issue comment 59 --repo TrekLink-Team/treklink-docs --body-file result.md
```

If `gh` is not signed in, give the member the finished text to paste on the issue page instead.

```markdown
## Core flow study result: <member short name> (<own Main Flow>)

**Model used**: <model>
**Understanding check**: <for each block A to I: understood first time / understood after correction / still unclear, one line each>
**Corrections made during the session**: <what the member first got wrong, briefly>

### Agreement
| Topic | Agree? | Member's comment |
|---|---|---|
| Direction (D-033) | Yes / Partly / No | |
| Own Main Flow | Yes / Partly / No | |
| Architecture | Yes / Partly / No | |
| D-039 option | 1 / 2 / 3 / undecided | |

### Suggested changes
- <each change the member proposes, with the reason they gave>

### Sub-steps that need a sequence diagram first
- <from question 2>

### Open questions the sources did not answer
- <question, and which source was checked>

### Source disagreements found
- <where this brief or one source contradicts another, with file and section; "none" if none>
```
