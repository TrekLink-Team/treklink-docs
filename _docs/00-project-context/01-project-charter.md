# TrekLink — Project Charter

**Duration**: 09/2026 – 03/2027 · **Class/Specialty**: SE · **Supervisor**: Đặng Ngọc Minh Đức (Assoc. Prof)

**Team & skill matrix** (used for backlog assignment — see `03-backlog/`):

| Name | Code | MSSV | Tech Stack | Role |
|---|---|---|---|---|
| Đỗ Đăng Khoa | KhoaDD | SE192357 | Embedded C, Spring Boot, Java, ReactJS, TypeScript, **NestJS**, PostgreSQL | Leader — only member with NestJS listed; anchors backend architecture/review |
| Lâm Phi Long | LongLP | SE182769 | PostgreSQL, Node.js, ReactJS, TypeScript | Member — Gateway Bridge (Node.js) + data-heavy backend |
| Trần Khải Hoàng | HoangTK | SE182767 | Node.js, ReactJS | Member — frontend-leaning |
| Nguyễn Ngọc Long | LongNN | SE193490 | Java Spring Boot, ReactJS, TypeScript, PostgreSQL | Member — backend CRUD modules (Spring Boot → NestJS transfer) |
| Nguyễn Bá Tân | TanNB | SE183860 | PostgreSQL, MySQL, ReactJS, TypeScript | Member — reporting/DB + monitoring frontend |

> ⚠️ **Skill-gap note** (from the matrix above): NestJS is explicitly listed only for Khoa, yet it's the whole backend framework. Budget Sprint 1–2 ramp-up/pairing on NestJS module conventions (`01-conventions/05-backend-conventions.md`) for Long L.P., Hoàng, Long N.N., and Tân, mentored by Khoa — tracked as an added risk in `03-decisions-and-risk-register.md`.

> This charter reconciles `Phieu_FA26SE159.docx` (primary, authoritative — has formal RQs/NFRs/experiments) with `Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.docx` (earlier draft, same project). Differences are called out inline and logged as Decision D-000 in [`03-decisions-and-risk-register.md`](03-decisions-and-risk-register.md).

## 1. Problem

Vietnamese trekking routes (Tà Năng–Phan Dũng, Tả Liên Sơn, Bạch Mộc Lương Tử, …) run through multi-day cellular dead zones. SU26 produced **TrekLink firmware**: an open-source LoRa mesh (ESP32/ESP32-S3, forked from Meshtastic v2.7.19, ~636 files / ~149k LOC, 4 hardware variants v1–v4) with mesh messaging, GPS tracking, IMU-based fall detection, and device-level SOS broadcast — already working and **not being rebuilt**.

Two operational gaps remain, unaddressed by the firmware or by any existing product:
1. **No store-and-forward path to the cloud.** Field events generated during connectivity loss are silently lost — there is no Gateway between the mesh and a backend.
2. **No structured incident/rental operations layer.** A device-level SOS triggers nothing beyond a local mesh alert; there's no fleet, rental, or trip management; agencies coordinate by phone/WhatsApp with no audit trail.

## 2. What we're building

**TrekLink Operations Platform** — extends the inherited firmware with:
- **Gateway Bridge** (Node.js/TypeScript): LoRa-serial → SQLite priority queue (P0 SOS / P1 incident-location / P2 GPS / P3 telemetry) → MQTT → cloud, with store-and-forward and reconnection flush. *How a node actually reaches the internet (dedicated Wi-Fi/cellular hardware vs. a phone running the Meshtastic app) is still open — see Decision D-005.*
- **Idempotent event ingestion**: `eventId = DeviceID + SessionID + SequenceNumber` as the backend idempotency key — N deliveries of the same event ⇒ exactly 1 Incident + 1 notification.
- **Device Fleet & Rental Management**: 7-state device lifecycle `Available → Reserved → Rented → In-Field → Returned → Maintenance → Retired`.
- **SOS-to-Incident pipeline**: 5-state FSM `Detected → Acknowledged → In Progress → Resolved → Closed`, actor+timestamp+note on every transition, WebSocket push to Staff/Guide.
- **Real-time monitoring**: live map (Leaflet.js) of trip positions, device telemetry, gateway connectivity.
- **Trip/Booking/Billing**: packages, bookings, device reservation, check-out/check-in, deposits, damage/late fees, mock/sandbox payment.

**Explicitly out of scope**: firmware redesign, native mobile apps (responsive web only), production payment gateway, route/trail recommendation, localization, hardware certification (FCC/CE).

## 3. Actors & role summary

| Role | Core capability |
|---|---|
| **Admin** | Orgs/users/roles, device types & firmware versions, pricing config, system health, audit logs |
| **Staff** | Bookings, device allocation, rental agreements, check-out/in, fees, incident acknowledgment/coordination |
| **Guide** | Assigned trips/devices, device handover confirmation, live group view, incident ack + response notes |
| **Customer** | Browse/book packages, reserve devices, view booking/rental/payment history |

## 4. Research questions (drive the experiment plan — see roadmap)

- **RQ1**: Gateway reliability — delivery rate, data-loss rate, duplicate rate under intermittent connectivity.
- **RQ2**: Effect of connectivity-loss duration/reconnection pattern on delivery rate, sync latency, priority-ordering compliance.
- **RQ3**: SOS-to-Incident pipeline vs. uncoordinated baseline — MTTA, MTTR, traceability score, completion rate, via controlled drills.

## 5. Non-functional targets (binding — used as PR/Definition-of-Done gates)

| Property | Target |
|---|---|
| API latency | ≤300ms for 95% of requests @ 50 concurrent users |
| Gateway→cloud sync | ≤5s when uplink available |
| Offline recovery delivery rate | ≥99% after reconnection (30s–30min loss, ≥20 trials/condition) |
| Duplicate prevention | 0 duplicate Incidents for repeated `eventId` delivery (10× replay test) |
| Priority-ordering compliance | ≥99% — all P0 flushed before P2/P3 on reconnect |
| Concurrency | ≥20 simultaneous gateway submissions, 0 loss/duplication |
| Fleet scale | ≥50 devices, multiple concurrent trips, no architecture change |
| Security | JWT + RBAC + TLS + bcrypt; immutable/append-only incident & device audit logs |

## 6. Tech stack (as registered — see D-001 in decisions log, resolved)

| Layer | Technology |
|---|---|
| Embedded firmware | ESP32/ESP32-S3, C++/PlatformIO, RadioLib, Meshtastic base — **inherited, version-locked, not a new deliverable** |
| Gateway bridge | Node.js + TypeScript, SQLite (local queue), MQTT client |
| Backend | NestJS (TypeScript), REST + WebSocket (Socket.io) |
| Database | PostgreSQL. **ORM: Prisma** (resolved via D-001 — FA26SE159 form originally specified TypeORM, team's FINAL draft specified Prisma; Prisma locked as team mandate) |
| Messaging | MQTT (Mosquitto, gateway↔backend) + Socket.io (backend↔browser) |
| Frontend | React + TypeScript, role-based views, Leaflet.js map |
| Auth/AuthZ | JWT + bcrypt; RBAC — CASL (`@casl/ability`) per the FINAL draft's more specific tech table |
| DevOps | Docker / Docker Compose, GitHub Actions CI/CD |

## 7. Deliverables (map 1:1 to Jira epics and the roadmap's TP packages)

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

## 8. Related work / gap statement (condensed)

Meshtastic and consumer satellite messengers (SPOT, Garmin inReach, Zoleo) solve field comms but have no rental/fleet/incident layer. Generic IoT fleet platforms (AWS IoT Core, Azure IoT Hub, Balena) have no LoRa integration or store-and-forward for intermittent connectivity. DTN/store-and-forward research (RFC 4838, MQTT-SN) is protocol-level, not tied to a business workflow. IT incident tools (JIRA SM, PagerDuty, Opsgenie) have no IoT field-event ingestion. TrekLink is the first to combine all five dimensions in one domain-specific platform.
