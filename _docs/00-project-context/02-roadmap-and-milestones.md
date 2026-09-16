# TrekLink — Roadmap & Milestone Calendar

> **Rewritten Session 6 (2026-09-16) against the SEP490 Fall-2026 documents.** The previous version
> was derived from `SWP490_Lo-trinh-Capstone_v1.0.pdf` and described a different execution model —
> Review 1 as a Week 4–5 window, councils at Weeks 14 and 15, and delivery organised by TP package
> and Iteration. The course now issues SEP490 material that supersedes it on **timing and
> structure**. Do not rely on any copy of the old table. See **D-013**.
>
> **Authoritative sources**, in order:
> 1. `capstone/Documents/SEP490_Student_Project_Execution_Schedule.pdf` (50 pp) — the master
>    schedule, weekly Definition of Done, and anti-fail checks.
> 2. `capstone/Documents/SEP490_Huong_dan_nhanh_cho_sinh_vien.pdf` (6 pp) — the student summary.
> 3. `capstone/Documents/TrekLink-proposed-mainflow-ducndm.png` — **the supervisor's own Main Flow
>    set for this project** (D-016).
> 4. `capstone/Documents/templates/Cam-nang-tranh-loi-Capstone-SE.pdf` — the faculty fault-
>    prevention handbook. Its failure modes are graded criteria, not advice.
> 5. [`topics/Phieu_FA26SE159.md`](../../topics/Phieu_FA26SE159.md) — governs **content** (D-000).
>
> `SWP490_Lo-trinh-Capstone_v1.0.pdf` is retained deliberately: practices it describes that SEP490
> does not contradict remain in force — the phase discipline, the deliverable-ledger shape, and the
> **Week-6 scope lock** (§6), which SEP490 never mentions but which is real.

**Project code**: FA26SE159 · **Group code**: GFA26SE55 · **Supervisor**: Đặng Ngọc Minh Đức
**Term start**: Monday, Sep 7, 2026 · **Working plan ends**: Sunday, Dec 20, 2026 (Week 15)

> **On the "09/2026 – 03/2027" duration** printed on the registration form and in Report 1 §1.1:
> that span includes the **retake window**. A group that fails at either council sits a council in
> the following term, around March 2027. The figure is correct as registered. **Plan for December.**

---

## 1. The five things to know before reading anything else

1. **Three gates, and they are checkpoints rather than start lines.** Review 1 (W4), Review 2 (W8),
   Faculty Council (W13), then Final Submission & Defense (W15). The faculty guide opens with
   *"Review là điểm kiểm tra, không phải điểm bắt đầu"* — arriving at a gate having just started
   the work it assesses is the standard way to fail it.
2. **Delivery is organised by Main Flow, not by module or phase.** From W3 to W12 the project is
   built incrementally, one Main Flow at a time, each going Prototype/Figma → detailed spec →
   implement → test → demo. The five flows are fixed by the supervisor (§4). The **Mainflow
   Coverage Matrix** is the single instrument used to confirm progress at the weekly Group Meeting.
3. **The registration form still locks at the end of Week 6.** SEP490 does not mention a scope
   lock; the SWP490 roadmap does, and the team lead confirms it is real. Anything the form says
   that current decisions contradict must be amended before then — see §7.
4. **Everything produced must have evidence, and documents must match the software.** Commit,
   document, screenshot, test result, meeting minute. The faculty handbook's most common outcome is
   *"passed but must revise and resubmit documentation"* — the product ran and the paperwork pulled
   the mark down. The golden rule is *"có làm mới ghi, không làm đừng ghi"*: write only what was
   built, and be able to point at where each written claim is implemented or tested.
5. **Everything is in English**, following the SEP490 report templates.

---

## 2. Gate schedule

| Gate | Week | Focus | The questions the panel will ask |
|---|---|---|---|
| **Review 1 — Gate 1** | **W4** | Proposal & Requirement | What is the problem? Who uses it? How far does scope go? Are the requirements clear and verifiable? |
| **Review 2 — Gate 2** | **W8** | System & Design | How will the system be built? Is the design clear enough to code from? |
| **Faculty Council — Gate 3** | **W13** | Final Product Evaluation | What did the group build? How do you prove it runs? Which part did *you* do? |
| **Final Submission & Defense** | **W15** | Submission | Is the package complete, consistent, and installable on a clean machine? |
| Retake council | ~Mar 2027 | — | only if W13 or W15 fails |

**The dual-council naming.** "Hội đồng 1.1 / 1.2" is the *Hội đồng kín* terminology, conveyed
through the supervisor's outline and never published as an official document. It is **not** a
separate pair of events — it maps onto the table above: **Hội đồng 1.1 = Faculty Council (W13)**,
**Hội đồng 1.2 = Final Submission & Defense (W15)**. Use it in internal planning; cite only the
SEP490 names in graded documents and slides.

**Preparation loop.** Every gate is preceded by the same four-step cycle, run three times in the
term: Common Meeting → team self-check → Group Meeting → fix → readiness check → gate.

```
CM1 (W1)  -> self-check -> GM -> fix -> readiness -> (foundation for the term)
CM2 (W3)  -> self-check -> GM -> fix -> readiness -> REVIEW 1  (W4)
CM3 (W7)  -> self-check -> GM -> fix -> readiness -> REVIEW 2  (W8)
CM4 (W12) -> self-check -> Mock Council -> fix -> readiness -> COUNCIL (W13)
```

**Meetings.** Four **Common Meetings** (all groups together) at **W1, W3, W7, W12**. A **Group
Meeting** every week, ours on **Sunday**, time set by the supervisor. In a Common Meeting week the
Group Meeting follows the CM — it exists to handle this group's specific problems, not to repeat
what was just briefed to everyone.

**Feedback is closed-loop and tracked.** Every comment from any gate is recorded as
`Feedback → Required Action → Owner → Deadline → Evidence → Status`, in the Review Feedback
Tracker. Repeating a Review 1 mistake at Review 2 is named as a direct cause of failure, and a
comment the group chooses not to follow needs a stated, defensible reason — not silence.

---

## 3. Week-by-week calendar

Weeks run Mon–Sun from Sep 7, 2026. "Due" means end of that week unless stated.

| Wk | Dates 2026 | Common Mtg | Phase | Gate / event | **Deliverable due** |
|---|---|---|---|---|---|
| 1 | Sep 7–13 | **CM1** Kick-off & Working Guideline | Initiation | Group kick-off | Project Introduction · Initial Scope · Team Working Plan |
| 2 | Sep 14–20 | — | Planning | WBS / timeline / risk review | **PMP Draft · WBS · Feature Tree · Mainflow list · Gantt · Responsibility Matrix · Risk List** |
| 3 | Sep 21–27 | **CM2** Review 1 Clinic | Requirement + Foundation Design | SRS draft / UC / BR review | **SRS Draft · Architecture Diagram · ERD · Package Design · prioritised Mainflow list** · demo MF-01 |
| 4 | Sep 28–Oct 4 | — | Review 1 | **REVIEW 1 — GATE 1** | **Registration Form · PMP Draft · SRS Draft · Review 1 slides** |
| 5 | Oct 5–11 | — | System Design | Architecture + ERD approval | Figma/prototype per Main Flow · SDD update |
| 6 | Oct 12–18 | — | Detailed Design | Sequence/Class/Workflow approval · **SCOPE LOCK** | **Amended registration form — GVHD-confirmed, FROZEN** |
| 7 | Oct 19–25 | **CM3** Review 2 Clinic | Design Baseline | Baseline SRS/SDD, Test Plan, readiness | **MF-01 + MF-02 complete · MF-03 in progress · MF-04/05 have Figma + spec** |
| 8 | Oct 26–Nov 1 | — | Review 2 | **REVIEW 2 — GATE 2** | **PMP Updated · SRS Final · SDD Initial · Test Plan Draft · slides** · demo MF-01,02 |
| 9 | Nov 2–8 | — | Implementation I | Iteration 1 review | Product v0.1 · demo highest-priority Main Flow end-to-end |
| 10 | Nov 9–15 | — | Implementation II | Iteration 2 review | All Main Flows demoable · Coverage Matrix updated |
| 11 | Nov 16–22 | — | Implementation III | Iteration 3 review + readiness | **Feature complete · Product v0.9 / Release Candidate · Configuration Matrix updated · Report 5** |
| 12 | Nov 23–29 | **CM4** Council Readiness | Testing & Council Prep | **Mock Council** + buffer sprint | **STD / Test Results · Deployment Package · Demo Script** · 100 % Coverage Matrix |
| 13 | Nov 30–Dec 6 | — | Final Evaluation | **FACULTY COUNCIL — GATE 3** | **Final Product · PMP/SRS/SDD/STD · Software Package · Reports 1–5 · final slides** |
| 14 | Dec 7–13 | — | Finalization | Feedback closure + consistency audit | **User Guide · Installation Guide · Reports 6–7 · Final Project Package** |
| 15 | Dec 14–20 | — | Submission | **FINAL SUBMISSION & DEFENSE** | **Final Report · final slides · Software Package installable on a clean machine** |

> **Week↔date mapping** assumes Week 1 is the calendar week containing Sep 7, 2026, with no holiday
> gaps. No Vietnamese public holiday falls inside W1–W15. Exact gate dates, rooms and reviewer
> assignments are notified per group; this table fixes the windows.

### 3.1 Two contradictions inside the SEP490 source, and how we resolve them

Flagged rather than hidden, so nobody "corrects" this file back later.

| Contradiction | Resolution |
|---|---|
| Review 1 at **W4** (Roadmap table, Master Schedule 5.2, quick guide) vs **W3** (§4 prose item 2) | **W4** — two sources to one |
| "Two Main Flows complete at **W7**" (§4, Master Schedule 5.1) vs "Sprint 1 (**W8**) → MF-01, MF-02" (Sprint Plan) | Plan to the **stricter W7**; W8 is the confirmation demo |

### 3.2 Continuous obligations

Not one-off deliverables; checked at every gate.

- **Group Meeting every week** — all members attend. A member who misses reviews and contributes
  little **fails individually even if the group passes.**
- **Progress Log** (`GFA26SE55_Progress_Log.xlsx`) — updated **before every Group Meeting**,
  per-member and per-week, each entry tied to a named deliverable. This is the primary evidence for
  Individual Contribution and it starts at W1, not at the council. "Continued working on the
  project" is not an entry.
- **Mainflow Coverage Matrix** — the supervisor's progress instrument. Kept current weekly.
- **Review Feedback Tracker** — every gate comment carried to a closed status with evidence.
- **Evidence habit** — commits, documents, screenshots, test results, meeting minutes.

### 3.3 The weekly routine

`Plan → Execute → Team meeting → Evidence → Update Progress Log & report to GVHD → Weekly close`,
closing each week as DONE / IN PROGRESS / BLOCKED / NEXT WEEK. Anything that misses its Definition
of Done carries into the next Group Meeting rather than quietly disappearing.

Our own cadence, inside that frame: asynchronous daily report via GitHub Issues; online team
meetings **Monday** and **Thursday**; offline meeting **Sunday**; an offline retrospective and
review at each two-week sprint boundary.

---

## 4. The five Main Flows

Fixed by the supervisor — see **D-016** and `Documents/TrekLink-proposed-mainflow-ducndm.png`.
These are the units the Coverage Matrix tracks, the units demoed at each Iteration review, and the
units the council evaluates.

| MF | Name | Substance | Owner | Backlog epics |
|---|---|---|---|---|
| **MF-01** | Booking → Rental → Trip Preparation | Customer browses package, submits booking, reserves device → Staff reviews, confirms, allocates device, assigns guide, generates rental agreement, checks out → Guide receives device and prepares | **TanNB** | E3, E2, E1 |
| **MF-02** | Field Data → Offline Gateway → Cloud Sync | Device SOS/GPS/telemetry over LoRa mesh → Gateway Bridge with SQLite priority queue while offline → MQTT → NestJS; P0–P3 with idempotency; priority-ordered flush on reconnect | **KhoaDD** | E4 |
| **MF-03** | SOS → Incident → Emergency Response | SOS broadcast → gateway → idempotency check on `eventId` → Incident created if absent → FSM Detected → Acknowledged → In Progress → Resolved → Closed with actor/timestamp/note on every transition → WebSocket to Staff and Guide | **HoangTK** | E5 |
| **MF-04** | Real-Time Trip Monitoring | Device → gateway → MQTT → backend → WebSocket → dashboard: active trips, positions, battery, incident alerts, last-seen. Admin / Staff / Guide | **LongNN** | E5 (frontend) |
| **MF-05** | Return → Inspection → Billing → Maintenance | Check-in, return inspection, charge calculation, payment, rental close; device FSM Available → Reserved → Rented → In-Field → Returned → Maintenance → Retired | **LongLP** | E6, E2 |

**E7 (DevOps/CI-CD) and E8 (Research & Experimental Evaluation) are cross-cutting and deliberately
are not Main Flows.** State this wherever the Coverage Matrix is presented, so their absence does
not read as an oversight.

### 4.1 How a Main Flow is built

Each one goes through the full cycle; the system is **not** designed end-to-end before coding
starts. Architecture, the foundational ERD and the technology decisions are made **once** at W3 and
serve every flow.

```
Prototype / Figma
  -> detailed functional spec  (input, output, validation, business rule, happy + unhappy path)
  -> sequence + class diagram, state diagram for anything with a lifecycle
  -> API / interface spec      (endpoint, request/response, DB or third-party call)
  -> implement
  -> test
  -> demo
```

A flow whose design finishes first may be implemented first, in parallel with the design of the
others. No flow enters implementation (W9–W11) without Figma **and** a detailed spec.

**Traceability must hold in both directions**: Main Flow → Use Case → Sequence → Class/Service →
Database → Code. A reviewer will pick a requirement and walk it to the implementation, or pick a
diagram component and ask which code it is.

### 4.2 Sprint plan

Sprint boundaries align to gates, never to a fixed drumbeat.

| Sprint | Weeks | Closes on | Carries |
|---|---|---|---|
| 1 | 1–3 | Review 1 readiness (W3) | Requirements, architecture + ERD foundation, MF-01 first cycle |
| 2 | 4–6 | **Scope lock (W6)** | Review 1 feedback closure, MF-01/MF-02 design, **form amendments** |
| 3 | 7–8 | **Review 2 (W8)** | MF-01 + MF-02 complete; MF-03 in progress; MF-04/05 spec'd; Test Plan |
| 4 | 9–10 | Iteration reviews | MF-03, MF-04 implemented — Product v0.1 |
| 5 | 11 | Feature complete (W11) | MF-05 + full-system integration — Release Candidate |
| 6 | 12 | **Mock Council (W12)** | Buffer for anything outstanding, system testing, regression, deployment, demo rehearsal |
| 7 | 13–15 | Councils | Council, feedback closure, user/installation guides, final report, defence |

The W12 buffer is a **safety net, not the plan**. The target is every Main Flow finished by the end
of W11. The council expects all Main Flows working plus at least 80 % of use cases.

---

## 5. Deliverable ledger and ownership

| Deliverable | Planned | Owner | Reviewer | Status |
|---|---|---|---|---|
| Report 1 — Project Introduction | W1 → W4 | KhoaDD | TanNB | Draft complete |
| **Report 2 — Project Management Plan (PMP)** | **W2 draft → W4 → updated W8** | **KhoaDD** | LongLP | In progress |
| **Report 3 — Software Requirement Specification (SRS)** | **W3 draft → W4 → final W8** | **TanNB** | KhoaDD | Not started |
| Report 4 — Software Design Document (SDD) | W3 draft → W8 initial → W13 final | KhoaDD + HoangTK | LongLP | Not started |
| Report 5 — Test Plan → STD & Test Results | W7 plan → W11 → W12 complete | TanNB | HoangTK | Not started |
| Report 6 — User Guide | W14 | LongNN | TanNB | Not started |
| Report 7 — Final Project Report | W15 | KhoaDD | all | Not started |
| **Installation Guide** | W14 | LongLP | KhoaDD | Not started |
| Software Package (v0.1 / v0.9 / final) | W9 / W11 / W13 | whole team | — | Not started |
| Presentation / slides | W4, W8, W13, W15 | KhoaDD | all | Not started |
| Progress Log | weekly from W1 | KhoaDD | all | To create |
| Mainflow Coverage Matrix | weekly from W3 | KhoaDD | supervisor | To create |

**Report 3 is split across two deadlines.** W4 needs the draft — Product Overview, User
Requirements, System Functional Overview, Context Diagram, Actors, Use Cases, initial Business
Rules, Exception Scenarios. The full EARS SRS is W8. Write the W4 draft so the W8 version grows out
of it rather than replacing it.

**Two UML State Machine Diagrams are named, graded deliverables** (register §f): Device Lifecycle
(7 states) and Incident Lifecycle (5 states). They belong in Report 4 and in
`specs/devices/design.md` / `specs/incidents/design.md`, and they are visible in MF-03 and MF-05.

### 5.1 Module lanes

Assigned against the enrolment framework codes. `BIT_SE_NJS_18D` is the Node.js track and is
treated as covering NestJS; backend capability is **3 of 5**, not 1 of 5 as previously recorded.

| Member | Track | Lane | Main Flow |
|---|---|---|---|
| **KhoaDD** — leader | IC 19A | Prisma schema, `devices`, firmware, `gateway-sync`, UI layout, architecture | MF-02 owner, MF-05 support |
| **LongLP** — delegate | **NJS** 18D | `auth`, `rentals`, `billing` | MF-05 owner, MF-01 support |
| **HoangTK** | **NJS** 18D | `incidents`, `monitoring` ingestion, WebSocket | MF-03 owner, MF-04 backend |
| **LongNN** | IC 19A | `frontend` (FSD), map and monitoring UI | MF-04 owner |
| **TanNB** — delegate | IC 18D | `trips`, booking, QA and test lead; secondary Meshtastic knowledge | MF-01 owner |

Lanes run as concurrent branches across decoupled NestJS modules rather than serialising on one
branch. Ramp-up for the two IC-track members on
[`01-conventions/05-backend-conventions.md`](../01-conventions/05-backend-conventions.md) during
W2–W5 is budgeted work, not slack, and is a tracked risk in the register.

---

## 6. ⚠️ The Week-6 scope lock

SEP490 does not mention it; the SWP490 roadmap does, and it is real (D-013). After the end of W6
the registration form is frozen, and the Faculty Council grades the product against that frozen
form. Note there are now **two** baselines and they are not the same: the **requirement** baseline
is set at Review 1 (W4), the **form** freeze at W6.

### 6.1 Supervisor questions — all closed

| # | Question | Decision | Outcome |
|---|---|---|---|
| 1 | Keep Stage B (the basecamp bridge) or drop it? | **D-005** | **Keep — permanently.** It is the substance of MF-02. Offline NFRs and RQ1/RQ2 stay binding |
| 2 | Do firmware commits earn graded credit? | **D-008 Q3** | **Yes** — with the caveat that code volume alone is not what is assessed |
| 3 | Are targeted firmware fixes read as out-of-scope "firmware redesign"? | **D-008 Q2** | **No** — firmware enhancement and integration are in scope; only a mesh-stack rearchitecture is excluded |

The supervisor's position as given on 2026-09-13: the team may change tech stack, flows and scope
as it judges best, then pitch and defend the result at the next meeting. His own outline is
guidance, not a restriction. **Nothing is blocked on him.** What remains is our own obligation to
put the amended form in front of him before W6.

### 6.2 Register text to amend in the Week-6 update

The submitted form contains statements later work proved wrong. Each must be amended, or the
product will diverge from the document it is graded against.

| Register says | Reality | Source |
|---|---|---|
| "Apply PostgreSQL migrations via **TypeORM**" (§e) | Prisma, locked as team mandate | **D-001** |
| `eventId = Device ID + Session ID + Sequence Number` (§b, §c) | Neither field exists in firmware; key is `sha256(nodeNum:packetId)` plus open-Incident correlation | **D-006**, [`04-firmware-ground-truth.md`](04-firmware-ground-truth.md) §3 |
| Firmware "version-locked to Summer 2026 release" (§b) | Editable, credited, and in scope for enhancement | **D-008** |
| Gateway is dedicated hardware with its own uplink (§b) | Staged: Stage A = node's own MQTT; Stage B = basecamp bridge. Both in scope | **D-005**, **D-016** |
| Frontend map library | Leaflet replaced by **MapLibre GL + Goong Maps**; OSM tiles are unlawful to publish in Vietnam | **D-012** |
| — | v1 hardware compiles MQTT out and is **out of the demo set** | **D-005**, ground truth §5 |

> The `eventId` amendment matters most. The register makes it a **named scientific contribution**
> (§3.3d, "a formally defined eventId scheme") and the duplicate-prevention NFR is written in terms
> of it. Changing the formula silently and presenting a different one at defence is exactly what the
> council exists to catch. Amend the wording to the constructible form and keep the intent.

---

## 7. Gate readiness checklists

### Before Review 1 (W4)

- [ ] Problem, target users, objective and scope stated clearly
- [ ] **Context Diagram**, Actors, Use Case Diagram complete
- [ ] FR and NFR written at a verifiable level — no "Admin manages everything"
- [ ] **Feature Tree** complete
- [ ] **Business Rule Matrix** first version — `BR ID | Business Rule | Requirement | Implementation | Test Case`
- [ ] At least one **exception scenario per Main Flow**
- [ ] Main Flow list identified and prioritised, presented as activity/swimlane diagrams
- [ ] Registration Form, PMP Draft, SRS Draft submitted; slides consistent with the SRS
- [ ] Use cases are functions, not workflows; `include` / `extend` / generalization used correctly
- [ ] Every decision-register item either resolved or explicitly tabled

### Before Review 2 (W8)

- [ ] SRS Final, SDD Initial, Test Plan Draft
- [ ] Architecture, ERD with PK / FK / relationships / cardinality, Package Design
- [ ] State / Sequence / Class diagrams for the main data objects
- [ ] Traceable Use Case → Design → Class/Service → Database
- [ ] Working prototype or workflow demo; **MF-01 and MF-02 demoed**
- [ ] Business parameters configurable, not hardcoded (**D-015**)
- [ ] Entity and attribute names consistent between ERD, SRS and code
- [ ] Every architecture and technology choice has a stated reason
- [ ] No component drawn that the team does not intend to implement
- [ ] Review 1 feedback closed with evidence

### Before the Faculty Council (W13)

- [ ] **Every Main Flow runs end-to-end**; ≥ 80 % of use cases working
- [ ] Coverage Matrix 100 % Implemented / Tested / Demo Ready
- [ ] Each important FR has at least one test case with evidence
- [ ] Product deploys outside a developer machine; demo data ready and realistic
- [ ] Demo rehearsed at least twice, with a backup video of each Main Flow
- [ ] Business parameters demonstrably configurable — expect to be asked live
- [ ] Documentation matches the software that will be demoed
- [ ] RQ1 / RQ2 / RQ3 results written up
- [ ] Every member can answer: *"what did you do, and where is it in the code?"*
- [ ] Review 1 and Review 2 feedback closed with evidence, tracker in hand

### Before Final Submission (W15)

- [ ] Package complete and internally consistent; no template placeholders left
- [ ] Software Package installs on a clean machine
- [ ] User Guide and Installation Guide complete
- [ ] Every member can answer questions about the **whole** system, not only their own part
- [ ] Submitted build is the build that was demoed

---

## 8. Known failure modes to design against

From the faculty fault-prevention handbook. These are graded criteria.

**The six causes of not passing**, in order of frequency: a Main Flow that breaks during the demo
or cannot be shown in the allotted time · hardcoded business parameters · documentation that is
wrong, incomplete, or not on the official template · business logic detached from reality with no
exception handling · Review feedback not acted on · not being approved to defend, or a member who
contributed too little.

**Specific to this project:**

- **Demo failure is the single most common cause of failure.** Rehearse twice, keep a backup video,
  keep an IDE open on the repository, use short demo passwords, never build a special "demo
  version", and if something breaks, stop and explain the fault rather than skimming past it.
- **Hardcoding** — see **D-015**. The first question in the handbook's most-asked list is *"can this
  number be changed? show me now."*
- **The word "Smart" in our registered title.** The handbook devotes a section to projects whose
  name promises AI and whose demo is CRUD, and says plainly that a rule-based system must be called
  rule-based. TrekLink has no ML component. The honest answer — rehearsed, and known by every
  member — is that the intelligence is **device-level autonomy**: IMU fall detection, autonomous SOS
  broadcast, multi-hop mesh routing, priority-ordered store-and-forward. Never write "AI" for the
  platform in a graded document or slide.
- **AI-written documentation and fabricated test results** are called out as a fast-growing and
  serious failure. Every NFR and business rule must point at the code or test that implements it.
  Graded documents describe the work as **AI-assisted development with mandatory human review**.
- **Data, security and legal** — collect only what is used; no secrets in source; cite third-party
  data sources; keep a short Legal & Compliance section. The map-provider migration (**D-012**) sits
  here and is a legal obligation, not a preference.
- **Individual contribution** — commits and weekly minutes are the evidence. A repository where one
  or two people committed everything cannot demonstrate who did what.

---

## Appendix A — TP1–TP6 (historical, no longer the planning unit)

The register (§g) organises work into six task packages. SEP490 organises delivery by Main Flow, and
**the Main Flow model governs** (D-013). This table is retained so register cross-references resolve,
and is mapped onto the current plan.

| TP | Register scope | Now carried by |
|---|---|---|
| **TP1** | SRS, 2 UML state machines, architecture doc, inherited-component analysis, DB schema, RQ/experiment protocol, PoC parser | W2–W3 foundation work + Report 3/4 |
| **TP2** | Gateway Bridge: serial parser, SQLite P0–P3 queue, MQTT publish, reconnect/flush, gateway dedup, health API | **MF-02** |
| **TP3** | NestJS auth/RBAC, device fleet FSM, rental lifecycle, idempotent ingestion, sync audit log, migrations | **MF-01**, **MF-02**, **MF-05** |
| **TP4** | Telemetry ingestion, live map + WebSocket, SOS→Incident pipeline, incident FSM, notifications | **MF-03**, **MF-04** |
| **TP5** | Trip/booking, reservation/assignment, check-out/in, agreements, billing, role-based views | **MF-01**, **MF-05** |
| **TP6** | LoRa experiments (RQ1/RQ2), RQ3 drills, dedup/concurrency results, evaluation report, Docker Compose, CI/CD, final docs | **E7 + E8**, cross-cutting; W11–W13 |

The one TP-era constraint that survives unchanged: **the message-schema freeze is a hard dependency
for everything downstream.** Do not start Gateway or ingestion implementation before the schema is
committed to `specs/gateway-sync/design.md`.

## Appendix B — Superseded framings

Do not reintroduce these; they appear in older documents and in the SWP490 roadmap.

| Superseded | Replaced by |
|---|---|
| Review 1 as a "Weeks 4–5 window with a Week-3 dossier" | Review 1 = **W4** |
| Review 2 as "Weeks 8–9 with a Week-7 dossier" | Review 2 = **W8** |
| Hội đồng 1.1 at W14 and 1.2 at W15 as separate extra events | **W13 Faculty Council** and **W15 Final Submission & Defense** |
| Iteration 1 / 2 / 3 completing at W7 / W11 / W13 | Iteration reviews at **W9 / W10 / W11**, feature complete W11 |
| Seven sprints on a fixed two-week drumbeat | The gate-aligned sprint plan in §4.2 |
| "NestJS is a skill only for Khoa" | **3 of 5** — see §5.1 |
| Leaflet.js as the map library | **MapLibre GL + Goong Maps** (D-012) |
