# TrekLink — The Five Main Flows

> **Source of the flow set**: `capstone/Documents/course-material/TrekLink-proposed-mainflow-ducndm.png`, supplied by
> the supervisor. These five are **binding** — see **D-016**. They are the units the Mainflow
> Coverage Matrix tracks, the units demoed at each Iteration review, and the units the Faculty
> Council evaluates.
>
> **What this file is for.** It is the single source for the Main Flow material that appears in
> Report 2 §3, Report 3 (SRS), the Review 1 slide deck, and the Mainflow Coverage Matrix. Diagrams
> are Mermaid so they regenerate rather than rot — never paste a screenshot of one back into a doc.
>
> **Layout convention**: each diagram is a true Mermaid **`swimlane-beta`** diagram — one `subgraph`
> per actor lane, matching `Documents/templates/Main flows_ex02.jpg`, the actor-partitioned example
> the course supplies. `swimlane-beta` requires **Mermaid ≥ 11.16.0**; the handbook build is pinned
> to 12.0.0. Orientation is `TB` so lanes run as columns and the flow runs down the page, which is
> what fits A4 portrait. See [`01-conventions/13-diagram-and-figure-conventions.md`](../01-conventions/13-diagram-and-figure-conventions.md).
>
> **Every flow carries at least one exception scenario.** That is a W3 Definition-of-Done item and a
> named anti-fail check: *"Mỗi mainflow đều có ít nhất một exception scenario."* The scenarios below
> populate the Exception Scenario Matrix directly.

**Actors across all flows**: Customer · Staff · Guide · Admin · TrekLink Device · Gateway Bridge ·
Cloud Backend.

| MF | Name | Owner | Epics | Priority |
|---|---|---|---|---|
| [MF-01](#mf-01--booking--rental--trip-preparation) | Booking → Rental → Trip Preparation | TanNB | E3, E2, E1 | High |
| [MF-02](#mf-02--field-data--offline-gateway--cloud-synchronization) | Field Data → Offline Gateway → Cloud Sync | KhoaDD | E4 | **Highest** |
| [MF-03](#mf-03--sos--incident--emergency-response) | SOS → Incident → Emergency Response | HoangTK | E5 | **Highest** |
| [MF-04](#mf-04--real-time-trip-monitoring) | Real-Time Trip Monitoring | LongNN | E5 | High |
| [MF-05](#mf-05--return--inspection--billing--maintenance) | Return → Inspection → Billing → Maintenance | LongLP | E6, E2 | Medium |

**E7 (DevOps/CI-CD) and E8 (Research & Experimental Evaluation) are cross-cutting and deliberately
are not Main Flows.** Say so whenever the Coverage Matrix is presented.

---

## MF-01 — Booking → Rental → Trip Preparation

**Goal**: take a customer from browsing a trek package to a guide holding a provisioned device,
ready to depart. See **Figure 1**.

**Actors**: Customer, Cloud Backend, Staff, Guide
**Precondition**: trek packages published; at least one device in `Available` state
**Postcondition**: rental agreement generated; device in `Rented`; trip in `Scheduled`; guide assigned

```mermaid
swimlane-beta TB
    subgraph customer["Customer"]
        c1[Browse trek packages]
        c2[Submit booking request]
        c3[Reserve device]
        c4[Receive confirmation]
    end
    subgraph backend["Cloud Backend"]
        s1[Validate dates and stock]
        s2[Create Booking: Pending]
        s3[Device to Reserved]
        s4[Device to Rented<br/>Trip to Scheduled]
    end
    subgraph staff["Staff"]
        t1[Review booking]
        t2[Confirm booking]
        t3[Allocate device and guide]
        t4[Generate rental agreement]
        t5[Check out device]
    end
    subgraph guide["Guide"]
        g1[Receive device]
        g2[Verify battery and GPS]
        g3[Ready for trek]
    end
    c1 --> c2 --> s1 --> s2 --> t1 --> t2 --> c4
    c4 --> c3 --> s3 --> t3 --> t4 --> t5 --> s4 --> g1 --> g2 --> g3
```

***Figure 1*** — MF-01 Booking to Rental to Trip Preparation. Lanes are actors; the flow runs top to bottom. Placement: inline, 182.0 x 219.0 mm, labels at 8.06 pt.

**Main path**

1. Customer browses published trek packages and submits a booking request.
2. Backend validates date availability and device stock, creates `Booking(Pending)`.
3. Customer reserves a device; backend moves a device `Available → Reserved`.
4. Staff reviews and confirms the booking; customer is notified.
5. Staff allocates a specific physical device and assigns a guide.
6. Staff generates the rental agreement and checks the device out.
7. Backend moves the device `Reserved → Rented` and the trip to `Scheduled`.
8. Guide receives the device, verifies battery and GPS fix, and marks ready.

**Exception scenarios**

| # | Scenario | Expected behaviour |
|---|---|---|
| E01-1 | Two customers reserve the last device simultaneously | Reservation is transactional with a row-level lock on the device; the loser receives "no longer available" and the booking stays `Pending` with no device attached. Never oversell. |
| E01-2 | Customer cancels after staff confirmation but before check-out | Booking → `Cancelled`; device returns to `Available`; cancellation fee applied per the configured policy. |
| E01-3 | Allocated device fails the guide's health check | Guide rejects handover; device → `Maintenance`; staff re-allocates without re-doing the booking. |
| E01-4 | No guide available for the requested date | Booking cannot be confirmed; staff sees the conflict before confirming, not after. |
| E01-5 | Booking dates overlap an existing rental for the same device | Rejected at validation with the conflicting rental identified. |

**Business rules touched**: device-availability, double-booking prevention, cancellation-fee policy,
guide-assignment eligibility, rental-agreement generation, deposit calculation.

**Configurable parameters** (D-015): cancellation-fee schedule, deposit amount, reservation hold
duration, minimum battery percentage for handover, maximum devices per booking.

---

## MF-02 — Field Data → Offline Gateway → Cloud Synchronization

**Goal**: deliver every field event from the mesh to the cloud exactly once, including events
generated while the uplink is down. This is the flow that carries the project's research claim.
See **Figure 2**.

**Actors**: TrekLink Device, Gateway Bridge, Cloud Backend
**Precondition**: device paired to a trip; gateway running at basecamp
**Postcondition**: every event persisted exactly once, in priority order, regardless of uplink state

```mermaid
swimlane-beta TB
    subgraph device["TrekLink Device"]
        d1[Generate event:<br/>SOS, GPS, telemetry]
        d2[Broadcast over LoRa mesh]
    end
    subgraph gateway["Gateway Bridge"]
        w1[Normalize, derive eventId,<br/>assign priority tier]
        w2{Uplink up?}
        w3[Buffer in SQLite queue,<br/>flush P0 to P3 on reconnect]
        w4[Publish to MQTT]
    end
    subgraph cloud["Cloud Backend"]
        b1{eventId seen?}
        b2[Discard:<br/>idempotent no-op]
        b3[Persist, then route<br/>to MF-03 or MF-04]
    end
    d1 --> d2 --> w1 --> w2
    w2 -->|yes| w4
    w2 -->|no| w3 --> w4
    w4 --> b1
    b1 -->|yes| b2
    b1 -->|no| b3
```

***Figure 2*** — MF-02 Field Data to Offline Gateway to Cloud Synchronization. The SQLite buffer is on the no branch: events generated while the uplink is down are held and flushed in priority order. Placement: inline, 135.0 x 266.0 mm, labels at 7.50 pt.

**Priority tiers**: `P0` SOS · `P1` incident location · `P2` GPS · `P3` telemetry. All P0 events
flush before any P2 or P3 event — the ordering-compliance NFR is measured on exactly this.

**Two delivery stages, both in permanent scope** (D-005): **Stage A** uses the node's own MQTT
uplink and has no buffer; **Stage B** adds the basecamp bridge that holds the SQLite queue. Stage A
is the first increment, never a substitute — the offline NFRs are only satisfiable with Stage B.

**Main path**

1. Device generates an event and broadcasts it over the LoRa mesh.
2. Gateway receives the packet and normalizes it to the internal `TrekLinkEvent` shape.
3. Gateway derives `eventId = sha256(nodeNum : packetId)` and assigns a priority tier.
4. Uplink available → publish to MQTT. Uplink down → enqueue in SQLite by priority.
5. On reconnection, the queue flushes in strict priority order, oldest first within a tier.
6. Backend consumes, checks `eventId` against a unique index, discards duplicates as a no-op.
7. New events are persisted and routed by kind — SOS into MF-03, position into MF-04.

**Exception scenarios**

| # | Scenario | Expected behaviour |
|---|---|---|
| E02-1 | Uplink drops mid-flush | Partially flushed batch is not lost; only rows confirmed published are deleted. Flush resumes from the queue head on reconnect. |
| E02-2 | The same packet arrives twice — mesh rebroadcast or replay | Unique index on `eventId` makes the second insert a no-op. **0 duplicate Incidents across a 10× replay is a binding NFR and a demo obligation.** |
| E02-3 | Gateway process restarts with a non-empty queue | SQLite is on disk; the queue survives and flushes on next connect. Restart must not mint new `eventId`s. |
| E02-4 | Malformed or undecodable packet | Logged with the raw payload, counted, and dropped — never crashes the ingest loop, never blocks the queue head. |
| E02-5 | Queue grows beyond its configured bound during a long outage | P3 telemetry is shed first, P0 never. The shedding policy is configuration and the event is logged. |
| E02-6 | Clock skew between gateway and backend | Ordering uses queue sequence and priority, not wall-clock comparison across hosts. |

**Business rules touched**: priority-tier assignment, idempotency, flush ordering, queue retention
and shedding, reconnect backoff.

**Configurable parameters** (D-015): MQTT broker URL and topic prefix, reconnect period, flush batch
size, queue size bound, shedding policy, priority-tier mapping, sync-latency target.

**Research questions**: **RQ1** (delivery, loss and duplicate rates under intermittent connectivity)
and **RQ2** (effect of outage duration on delivery rate, sync latency, ordering compliance) are both
measured on this flow.

---

## MF-03 — SOS → Incident → Emergency Response

**Goal**: turn a device-level SOS broadcast into a structured, auditable incident that a named human
owns and closes. See **Figure 3**.

**Actors**: TrekLink Device, Gateway Bridge, Cloud Backend, Staff, Guide
**Precondition**: device in `In-Field` on an active trip
**Postcondition**: exactly one Incident per SOS episode, closed with a complete audit trail

```mermaid
swimlane-beta TB
    subgraph device["TrekLink Device"]
        d1[SOS triggered:<br/>button or fall]
        d2[Beacon position:<br/>5s, then 30s]
    end
    subgraph gateway["Gateway"]
        w1[Tag P0,<br/>deliver first]
    end
    subgraph cloud["Cloud Backend"]
        b1{Open incident<br/>in window?}
        b2[Append to episode]
        b3[Create Incident:<br/>Detected]
    end
    subgraph staff["Staff"]
        t1[Acknowledge]
        t2[In Progress, then<br/>Resolve and Close]
    end
    subgraph guide["Guide"]
        g1[Confirm situation]
        g2[Report notes]
    end
    d1 --> d2 --> w1 --> b1
    b1 -->|yes| b2
    b1 -->|no| b3
    b2 -->|WebSocket| t1
    b3 -->|WebSocket| t1
    b3 -->|WebSocket| g1
    t1 --> t2
    g1 --> g2 --> t2
```

***Figure 3*** — MF-03 SOS to Incident to Emergency Response. The decision node is what makes one SOS episode produce exactly one Incident. Placement: rotated plate, 182.0 x 215.6 mm, labels at 7.40 pt.

**Incident FSM**: `Detected → Acknowledged → In Progress → Resolved → Closed`. **Every transition
records actor, timestamp and note.** The audit trail is append-only; transitions are never silently
back-dated or overwritten.

**Two derivation paths into an Incident**

1. **Confirmed** — the SOS text discriminator arrived. High confidence.
2. **Suspected** — the discriminator was lost over RF, but position beacons arrived at SOS cadence
   rather than routine cadence. Raised at lower confidence, visually distinct in the UI, and
   dismissable with a lighter action than the full Resolved → Closed flow.

Path 2 exists because the firmware announces an SOS with exactly **one unacknowledged text frame**;
if that frame is lost, every following beacon looks like a routine position report. This is carried
as a Critical risk in the register, and is also a firmware-fix candidate under D-008.

**Exception scenarios**

| # | Scenario | Expected behaviour |
|---|---|---|
| E03-1 | The single SOS text frame is lost over RF | Cadence-anomaly detection raises a `Suspected` episode from beacon density. Staff sees it flagged as lower-confidence, not as a confirmed SOS. |
| E03-2 | One episode produces dozens of beacons | Episode correlation appends to the open Incident. **One fall produces exactly one Incident.** |
| E03-3 | Two staff acknowledge simultaneously | First write wins; the second sees the current state and the identity of the acknowledging actor. No lost update. |
| E03-4 | SOS from a device with no active trip | Incident is still created — safety events are never dropped for referential tidiness — and flagged as unassigned for triage. |
| E03-5 | Episode window expires, then the same device triggers again | A new Incident. The window boundary must not split one episode nor merge two. |
| E03-6 | Staff resolves, then new beacons arrive from the same device | Incident reopens rather than a second one being created, and the reopen is recorded in the audit trail. |
| E03-7 | WebSocket connection is down when the SOS lands | Incident is persisted regardless; the client reconciles on reconnect. Delivery of the alert never gates creation of the record. |

**Business rules touched**: idempotency, episode correlation and window, SOS confidence
classification, FSM transition legality, acknowledgement authority, audit immutability.

**Configurable parameters** (D-015): episode-correlation window, backward grace window,
cadence-anomaly threshold (N positions in window W), notification fan-out targets, auto-escalation
timeout.

**Research question**: **RQ3** — MTTA, MTTR, traceability and completion rate against an
uncoordinated baseline — is measured on this flow.

---

## MF-04 — Real-Time Trip Monitoring

**Goal**: give Staff, Admin and Guide one live operational picture of every active trip, device and
incident. See **Figure 4**.

**Actors**: TrekLink Device, Gateway Bridge, Cloud Backend, Admin, Staff, Guide
**Precondition**: at least one trip `In Progress` with devices in `In-Field`
**Postcondition**: dashboard reflects field state within the configured sync target

```mermaid
swimlane-beta TB
    subgraph device["TrekLink Device"]
        d1[GPS position<br/>and telemetry]
        d2[Broadcast<br/>over mesh]
    end
    subgraph gateway["Gateway"]
        w1[Normalize:<br/>P2 and P3]
        w2[Publish<br/>to MQTT]
    end
    subgraph cloud["Cloud Backend"]
        b1[Ingest<br/>and dedupe]
        b2[Update position<br/>and last-seen]
        b3[Emit over WebSocket,<br/>scoped by role]
    end
    subgraph ui["Monitoring Dashboard"]
        u1[MapLibre GL<br/>over Goong tiles]
        u2[Markers by status,<br/>battery, last-seen]
        u3[Incident alerts<br/>highlighted]
    end
    subgraph viewers["Admin, Staff, Guide"]
        r1[Admin: whole system<br/>Staff: operations<br/>Guide: own trip only]
    end
    d1 --> d2 --> w1 --> w2 --> b1 --> b2 --> b3 --> u1 --> u2 --> u3 --> r1
```

***Figure 4*** — MF-04 Real-Time Trip Monitoring. Role scoping is applied server-side at the WebSocket emit, not in the browser. Placement: rotated plate, 182.0 x 214.2 mm, labels at 7.61 pt.

**Role scoping is enforced server-side.** A Guide's WebSocket subscription carries only their own
trip. Filtering in the browser is not access control, and a council reviewer is entitled to test it.

**Map rendering** uses MapLibre GL JS over Goong Maps vector styles, with provider, style URL, key
and viewport held in configuration (**D-012**, **D-015**). OpenStreetMap and other global default
tile sources are prohibited: their base layers label Hoàng Sa and Trường Sa with foreign toponyms,
which makes the rendered product unlawful to publish in Vietnam.

**Exception scenarios**

| # | Scenario | Expected behaviour |
|---|---|---|
| E04-1 | Device goes silent — out of mesh range or flat battery | Marker ages into a "stale" state after the configured threshold, with last-seen shown explicitly. Never a marker frozen at an old position with no indication. |
| E04-2 | Gateway offline | A per-gateway connectivity indicator turns stale. This surfaces the NFR the register cares about — it does not belong in a tooltip. |
| E04-3 | Browser loses the WebSocket | Automatic reconnect with a state resync on reopen; a visible "reconnecting" indicator; no silent divergence. |
| E04-4 | Position arrives with an implausible jump or out-of-range coordinate | Rejected at validation, logged, and not plotted. |
| E04-5 | Guide requests a trip that is not theirs | Server-side authorization denies it; the UI never had the data. |
| E04-6 | Map provider unreachable or key rejected | Map degrades to a visible error state with markers still listed in the incident and device panels. The dashboard does not go blank. |

**Business rules touched**: staleness thresholds, role-scoped visibility, position validation,
battery-warning levels.

**Configurable parameters** (D-015): stale-device threshold, gateway-stale threshold, map provider /
style / key / default viewport and zoom, battery warning and critical levels, position sanity bounds.

---

## MF-05 — Return → Inspection → Billing → Maintenance

**Goal**: close the rental — take the device back, assess its condition, settle the money, and
return the unit to service or take it out of service. See **Figure 5**.

**Actors**: Guide, Staff, Cloud Backend, Customer
**Precondition**: trip complete; device in `In-Field` or `Returned`
**Postcondition**: rental `Closed`; payment settled; device in `Available`, `Maintenance` or `Retired`

```mermaid
swimlane-beta TB
    subgraph guide["Guide"]
        g1[Return device]
    end
    subgraph staff["Staff"]
        t1[Check in device]
        t2[Inspect]
        t3{Damage?}
        t4[Record damage<br/>and fee]
        t5[Pay and<br/>close rental]
    end
    subgraph backend["Backend"]
        s1[To Returned]
        s2[Compute charge<br/>and deposit]
        s3{Serviceable?}
        s4[To Available]
        s5[Maintenance<br/>or Retired]
    end
    subgraph customer["Customer"]
        c1[Invoice or<br/>refund]
    end
    g1 --> t1 --> s1 --> t2 --> t3
    t3 -->|yes| t4 --> s2
    t3 -->|no| s2
    s2 --> t5 --> c1
    t5 --> s3
    s3 -->|yes| s4
    s3 -->|no| s5
```

***Figure 5*** — MF-05 Return to Inspection to Billing to Maintenance. Placement: inline, 182.0 x 220.5 mm, labels at 7.73 pt.

**Device lifecycle FSM**: `Available → Reserved → Rented → In-Field → Returned → Maintenance →
Retired`, with `Maintenance → Available` as the repair path. This is one of the two UML state
machines named as a graded deliverable.

**Main path**

1. Guide returns the device; staff checks it in. Device → `Returned`.
2. Staff performs the return inspection — condition, accessories, battery.
3. Backend computes the charge: base rate + late fee + damage fee − deposit.
4. Payment processed in sandbox; customer receives invoice or deposit refund.
5. Rental → `Closed`.
6. Serviceable device → `Available`. Otherwise → `Maintenance`, and if unrepairable → `Retired`.

**Exception scenarios**

| # | Scenario | Expected behaviour |
|---|---|---|
| E05-1 | Device returned late | Late fee computed from the configured schedule, shown itemised on the invoice — never folded into an unexplained total. |
| E05-2 | Device returned damaged | Damage recorded with evidence, fee assessed against the configured schedule, device → `Maintenance`. Deposit applies before any balance is charged. |
| E05-3 | Device not returned at all | Rental stays open and escalates; device → `Retired` with a loss record after the configured grace period. |
| E05-4 | Payment fails part-way | Rental does **not** close. Balance stays outstanding and is visible to both staff and customer; no partial-settlement state is silently written. |
| E05-5 | Damage fee exceeds the deposit | Deposit is consumed and the remaining balance is invoiced. Never a negative refund. |
| E05-6 | Device fails inspection but the trip had no incident | Still → `Maintenance`; maintenance record created. Condition is independent of incident history. |
| E05-7 | Staff member who inspected also approves the fee waiver | Separation of duty — the approver must differ from the inspector above the configured threshold. |

**Business rules touched**: rental-charge calculation, late-fee schedule, damage-fee schedule,
deposit application order, refund policy, device-serviceability assessment, retirement criteria,
fee-waiver authority.

**Configurable parameters** (D-015): base rental rate, late-fee rate and grace period, damage-fee
schedule, deposit amount, non-return grace period, fee-waiver approval threshold, maintenance
turnaround target.

---

## Coverage tracking

The Mainflow Coverage Matrix is the single instrument the supervisor uses to confirm sprint progress
at the weekly Group Meeting. It is authoritative over any other progress view.

| Mainflow | Requirement | Implementation | Tested | Demo Ready | Owner |
|---|---|---|---|---|---|
| MF-01 | ☐ | ☐ | ☐ | ☐ | TanNB |
| MF-02 | ☐ | ☐ | ☐ | ☐ | KhoaDD |
| MF-03 | ☐ | ☐ | ☐ | ☐ | HoangTK |
| MF-04 | ☐ | ☐ | ☐ | ☐ | LongNN |
| MF-05 | ☐ | ☐ | ☐ | ☐ | LongLP |

**Milestones**: MF-01 and MF-02 complete by **W7**; MF-03 in progress with MF-04 and MF-05 holding
Figma plus detailed spec by **W7**; feature complete by **W11**; 100 % Implemented / Tested / Demo
Ready by **W12**, before the Faculty Council.

**Demo discipline** — the faculty handbook ranks a Main Flow breaking during the demo as the single
most common cause of failure. Every flow gets a rehearsed demo script, realistic seed data, and a
backup screen recording. Demo the real product; never build a special build to demo.
