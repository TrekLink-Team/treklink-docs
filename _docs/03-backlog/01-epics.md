# 01 — Epics

> Generated from `build_backlog.py` (kept alongside this file for regeneration) — the same data drives `02-user-stories.md` and `User_Story_Agile_TrekLink.xlsx`, so all three stay consistent. Epic taxonomy: the 7 epics locked in `02-templates/05-user-story-template.md`, plus **E8 (Research & Experimental Evaluation)**, added this session to home RQ1-RQ3/TP6 work that didn't fit the original 7.

**Backlog totals**: 8 epics · 88 stories · 365 story points.

| Epic | Jira | Name | Module(s) | Stories | Points | Sprint range | Primary owner | Reviewer |
|---|---|---|---|---|---|---|---|---|
| E1 | `TK-1` | Identity & RBAC | `module:auth` | 10 | 37 | Sprint 1-3 (MF-01 foundation: auth) | Lâm Phi Long | Đỗ Đăng Khoa |
| E2 | `TK-2` | Device Fleet & Maintenance | `module:devices` | 12 | 42 | Sprint 1-3 (MF-01 / MF-05: device fleet) | Nguyễn Ngọc Long | Đỗ Đăng Khoa |
| E3 | `TK-3` | Trip & Rental Management | `module:trips`, `module:rentals` | 18 | 65 | Sprint 1-3 (MF-01: trips & rentals) | Lâm Phi Long | Đỗ Đăng Khoa |
| E4 | `TK-4` | Gateway & Offline Sync | `module:gateway-sync` | 12 | 61 | Sprint 1-3 (MF-02: gateway & offline sync) | Đỗ Đăng Khoa | Đỗ Đăng Khoa |
| E5 | `TK-5` | Real-Time Monitoring & SOS Incidents | `module:monitoring`, `module:incidents` | 15 | 65 | Sprint 2-4 (MF-03 + MF-04) | Nguyễn Bá Tân | Đỗ Đăng Khoa |
| E6 | `TK-6` | Billing & Reporting | `module:billing` | 8 | 25 | Sprint 2-5 (MF-05: billing) | Nguyễn Bá Tân | Đỗ Đăng Khoa |
| E7 | `TK-7` | DevOps / CI-CD | `module:devops` | 7 | 21 | Sprint 1 then ongoing (cross-cutting, not a Main Flow) | Đỗ Đăng Khoa | Đỗ Đăng Khoa |
| E8 | `TK-8` | Research & Experimental Evaluation | `module:docs` | 6 | 49 | Sprint 6 (cross-cutting research, not a Main Flow) | Đỗ Đăng Khoa | Đỗ Đăng Khoa |

---

## E1 (`TK-1`) — Identity & RBAC

Registration, login, password recovery, refresh-token session security, and a data-driven Role & Permission (RBAC/CASL) model so Admin/Staff/Guide/Customer access control can evolve without code changes.

- **Module label(s)**: `module:auth`
- **Primary Prisma tables/entities**: users, roles, permissions, role_permissions, refresh_tokens
- **Sprint range**: Sprint 1-3 (MF-01 foundation: auth)
- **Stories**: 10 · **Points**: 37
- **Primary owner**: Lâm Phi Long (LongLP) · **Secondary**: Trần Khải Hoàng · **Reviewer/Architect**: Đỗ Đăng Khoa (Khoa)

| Story | Summary | Main Flow | Points | Sprint | Status |
|---|---|---|---|---|---|
| [US-006](./02-user-stories.md#us-006) | Logout / token revocation | MF-01 | 2 | Sprint 3 | Backlog |
| [US-002](./02-user-stories.md#us-002) | Account registration | MF-01 | 3 | Sprint 2 | Backlog |
| [US-003](./02-user-stories.md#us-003) | Login issues JWT access + refresh token | MF-01 | 3 | Sprint 2 | Backlog |
| [US-004](./02-user-stories.md#us-004) | Auth audit log (login/logout/failed attempts) | MF-01 | 3 | Sprint 2 | Backlog |
| [US-007](./02-user-stories.md#us-007) | Password reset / recovery | MF-01 | 3 | Sprint 3 | Backlog |
| [US-010](./02-user-stories.md#us-010) | Guide profile management | MF-01 | 3 | Sprint 3 | Backlog |
| [US-001](./02-user-stories.md#us-001) | Data-driven Role & Permission (RBAC) schema | MF-01 | 5 | Sprint 1 | Ready |
| [US-005](./02-user-stories.md#us-005) | Refresh-token rotation & silent session renewal | MF-01 | 5 | Sprint 3 | Backlog |
| [US-008](./02-user-stories.md#us-008) | CASL PoliciesGuard enforcement | MF-01 | 5 | Sprint 3 | Backlog |
| [US-009](./02-user-stories.md#us-009) | Admin: manage user accounts | MF-01 | 5 | Sprint 3 | Backlog |

## E2 (`TK-2`) — Device Fleet & Maintenance

Physical TrekLink device registration across hardware variants v1-v4, the 7-state rental lifecycle FSM, telemetry ingestion, maintenance scheduling, and damage logging.

- **Module label(s)**: `module:devices`
- **Primary Prisma tables/entities**: devices, device_types, device_telemetry, maintenance_logs, damage_logs
- **Sprint range**: Sprint 1-3 (MF-01 / MF-05: device fleet)
- **Stories**: 12 · **Points**: 42
- **Primary owner**: Nguyễn Ngọc Long (LongNN) · **Secondary**: Nguyễn Ngọc Long · **Reviewer/Architect**: Đỗ Đăng Khoa (Khoa)

| Story | Summary | Main Flow | Points | Sprint | Status |
|---|---|---|---|---|---|
| [US-016](./02-user-stories.md#us-016) | Device detail view | MF-01 | 2 | Sprint 3 | Backlog |
| [US-020](./02-user-stories.md#us-020) | Retire a device | MF-01 | 2 | Sprint 3 | Backlog |
| [US-021](./02-user-stories.md#us-021) | Device fleet dashboard widget | MF-01 | 2 | Sprint 3 | Backlog |
| [US-011](./02-user-stories.md#us-011) | Manage device type / hardware variant catalog | MF-01 | 3 | Sprint 3 | Backlog |
| [US-012](./02-user-stories.md#us-012) | Register a physical TrekLink device | MF-01 | 3 | Sprint 3 | Backlog |
| [US-015](./02-user-stories.md#us-015) | Device fleet list with filters | MF-01 | 3 | Sprint 3 | Backlog |
| [US-018](./02-user-stories.md#us-018) | Schedule device maintenance | MF-01 | 3 | Sprint 3 | Backlog |
| [US-019](./02-user-stories.md#us-019) | Log device damage on return inspection | MF-01 | 3 | Sprint 3 | Backlog |
| [US-022](./02-user-stories.md#us-022) | Device assignment/rental/incident history view | MF-01 | 3 | Sprint 3 | Backlog |
| [US-014](./02-user-stories.md#us-014) | Prevent allocation of unavailable devices | MF-01 | 5 | Sprint 3 | Backlog |
| [US-017](./02-user-stories.md#us-017) | Ingest device telemetry from Gateway | MF-01 | 5 | Sprint 3 | Backlog |
| [US-013](./02-user-stories.md#us-013) | Device 7-state lifecycle FSM engine | MF-01 | 8 | Sprint 3 | Backlog |

## E3 (`TK-3`) — Trip & Rental Management

Trek package browsing/booking, device reservation and allocation, rental agreements, deposit/check-out/check-in workflow, late-return and damage fees, and Guide-to-trip assignment.

- **Module label(s)**: `module:trips`, `module:rentals`
- **Primary Prisma tables/entities**: trek_packages, trips, bookings, rentals, rental_agreements
- **Sprint range**: Sprint 1-3 (MF-01: trips & rentals)
- **Stories**: 18 · **Points**: 65
- **Primary owner**: Lâm Phi Long (LongLP) · **Secondary**: Trần Khải Hoàng · **Reviewer/Architect**: Đỗ Đăng Khoa (Khoa)

| Story | Summary | Main Flow | Points | Sprint | Status |
|---|---|---|---|---|---|
| [US-024](./02-user-stories.md#us-024) | Browse trek packages | MF-01 | 2 | Sprint 3 | Backlog |
| [US-031](./02-user-stories.md#us-031) | Record deposit | MF-01 | 2 | Sprint 3 | Backlog |
| [US-040](./02-user-stories.md#us-040) | Customer: view trip & rental history | MF-01 | 2 | Sprint 3 | Backlog |
| [US-023](./02-user-stories.md#us-023) | Manage trek packages | MF-01 | 3 | Sprint 3 | Backlog |
| [US-027](./02-user-stories.md#us-027) | Review and approve/reject a booking | MF-01 | 3 | Sprint 3 | Backlog |
| [US-029](./02-user-stories.md#us-029) | Assign a Guide to a trip | MF-01 | 3 | Sprint 3 | Backlog |
| [US-033](./02-user-stories.md#us-033) | Guide confirms device receipt/handover | MF-01 | 3 | Sprint 3 | Backlog |
| [US-035](./02-user-stories.md#us-035) | Calculate late-return fee | MF-01 | 3 | Sprint 3 | Backlog |
| [US-036](./02-user-stories.md#us-036) | Calculate damage fee | MF-01 | 3 | Sprint 3 | Backlog |
| [US-037](./02-user-stories.md#us-037) | Guide: view assigned trips, group, devices | MF-01 | 3 | Sprint 3 | Backlog |
| [US-039](./02-user-stories.md#us-039) | Customer: view booking/rental/deposit/payment info | MF-01 | 3 | Sprint 3 | Backlog |
| [US-025](./02-user-stories.md#us-025) | Submit a booking request | MF-01 | 5 | Sprint 3 | Backlog |
| [US-026](./02-user-stories.md#us-026) | Reserve devices during booking | MF-01 | 5 | Sprint 3 | Backlog |
| [US-028](./02-user-stories.md#us-028) | Allocate specific devices to a confirmed booking | MF-01 | 5 | Sprint 3 | Backlog |
| [US-030](./02-user-stories.md#us-030) | Generate rental agreement | MF-01 | 5 | Sprint 3 | Backlog |
| [US-032](./02-user-stories.md#us-032) | Device check-out workflow | MF-01 | 5 | Sprint 3 | Backlog |
| [US-034](./02-user-stories.md#us-034) | Device check-in workflow on return | MF-01 | 5 | Sprint 3 | Backlog |
| [US-038](./02-user-stories.md#us-038) | Guide: live group position/device status during trip | MF-04 | 5 | Sprint 4 | Backlog |

## E4 (`TK-4`) — Gateway & Offline Sync

The eventId scheme, SQLite priority queue (P0-P3), MQTT publish/reconnect-flush on the gateway, and idempotent event ingestion + sync audit log on the backend. The module most different from a normal CRUD app — graded on delivery rate, duplicate rate, and priority-ordering compliance.

- **Module label(s)**: `module:gateway-sync`
- **Primary Prisma tables/entities**: gateway_events, event_queue (gateway-local SQLite), sync_audit_log
- **Sprint range**: Sprint 1-3 (MF-02: gateway & offline sync)
- **Stories**: 12 · **Points**: 61
- **Primary owner**: Đỗ Đăng Khoa (Khoa) · **Secondary**: Lâm Phi Long · **Reviewer/Architect**: Đỗ Đăng Khoa (Khoa)

| Story | Summary | Main Flow | Points | Sprint | Status |
|---|---|---|---|---|---|
| [US-042](./02-user-stories.md#us-042) | Freeze the eventId schema | MF-02 | 3 | Sprint 1 | Ready |
| [US-045](./02-user-stories.md#us-045) | Gateway-side duplicate suppression | MF-02 | 3 | Sprint 2 | Backlog |
| [US-049](./02-user-stories.md#us-049) | Gateway health-reporting API | MF-02 | 3 | Sprint 3 | Backlog |
| [US-052](./02-user-stories.md#us-052) | Automated duplicate-delivery test | MF-02 | 3 | Sprint 3 | Backlog |
| [US-043](./02-user-stories.md#us-043) | SQLite local priority queue schema | MF-02 | 5 | Sprint 2 | Backlog |
| [US-044](./02-user-stories.md#us-044) | Enqueue incoming LoRa events into the priority queue | MF-02 | 5 | Sprint 2 | Backlog |
| [US-046](./02-user-stories.md#us-046) | D-005 Gateway connectivity PoC | MF-02 | 5 | Sprint 2 | Backlog |
| [US-047](./02-user-stories.md#us-047) | MQTT publish client (gateway → broker) | MF-02 | 5 | Sprint 3 | Backlog |
| [US-051](./02-user-stories.md#us-051) | Backend: synchronization audit log | MF-02 | 5 | Sprint 3 | Backlog |
| [US-041](./02-user-stories.md#us-041) | LoRa-to-Gateway serial parser (PoC) | MF-02 | 8 | Sprint 1 | Ready |
| [US-048](./02-user-stories.md#us-048) | Reconnection detection + priority-ordered flush | MF-02 | 8 | Sprint 3 | Backlog |
| [US-050](./02-user-stories.md#us-050) | Backend: idempotent event ingestion endpoint | MF-02 | 8 | Sprint 3 | Backlog |

## E5 (`TK-5`) — Real-Time Monitoring & SOS Incidents

Live map/telemetry dashboard over WebSocket, automatic SOS-to-Incident creation on idempotency pass, the 5-state Incident FSM with append-only audit trail, and Staff/Guide acknowledgment-and-response workflow (MTTA/MTTR are graded RQ3 metrics).

- **Module label(s)**: `module:monitoring`, `module:incidents`
- **Primary Prisma tables/entities**: incidents, incident_audit_log, device_positions (live, via WebSocket)
- **Sprint range**: Sprint 2-4 (MF-03 + MF-04)
- **Stories**: 15 · **Points**: 65
- **Primary owner**: Nguyễn Bá Tân (TanNB) · **Secondary**: Trần Khải Hoàng · **Reviewer/Architect**: Đỗ Đăng Khoa (Khoa)

| Story | Summary | Main Flow | Points | Sprint | Status |
|---|---|---|---|---|---|
| [US-056](./02-user-stories.md#us-056) | Device telemetry live display on map | MF-04 | 3 | Sprint 4 | Backlog |
| [US-059](./02-user-stories.md#us-059) | Append-only incident audit trail | MF-03 | 3 | Sprint 4 | Backlog |
| [US-060](./02-user-stories.md#us-060) | Staff: acknowledge an incident | MF-03 | 3 | Sprint 4 | Backlog |
| [US-061](./02-user-stories.md#us-061) | Staff: update/coordinate an incident | MF-03 | 3 | Sprint 4 | Backlog |
| [US-062](./02-user-stories.md#us-062) | Staff: close/resolve an incident | MF-03 | 3 | Sprint 4 | Backlog |
| [US-064](./02-user-stories.md#us-064) | Staff: manually create a non-SOS incident | MF-03 | 3 | Sprint 4 | Backlog |
| [US-065](./02-user-stories.md#us-065) | Gateway connectivity status indicator | MF-04 | 3 | Sprint 4 | Backlog |
| [US-066](./02-user-stories.md#us-066) | Incident queue panel | MF-03 | 3 | Sprint 4 | Backlog |
| [US-053](./02-user-stories.md#us-053) | WebSocket gateway (Socket.io) for live push | MF-04 | 5 | Sprint 4 | Backlog |
| [US-057](./02-user-stories.md#us-057) | Auto-create Incident from a valid SOS event | MF-03 | 5 | Sprint 4 | Backlog |
| [US-058](./02-user-stories.md#us-058) | WebSocket push notification within 2 seconds | MF-03 | 5 | Sprint 4 | Backlog |
| [US-063](./02-user-stories.md#us-063) | Guide: acknowledge + submit response notes | MF-03 | 5 | Sprint 4 | Backlog |
| [US-088](./02-user-stories.md#us-088) | Staff: distinguish and dismiss a Suspected (cadence-inferred) SOS episode | MF-03 | 5 | Sprint 4 | Backlog |
| [US-054](./02-user-stories.md#us-054) | Incident 5-state FSM engine | MF-03 | 8 | Sprint 4 | Backlog |
| [US-055](./02-user-stories.md#us-055) | Live operational map (MapLibre GL + Goong Maps) | MF-04 | 8 | Sprint 4 | Backlog |

## E6 (`TK-6`) — Billing & Reporting

Rental pricing rules, automatic invoice generation, mock/sandbox payment status tracking, and usage/incident/utilization reporting for agency management.

- **Module label(s)**: `module:billing`
- **Primary Prisma tables/entities**: pricing_rules, invoices, payments (sandbox), reports (derived views)
- **Sprint range**: Sprint 2-5 (MF-05: billing)
- **Stories**: 8 · **Points**: 25
- **Primary owner**: Nguyễn Bá Tân (TanNB) · **Secondary**: — · **Reviewer/Architect**: Đỗ Đăng Khoa (Khoa)

| Story | Summary | Main Flow | Points | Sprint | Status |
|---|---|---|---|---|---|
| [US-070](./02-user-stories.md#us-070) | View invoice & payment status | MF-05 | 2 | Sprint 5 | Backlog |
| [US-073](./02-user-stories.md#us-073) | System health & audit-log report view | MF-05 | 2 | Sprint 5 | Backlog |
| [US-074](./02-user-stories.md#us-074) | Billing dashboard widget | MF-05 | 2 | Sprint 5 | Backlog |
| [US-069](./02-user-stories.md#us-069) | Mock/sandbox payment integration | MF-05 | 3 | Sprint 5 | Backlog |
| [US-071](./02-user-stories.md#us-071) | Usage & device-utilization report | MF-05 | 3 | Sprint 5 | Backlog |
| [US-072](./02-user-stories.md#us-072) | Incident / response-performance report | MF-05 | 3 | Sprint 5 | Backlog |
| [US-067](./02-user-stories.md#us-067) | Manage rental pricing rules | MF-05 | 5 | Sprint 5 | Backlog |
| [US-068](./02-user-stories.md#us-068) | Automatic invoice generation | MF-05 | 5 | Sprint 5 | Backlog |

## E7 (`TK-7`) — DevOps / CI-CD

Docker Compose for all services, GitHub Actions CI (lint/typecheck/test/build) and CD, health-check endpoint, environment configuration matrix, deployment guide, and demo seed data.

- **Module label(s)**: `module:devops`
- **Primary Prisma tables/entities**: n/a (infrastructure)
- **Sprint range**: Sprint 1 then ongoing (cross-cutting, not a Main Flow)
- **Stories**: 7 · **Points**: 21
- **Primary owner**: Đỗ Đăng Khoa (Khoa) · **Secondary**: Lâm Phi Long · **Reviewer/Architect**: Đỗ Đăng Khoa (Khoa)

| Story | Summary | Main Flow | Points | Sprint | Status |
|---|---|---|---|---|---|
| [US-077](./02-user-stories.md#us-077) | Backend health-check endpoint | X-DevOps | 2 | Sprint 1 | Ready |
| [US-079](./02-user-stories.md#us-079) | Environment configuration matrix | X-DevOps | 2 | Sprint 1 | Ready |
| [US-076](./02-user-stories.md#us-076) | GitHub Actions CI: lint + typecheck + test + build | X-DevOps | 3 | Sprint 1 | Backlog |
| [US-078](./02-user-stories.md#us-078) | GitHub Actions CD: build & push images on merge | X-DevOps | 3 | Sprint 1 | Ready |
| [US-080](./02-user-stories.md#us-080) | Deployment guide (clean-environment validated) | X-DevOps | 3 | Sprint 1 | Ready |
| [US-081](./02-user-stories.md#us-081) | Seed/demo data script | X-DevOps | 3 | Sprint 1 | Ready |
| [US-075](./02-user-stories.md#us-075) | Dockerfiles + docker-compose for all services | X-DevOps | 5 | Sprint 1 | Ready |

## E8 (`TK-8`) — Research & Experimental Evaluation

Added this session — homes the graded RQ1-RQ3 work that doesn't fit the other 7 template epics: the connectivity-loss experiment protocol/execution (RQ1/RQ2), the SOS-drill protocol/execution (RQ3), the end-to-end verification suite, and the evaluation report feeding Defense 1.

- **Module label(s)**: `module:docs`
- **Primary Prisma tables/entities**: n/a (experiment protocol + evaluation report)
- **Sprint range**: Sprint 6 (cross-cutting research, not a Main Flow)
- **Stories**: 6 · **Points**: 49
- **Primary owner**: Đỗ Đăng Khoa (Khoa) · **Secondary**: Đỗ Đăng Khoa · **Reviewer/Architect**: Đỗ Đăng Khoa (Khoa)

| Story | Summary | Main Flow | Points | Sprint | Status |
|---|---|---|---|---|---|
| [US-082](./02-user-stories.md#us-082) | Design RQ1/RQ2 connectivity-loss experiment protocol | X-Research | 5 | Sprint 6 | Backlog |
| [US-083](./02-user-stories.md#us-083) | Design RQ3 SOS-drill experiment protocol | X-Research | 5 | Sprint 6 | Backlog |
| [US-087](./02-user-stories.md#us-087) | Compile evaluation report | X-Research | 5 | Sprint 6 | Backlog |
| [US-086](./02-user-stories.md#us-086) | End-to-end integration test suite | X-Research | 8 | Sprint 6 | Backlog |
| [US-084](./02-user-stories.md#us-084) | Execute RQ1/RQ2 physical Gateway experiments | X-Research | 13 | Sprint 6 | Backlog |
| [US-085](./02-user-stories.md#us-085) | Execute RQ3 randomized SOS drills | X-Research | 13 | Sprint 6 | Backlog |

