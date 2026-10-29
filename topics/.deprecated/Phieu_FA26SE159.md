![Phieu_FA26SE159](Phieu_FA26SE159.png)

**CAPSTONE PROJECT REGISTER**

**Class**: **Duration time**: from 09/2026 To 03/2027

**(*) Profession:** Software Engineer **Specialty**: SE ![Phieu_FA26SE159](<Phieu_FA26SE159 1.png>)

**(*) Kinds of person make registers:** Lecturer ![Phieu_FA26SE159](<Phieu_FA26SE159 2.png>) Students

**1. Register information for supervisor (if have)**

| No.        | Full name          | Phone | **E-Mail**        | **Title**  |
| ---------- | ------------------ | ----- | ----------------- | ---------- |
| Supervisor | Đặng Ngọc Minh Đức |       | ducdnm2@fe.edu.vn | Giảng viên |

**2. Register information for students (if have)**

| **No.** | **Full name**    | **Student code** | **Phone** | **E-mail**                  | **Role in Group** |
| ------- | ---------------- | ---------------- | --------- | --------------------------- | ----------------- |
| 1       | Đỗ Đăng Khoa     | SE192357         |           | khoado7577@gmail.com        | Leader            |
| 2       | Trần Khải Hoàng  | SE182767         |           | HoangTKSE182767@fpt.edu.vn  | Member            |
| 3       | Lâm Phi Long     | SE182769         |           | LongLPSE182769@fpt.edu.vn   | Member            |
| 4       | Nguyễn Bá Tân    | SE183860         |           | TanNBSE183860@fpt.edu.vn    | Member            |
| 5       | Nguyễn Ngọc Long | SE193490         |           | nguyenngoclong216@gmail.com | Member            |

**3. Register content of Capstone Project**

**(*) 3.1. Capstone Project name:**

3.1.1. English: **_TrekLink — An Integrated Off-Grid Communication and Smart Device Rental Management Platform for Trekking Agencies_**

3.1.2. Vietnamese: **_TrekLink — Nền tảng tích hợp liên lạc ngoài vùng phủ sóng và quản lý cho thuê thiết bị thông minh cho doanh nghiệp trekking_**

**Abbreviation: TrekLink**

**(*) 3.2. Main proposal content (including result and product)**

**a) Context:**

Vietnam's trekking and outdoor tourism sector has grown significantly in recent years, with major routes such as Tà Năng–Phan Dũng, Tả Liên Sơn, and Bạch Mộc Lương Tử attracting thousands of participants annually. These routes traverse mountainous and forested terrain where cellular connectivity is entirely unavailable for extended stretches, sometimes spanning multiple days. Search-and-rescue operations in these zones are routinely delayed because SOS signals cannot reach coordination staff in a structured or traceable way, and because agencies lack digital tools to monitor their groups in the field.

During Summer 2026, the project team developed TrekLink, an open-source LoRa mesh communication firmware for ESP32/ESP32-S3 devices. The firmware — authored by this team and based on Meshtastic — supports multi-hop mesh messaging, GPS tracking, fall detection, and automatic SOS broadcasting. It is version-controlled and serves as the inherited technical foundation for this Capstone; it will not be rebuilt.

Although the embedded communication layer is operational, a significant gap remains between this firmware prototype and a deployable operational platform. Trekking agencies currently have no way to track which device is rented to which group, no persistent record of SOS events and their resolution, no visibility into active trip status when guides are in the field, and no structured workflow to coordinate emergency responses. Staff rely on informal channels such as phone calls or WhatsApp messages, which produce no audit trail and cannot scale across concurrent trips.

This Capstone bridges that gap by developing the software layers that transform TrekLink from a field communication tool into an integrated trekking-agency operations platform.

**Scope Boundary:** The LoRa mesh firmware and basic field-device communication developed during Summer 2026 are treated as inherited components and are not claimed as new Capstone contributions. The Capstone focuses exclusively on the Gateway Bridge, offline-resilient synchronization, cloud backend, fleet and rental management, incident management, real-time monitoring, system integration, and experimental evaluation.

The five operational gaps that drive this Capstone are:

- **No fleet or rental management:** Agencies cannot track device lifecycle, assignment, condition, or maintenance history across concurrent rentals.

- **Unreliable event delivery:** Field events generated during connectivity loss are silently discarded; no store-and-forward mechanism exists between the LoRa mesh and the cloud.

- **Uncoordinated incident response:** A device-level SOS broadcast triggers no structured workflow; acknowledgment, response actions, and resolution are undocumented and untraceable.

- **No trip or rental operations platform:** Booking, device reservation, check-out/check-in, billing, and guide assignment are handled through disconnected manual processes.

- **No field visibility:** Staff have no real-time view of active trips, device positions, or emergency events during connectivity windows.

**b) Proposed Solutions:**

TrekLink extends the existing LoRa mesh firmware into a full trekking-agency operations platform through five core capabilities:

- **Offline-Resilient Gateway:** Each field event is assigned a unique Event ID at the source (Device ID + Session ID + Sequence Number). When Internet connectivity is unavailable, the Gateway Bridge persistently stores events in a local SQLite queue. Safety-critical SOS events are assigned P0 priority and synchronized first on reconnection; GPS updates are P2 and routine telemetry P3. The Gateway automatically flushes the queue in priority order through MQTT to the cloud backend when connectivity is restored.

- **Idempotent Event Processing:** The cloud backend uses the Event ID as an idempotency key. Regardless of how many times the same event is delivered — due to retransmission, reconnection replay, or duplicate LoRa broadcast — the backend creates exactly one Incident and sends exactly one notification, preventing alert fatigue and ensuring data consistency.

- **Incident Management:** SOS events are automatically converted into operational incidents with a defined five-state lifecycle: Detected → Acknowledged → In Progress → Resolved → Closed. Each state transition is recorded with actor, timestamp, and action note, creating a complete auditable emergency response record. Staff and Guides receive real-time WebSocket notifications.

- **Fleet and Rental Management:** Each physical TrekLink device is managed through an explicit seven-state lifecycle: Available → Reserved → Rented → In-Field → Returned → Maintenance → Retired. Device assignment is linked to rental agreements and trip records, enabling agencies to track availability, usage history, damage, and maintenance across all concurrent rentals.

- **Real-Time Field Monitoring:** When gateway connectivity is available, the platform displays active trip positions, device telemetry, battery levels, and incident alerts on an operational map dashboard with live WebSocket updates.

Technology stack:

- **Embedded firmware:** ESP32/ESP32-S3 + TrekLink firmware (inherited, version-locked to Summer 2026 release)

- **Gateway bridge:** Node.js (TypeScript) — async I/O for concurrent MQTT + LoRa serial communication

- **Backend:** NestJS (TypeScript) — modular architecture with REST and WebSocket support

- **Database:** PostgreSQL — ACID compliance for rental transactions and incident audit trail

- **IoT messaging:** MQTT (Mosquitto) — QoS-based delivery between Gateway and backend

- **Real-time push:** Socket.io WebSocket — live dashboard updates

- **Frontend:** React + TypeScript — role-based views with Leaflet.js map integration

- **DevOps:** Docker Compose + GitHub Actions — containerised deployment and CI/CD

**c) Functional Requirements:**

- **Admin:**

• Manage organizations, users, roles, permissions, and system configurations.

• Manage TrekLink device types, hardware variants, firmware versions, and operational parameters.

• Manage rental pricing rules, fees, and billing configurations.

• Monitor system health, gateway connectivity, active trips, and incidents.

• View audit logs, operational statistics, and management reports.

- **Staff:**

• Manage trek packages, trips, bookings, and customer information.

• Review bookings and reserve available TrekLink devices for customer groups.

• Allocate devices and guides to confirmed trips.

• Generate rental agreements and perform device check-out/check-in.

• Record deposits, late-return fees, damage fees, and payment status.

• Monitor active trips, device telemetry, and field incidents.

• Acknowledge, coordinate, update, and close SOS incidents.

• Manage returned-device inspection and transfer devices to maintenance when required.

- **Guide:**

• View assigned trips, customer groups, and allocated devices.

• Confirm receipt and handover of TrekLink devices.

• View group positions and device status during active trips.

• Receive SOS and incident notifications via WebSocket push.

• Acknowledge incidents and record response actions.

• Submit incident notes and resolution information.

• View gateway synchronization status and pending field data.

- **Customer:**

• Browse trek packages and submit booking requests.

• Reserve TrekLink devices for a trekking group.

• View booking, rental, deposit, and payment information.

• Review assigned devices and basic usage instructions.

• View trip and rental history.

- **Device Fleet & Maintenance:**

• Register each physical TrekLink unit with device ID, hardware variant, firmware version, and status.

• Manage the complete seven-state device lifecycle: Available → Reserved → Rented → In-Field → Returned → Maintenance → Retired.

• Record battery level, last-seen time, latest GPS position, and telemetry status.

• Maintain device assignment, rental, incident, damage, and maintenance histories.

• Schedule maintenance and prevent unavailable or expired-maintenance devices from being allocated.

- **Event Reliability & Offline Synchronization:**

• Each field event shall contain a globally unique eventId (Device ID + Session ID + Sequence Number), source device ID, event type, UTC timestamp, and priority tier.

• The Gateway shall persist unsent events in a local SQLite queue when cloud connectivity is unavailable.

• SOS and safety-critical events (P0) shall receive higher synchronization priority than GPS updates (P2) and routine telemetry (P3). On reconnection, P0 events shall be delivered before any lower-priority queued events, regardless of their original arrival order.

• The Gateway shall automatically flush queued events after connectivity is restored, reporting synchronization status, retry count, and queue depth per priority tier.

• The backend shall process all incoming events idempotently using eventId as the idempotency key.

• Duplicate reception or retransmission of the same SOS event shall create exactly one Incident and one logical notification event in the backend.

• The system shall record synchronization status, retry count, and processing history for each event for diagnostic and audit purposes.

• Acceptance criterion: repeated delivery of the same SOS event (identical eventId) shall produce exactly one Incident record and one notification, regardless of delivery count.

- **Field Monitoring & Incident Management:**

• Display active trips, group positions, device status, and last-seen information on a real-time operational map.

• Create an Incident automatically when a valid SOS event is received and idempotency check passes.

• Notify responsible Staff and Guide users via WebSocket push notification within 2 seconds of incident creation.

• Support the full incident lifecycle: Detected → Acknowledged → In Progress → Resolved → Closed.

• Record actor (user ID + role), timestamp, and action note at each state transition.

• Preserve a complete, append-only incident history for audit purposes.

• Support manual incident creation by Staff for non-SOS emergencies.

- **Billing & Reporting:**

• Calculate rental charges based on device type, quantity, and rental duration.

• Generate invoices and track payment status.

• Support mock or sandbox payment integration for the Capstone scope.

• Generate reports on rentals, device utilization, maintenance, active trips, incidents, and response performance.

**d) Non-Functional Requirements:**

- **API Performance:** At least 95% of normal backend API requests shall complete within 300 ms under the defined test workload of 50 concurrent users.

- **Synchronization Latency:** When gateway uplink connectivity is available, newly received field events shall reach the cloud backend within 5 seconds under normal load conditions.

- **Offline Recovery — Delivery Rate:** The Gateway shall achieve a message delivery rate of ≥ 99% after connectivity recovery under the defined experimental conditions (connectivity-loss durations of 30 s to 30 min, minimum 20 trials per condition).

- **Offline Recovery — Testability:** Connectivity loss shall be reproducible in a controlled lab environment by programmatically interrupting the gateway's network interface, allowing repeatable experiment execution.

- **Duplicate Prevention:** Zero duplicate Incident records shall be created for repeated delivery of any SOS event carrying the same eventId. This shall be verified by a dedicated automated test that delivers the same SOS event 10 times and asserts exactly one Incident is created.

- **Priority Ordering:** On every reconnection, all P0 (SOS) events queued during the offline period shall be delivered to the backend before any P2 or P3 events. Priority-ordering compliance rate shall be ≥ 99% across all experimental trials.

- **Concurrency:** The backend shall process at least 20 simultaneous gateway event submissions without message loss or duplicate Incident creation, verified by a concurrent load test.

- **Offline Resilience:** Loss of cloud connectivity shall not interrupt local LoRa mesh communication or device-level SOS propagation on the field devices.

- **Data Consistency:** Replayed gateway messages shall not create duplicate incidents or duplicate telemetry records, enforced by eventId-keyed idempotency at the backend.

- **Security:** JWT-based authentication, RBAC, TLS-encrypted transport, bcrypt password hashing, and auditable access to sensitive trip and incident data.

- **Auditability:** Every incident state transition, device lifecycle transition, and rental lifecycle event shall be traceable to an actor (user ID + role) and a UTC timestamp.

- **Scalability:** The system shall support at least 50 TrekLink devices and multiple simultaneous active trips without architectural changes.

- **Deployability:** All server components shall support containerized deployment via Docker Compose and automated CI/CD via GitHub Actions.

**e) Theory & Practical:**

**Theory: The project applies software engineering and distributed systems principles to integrate an intermittently connected LoRa mesh network with a cloud-based operational platform.**

- **Finite State Machines:** Model the seven-state device rental lifecycle and the five-state SOS incident lifecycle (Detected → Acknowledged → In Progress → Resolved → Closed) with controlled, auditable state transitions. Each transition is an atomic, logged operation.

- **Distributed Systems and Eventual Consistency:** The Gateway and cloud backend are loosely coupled through MQTT. Field events are produced offline and delivered when connectivity permits; the backend converges to a consistent state after all queued events are processed.

- **Priority-Aware Store-and-Forward:** Classify field events by safety criticality (P0 SOS → P1 incident-related location → P2 GPS tracking → P3 routine telemetry) and enforce priority ordering during queue flush, ensuring safety-critical events are not delayed behind routine data.

- **Idempotent Event Processing:** Backend event handlers produce the same outcome regardless of delivery count, using eventId as a natural idempotency key. This decouples reliability from the transport layer and eliminates the need for exactly-once delivery guarantees at the MQTT level.

- **IoT Messaging Protocols:** MQTT QoS 1 (at-least-once) is used in conjunction with backend-side idempotency to achieve effective exactly-once processing without requiring QoS 2.

- **Event-Driven Architecture:** SOS events trigger an asynchronous processing pipeline — event ingestion → idempotency check → incident creation → role-based notification → audit logging — where each stage is decoupled and independently testable.

- **Role-Based Access Control (RBAC):** Fine-grained permissions enforced at the API layer for Admin, Staff, Guide, and Customer roles.

- **Software Architecture:** Domain-driven modular design separates gateway, devices, trips, rentals, incidents, billing, and reporting into independent NestJS modules with documented REST and WebSocket APIs.

**Practical: Inherit and version-lock the existing ESP32/ESP32-S3 LoRa mesh firmware (Summer 2026 release). Document the complete message schema — eventId structure, message types, payload format — before any gateway implementation begins.**

- Develop the Gateway Bridge (Node.js/TypeScript): LoRa-to-serial message parser, SQLite persistent priority queue, MQTT uplink publisher, reconnection flush logic, and gateway health reporter.

- Develop the NestJS backend: auth/RBAC module, device fleet module, trip and rental module, gateway sync module (idempotent event ingestion), incident module (FSM + WebSocket notifications), billing module, and reporting module. Apply PostgreSQL migrations via TypeORM.

- Develop the React/TypeScript web client: role-based views, real-time operational map (Leaflet.js), incident dashboard with WebSocket updates, rental management interface, and reporting views.

- Deploy with Docker Compose; automate testing and deployment with GitHub Actions CI/CD.

- Design and execute the experimental protocol for RQ1, RQ2, and RQ3 as specified in the Research Description section.

**f) Products (Expected Deliverables):**

- **TrekLink Operations Platform:** Integrated web application supporting Admin, Staff, Guide, and Customer workflows.

- **Gateway Bridge Module:** LoRa-to-cloud gateway with persistent SQLite priority queue (P0–P3), idempotent MQTT synchronization, reconnection flush, and health reporting. Primary new hardware-integration deliverable.

- **Event Reliability Layer:** End-to-end eventId scheme, backend idempotency enforcement, synchronization audit log, and duplicate-prevention test suite.

- **Device Fleet & Rental Management Module:** Seven-state device lifecycle, allocation, rental agreement, return, damage, and maintenance management.

- **SOS Incident Management Module:** Automatic Incident creation from SOS events, five-state FSM (Detected → Acknowledged → In Progress → Resolved → Closed), WebSocket notification, response tracking, and append-only audit history.

- **Real-Time Field Monitoring Module:** Active-trip map, device telemetry, positions, gateway connectivity status, and WebSocket-pushed alerts.

- **Trip, Booking & Billing Module:** Trek packages, bookings, device reservation, guide assignment, rental agreements, invoicing, and payment-status tracking.

- **Backend API & Real-Time Services:** REST API (OpenAPI/Swagger documented) and Socket.io WebSocket services.

- **Technical Documentation:** SRS with two UML State Machine Diagrams (Device Lifecycle — 7 states; Incident Lifecycle — 5 states), system architecture, database schema, API reference, test plan, deployment guide, and user guide.

- **Evaluation Report:** Experimental results for RQ1 (gateway delivery rate, latency, duplicate rate), RQ2 (effect of connectivity-loss duration), and RQ3 (SOS-to-Incident workflow vs. baseline).

- **Source Code & Deployment Package:** Version-controlled repositories (gateway, backend, frontend), Docker Compose configuration, GitHub Actions CI/CD, and a runnable demonstration environment.

**g) Proposed Tasks:**

- **TP1 — Requirements, Architecture & Experimental Design (Weeks 1–3):** SRS, UML State Machine Diagrams (Device Lifecycle, Incident Lifecycle), system architecture document, inherited-component analysis (firmware message schema, eventId structure), database schema design, RQ/experiment protocol design, and proof-of-concept LoRa-to-Gateway serial message parser. All subsequent TPs depend on the frozen message schema produced in TP1.

- **TP2 — Gateway Bridge & Offline Synchronization (Weeks 2–6):** LoRa-to-Gateway serial integration, SQLite persistent priority queue with P0–P3 tiers, MQTT publish logic, reconnection detection and flush routine, duplicate-prevention via eventId at gateway level, gateway health monitoring API, and unit/integration tests covering offline queue, priority ordering, and reconnection recovery.

- **TP3 — Core Backend & Reliability Services (Weeks 3–7):** NestJS authentication and RBAC module, device fleet FSM module, rental lifecycle module, idempotent event ingestion endpoint (eventId-keyed deduplication), synchronization audit log, PostgreSQL schema and migrations, and automated tests for idempotency (10× same eventId → 1 Incident) and concurrent event submission (20 simultaneous requests → 0 duplicates).

- **TP4 — Monitoring & Incident Management (Weeks 5–9):** Real-time telemetry ingestion, Leaflet.js operational map with WebSocket live updates, SOS-to-Incident processing pipeline, five-state incident FSM, role-based WebSocket notification (Staff + Guide), acknowledgment and escalation workflows, and append-only incident audit trail.

- **TP5 — Business Operations (Weeks 6–10):** Trip and booking management, device reservation and assignment, check-out/check-in workflow, rental agreement generation, billing and invoicing, Admin/Staff/Guide/Customer web views, operational dashboards, audit log views, and management reports.

- **TP6 — Integration, Experimental Evaluation & Deployment (Weeks 9–13):** Physical LoRa experiment execution (RQ1/RQ2 — 3–5 devices, connectivity-loss matrix, ≥ 20 trials per condition), offline/recovery experiment results, duplicate-event test results, concurrency/load test results, RQ3 SOS drill evaluation (randomized, ≥ 15 drills per condition, automatic timestamp recording), evaluation report, end-to-end integration test suite, Docker Compose deployment, GitHub Actions CI/CD pipeline, and final Capstone documentation.

Risk assessment:

- **Insufficient physical TrekLink devices** (Likelihood: Medium / Impact: High) — Simulate additional Gateway-to-Cloud load using MQTT scripts. Physical devices are required only for mesh-to-gateway experiments; simulation shall not be used to claim LoRa RF reliability.

- **Gateway sync latency exceeds 5-second NFR** (Likelihood: Medium / Impact: Medium) — Tune MQTT QoS level, reduce payload size, implement backpressure on the queue flush rate.

- **RQ3 baseline not objectively measurable** (Likelihood: High / Impact: Medium) — Use randomized simulation drills; independent observer triggers SOS and records timestamp; participants do not know exact trigger time in advance.

- **NestJS + MQTT + WebSocket integration underestimated** (Likelihood: Medium / Impact: High) — Proof-of-concept gateway-to-backend integration completed in TP1 Week 2; does not wait for TP3.

- **Firmware message schema incompatible with new gateway** (Likelihood: Low / Impact: High) — Schema frozen and documented in TP1 before any gateway implementation begins.

- **Scope creep** (Likelihood: High / Impact: Medium) — Feature freeze after TP5 Week 10; additional features go to post-Capstone backlog.

**3.3. Research Information**

**a. Research Problem / Research Question**

Trekking agencies operating in cellular dead zones face two unsolved problems. First, field events generated during connectivity loss — including SOS alerts — are never delivered to the cloud because no persistent store-and-forward mechanism exists between the LoRa mesh and the agency backend. Second, when an SOS event does reach staff, there is no structured workflow to coordinate the response: no automatic incident record is created, no acknowledgment is tracked, and no audit trail exists.

The existing TrekLink firmware prototype solves the field communication layer but leaves both problems unaddressed. This Capstone proposes a Gateway Bridge with priority-aware offline queuing and idempotent event processing, and an SOS-to-Incident pipeline with a formally defined lifecycle FSM, as the technical solutions to these two problems.

Three research questions operationalize the evaluation:

- **RQ1:** How reliably can the TrekLink Gateway Bridge synchronize SOS, GPS, and telemetry events from an intermittently connected LoRa mesh to the cloud backend, measured by message delivery rate, data-loss rate, and duplicate rate?

- **RQ2:** How do varying connectivity-loss durations and reconnection patterns affect message delivery rate, synchronization latency, and priority-ordering compliance of the proposed Gateway architecture?

- **RQ3:** Compared with the existing uncoordinated device-level SOS workflow, to what extent does the TrekLink SOS-to-Incident pipeline improve incident response coordination, traceability, and acknowledgment consistency, as measured by MTTA, MTTR, traceability score, and incident-completion rate in controlled emergency drills?

RQ1 and RQ2 directly evaluate the Event Reliability & Offline Synchronization functional requirements. RQ3 directly evaluates the Incident Management functional requirements and the five-state incident FSM. All three RQs trace back to specific functional requirements, system modules, task packages, and experiment conditions defined in this proposal.

**Baseline definition for RQ3:** In the existing workflow, a TrekLink device triggers an SOS broadcast across the LoRa mesh. If a guide's Meshtastic-paired phone receives the alert, the guide contacts staff by voice call or messaging application. There is no structured acknowledgment, no timestamp recording, no response-action log, and no audit trail. Baseline MTTA is the elapsed time from SOS device trigger to the first documented verbal or text acknowledgment, recorded by an independent observer. Baseline traceability score is 0% by definition (no audit record exists). A reduction in MTTA is not assumed in advance; outcomes will be reported as measured.

**b. Research Objectives**

- Design and implement a priority-aware, offline-resilient Gateway Bridge with end-to-end idempotent event processing connecting the TrekLink LoRa mesh to a cloud backend.

- Evaluate gateway synchronization reliability under a controlled matrix of connectivity-loss durations and reconnection patterns, using physical TrekLink hardware for all mesh-to-gateway measurements.

- Design and implement an SOS-to-Incident pipeline with a formally defined five-state FSM, role-based WebSocket notification, and append-only audit trail.

- Evaluate incident-response workflow efficiency using MTTA, MTTR, traceability score, and incident-completion rate in randomized controlled emergency drills, compared with the uncoordinated baseline.

- Integrate the evaluated gateway and incident mechanisms into a complete trekking-agency platform covering fleet management, rental operations, real-time monitoring, and billing.

**c. Research Scope & Methodology**

In scope: TrekLink ESP32/ESP32-S3 devices and LoRa mesh (Summer 2026 firmware, version-locked); Gateway Bridge — LoRa-to-MQTT-to-cloud synchronization with priority queue and idempotency; SOS, GPS, and selected telemetry message types; connectivity-loss/recovery experiments in a controlled lab environment; SOS-to-Incident workflow evaluation using controlled drills; device fleet, rental, and trip-management modules; responsive web client (desktop/tablet); mock/sandbox payment only.

Out of scope: Firmware redesign, native mobile apps, commercial payment, hardware radio certification.

Methodology:

- **Literature Review:** Survey LoRa mesh systems, store-and-forward and DTN protocols, IoT fleet management, and emergency incident workflows. Identify and articulate the integration gap.

- **Architecture & Design:** Freeze firmware message schema and eventId structure. Design gateway synchronization architecture, SQLite priority queue schema, idempotency table, incident FSM, and experiment protocol. Produce SRS, UML State Machine Diagrams, architecture diagrams, and sequence diagrams.

- **Implementation:** Develop gateway bridge, backend modules, and web client per TP1–TP5.

- **Experiment 1 — Gateway Synchronization (RQ1 & RQ2):** Use 3–5 physical TrekLink devices for all mesh-to-gateway reliability measurements. MQTT simulation scripts may supplement Gateway-to-Cloud workload evaluation only — not used to claim LoRa RF reliability. Apply connectivity-loss matrix: 0 s (control), 30 s, 2 min, 5 min, 10 min, 30 min; two reconnection patterns (immediate and delayed 60 s). Minimum 20 trials per condition. Measures: delivery rate (%), data-loss rate (%), duplicate rate (%), sync latency (mean / median / P95 in seconds), queue-recovery time (s), priority-ordering compliance rate (%).

- **Experiment 2 — SOS-to-Incident Workflow (RQ3):** Controlled emergency drills with 1 TrekLink device, 1 gateway, 1 Staff account, 1 Guide account, minimum 3 participants rotating. Scenario order randomized; participants do not know exact SOS trigger time; independent observer triggers SOS and starts external timer. All TrekLink-condition timestamps recorded automatically by the backend; baseline timestamps recorded by independent observer (hardware stopwatch). 15–20 drills per condition; vary network latency (LAN and 4G hotspot). Measures: MTTA (mean / median / P95 in seconds), MTTR (mean / median in minutes), traceability score (% of FSM transitions with complete actor + timestamp + action), missed-alert rate (%), duplicate-alert rate (%), incident-completion rate (%).

- **Integration & System Testing:** End-to-end test cases for all functional requirements, idempotency tests (10× same eventId → 1 Incident), concurrency tests (20 simultaneous events → 0 duplicates), RBAC validation, and audit-log completeness check.

**d. Expected Scientific Contribution**

- **A priority-aware, offline-resilient gateway pattern** for connecting intermittently connected LoRa mesh devices to cloud-based operational systems, with a formally defined eventId scheme, SQLite persistence model, and idempotent backend processing.

- **Empirical benchmark** of gateway synchronization reliability and latency under a controlled connectivity-loss matrix on low-cost ESP32 hardware.

- **An SOS-to-Incident workflow design** with a formally specified five-state FSM, role-based notification chain, and append-only audit trail, directly traceable to measurable research outcomes.

- **Comparative evaluation** of uncoordinated vs. structured incident response (MTTA, MTTR, traceability) using randomized controlled drills.

- **A practical case study** demonstrating end-to-end integration of an open-source LoRa mesh prototype into a domain-specific operational platform for trekking agencies.

**e. Related Works / Literature Review (Preliminary)**

- **LoRa mesh communication** (Meshtastic, RAK WisBlock Mesh): Multi-hop messaging, GPS, local SOS broadcast, fall detection. Gap: no agency-side rental workflow, no device fleet management, no persistent cloud incident pipeline, no store-and-forward to cloud.

- **Commercial off-grid safety devices** (Garmin inReach Mini 2, SPOT Gen4, Zoleo): Satellite SOS, two-way messaging, GPS tracking. Gap: closed proprietary ecosystems; individual-use oriented; no fleet rental; no operational incident management.

- **IoT fleet management platforms** (AWS IoT Core, Azure IoT Hub, Balena): Device registration, telemetry ingestion, remote monitoring, lifecycle states. Gap: generic cloud platforms; no LoRa mesh integration; no store-and-forward for intermittent connectivity; no rental domain.

- **Delay/Disruption-Tolerant and store-and-forward systems** (DTN RFC 4838 Bundle Protocol, MQTT-SN, LoRaWAN ADR): Message persistence and forwarding under intermittent connectivity. Gap: protocol-level designs; not integrated with business workflows or incident management.

- **Incident management systems** (JIRA Service Management, PagerDuty, Opsgenie): Ticket lifecycle, escalation, notification, SLA tracking, audit trail. Gap: designed for IT/DevOps; no IoT field-event ingestion; no outdoor or trekking domain context.

Gap statement: TrekLink addresses the integration gap where all five dimensions — off-grid LoRa mesh communication, intermittent-connectivity store-and-forward synchronization, device rental lifecycle management, real-time field monitoring, and structured SOS-to-incident response — must be combined into a single domain-specific platform. Each existing solution addresses at most two of these dimensions.

Key References:

- [1] A. W.-L. Wong, S. L. Goh, M. K. Hasan, and S. Fattah, "Multi-hop and mesh for LoRa networks: Recent advancements, issues, and recommended applications," ACM Comput. Surv., vol. 56, no. 6, Article 136, pp. 1–43, Jan. 2024. DOI: 10.1145/3638241

- [2] Muladi, H. Wijaya, S. D. Prasetyo, S. A. Hamzah, and A. K. Mahamad, "LoRa mesh-based IoT GPS tracking system for mountain climbers," Int. J. Safety Security Eng., vol. 14, no. 6, pp. 1751–1761, Dec. 2024. DOI: 10.18280/ijsse.140610

- [3] H. Zhang, R. Zhang, and J. Sun, "Developing real-time IoT-based public safety alert and emergency response systems," Sci. Rep., vol. 15, Article 29056, Aug. 2025. DOI: 10.1038/s41598-025-13465-7

- [4] OASIS, "MQTT Version 5.0," OASIS Standard, Mar. 2019. https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html

- [5] V. Cerf, S. Burleigh, A. Hooke, L. Torgerson, R. Durst, K. Scott, K. Fall, and H. Weiss, "Delay-tolerant networking architecture," IETF RFC 4838, Apr. 2007. https://www.rfc-editor.org/rfc/rfc4838

- [6] Meshtastic Project, "Official Documentation," 2024. [Online]. Available: https://meshtastic.org/docs/

**4. Other comments (propose all relative things if have):**

The existing TrekLink LoRa mesh firmware (ESP32/ESP32-S3) is an output of a prior project by this team (Summer 2026) and is treated as an inherited technical foundation — not a new Capstone deliverable. The Fall 2026 Capstone scope covers only the Gateway Bridge, cloud backend, web client, and their experimental evaluation. This boundary must be clearly stated in the SRS, implementation report, and defense presentation. All effort reporting, source-code statistics, and test coverage metrics shall exclude the inherited firmware and cover only the newly developed software components.

| **Supervisor (If have)**<br><br>_(Sign and full name)_ | HCM, date 25/07/2026<br><br>**On behalf of Registers**<br><br>_(Sign and full name)_ |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------ |
