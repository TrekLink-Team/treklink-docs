# TrekLink: Project Charter

> **Superseded in scope by D-033 (2026-10-03).** This charter describes the booking scope registered in September. TrekLink is now an enterprise device-rental platform built on asset management; read `03-decisions-and-risk-register.md` D-033 to D-035 first. The team, the research questions and the technical foundation below still hold.


**Project code**: FA26SE159 · **Group code**: GFA26SE55 · **Class/Specialty**: SE
**Duration**: 09/2026 – 03/2027 *(as registered, includes the retake window; the working plan ends Week 15, Dec 20 2026)* · **Supervisor**: Đặng Ngọc Minh Đức (Assoc. Prof)

**Team & skill matrix** (used for backlog and Main Flow assignment, see `03-backlog/` and
[`02-roadmap-and-milestones.md`](02-roadmap-and-milestones.md) §5.1):

| Name | Code | MSSV | Framework track | Tech stack | Lane | Main Flow |
|---|---|---|---|---|---|---|
| Đỗ Đăng Khoa | KhoaDD | SE192357 | BIT_SE_IC_19A | Embedded C, **NestJS**, Spring Boot, Java, ReactJS, TypeScript, PostgreSQL | Leader, Prisma schema, `devices`, firmware, `gateway-sync`, UI layout, architecture | **MF-02** |
| Lâm Phi Long | LongLP | SE182769 | **BIT_SE_NJS_18D** | Node.js, PostgreSQL, ReactJS, TypeScript | Delegate, `auth`, `rentals`, `billing` | **MF-05** |
| Trần Khải Hoàng | HoangTK | SE182767 | **BIT_SE_NJS_18D** | Node.js, ReactJS | `incidents`, `monitoring` ingestion, WebSocket | **MF-03** |
| Nguyễn Ngọc Long | LongNN | SE193490 | BIT_SE_IC_19A | Java Spring Boot, ReactJS, TypeScript, PostgreSQL | `frontend` (FSD), map and monitoring UI | **MF-04** |
| Nguyễn Bá Tân | TanNB | SE183860 | BIT_SE_IC_18D | PostgreSQL, MySQL, ReactJS, TypeScript | Delegate, `trips`, booking, QA & test lead | **MF-01** |

> **Skill-coverage note**, *corrected Session 6.* An earlier version of this matrix recorded NestJS
> as a skill held only by the leader, and that was wrong. **`BIT_SE_NJS_18D` is the Node.js
> enrolment track, and NestJS is a framework over Node**; LongLP and HoangTK are both on it, so
> backend capability is **3 of 5**, not 1 of 5. Core backend work is routed to them by lane.
> The residual exposure is the two IC-track members, LongNN and TanNB, picking up backend stories
> solo. Budgeted mitigation: ramp-up and pairing on
> [`01-conventions/05-backend-conventions.md`](../01-conventions/05-backend-conventions.md) across
> W2–W5, mentored by Khoa and LongLP. This is the substance of the Report 2 §2.3 Training Plan and
> is a downgraded risk in [`03-decisions-and-risk-register.md`](03-decisions-and-risk-register.md).

> **Supervisor mandate** (2026-09-13): the team sets its own scope, flows and technology stack, and
> pitches and defends the result. The supervisor's outline is guidance, not a restriction. Decisions
> that depart from the registration form are logged in the decisions register and amended into the
> form before the Week-6 scope lock.

> This charter reconciles `Phieu_FA26SE159.docx` (primary, authoritative, has formal RQs/NFRs/experiments) with `Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.docx` (earlier draft, same project). Differences are called out inline and logged as Decision D-000 in [`03-decisions-and-risk-register.md`](03-decisions-and-risk-register.md).

## 1. Problem

**Market context.** Trekking in Vietnam often takes place in remote mountainous areas (Tà Năng–Phan Dũng, Tả Liên Sơn, Bạch Mộc Lương Tử) where cellular connectivity is limited or unavailable for long stretches.

**Identified gap.** Integrated platforms combining off-grid IoT communication, monitoring, device management and structured incident coordination are not yet widely adopted in Vietnam's trekking service market.

**Project opportunity.** SU26 produced **TrekLink firmware**: a LoRa mesh (ESP32/ESP32-S3, based on the open-source Meshtastic v2.7.19, ~636 files / ~149k LOC, 4 hardware variants v1–v4) with mesh messaging, GPS tracking, IMU-based fall detection and device-level SOS, already working and **not being rebuilt**. This Capstone extends it into an integrated operational platform for the Vietnamese trekking environment (scope: D-033). Two technical requirements follow:
1. **Store-and-forward to the cloud.** Field events must survive long outages; the node's uplink queue holds 16 events in RAM, so a durable priority queue is added on the device and at the Field Station.
2. **Structured incident operations.** Each SOS becomes one incident with an owner, tiered alerts and an audit trail (D-034).

> Wording follows the Review 1 minutes (2026-10-01). The panel rejected the earlier framing that a device SOS reaches nobody and asked for comparison within Vietnam only.

## 2. What we're building

**TrekLink Operations Platform**, extends the inherited firmware with:
- **Gateway Bridge** (Node.js/TypeScript): LoRa-serial → SQLite priority queue (P0 SOS / P1 incident-location / P2 GPS / P3 telemetry) → MQTT → cloud, with store-and-forward and priority-ordered reconnection flush. Delivered in two stages, **both in permanent scope** (D-005): Stage A uses the node's own MQTT uplink; Stage B adds the basecamp bridge that holds the offline buffer. This is **MF-02**.
- **Idempotent event ingestion**: `GatewayEvent.eventId = sha256(nodeNum : packetId)` as the packet-level dedup key, plus open-Incident correlation for episode-level grouping, N deliveries of the same event ⇒ exactly 1 Incident + 1 notification. *The register's `DeviceID + SessionID + SequenceNumber` formula is not constructible from what the firmware transmits; see **D-006** and [`04-firmware-ground-truth.md`](04-firmware-ground-truth.md) §3. The intent, a natural, device-derived idempotency key, is unchanged.*
- **Device Fleet & Rental Management**: 7-state device lifecycle `Available → Reserved → Rented → In-Field → Returned → Maintenance → Retired`.
- **SOS-to-Incident pipeline**: 5-state FSM `Detected → Acknowledged → In Progress → Resolved → Closed`, actor+timestamp+note on every transition, WebSocket push to Staff/Guide. This is **MF-03**.
- **Real-time monitoring**: live map of trip positions, device telemetry and gateway connectivity, rendered with **Leaflet over OpenStreetMap** and a Vietnamese sovereignty overlay (D-031). This is **MF-04**.
- **Trip/Booking/Billing**: packages, bookings, device reservation, check-out/check-in, deposits, damage/late fees, mock/sandbox payment. **MF-01** and **MF-05**.

**Explicitly out of scope**: rearchitecting the Meshtastic mesh stack, native mobile apps (responsive web only), production payment gateway, route/trail recommendation, localization, hardware certification (FCC/CE).

> **On firmware scope**, the register's "firmware redesign is out of scope" is read narrowly
> (**D-008**, supervisor-confirmed 2026-09-13). Firmware **enhancement and integration** is in scope
> and earns graded credit: a custom PortNum, an explicit SOS discriminator, a boot `sessionId` and
> per-packet `sequenceNumber`, and beacon priority are all legitimate work. What remains excluded is
> a rearchitecture of the mesh stack itself.

## 3. Actors & role summary

| Role | Core capability |
|---|---|
| **Admin** | Orgs/users/roles, device types & firmware versions, pricing config, system health, audit logs |
| **Staff** | Bookings, device allocation, rental agreements, check-out/in, fees, incident acknowledgment/coordination |
| **Guide** | Assigned trips/devices, device handover confirmation, live group view, incident ack + response notes |
| **Customer** | Browse/book packages, reserve devices, view booking/rental/payment history |

## 4. Research questions (drive the experiment plan: see roadmap)

- **RQ1**: Gateway reliability, delivery rate, data-loss rate, duplicate rate under intermittent connectivity.
- **RQ2**: Effect of connectivity-loss duration/reconnection pattern on delivery rate, sync latency, priority-ordering compliance.
- **RQ3**: SOS-to-Incident pipeline vs. uncoordinated baseline, MTTA, MTTR, traceability score, completion rate, via controlled drills.

## 5. Non-functional targets (binding: used as PR/Definition-of-Done gates)

| Property | Target |
|---|---|
| API latency | ≤300ms for 95% of requests @ 50 concurrent users |
| Gateway→cloud sync | ≤5s when uplink available |
| Offline recovery delivery rate | ≥99% after reconnection (30s–30min loss, ≥20 trials/condition) |
| Duplicate prevention | 0 duplicate Incidents for repeated `eventId` delivery (10× replay test) |
| Priority-ordering compliance | ≥99%, all P0 flushed before P2/P3 on reconnect |
| Concurrency | ≥20 simultaneous gateway submissions, 0 loss/duplication |
| Fleet scale | ≥50 devices, multiple concurrent trips, no architecture change |
| Security | JWT + RBAC + TLS + bcrypt; immutable/append-only incident & device audit logs |

## 6. Tech stack (as registered: see D-001 in decisions log, resolved)

| Layer | Technology |
|---|---|
| Embedded firmware | ESP32/ESP32-S3, C++/PlatformIO, RadioLib, Meshtastic base, **inherited, and editable this term**. Enhancement and integration are in scope and credited (D-008); mesh-stack rearchitecture is not |
| Gateway bridge | Node.js + TypeScript, SQLite (local queue), MQTT client |
| Backend | NestJS (TypeScript), REST + WebSocket (Socket.io) |
| Database | PostgreSQL. **ORM: Prisma** (resolved via D-001, FA26SE159 form originally specified TypeORM, team's FINAL draft specified Prisma; Prisma locked as team mandate) |
| Messaging | MQTT (Mosquitto, gateway↔backend) + Socket.io (backend↔browser) |
| Frontend | React + TypeScript, role-based views, **Leaflet** map over **OpenStreetMap** tiles with a Vietnamese sovereignty overlay (D-031, provider held in configuration, not hardcoded) |
| Auth/AuthZ | JWT + bcrypt; RBAC, CASL (`@casl/ability`) per the FINAL draft's more specific tech table |
| DevOps | Docker / Docker Compose, GitHub Actions CI/CD |

## 7. Deliverables (map to Jira epics and the five Main Flows: see roadmap §4)

- TrekLink Operations Platform (web app, 4 role-based views)
- Gateway Bridge module (priority SQLite queue, idempotent MQTT sync, health reporting)
- Event Reliability Layer (eventId scheme, idempotency enforcement, sync audit log, dedup test suite)
- Device Fleet & Rental Management module
- SOS Incident Management module (FSM + WebSocket + audit trail)
- Real-Time Field Monitoring module
- Trip/Booking/Billing module
- Backend API (OpenAPI/Swagger) + WebSocket services
- Technical docs: SRS, 2 UML State Machine diagrams (Device 7-state, Incident 5-state), architecture, DB schema, API reference, test plan, deployment guide, user guide
- Evaluation report: RQ1/RQ2/RQ3 results
- Source + deployment package: gateway/backend/frontend repos, Docker Compose, CI/CD, demo environment

## 8. Legal & compliance

Short by design, but not optional, the faculty fault handbook §10 treats data, security and legal
handling as a graded topic that groups routinely arrive unprepared for.

| Area | Position |
|---|---|
| **Map sovereignty** | Vietnamese law penalises publishing a map of Vietnam that fails to fully or correctly depict national sovereignty, **Nghị định 174/2026/NĐ-CP Art. 93(3)(a)**, in force 1 Jul 2026, 30–40 M VND, with forced takedown or removal of the application. OpenStreetMap base layers label Hoàng Sa and Trường Sa with foreign toponyms. TrekLink uses OpenStreetMap under the supervisor's acceptance for the course, with an overlay that labels both archipelagos in Vietnamese, and keeps Goong Maps in configuration for any deployment beyond it (**D-031**). The overlay is checked over both archipelagos with filed screenshots (TC-24). |
| **Personal data** | Minimum-necessary collection. We store what operations require, name, contact, booking, rental and position history, and nothing else. No national ID, no document verification. Position data is operational telemetry tied to a rental, retained with the trip record. |
| **Secrets** | No API key or secret in source. The map key is unavoidably visible in the browser and is mitigated with an HTTP-referer allowlist and a per-IP rate limit; every other credential lives in environment configuration outside version control. |
| **Third-party sources** | Every third-party data source is cited: map tiles from OpenStreetMap (© OpenStreetMap contributors, ODbL); mesh firmware forked from Meshtastic (GPL-3.0) with attribution retained. |
| **Payments** | Sandbox/mock only. No real funds move, and no card data is collected, transmitted or stored. |
| **Radio** | LoRa operation on the Vietnamese licence-exempt band as configured in the inherited firmware. Hardware certification (FCC/CE) is out of scope and is not claimed. |
| **Emergency-response disclaimer** | TrekLink is an operations and coordination tool, not a certified safety-of-life system. It does not replace official search-and-rescue channels, and the user guide must say so plainly. |

## 9. Related work / gap statement (condensed)

Meshtastic, which TrekLink builds on, is designed to work independently of infrastructure; TrekLink adds the organization-side layer. Generic IoT fleet platforms (AWS IoT Core, Azure IoT Hub, Balena) have no LoRa integration or store-and-forward for intermittent connectivity. DTN/store-and-forward research (RFC 4838, MQTT-SN) is protocol-level, not tied to a business workflow. IT incident tools (JIRA SM, PagerDuty, Opsgenie) have no IoT field-event ingestion. TrekLink combines the five dimensions in one domain-specific platform. Satellite messengers are deliberately not compared (Review 1: compare within Vietnam only).
