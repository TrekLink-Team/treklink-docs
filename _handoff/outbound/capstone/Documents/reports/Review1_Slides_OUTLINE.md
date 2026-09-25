% TrekLink, Review 1
% Group GFA26SE55 · FA26SE159 · Supervisor: Đặng Ngọc Minh Đức
% Week 4 · Gate 1, Proposal and Requirement

<!--
Revised 2026-09-25 against Review1_Slide_Template.pptx and Report 3 (SRS) of the same date.
Slides 1 to 6 follow the template's order exactly; the Main Flow slides follow as the template's
slide 7 pattern, one per flow plus its swimlane; slides 17 to 21 close the talk.
Every member presents (Review 1 guideline). Presenter per slide is in the "Presenter" line, taken
from 07-clarification-answers.md §5 question 19. Built into Review1_Slides_TrekLink.pptx by
_handoff/tools/build_deck.py. Figures are the SRS figures, upright.
-->

# Presenter plan

| Member | Slides | Time budget |
|---|---|---|
| Đỗ Đăng Khoa (KhoaDD), leader | 1 Title, 2 Context, 4 Proposed Solution, 9 to 10 MF-02 | about 4 min |
| Lâm Phi Long (LongLP) | 3 Existing Situation and Problems, 15 to 16 MF-05, 18 How we will know it works | about 3 min |
| Trần Khải Hoàng (HoangTK) | 5 Key Features, 11 to 12 MF-03, 19 Top risks | about 3 min |
| Nguyễn Ngọc Long (LongNN) | 6 Actors and Functions, 13 to 14 MF-04 | about 3 min |
| Nguyễn Bá Tân (TanNB) | 7 to 8 MF-01, 17 Scope, 20 Plan, 21 What we ask | about 3 min |

Slides 18 and 19 are not in question 19's list; they are assigned to balance speaking time.

# 1. Title

TrekLink Operations Platform: off-grid trekking safety and operations over a LoRa mesh.

Team: Đỗ Đăng Khoa, Team Leader · Lâm Phi Long · Trần Khải Hoàng · Nguyễn Ngọc Long · Nguyễn Bá Tân.
Mentor: Đặng Ngọc Minh Đức.

Presenter: KhoaDD

# 2. Context

**Domain**: trekking agencies running multi-day routes in Vietnam's cellular dead zones (Tà Năng to
Phan Dũng, Tả Liên Sơn, Bạch Mộc Lương Tử).

**Who is affected**: the agency's operators at base, its field guides, and its customers on the
trail.

**Why now**: in Summer 2026 the team built TrekLink firmware, a LoRa mesh on ESP32 that sends SOS,
fall detection and positions without cellular coverage. Nothing yet carries that data to the people
who must act on it.

**System, not platform.** We build one operations system for one agency. What makes it more than a
single system is a set of seams: new field transports plug in, every business rule is
configuration, stock Meshtastic devices and apps keep working, and staff roles extend as data.

**Scope boundary**: the web system, the gateway and targeted firmware work. Not the mesh stack, not
native apps, not real payments.

Presenter: KhoaDD

# 3. Existing Situation and Problems

1. **Field events are lost.** The node's uplink queue holds 16 events in RAM and discards the oldest
   first, so in an outage the one SOS text frame is the first thing dropped. Evidence: firmware
   source, `MQTT.cpp` lines 821 to 823.
2. **An SOS goes nowhere.** A device SOS raises a local radio alarm and nothing else. No one is
   assigned, nothing is recorded.
3. **No operational records.** Devices, rentals and trips are not tracked in any system; agencies
   coordinate by phone and messaging app.
4. **Impact**: response depends on who happens to notice; there is no audit trail to review an
   emergency afterwards; device custody and charges are disputed by memory.

No measured figures are claimed (07 §5 question 18).

Presenter: LongLP

# 4. Proposed Solution

**One sentence**: a web operations system plus gateway that delivers every field event to the cloud
exactly once, turns each SOS into one owned and audited incident, and runs the device fleet,
rentals and trips around it.

| Problem | How it is resolved |
|---|---|
| Events lost in outages | Durable priority queues on the device and at basecamp; P0 SOS always first; `eventId` deduplication |
| SOS goes nowhere | One incident per SOS episode, five-state lifecycle, alert in 2 seconds, full audit trail |
| No records | Booking, rental, 7-state device lifecycle, inspection and sandbox billing |

**Approach**: responsive web app (React), NestJS backend, Node.js gateway, MQTT, PostgreSQL,
MapLibre with Goong Maps.

**Out of scope**: mesh-stack rearchitecture, native mobile apps, real payments, route
recommendation, localization, hardware certification, multi-tenancy.

Presenter: KhoaDD

# 5. Key Features

1. **Offline-safe field sync**: every event arrives exactly once, SOS first after an outage.
2. **SOS to incident**: one episode, one incident, owned, acknowledged and closed with a full trail.
3. **Live trip monitoring**: one map of trips, devices and incidents, scoped by role on the server.
4. **Booking and rental**: from a customer's booking to a provisioned device in the Guide's hands.
5. **Return and billing**: inspection, itemized fees, deposit first, sandbox payment.
6. **Rules as configuration**: every fee, threshold and window changeable live, and demonstrable.

Presenter: HoangTK

# 6. Actors and Their Functions

| Actor | Key functions |
|---|---|
| Guest | Browse packages · Register |
| Customer | Book · Pay · Sign agreement · View own history |
| Operator (Staff) | Confirm bookings · Allocate and provision devices · Check out and in · Inspect · Coordinate incidents |
| Guide (Staff) | Confirm handover · Start and end trip · Acknowledge incidents · Report from the field · Own trips only |
| Admin (Staff) | Users and roles · Pricing and parameters · Device catalogue · Audit and health |
| TrekLink Device, Gateway Bridge, Scheduler | Emit SOS and positions · Buffer and deliver events · Expire holds, flag stale, escalate |

Presenter: LongNN

# 7. Main Flow 1: Booking to Rental to Trip Preparation

1. Customer books a package; one device is held for 10 minutes.
2. Operator confirms, seeing device and Guide conflicts first.
3. Operator allocates devices, provisions the fleet key, generates the agreement.
4. Customer signs; deposit paid; Guide confirms handover and checklist.
5. Check-out: devices Rented, trip ready to start.

Exception shown: two customers take the last device at once, one gets "no longer available".

Presenter: TanNB

# 8. MF-01 swimlane

SRS Figure 16.

Presenter: TanNB

# 9. Main Flow 2: Field Data to Offline Gateway to Cloud Sync

1. Device broadcasts SOS, position or telemetry over the mesh.
2. Event is classified P0 to P3 and queued durably before any send.
3. Uplink down: the queue holds it on the device (Stage B) and at basecamp (Stage C).
4. Uplink back: flush in strict priority order, SOS first.
5. Backend keys it by `eventId`; a replay is a no-op.

Exception shown: the same packet delivered 10 times creates 0 duplicate incidents.

Presenter: KhoaDD

# 10. MF-02 swimlane

SRS Figure 17.

Presenter: KhoaDD

# 11. Main Flow 3: SOS to Incident to Emergency Response

1. SOS by button, gesture or fall detection.
2. Backend opens one incident for the episode, or appends to the open one.
3. Guide and Operators alerted within 2 seconds.
4. First acknowledgement takes ownership and starts the clock.
5. In Progress, Resolved, Closed, each with actor, time and note.

Exception shown: the SOS text frame is lost; beacon cadence raises a Suspected incident.

Presenter: HoangTK

# 12. MF-03 swimlane

SRS Figure 18.

Presenter: HoangTK

# 13. Main Flow 4: Real-Time Trip Monitoring

1. Positions and telemetry arrive through MF-02.
2. Backend updates position, battery and last-seen.
3. Server pushes only what each role may see.
4. Map shows markers by status, battery, last-seen, incidents.
5. Silent devices and gateways turn visibly stale.

Exception shown: a Guide asks for another Guide's trip and is refused on the server.

Presenter: LongNN

# 14. MF-04 swimlane

SRS Figure 19.

Presenter: LongNN

# 15. Main Flow 5: Return to Inspection to Billing to Maintenance

1. Guide collects every device and ends the trip.
2. Operator checks devices in and inspects them.
3. Backend computes base, late and damage fees, deposit first.
4. Balance paid or refunded in sandbox; rental closes.
5. Device back to Available, or to Maintenance, or Retired.

Exception shown: payment fails, and the rental stays open with the balance visible.

Presenter: LongLP

# 16. MF-05 swimlane

SRS Figure 20.

Presenter: LongLP

# 17. Scope, stated now

In scope: five Main Flows, 58 use cases, 112 functional requirements (SRS §2 and §3), gateway,
targeted firmware work (on-device queue, fleet channel key).

Out of scope: mesh-stack rearchitecture, native mobile apps, production payment, route
recommendation, localization of the system, hardware certification, multi-tenancy.

Presenter: TanNB

# 18. How we will know it works

| Property | Target |
|---|---|
| Gateway to cloud sync | ≤ 5 s when the uplink is available |
| Offline recovery | ≥ 99 % delivered after a 30 s to 30 min loss |
| Duplicate prevention | 0 duplicate incidents across a 10× replay |
| Priority ordering | ≥ 99 %, all P0 before any P2 or P3 |
| Incident alert | ≤ 2 s from creation to connected clients |
| API latency | ≤ 300 ms at p95, 50 concurrent users |

Measured in the evaluation, not asserted.

Presenter: LongLP

# 19. Top risks

| Risk | Impact | Mitigation |
|---|---|---|
| SOS announced by one unacknowledged radio frame | Critical | Cadence-anomaly detection now; firmware marker on every beacon |
| Node queue drops the SOS first in an outage | Critical | On-device durable priority queue (Stage B) |
| Map tiles misrepresenting national sovereignty | Critical | Goong Maps held in configuration; sovereignty screenshots to file |
| Few physical devices for radio testing | High | Simulation supplements, never presented as radio evidence |

Presenter: HoangTK

# 20. Plan to Review 2

| Gate | Week | Assessed |
|---|---|---|
| Review 1 | W4 | Problem, scope, requirement baseline |
| Review 2 | W8 | Design baseline; MF-01 and MF-02 demonstrated |
| Faculty Council | W13 | Final product, 85 % of use cases |
| Submission and defence | W15 | Complete package |

Presenter: TanNB

# 21. What we ask

1. Confirmation that the five Main Flows are the right scope for the term.
2. Confirmation that the requirement baseline is clear and verifiable.
3. Feedback recorded against an owner and a deadline, closed with evidence at Review 2.

Thank you. Questions.

Presenter: TanNB

---

# Review 2 outline skeleton (Week 8)

Template: `Review2_Slide_Template.pptx`. The Review 2 guideline asks the team to open with what was
done, changed or dropped since Review 1. Status is as of 2026-09-25.

| # | Slide | Content | Diagram | Status |
|---|---|---|---|---|
| 1 | Title | Team, mentor | none | todo |
| 2 | Context, quick recap | Problem in two sentences; **what was done, changed or dropped since Review 1** | none | todo, after Review 1 feedback |
| 3 | Key Features | The six features, each marked Done or In progress | none | todo |
| 4 | Context Diagram | Level-0 DFD, one process, labelled flows | SRS Figure 1 | **done** |
| 5 | System Architecture | Layers and components, every arrow labelled with protocol | Architecture diagram (SDD) | todo |
| 6 | Technology Stack | One-clause reason per choice | none | partial: reasons exist for Prisma (D-001), Neon (D-010), MapLibre and Goong (D-012); the rest todo |
| 7 | Data Design, ERD | 5 to 8 core entities, PK, FK, cardinality | SRS Figures 21 and 22 (conceptual) | **done** conceptually; physical ERD from `schema.prisma` todo |
| 8 | Use Case Diagram | Actors, use cases, relationships | SRS Figures 3 to 11 | **done** |
| 9 | State Machine Diagram | The most complex entity: Incident | SRS Figure 24 (Device: Figure 23) | **done** |
| 10 | Activity Diagram | One Main Flow as activity or swimlane | SRS Figures 16 to 20 | **done** |
| 11 | Demo | MF-01 and MF-02 demonstrated | none | todo |
