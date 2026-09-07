# TrekLink — Roadmap & Milestone Calendar

**Term start**: Monday, Sep 7, 2026 (today = Week 1, Day 1) · **Term span**: 09/2026–03/2027

## 1. Capstone review schedule (as given)

| Milestone | Timing | What happens |
|---|---|---|
| **Review 1** | Week 4 | Topic clarification, graded by 2 lecturers |
| Review 1 deadline | Week 6 | Revisions due |
| **Review 2** | Week 8 | System architecture (tech stack, features) |
| **Review 3** | Week 14 | Full product + documentation review — **go/no-go for Defense 1** |
| **Defense 1** | Week 15 | First defense |
| **Defense 2** | Week 19 (4 weeks after Defense 1) | Retake — **−20% score penalty** |

## 2. Calendar mapping (Mon–Sun weeks, from Sep 7, 2026)

| Week | Dates (2026) | Capstone milestone | TP phase(s) active (from FA26SE159 register) | Sprint |
|---|---|---|---|---|
| 1 | Sep 7 – Sep 13 | Kickoff (**today**) | TP1 start | Sprint 1 |
| 2 | Sep 14 – Sep 20 | — | TP1, TP2 start | Sprint 1 |
| 3 | Sep 21 – Sep 27 | — | TP1 close, TP2, TP3 start | Sprint 2 |
| 4 | Sep 28 – Oct 4 | **Review 1** (topic clarification) | TP2, TP3 | Sprint 2 |
| 5 | Oct 5 – Oct 11 | — | TP2 close, TP3, TP4 start | Sprint 3 |
| 6 | Oct 12 – Oct 18 | **Review 1 deadline** | TP3, TP4 | Sprint 3 |
| 7 | Oct 19 – Oct 25 | — | TP3 close, TP4, TP5 start | Sprint 4 |
| 8 | Oct 26 – Nov 1 | **Review 2** (architecture) | TP4, TP5 | Sprint 4 |
| 9 | Nov 2 – Nov 8 | — | TP4 close, TP5, TP6 start | Sprint 5 |
| 10 | Nov 9 – Nov 15 | — | TP5 close, TP6 | Sprint 5 |
| 11 | Nov 16 – Nov 22 | — | TP6 (integration/experiments) | Sprint 6 |
| 12 | Nov 23 – Nov 29 | — | TP6 | Sprint 6 |
| 13 | Nov 30 – Dec 6 | — | TP6 close (deployment, CI/CD, docs) | Sprint 7 |
| 14 | Dec 7 – Dec 13 | **Review 3** (full product + docs, go/no-go) | Buffer / freeze | Sprint 7 |
| 15 | Dec 14 – Dec 20 | **Defense 1** | — | Sprint 8 (short) |
| 16–18 | Dec 21 – Jan 10 | Post-defense fixes (if any) | — | — |
| 19 | ~Jan 11 – Jan 17, 2027 | **Defense 2** (only if needed, −20%) | — | — |

> Recompute exact dates once the school publishes the official academic calendar — this table assumes Week 1 = the calendar week containing Sep 7, 2026, with no holiday gaps.

## 3. TP1–TP6 → GitHub milestone mapping

Create one **GitHub Milestone** per sprint (2-week cadence, per the register's Scrum methodology), due-dated to the Friday closing each sprint. Because GitHub Milestones only carry a due date (no start date), put the sprint window in the milestone description, e.g. `Sprint 2 (Sep 21 – Oct 4) — TP1 close / TP2-TP3 ramp`.

| TP | Scope | Primary weeks | Suggested labels |
|---|---|---|---|
| **TP1** | SRS, UML state diagrams (Device 7-state, Incident 5-state), architecture doc, message-schema freeze, DB schema, RQ/experiment design, PoC serial parser | 1–3 | `module:docs`, `module:gateway-sync` |
| **TP2** | Gateway Bridge: LoRa-serial parser, SQLite P0–P3 queue, MQTT publish, reconnect/flush, dedup-at-gateway, health API | 2–6 | `module:gateway-sync` |
| **TP3** | NestJS auth/RBAC, device fleet FSM, rental lifecycle, idempotent ingestion endpoint, sync audit log, Postgres migrations | 3–7 | `module:auth`, `module:devices`, `module:rentals` |
| **TP4** | Telemetry ingestion, Leaflet map + WebSocket live updates, SOS→Incident pipeline, incident FSM, notifications | 5–9 | `module:monitoring`, `module:incidents` |
| **TP5** | Trip/booking, device reservation/assignment, check-out/in, rental agreements, billing, role-based web views | 6–10 | `module:trips`, `module:billing`, `module:frontend` |
| **TP6** | Physical LoRa experiments (RQ1/RQ2), RQ3 drills, dedup/concurrency test results, evaluation report, Docker Compose, CI/CD, final docs | 9–13 | `module:devops`, `module:docs` |

**Key gate**: TP1's message schema freeze is a hard dependency for TP2–TP5. Do not start Gateway or backend event-ingestion implementation before the schema is committed to `specs/gateway-sync/design.md`.

## 4. Review-readiness checklist per gate

- **Before Review 1 (Wk4)**: Charter + RQs finalized, `requirements.md` for at least Gateway-Sync and Incident modules written in EARS syntax, architecture diagram drafted, decisions in `03-decisions-and-risk-register.md` resolved (especially D-001 ORM choice — needed before any migration is written).
- **Before Review 2 (Wk8)**: Backend skeleton running (auth, devices, rentals), Gateway Bridge demoable against ≥1 physical device, architecture doc + ER diagram finalized, CI pipeline green.
- **Before Review 3 (Wk14)**: All TP1–TP6 deliverables complete, RQ1/RQ2/RQ3 experiment results written up, full regression suite green, deployment guide validated on a clean environment, defense slides drafted.

## 5. Parallel workstreams (concurrent PR/branch convention)

Per the team's GitLab experience, run concurrent feature branches/PRs across decoupled NestJS modules rather than serializing on one branch. Suggested default parallel lanes once TP1's schema is frozen:

- **Lane A** — Gateway Bridge (`module:gateway-sync`)
- **Lane B** — Backend core (auth/devices/rentals) (`module:auth`, `module:devices`, `module:rentals`)
- **Lane C** — Incidents + monitoring (`module:incidents`, `module:monitoring`) — depends on Lane B's device/trip models existing
- **Lane D** — Frontend (`module:frontend`) — consumes Lane B/C's OpenAPI contracts, can stub against `02-templates/04-api-endpoint-template.md` specs before backend is done

See [`01-conventions/07-github-workflow-git-conventions.md`](../01-conventions/07-github-workflow-git-conventions.md) for how these lanes map to branches, PRs, and required reviewers.
