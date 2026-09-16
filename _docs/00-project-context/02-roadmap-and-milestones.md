# TrekLink — Roadmap & Milestone Calendar

> **Rewritten Session 4 against the official schedule.** The previous version of this file was
> derived from the capstone register alone and **understated every deadline** — it placed
> Review 1 at Week 4 (actually a Week 4–5 window whose dossier is due end of Week 3), had no
> Week-6 scope lock, and did not mention Reports 1–7 at all. Do not rely on any copy of the old
> table.
>
> **Authoritative source**: `capstone/Documents/SWP490_Lo-trinh-Capstone_v1.0.pdf`
> ("Lộ trình thực hiện đồ án Capstone trong học kỳ", v1.0, issued 09/2026), cross-read with
> [`topics/Phieu_FA26SE159.md`](../../topics/Phieu_FA26SE159.md) (Tier 1 per D-000).
> Where the school's roadmap and the register disagree on timing, **the school's roadmap wins** —
> it governs submission, the register governs content.

**Term start**: Monday, Sep 7, 2026 · **Term span**: 09/2026–03/2027 · **Supervisor**: Đặng Ngọc Minh Đức

---

## 1. The three things to know before reading anything else

1. **Reports 1–7 are the graded artifacts, not the engineering docs.** The council reads
   Report 1–7, the registration form, and the review minutes. "SRS" is **Report 3**; "SDD" is
   **Report 4**; the test plan is **Report 5**. Charter §7's deliverables list is organised by
   engineering artifact and does not map 1:1 — §4 below is the reconciliation.
2. **The registration form locks at the end of Week 6.** After that, scope cannot change, and
   Hội đồng 1.1 in Week 14 grades the product *against that frozen form*. Every open scope
   question must be settled before then — see §6.
3. **Everything is in English.** Roadmap §06 rule 5: all documentation and the council
   presentation use English, following the course's Report 1–7 templates.

---

## 2. Official milestone schedule

| Milestone | Window | Dossier deadline | Who | Output |
|---|---|---|---|---|
| Topic registration | start of term | — | team + GVHD | assigned GVHD + 2 reviewers |
| Work with GVHD | Weeks 1–3 | see §3 | GVHD | Reports 1–3 (overview), Project Tracking |
| **Review 1 — feasibility** | **Weeks 4–5** | **end of Week 3** | 2 reviewers (not GVHD) | minutes + *keep scope* / *adjust scope* |
| **Registration form update** | — | **end of Week 6** | team + GVHD confirms | **form frozen — no scope change after this** |
| **Review 2 — SRS / design / features** | **Weeks 8–9** | **end of Week 7** | same 2 reviewers | minutes + **mandatory feature list** |
| Development & testing | Weeks 10–13 | — | GVHD weekly only | Iterations 2–3 |
| **Hội đồng 1.1 — defence eligibility** | **Week 14** | **end of Week 13** | 3-member council | *pass* → 1.2 · *fail* → HĐ2 |
| **Hội đồng 1.2 — official defence** | **Week 15** | ≥2 working days prior | council | *pass* → Capstone complete |
| Hội đồng 2 — retake | ~Week 19 (next term) | ≥2 working days prior | council | only if 1.1 or 1.2 failed |

**Submission rule** (roadmap §06.1): dossiers are due **≥2 working days** before any
Review/Council session. For Review 1, Review 2 and Hội đồng 1.1 the deadline is the **end of the
week immediately preceding** the assessment window, so every team gets equal preparation time.
That is why Review 1's dossier is due end of Week 3 even if your slot falls in Week 5.

**Review 2 produces the contract.** The "mandatory feature list" (*danh sách tính năng bắt buộc*)
agreed at Review 2 — bounded by the already-frozen registration form — is the specific thing
Hội đồng 1.1 checks the product against. Treat Review 2 as scope *ratification*, not feedback.

---

## 3. Week-by-week calendar and deliverable ledger

Weeks run Mon–Sun from Sep 7, 2026. "Due" means end of that week unless stated.

| Wk | Dates (2026) | Milestone | **Deliverable due** | TP active | Iteration |
|---|---|---|---|---|---|
| 1 | Sep 7 – Sep 13 | kickoff with GVHD | **Report 1 — Project Introduction** | TP1 | — |
| 2 | Sep 14 – Sep 20 | project planning | **Report 2 — Project Management Plan + Project Schedule** | TP1, TP2 | — |
| 3 | Sep 21 – Sep 27 | requirements overview | **Report 3 (overview part)** + **Project Tracking** · **Review 1 dossier** | TP1 close, TP2, TP3 | — |
| 4 | Sep 28 – Oct 4 | **Review 1** window opens | — | TP2, TP3 | — |
| 5 | Oct 5 – Oct 11 | **Review 1** window closes | Review 1 minutes received | TP2 close, TP3, TP4 | — |
| 6 | Oct 12 – Oct 18 | **scope lock** | **Updated registration form — GVHD-confirmed. FROZEN.** | TP3, TP4 | — |
| 7 | Oct 19 – Oct 25 | Review 2 prep | **Report 3 (full SRS)**, **Report 4 (SDD)**, **Report 5 (test plan)**, **Software Package 1** · **Review 2 dossier** | TP3 close, TP4, TP5 | **Iteration 1 complete** |
| 8 | Oct 26 – Nov 1 | **Review 2** window opens | — | TP4, TP5 | — |
| 9 | Nov 2 – Nov 8 | **Review 2** window closes | Review 2 minutes + **mandatory feature list** | TP4 close, TP5, TP6 | — |
| 10 | Nov 9 – Nov 15 | build | — | TP5 close, TP6 | Iteration 2 |
| 11 | Nov 16 – Nov 22 | build | **Software Package 2** + updated Reports 3, 4, 5 | TP6 | **Iteration 2 complete** |
| 12 | Nov 23 – Nov 29 | build + system test | — | TP6 | Iteration 3 |
| 13 | Nov 30 – Dec 6 | freeze | **Full Software Package**, system test, **Report 5 complete** (test cases, test report, defect list), **Report 6 draft — User Guides** · **HĐ 1.1 dossier** | TP6 close | **Iteration 3 complete** |
| 14 | Dec 7 – Dec 13 | **Hội đồng 1.1** | Reports 1–6, working demo, frozen form, Review 1+2 minutes | — | — |
| 15 | Dec 14 – Dec 20 | **Hội đồng 1.2 — defence** | **Report 7 — Final Project Report**, slides, final package (≥2 working days prior) | — | — |
| 16–18 | Dec 21 – Jan 10 | post-defence fixes (if needed) | — | — | — |
| 19 | ~Jan 11 – 17, 2027 | **Hội đồng 2** (only if failed) | updated package + **per-comment response table** | — | — |

> Week↔date mapping assumes Week 1 is the calendar week containing Sep 7, 2026, with no holiday
> gaps. Recompute once the school publishes the official academic calendar. **Exact session
> dates, rooms, and reviewer assignments are notified per-group** — the roadmap only fixes the
> windows.

### 3.1 Continuous obligations (roadmap §06.3–4)

These are not one-off deliverables and are checked at every gate:

- **Weekly GVHD meeting** — *all* members attend, and at Review 1, Review 2, and every council session.
- **Project Weekly Report** — submitted to GVHD each week.
- **Project Tracking** — WBS, Issues, Defects, Q&A — maintained live and shared with GVHD.
- **Project Schedule** — maintained live (first submitted with Report 2 in Week 2).
- **Minutes** — every Review/Council produces minutes; keep them and respond to each comment at the next gate.

---

## 4. Report 1–7 ↔ engineering artifact map

The course numbers its reports; this repo organises by engineering artifact. This table is the
join. **Owner is unassigned** — set it at Sprint 1 planning against the skill matrix in
[`01-project-charter.md`](01-project-charter.md).

| Report | Course title | First due | Fed by | Owner |
|---|---|---|---|---|
| **1** | Project Introduction | **Wk 1** | charter §§1–4, register §a/§3.3a | TBD |
| **2** | Project Management Plan + Project Schedule | Wk 2 | this file, `03-backlog/`, charter team matrix | TBD |
| **3** | Software Requirement Specification (SRS) | Wk 3 overview → **Wk 7 full** → updated Wk 11 | register §c/§d, `specs/{module}/requirements.md`, `03-backlog/02-user-stories.md` | TBD |
| **4** | Software Design Document (SDD) — architecture, detailed design, database | **Wk 7** → updated Wk 11 | `01-conventions/04-architecture-conventions.md`, `specs/{module}/design.md`, `backend/prisma/schema.prisma`, the 2 UML state machines | TBD |
| **5** | Test plan → full test documentation | Wk 7 plan → **Wk 13 complete** | `specs/{module}/tasks.md` test phases, RQ1–RQ3 experiment protocol (register §3.3c) | TBD |
| **6** | User Guides | Wk 13 draft → Wk 14 | frontend role-based views | TBD |
| **7** | Final Project Report | **Wk 15** | everything + evaluation report | TBD |
| — | Software Package 1 / 2 / Full | Wk 7 / Wk 11 / Wk 13 | `treklink-web` source + DB script | whole team |

**Report 3 is split across two deadlines.** Week 3 needs only the *overview* portion — Product
Overview, User Requirements, System Functional Overview. The full EARS SRS is Week 7. Write the
Week-3 overview so the Week-7 SRS grows out of it rather than replacing it.

**Two UML State Machine Diagrams are named, graded deliverables** (register §f): Device Lifecycle
(7 states) and Incident Lifecycle (5 states). They belong in Report 4 and in
`specs/devices/design.md` / `specs/incidents/design.md`.

---

## 5. TP1–TP6 ↔ Iteration ↔ Sprint reconciliation

Three schedules exist and they are not the same thing:

| Scheme | Origin | Status |
|---|---|---|
| **Iteration 1 / 2 / 3** | school roadmap | **binding** — submission gates at Wks 7, 11, 13 |
| **TP1–TP6** | register §g | binding on *content* — what the council expects to exist |
| **Sprints** | team's own Scrum cadence | internal only — must not straddle an Iteration gate |

**Rule: sprint boundaries align to Iteration gates, not to a fixed 2-week drumbeat.**
A sprint that ends Week 8 is useless when Iteration 1 was due end of Week 7.

| Sprint | Weeks | Closes on | Carries |
|---|---|---|---|
| 1 | 1–3 | Review 1 dossier (Wk 3) | TP1 — SRS overview, architecture draft, schema freeze, PoC parser |
| 2 | 4–6 | scope lock (Wk 6) | TP2 ramp, TP3 start, **form amendments** |
| 3 | 7 | **Iteration 1** (Wk 7) | SRS + SDD + test plan + Software Package 1 |
| 4 | 8–9 | Review 2 (Wk 9) | TP4 start; absorb Review 2 minutes |
| 5 | 10–11 | **Iteration 2** (Wk 11) | TP5, Software Package 2, doc refresh |
| 6 | 12–13 | **Iteration 3** (Wk 13) | TP6 experiments, system test, full package |
| 7 | 14–15 | councils | demo, Report 7, slides |

### 5.1 TP scope (register §g, unchanged)

| TP | Scope | Weeks | Labels |
|---|---|---|---|
| **TP1** | SRS, 2 UML state machines, architecture doc, inherited-component analysis (firmware schema + eventId), DB schema, RQ/experiment protocol, PoC serial parser | 1–3 | `module:docs`, `module:gateway-sync` |
| **TP2** | Gateway Bridge: serial parser, SQLite P0–P3 queue, MQTT publish, reconnect/flush, gateway-side dedup, health API | 2–6 | `module:gateway-sync` |
| **TP3** | NestJS auth/RBAC, device fleet FSM, rental lifecycle, idempotent ingestion, sync audit log, Postgres migrations | 3–7 | `module:auth`, `module:devices`, `module:rentals` |
| **TP4** | Telemetry ingestion, Leaflet map + WebSocket, SOS→Incident pipeline, incident FSM, notifications | 5–9 | `module:monitoring`, `module:incidents` |
| **TP5** | Trip/booking, reservation/assignment, check-out/in, agreements, billing, role-based views | 6–10 | `module:trips`, `module:billing`, `module:frontend` |
| **TP6** | Physical LoRa experiments (RQ1/RQ2), RQ3 drills, dedup/concurrency results, evaluation report, Docker Compose, CI/CD, final docs | 9–13 | `module:devops`, `module:docs` |

**Key gate, unchanged**: TP1's message-schema freeze is a hard dependency for TP2–TP5. Do not
start Gateway or ingestion implementation before the schema is committed to
`specs/gateway-sync/design.md`.

**Risk carried from the register**: TP1 Week 2 must deliver a PoC gateway→backend integration —
the register explicitly refuses to defer NestJS + MQTT + WebSocket integration to TP3.

---

## 6. ⚠️ The Week-6 scope lock — what must be settled before it

After Week 6 the registration form is frozen and Hội đồng 1.1 grades against it. Two categories
of work are therefore **deadlined to Week 6**, not merely "open".

### 6.1 Open decisions needing a supervisor answer

Raise these at a weekly GVHD meeting or at Review 1. See
[`03-decisions-and-risk-register.md`](03-decisions-and-risk-register.md).

| # | Question | Decision | If unanswered by Wk 6 |
|---|---|---|---|
| 1 | Keep Stage B (basecamp bridge) or drop it? | **D-005** | Defaults to *keep* — the form's offline NFRs and RQ1/RQ2 stay binding and must be delivered. Dropping Stage B **after** Wk 6 means failing the frozen form. |
| 2 | Do firmware commits earn graded credit? | **D-008 Q3** | Register §4 already says effort reporting, source statistics, and test coverage **exclude** the inherited firmware. Treat as answered *no* unless the supervisor says otherwise; budget sprint capacity accordingly. |
| 3 | Are targeted firmware fixes read as the out-of-scope "firmware redesign"? | **D-008 Q2** | Charter §2 / register §3.3c list "firmware redesign" as out of scope. A surgical reliability fix is not a redesign — but get it on the record before Wk 6. |

### 6.2 Register text that current decisions contradict

The submitted form contains statements later work proved wrong. Each must be **amended in the
Week-6 update** or the product will diverge from the document it is graded against.

| Register says | Reality | Source |
|---|---|---|
| "Apply PostgreSQL migrations via **TypeORM**" (§e Practical) | Prisma, locked as team mandate | **D-001** |
| `eventId = Device ID + Session ID + Sequence Number` (§b, §c) | Neither field exists in firmware; key is `sha256(nodeNum:packetId)` + open-Incident correlation | **D-006**, [`04-firmware-ground-truth.md`](04-firmware-ground-truth.md) §3 |
| Firmware "version-locked to Summer 2026 release" (§b) | Editable; team owns the repo and can reflash | **D-008** |
| Gateway is dedicated hardware with its own uplink (§b) | Staged: Stage A = node's own MQTT; Stage B = basecamp bridge | **D-005** |
| — | v1 hardware compiles MQTT out and is **out of the demo set** | **D-005**, ground truth §5 |

> The `eventId` amendment is the one that matters most. The register makes it a **named
> scientific contribution** (§3.3d: "a formally defined eventId scheme") and the duplicate-
> prevention NFR is written in terms of it. Changing the formula silently, then presenting a
> different one at defence, is the kind of gap Hội đồng 1.1 exists to catch. Amend the wording
> to the constructible form and keep the intent.

---

## 7. Review-readiness checklists

**Before the Review 1 dossier (end of Wk 3)** — judged on feasibility, requirement clarity, and
whether scope is too wide or too narrow for a capstone:
- [ ] Report 1, Report 2 + Project Schedule submitted and GVHD-reviewed
- [ ] Report 3 overview: Product Overview, User Requirements, System Functional Overview
- [ ] Project Tracking live (WBS, Issues, Defects, Q&A)
- [ ] `requirements.md` in EARS for at least `gateway-sync` and `incidents`
- [ ] Architecture diagram drafted; RQ1–RQ3 experiment protocol restated
- [ ] Every `OPEN` item in the decisions register either resolved or explicitly tabled for Review 1
- [ ] §6.1 questions written down as questions to *ask*, not assumptions to carry

**Before the Review 2 dossier (end of Wk 7)**:
- [ ] Report 3 full SRS — every register §c FR traced to an EARS criterion and a module spec
- [ ] Report 4 SDD — architecture, detailed design, DB schema, **both UML state machines**
- [ ] Report 5 test plan
- [ ] **Software Package 1**: Iteration 1 code + DB script, running. Backend skeleton (auth, devices, rentals) up; Gateway demoable against ≥1 physical device; CI green
- [ ] Reports 1–2 and Project Tracking refreshed
- [ ] Registration form (frozen Wk 6) attached

**Before the Hội đồng 1.1 dossier (end of Wk 13)**:
- [ ] Full Software Package + working demo
- [ ] Reports 1–6 complete; Report 5 with test cases, test report, defect list
- [ ] RQ1/RQ2/RQ3 results written up
- [ ] Product demonstrably covers the frozen form **and** the Review 2 mandatory feature list
- [ ] SRS and Design consistent with what actually shipped — the council checks this explicitly
- [ ] Deployment guide validated on a clean environment; defence slides drafted

---

## 8. Parallel workstreams

Per the team's GitLab experience, run concurrent feature branches across decoupled NestJS
modules rather than serialising on one branch. Lanes, once TP1's schema is frozen:

- **Lane A** — Gateway Bridge (`module:gateway-sync`)
- **Lane B** — Backend core (`module:auth`, `module:devices`, `module:rentals`)
- **Lane C** — Incidents + monitoring (`module:incidents`, `module:monitoring`) — needs Lane B's device/trip models
- **Lane D** — Frontend (`module:frontend`) — consumes Lane B/C OpenAPI contracts; can stub against `02-templates/04-api-endpoint-template.md`

> **Capacity note**: NestJS is listed as a skill only for Khoa (charter skill matrix). Lanes B
> and C are the exposure. Sprint 1–2 pairing on
> [`01-conventions/05-backend-conventions.md`](../01-conventions/05-backend-conventions.md) is
> budgeted work, not slack — it is a tracked risk in the register.

GitHub Milestones carry only a due date, so put the window in the description:
`Sprint 3 (Wk 7) — Iteration 1: SRS + SDD + Software Package 1`. Branch/PR mechanics:
[`01-conventions/07-github-workflow-git-conventions.md`](../01-conventions/07-github-workflow-git-conventions.md).
