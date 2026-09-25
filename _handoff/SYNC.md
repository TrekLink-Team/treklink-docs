# Handoff log: cloud session and local orchestrator

Append-only. Never edit an earlier entry. Cloud entries are `C-nnn`, orchestrator answers are
`O-nnn | re C-nnn`. Files for other repositories live under `outbound/`, laid out by target path.

---

### C-001 | cloud to orchestrator | 2026-09-25 03:12 UTC | STATUS

**Branch**: `claude/blissful-pasteur-wseu0g`. The environment forces this name, so
`docs/srs-and-review-deliverables` is not used. The branch was reset onto `origin/dev` (089374b)
before any commit, because it had been created from `main`, which is not an ancestor of `dev`. It
carried no commits of its own, so nothing was discarded.

**Context pack**: attached to the session, unzipped into `ignore/capstone-pack/` (gitignored, not
committed). `PACK.txt` reads capstone@cecdae7, built 2026-09-25T02:58:37Z.

**Start-up reading done**: `AGENTS.md`; conventions 00, 02, 07, 08, 11, 13, 14; project context 01
to 07 and the full decision register; pack reports, template extract, review guidelines and slide
templates.

**Recent sessions**: no `docs/sessions/` or `ignore/*/docs/sessions/` files exist in this repository.

**Open register items touching this work**: none block the SRS. D-020 (Stage C form) is decided in
principle only. `CA` questions 30 to 73 are Recorded, not Confirmed, which is why C-002 question 3
exists.

**SSOT corrections committed in this pass** (AGENTS.md §2.6), listed in `srs-gap-audit.md` §8:
`05-main-flows.md` and `02-roadmap-and-milestones.md` aligned to D-018's Stage A/B/C naming;
D-012 gains a dated note that `CA-Q28` records the sovereignty check as done.

---

### C-002 | cloud to orchestrator | 2026-09-25 03:12 UTC | QUESTION

Task A is done. The gap table is `_handoff/srs-gap-audit.md` (52 rows, G-01 to G-52). Each row names
the source that settles it; the rows that no source settles point to a question below. Task B waits
for these answers.

Questions are numbered in one run and ordered by how much work each one blocks. Where I have a
recommendation it is stated, so a one-word answer ("agree") is enough.

**Framing and actors**

1. **System or platform.** Review 1 asks the team to distinguish "building a system" from "building
   a platform". `CA-Q32` says one tenant, which argues against a multi-tenant platform claim. What
   does the SRS claim? Recommendation: a single-tenant operations **system**, named TrekLink
   Operations Platform, whose platform properties are its extension seams: pluggable ingress
   adapters (D-007), configuration-driven business rules (D-015), stock Meshtastic compatibility
   (D-019) and an extensible Staff sub-role list (`CA-Q33`). If the team intends a multi-tenant
   platform, `CA-Q32` changes.
2. **Actor model.** The draft has Customer, Staff, Guide and Admin as peers, with Admin generalizing
   Staff for reads only (RF §2). `CA-Q33` (Recorded) says two major roles, Customer and Staff, where
   Staff has sub-roles Operator, Guide and Admin. Recommendation: human actors **Guest** (anonymous
   browse, `CA-Q30`), **Customer**, and an abstract **Staff** generalizing **Operator**, **Guide** and
   **Admin**. "Staff" in the Main Flows becomes "Operator". Confirm, and confirm whether RF §2's rule
   still holds that an Admin does not perform operational actions such as acknowledging an incident.
3. **Recorded answers in a graded SRS.** `CA` questions 30 to 73 are Recorded, not Confirmed, and
   several contradict RF and MF: BR-04 versus `Q52`, BR-03 versus `Q60`, trip states versus `Q66`,
   booking states versus `Q56`, and the missing rules in gap row G-37. May the SRS adopt the Recorded
   answers as requirements, each marked provisional pending the module interview? Recommendation:
   yes, and where a Recorded answer contradicts RF, the Recorded answer wins because it is newer and
   comes from the leader.

**State machines**

4. **Device FSM.** The charter and D-016 fix seven states; `CA-Q47` says the FSM is not final, and
   `CA-Q53` needs a device to be pre-allocated to a future trip while still `In-Field`. Recommendation:
   keep the seven states as the device's **physical** state, and model future commitments as
   Allocation records with non-overlapping time windows, so `Reserved` means "held for the next
   trip that starts". Also: what moves `Rented` to `In-Field`, a Guide or Operator "start trip"
   action, or the first field event from that device on an active trip?
5. **Trip FSM.** `CA-Q66` lists `Draft`, `On Prepare`, `On Booking`, `On Start`, `Ongoing`,
   `Finished`, `Cancelled` and an emergency state whose name is open (the question 76 that `CA`
   references but never recorded). What is the emergency state called, and does an open Incident
   move the trip into it automatically, or only by an Operator action?
6. **Incident FSM gaps.** Three undefined transitions: (a) E03-6 reopen: from `Resolved` back to
   `In Progress`, and can a `Closed` incident reopen or does a new one open? (b) A `Suspected`
   incident: a separate state, or a confidence attribute on `Detected`? (c) Dismissing a suspected
   incident, the "lighter action" in MF-03: which transition, and who may do it? Recommendation:
   confidence is an attribute; dismissal is `Detected` to `Closed` with a mandatory reason; reopen
   is `Resolved` to `In Progress` only, and new beacons after `Closed` open a new Incident.
7. **Incident authority.** UC-15 lists Staff and Guide as acknowledgers, but MF-03 shows only Staff
   acknowledging while the Guide confirms the situation. Does a Guide's acknowledgement perform the
   `Acknowledged` transition and stop the MTTA clock? Who may move an incident to `Resolved` and to
   `Closed`: Operator only, or a Guide in the field too?

**Money and documents**

8. **Who pays, and when.** MF-05 shows Staff paying and closing the rental, UC-12 has Staff as actor,
   while `CA-Q60` mentions escrow and an instant refund, which implies the Customer pays at booking.
   Is there a Customer payment at booking time (rental fee and deposit into escrow) plus a settlement
   at return, or a single settlement recorded by an Operator at return?
9. **Notification channel.** The context diagram has an unnamed "Notification channel". Which
   channels are in scope: in-app WebSocket only, email (already needed for OTP, `CA-Q31`), SMS, Zalo?
   A Guide in a dead zone cannot receive any of them; is WebSocket to the Guide's phone at signal
   recovery acceptable?
10. **System boundary.** RF's context diagram puts the Gateway Bridge outside the system, but the team
    builds it. Recommendation: inside the boundary (Level-0 DFD process), with the TrekLink Device and
    LoRa mesh as the external entity. The on-device queue (Stage B) is firmware; describe it as an
    external interface requirement on the device, not as part of the platform process. Agree?
11. **Authentication externals.** Confirm that `CA-Q31` (Google OAuth, email OTP) is in scope for the
    SRS, so Google Identity and an email delivery service join the context diagram as external systems.
12. **What the W4 SRS contains.** The draft defers Screens Flow, Screen Descriptions, Screen
    Authorization, ERD and Messages to W8. Recommendation: write now the Screen Authorization matrix
    (derivable from the roles), a conceptual ERD of 5 to 8 entities (Review 2 needs it anyway), and
    the Messages list (derived from the exception scenarios); keep Screens Flow and Screen
    Descriptions deferred to W8, since no screen design exists. Agree?
13. **Use case set.** Keep UC-01 to UC-26 stable and add from UC-27. Proposed additions: Register
    Account, Reset Password, Cancel Booking, Extend Reservation Hold, Manage Trek Packages, Create
    Trip, Request Trip (Guide), Reschedule Trip, Start Trip, End Trip, Confirm Device Handover
    (Guide readiness checklist, `CA-Q73`), Register Device, Provision Device Channel Key (D-021),
    Report Missing Device, Record Maintenance, Retire Device, Sign Rental Agreement, Approve Fee
    Waiver, View Booking History, Dismiss Suspected Incident, Trigger SOS (Device), View System
    Health. Also correct two `include` errors: UC-13 no longer includes UC-23 (notification follows
    incident creation, so UC-23 is included by a new "Create Incident" system use case or by UC-15),
    and UC-11 no longer includes UC-10 (inspection precedes the charge as its own use case). Add,
    drop or rename any?
14. **UC diagrams per Main Flow.** UC-18 to UC-21 and several additions belong to no Main Flow.
    Recommendation: five per-MF diagrams plus a sixth "Administration and access" diagram. Agree?

**Requirements form**

15. **FR identifiers.** The BR matrix cites 24 FR IDs that exist nowhere. Recommendation: build the FR
    catalogue with prefixes AUTH, DEV, BOOK, TRIP, EVT, INC, MON, BILL, CFG, reserving those 24 IDs
    with the meaning the BR matrix implies, and write each FR's EARS text from the backlog acceptance
    criteria, citing the `US-nnn` it comes from. Agree?
16. **MF-02 swimlane.** It draws the SQLite buffer in the Gateway lane only. After D-018 the first
    durable buffer is on the device. The diagram is supervisor-derived (D-016). Redraw it with a
    device-side buffer step, or keep the diagram and explain the stages in text?
17. **Usability and availability numbers.** NFR-USE-01 (at most 4 steps, 6 fields per step) and
    NFR-USE-02 (acknowledge in one step, at most 2 fields) have no source in the SSOT. Keep them as
    team targets, supply the source, or drop them? And is there an availability target for the
    platform (the template's §4.2.2 asks for one)? If there is none, I will leave the row as
    `(needs check)` and invent no figure.

**Review 1 deck**

18. **Evidence for the pain points.** The Review 1 template asks for a number, a quote or a
    screenshot per problem. The SSOT has none measured. Is there any agency interview, survey or
    incident account the team can cite? If not, the slides state the problems without figures.
19. **Presenters.** Every member must present. Proposal, following Main Flow ownership: KhoaDD takes
    title, Context and Proposed Solution, then MF-02. LongLP takes Existing Situation and Problems,
    then MF-05. HoangTK takes Key Features, then MF-03. LongNN takes Actors and Functions, then MF-04.
    TanNB takes MF-01, then scope, plan and the closing ask. Change any?

**Scope edges and records**

20. **Landing page and localization.** SRS, charter and Report 1 put localization out of scope;
    `CA-Q9` needs a locale system for the landing page. Recommendation: the landing page is a separate
    deliverable outside the SRS (it is not a Main Flow, `CA-Q24`), and localization stays out of
    scope for the operations system. Agree?
21. **Rental agreement signer.** `CA-Q62` needs a draw-on-web signature saved onto the PDF. Who signs:
    the Customer, or the Guide or Operator on behalf of an unauthenticated customer (`CA-Q55`)? At
    booking confirmation or at check-out?
22. **Sandbox payment provider.** An internal mock with Pending, Paid and Failed (BL US-069), or a
    third-party sandbox such as VNPay or MoMo test mode? It decides whether Sandbox Payment is an
    external system on the context diagram.
23. **Sovereignty evidence.** `CA-Q28` says the check is done. Are the screenshots filed, and where?
    BR-24 and TC-24 cite them.
24. **Part I and authorship.** The template's Part I asks for a status report, per-member team
    involvement and issues. Include it? If yes, who contributed what to the SRS so far? And whose
    name goes in "In charge" for this revision: TanNB as SRS owner (roadmap §5), or KhoaDD?

---

### C-003 | cloud to orchestrator | 2026-09-25 04:05 UTC | STATUS

**C-002 answered by the leader in chat, not through an `O-` entry.** Instruction: default to the
recommendation for every unanswered question. No question received an individual answer, so all 24
take their defaults. Questions without a recommendation (4 trigger, 5, 7, 8, 9, 16, 17 availability,
18, 21, 22, 23, 24) took a conservative default, marked "needs check".

Recorded same-pass in `_docs/00-project-context/07-clarification-answers.md` §5, one row per
question with its level. Override any row with an `O-` entry and I will rework the SRS to match.

**Correction to C-002**: question 17 said NFR-USE-01 and NFR-USE-02 have no SSOT source. They do:
`01-conventions/06-frontend-conventions.md` §3. Gap row G-33 is corrected.

Task B starts now.

---

### C-004 | cloud to orchestrator | 2026-09-25 04:30 UTC | STATUS

**Supersedes C-003's claim that every answer was a default.** C-003 was premature: the leader had
not yet seen the question list. The leader has now answered in chat: questions 1 to 22 agree to the
stated default; question 23, no sovereignty screenshots are filed yet; question 24, "In charge" is
Đỗ Đăng Khoa and Nguyễn Bá Tân, or Đỗ Đăng Khoa alone where only one name fits.

`07-clarification-answers.md` §5 now marks all 24 rows Confirmed. D-012 gains a note that the
screenshot evidence is outstanding.

Task B starts now.

---

### C-005 | cloud to orchestrator | 2026-09-25 | DELIVERY

Session ended early by the leader (context budget). Tasks B, C and D are delivered; task E is not
started. Everything is on branch `claude/blissful-pasteur-wseu0g`; PR into `dev` opened.

**Delivered under `_handoff/outbound/capstone/Documents/reports/`** (copy into `capstone/Documents/reports/`):

| File | What |
|---|---|
| `Report3_SRS_DRAFT.md` | Full SRS per the official template: Part I, Record of Changes, overview with system-vs-platform framing, Level-0 context diagram, 12 actors, 58 use cases (UC-27 to UC-58 new) each specified, 112 EARS FRs traced to UC and MF (reserved BR IDs kept), screen authorization, non-screen functions, 2-part conceptual ERD, 5 state machines, NFRs incl. security/availability/notification, 37 BRs, 31 exception scenarios, 33 messages, glossary, MF to UC to FR matrix |
| `Report3_SRS_TrekLink.docx` | Built with pandoc against the official template: template cover and a fresh TOC field (Word updates it on open), template heading and table styles |
| `assets/srs-fig1.png` to `srs-fig27.png`, `assets/mermaid/*.mmd` | Rendered with mermaid-cli and Mermaid 12.0.0; Mermaid source kept. `sizes.txt` holds each placement, `figures.txt` the figure index |
| `Review1_Slides_OUTLINE.md` | Template slide order, a named presenter per slide, and the Review 2 skeleton with each diagram marked done or todo |
| `Review1_Slides_TrekLink.pptx` | 21 slides built with python-pptx from `Review1_Slide_Template.pptx`; the TIP bar carries the presenter |

**Build tools**: `_handoff/tools/` (`srs_data.py`, `build_srs.py`, `render_figures.sh`,
`measure_figures.py`, `build_docx.py`, `build_deck.py`). Move them before `_handoff/` is removed
if the SRS will be regenerated.

**SSOT changes committed on this branch**: `07-clarification-answers.md` §5 (questions 1 to 28,
all Confirmed); `06-requirements-foundation.md` (actor model, BR-03, BR-04, `include` fixes);
`05-main-flows.md` and roadmap (Stage A/B/C naming); D-012 (sovereignty screenshots not filed);
`01-conventions/13` §4.1 (report figures stay upright, leader instruction) and four carried
below-floor figures.

**Open, for the orchestrator or next session**:
1. Task E not done: list where Report 1 and the PMP contradict the SRS (known: two-stage gateway
   wording, four peer roles, localization note, SQLite queue placed only at the gateway).
2. MF-02 to MF-05 swimlanes print at 5.45 to 6.75 pt in the docx (upright, full-page plates, as the
   leader chose). Splitting each flow into two figures would clear 7 pt; leader decision needed.
3. Neither the docx nor the pptx has had human visual review. The docx was checked page by page in
   LibreOffice; the pptx was not opened visually.
4. Backlog (leader only, `build_backlog.py`): US-002 still says email plus password registration
   and Admin-only Staff provisioning; SRS follows `07` §3 questions 31 and 41 and §5 question 2.
5. Sovereignty screenshots are still to be filed (BR-24).
