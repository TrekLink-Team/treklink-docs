#!/usr/bin/env python3
"""Assemble Report 3 (SRS) Markdown and its Mermaid sources.

    python3 _handoff/tools/build_srs.py

Writes
  _handoff/outbound/capstone/Documents/reports/Report3_SRS_DRAFT.md
  _handoff/outbound/capstone/Documents/reports/assets/mermaid/srs-figN.mmd
Rendering to PNG is done by render_figures.sh.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from srs_data import FR, MF_NAMES, REL, SPEC, UC  # noqa: E402

REPO = HERE.parent.parent
OUT = REPO / "_handoff/outbound/capstone/Documents/reports"
MMD = OUT / "assets/mermaid"
CTX = REPO / "_docs/00-project-context"


def blocks(path: Path) -> list[str]:
    return re.findall(r"```mermaid\n(.*?)```", path.read_text(), re.S)


MF_SRC = blocks(CTX / "05-main-flows.md")
RF_SRC = blocks(CTX / "06-requirements-foundation.md")

FIG: dict[str, tuple[int, str]] = {}   # key -> (number, caption)
FIG_SRC: dict[int, str] = {}
FIG_SIZE: dict[int, str] = {}
FIG_PLACE: dict[int, str] = {}
PAGEBREAK = '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'


def fig(key: str, caption: str, src: str) -> int:
    n = len(FIG) + 1
    FIG[key] = (n, caption)
    FIG_SRC[n] = src.strip() + "\n"
    return n


def ref(key: str) -> str:
    return f"**Figure {FIG[key][0]}**"


def place(key: str) -> str:
    n, cap = FIG[key]
    clause = FIG_PLACE.get(n, "")
    plate = clause.startswith("Placement: full-page plate")
    body = (f"![{cap}](assets/srs-fig{n}.png){{ {FIG_SIZE.get(n, 'width=159mm')} }}\n\n"
            f"***Figure {n}***: {cap} {clause}\n")
    return (PAGEBREAK + "\n" + body + "\n" + PAGEBREAK) if plate else body


# ---------------------------------------------------------------------------
# Diagrams
# ---------------------------------------------------------------------------
CONTEXT = """flowchart LR
    GUE[Guest]
    CUS[Customer]
    OPR[Operator]
    GUI[Guide]
    ADM[Admin]
    SYS(("0<br/>TrekLink<br/>Operations<br/>Platform"))
    DEV[TrekLink<br/>Device]
    MAP[Goong<br/>Maps]
    GID[Google<br/>Identity]
    EML[Email<br/>service]
    GUE <-->|sign-up /<br/>packages| SYS
    CUS <-->|bookings /<br/>invoices| SYS
    OPR <-->|custody /<br/>alerts| SYS
    GUI <-->|acks /<br/>alerts| SYS
    ADM <-->|settings /<br/>audit| SYS
    SYS <-->|key /<br/>SOS, GPS| DEV
    SYS <-->|OAuth /<br/>identity| GID
    SYS -->|OTP,<br/>alerts| EML
    SYS <-->|requests /<br/>tiles| MAP
    style SYS stroke-width:3px
"""

ACTORS = """flowchart TB
    STF[Staff<br/>abstract]
    OPR[Operator]
    GUI[Guide]
    ADM[Admin]
    GUE[Guest]
    CUS[Customer]
    OPR -->|is a| STF
    GUI -->|is a| STF
    ADM -->|is a| STF
    ADM -.->|holds every permission of| OPR
    CUS -.->|registers from| GUE
"""

ACTOR_ID = {"Guest": "GUE", "Customer": "CUS", "Operator": "OPR", "Guide": "GUI",
            "Admin": "ADM", "Gateway Bridge": "GWB", "TrekLink Device": "DEV",
            "Scheduler": "SCH"}


def uc_diagram(ucs: list[int], extra_actor_edges: list[tuple[str, int]] = ()) -> str:
    lines = ["flowchart LR"]
    actors: dict[str, list[int]] = {}
    for u in ucs:
        for a in [x.strip() for x in UC[u][1].split(",")]:
            if a in ACTOR_ID:
                actors.setdefault(a, []).append(u)
    for a, u in extra_actor_edges:
        actors.setdefault(a, []).append(u)
    for a in actors:
        lines.append(f"    {ACTOR_ID[a]}[{a}]")
    lines.append('    subgraph SYS["TrekLink Operations Platform"]')
    for u in ucs:
        lines.append(f"        U{u}([UC-{u:02d} {UC[u][0]}])")
    lines.append("    end")
    for a, us in actors.items():
        for u in us:
            lines.append(f"    {ACTOR_ID[a]} --- U{u}")
    shown = set(ucs)
    for base, kind, tgt in REL:
        if base in shown and tgt in shown:
            if kind == "include":
                lines.append(f"    U{base} -. include .-> U{tgt}")
            else:
                lines.append(f"    U{base} -. extend .-> U{tgt}")
    return "\n".join(lines) + "\n"


UC_DIAGRAMS = [
    ("uc-mf01a", "MF-01 use cases, part 1 of 2: browsing, booking and holds.",
     [1, 2, 3, 4, 22, 27, 29, 30, 45, 55]),
    ("uc-mf01b", "MF-01 use cases, part 2 of 2: trip set-up, allocation, agreement and check-out.",
     [5, 6, 7, 8, 22, 31, 32, 33, 34, 37, 39, 43]),
    ("uc-mf02", "MF-02 use cases: ingestion, offline flush and the extension point into incident creation.",
     [13, 54, 49]),
    ("uc-mf03a", "MF-03 use cases, part 1 of 2: SOS, incident creation, manual incidents and escalation.",
     [48, 13, 49, 47, 23, 57]),
    ("uc-mf03b", "MF-03 use cases, part 2 of 2: acknowledgement, status updates, notes, reopen and dismissal.",
     [15, 23, 16, 26, 17, 46]),
    ("uc-mf04", "MF-04 use cases: live monitoring, trip start, staleness and system health.",
     [14, 35, 53, 56]),
    ("uc-mf05a", "MF-05 use cases, part 1 of 2: trip end, return, inspection and device disposition.",
     [36, 40, 9, 10, 41, 42, 58]),
    ("uc-mf05b", "MF-05 use cases, part 2 of 2: charging, fees, waiver, payment and reports.",
     [11, 24, 25, 44, 12, 50, 52]),
    ("uc-admin", "Administration and access use cases, shared across all Main Flows.",
     [21, 28, 18, 19, 20, 38, 51]),
]

ERD1 = """erDiagram
    USER ||--o{ BOOKING : places
    USER }o--o{ TRIP : guides
    TREK_PACKAGE ||--o{ TRIP : "scheduled as"
    TRIP ||--o{ BOOKING : receives
    BOOKING |o--o| RENTAL : "becomes"
    USER ||--o{ RENTAL : rents
    RENTAL }o--|{ DEVICE : allocates
    USER {
        uuid id PK
        string username UK
    }
    TREK_PACKAGE {
        uuid id PK
    }
    TRIP {
        uuid id PK
        uuid packageId FK
    }
    BOOKING {
        uuid id PK
        uuid customerId FK
        uuid tripId FK
    }
    RENTAL {
        uuid id PK
        uuid bookingId FK
        uuid customerId FK
    }
    DEVICE {
        uuid id PK
        string deviceCode UK
    }
"""

ERD2 = """erDiagram
    DEVICE ||--o{ FIELD_EVENT : emits
    FIELD_EVENT }o--o| INCIDENT : "opens or joins"
    DEVICE ||--o{ INCIDENT : raises
    TRIP |o--o{ INCIDENT : concerns
    DEVICE {
        uuid id PK
        string deviceCode UK
    }
    FIELD_EVENT {
        string eventId PK
        uuid deviceId FK
    }
    INCIDENT {
        uuid id PK
        uuid deviceId FK
        uuid tripId FK
    }
    TRIP {
        uuid id PK
    }
"""

DEVICE_FSM = """stateDiagram-v2
    [*] --> Available : register
    Available --> Reserved : allocate for next window
    Reserved --> Available : allocation released
    Reserved --> Rented : check out
    Rented --> In_Field : start trip
    In_Field --> Returned : check in
    Returned --> Available : inspection passed
    Returned --> Maintenance : inspection failed
    Available --> Maintenance : send to maintenance
    Reserved --> Maintenance : fails handover check
    Maintenance --> Available : repaired
    Maintenance --> Retired : unrepairable
    Available --> Retired : retire
    In_Field --> Retired : loss recorded
    Retired --> [*]
"""

INCIDENT_FSM = """stateDiagram-v2
    [*] --> Detected : SOS episode, cadence anomaly, or manual
    Detected --> Acknowledged : first acknowledgement
    Detected --> Closed : dismiss suspected
    Acknowledged --> In_Progress : coordination note
    In_Progress --> In_Progress : further note
    In_Progress --> Resolved : resolution note
    Resolved --> In_Progress : reopen on new beacons
    Resolved --> Closed : close
    Closed --> [*]
"""

BOOKING_FSM = """stateDiagram-v2
    [*] --> Start : open booking, hold starts
    Start --> Sent : submit
    Start --> Expired : hold lapses
    Sent --> Pending : Operator confirms
    Sent --> Rejected : Operator rejects
    Pending --> Completed : check out
    Start --> Cancelled : cancel
    Sent --> Cancelled : cancel
    Pending --> Cancelled : cancel
    Expired --> [*]
    Rejected --> [*]
    Cancelled --> [*]
    Completed --> [*]
"""

TRIP_FSM = """stateDiagram-v2
    [*] --> Draft : create or request
    Draft --> On_Prepare : start provisioning
    On_Prepare --> On_Booking : open for booking
    On_Booking --> On_Start : devices checked out
    On_Start --> Ongoing : start trip
    Ongoing --> Emergency : Operator declares
    Emergency --> Ongoing : emergency cleared
    Emergency --> Finished : end trip
    Ongoing --> Finished : end trip
    Draft --> Cancelled : cancel
    On_Prepare --> Cancelled : cancel
    On_Booking --> Cancelled : cancel
    On_Start --> Cancelled : cancel
    Finished --> [*]
    Cancelled --> [*]
"""

RENTAL_FSM = """stateDiagram-v2
    [*] --> Created : agreement generated
    Created --> Active : check out
    Active --> Returned : all devices checked in
    Active --> Escalated : non-return grace expires
    Escalated --> Returned : remaining devices checked in
    Escalated --> Closed : loss recorded and settled
    Returned --> Closed : balance settled
    Closed --> [*]
"""

_ft2 = RF_SRC[5].splitlines()
FT_GW = "\n".join(l for l in _ft2 if "F5" not in l) + "\n"
FT_MON = "\n".join(l for l in _ft2 if "F4" not in l) + "\n"

# register figures in reading order
fig("context", "Context Diagram, drawn as a Level-0 data flow diagram: the system as one process, every external entity, and the data each flow carries.", CONTEXT)
fig("actors", "Actor generalization. Operator, Guide and Admin specialize the abstract Staff actor; Admin also holds every Operator permission.", ACTORS)
for key, cap, ucs in UC_DIAGRAMS:
    extra = [("TrekLink Device", 13)] if key in ("uc-mf02",) else []
    fig(key, cap, uc_diagram(ucs, extra))
fig("ft1", "Feature Tree, part 1 of 4: Identity and Access, Device Fleet, Trip and Rental.", RF_SRC[4])
fig("ft2", "Feature Tree, part 2 of 4: Gateway and Sync.", FT_GW)
fig("ft2b", "Feature Tree, part 3 of 4: Monitoring and Incidents.", FT_MON)
fig("ft3", "Feature Tree, part 4 of 4: Billing and Administration.", RF_SRC[6])
fig("mf01", "MF-01 Booking to Rental to Trip Preparation. Lanes are actors; the flow runs top to bottom.", MF_SRC[0])
fig("mf02", "MF-02 Field Data to Offline Gateway to Cloud Synchronization. The buffer sits on the no branch: events generated while the uplink is down are held and flushed in priority order.", MF_SRC[1])
fig("mf03", "MF-03 SOS to Incident to Emergency Response. The decision node is what makes one SOS episode produce exactly one Incident.", MF_SRC[2])
fig("mf04", "MF-04 Real-Time Trip Monitoring. Role scoping is applied server-side at the WebSocket emit, not in the browser.", MF_SRC[3])
fig("mf05", "MF-05 Return to Inspection to Billing to Maintenance.", MF_SRC[4])
fig("erd1", "Conceptual ERD, part 1 of 2: accounts, packages, trips, bookings, rentals and devices, with primary, unique and foreign keys and cardinality.", ERD1)
fig("erd2", "Conceptual ERD, part 2 of 2: devices, field events, incidents and trips.", ERD2)
fig("fsm-device", "Device lifecycle state machine, seven states. The state is the device's physical condition; future commitments are Allocation records.", DEVICE_FSM)
fig("fsm-incident", "Incident lifecycle state machine, five states, with the reopen and suspected-dismissal transitions.", INCIDENT_FSM)
fig("fsm-booking", "Booking state machine.", BOOKING_FSM)
fig("fsm-trip", "Trip state machine.", TRIP_FSM)
fig("fsm-rental", "Rental state machine.", RENTAL_FSM)

# figure print sizes, written by render_figures.sh as sizes.txt when present
sizes = OUT / "assets/mermaid/sizes.txt"
if sizes.exists():
    for line in sizes.read_text().splitlines():
        if line.count("|") != 2:
            continue
        n, spec, clause = line.split("|")
        FIG_SIZE[int(n)] = spec
        FIG_PLACE[int(n)] = clause


# ---------------------------------------------------------------------------
# Generated sections
# ---------------------------------------------------------------------------
def uc_catalogue() -> str:
    rows = ["| ID | Use Case | Actors | Main Flow | Use Case Description |", "|---|---|---|---|---|"]
    for u, (name, actors, mfs, desc) in UC.items():
        mf = ", ".join(m if m != "X" else "cross-cutting" for m in mfs)
        rows.append(f"| UC-{u:02d} | {name} | {actors} | {mf} | {desc} |")
    return "\n".join(rows) + "\n"


def frs_for_uc(u: int) -> list[str]:
    return [f[0] for f in FR if u in f[2]]


def uc_specs() -> str:
    out = []
    for u, (name, actors, mfs, desc) in UC.items():
        trig, pre, post, steps, alts, brs = SPEC[u]
        mf = ", ".join(m if m != "X" else "cross-cutting" for m in mfs)
        out.append(f"###### UC-{u:02d} {name}\n")
        out.append("| Field | Content |\n|---|---|")
        out.append(f"| Actors | {actors} |")
        out.append(f"| Main Flow | {mf} |")
        out.append(f"| Description | {desc} |")
        out.append(f"| Trigger | {trig} |")
        if pre:
            out.append(f"| Precondition | {pre} |")
        if post:
            out.append(f"| Postcondition | {post} |")
        out.append("| Normal flow | " + "<br/>".join(f"{i}. {s}" for i, s in enumerate(steps, 1)) + " |")
        if alts:
            out.append("| Alternatives and exceptions | " + "<br/>".join(f"- {a}" for a in alts) + " |")
        rel = [f"{k} UC-{t:02d}" for b, k, t in REL if b == u]
        if rel:
            out.append(f"| Relationships | {', '.join(rel)} |")
        if brs:
            out.append(f"| Business rules | {', '.join(brs)} |")
        frs = frs_for_uc(u)
        if frs:
            out.append(f"| Requirements | {', '.join(frs)} |")
        out.append("")
    return "\n".join(out)


FR_GROUPS = [
    ("AUTH", "3.2", "Identity and Access", "Accounts, sessions, roles and the server-side scoping every other feature relies on."),
    ("DEV", "3.3", "Device Fleet", "Registration, the device lifecycle, allocation windows, provisioning and maintenance."),
    ("BOOK", "3.4", "Booking and Rental", "From a Customer's booking through the agreement, check-out and check-in."),
    ("TRIP", "3.5", "Trips and Packages", "The trip lifecycle, Guide assignment and the package catalogue."),
    ("EVT", "3.6", "Gateway and Synchronization", "Getting every field event to the cloud exactly once and in priority order."),
    ("INC", "3.7", "Incident Management", "Turning an SOS episode into one owned, audited incident."),
    ("MON", "3.8", "Real-Time Monitoring", "The live operational picture and its failure states."),
    ("BILL", "3.9", "Billing", "Charges, deposits, sandbox payment and invoices."),
    ("CFG", "3.10", "Configuration", "Business parameters held as configuration (D-015)."),
]


def fr_sections() -> str:
    out = []
    for prefix, num, title, blurb in FR_GROUPS:
        out.append(f"#### {num} {title}\n")
        out.append(blurb + "\n")
        out.append("| ID | Requirement (EARS) | Use Cases | Main Flow | Source |")
        out.append("|---|---|---|---|---|")
        for fid, text, ucs, mfs, src in FR:
            if fid.startswith(f"FR-{prefix}-"):
                u = ", ".join(f"UC-{x:02d}" for x in ucs)
                m = ", ".join(x if x != "X" else "cross-cutting" for x in mfs)
                out.append(f"| {fid} | {text} | {u} | {m} | {src} |")
        out.append("")
    return "\n".join(out)


def trace_matrix() -> str:
    out = ["| Main Flow | Use Case | Functional Requirements |", "|---|---|---|"]
    for mf in ["MF-01", "MF-02", "MF-03", "MF-04", "MF-05", "X"]:
        label = mf if mf != "X" else "Cross-cutting"
        for u, (name, _a, mfs, _d) in UC.items():
            if mf in mfs:
                frs = ", ".join(frs_for_uc(u)) or "covered by the including or extended use case"
                out.append(f"| {label} | UC-{u:02d} {name} | {frs} |")
    return "\n".join(out) + "\n"


def coverage_check() -> list[str]:
    problems = []
    for fid, _t, ucs, _m, _s in FR:
        for u in ucs:
            if u not in UC:
                problems.append(f"{fid} cites missing UC-{u}")
    for u in UC:
        if u not in SPEC:
            problems.append(f"UC-{u} has no specification")
    ids = [f[0] for f in FR]
    if len(ids) != len(set(ids)):
        problems.append("duplicate FR id")
    return problems


# ---------------------------------------------------------------------------
# Document
# ---------------------------------------------------------------------------
def document() -> str:
    nfr = len(FR)
    return f"""# Capstone Project Report, Report 3: Software Requirement Specification

> **Status**: **Draft for Review 1 (Week 4)**, revised 2026-09-25. This revision fills the template
> end to end except the Screens Flow and Screen Descriptions (§3.1.2, §3.1.3), which follow the
> screen design work of W5 to W7 and are written for the Final SRS at Review 2 (Week 8).
>
> **Provisional requirements.** Requirements whose source carries **(P)** rest on the leader's
> Recorded answers for modules not yet specified (clarification questions 30 to 73). They are in
> force for this document and are re-confirmed at each module's own specification interview.
>
> Structure follows the SEP490 template `Report3_Software Requirement Specification.docx`.
> Section numbers of the Review 1 draft are kept so later reports can cite them.

**Project code**: FA26SE159 · **Group code**: GFA26SE55 · **Supervisor**: Đặng Ngọc Minh Đức

---

## I. Project Report

### 1. Status Report

| Item | Status on 2026-09-25 |
|---|---|
| This document | Review 1 draft revised: {len(UC)} use cases with specifications, {nfr} functional requirements in EARS, measurable NFRs, 37 business rules, 31 exception scenarios, conceptual ERD and five state machines |
| Main Flow implementation | None of MF-01 to MF-05 is implemented. Every Implementation and Tested cell in §5.1 and §5.2 is therefore empty |
| Specifications | `gateway-sync` has requirements, design and tasks. The other modules are template stubs |
| Screens | No screen design exists yet. Screens Flow and Screen Descriptions are written at W8 |

### 2. Team Involvements

Lanes are the assigned areas of responsibility (roadmap §5.1). This table records assignment for
this document, not a claim of completed work.

| Member | Code | Main Flow owned | SRS areas assigned |
|---|---|---|---|
| Đỗ Đăng Khoa | KhoaDD | MF-02 | Overall structure and review; §3.6 Gateway and Synchronization; §4.1 External Interfaces |
| Nguyễn Bá Tân | TanNB | MF-01 | Document owner; §2 User Requirements; §3.4 Booking and Rental; §3.5 Trips; §5.2 Exception Scenarios |
| Trần Khải Hoàng | HoangTK | MF-03 | §3.7 Incident Management; incident state machine |
| Nguyễn Ngọc Long | LongNN | MF-04 | §3.8 Real-Time Monitoring; §3.1.4 Screen Authorization |
| Lâm Phi Long | LongLP | MF-05 | §3.2 Identity and Access; §3.9 Billing |

### 3. Issues/Suggestions

| # | Issue | Owner | Action |
|---|---|---|---|
| 1 | Map sovereignty acceptance test: the check was done by inspection, but no screenshots are filed. BR-24 and its test stay open | KhoaDD, LongNN | File the screenshots over Hoàng Sa and Trường Sa before Review 1 |
| 2 | Requirements marked (P) rest on Recorded answers | Module owners | Re-confirm at each module's specification interview; update this document |
| 3 | No availability target is set for the platform (§4.2.7) | KhoaDD | Decide before the Final SRS |
| 4 | Report 1 and the PMP still describe a two-stage gateway and four peer roles | KhoaDD | Align them with this document before Review 1 |

---

## II. Software Requirement Specification

### Record of Changes

| Date | A\\*<br/>M, D | In charge | Change Description |
|---|---|---|---|
| 2026-09-17 | A | Nguyễn Bá Tân | Initial draft for Review 1: overview, actors, use cases, feature tree, NFRs, business rules |
| 2026-09-25 | M | Đỗ Đăng Khoa, Nguyễn Bá Tân | Template completed: Part I; Level-0 context diagram; actor model with Guest and Staff sub-roles; use case diagrams per Main Flow; UC-27 to UC-58 added and all 58 specified; `include` corrections on UC-11 and UC-13; functional requirements in EARS (§3.2 to §3.10); screen authorization; conceptual ERD; five state machines; external interfaces corrected to the stock MQTT topics; security, availability and notification NFRs; BR-03 and BR-04 revised, BR-25 to BR-37 added; messages, glossary and traceability matrix |

\\*A - Added M - Modified D - Deleted

### 1. Product Overview

Vietnamese trekking routes such as Tà Năng to Phan Dũng, Tả Liên Sơn and Bạch Mộc Lương Tử run
through cellular dead zones lasting several days. During Summer 2026 the team built **TrekLink
firmware**, a LoRa mesh for ESP32 devices forked from Meshtastic, in four hardware variants. It
sends device-level SOS by button, gesture or IMU fall detection, followed by a position beacon, and
reports position and telemetry over the mesh. It is inherited and extended, not rebuilt.

Two operational gaps remain, and neither the firmware nor any existing product closes them.

**Field events are lost.** There is no store-and-forward path between the mesh and a backend. The
node's own uplink queue holds 16 events in RAM and discards the oldest first, so during an outage
the single SOS text frame is the first event dropped.

**A device-level SOS triggers nothing beyond a local radio alert.** There is no fleet, rental or
trip management and no structured incident workflow. Agencies coordinate emergency response by
phone and messaging app, with no audit trail, across concurrent trips.

**TrekLink Operations Platform** is a responsive web application and gateway system that closes
both. It delivers every field event from the trail to the cloud exactly once, including events
generated during connectivity loss; it turns each SOS episode into one auditable incident that a
named person owns and closes; and it manages the device fleet, rentals and trips around it.

**A system with platform seams.** TrekLink is built as a single-tenant operations **system** for
one trekking agency. What it offers beyond a single system is a set of extension seams, each
already decided:

| Seam | What it allows | Decision |
|---|---|---|
| Ingress adapters | A new field transport (node MQTT, basecamp bridge, phone app proxy) plugs in without touching ingestion | D-007 |
| Business parameters as configuration | Fees, thresholds, windows and map provider change at run time, without a release | D-015 |
| Stock Meshtastic compatibility | Any stock Meshtastic client and app keeps working with TrekLink devices | D-019 |
| Extensible Staff sub-roles | New staff roles, for example Manager, are added as data | Clarification Q33 |

**What "Smart" refers to** in the registered title: SOS and automatic fall detection, the offline
fallback with its priority queue, the append-only audit logs, and watchdogs such as staleness and
escalation checks. No AI or machine-learning component is claimed.

**Positioning.** Consumer satellite messengers (Garmin inReach, SPOT, Zoleo) solve field
communication but are closed, individual-use, and have no agency-side rental or incident layer.
Generic IoT fleet platforms (AWS IoT Core, Azure IoT Hub, Balena) have no LoRa mesh integration and
no store-and-forward design for intermittent field connectivity. IT incident tools (Jira Service
Management, PagerDuty, Opsgenie) have mature ticket lifecycles but no path from a physical SOS
broadcast to a ticket.

**Target users**: trekking agencies operating in areas without cellular coverage: their operators,
field guides, administrators and customers.

#### 1.1 Context Diagram

The system is one process. Around it are its five human actors, the TrekLink devices on the mesh,
and three external services. See {ref('context')}. The Gateway Bridge is inside the boundary: the
team builds it, and it is part of process 0. Payment is an internal sandbox module and therefore not
an external entity. Each arrow label reads "into the system / out of the system"; the table after
the figure lists every flow in full.

{place('context')}

| External entity | Flow into the system | Flow out of the system |
|---|---|---|
| Guest | Package queries, sign-up details | Package list, OTP prompt |
| Customer | Bookings, payments, cancellations, agreement signatures | Confirmations, agreement PDF, invoices, refunds |
| Operator | Confirmations, allocations, provisioning, check-out and check-in, inspections, incident actions | Booking queue, fleet state, live map, incident alerts, reports |
| Guide | Handover confirmation, trip start and end, missing-device reports, acknowledgements, notes | Assigned trips, own-trip map, incident alerts |
| Admin | Accounts and roles, business parameters, pricing, device catalogue | Audit logs, system health |
| TrekLink Device | SOS, position and telemetry packets over the mesh | Fleet channel key at provisioning |
| Google Identity | Identity assertion | OAuth request |
| Email service | (none) | OTP, password reset and incident email |
| Goong Maps | Vector tiles and style | Tile requests, from the browser |

#### 1.2 The five Main Flows

The product is built, tested and demonstrated as five Main Flows fixed with the supervisor
(D-016). Their swimlane diagrams are in §3.1.1.

| MF | Name | Owner | Priority | What it delivers |
|---|---|---|---|---|
| MF-01 | Booking → Rental → Trip Preparation | TanNB | High | A customer's booking becomes a provisioned device in a Guide's hands |
| MF-02 | Field Data → Offline Gateway → Cloud Synchronization | KhoaDD | Highest | Every field event reaches the cloud exactly once, in priority order |
| MF-03 | SOS → Incident → Emergency Response | HoangTK | Highest | One SOS episode becomes one owned, audited incident |
| MF-04 | Real-Time Trip Monitoring | LongNN | High | One live picture of trips, devices and incidents, scoped by role |
| MF-05 | Return → Inspection → Billing → Maintenance | LongLP | Medium | The rental closes, the money settles, the device returns to service or leaves it |

E7 (DevOps) and E8 (Research and Evaluation) are cross-cutting epics and are deliberately not Main
Flows.

#### 1.3 Delivery stages of MF-02

MF-02's offline guarantee is delivered in three stages, all in permanent scope (D-005, D-018,
D-020). The MF-02 swimlane (Figure {FIG['mf02'][0]}) draws the buffer in the gateway lane; the
stages below state where each buffer actually sits.

| Stage | Where the buffer is | What it covers |
|---|---|---|
| A | None: the node publishes straight to MQTT over its own Wi-Fi | The first increment. No offline guarantee |
| B | On the device: a durable, priority-ordered queue in the firmware | Survives outages and reboots for that node's own events. Built first |
| C | At basecamp: the Gateway Bridge's SQLite queue, fed by a tethered node | Aggregates the whole local mesh. Browser-first form (D-020) |

---

### 2. User Requirements

#### 2.1 Actors

| # | Actor | Type | Description | Main Flows |
|---|---|---|---|---|
| 1 | Guest | Primary, human | Anonymous visitor. Browses packages, registers | MF-01 |
| 2 | Customer | Primary, human | Books packages, pays, signs the agreement, views own history. Never returns devices directly | MF-01, MF-05 |
| 3 | Staff | Abstract, human | Generalizes Operator, Guide and Admin. Sub-roles are data and can be extended | all |
| 4 | Operator | Primary, human (Staff) | Bookings, allocation, provisioning, agreements, check-out and check-in, inspection, billing, incident coordination | MF-01, MF-03, MF-04, MF-05 |
| 5 | Guide | Primary, human (Staff) | Leads the trek, confirms handover, starts and ends the trip, collects devices, acknowledges and reports in the field. Sees only assigned trips | MF-01, MF-03, MF-04, MF-05 |
| 6 | Admin | Primary, human (Staff) | Accounts and roles, device catalogue, pricing, business parameters, audit logs, system health. Holds every Operator permission | all |
| 7 | TrekLink Device | Secondary, system | ESP32 LoRa node on inherited firmware. Emits SOS, position and telemetry | MF-02, MF-03, MF-04 |
| 8 | Gateway Bridge | Secondary, system (inside the boundary) | Normalizes mesh packets, buffers them, publishes to MQTT | MF-02, MF-03, MF-04 |
| 9 | Scheduler | Secondary, system | Time-triggered checks: hold expiry, staleness, escalation | MF-01, MF-03, MF-04, MF-05 |
| 10 | Google Identity | External system | OAuth sign-in for Customers | MF-01 |
| 11 | Email service | External system | OTP, password reset and incident email | MF-01, MF-03 |
| 12 | Goong Maps | External system | Vector tiles and styles for the live map (D-012) | MF-04 |

**Role generalization.** Operator, Guide and Admin specialize Staff. Admin is Staff with
privileges and holds every Operator permission. The Guide's reads are limited to assigned trips on
the server. See {ref('actors')}.

{place('actors')}

#### 2.2 Use Cases

##### 2.2.1 Diagram(s)

One diagram per Main Flow, with MF-01, MF-03 and MF-05 each split in two for legibility, plus one diagram for the
administration and access use cases every flow shares. See {ref('uc-mf01a')}, {ref('uc-mf01b')},
{ref('uc-mf02')}, {ref('uc-mf03a')}, {ref('uc-mf03b')}, {ref('uc-mf04')}, {ref('uc-mf05a')}, {ref('uc-mf05b')} and {ref('uc-admin')}.

{place('uc-mf01a')}
{place('uc-mf01b')}
{place('uc-mf02')}
{place('uc-mf03a')}
{place('uc-mf03b')}
{place('uc-mf04')}
{place('uc-mf05a')}
{place('uc-mf05b')}
{place('uc-admin')}

**How `include` and `extend` are used.** An included use case **always** runs as part of its base:
Submit Booking, Confirm Booking and Allocate Device always verify availability; Check Out Device
always generates the agreement, captures the signature and takes the Guide's handover
confirmation; Create Incident always sends the notification, and Acknowledge Incident always
pushes the acknowledgement to the other responders. An extending use case runs **only
when its condition holds**: Apply Late Fee when the device came back late, Apply Damage Fee when the
inspection recorded damage, Approve Fee Waiver when a waiver above the threshold is requested,
Reopen Incident when beacons arrive after resolution, and Create Incident when an ingested event is
an SOS or crosses the cadence threshold. Two relationships of the Review 1 draft were inverted and
are corrected here: Ingest Field Event no longer includes Send Notification, because most field
events notify nobody; Calculate Rental Charge no longer includes Inspect Returned Device, because
inspection is the Operator's own use case and precedes the charge. Generalization is used only
between actors.

##### 2.2.2 Descriptions

UC-01 to UC-26 keep the Review 1 numbering. UC-27 to UC-58 are added in this revision.

{uc_catalogue()}

##### 2.2.3 Use Case Specifications

Message codes (MSGnn) refer to §5.3; rule codes (BR-nn) to §5.1; exception codes (Enn-n) to §5.2.

{uc_specs()}

---

### 3. Functional Requirements

#### 3.1 System Functional Overview

The functional scope, decomposed as a feature tree in four parts for legibility. See
{ref('ft1')}, {ref('ft2')}, {ref('ft2b')} and {ref('ft3')}.

{place('ft1')}
{place('ft2')}
{place('ft2b')}
{place('ft3')}

##### 3.1.1 Main Flows

Each Main Flow is a swimlane, one lane per actor, with the flow running down the page. The lanes
say "Staff" where this document says Operator. See {ref('mf01')}, {ref('mf02')}, {ref('mf03')},
{ref('mf04')} and {ref('mf05')}.

{place('mf01')}
{place('mf02')}
{place('mf03')}
{place('mf04')}
{place('mf05')}

##### 3.1.2 Screens Flow

**Deferred to the Final SRS (Review 2, Week 8).** No screen design exists yet; a screens flow
written now would describe screens the software later contradicts.

##### 3.1.3 Screen Descriptions

**Deferred to the Final SRS (Review 2, Week 8)**, for the same reason as §3.1.2.

##### 3.1.4 Screen Authorization

Functions rather than screens, because screens are designed at W5 to W7. An **X** grants the
function; **own** limits it to the actor's own records; **assigned** limits it to trips the Guide
is assigned to. Every row is enforced on the server (FR-AUTH-01, NFR-SEC-03).

| Function | Guest | Customer | Operator | Guide | Admin |
|---|---|---|---|---|---|
| Browse packages (UC-01) | X | X | X | X | X |
| Register account (UC-27) | X | | X | X | X |
| Submit booking, reserve device (UC-02, UC-03) | | X | X | X | X |
| Cancel booking (UC-29) | | own | X | | X |
| Confirm or reject booking (UC-04) | | | X | | X |
| Manage packages (UC-31) | | | X | | X |
| Create, reschedule, cancel trip (UC-32, UC-34) | | | X | | X |
| Request trip (UC-33) | | | | X | |
| Allocate device, assign Guide (UC-05, UC-06) | | | X | | X |
| Provision channel key (UC-39) | | | X | | X |
| Generate agreement, check out, check in (UC-07, UC-08, UC-09) | | | X | | X |
| Sign agreement (UC-43) | | own | capture | capture | |
| Confirm handover, report missing device (UC-37, UC-40) | | | | assigned | |
| Start and end trip (UC-35, UC-36) | | | X | assigned | X |
| Inspect, record maintenance (UC-10, UC-41) | | | X | | X |
| Approve fee waiver (UC-44) | | | X, not the inspector | | X, not the inspector |
| Pay (UC-12) | | own | record | | record |
| View bookings, invoices (UC-45) | | own | X | | X |
| View live map (UC-14) | | | X | assigned | X |
| Acknowledge incident (UC-15) | | | X | assigned | X |
| Move incident to In Progress (UC-16) | | | X | assigned | X |
| Resolve or close incident (UC-16) | | | X | | X |
| Dismiss suspected, create manual incident (UC-46, UC-47) | | | X | | X |
| Record response note (UC-17) | | | X | assigned | X |
| Register and retire device, manage types (UC-38, UC-42, UC-51) | | | | | X |
| Manage users and roles (UC-18) | | | | | X |
| Configure parameters, pricing (UC-19, UC-50) | | | | | X |
| View audit log, system health (UC-20, UC-53) | | | | | X |
| View reports (UC-52) | | | X | | X |

##### 3.1.5 Non-Screen Functions

Functions with no user interface, driven by ingestion or by time.

| # | Feature | System Function | Description |
|---|---|---|---|
| 1 | Gateway and Sync | Event ingestion (UC-13) | Decode stock topic payloads, derive `eventId`, deduplicate, persist, route by kind |
| 2 | Gateway and Sync | Local queueing | Classify P0 to P3 and persist before any network attempt; bounded, sheds P3 first |
| 3 | Gateway and Sync | Priority-ordered flush (UC-54) | On reconnect, publish by tier then queue sequence; mark flushed on broker acknowledgement |
| 4 | Gateway and Sync | Gateway health reporting | Queue depth per tier, last sync time, oldest retry count |
| 5 | Incidents | Episode correlation (UC-49) | Append an SOS event to the open incident inside the correlation window, or create one |
| 6 | Incidents | Cadence-anomaly detection (UC-49) | Raise a `Suspected` incident when N positions arrive within window W |
| 7 | Incidents | Notification fan-out (UC-23) | WebSocket and email to the Guide and online Staff after the incident is persisted |
| 8 | Incidents | Auto-escalation (UC-57) | Re-notify when an incident stays `Detected` past the timeout |
| 9 | Monitoring | Staleness marking (UC-56) | Flag devices and gateways silent beyond their thresholds |
| 10 | Monitoring | Role-scoped push | Emit position, telemetry and incident updates only to subscribers allowed to read them |
| 11 | Booking | Hold expiry (UC-55) | Release a lapsed device hold; booking to `Expired` |
| 12 | Billing | Non-return escalation (UC-58) | Move a rental to `Escalated` after the non-return grace period |
| 13 | Billing | Invoice generation | One immutable, itemized invoice per rental once inspections complete |
| 14 | Device (firmware) | On-device durable queue (Stage B) | Hold the node's own events in priority order across outages and reboots; see §4.1.4 |

##### 3.1.6 Entity Relationship Diagram

A conceptual model of the eight core entities, in two parts that share Device and Trip. The
diagrams show keys and cardinality; the entity table lists the other attributes the requirements
depend on. The physical schema follows in the SDD. See {ref('erd1')} and {ref('erd2')}.

{place('erd1')}
{place('erd2')}

**Entities Description**

| # | Entity | Description |
|---|---|---|
| 1 | User | Any account. Username is the login key; `subRole` is Customer or a Staff sub-role (Operator, Guide, Admin, extensible); soft-deleted, `isActive` flag |
| 2 | Trek Package | A sellable route with duration, base price, device requirements and an active flag |
| 3 | Trip | A dated run of a package, with its state, guides-per-trip setting and accepted hardware versions |
| 4 | Booking | A Customer's request on a trip, with its state and device hold expiry |
| 5 | Rental | The agreement and custody record from check-out to settlement. Exists with or without a booking |
| 6 | Device | A physical TrekLink unit, with its physical state, hardware version, provisioning flag, battery and last-seen time |
| 7 | Field Event | One ingested mesh event keyed by `eventId`, with kind and priority tier |
| 8 | Incident | One SOS episode or manual report, with state, detection confidence and the timestamps behind MTTA and MTTR |

Supporting entities, not drawn: **Allocation** (device, rental and time window; resolves the
Rental to Device many-to-many), **Trip Guide** (trip to Guide assignment), **Incident Transition**
(append-only audit of incident state changes), **Device Transition**, **Damage Report**,
**Maintenance Record**, **Payment**, **Invoice**, **Pricing Rule**, **Gateway**, **Configuration
Parameter**, **Role** and **Permission**, and the authentication and synchronization audit logs.

##### 3.1.7 State Machines

Five entities have lifecycles. The device and incident machines are named graded deliverables.
See {ref('fsm-device')}, {ref('fsm-incident')}, {ref('fsm-booking')}, {ref('fsm-trip')} and
{ref('fsm-rental')}. State names with a space (`In-Field`, `In Progress`, `On Prepare`) are drawn
with an underscore.

{place('fsm-device')}

A device can be allocated to a future trip while it is still `In-Field` on the current one: the
future commitment is an Allocation record with a non-overlapping window, and the device enters
`Reserved` only when that window is next.

{place('fsm-incident')}

Detection confidence (`Confirmed`, `Suspected`) is an attribute of the incident. A late SOS text
frame upgrades a `Suspected` incident to `Confirmed` in place.

{place('fsm-booking')}
{place('fsm-trip')}
{place('fsm-rental')}

{fr_sections()}
---

### 4. Non-Functional Requirements

#### 4.1 External Interfaces

##### 4.1.1 User interfaces

| ID | Requirement |
|---|---|
| NFR-UI-01 | The web client SHALL be responsive and usable on a mobile browser, because Guides work from a phone at the trailhead |
| NFR-UI-02 | Every API response SHALL use the envelope `{{ result, isSuccess, statusCode, message }}` (D-002), and the client SHALL show `message` rather than a raw error |
| NFR-UI-03 | Sandbox payments SHALL be labelled as sandbox wherever they appear |

##### 4.1.2 Hardware interfaces

| Interface | Direction | Protocol | Notes |
|---|---|---|---|
| Device to device | Both | LoRa, Meshtastic packet format | Inherited firmware. SOS rides stock `TEXT_MESSAGE_APP` and `POSITION_APP`; no custom PortNum exists (FGT §1, §6) |
| Device to basecamp host (Stage C) | Device to host | Web Serial or Web Bluetooth, Chromium browsers only | D-020. iOS has no browser path; an iPhone Guide uses the stock Meshtastic app path |
| Device to phone app | Both | Bluetooth LE, stock Meshtastic app with MQTT proxy | Must keep working unmodified (D-019) |

##### 4.1.3 Software and communication interfaces

| Interface | Direction | Protocol | Notes |
|---|---|---|---|
| Node or Gateway Bridge to broker | Outbound | MQTT, QoS 1 | Stock topics `<root>/2/e/<channelId>/<nodeId>` (ServiceEnvelope) and `<root>/2/json/...` (JSON). The JSON envelope carries no packet priority, so the platform does not rely on it (FGT §4, D-019) |
| Broker to backend | Inbound | MQTT over TLS, per-gateway API key | At-least-once delivery; duplicates removed by `eventId` (D-021) |
| Backend to web client | Both | HTTPS REST and Socket.io WebSocket | One authenticated socket per client; subscriptions scoped by role on the server |
| Browser to map provider | Outbound | HTTPS | Goong Maps tiles and style, fetched by the browser. The key is browser-visible and restricted by referer allowlist and rate limit (D-012) |
| Backend to Google Identity | Both | OAuth 2.0 over HTTPS | Customer sign-in |
| Backend to email service | Outbound | SMTP or HTTPS API | OTP, reset and incident email |

##### 4.1.4 Interface requirements on the device firmware

The platform depends on the following behaviour of the TrekLink firmware. They are requirements on
the firmware work in scope under D-008 and D-019, specified in `treklink-firmware/specs/onboard-queue/`.

| ID | Requirement |
|---|---|
| NFR-IF-01 | The device SHALL hold its own events in a durable, priority-ordered queue that survives an uplink outage and a reboot, and SHALL shed routine telemetry before any SOS event (Stage B, D-018) |
| NFR-IF-02 | Firmware changes SHALL keep the stock publish topics and payload shapes and SHALL keep stock Meshtastic app pairing working (D-019) |
| NFR-IF-03 | Each device SHALL use the fleet's custom channel key on its primary channel, replacing the published default key (D-021) |

#### 4.2 Quality Attributes

##### 4.2.1 Reliability

| ID | Requirement |
|---|---|
| NFR-REL-01 | WHEN the uplink is available, the system SHALL deliver a field event from gateway to cloud within **5 seconds** |
| NFR-REL-02 | WHEN connectivity is restored after a loss of 30 seconds to 30 minutes, the system SHALL deliver at least **99 %** of events generated during the loss, measured over at least 20 trials per condition |
| NFR-REL-03 | WHEN the same event is delivered repeatedly, the system SHALL create **exactly one** Incident and **exactly one** notification. Verified by a 10× replay producing **0** duplicates |
| NFR-REL-04 | WHEN a queued backlog is flushed on reconnection, the system SHALL flush all P0 events before any P2 or P3 event, with at least **99 %** ordering compliance |
| NFR-REL-05 | WHILE the uplink is unavailable, queued events SHALL survive a restart of the process or device holding them: the device queue (Stage B) and the basecamp queue (Stage C) |
| NFR-REL-06 | IF a malformed packet is received, THEN the system SHALL log it, count it, and continue processing without interrupting the ingestion loop |

##### 4.2.2 Performance

| ID | Requirement |
|---|---|
| NFR-PERF-01 | The system SHALL respond to at least **95 %** of API requests within **300 ms** at 50 concurrent users |
| NFR-PERF-02 | The system SHALL accept at least **20 simultaneous** gateway submissions with **0** loss and **0** duplication |
| NFR-PERF-03 | The system SHALL support at least **50 devices** across concurrent trips without architectural change |
| NFR-PERF-04 | WHEN an incident is created, the system SHALL push its notification to connected clients within **2 seconds** under normal load (US-058) |

##### 4.2.3 Security

| ID | Requirement |
|---|---|
| NFR-SEC-01 | Every mutating endpoint SHALL require both an authenticated session and an authorization policy check |
| NFR-SEC-02 | Passwords SHALL be stored only as bcrypt hashes; plaintext SHALL never be persisted or logged, and no staff member SHALL be able to view a password |
| NFR-SEC-03 | Authorization SHALL be enforced server-side. Hiding a control in the user interface SHALL NOT be treated as access control |
| NFR-SEC-04 | The incident, device, authentication and configuration audit trails SHALL be append-only; no entry may be edited or deleted |
| NFR-SEC-05 | No credential or secret SHALL appear in source. Where a credential is necessarily exposed to the browser, it SHALL be restricted by referer allowlist and rate limit |
| NFR-SEC-06 | The broker hop SHALL be protected by TLS and a per-gateway API key (D-021) |
| NFR-SEC-07 | The fleet channel key SHALL be treated as a recovery-critical secret: never committed, never printed in a document or log, with an escrowed copy (D-021) |
| NFR-SEC-08 | Records SHALL be soft-deleted, except where hard deletion is specified for a record type (Q36, provisional) |

##### 4.2.4 Usability

| ID | Requirement |
|---|---|
| NFR-USE-01 | Any multi-step flow SHALL complete in at most **4 steps**, with at most **6 fields** per step (`06-frontend-conventions.md` §3) |
| NFR-USE-02 | Incident acknowledgement SHALL be a **single step with at most 2 fields**, because every added step adds seconds to the mean time to acknowledge (`06-frontend-conventions.md` §3) |
| NFR-USE-03 | The interface SHALL meet **WCAG 2.1 AA**: logical tab order, visible focus indication, keyboard operation of every interactive control |
| NFR-USE-04 | The interface SHALL be usable on a mobile browser |
| NFR-USE-05 | A device that has not reported recently SHALL be displayed as stale with its last-seen time, never as a marker frozen at an old position with no indication |
| NFR-USE-06 | Times SHALL be shown in the viewer's timezone, defaulting to UTC+7 (Q37, provisional) |

##### 4.2.5 Maintainability and Configurability

| ID | Requirement |
|---|---|
| NFR-CFG-01 | No business parameter SHALL appear as a literal in source. Each SHALL be configurable and SHALL be demonstrable as changeable at run time |
| NFR-CFG-02 | Every configurable parameter SHALL be registered in the Configuration Matrix with its current value, location and demonstration path |
| NFR-MNT-01 | Backend modules SHALL NOT access another module's repositories or entities directly |

##### 4.2.6 Legal and Compliance

| ID | Requirement |
|---|---|
| NFR-LEG-01 | Map imagery SHALL fully and correctly depict Vietnamese national sovereignty, including the Hoàng Sa and Trường Sa archipelagos. Publishing a map that does not is prohibited by **Nghị định 174/2026/NĐ-CP, Điều 93 khoản 3 điểm a** |
| NFR-LEG-02 | The system SHALL collect only personal data it uses operationally. Identity documents SHALL NOT be collected |
| NFR-LEG-03 | Third-party data sources SHALL be attributed: Goong Maps (IMAP JSC) for tiles, Meshtastic (GPL-3.0) for the firmware base |
| NFR-LEG-04 | The product SHALL state that it is an operations and coordination tool and does not replace official search-and-rescue channels |

##### 4.2.7 Availability

| ID | Requirement |
|---|---|
| NFR-AVL-01 | (needs check) No availability target has been set for the hosted platform. It is decided before the Final SRS; see Part I, issue 3 |
| NFR-AVL-02 | A backend or uplink outage SHALL NOT lose field events buffered on devices or at basecamp; delivery resumes on recovery (NFR-REL-02, NFR-REL-05) |

---

### 5. Requirement Appendix

#### 5.1 Business Rules

Each rule names the requirement that states it, where it is implemented and how it is tested.
Implementation has not begun, so the module column states the planned home and no rule is marked
implemented.

| BR ID | Business Rule | Requirement | Implementation | Test Case |
|---|---|---|---|---|
| BR-01 | A device may be committed to at most one booking or rental for any overlapping time window | FR-BOOK-02 | `rentals`, transactional reserve with row lock | TC-01 concurrent reserve |
| BR-02 | A booking cannot be confirmed without enough allocatable devices and an eligible Guide | FR-BOOK-04 | `rentals`, `trips` | TC-02 |
| BR-03 | Cancellation is free within the configured window after payment (default 10 minutes), with instant escrow refund; after it, the configured percentage of the rental fee (default 5 %) is retained, never a share of the trip fee (provisional) | FR-BOOK-07 | `billing`, config-driven | TC-03 |
| BR-04 | Battery level never blocks allocation or check-out. Below the advisory level (default 90 %) the system advises charging; below the warning level (default 50 %) the Operator or Guide confirms manual verification. The Guide is responsible for the manual check and for charging | FR-DEV-05 | `devices` | TC-04 |
| BR-05 | Device state transitions follow the 7-state FSM; no transition may be skipped | FR-DEV-01 | `devices`, FSM guard | TC-05 state matrix |
| BR-06 | Every field event is persisted at most once, keyed on `eventId` | FR-EVT-01 | `gateway-sync`, unique index | **TC-06 10× replay ⇒ 0 duplicates** |
| BR-07 | On reconnection, all P0 events flush before any P1, P2 or P3 | FR-EVT-03 | `gateway` queue ordering | TC-07 ordering compliance ≥99 % |
| BR-08 | An SOS episode from one device within the correlation window yields exactly one Incident | FR-EVT-05 | `incidents`, episode correlation | TC-08 beacon storm |
| BR-09 | Beacon cadence above the configured threshold raises a `Suspected` incident | FR-EVT-06 | `incidents`, cadence anomaly | TC-09 discriminator loss |
| BR-10 | Incident transitions follow the 5-state FSM; each records actor, timestamp and note | FR-INC-02 | `incidents`, FSM and audit | TC-10 |
| BR-11 | The incident audit trail is append-only; no entry may be edited or deleted | FR-INC-04 | `incidents`, DB constraint | TC-11 |
| BR-12 | Beacons after resolution reopen the Incident; beacons after closure open a new one | FR-INC-06 | `incidents` | TC-12 |
| BR-13 | A Guide may read only their assigned trips' devices, positions and incidents | FR-AUTH-03 | `auth`, CASL policy, server-side | TC-13 cross-trip access denied |
| BR-14 | Every mutating endpoint requires both a JWT guard and a policy check | FR-AUTH-01 | `auth` | TC-14 |
| BR-15 | A device silent beyond the stale threshold is displayed as stale with its last-seen time | FR-MON-03 | `monitoring` | TC-15 |
| BR-16 | Positions outside plausible bounds or with implausible jumps are rejected and logged | FR-MON-05 | `monitoring`, validation | TC-16 |
| BR-17 | Rental charge = base rate + late fee + damage fee − deposit; the deposit applies before any balance | FR-BILL-01 | `billing` | TC-17 |
| BR-18 | Late fee accrues at the configured rate after the configured grace period | FR-BILL-02 | `billing`, config-driven | TC-18 |
| BR-19 | A rental may not be closed while a payment balance is outstanding | FR-BILL-05 | `billing` | TC-19 payment failure |
| BR-20 | Damage fee above the deposit produces an invoiced balance, never a negative refund | FR-BILL-06 | `billing` | TC-20 |
| BR-21 | A fee waiver above the configured threshold must be approved by someone other than the inspector | FR-BILL-08 | `billing`, separation of duty | TC-21 |
| BR-22 | A device not returned within the configured grace period escalates the rental and, once the loss is recorded, is retired with a loss record | FR-DEV-09 | `devices`, `rentals` | TC-22 |
| BR-23 | No business parameter is a source literal; each is configurable and demonstrable | NFR-CFG-01, FR-CFG-01 | all modules and the Configuration Matrix | TC-23 live change demo |
| BR-24 | Map tiles come from a provider that correctly depicts Vietnamese sovereignty | NFR-LEG-01 | `frontend`, config-driven provider | TC-24 sovereignty screenshot check. **Open: no screenshots filed yet** |
| BR-25 | Browsing needs no account; submitting a booking does (provisional) | FR-AUTH-14 | `auth`, `trips` | TC-25 |
| BR-26 | A Customer booking reserves exactly one device; a Guide or Operator booking may hold several (provisional) | FR-BOOK-03 | `rentals` | TC-26 |
| BR-27 | A Customer's device hold lasts the configured duration (default 10 minutes); only Staff or Guide bookings may have the hold extended or disabled (provisional) | FR-BOOK-05 | `rentals`, scheduler | TC-27 hold expiry |
| BR-28 | A trip may restrict the hardware versions it accepts; every version, v1 included, is registrable (provisional) | FR-DEV-04 | `devices`, `trips` | TC-28 |
| BR-29 | One device may hold several allocations whose windows do not overlap (provisional) | FR-DEV-07 | `devices`, `rentals` | TC-29 overlap rejected |
| BR-30 | An agreement is generated from recorded data, is immutable once check-out begins, and a pricing or package change never alters a signed agreement | FR-BOOK-09, FR-BILL-11, FR-TRIP-11 | `rentals`, `billing` | TC-30 |
| BR-31 | A device must carry the fleet channel key before its first check-out, and the Guide must confirm handover | FR-DEV-13, FR-BOOK-11 | `devices`, `rentals` | TC-31 |
| BR-32 | Devices come back only through the Guide or an Operator, never from a customer directly (provisional) | FR-BOOK-13 | `rentals` | TC-32 |
| BR-33 | A device's serviceability is decided by inspection, independent of the trip's incident history; manual verification overrides telemetry | FR-DEV-10, FR-DEV-14 | `devices` | TC-33 |
| BR-34 | Payments are sandbox only; no real funds move and no card data is collected | FR-BILL-07 | `billing` | TC-34 |
| BR-35 | The username is the login key, derived by default from the email local part (provisional) | FR-AUTH-02 | `auth` | TC-35 |
| BR-36 | Staff may trigger a password reset but never view or set a password; the reset goes to the registered email only (provisional) | FR-AUTH-08 | `auth` | TC-36 |
| BR-37 | A Customer reads only their own bookings, rentals, agreements and invoices | FR-AUTH-12 | `auth`, CASL | TC-37 |

#### 5.2 Exception Scenarios

Every Main Flow carries at least one. Entries marked ✦ cover the five situations the faculty
guidance names as most often missing: payment failing part-way, two users acting simultaneously, a
user cancelling after approval, data outside plausible range, and one role attempting another
role's action. Scenarios E01-2, E01-3 and E05-3 are updated for the revised booking, device and
rental lifecycles.

| ID | Main Flow | Scenario | Expected behaviour | Requirement | Impl | Tested |
|---|---|---|---|---|---|---|
| E01-1 ✦ | MF-01 | Two customers reserve the last device at once | Row lock; loser told unavailable; never oversold | FR-BOOK-02 | ☐ | ☐ |
| E01-2 ✦ | MF-01 | Cancel after confirmation, before check-out | Booking `Cancelled`, devices released, fee per BR-03 | FR-BOOK-07 | ☐ | ☐ |
| E01-3 | MF-01 | Device fails the Guide's handover check | Handover rejected for that device, device to `Maintenance`, Operator re-allocates | FR-BOOK-12, FR-DEV-10 | ☐ | ☐ |
| E01-4 | MF-01 | No Guide available | Conflict shown before confirmation | FR-BOOK-04 | ☐ | ☐ |
| E01-5 | MF-01 | Booking window overlaps an existing allocation | Rejected, conflict identified | FR-DEV-07 | ☐ | ☐ |
| E02-1 | MF-02 | Uplink drops mid-flush | Only acknowledged rows marked flushed; resume from head | FR-EVT-04 | ☐ | ☐ |
| E02-2 | MF-02 | Duplicate packet delivery | Unique `eventId` ⇒ no-op. 10× replay ⇒ 0 duplicates | FR-EVT-01 | ☐ | ☐ |
| E02-3 | MF-02 | Gateway or device restarts with queued events | Durable queue survives; no new `eventId`s minted | FR-EVT-09, NFR-REL-05 | ☐ | ☐ |
| E02-4 | MF-02 | Malformed packet | Logged, counted, dropped; loop never crashes | FR-EVT-07 | ☐ | ☐ |
| E02-5 | MF-02 | Queue exceeds bound in a long outage | Shed P3 first, never P0; policy configurable; logged | FR-EVT-08 | ☐ | ☐ |
| E02-6 | MF-02 | Clock skew between hosts | Order by queue sequence and priority, not wall clock | FR-EVT-10 | ☐ | ☐ |
| E03-1 | MF-03 | SOS text frame lost over RF | Cadence anomaly raises `Suspected` at lower confidence | FR-EVT-06 | ☐ | ☐ |
| E03-2 | MF-03 | Dozens of beacons in one episode | Appended to the open Incident; one fall ⇒ one Incident | FR-EVT-05 | ☐ | ☐ |
| E03-3 ✦ | MF-03 | Two staff acknowledge simultaneously | First write wins; second sees current state and actor | FR-INC-05 | ☐ | ☐ |
| E03-4 | MF-03 | SOS from a device with no active trip | Incident still created, flagged unassigned | FR-INC-01 | ☐ | ☐ |
| E03-5 | MF-03 | Repeat trigger after window expiry | New Incident; the window never splits or merges an episode | FR-EVT-05 | ☐ | ☐ |
| E03-6 | MF-03 | Beacons arrive after resolution | Incident reopens to `In Progress`; reopen recorded | FR-INC-06 | ☐ | ☐ |
| E03-7 | MF-03 | WebSocket down when the SOS lands | Record persisted regardless; client reconciles on reconnect | FR-INC-11 | ☐ | ☐ |
| E04-1 | MF-04 | Device goes silent | Marker ages to stale with explicit last-seen | FR-MON-03 | ☐ | ☐ |
| E04-2 | MF-04 | Gateway offline | Per-gateway connectivity indicator turns stale, visibly | FR-MON-04 | ☐ | ☐ |
| E04-3 | MF-04 | Browser loses the WebSocket | Auto-reconnect, state resync, visible indicator | FR-MON-06 | ☐ | ☐ |
| E04-4 ✦ | MF-04 | Implausible position or coordinate jump | Rejected at validation, logged, not plotted | FR-MON-05 | ☐ | ☐ |
| E04-5 ✦ | MF-04 | Guide requests another Guide's trip | Server-side denial; data never reaches the client | FR-AUTH-03 | ☐ | ☐ |
| E04-6 | MF-04 | Map provider unreachable or key rejected | Visible error state; device and incident panels still work | FR-MON-07 | ☐ | ☐ |
| E05-1 | MF-05 | Device returned late | Late fee itemized on the invoice, never folded into a total | FR-BILL-02 | ☐ | ☐ |
| E05-2 | MF-05 | Device returned damaged | Damage recorded with evidence; deposit applied first | FR-BILL-03, FR-DEV-14 | ☐ | ☐ |
| E05-3 | MF-05 | Device never returned | Rental `Escalated` after grace; device retired with a loss record | FR-DEV-09 | ☐ | ☐ |
| E05-4 ✦ | MF-05 | Payment fails part-way | Rental stays open; balance visible; no partial state written | FR-BILL-12, FR-BILL-05 | ☐ | ☐ |
| E05-5 | MF-05 | Damage fee exceeds deposit | Deposit consumed, balance invoiced; never a negative refund | FR-BILL-06 | ☐ | ☐ |
| E05-6 | MF-05 | Fails inspection with no incident on the trip | Still to `Maintenance`; condition independent of incident history | FR-DEV-10 | ☐ | ☐ |
| E05-7 ✦ | MF-05 | Inspector also approves the fee waiver | Refused above the configured threshold | FR-BILL-08 | ☐ | ☐ |

#### 5.3 Application Messages List

Every error message says what happened and what the user can do next, and never shows a stack
trace or an internal identifier. Texts are English; the platform is not localized.

| # | Message code | Message Type | Context | Content |
|---|---|---|---|---|
| 1 | MSG01 | In line | A list or search returns nothing | *No results match your filters.* |
| 2 | MSG02 | In red, under the field | Required field empty or value out of range | *{{field}} is required.* / *{{field}} must be between {{min}} and {{max}}.* |
| 3 | MSG03 | Toast | A record is saved | *Saved.* |
| 4 | MSG04 | Toast | Booking submitted | *Booking sent. We will confirm it shortly.* |
| 5 | MSG05 | Toast | Booking confirmed, sent to the Customer | *Your booking is confirmed. Complete payment to secure it.* |
| 6 | MSG06 | Toast | Check-out complete | *Check-out complete. {{n}} devices issued to {{guide}}.* |
| 7 | MSG07 | Toast | Check-in complete | *Check-in complete. {{n}} of {{m}} devices returned.* |
| 8 | MSG08 | In red, under the field | OTP or reset token wrong, expired or used | *This code is invalid or has expired. Request a new one.* |
| 9 | MSG09 | In line | Sign-in fails | *Incorrect username or password. Please try again.* |
| 10 | MSG10 | In red, under the field | Email or device ID already registered | *{{value}} is already registered.* |
| 11 | MSG11 | Dialog | Last device taken by a concurrent booking | *That device is no longer available. Choose other dates or try again.* |
| 12 | MSG12 | Dialog | Window overlaps an existing allocation or assignment | *{{item}} is already committed from {{start}} to {{end}}.* |
| 13 | MSG13 | In line | Customer booking asks for more than one device | *Customer bookings include one device. Contact a Guide for group bookings.* |
| 14 | MSG14 | Dialog | Device hold lapsed | *Your device hold expired. Start the booking again.* |
| 15 | MSG15 | Toast | Booking cancelled | *Booking cancelled. Refund: {{amount}}. Fee retained: {{fee}}.* |
| 16 | MSG16 | Toast, to the Customer | Booking rejected | *Your booking was not accepted: {{reason}}.* |
| 17 | MSG17 | In line | Device in `Maintenance` or `Retired` | *This device cannot be allocated while it is {{state}}.* |
| 18 | MSG18 | In line | Hardware version not accepted by the trip | *This trip does not accept {{version}} devices.* |
| 19 | MSG19 | Banner, amber | Battery below the advisory level | *Battery {{pct}} %. Charge before departure.* |
| 20 | MSG20 | Dialog | Battery below the warning level | *Battery {{pct}} %. Confirm you have checked and will charge this device.* |
| 21 | MSG21 | In line | Assigning a user without the Guide sub-role | *Only Guides can be assigned to a trip.* |
| 22 | MSG22 | In line | Check-out without a paid deposit | *The deposit is not paid yet.* |
| 23 | MSG23 | In line | Check-out without a signed agreement | *The rental agreement is not signed yet.* |
| 24 | MSG24 | In line | Device not provisioned with the fleet key | *Provision this device before check-out.* |
| 25 | MSG25 | Dialog | Sandbox payment failed | *Payment failed. Nothing was charged. The balance remains due.* |
| 26 | MSG26 | Full-page notice | Action or record outside the caller's permission | *You do not have access to this.* |
| 27 | MSG27 | Toast | Incident already acknowledged by someone else | *{{actor}} acknowledged this incident at {{time}}.* |
| 28 | MSG28 | In line | Illegal state transition | *This incident cannot move from {{from}} to {{to}}.* |
| 29 | MSG29 | Dialog | Retire or delete blocked by a dependency | *This cannot be removed while it has active {{dependency}}.* |
| 30 | MSG30 | Dialog | Fee waiver approver is the inspector | *A different staff member must approve this waiver.* |
| 31 | MSG31 | Banner, red, pulsing | New incident pushed to the client | *SOS: {{device}} on {{trip}}, {{time}}.* |
| 32 | MSG32 | Banner | WebSocket reconnecting | *Reconnecting. Live data is paused.* |
| 33 | MSG33 | Panel | Map provider unreachable | *The map is unavailable. Device and incident lists are still live.* |

#### 5.4 Other Requirements

**Assumptions**

1. The demonstration fleet uses v2, v3 and v4 hardware. v1 compiles the MQTT module out at build
   time (FGT §5) and is outside the demonstration set, though registrable in the product.
2. A basecamp machine with intermittent internet hosts the Stage C gateway during field trials.
3. Physical device availability limits the scale of radio testing; simulation supplements it and
   is never presented as evidence of radio reliability.

**Constraints**

1. Fifteen weeks, five part-time members.
2. The mesh firmware is inherited. Targeted enhancement is in scope; rearchitecting the mesh stack
   is not (D-008). Firmware changes are additive and keep stock behaviour (D-019).
3. Payment is sandbox only.
4. Map data comes from a provider that satisfies NFR-LEG-01.
5. One tenant.

**Out of scope**: native mobile applications, production payment processing, route or trail
recommendation and route drawing, localization of the operations system, hardware certification,
multi-tenancy. The public landing page is a separate deliverable outside this specification.

#### 5.5 Glossary

| Term | Meaning |
|---|---|
| Allocation | A commitment of one device to one rental for a time window |
| Episode | All packets of one SOS occurrence from one device inside the correlation window |
| `eventId` | `sha256(nodeNum : packetId)`, the idempotency key of a field event (D-006) |
| EARS | Easy Approach to Requirements Syntax: WHEN, WHILE, IF THEN, WHERE and ubiquitous SHALL patterns |
| Fleet channel key | The custom pre-shared key on the devices' primary LoRa channel (D-021) |
| Gateway Bridge | The team-built software that normalizes mesh packets, queues them and publishes to MQTT |
| Main Flow (MF) | One of the five supervisor-specified end-to-end flows that organize delivery (D-016) |
| MTTA, MTTR | Mean time to acknowledge and mean time to resolve an incident, measured for RQ3 |
| P0 to P3 | Priority tiers: SOS, incident location, GPS position, telemetry |
| Provisional (P) | A requirement resting on a Recorded answer, re-confirmed at its module interview |
| Stage A, B, C | The three MF-02 delivery stages: node uplink, on-device queue, basecamp bridge (D-018) |
| Stale | A device or gateway silent beyond its configured threshold |
| Suspected incident | An incident inferred from beacon cadence because the SOS text frame was lost |

**Source codes** used in the requirement tables: US-nnn is a backlog story; Qnn is a clarification
answer of 22 September 2026; S9-Qn is a clarification answer of 25 September 2026; D-nnn is a
decision register entry; Enn-n is an exception scenario; FGT is the firmware ground truth.

#### 5.6 Traceability Matrix

Main Flow to use case to functional requirement. Use cases shared by several flows appear under
each.

{trace_matrix()}
"""


def main() -> None:
    problems = coverage_check()
    if problems:
        sys.exit("\n".join(problems))
    OUT.mkdir(parents=True, exist_ok=True)
    MMD.mkdir(parents=True, exist_ok=True)
    for n, src in FIG_SRC.items():
        (MMD / f"srs-fig{n}.mmd").write_text(src)
    (MMD / "figures.txt").write_text("".join(f"{k} {n}\n" for k, (n, _c) in FIG.items()))
    (OUT / "Report3_SRS_DRAFT.md").write_text(document())
    print(f"{len(UC)} use cases, {len(FR)} FRs, {len(FIG)} figures")


if __name__ == "__main__":
    main()
