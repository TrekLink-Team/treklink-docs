# TrekLink: The Five Main Flows

> **Source of the flow set**: `capstone/Documents/course-material/TrekLink-proposed-mainflow-ducndm.png`, supplied by
> the supervisor. These five are **binding**. The set was redrawn after Review 1 by **D-033**, which supersedes D-016; identifiers and owners are unchanged. They are the units the Mainflow
> Coverage Matrix tracks, the units demoed at each Iteration review, and the units the Faculty
> Council evaluates.
>
> **What this file is for.** It is the single source for the Main Flow material that appears in
> Report 2 §3, Report 3 (SRS), the Review 1 slide deck, and the Mainflow Coverage Matrix. Diagrams
> are Mermaid so they regenerate rather than rot, never paste a screenshot of one back into a doc.
>
> **Layout convention**: each diagram is a true Mermaid **`swimlane-beta`** diagram, one `subgraph`
> per actor lane, matching `Documents/templates/Main flows_ex02.jpg`, the actor-partitioned example
> the course supplies. `swimlane-beta` requires **Mermaid ≥ 11.16.0**; the handbook build is pinned
> to 12.0.0. Orientation is `TB` so lanes run as columns and the flow runs down the page, which is
> what fits A4 portrait. See [`01-conventions/13-diagram-and-figure-conventions.md`](../01-conventions/13-diagram-and-figure-conventions.md).
>
> **Every flow carries at least one exception scenario.** That is a W3 Definition-of-Done item and a
> named anti-fail check: *"Mỗi mainflow đều có ít nhất một exception scenario."* The scenarios below
> populate the Exception Scenario Matrix directly.

**Actors across all flows**: Guest · TrekLink Admin · TrekLink Staff · Organization Manager ·
Organization Operator · TrekLink Device · Field Station · Cloud Backend · SePay. Device holders carry
devices and use the stock Meshtastic app; they are not system users.

| MF | Name | Owner | Priority |
|---|---|---|---|
| [MF-01](#mf-01-organization-onboarding--rental-contract--handover) | Organization onboarding → Rental contract → Handover | TanNB | High |
| [MF-02](#mf-02-field-data--field-station--cloud-synchronization) | Field data → Field Station → Cloud synchronization | KhoaDD | **Highest** |
| [MF-03](#mf-03-sos--tiered-alert--escalation) | SOS → Tiered alert → Escalation | HoangTK | **Highest** |
| [MF-04](#mf-04-live-telemetry-web-map-and-organization-api) | Live telemetry: web map and organization API | LongNN | High |
| [MF-05](#mf-05-term-end--return--inspection--billing--maintenance) | Term end → Return → Inspection → Billing → Maintenance | LongLP | Medium |

**The device's life as a rented asset is the spine**: MF-01 takes it out, MF-02 to MF-04 run while
it is out, MF-05 brings it back and restocks it. Device intake and provisioning are supporting use
cases that feed MF-01. **E7 (DevOps/CI-CD) and E8 (Research & Experimental Evaluation) are
cross-cutting and deliberately are not Main Flows.** Say so whenever the Coverage Matrix is presented.

---

## MF-01: Organization onboarding → Rental contract → Handover

**Goal**: take a trekking company from self-registration to holding provisioned, monitored devices
under a signed rental contract. See **Figure 1**.

**Actors**: Organization Manager, Cloud Backend, TrekLink Staff, TrekLink Admin, SePay
**Precondition**: devices of the requested variant in `AVAILABLE`
**Postcondition**: organization `ACTIVE`; contract `ACTIVE`; devices `RENTED`, provisioned with the organization's channel key and monitored

```mermaid
swimlane-beta TB
    subgraph manager["Organization Manager"]
        m1[Self-register<br/>the organization]
        m2[Verify in person,<br/>sign master contract]
        m3[Request plan:<br/>variant, quantity, start]
        m4[Pay first amount]
        m5[Sign handover<br/>at the counter]
    end
    subgraph backend["Cloud Backend"]
        s1[Organization:<br/>Pending]
        s2{MOQ and<br/>stock?}
        s3[Contract: Approved<br/>devices Reserved]
        s4[Contract: Active<br/>devices Rented]
    end
    subgraph staff["TrekLink Staff and Admin"]
        t1[Verify identity<br/>and documents]
        t2[Admin approves:<br/>Active]
        t3[Provision devices<br/>with org channel key]
        t4[Hand over,<br/>issue Field Station]
    end
    subgraph pay["SePay"]
        p1[VietQR payment,<br/>webhook confirms]
    end
    m1 --> s1 --> m2 --> t1 --> t2 --> m3 --> s2
    s2 -->|yes| s3 --> m4 --> p1 --> t3 --> t4 --> m5 --> s4
    s2 -->|no| m3
```

***Figure 1***: MF-01 Organization onboarding to Rental contract to Handover. Lanes are actors; the flow runs top to bottom. Placement: rotated plate, 182.0 x 194.6 mm, labels at 8.25 pt.

**Main path**

1. The Manager self-registers the organization (company name, tax code, Manager, contacts); the organization is `PENDING`.
2. The Manager comes to the TrekLink counter or calls; Staff verify identity and documents and the master contract is signed.
3. An Admin approves; the organization is `ACTIVE` and the Manager can invite members and set the on-duty roster.
4. The Manager requests a plan: monthly or day plan, hardware variant, quantity, start date.
5. The backend checks the minimum order quantity and stock; Staff approve and the devices become `RESERVED`.
6. The first amount is paid: the holding fee (half the term fee) for a monthly plan, the full amount for a day plan, through SePay or recorded at the counter.
7. Staff provision each device with the organization's channel key, hand them over with the Field Station package, and the Manager signs the handover note on the spot.
8. The contract becomes `ACTIVE`, the devices `RENTED`, and monitoring starts.

**Exception scenarios**

| # | Scenario | Expected behaviour |
|---|---|---|
| E01-1 | Two contracts claim the last devices of a variant at once | Allocation is transactional with row locks on the devices; the second approval sees the shortfall and is not approved. Never over-allocate. |
| E01-2 | Requested quantity below the minimum order quantity | Rejected at request time with the current minimum shown. |
| E01-3 | Organization still `PENDING`, `REJECTED` or `SUSPENDED` requests a plan | Rejected; only an `ACTIVE` organization can open a contract. |
| E01-4 | Payment not confirmed by handover time | Handover cannot be signed; the contract stays `APPROVED` until the payment is confirmed or recorded, or Staff cancel it and the devices return to `AVAILABLE`. |
| E01-5 | A reserved device fails the provisioning check at handover | Device to `MAINTENANCE`; Staff swap in another `AVAILABLE` unit of the same variant inside the same contract; if none exists the handover is held. |
| E01-6 | SePay webhook arrives twice, or after a counter payment was recorded | The payment is matched by its reference and recorded once; a duplicate is a logged no-op. |
| E01-7 | The organization cancels after approval, before handover | Contract `CANCELLED`; reserved devices return to `AVAILABLE`; a holding fee already paid is retained. |

**Business rules touched**: organization approval, minimum order quantity, no over-allocation,
first-payment rule per plan, on-the-spot handover with signature, channel-key provisioning.

**Configurable parameters** (D-015): minimum order quantity, monthly price per variant, day-plan
lengths and premium, holding-fee ratio, reservation expiry before handover.

---

## MF-02: Field data → Field Station → Cloud synchronization

**Goal**: deliver every field event from the mesh to the cloud exactly once, including events
generated while the uplink is down. This is the flow that carries the project's research claim.
See **Figure 2**.

**Actors**: TrekLink Device, Field Station (Gateway Bridge), Cloud Backend
**Precondition**: device `RENTED` on a running contract; a node uplinks over its own Wi-Fi (Stage A) or the organization runs the Field Station (Stage C)
**Postcondition**: every event persisted exactly once, in priority order, regardless of uplink state

```mermaid
swimlane-beta TB
    subgraph device["TrekLink Device"]
        d1[Generate event:<br/>SOS, GPS, telemetry]
        d2[Broadcast over LoRa mesh]
    end
    subgraph gateway["Field Station"]
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

***Figure 2***: MF-02 Field data to Field Station to Cloud synchronization. The SQLite buffer is on the no branch: events generated while the uplink is down are held and flushed in priority order. Placement: inline, 135.0 x 266.0 mm, labels at 7.50 pt.

**Priority tiers**: `P0` SOS · `P1` incident location · `P2` GPS · `P3` telemetry. All P0 events
flush before any P2 or P3 event, the ordering-compliance NFR is measured on exactly this.

**Three delivery stages, all in permanent scope** (D-005, refined by **D-018**): **Stage A** uses
the node's own MQTT uplink and has no durable buffer; **Stage B** is the on-device durable priority
queue in the firmware, built first; **Stage C** is the **Field Station**, a bundled executable on the organization's own laptop with one of its rented nodes on a USB serial port; it holds the large SQLite queue for the whole local mesh and shows the field picture locally while offline (form per **D-033**, superseding D-020). Stage A is the first increment, never a
substitute. Stage B buffers only its own node's events, so it does not replace Stage C. Documents
written before 2026-09-17 call the basecamp bridge "Stage B"; that is Stage C.

**Main path**

1. Device generates an event and broadcasts it over the LoRa mesh.
2. Gateway receives the packet and normalizes it to the internal `TrekLinkEvent` shape.
3. Gateway derives `eventId = sha256(nodeNum : packetId)` and assigns a priority tier.
4. Uplink available → publish to MQTT. Uplink down → enqueue in SQLite by priority.
5. On reconnection, the queue flushes in strict priority order, oldest first within a tier.
6. Backend consumes, checks `eventId` against a unique index, discards duplicates as a no-op.
7. New events are persisted and routed by kind, SOS into MF-03, positions and telemetry into MF-04.

**Exception scenarios**

| # | Scenario | Expected behaviour |
|---|---|---|
| E02-1 | Uplink drops mid-flush | Partially flushed batch is not lost; only rows confirmed published are deleted. Flush resumes from the queue head on reconnect. |
| E02-2 | The same packet arrives twice, mesh rebroadcast or replay | Unique index on `eventId` makes the second insert a no-op. **0 duplicate Incidents across a 10× replay is a binding NFR and a demo obligation.** |
| E02-3 | Gateway process restarts with a non-empty queue | SQLite is on disk; the queue survives and flushes on next connect. Restart must not mint new `eventId`s. |
| E02-4 | Malformed or undecodable packet | Logged with the raw payload, counted, and dropped, never crashes the ingest loop, never blocks the queue head. |
| E02-5 | Queue grows beyond its configured bound during a long outage | P3 telemetry is shed first, P0 never. The shedding policy is configuration and the event is logged. |
| E02-6 | Clock skew between gateway and backend | The gateway flush orders by queue sequence and priority, not wall-clock comparison across hosts. The backend orders display, trails and episode correlation by the event's own timestamp when it is valid, because stock firmware drains a queued backlog one entry per reconnect. |

**Business rules touched**: priority-tier assignment, idempotency, flush ordering, queue retention
and shedding, reconnect backoff.

**Configurable parameters** (D-015): MQTT broker URL and topic prefix, reconnect period, flush batch
size, queue size bound, shedding policy, priority-tier mapping, sync-latency target.

**Research questions**: **RQ1** (delivery, loss and duplicate rates under intermittent connectivity)
and **RQ2** (effect of outage duration on delivery rate, sync latency, ordering compliance) are both
measured on this flow.

---

## MF-03: SOS → Tiered alert → Escalation

**Goal**: turn a device SOS into one incident that a named organization member owns, and make sure
that somebody is always responsible for it. See **Figure 3**. The state machine is **D-034**.

**Actors**: TrekLink Device, Field Station, Cloud Backend, Organization Operator (on duty and
backup), Organization Manager, TrekLink Staff
**Precondition**: device `RENTED`, or any device that raises an SOS
**Postcondition**: exactly one incident per SOS episode, owned at every moment, `CLOSED` with a complete audit trail

```mermaid
swimlane-beta TB
    subgraph device["TrekLink Device"]
        d1[SOS: button,<br/>gesture or fall]
    end
    subgraph cloud["Cloud Backend"]
        b1{Open incident<br/>for device?}
        b2[Append to episode]
        b3[Detected, route<br/>to organization]
        b4{Acknowledged<br/>in time?}
    end
    subgraph org["Organization on duty"]
        o1[Primary, then backup,<br/>then Manager alerted]
        o2[Acknowledge]
        o3[Report status,<br/>then outcome]
    end
    subgraph staff["TrekLink Staff"]
        t1[Escalated:<br/>review the log]
        t2[Report to<br/>authorities]
    end
    d1 --> b1
    b1 -->|yes| b2
    b1 -->|no| b3 --> o1 --> b4
    b4 -->|yes| o2 --> o3
    b4 -->|no| t1 --> t2
```

***Figure 3***: MF-03 SOS to Tiered alert to Escalation. Each tier has its own timeout; an unacknowledged alert always ends with TrekLink Staff. Placement: inline, 182.0 x 207.2 mm, labels at 7.71 pt.

**Main path**

1. The device raises an SOS; MF-02 delivers it first (P0).
2. The backend correlates it to an open episode or creates the incident and routes it, in one transaction, to the organization holding the device.
3. The on-duty member is alerted on the web, over WebSocket, by email and as an API event. Without acknowledgement within the timeout the backup is alerted, then the Manager.
4. A member acknowledges and owns the response; the organization coordinates the rescue itself, outside TrekLink.
5. The owner reports status on a cadence, then the outcome; the incident is `RESOLVED`, or `FALSE_ALARM` with a reason.
6. After the reopen window the incident is `CLOSED`.
7. If no tier acknowledges, or the response goes silent, the incident is `ESCALATED`; TrekLink Staff review the audit log and report to the authorities, recording the agency and reference.

**Exception scenarios**

| # | Scenario | Expected behaviour |
|---|---|---|
| E03-1 | The single SOS text frame is lost over RF | Cadence-anomaly detection raises a suspected episode from beacon density, flagged as lower confidence. |
| E03-2 | One episode produces dozens of beacons | Correlation appends to the open incident. One fall produces exactly one incident. |
| E03-3 | Two members acknowledge at once | Compare-and-set on state and version; the first wins, the second sees who owns it. |
| E03-4 | SOS from a device on no running contract, or the organization has no reachable member | `UNROUTED`; TrekLink Staff own it. Safety events are never dropped. |
| E03-5 | The owner stops reporting during a response | After the stale limit, `ESCALATED` with the owner kept and the Manager notified. |
| E03-6 | New SOS from the same device after `RESOLVED`, inside the reopen window | Reopens to `NOTIFY_PRIMARY`; the reopen is in the audit trail. |
| E03-7 | Alert delivery fails (WebSocket down, email bounce) | The incident and its timers proceed; delivery is retried from the outbox and logged. |
| E03-8 | The device holder cancels the SOS from the device | Recorded on the incident; the owner must confirm a false alarm. A cancel never closes an incident by itself. |
| E03-9 | The contract is overdue or the organization suspended | The incident is still created and routed. Safety first. |

**Business rules touched**: one episode one incident, tier order and timeouts, acknowledgement
authority, stale-response escalation, authority reporting by TrekLink only on escalation, audit
immutability.

**Configurable parameters** (D-015): episode window, cadence-anomaly threshold, tier timeouts,
stale-response limit, reopen window, notification channels.

**Research question**: **RQ3** (time to acknowledge, time to resolve, traceability) is measured on
this flow.

---

## MF-04: Live telemetry: web map and organization API

**Goal**: give each organization a live picture of its own rented devices, on the TrekLink web
platform or inside its own system through the API, and give TrekLink a fleet-wide view. See **Figure 4**.

**Actors**: TrekLink Device, Field Station, Cloud Backend, Organization Operator, Organization
Manager, organization's own system (API client), TrekLink Staff
**Precondition**: at least one device `RENTED`
**Postcondition**: each viewer sees only what its organization rents, within the sync-latency target

```mermaid
swimlane-beta TB
    subgraph device["TrekLink Device"]
        d1[Position, battery,<br/>telemetry]
    end
    subgraph station["Field Station"]
        f1[Local live view,<br/>also offline]
        f2[Queue and upload]
    end
    subgraph cloud["Cloud Backend"]
        b1[Ingest, dedupe,<br/>update last seen]
        b2[Scope by<br/>organization]
    end
    subgraph web["Organization web map"]
        u1[Leaflet map:<br/>devices, alerts, stale]
    end
    subgraph api["Organization system"]
        a1[REST and WebSocket<br/>with org API key]
    end
    d1 --> f1 --> f2 --> b1 --> b2
    b2 --> u1
    b2 --> a1
```

***Figure 4***: MF-04 Live telemetry to the web map and the organization API. Scoping by organization is applied on the server, at the query and at the WebSocket emit. Placement: rotated plate, 104.2 x 266.0 mm, labels at 9.45 pt.

**Main path**

1. Devices report position, battery and telemetry; MF-02 delivers them.
2. The backend updates last seen and last position and scopes every read and push to the organization holding the device.
3. Organization operators see their devices and alerts on the Leaflet map; TrekLink Staff see the whole fleet.
4. An organization's own system reads the same data over REST and subscribes over WebSocket with its organization API key.
5. Offline, the Field Station shows the local mesh directly to the operators on site.

**Exception scenarios**

| # | Scenario | Expected behaviour |
|---|---|---|
| E04-1 | Device silent: out of range or flat battery | Marker ages to stale after the threshold, last seen shown. Never a frozen marker without indication. |
| E04-2 | Field Station or uplink offline | Per-station connectivity indicator turns stale; the local view keeps working on site. |
| E04-3 | Browser or API client loses the WebSocket | Reconnect with resync from the last event cursor; a visible reconnecting indicator on the web. |
| E04-4 | An API key or user asks for another organization's device | Denied on the server; the data is never sent. |
| E04-5 | API key revoked or rate limit exceeded | 401 or 429 in the standard envelope; the key's last use is logged. |
| E04-6 | Implausible position jump | Rejected at validation, logged, not plotted. |
| E04-7 | Device returned: no longer rented by the organization | Its live data stops reaching that organization from the check-in time; history stays with TrekLink. |

**Business rules touched**: organization scoping, API key per organization, staleness thresholds,
position validation, map sovereignty overlay (D-031).

**Configurable parameters** (D-015): stale-device and stale-station thresholds, API rate limit,
map provider and viewport, battery warning levels, position sanity bounds.

---

## MF-05: Term end → Return → Inspection → Billing → Maintenance

**Goal**: end the contract, take every device back at the counter, assess it, settle the money and
restock or service the device. See **Figure 5**.

**Actors**: Organization Manager, TrekLink Staff, TrekLink Admin, Cloud Backend, SePay
**Precondition**: contract `RETURN_DUE` (day plan ended, or monthly notice given and the term ended)
**Postcondition**: contract `CLOSED`; devices `AVAILABLE`, `MAINTENANCE`, `LOST` or `RETIRED`

```mermaid
swimlane-beta TB
    subgraph manager["Organization Manager"]
        m1[Return devices<br/>at the counter]
        m2[Pay the balance]
    end
    subgraph staff["TrekLink Staff"]
        t1[Check in by<br/>asset tag]
        t2[Reset and inspect]
        t3{Damage?}
        t4[Record damage,<br/>Admin approves fee]
    end
    subgraph backend["Cloud Backend"]
        s1[Devices Returned]
        s2[Compute balance:<br/>term, late, damage, loss]
        s3{Serviceable?}
        s4[Available]
        s5[Maintenance<br/>or Retired]
        s6[Contract Closed]
    end
    m1 --> t1 --> s1 --> t2 --> t3
    t3 -->|yes| t4 --> s2
    t3 -->|no| s2
    s2 --> m2 --> s6
    t2 --> s3
    s3 -->|yes| s4
    s3 -->|no| s5
```

***Figure 5***: MF-05 Term end to Return to Inspection to Billing to Maintenance. Placement: inline, 162.0 x 266.0 mm, labels at 9.00 pt.

**Main path**

1. A day plan reaches its end date, or a monthly contract reaches the end of the term after notice; the contract is `RETURN_DUE`.
2. The Manager returns the devices at the counter; Staff check each in by asset tag; devices `RETURNED`.
3. Staff reset each device (channel key, node database, owner name) and inspect it.
4. The backend computes the balance: the second half of the term fee for a monthly plan, plus late, damage and loss charges; damage above the threshold waits for Admin approval.
5. The Manager pays through SePay or at the counter; the contract is `CLOSED` when every charge is paid and no incident is open.
6. Serviceable devices return to `AVAILABLE`; others go to `MAINTENANCE`, and to `RETIRED` if beyond repair.

**Exception scenarios**

| # | Scenario | Expected behaviour |
|---|---|---|
| E05-1 | Devices returned late | Contract `OVERDUE`; late fee per device per day after the grace period, itemized on the invoice. |
| E05-2 | Devices not returned after the grace period, or the organization stops responding | Contract `DEFAULTED`; the organization is `SUSPENDED`; the devices' last positions are tracked; Staff report to the authorities with the audit log as evidence. |
| E05-3 | Device recorded lost | Device `LOST`; loss charge at its remaining value; `RETIRED` on write-off, back to `RETURNED` if recovered. |
| E05-4 | Payment fails part-way | The contract does not close; the balance stays outstanding and visible to both sides. |
| E05-5 | Monthly term ends without notice | No return: the term's balance and the next term's holding fee fall due together, and the contract runs on. |
| E05-6 | The inspector also approves a damage waiver above the threshold | Refused: the approver must differ from the inspector. |
| E05-7 | An incident on a returned device is still open | The contract cannot close until the incident is `CLOSED` (D-034). |

**Business rules touched**: term balance, late fee, damage fee and approval, loss at remaining
value, reset before restock, separation of duty, closing conditions.

**Configurable parameters** (D-015): late fee and grace period, damage-fee schedule and approval
threshold, remaining-value schedule per variant, default threshold, maintenance turnaround target.

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

**Demo discipline**, the faculty handbook ranks a Main Flow breaking during the demo as the single
most common cause of failure. Every flow gets a rehearsed demo script, realistic seed data, and a
backup screen recording. Demo the real product; never build a special build to demo.
