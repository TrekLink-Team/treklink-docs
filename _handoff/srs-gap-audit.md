# SRS Gap Audit: `Report3_SRS_DRAFT.md` against the template, the SSOT and the gates

Task A of the cloud session brief. Input: `Documents/reports/Report3_SRS_DRAFT.md` from the context
pack built 2026-09-25 (capstone@cecdae7). The as-built `.docx` (`extracted/Report3_SRS_TrekLink_asbuilt.md`)
carries the same content, so every row below applies to both.

Sources compared:

| Code | Source |
|---|---|
| **TPL** | `extracted/Report3_SRS_TEMPLATE.md`, the official SRS template |
| **MF** | `_docs/00-project-context/05-main-flows.md` (D-016) |
| **RF** | `_docs/00-project-context/06-requirements-foundation.md` |
| **CA** | `_docs/00-project-context/07-clarification-answers.md` (question numbers are `CA-Qn`) |
| **FGT** | `_docs/00-project-context/04-firmware-ground-truth.md` |
| **REG** | `_docs/00-project-context/03-decisions-and-risk-register.md` |
| **BL** | `_docs/03-backlog/02-user-stories.md`, 88 stories with EARS acceptance criteria |
| **R1 / R2** | Review 1 and Review 2 guideline extracts plus slide templates in `extracted/` |
| **Qn** | A question in the batch in `_handoff/SYNC.md` entry C-002 |

"Settled by" names the source that decides the fix. Where it names a question, the SSOT does not
settle it and the rewrite waits for the answer.

---

## 1. Template structure

| # | Section | Missing or wrong | Settled by |
|---|---|---|---|
| G-01 | Part I, Project Report | The template opens with Part I: Status Report, Team Involvements, Issues/Suggestions. The draft has no Part I | TPL §I; content in **Q24** |
| G-02 | Record of Changes | One row dated 2026-09-17. The rewrite appends rows; it never edits the first | TPL; author attribution in **Q24** |
| G-03 | Numbering | The draft inserts §3.1.1 Main Flows, which pushes Non-Screen Functions to §3.1.5 and the ERD to §3.1.6 (template: §3.1.4 and §3.1.5). Template §3.2 onwards is per-feature function detail; the draft has none | Brief says keep the draft's numbering where possible. Plan: keep §3.1.1 to §3.1.6 as numbered, add §3.2 onwards per feature |
| G-04 | Figure captions | Captions use `***Figure N*** —`. The separator must be a colon, and the em dash is banned in prose. Captions carry "Rendered at 300 dpi" rather than the placement clause | `01-conventions/13` §3, `14` §1 |
| G-05 | Prose | Em dashes throughout (status block, Record of Changes, §1, §2.1, §2.2, §4.2.4, §5.1) | `14` §1 |
| G-06 | Status block | States that screens, ERD and feature specs are deferred to W8. Must be restated for the version being written | Scope decision in **Q12** |

## 2. Product Overview (§1)

| # | Section | Missing or wrong | Settled by |
|---|---|---|---|
| G-07 | §1 | No "building a system" versus "building a platform" framing. Review 1 asks for exactly this distinction. `CA-Q32` (one tenant) cuts against a platform claim, while D-007 (ingress seam), D-015 (configuration), D-019 (stock app compatibility) and `CA-Q33` (extensible sub-roles) support one | R1; the claim itself in **Q1** |
| G-08 | §1 | "Smart" in the registered title is never explained, although the register carries it as a risk | `CA-Q29` (SOS, fall detection, fallback and priority queue, audit logs, watchdogs), REG risk row "Smart Device Rental Management" |
| G-09 | §1 | Firmware described as having "multi-hop messaging" and "It works". Neither is cited in FGT | `14` §1.5: cite FGT or mark `(unverified)` |
| G-10 | §1.1 Context Diagram | Arrows carry no labels. The template asks for data, control and material flows; Review 2 asks for a Level-0 DFD with one process and labelled flows | TPL §1, R2 slide 4 |
| G-11 | §1.1 | Gateway Bridge is drawn **outside** the system boundary, yet the team builds it (MF-02, epic E4). The device-side durable queue (Stage B, D-018) is team-built firmware | **Q10** |
| G-12 | §1.1 | Missing external systems implied by `CA-Q31` and `CA-Q35`: Google OAuth and an email service for OTP. "Notification channel" is unnamed | **Q9**, **Q11** |
| G-13 | §1 | Delivery stages absent. MF-02's offline claim depends on Stage B (on-device queue) and Stage C (basecamp bridge) | REG D-018, D-020. SSOT corrected in this pass, see §8 |

## 3. User Requirements (§2)

| # | Section | Missing or wrong | Settled by |
|---|---|---|---|
| G-14 | §2.1 Actors | Actor model contradicts `CA-Q33`: two major roles, Customer and Staff, with Staff sub-roles Operator, Guide, Admin, extensible. The draft has four peer roles plus a read-only Admin to Staff generalization (RF §2) | **Q2** |
| G-15 | §2.1 | No anonymous visitor, although `CA-Q30` lets a Customer browse without an account | **Q2** |
| G-16 | §2.1 | Scheduler is listed as an actor but appears in no diagram and invokes no use case. TrekLink Device is an actor but absent from every UC diagram | Plan: keep both, show Device on MF-02/03/04 diagrams, attach Scheduler to the time-driven UCs |
| G-17 | §2.2.1 Diagrams | Drawn per actor (three figures), not per Main Flow. No system boundary box. Admin to View Live Map is in the catalogue (UC-14) but on no diagram. The actor generalization is described in prose and never drawn | Brief task B; TPL §2.2.1; cross-cutting UCs in **Q14** |
| G-18 | §2.2.1 | `include` misuse. UC-13 Ingest Field Event includes UC-23 Send Notification, but most field events (GPS, telemetry) notify nobody. UC-11 Calculate Rental Charge includes UC-10 Inspect Returned Device, which inverts the dependency: inspection is Staff's own use case and precedes the charge | RF §3.2's own rule. Fix proposed in **Q13** |
| G-19 | §2.2.2 Descriptions | Catalogue only (ID, name, actor, MF, priority). The template column "Use Case Description" is empty, and the brief requires a full specification per use case | TPL §2.2.2, brief task B |
| G-20 | §2.2.2 | Use cases the Main Flows and answers require are missing. Candidates listed in **Q13** | MF main paths and exceptions, `CA-Q31`, `Q35`, `Q59`, `Q62`, `Q65`, `Q71`, `Q72`, D-021 |

## 4. Functional Requirements (§3)

| # | Section | Missing or wrong | Settled by |
|---|---|---|---|
| G-21 | §3 | No functional requirement exists in EARS form. The BR matrix cites 24 FR IDs (FR-BOOK-02, FR-DEV-05, FR-EVT-01 and others) that are **defined nowhere** in the draft, RF or BL. Every one is a dangling reference | BL acceptance criteria are EARS already. ID scheme in **Q15** |
| G-22 | §3.1.2 to §3.1.4 | Screens Flow, Screen Descriptions and Screen Authorization deferred | TPL §3.1; **Q12** |
| G-23 | §3.1.5 Non-Screen Functions | Missing: on-device durable queue (Stage B), queue bound and shedding (E02-5), gateway staleness (E04-2), incident auto-escalation (MF-03 parameter), non-return grace expiry (BR-22), reservation hold of 10 minutes (`CA-Q59`). "Priority-ordered flush" is attributed to the gateway only | MF, REG D-018, `CA-Q59` |
| G-24 | §3.1.6 ERD | Deferred. Review 2 needs a 5 to 8 entity ERD with PK, FK and cardinality. `CA-Q55` makes Booking and Rental separate entities | R2 slide 7; **Q12** |
| G-25 | §3 | No state machines. Device 7-state and Incident 5-state are named graded deliverables. Booking (`CA-Q56`) and Trip (`CA-Q66`) FSMs exist only as Recorded answers | Charter §7; **Q3**, **Q4**, **Q5**, **Q6** |
| G-26 | §3 | State names conflict across sources. MF-01 postcondition "trip in `Scheduled`" and MF-04 precondition "trip `In Progress`" match no state in `CA-Q66`. MF-01 "Booking(Pending)" plus E01-2 "`Cancelled`" do not match `CA-Q56` (`start`, `sent`, `pending`, `completed`) | **Q3**, **Q5** |
| G-27 | §3 | `CA-Q47` says the device FSM is not final, while the charter and D-016 fix seven states. `CA-Q53` (pre-allocation to a future trip while the device is still out) cannot be expressed as a single device state | **Q4** |

## 5. Non-Functional Requirements (§4)

| # | Section | Missing or wrong | Settled by |
|---|---|---|---|
| G-28 | §4.1 | "Gateway to backend, topic carries the priority tier" contradicts D-019 (stock topic `<root>/2/e/...` and `<root>/2/json/...`) and FGT §4 (JSON envelope has no `priority`) | REG D-019, FGT §4 |
| G-29 | §4.1 | "Backend to map provider" is wrong: tiles are fetched by the browser, which is why the key is browser-visible | Charter §8, REG D-012 |
| G-30 | §4.1 | Missing interfaces: device direct MQTT over Wi-Fi (Stage A), Web Serial and Web Bluetooth to the node (Stage C, D-020), stock Meshtastic app proxy path (D-019), user interface section, Google OAuth and email (`CA-Q31`) | REG D-018 to D-020; **Q9**, **Q11** |
| G-31 | §4.2.1 | NFR-REL-05 puts durable storage on "the gateway". After D-018 the first durable buffer is on the device (Stage B) and the large one at basecamp (Stage C) | REG D-018 |
| G-32 | §4.2.3 | Missing security requirements already decided: custom per-fleet channel PSK (D-021), TLS plus per-gateway API key on the broker hop (D-021), staff never see a password (`CA-Q35`), audit of everything (`CA-Q46`), soft delete (`CA-Q36`) | REG D-021; CA |
| G-33 | §4.2.4 | NFR-USE-01 (4 steps, 6 fields) and NFR-USE-02 (2 fields) have no source anywhere in the SSOT | `14` §1.6; **Q17** |
| G-34 | §4.2 | No availability, MTBF or MTTR target for the platform (template §4.2.2). Incident notification latency of 2 s (BL US-058) is absent. RQ3's MTTA and MTTR are not stated as measured quantities | TPL §4.2.2, BL US-058; availability in **Q17** |

## 6. Requirement Appendix (§5)

| # | Section | Missing or wrong | Settled by |
|---|---|---|---|
| G-35 | §5.1 BR-04 | "A device below the configured minimum battery may not be checked out" contradicts `CA-Q52`: telemetry never blocks assignment, manual verification is final | **Q3** |
| G-36 | §5.1 BR-03 | "Per the configured schedule and by notice period" is less specific than `CA-Q60`: free within 10 minutes, then 5 % of the rental fee, all configurable | **Q3** |
| G-37 | §5.1 | Rules stated in answers and decisions but missing from the matrix: username derived from email local part (`CA-Q41`), staff reset without seeing the password (`Q35`), soft delete (`Q36`), trip may restrict device versions (`Q50`), one device on two non-overlapping trips (`Q53`), rental without booking (`Q55`), multi-device only for Guide bookings (`Q57`), 10-minute hold (`Q59`), deposit by tier (`Q61`), devices return only through the Guide (`Q71`), PSK provisioning is mandatory (D-021) | **Q3** |
| G-38 | §5.2 E03-6 | "Incident reopens" has no matching transition in the 5-state FSM | **Q6** |
| G-39 | §5.3 Messages | Deferred. The brief requires a messages appendix. Derivable from the exception scenarios and the error-code convention (`CA-Q39`) | Brief task B |
| G-40 | §5 | No glossary. No MF to UC to FR traceability matrix | Brief task B |
| G-41 | §5.4 | "Localization" is out of scope, while `CA-Q9` requires a locale system for the landing page | **Q20** |
| G-42 | §5.4 | "v1 is out of the demonstration set" versus `CA-Q50` "v1 is registrable". Both hold: registrable in the product, absent from the demo set | D-005, `CA-Q50`. No question |

## 7. Review 1 and Review 2 expectations

| # | Item | Status | Settled by |
|---|---|---|---|
| G-43 | R1 template order: Context, Existing Situation and Problems, Proposed Solution, Key Features, Actors and Functions, Main Flow slides | Current outline opens with Team and Background, has no Key Features slide, and adds Why-no-existing-product, Scope, Out of scope, Metrics, Plan, Risks, Ask | R1 template; task D |
| G-44 | R1 Existing Situation | Template asks for evidence per pain point (a number, a quote, a screenshot). The SSOT holds no measured evidence | **Q18** |
| G-45 | R1 every member presents | Outline names flow owners, not presenters | **Q19** |
| G-46 | R2 Context Diagram (Level-0 DFD) | todo: current figure has no labelled flows | G-10 |
| G-47 | R2 System Architecture | todo: belongs in the SDD, not drawn anywhere in the pack | Out of this task |
| G-48 | R2 Tech Stack with a one-clause reason per choice | partial: charter §6 lists the stack; reasons exist only for Prisma (D-001), Neon (D-010), MapLibre and Goong (D-012) | REG |
| G-49 | R2 ERD, 5 to 8 core entities | todo | **Q12** |
| G-50 | R2 Use Case Diagram | draft exists, needs the per-MF redraw | G-17 |
| G-51 | R2 State Machine, most complex entity | todo: Incident (5 states plus reopen and suspected handling) or Device | **Q4**, **Q6** |
| G-52 | R2 Activity Diagram | done in substance: the five MF swimlanes | MF |

## 8. SSOT corrections made in this pass (AGENTS.md §2.6)

| File | Change | Basis |
|---|---|---|
| `05-main-flows.md` MF-02 | "Two delivery stages" rewritten to the three-stage model; the basecamp bridge is Stage C | D-018 naming note |
| `02-roadmap-and-milestones.md` §6.1 row 1, §6.2 gateway row | Stage naming aligned to D-018 | D-018 |
| `03-decisions-and-risk-register.md` D-012 | Appended a dated update: `CA-Q28` records the sovereignty check as done; screenshot filing unrecorded | `CA-Q28` |

Not corrected, because the fix is a content decision rather than a naming fix: the MF-02 swimlane
still draws the SQLite buffer in the Gateway lane only (**Q16**).
