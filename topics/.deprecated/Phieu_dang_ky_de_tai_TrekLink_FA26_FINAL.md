# **CAPSTONE PROJECT REGISTER**

**Class:** SE **Duration time:** from 09/2026 to 03/2027

**(*) Profession:** Software Engineer **Specialty:** SE

**(*) Kinds of person who make register:** [ ] Lecturer [X] Students

## 1. Register information for supervisor (if have)

|   |   |   |   |   |
|---|---|---|---|---|
|**No.**|**Full name**|**Phone**|**E-Mail**|**Title**|
|Supervisor|Đặng Ngọc Minh Đức||ducdnm2@fpt.edu.vn|Assoc. Prof|

## 2. Register information for students

|   |   |   |   |   |   |
|---|---|---|---|---|---|
|**No**|**Full name**|**Student code**|**Phone**|**E-mail**|**Role in Group**|
|1|Đỗ Đăng Khoa|SE192357||khoado7577@gmail.com|Leader|
|2|Lâm Phi Long|SE182769||LongLPSE182769@fpt.edu.vn|Member|
|3|Trần Khải Hoàng|SE182767||HoangTKSE182767@fpt.edu.vn|Member|
|4|Nguyễn Ngọc Long|SE193490||nguyenngoclong216@gmail.com|Member|
|5|Nguyễn Bá Tân|SE183860||TanNBSE183860@fpt.edu.vn|Member|

## 3. Register Content of Capstone Project

### (*) 3.1. Capstone Project Name

**English:** TrekLink — An Integrated Off-Grid Communication & Smart Device Rental Management Platform for Trekking Agencies

**Vietnamese:** TrekLink — Nền tảng Quản lý và Cho thuê Thiết bị Liên lạc Offline Tích hợp cho Doanh nghiệp Trekking

**a. Context**

During SU26, our team developed TrekLink, an open-source LoRa mesh communication firmware (forked from Meshtastic) targeting ESP32/ESP32-S3 hardware for Search & Rescue use in cellular “dead zones.” The firmware already provides self-healing mesh messaging, GPS tracking, and an IMU-agnostic fall detection state machine that auto-escalates to a mesh-wide SOS broadcast, across four hardware variants (v1.0–v4.0).

While the embedded firmware is functionally complete, it has no business or operational layer: there is no way for an organization to track which device is with which person, manage a fleet of rentable units, coordinate a response when an SOS fires in the field, or bill a customer for usage. This gap is common to trekking and outdoor tour agencies, who today either provide no safety device at all, or rely on standalone satellite messengers (SPOT / Garmin inReach) with no agency-side fleet, booking, or incident-management tooling.

This project extends TrekLink into a full Trekking Agency Operations Platform: the existing mesh devices become a rentable, trackable fleet, and a new web/mobile management layer introduces the actors and workflows of a real agency — Admin, Staff, Guide, and Customer — handling booking, device rental, real-time field monitoring, and SOS incident response end-to-end.

**Functional Requirement**

**Module 1: Identity & Role Management**

- Account registration/login for Admin, Staff, Guide, and Customer roles
- Role-Based Access Control (RBAC) governing access to devices, trips, and incident data
- Guide profile management (assigned trips, device-handling history)

**Module 2: Device Fleet & Inventory Management**

- Register each physical TrekLink unit (device ID, hardware variant v1–v4, firmware version)
- Device lifecycle state machine: Available → Reserved → Rented → In-Field → Returned → Maintenance → Retired
- Battery/telemetry status feed per device (last-seen, battery %, last GPS fix)
- Maintenance scheduling and damage/incident logging per device

**Module 3: Trip & Rental Management**

- Customer browses/books a trek package and reserves devices for the group
- Staff reviews bookings, allocates available devices, generates the rental agreement
- Deposit handling, check-out/check-in workflow, late-return and damage fee calculation
- Guide assigned to a trip together with the group's rented device set

**Module 4: Real-Time Field Monitoring & SOS Operations**

- A Gateway/Bridge node (TrekLink hardware + Wi-Fi/cellular uplink, carried by the Guide or placed at basecamp) relays mesh traffic — position beacons and SOS broadcasts — to the cloud backend whenever it has connectivity
- Live dashboard (Staff/Admin/Guide) showing each active trip's group position and device status
- SOS pipeline: firmware-level SOS → gateway relay → backend incident creation → Staff/Guide notification → resolution logging
- Store-and-forward sync for periods when the gateway itself is out of coverage

**Module 5: Billing & Reporting**

- Rental pricing rules (per device, per day/trip), automatic invoice generation
- Payment status tracking (mock/sandbox payment integration acceptable for MVP)
- Usage and incident reports for agency management

**Carried over from SU26 R&D (retained as the embedded foundation)**

- LoRa mesh communication, AES-256 encrypted traffic, managed flooding routing
- IMU-agnostic fall detection (5-state machine) and automatic SOS escalation
- GPS tracking, Haversine distance/bearing calculation

**Non-Functional Requirement**

**Performance**

- API response time below 300ms for 95% of requests
- Gateway-to-cloud sync latency under 5 seconds when connectivity is available
- Embedded performance carried over: adaptive IMU polling (2Hz idle / 10Hz active), 3–5 day device battery life

**Reliability**

- Store-and-forward queuing on the gateway node so no SOS/position data is lost during connectivity gaps
- Graceful degradation if a device or gateway drops off the mesh (no single point of failure for in-progress trips)

**Security**

- JWT-based authentication and RBAC for all platform actors
- End-to-end encrypted mesh traffic between devices (AES-256, carried over from firmware)
- Auditable incident/SOS logs (immutable once created)

**Scalability**

- Backend designed to support multiple concurrent agencies/trips (multi-tenant-ready schema)
- Device fleet management scales to 50+ units without architecture changes
- Dockerized deployment, CI/CD via GitHub Actions

### (*) 3.2. Main Proposal Content

**a. Proposed Solutions**

- Trekking Agency Operations Platform — web (Admin/Staff) + mobile/responsive (Guide/Customer) app layered on the existing TrekLink mesh hardware, adding the actor-driven workflows the firmware-only project currently lacks
- Gateway/Bridge Architecture — a dedicated TrekLink node configured as a mesh-to-cloud bridge, using store-and-forward sync so offline field data reaches the backend once connectivity returns
- Device-as-Rentable-Asset Model — every physical unit across all four hardware variants tracked through a formal lifecycle state machine
- SOS-to-Incident Pipeline — converts the firmware's device-level SOS broadcast into an operational workflow: incident creation, notification, and resolution tracking
- Reuse of Hardware Variant Diversity — the four existing hardware tiers double as rental “tiers” the agency can offer at different price points

**b. Applied Theory**

|   |   |
|---|---|
|**Theory**|**Application**|
|Automata Theory (Finite State Machines)|Formal model behind the device-rental lifecycle (Available → Rented → Returned → Maintenance) and the existing 5-state fall-detection machine|
|Graph Theory / Network Routing Theory|Underlies the LoRa mesh's managed-flooding routing — nodes and edges model the mesh topology and multi-hop packet relay|
|Role-Based Access Control (RBAC) Model|Formal access-control model (NIST RBAC) governing Admin / Staff / Guide / Customer permissions across the platform|
|CAP Theorem / Eventual Consistency|Justifies the store-and-forward, offline-first design of the gateway-to-cloud sync under intermittent connectivity|
|Queueing Theory|Underpins the priority message queue (SOS pre-empts other mesh traffic) and the incident-notification queue on the backend|
|Cryptographic Theory (Authenticated Encryption)|AES-256-GCM secures mesh traffic confidentiality and integrity, carried over from the firmware|
|Sensor Fusion / Filtering Theory (Madgwick AHRS)|Fuses accelerometer, gyroscope, and magnetometer data to recognize fall signatures (freefall, impact), carried over from the firmware|
|Statistical Signal Processing / Threshold Detection Theory|Underpins the 250-sample noise-floor self-calibration and adaptive threshold tuning that separates genuine falls from false positives in the fall-detection module|
|Real-Time Scheduling Theory|Governs the adaptive IMU polling rate (2Hz idle / 10Hz active), trading detection latency against power consumption on battery-constrained hardware|

**c. Tech Stack**

|   |   |
|---|---|
|**Layer**|**Technology (proposed)**|
|Embedded / Firmware|C++ on ESP32/ESP32-S3, PlatformIO, RadioLib (LoRa), Meshtastic protocol base|
|Gateway / Bridge node|TrekLink hardware configured as mesh-to-cloud bridge; Wi-Fi/cellular uplink; MQTT client|
|Backend API|NestJS (TypeScript) — REST + WebSocket endpoints|
|Database|PostgreSQL — relational schema (devices, trips, rentals, incidents, billing) plus JSONB columns for GPS/telemetry data; Prisma ORM|
|Real-Time Messaging|MQTT (gateway-side, lightweight IoT transport) + WebSocket/Socket.io (browser-side, live dashboard and SOS relay) — hybrid, matched to each leg of the data path|
|Web Frontend (Admin/Staff/Guide/Customer)|React + TypeScript, single responsive web app with role-based views|
|Authentication & Authorization|JWT session tokens, bcrypt password hashing; CASL (@casl/ability) for RBAC policy enforcement across Admin/Staff/Guide/Customer|
|DevOps / Deployment|Docker, GitHub Actions CI/CD, cloud VPS (AWS/GCP/Azure free tier or university server)|

**d. Products (Expected Deliverables)**

**Software Products**

- Backend API service (trip, rental, device, incident, billing endpoints)
- Admin/Staff Web Dashboard (fleet, bookings, live incident monitoring)
- Guide client (trip roster, live group view, SOS handling)
- Customer-facing booking & rental web app
- Gateway/Bridge firmware module (mesh-to-cloud sync)
- TrekLink embedded firmware (carried over from SU26 — mesh comm, fall detection, SOS)

**Research Outputs**

- Updated SRS reflecting the multi-actor platform scope
- System architecture & database design documentation
- Field test report (device rental workflow + live SOS-to-incident pipeline)

**e. Proposed Tasks**

**Phase 1 — Requirements & Architecture**

- Actor/role and workflow modeling (Admin, Staff, Guide, Customer)
- Database schema design (devices, trips, rentals, incidents, billing)
- Gateway/bridge sync architecture design

**Phase 2 — Platform Core Development**

- Backend API + RBAC authentication
- Device fleet & rental lifecycle module
- Admin/Staff dashboard

**Phase 3 — Field Integration**

- Gateway/bridge firmware (mesh-to-cloud relay)
- Real-time SOS-to-incident pipeline and live monitoring dashboard
- Guide and Customer client apps

**Phase 4 — Testing & Evaluation**

- Combined hardware + software field test (simulated rental + SOS trigger)
- Billing/reporting validation
- Defense preparation

## 3.3. Research Information

**a. Research Problem / Research Question**

**Problem:** Trekking and outdoor tour agencies that want to provide off-grid safety communication to customers currently have no integrated way to manage a device fleet, rent it out, and operationally respond to field incidents. Existing options are either hardware-only (consumer satellite messengers, our own SU26 TrekLink firmware) with no business layer, or generic rental/booking software with no real safety-device integration.

**Research Questions:**

- Can the existing TrekLink hardware/firmware be extended with a gateway/bridge node that reliably relays SOS and position data to a cloud backend under intermittent connectivity?
- Can a single platform model the full actor set of a trekking agency (Admin, Staff, Guide, Customer) around a physical device-rental lifecycle without excessive complexity for a 4-person team in one capstone term?
- Does converting a device-level SOS broadcast into a tracked operational incident measurably improve response coordination compared to the current local-alarm-only behavior?

**b. Research Objectives**

**General Objective:** Design, implement, and validate a trekking-agency operations platform — covering device rental, real-time field monitoring, and SOS incident response — built on top of the team's existing TrekLink mesh firmware.

- Implement RBAC-based actor workflows for Admin, Staff, Guide, and Customer
- Implement a device lifecycle model that tracks every physical unit through rental, field use, return, and maintenance
- Implement a gateway/bridge node that reliably syncs mesh position/SOS data to the cloud under intermittent connectivity
- Convert SOS broadcasts into trackable incidents with notification and resolution logging
- Validate the end-to-end pipeline (rental → field trip → SOS trigger → incident resolution) in a field test

**c. Research Scope & Methodology**

**In Scope:**

- Four actor roles: Admin, Staff, Guide, Customer
- Device rental lifecycle for the existing four TrekLink hardware variants
- Gateway/bridge node for mesh-to-cloud sync (store-and-forward)
- Real-time monitoring dashboard and SOS-to-incident pipeline
- Billing module (rental pricing, mock/sandbox payment)

**Out of Scope:**

- Native mobile apps for all four roles (responsive web acceptable for MVP)
- Production payment gateway integration (sandbox/mock only)
- Route planning / trail recommendation features
- Multi-language localization
- Commercial certification (FCC, CE) of the hardware itself

**Research Methodology:**

|   |   |
|---|---|
|**Method**|**Application**|
|Literature Review|Review of rental/asset-management platforms, IoT fleet management, and existing SAR communication systems|
|Agile Development (Scrum)|Two-week sprints across requirements, backend, frontend, and field-integration phases|
|Test-Driven Development|Unit/integration tests for rental lifecycle, RBAC, and sync logic|
|Field Testing|Simulated rental cycle + live SOS trigger to validate the full pipeline end-to-end|

**d. Expected Scientific / Practical Contribution**

- A reusable Gateway/Bridge pattern for syncing intermittent LoRa mesh data (position, SOS, telemetry) to a cloud backend via store-and-forward
- A device-rental lifecycle model that turns a fleet of safety-communication hardware into a billable, trackable asset pool
- An SOS-to-Incident pipeline demonstrating how a device-level safety event can be escalated into a coordinated, role-based operational response
- A case study in layering a multi-actor business platform on top of an existing embedded/IoT codebase without re-architecting the firmware itself

**e. Related Works / Literature Review (Preliminary)**

|   |   |   |
|---|---|---|
|**Work**|**Summary**|**Gap / Our Contribution**|
|Meshtastic|Open-source LoRa mesh firmware; base platform for TrekLink|No business/rental layer; no agency-side fleet or incident management|
|SPOT / Garmin inReach|Consumer satellite messengers with SOS|Subscription-based, single-device focus; no agency fleet management or rental workflow|
|Generic tour/rental booking platforms|Manage bookings and equipment rental for tour operators|No real-time field safety integration; SOS/incident handling is absent|
|TrekLink (SU26, this team)|Our own prior-semester firmware: mesh comm, fall detection, SOS|Hardware-complete but has no operational/business layer — the gap this project addresses|

## 4. Other Comments

The embedded firmware foundation for this project is not a from-scratch build: TrekLink (SU26) is an existing, working codebase (~636 source files, ~149,000 lines, 4 build environments across ESP32/ESP32-S3 hardware variants, based on Meshtastic v2.7.19) with mesh communication, fall detection, and SOS already implemented and tested. This capstone term focuses on the new actor-driven management platform described above; the firmware itself is treated as a stable dependency rather than a deliverable to be rebuilt.