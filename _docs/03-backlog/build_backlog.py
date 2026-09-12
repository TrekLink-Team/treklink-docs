#!/usr/bin/env python3
"""
TrekLink Backlog Generator — single source of truth for:
  - treklink-docs/_docs/03-backlog/01-epics.md
  - treklink-docs/_docs/03-backlog/02-user-stories.md
  - User_Story_Agile_TrekLink.xlsx (Backlog / Epic Summary & Traceability / Workload Summary)

Design choices (stated explicitly, not silently assumed — per TrekLink's
"decisions must be explicit and traceable" convention):
  - Epic taxonomy: the 7 epics already locked in
    02-templates/05-user-story-template.md, plus an 8th (Research &
    Experimental Evaluation) added this session to home RQ1-RQ3/TP6.
  - Story granularity: FINE — one story per discrete actor-action, per the
    explicit instruction that coarse epics create development ambiguity.
  - Sprint pre-population: every story is pre-mapped to a Sprint using the
    TP-to-week table in 00-project-context/02-roadmap-and-milestones.md.
    Status is "Ready" only for the 4 stories that are genuinely started
    this sprint (Sprint 1 = Week 1-2, gateway-sync + auth per your answer);
    everything else is "Backlog" pending team sprint planning.
  - Assignment: primary owner chosen from the team skill matrix
    (01-project-charter.md), Khoa (Leader, only NestJS-listed member) set
    as Reviewer/Architect on backend-heavy stories rather than sole owner.
  - Session 2 rearrangement (per Khoa's explicit direction): Khoa's role
    shifts toward PO/reviewer/end-user-testing, so his primary ownership is
    now bounded to schema-freezing, FSM-engine, idempotency, and PoC/
    decision-closing stories (US-001/008/013/041/042/046/050/052/054/057)
    plus E8 research-design/evaluation work and DevOps (US-075/076/080),
    rather than routine CRUD. Competence ranking supplied by Khoa (TanNB >
    Khoa > LongLP; HoangTK unproven; LongNN reliable on chores but not on
    quality/deadline-sensitive work) drives three changes: (1) LongNN is
    removed entirely from DevOps/E7 (US-075, US-078 reassigned) but keeps
    his existing CRUD-tier stories elsewhere; (2) TanNB is delegated more
    (E7 CD pipeline, E5 WebSocket infra US-053/058); (3) LongLP keeps
    Gateway/E4 build-out but is no longer solo on either 8-point item
    (US-041, US-048) — Khoa now owns or co-owns the two riskiest E4
    stories plus the D-005-closing PoC (US-046).
  - Backlog sheet ordering: Epics first (E1..E8, structural header rows with
    rollup totals), then that epic's stories sorted by Story Points
    ascending — this satisfies "arrange it per story points" at the level
    where teams actually use it (sequencing work within an epic) while
    keeping epic traceability intact instead of scattering a flat global
    sort. If a pure flat global sort was intended instead, say so and I'll
    regenerate.
"""
import copy

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

# ---------------------------------------------------------------------------
# 1. TEAM (skill matrix, from the project charter)
# ---------------------------------------------------------------------------
TEAM = {
    "Khoa": {
        "full_name": "Đỗ Đăng Khoa",
        "code": "KhoaDD",
        "mssv": "SE192357",
        "skills": "Embedded C, Spring Boot, Java, ReactJS, TypeScript, NestJS, PostgreSQL",
        "role": "Leader",
    },
    "LongLP": {
        "full_name": "Lâm Phi Long",
        "code": "LongLP",
        "mssv": "SE182769",
        "skills": "PostgreSQL, Node.js, ReactJS, TypeScript",
        "role": "Member",
    },
    "HoangTK": {
        "full_name": "Trần Khải Hoàng",
        "code": "HoangTK",
        "mssv": "SE182767",
        "skills": "Node.js, ReactJS",
        "role": "Member",
    },
    "LongNN": {
        "full_name": "Nguyễn Ngọc Long",
        "code": "LongNN",
        "mssv": "SE193490",
        "skills": "Java Spring Boot, ReactJS, TypeScript, PostgreSQL",
        "role": "Member",
    },
    "TanNB": {
        "full_name": "Nguyễn Bá Tân",
        "code": "TanNB",
        "mssv": "SE183860",
        "skills": "PostgreSQL, MySQL, ReactJS, TypeScript",
        "role": "Member",
    },
}

# ---------------------------------------------------------------------------
# 2. EPICS
# ---------------------------------------------------------------------------
EPICS = [
    {
        "id": "E1",
        "name": "Identity & RBAC",
        "modules": ["auth"],
        "desc": (
            "Registration, login, password recovery, refresh-token session security, and a "
            "data-driven Role & Permission (RBAC/CASL) model so Admin/Staff/Guide/Customer "
            "access control can evolve without code changes."
        ),
        "tables": "users, roles, permissions, role_permissions, refresh_tokens",
        "sprint_range": "Sprint 1-3 (TP1 + TP3)",
    },
    {
        "id": "E2",
        "name": "Device Fleet & Maintenance",
        "modules": ["devices"],
        "desc": (
            "Physical TrekLink device registration across hardware variants v1-v4, the "
            "7-state rental lifecycle FSM, telemetry ingestion, maintenance scheduling, and "
            "damage logging."
        ),
        "tables": "devices, device_types, device_telemetry, maintenance_logs, damage_logs",
        "sprint_range": "Sprint 3-4 (TP3)",
    },
    {
        "id": "E3",
        "name": "Trip & Rental Management",
        "modules": ["trips", "rentals"],
        "desc": (
            "Trek package browsing/booking, device reservation and allocation, rental "
            "agreements, deposit/check-out/check-in workflow, late-return and damage fees, "
            "and Guide-to-trip assignment."
        ),
        "tables": "trek_packages, trips, bookings, rentals, rental_agreements",
        "sprint_range": "Sprint 3-5 (TP3 + TP5)",
    },
    {
        "id": "E4",
        "name": "Gateway & Offline Sync",
        "modules": ["gateway-sync"],
        "desc": (
            "The eventId scheme, SQLite priority queue (P0-P3), MQTT publish/reconnect-flush "
            "on the gateway, and idempotent event ingestion + sync audit log on the backend. "
            "The module most different from a normal CRUD app — graded on delivery rate, "
            "duplicate rate, and priority-ordering compliance."
        ),
        "tables": "gateway_events, event_queue (gateway-local SQLite), sync_audit_log",
        "sprint_range": "Sprint 1-3 (TP1 + TP2)",
    },
    {
        "id": "E5",
        "name": "Real-Time Monitoring & SOS Incidents",
        "modules": ["monitoring", "incidents"],
        "desc": (
            "Live map/telemetry dashboard over WebSocket, automatic SOS-to-Incident creation "
            "on idempotency pass, the 5-state Incident FSM with append-only audit trail, and "
            "Staff/Guide acknowledgment-and-response workflow (MTTA/MTTR are graded RQ3 "
            "metrics)."
        ),
        "tables": "incidents, incident_audit_log, device_positions (live, via WebSocket)",
        "sprint_range": "Sprint 3-5 (TP4)",
    },
    {
        "id": "E6",
        "name": "Billing & Reporting",
        "modules": ["billing"],
        "desc": (
            "Rental pricing rules, automatic invoice generation, mock/sandbox payment status "
            "tracking, and usage/incident/utilization reporting for agency management."
        ),
        "tables": "pricing_rules, invoices, payments (sandbox), reports (derived views)",
        "sprint_range": "Sprint 4-5 (TP5)",
    },
    {
        "id": "E7",
        "name": "DevOps / CI-CD",
        "modules": ["devops"],
        "desc": (
            "Docker Compose for all services, GitHub Actions CI (lint/typecheck/test/build) "
            "and CD, health-check endpoint, environment configuration matrix, deployment "
            "guide, and demo seed data."
        ),
        "tables": "n/a (infrastructure)",
        "sprint_range": "Sprint 1, 4, 7 (ongoing + TP6 close)",
    },
    {
        "id": "E8",
        "name": "Research & Experimental Evaluation",
        "modules": ["docs"],
        "desc": (
            "Added this session — homes the graded RQ1-RQ3 work that doesn't fit the other 7 "
            "template epics: the connectivity-loss experiment protocol/execution (RQ1/RQ2), "
            "the SOS-drill protocol/execution (RQ3), the end-to-end verification suite, and "
            "the evaluation report feeding Defense 1."
        ),
        "tables": "n/a (experiment protocol + evaluation report)",
        "sprint_range": "Sprint 5-7 (TP6)",
    },
]
EPIC_BY_ID = {e["id"]: e for e in EPICS}

# ---------------------------------------------------------------------------
# 3. STORIES
# Fields: id, epic, module, actor, summary, story, ac[3], priority, points,
#         sprint, status, assignee, secondary, reviewer
# ---------------------------------------------------------------------------
STORIES = []


def add(epic, module, actor, summary, story, ac, priority, points, sprint,
        assignee, secondary=None, reviewer="Khoa", status=None):
    n = len(STORIES) + 1
    STORIES.append({
        "id": f"US-{n:03d}",
        "epic": epic,
        "module": module,
        "actor": actor,
        "summary": summary,
        "story": story,
        "ac": ac,
        "priority": priority,
        "points": points,
        "sprint": sprint,
        "status": status or ("Ready" if sprint == 1 else "Backlog"),
        "assignee": assignee,
        "secondary": secondary,
        "reviewer": reviewer,
    })


# --- E1 Identity & RBAC ----------------------------------------------------
add("E1", "auth", "Admin",
    "Data-driven Role & Permission (RBAC) schema",
    "As an Admin, I want roles and permissions stored as data (not hardcoded), "
    "so that access control can evolve without a code deploy.",
    ["The system SHALL persist roles, permissions, and role-permission mappings as queryable entities.",
     "WHEN a permission is added to a role, the system SHALL apply it on the next request without a redeploy.",
     "The default seed SHALL include Admin/Staff/Guide/Customer roles matching the charter's actor table."],
    "High", 5, 1, "Khoa", reviewer="Khoa")

add("E1", "auth", "Customer",
    "Account registration",
    "As a Customer (or Staff/Guide provisioned by Admin), I want to register an account with "
    "email + password, so that I can access my role's features.",
    ["WHEN a registration request has a unique email and a password meeting policy, the system SHALL create the account and hash the password with bcrypt.",
     "IF the email is already registered, THEN the system SHALL reject with 409 Conflict and a field-scoped message.",
     "The system SHALL assign the Customer role by default; Admin/Staff/Guide accounts are provisioned by an Admin (see US-008)."],
    "High", 3, 2, "LongLP", secondary="HoangTK")

add("E1", "auth", "Customer",
    "Login issues JWT access + refresh token",
    "As any registered user, I want to log in and receive an access token and a refresh token, "
    "so that I can call protected endpoints without re-entering credentials each request.",
    ["WHEN credentials are valid, the system SHALL return a short-lived JWT access token and a longer-lived refresh token.",
     "IF credentials are invalid, THEN the system SHALL return 401 Unauthorized without revealing whether the email or password was wrong.",
     "The response envelope SHALL match API_Design_Template.md exactly (result/isSuccess/statusCode/message)."],
    "High", 3, 2, "LongLP", secondary="HoangTK")

add("E1", "auth", "System",
    "Auth audit log (login/logout/failed attempts)",
    "As an Admin, I want login, logout, and failed-attempt events logged, "
    "so that I can investigate suspicious access per the register's Security NFR.",
    ["The system SHALL record actor (user ID or attempted email), event type, IP, and UTC timestamp for every auth event.",
     "Failed-login records SHALL NOT store the attempted password in any form.",
     "Records SHALL be append-only (no update/delete endpoint exposed)."],
    "Medium", 3, 2, "TanNB", reviewer="Khoa")

add("E1", "auth", "System",
    "Refresh-token rotation & silent session renewal",
    "As a logged-in user, I want my session to silently renew via the refresh token, "
    "so that I'm not forced to log in again every few minutes.",
    ["WHEN a valid, unexpired refresh token is presented, the system SHALL issue a new access token and rotate the refresh token.",
     "IF a refresh token is reused after rotation (replay), THEN the system SHALL revoke the whole token family and force re-login.",
     "The frontend apiClient SHALL implement a silent-refresh interceptor per 06-frontend-conventions.md §6.1."],
    "High", 5, 3, "LongLP", secondary="Khoa", reviewer="Khoa")

add("E1", "auth", "System",
    "Logout / token revocation",
    "As a logged-in user, I want to log out and have my refresh token revoked, "
    "so that a stolen token can't be used to renew my session afterward.",
    ["WHEN a logout request is received, the system SHALL revoke the presented refresh token immediately.",
     "The system SHALL clear any server-side session state associated with that token.",
     "A revoked refresh token SHALL return 401 on any subsequent renewal attempt."],
    "Medium", 2, 3, "LongLP")

add("E1", "auth", "Customer",
    "Password reset / recovery",
    "As a user who forgot their password, I want to request a reset link/code and set a new "
    "password, so that I regain access without contacting an Admin.",
    ["WHEN a reset is requested for a known email, the system SHALL issue a single-use, time-limited reset token and SHALL NOT reveal whether the email exists.",
     "WHEN a valid reset token and a policy-compliant new password are submitted, the system SHALL update the password hash and invalidate the token.",
     "IF the reset token is expired or already used, THEN the system SHALL reject with a clear error and no partial state change."],
    "Medium", 3, 3, "HoangTK", reviewer="Khoa")

add("E1", "auth", "System",
    "CASL PoliciesGuard enforcement",
    "As a developer, I want a reusable PoliciesGuard + @CheckPolicies decorator wired globally, "
    "so that every mutating endpoint across all modules enforces RBAC consistently.",
    ["The system SHALL expose a PoliciesGuard usable via @UseGuards(JwtAuthGuard, PoliciesGuard) on any controller.",
     "IF a valid JWT holds insufficient role/CASL permission for the action, THEN the system SHALL return 403 Forbidden via the GlobalExceptionFilter envelope.",
     "The guard SHALL be unit-tested against at least one allow and one deny case per role."],
    "High", 5, 3, "Khoa", reviewer="Khoa")

add("E1", "auth", "Admin",
    "Admin: manage user accounts",
    "As an Admin, I want to list, create, deactivate, and role-assign user accounts, "
    "so that I can provision Staff/Guide accounts and manage access.",
    ["The system SHALL provide a paginated list of accounts filterable by role and active status.",
     "WHEN an Admin deactivates an account, the system SHALL immediately reject that account's existing refresh tokens.",
     "Only Admin-role callers SHALL be authorized to create Staff/Guide accounts or change a user's role."],
    "Medium", 5, 3, "LongNN", secondary="HoangTK")

add("E1", "auth", "Guide",
    "Guide profile management",
    "As a Guide, I want to see my profile with assigned trips and device-handling history, "
    "so that I have a single view of my responsibilities.",
    ["The system SHALL show the Guide's currently assigned trips and their status.",
     "The system SHALL show a chronological device-handling history (check-out/check-in events) for that Guide.",
     "A Guide SHALL only be able to view their own profile, not another Guide's (ownership check)."],
    "Low", 3, 3, "HoangTK")

# --- E2 Device Fleet & Maintenance ------------------------------------------
add("E2", "devices", "Admin",
    "Manage device type / hardware variant catalog",
    "As an Admin, I want to manage the catalog of device types, hardware variants (v1-v4), and "
    "firmware versions, so that new physical units can be registered against a known type.",
    ["The system SHALL allow Admin to create/edit a device type with hardware variant and firmware version fields.",
     "The device registration endpoint (US-012) SHALL only accept a hardwareVariant that exists in this catalog.",
     "The system SHALL NOT allow deleting a device type that has registered devices (referential integrity)."],
    "Medium", 3, 3, "LongNN", reviewer="Khoa")

add("E2", "devices", "Admin",
    "Register a physical TrekLink device",
    "As an Admin, I want to register a new physical device (device ID, hardware variant, "
    "firmware version), so that it enters the fleet as Available.",
    ["WHEN a valid, unique device ID is submitted, the system SHALL create the device with status=Available.",
     "IF the device ID already exists, THEN the system SHALL reject with 409 Conflict.",
     "The created device SHALL default battery/telemetry fields to null until the first telemetry event arrives (US-016)."],
    "High", 3, 3, "LongLP")

add("E2", "devices", "System",
    "Device 7-state lifecycle FSM engine",
    "As a developer, I want an explicit transition table for the device lifecycle "
    "(Available→Reserved→Rented→In-Field→Returned→Maintenance→Retired), so that every status "
    "change is validated and auditable, not an ad-hoc field write.",
    ["The system SHALL reject any status transition not present in the allowed-transitions table (04-architecture-conventions.md §2.1) with 409 Conflict.",
     "Every successful transition SHALL write an append-only audit row (actor, from-state, to-state, UTC timestamp).",
     "The FSM SHALL be unit-tested for every legal transition and at least one illegal transition per state."],
    "High", 8, 3, "Khoa", secondary="LongNN", reviewer="Khoa")

add("E2", "devices", "System",
    "Prevent allocation of unavailable devices",
    "As the system, I want to refuse allocating a device that is in Maintenance, Retired, or "
    "past its scheduled maintenance date, so that Staff can't accidentally rent out an unsafe unit.",
    ["WHILE a device is in Maintenance or Retired status, the system SHALL reject any allocation request referencing it (409 Conflict, DEVICE_NOT_ALLOCATABLE).",
     "IF a device's scheduled maintenance date has passed without being cleared, THEN the system SHALL block allocation even if status is still Available.",
     "This check SHALL run inside the same transaction as the allocation write (no check-then-write race)."],
    "High", 5, 3, "LongNN", reviewer="Khoa")

add("E2", "devices", "Staff",
    "Device fleet list with filters",
    "As Staff/Admin, I want to see the device list filterable by status, hardware variant, and "
    "battery level, so that I can find an available device quickly during allocation.",
    ["The system SHALL support filtering by status and hardwareVariant, and sorting by lastSeenAt/batteryPct.",
     "The response SHALL use the standard PagedResultDto shape (05-backend-conventions.md §3.2).",
     "The frontend list screen SHALL follow Pattern A (List & Search) from 06-frontend-conventions.md §4."],
    "Medium", 3, 4, "TanNB", secondary="HoangTK")

add("E2", "devices", "Staff",
    "Device detail view",
    "As Staff/Admin, I want a single device's detail page (current assignment, telemetry, "
    "history), so that I can inspect one unit without cross-referencing multiple screens.",
    ["The system SHALL return the device's current rental/trip assignment (if any) alongside its own fields.",
     "The detail view SHALL show the most recent 20 telemetry readings.",
     "The frontend SHALL link to this view from the fleet list row's Actions menu."],
    "Low", 2, 4, "HoangTK")

add("E2", "devices", "System",
    "Ingest device telemetry from Gateway",
    "As the system, I want to accept battery %, last-seen timestamp, and last GPS fix from "
    "gateway-sync events, so that the fleet view reflects real field state.",
    ["WHEN a telemetry-type gateway event is ingested, the system SHALL update the device's batteryPct, lastSeenAt, and last known position.",
     "The system SHALL discard telemetry with an older timestamp than the device's current lastSeenAt (out-of-order protection).",
     "This handler SHALL reuse the idempotent ingestion path from E4 (US-049), not a separate endpoint."],
    "High", 5, 4, "LongLP", secondary="Khoa")

add("E2", "devices", "Staff",
    "Schedule device maintenance",
    "As Staff, I want to move a device into Maintenance and schedule when it should return to "
    "service, so that damaged/due-for-service units aren't rented out.",
    ["WHEN Staff transitions a device to Maintenance, the system SHALL require a reason and SHALL accept an optional scheduled-return date.",
     "The transition SHALL go through the FSM guard (US-013) — only Available/Returned devices can enter Maintenance.",
     "The device SHALL remain excluded from allocation until explicitly transitioned back to Available."],
    "Medium", 3, 4, "LongNN")

add("E2", "devices", "Staff",
    "Log device damage on return inspection",
    "As Staff, I want to log a damage/incident report against a device during return "
    "inspection, so that repeated damage and fee calculation (US-036) have a record to reference.",
    ["The system SHALL let Staff attach a damage report (description, severity, optional photo reference) to a Returned device.",
     "A logged damage report SHALL be visible on the device's history (US-022) permanently (no hard delete).",
     "Logging a damage report SHALL NOT itself change device status — Staff separately decides Maintenance vs. re-Available."],
    "Medium", 3, 4, "TanNB")

add("E2", "devices", "Admin",
    "Retire a device",
    "As an Admin, I want to retire a device permanently, so that end-of-life units stop "
    "appearing as allocatable without deleting their historical records.",
    ["WHEN a device is retired, the system SHALL set status=Retired, a terminal state with no further outgoing transitions per the FSM.",
     "Retiring SHALL NOT delete the device row or its history — this is a status transition, not a DELETE (per the no-hard-deletes convention).",
     "IF the device has an active rental/trip assignment, THEN retirement SHALL be rejected until that assignment ends."],
    "Low", 2, 4, "LongNN")

add("E2", "devices", "Staff",
    "Device fleet dashboard widget",
    "As Staff/Admin, I want a summary widget of device counts by status, so that I can see "
    "fleet health at a glance without opening the full list.",
    ["The widget SHALL show a count per status (Available/Reserved/Rented/In-Field/Returned/Maintenance/Retired).",
     "Counts SHALL update on dashboard load via the standard TanStack Query cache (no separate polling mechanism).",
     "Clicking a status count SHALL deep-link to the filtered fleet list (US-014)."],
    "Low", 2, 4, "HoangTK")

add("E2", "devices", "Staff",
    "Device assignment/rental/incident history view",
    "As Staff/Admin, I want a chronological history per device (assignments, rentals, "
    "incidents, maintenance), so that I can audit a unit's full lifecycle for a review or a "
    "customer dispute.",
    ["The system SHALL aggregate rental, incident, and maintenance records for one device into a single chronological feed.",
     "Each entry SHALL show actor, event type, and UTC timestamp, consistent with the Auditability NFR.",
     "The feed SHALL be read-only (no edit/delete affordance) — it's an audit view, not a working list."],
    "Low", 3, 4, "TanNB")

# --- E3 Trip & Rental Management --------------------------------------------
add("E3", "trips", "Admin",
    "Manage trek packages",
    "As an Admin/Staff, I want to create and edit trek packages (route, duration, price, "
    "device requirements), so that Customers have something to browse and book.",
    ["The system SHALL let Admin/Staff create a trek package with route name, duration, base price, and default device count.",
     "An edited package SHALL NOT retroactively change already-confirmed bookings' agreed terms.",
     "The package SHALL support an active/inactive flag so past packages can be hidden without deletion."],
    "Medium", 3, 3, "LongNN", secondary="TanNB")

add("E3", "trips", "Customer",
    "Browse trek packages",
    "As a Customer, I want to browse available trek packages, so that I can choose one to book.",
    ["The system SHALL list only active packages to Customer-role callers.",
     "The list SHALL support filtering by route/duration/price range.",
     "The frontend SHALL follow Pattern A (List & Search) per 06-frontend-conventions.md."],
    "Medium", 2, 4, "HoangTK")

add("E3", "trips", "Customer",
    "Submit a booking request",
    "As a Customer, I want to submit a booking request for a trek package (dates, group size), "
    "so that Staff can review and confirm it.",
    ["WHEN a booking is submitted, the system SHALL create it in a Pending state awaiting Staff review.",
     "The system SHALL validate group size against the package's constraints before accepting.",
     "The booking form SHALL follow the 4-step/6-field UX rule (06-frontend-conventions.md §3)."],
    "High", 5, 4, "LongLP", secondary="HoangTK")

add("E3", "rentals", "Customer",
    "Reserve devices during booking",
    "As a Customer, I want to reserve TrekLink devices for my group as part of booking, so that "
    "the agency knows how many units to hold before Staff finalizes allocation.",
    ["WHEN a booking is submitted with a device count, the system SHALL create a soft device Reservation not yet bound to specific device IDs.",
     "The reserved count SHALL NOT exceed the package's max-device constraint.",
     "This reservation SHALL be converted to a specific-device allocation only at Staff review (US-028), not before."],
    "Medium", 5, 4, "LongLP")

add("E3", "trips", "Staff",
    "Review and approve/reject a booking",
    "As Staff, I want to review a Pending booking and approve or reject it, so that only "
    "feasible bookings proceed to device allocation.",
    ["WHEN Staff approves, the system SHALL transition the booking to Confirmed and unlock device allocation (US-028).",
     "WHEN Staff rejects, the system SHALL transition to Rejected with a required reason, releasing any soft reservation.",
     "Only Staff/Admin-role callers SHALL be authorized to approve/reject."],
    "High", 3, 4, "LongNN")

add("E3", "rentals", "Staff",
    "Allocate specific devices to a confirmed booking",
    "As Staff, I want to allocate specific available devices to a confirmed booking, so that "
    "each unit is traceable to the group renting it.",
    ["The system SHALL only allow allocating devices currently in Available status (reuses the US-019 guard).",
     "WHEN allocation succeeds, the system SHALL transition each allocated device to Reserved.",
     "IF fewer devices are Available than the booking requires, THEN the system SHALL reject the allocation with a clear count mismatch error."],
    "High", 5, 4, "LongLP", reviewer="Khoa")

add("E3", "trips", "Staff",
    "Assign a Guide to a trip",
    "As Staff, I want to assign a Guide to a confirmed trip together with its allocated device "
    "set, so that the Guide's profile (US-009) and live monitoring (E5) know which trip/devices "
    "they own.",
    ["The system SHALL only allow assigning a user with the Guide role.",
     "A Guide SHALL NOT be assigned to two trips with overlapping date ranges.",
     "The assignment SHALL be visible on the Guide's own profile view (US-009) immediately."],
    "Medium", 3, 4, "LongNN")

add("E3", "rentals", "Staff",
    "Generate rental agreement",
    "As Staff, I want to generate a rental agreement document for a confirmed, allocated "
    "booking, so that there's a formal record of what was rented, deposit terms, and fee rules.",
    ["The system SHALL generate the agreement from the booking + device allocation + pricing rule (E6) data, not free-typed fields.",
     "The generated agreement SHALL be immutable once check-out (US-032) begins — later changes create an addendum, not an edit.",
     "The agreement SHALL be retrievable by Staff, the assigned Guide, and the booking Customer."],
    "Medium", 5, 5, "LongLP")

add("E3", "rentals", "Staff",
    "Record deposit",
    "As Staff, I want to record a deposit payment against a rental agreement, so that "
    "check-out (US-032) can be gated on deposit received.",
    ["The system SHALL record deposit amount, method, and timestamp against the rental agreement.",
     "Check-out (US-032) SHALL be blocked if the required deposit is not marked received.",
     "This uses the same mock/sandbox payment status model as E6, not a separate ad-hoc field."],
    "Medium", 2, 5, "TanNB")

add("E3", "rentals", "Staff",
    "Device check-out workflow",
    "As Staff, I want a check-out workflow that issues the allocated devices to the group, so "
    "that device status correctly reflects Rented → In-Field as the trip begins.",
    ["WHEN check-out is completed, the system SHALL transition each allocated device Reserved→Rented, then In-Field once the trip start is confirmed.",
     "Check-out SHALL be blocked if deposit (US-031) is not recorded.",
     "Each device transition SHALL go through the FSM guard (US-013), not a direct field write."],
    "High", 5, 5, "LongLP", reviewer="Khoa")

add("E3", "trips", "Guide",
    "Guide confirms device receipt/handover",
    "As a Guide, I want to confirm receipt of the handed-over devices at check-out, so that "
    "there's a two-party (Staff + Guide) record of what physically changed hands.",
    ["The system SHALL require a Guide-side confirmation action before check-out (US-032) is considered complete.",
     "IF the Guide's confirmed device list differs from Staff's allocated list, THEN the system SHALL flag a mismatch for Staff to resolve before proceeding.",
     "This confirmation SHALL be timestamped and attributed to the specific Guide account."],
    "Medium", 3, 5, "HoangTK")

add("E3", "rentals", "Staff",
    "Device check-in workflow on return",
    "As Staff, I want a check-in workflow when the group returns, so that devices transition "
    "In-Field→Returned and become eligible for inspection/fee calculation.",
    ["WHEN check-in is completed, the system SHALL transition each returned device to Returned via the FSM guard.",
     "The system SHALL capture a check-in timestamp used as the basis for late-return fee calculation (US-035).",
     "Devices not physically returned SHALL remain In-Field and be flagged for Staff follow-up, not silently marked Returned."],
    "High", 5, 5, "LongLP")

add("E3", "rentals", "System",
    "Calculate late-return fee",
    "As the system, I want to calculate a late-return fee when check-in happens after the "
    "agreed return date, so that billing (E6) has an accurate invoice line item.",
    ["WHEN check-in timestamp exceeds the rental agreement's agreed return date, the system SHALL calculate a fee using the pricing rule's late-fee formula (E6).",
     "The calculated fee SHALL be itemized separately from the base rental charge on the resulting invoice (US-068).",
     "On-time check-in SHALL produce zero late fee, not a null/undefined field."],
    "Medium", 3, 5, "TanNB")

add("E3", "rentals", "System",
    "Calculate damage fee",
    "As the system, I want to calculate a damage fee from the device's logged damage report "
    "(US-018), so that billing reflects repair/replacement cost.",
    ["WHEN check-in inspection logs a damage report with a severity tier, the system SHALL calculate a fee from the pricing rule's damage-fee table.",
     "A device with no damage report at check-in SHALL produce zero damage fee.",
     "The fee calculation SHALL be traceable to the specific damage-log entry it was derived from."],
    "Medium", 3, 5, "TanNB")

add("E3", "trips", "Guide",
    "Guide: view assigned trips, group, devices",
    "As a Guide, I want to see my assigned trips, the customer group, and the allocated device "
    "set, so that I know what I'm responsible for before departure.",
    ["The system SHALL scope this view to only trips where the caller is the assigned Guide.",
     "The view SHALL show each allocated device's ID and current status.",
     "The view SHALL show the customer group's roster (names, contact) for that trip."],
    "Medium", 3, 5, "HoangTK")

add("E3", "monitoring", "Guide",
    "Guide: live group position/device status during trip",
    "As a Guide, I want to see my group's live position and device status while on an active "
    "trip, so that I have field situational awareness (this read model is populated by E5's "
    "monitoring pipeline).",
    ["WHILE a trip is In-Field, the system SHALL show live device positions/status to the assigned Guide via the shared WebSocket channel (US-053).",
     "This view SHALL reuse the LiveMapWidget (US-054) rather than a separate Guide-only map implementation.",
     "If the gateway is stale/disconnected, the view SHALL surface that state (US-065) rather than showing silently outdated positions."],
    "Medium", 5, 5, "TanNB", secondary="HoangTK")

add("E3", "trips", "Customer",
    "Customer: view booking/rental/deposit/payment info",
    "As a Customer, I want to view my booking, rental, deposit, and payment status, so that I "
    "know where things stand without contacting Staff.",
    ["The system SHALL scope this view to only bookings owned by the calling Customer.",
     "The view SHALL show current booking status, deposit status, and any calculated fees once available.",
     "This view SHALL reuse the billing status model from E6, not duplicate payment-state logic."],
    "Low", 3, 5, "HoangTK")

add("E3", "trips", "Customer",
    "Customer: view trip & rental history",
    "As a Customer, I want to see my past trips and rentals, so that I can reference or rebook "
    "a previous package.",
    ["The system SHALL list the Customer's completed/past bookings in reverse-chronological order.",
     "Each history entry SHALL link to that booking's rental agreement and final invoice.",
     "This is a read-only view — no edit affordance on historical records."],
    "Low", 2, 5, "HoangTK")

# --- E4 Gateway & Offline Sync -----------------------------------------------
add("E4", "gateway-sync", "System",
    "LoRa-to-Gateway serial parser (PoC)",
    "As the Gateway, I want to parse LoRa mesh messages received over serial from the "
    "TrekLink firmware, so that position/SOS/telemetry packets can be enqueued for sync. "
    "This is TP1's explicit Week 1-2 PoC exit gate.",
    ["The parser SHALL correctly decode the firmware's message schema for position, SOS, and telemetry packet types.",
     "The parser SHALL be unit-testable against captured/sample serial payloads without live hardware.",
     "This PoC SHALL be completed and demoed by TP1 Week 2 per the roadmap's risk mitigation for underestimated integration effort."],
    "High", 8, 1, "Khoa", secondary="LongLP", reviewer="Khoa")

add("E4", "gateway-sync", "System",
    "Freeze the eventId schema",
    "As the team, we want the eventId scheme frozen and documented in specs/gateway-sync/design.md, "
    "so that every downstream module (gateway queue, backend ingestion, incidents) builds against "
    "one stable contract. RESOLVED as D-006: the original deviceId+sessionId+sequenceNumber form is "
    "NOT constructible - the firmware transmits neither sessionId nor sequenceNumber. Replaced by a "
    "split key: GatewayEvent.eventId = sha256(nodeNum:packetId) for packet dedup, plus an open-Incident "
    "lookup (not a hash) for episode correlation.",
    ["The schema SHALL be documented in design.md before any gateway or backend ingestion code is written (hard TP1 gate). [DONE - design.md sections 1.1-2.4]",
     "The eventId SHALL be usable as a natural idempotency key (unique, deterministic, derived from data the firmware actually transmits).",
     "Any change to this schema after freeze SHALL be logged as a new decision in 03-decisions-and-risk-register.md, not a silent edit. [Honoured - see D-006.]",
     "Per D-008 the firmware is editable: adding a boot sessionId + per-packet sequenceNumber firmware-side would restore the original scheme AND enable gap detection (proving loss, not just deduplicating arrivals). Evaluate as a layered upgrade - the split key stands either way."],
    "High", 3, 1, "Khoa", reviewer="Khoa")

add("E4", "gateway-sync", "System",
    "SQLite local priority queue schema",
    "As the Gateway, I want a local SQLite table with P0-P3 priority tiers, so that events "
    "persist across connectivity loss instead of being lost in memory.",
    ["The schema SHALL include id, eventId, priority (P0-P3), payload, createdAt, retryCount.",
     "eventId SHALL carry a unique constraint at the gateway level too, not just backend-side.",
     "The queue logic SHALL be isolated from MQTT transport code so it's unit-testable without a live broker (04-architecture-conventions.md §3)."],
    "High", 5, 2, "LongLP")

add("E4", "gateway-sync", "System",
    "Enqueue incoming LoRa events into the priority queue",
    "As the Gateway, I want every parsed LoRa event enqueued with its correct priority tier "
    "(SOS=P0, incident-location=P1, GPS=P2, telemetry=P3), so that safety-critical events are "
    "never silently dropped.",
    ["WHEN a message is parsed (US-041), the system SHALL classify it into P0-P3 and insert it into the local queue before any network attempt.",
     "The system SHALL persist the event even if MQTT is unreachable at enqueue time.",
     "Classification SHALL be unit-tested for at least one example of each priority tier."],
    "High", 5, 2, "LongLP")

add("E4", "gateway-sync", "System",
    "Gateway-side duplicate suppression",
    "As the Gateway, I want to suppress re-enqueuing an eventId already in the local queue or "
    "already flushed, so that flaky serial reads don't multiply the same event before it even "
    "reaches the backend.",
    ["IF an incoming eventId matches one already queued or already marked flushed, THEN the system SHALL discard the duplicate without re-inserting.",
     "This check SHALL use the gateway-local unique constraint (US-043) as the enforcement mechanism, not just an in-memory set.",
     "This is a defense-in-depth layer — backend idempotency (US-049) is still required and is the authoritative guarantee."],
    "Medium", 3, 2, "LongLP")

add("E4", "gateway-sync", "System",
    "D-005 Gateway connectivity PoC",
    "As the team, we want to validate that the firmware's built-in Meshtastic MQTT-uplink "
    "module is sufficient for Wi-Fi/cellular connectivity at basecamp, so that D-005 (dedicated "
    "Gateway hardware vs. phone-bridging) can be closed before TP2 sprint planning locks in scope.",
    ["The PoC SHALL demonstrate a TrekLink node publishing position/SOS/telemetry via its built-in MQTT module to our broker, no firmware or mobile-app changes.",
     "The PoC result SHALL be logged back into D-005 in 03-decisions-and-risk-register.md as Resolved or Re-opened with evidence, not left implicit.",
     "IF Option 1 (dedicated hardware) proves insufficient, THEN this story blocks TP2 Gateway Bridge scope until escalated to the supervisor per D-005's Action clause."],
    "High", 5, 2, "Khoa", secondary="LongLP", reviewer="Khoa")

add("E4", "gateway-sync", "System",
    "MQTT publish client (gateway → broker)",
    "As the Gateway, I want an MQTT client that publishes queued events to the broker, so that "
    "the backend can receive them whenever connectivity is available.",
    ["The system SHALL publish using MQTT QoS 1 (at-least-once), matching the register's stated protocol choice.",
     "A successful publish acknowledgment SHALL mark the corresponding queue row as flushed, not delete it (audit trail).",
     "Publish failures SHALL leave the row queued for the next flush attempt, not silently drop it."],
    "High", 5, 3, "LongLP", reviewer="Khoa")

add("E4", "gateway-sync", "System",
    "Reconnection detection + priority-ordered flush",
    "As the Gateway, I want to detect reconnection and flush the queue in strict priority "
    "order (all P0 before any P2/P3), so that safety-critical events are never delayed behind "
    "routine telemetry — this is a graded NFR (≥99% priority-ordering compliance).",
    ["WHEN connectivity is restored, the system SHALL flush queued events ORDER BY priority ASC, createdAt ASC.",
     "The flush routine SHALL be interruptible and resumable — a second connectivity drop mid-flush SHALL NOT lose or reorder remaining events.",
     "This SHALL be integration-tested against simulated 30s/2min/5min/10min/30min connectivity-loss windows per the register's experiment matrix."],
    "High", 8, 3, "LongLP", secondary="Khoa", reviewer="Khoa")

add("E4", "gateway-sync", "System",
    "Gateway health-reporting API",
    "As Staff/Admin, I want a gateway health endpoint (queue depth per tier, last sync time, "
    "retry count), so that the monitoring dashboard (E5) can surface gateway connectivity "
    "status instead of it being a black box.",
    ["The endpoint SHALL report queue depth broken down by P0-P3 tier.",
     "The endpoint SHALL report lastSyncAt and the current retry count for the oldest queued event.",
     "This endpoint is what US-065 (connectivity indicator) consumes — it SHALL NOT be duplicated as a separate ad-hoc status field."],
    "Medium", 3, 3, "TanNB")

add("E4", "gateway-sync", "System",
    "Backend: idempotent event ingestion endpoint",
    "As the backend, I want to ingest gateway events using eventId as the idempotency key "
    "inside one DB transaction, so that N deliveries of the same event produce exactly one "
    "downstream effect (Incident, telemetry update, etc.).",
    ["The system SHALL enforce a DB-level unique constraint on eventId as the last line of defense, not only an application-level check.",
     "The idempotency check and any side-effect (e.g. Incident creation) SHALL happen inside the same transaction — never check-then-create as two round-trips.",
     "This SHALL pass the register's NFR test: 20 simultaneous submissions of related events, 0 loss/duplication."],
    "High", 8, 3, "Khoa", secondary="LongLP", reviewer="Khoa")

add("E4", "gateway-sync", "System",
    "Backend: synchronization audit log",
    "As Admin, I want a per-event processing history (received, processed, duplicate-rejected), "
    "so that RQ1/RQ2 experiment data (E8) has a source of truth to compute delivery/duplicate "
    "rates from.",
    ["The system SHALL record one audit row per ingestion attempt, including whether it was accepted or rejected as duplicate.",
     "Audit rows SHALL be append-only and queryable by time range and eventId prefix (deviceId).",
     "This log SHALL be the data source for US-083's delivery-rate/duplicate-rate calculations — not a separate export mechanism."],
    "Medium", 5, 3, "TanNB", reviewer="Khoa")

add("E4", "gateway-sync", "System",
    "Automated duplicate-delivery test",
    "As the team, we want an automated test that delivers the same eventId 10 times and "
    "asserts exactly one downstream effect, so that the register's Duplicate Prevention NFR is "
    "continuously verified in CI, not just checked manually once.",
    ["The test SHALL submit the identical event payload 10 times and assert exactly 1 resulting Incident/telemetry update.",
     "The test SHALL run in the backend CI job (E7) on every PR touching gateway-sync or incidents.",
     "A failing run of this test SHALL block merge — it directly verifies a graded NFR."],
    "High", 3, 3, "Khoa", reviewer="Khoa")

# --- E5 Real-Time Monitoring & SOS Incidents --------------------------------
add("E5", "monitoring", "System",
    "WebSocket gateway (Socket.io) for live push",
    "As a developer, I want one shared Socket.io gateway that all live features subscribe to, "
    "so that widgets don't each open their own connection (06-frontend-conventions.md §2).",
    ["The system SHALL expose typed events (e.g. incident:new, device:telemetry) over a single namespace.",
     "Connections SHALL be authenticated via the existing JWT, reusing the auth module rather than a parallel auth scheme.",
     "The frontend SHALL hold this connection in one shared shared/socketClient.ts, not per-widget."],
    "High", 5, 3, "TanNB", reviewer="Khoa")

add("E5", "incidents", "System",
    "Incident 5-state FSM engine",
    "As a developer, I want an explicit transition table for "
    "Detected→Acknowledged→In Progress→Resolved→Closed, so that every incident state change is "
    "guarded and auditable — this FSM is a graded deliverable (UML State Machine diagram).",
    ["The system SHALL reject any transition not in the allowed-transitions table, mirroring the device FSM pattern (04-architecture-conventions.md §2.1).",
     "Every transition SHALL write an append-only audit row: actor (user ID + role), timestamp, action note.",
     "The FSM SHALL be unit-tested for every legal transition and at least one illegal transition per state."],
    "High", 8, 3, "Khoa", reviewer="Khoa")

add("E5", "monitoring", "Staff",
    "Live operational map (Leaflet.js)",
    "As Staff/Admin/Guide, I want a live map showing active trip positions, so that I have "
    "field situational awareness without polling manually.",
    ["The map SHALL render device/trip markers colored by status per Pattern B (06-frontend-conventions.md §4).",
     "Position updates SHALL arrive via the shared WebSocket channel (US-053), not polling.",
     "The map SHALL be the LiveMapWidget consumed by both the Staff dashboard and the Guide's own trip view (US-038)."],
    "High", 8, 4, "TanNB", secondary="HoangTK")

add("E5", "monitoring", "System",
    "Device telemetry live display on map",
    "As Staff/Admin, I want battery and last-seen data shown on the live map markers, so that "
    "I can spot a device about to go dark before it becomes an incident.",
    ["Markers SHALL show battery % and a relative last-seen time (e.g. \"2m ago\").",
     "Stale telemetry (beyond a configurable threshold) SHALL visually distinguish itself from fresh telemetry on the marker.",
     "This reuses the telemetry ingestion pipeline from US-016 — no separate polling endpoint."],
    "Medium", 3, 4, "TanNB")

add("E5", "incidents", "System",
    "Auto-create Incident from a valid SOS event",
    "As the system, I want to automatically create an Incident when a valid SOS event passes "
    "the idempotency check, so that no manual step stands between a firmware SOS broadcast and "
    "a tracked operational response.",
    ["WHEN a SOS-type event passes idempotency (US-049), the system SHALL create exactly one Incident in Detected state within the same transaction.",
     "The Incident SHALL link back to the originating device, trip, and eventId for traceability.",
     "Re-delivery of the same eventId SHALL NOT create a second Incident (reuses US-049's guarantee, not a separate check)."],
    "High", 5, 4, "Khoa", secondary="LongNN", reviewer="Khoa")

add("E5", "incidents", "System",
    "WebSocket push notification within 2 seconds",
    "As Staff/Guide, I want to be notified within 2 seconds of an Incident being created, so "
    "that response time (MTTA, a graded RQ3 metric) starts as close to real SOS trigger as "
    "possible.",
    ["WHEN an Incident is created, the system SHALL push a notification to the assigned trip's Guide and to all online Staff/Admin within 2 seconds under normal load.",
     "The notification payload SHALL include enough context (device, trip, location) to act without an extra fetch.",
     "This latency SHALL be measured and reported as part of US-083/US-085's RQ evaluation, not just asserted."],
    "High", 5, 4, "TanNB", reviewer="Khoa")

add("E5", "incidents", "System",
    "Append-only incident audit trail",
    "As Admin, I want every incident state transition preserved permanently with actor, "
    "timestamp, and note, so that RQ3's traceability-score metric (% of transitions with "
    "complete actor+timestamp+action) can be computed directly from this data.",
    ["Every transition from US-057 SHALL write one audit row — no update/delete endpoint SHALL exist for these rows.",
     "The traceability-score calculation (US-087) SHALL be able to query this table directly without a separate export step.",
     "The audit trail SHALL be visible to Staff/Admin as a read-only timeline on the Incident detail view."],
    "Medium", 3, 4, "TanNB")

add("E5", "incidents", "Staff",
    "Staff: acknowledge an incident",
    "As Staff, I want to acknowledge a Detected incident, so that the system records who is "
    "taking ownership and starts the response clock.",
    ["WHEN Staff acknowledges, the system SHALL transition Detected→Acknowledged via the FSM guard (US-057).",
     "The acknowledgment timestamp SHALL be the value used for MTTA calculation (US-087), not a client-side timestamp.",
     "The acknowledgment action SHALL require no more than 1 step / 2 fields (button + optional note) per the time-critical UX rule (06-frontend-conventions.md §3)."],
    "High", 3, 5, "TanNB", reviewer="Khoa")

add("E5", "incidents", "Staff",
    "Staff: update/coordinate an incident",
    "As Staff, I want to transition an incident to In Progress with a coordination note, so "
    "that the response effort is documented as it happens, not reconstructed afterward.",
    ["WHEN Staff updates status to In Progress, the system SHALL require a non-empty action note.",
     "Multiple In Progress updates SHALL each write a separate audit row, preserving the full coordination timeline.",
     "Only Staff/Admin/the assigned Guide SHALL be authorized to update an incident's status."],
    "Medium", 3, 5, "TanNB")

add("E5", "incidents", "Staff",
    "Staff: close/resolve an incident",
    "As Staff, I want to transition an incident through Resolved to Closed with a resolution "
    "note, so that MTTR (a graded RQ3 metric) and the audit trail have a definite end.",
    ["WHEN Staff resolves, the system SHALL transition In Progress→Resolved, requiring a resolution note.",
     "WHEN Staff closes a Resolved incident, the system SHALL transition Resolved→Closed, the terminal state per the FSM.",
     "The Resolved timestamp SHALL be the value used for MTTR calculation (US-087)."],
    "Medium", 3, 5, "TanNB")

add("E5", "incidents", "Guide",
    "Guide: acknowledge + submit response notes",
    "As a Guide, I want to acknowledge an incident and submit response/resolution notes from "
    "the field, so that Staff has field-level context while coordinating.",
    ["The system SHALL allow the assigned Guide to acknowledge independently of Staff's own acknowledgment — both are recorded, not merged into one flag.",
     "Guide-submitted notes SHALL append to the same audit trail as Staff actions (US-064), attributed correctly by role.",
     "This flow SHALL follow the same 1-step/2-field time-critical UX rule as US-059."],
    "High", 5, 5, "HoangTK", reviewer="Khoa")

add("E5", "incidents", "Staff",
    "Staff: manually create a non-SOS incident",
    "As Staff, I want to manually open an incident for a non-SOS emergency (e.g. a phoned-in "
    "report), so that the same tracked FSM/audit workflow applies even without a device-level "
    "SOS trigger.",
    ["The system SHALL let Staff create an Incident directly in Detected state, optionally linked to a device/trip.",
     "Manually created incidents SHALL go through the identical FSM (US-057) as auto-created ones — no separate code path.",
     "The audit trail SHALL note that the incident was Staff-initiated, not device-triggered, for RQ3 baseline comparison purposes."],
    "Low", 3, 5, "TanNB")

add("E5", "monitoring", "Staff",
    "Gateway connectivity status indicator",
    "As Staff/Admin, I want a visible per-gateway connectivity indicator (last-seen, "
    "\"syncing\" vs. \"stale\") on the dashboard, so that a silent gateway dropout is obvious, "
    "not hidden in a tooltip (06-frontend-conventions.md §4 Pattern B).",
    ["The indicator SHALL consume the gateway health endpoint (US-048) directly.",
     "A gateway with no sync beyond a configurable threshold SHALL visually flip to a \"stale\" state.",
     "The indicator SHALL be visible on the main dashboard, not nested behind a secondary screen."],
    "Medium", 3, 5, "TanNB")

add("E5", "incidents", "Staff",
    "Incident queue panel",
    "As Staff/Admin/Guide, I want a list/filter panel of active incidents beside the map, so "
    "that an active SOS is visible without scrolling (06-frontend-conventions.md §4 Pattern B).",
    ["The panel SHALL list incidents filterable by status and sortable by created time.",
     "An active (non-Closed) incident SHALL visually pulse/highlight per the Pattern B spec.",
     "Selecting an incident SHALL center the live map (US-054) on its associated device/trip."],
    "Medium", 3, 5, "HoangTK")

# --- E6 Billing & Reporting --------------------------------------------------
add("E6", "billing", "Admin",
    "Manage rental pricing rules",
    "As an Admin, I want to configure pricing rules (per device type, per day/trip, late-fee "
    "and damage-fee formulas), so that fee calculation (US-035/036) and invoicing (US-068) "
    "aren't hardcoded.",
    ["The system SHALL let Admin define a base rate per device type and per day/trip.",
     "The system SHALL let Admin define late-fee and damage-fee formulas referenced by US-035/US-036.",
     "A pricing-rule change SHALL apply only to new agreements going forward, never retroactively to signed agreements (matches US-023's non-retroactive principle)."],
    "Medium", 5, 4, "TanNB", reviewer="Khoa")

add("E6", "billing", "System",
    "Automatic invoice generation",
    "As the system, I want to generate an invoice automatically from a completed rental "
    "agreement (base charge + late fee + damage fee), so that Staff don't manually tally "
    "charges.",
    ["WHEN check-in (US-034) completes and all fees (US-035/036) are calculated, the system SHALL generate one invoice itemizing base/late/damage charges.",
     "The invoice SHALL be immutable once generated — corrections require a documented adjustment, not a silent edit.",
     "Invoice generation SHALL be idempotent per rental agreement (re-triggering it SHALL NOT create a duplicate invoice)."],
    "Medium", 5, 5, "TanNB")

add("E6", "billing", "System",
    "Mock/sandbox payment integration",
    "As the system, I want a mock/sandbox payment flow with status tracking (Pending/Paid/"
    "Failed), so that the billing workflow is demonstrable without a production payment "
    "gateway, per the register's explicit MVP scope.",
    ["The system SHALL mark every transaction with a sandbox:true flag per the WHERE-clause requirement in the register.",
     "Payment status SHALL be one of Pending/Paid/Failed, transitioned only through this module — not written directly by other modules.",
     "This SHALL be clearly labeled as sandbox in both API responses and the UI, so it's never mistaken for a real charge."],
    "Low", 3, 5, "TanNB")

add("E6", "billing", "Customer",
    "View invoice & payment status",
    "As a Customer/Staff, I want to view an invoice's line items and payment status, so that "
    "there's transparency on what's owed and what's been paid.",
    ["Customers SHALL only see invoices tied to their own bookings (ownership check).",
     "The view SHALL show itemized base/late/damage charges plus current payment status.",
     "This view reuses the invoice data model from US-068 — no separate summarized/duplicated record."],
    "Low", 2, 5, "HoangTK")

add("E6", "billing", "Admin",
    "Usage & device-utilization report",
    "As Admin/Staff, I want a report on rentals and device utilization, so that fleet sizing "
    "and pricing decisions have data behind them.",
    ["The report SHALL show rental counts and per-device utilization % over a selectable date range.",
     "The report SHALL be derived from existing rental/device data — no separate manually maintained reporting table.",
     "The report SHALL be exportable (CSV) for the SRS/documentation deliverable."],
    "Low", 3, 5, "TanNB")

add("E6", "billing", "Admin",
    "Incident / response-performance report",
    "As Admin, I want a report summarizing incident counts, MTTA, and MTTR over time, so that "
    "response-team performance is visible to management (this doubles as input to US-087's "
    "evaluation report).",
    ["The report SHALL compute MTTA/MTTR from the incident audit trail (US-064) directly, matching the calculation used in US-087.",
     "The report SHALL be filterable by date range and by trip/Guide.",
     "The report SHALL be exportable (CSV)."],
    "Low", 3, 5, "TanNB")

add("E6", "billing", "Admin",
    "System health & audit-log report view",
    "As Admin, I want a view of system health (gateway connectivity summary, audit-log volume), "
    "so that operational health is visible without querying the database directly.",
    ["The view SHALL summarize gateway health (US-048) across all active gateways, not just one.",
     "The view SHALL show audit-log record counts (auth, device, incident) over a selectable date range.",
     "This view is Admin-only (RBAC-gated, not visible to Staff)."],
    "Low", 2, 5, "LongNN")

add("E6", "billing", "Staff",
    "Billing dashboard widget",
    "As Staff/Admin, I want a summary widget of revenue and outstanding payments, so that "
    "billing status is visible at a glance from the main dashboard.",
    ["The widget SHALL show total revenue and total outstanding (Pending) payments for a selectable period.",
     "The widget SHALL reuse the invoice/payment data model (US-068/069) — no separate cached summary table that can drift out of sync.",
     "Clicking the widget SHALL deep-link to the filtered invoice list."],
    "Low", 2, 5, "HoangTK")

# --- E7 DevOps / CI-CD -------------------------------------------------------
add("E7", "devops", "System",
    "Dockerfiles + docker-compose for all services",
    "As a developer, I want Dockerfiles for backend/gateway/frontend plus a docker-compose "
    "stack (Postgres, Mosquitto), so that the whole platform runs with one command on any "
    "machine, satisfying the Deployability NFR.",
    ["Each of backend/gateway/frontend SHALL have a working multi-stage Dockerfile.",
     "docker-compose.yml (already present) SHALL be extended to include Postgres and a Mosquitto MQTT broker service.",
     "`docker compose up` SHALL bring up a working stack against a clean checkout with no manual steps beyond copying .env.example."],
    "Medium", 5, 1, "Khoa", secondary="LongLP", reviewer="Khoa")

add("E7", "devops", "System",
    "GitHub Actions CI: lint + typecheck + test + build",
    "As the team, we want CI to run lint/typecheck/test/build on every PR across all 3 "
    "packages, so that broken code can't merge to develop/main.",
    ["CI SHALL run for backend, gateway, and frontend as separate jobs so a failure in one doesn't hide the others' results.",
     "The backend job SHALL run `prisma generate` before lint/build, since the Prisma client must exist for typecheck to pass.",
     "A red CI run SHALL block merge per branch protection (07-github-workflow-git-conventions.md)."],
    "High", 3, 4, "Khoa", reviewer="Khoa", status="Backlog")

add("E7", "devops", "System",
    "Backend health-check endpoint",
    "As Ops, I want a `/health` endpoint, so that uptime monitoring and the deployment guide "
    "have something concrete to point at.",
    ["The endpoint SHALL report basic liveness (process up) without requiring auth.",
     "The endpoint SHALL optionally report DB connectivity (Prisma $queryRaw ping) as a secondary field.",
     "The endpoint SHALL use the standard response envelope like every other endpoint (no special-cased shape)."],
    "Low", 2, 4, "LongLP")

add("E7", "devops", "System",
    "GitHub Actions CD: build & push images on merge",
    "As Ops, I want images built and pushed on merge to main, so that a deployable artifact "
    "always exists for the current main branch state.",
    ["The workflow SHALL build and tag images for backend/gateway/frontend on push to main.",
     "The workflow SHALL only run after the CI job (US-076) passes — no pushing an unverified image.",
     "Image tags SHALL include the short commit SHA for traceability back to source."],
    "Low", 3, 7, "TanNB", secondary="Khoa", reviewer="Khoa")

add("E7", "devops", "System",
    "Environment configuration matrix",
    "As a developer, I want .env.example fully covering every variable each package actually "
    "reads, so that onboarding doesn't involve guessing missing config.",
    ["Every env var referenced in backend/gateway/frontend source SHALL have a corresponding entry in .env.example with a comment.",
     "No secret/credential value SHALL be committed — only placeholder values.",
     "The README's setup section SHALL reference this file rather than duplicating the variable list inline."],
    "Low", 2, 7, "TanNB")

add("E7", "devops", "System",
    "Deployment guide (clean-environment validated)",
    "As the team, we want a deployment guide validated on a genuinely clean environment, so "
    "that Review 2/3 and the graders can stand the system up without tribal knowledge.",
    ["The guide SHALL be followed literally on a fresh clone/VM by someone other than its author before being marked done.",
     "The guide SHALL cover both docker-compose (US-075) and a manual npm-based path.",
     "Any step that fails during validation SHALL be fixed in the guide, not worked around verbally."],
    "Medium", 3, 7, "Khoa", reviewer="Khoa")

add("E7", "devops", "System",
    "Seed/demo data script",
    "As the team, we want a seed script producing a runnable demonstration environment "
    "(sample devices, trips, one triggered incident), so that Review/Defense demos don't start "
    "from an empty database.",
    ["The script SHALL populate a representative set of devices across all 7 lifecycle states.",
     "The script SHALL create at least one demo trip with an assigned Guide and one resolved Incident, so the full pipeline is visible immediately.",
     "The script SHALL be idempotent — re-running it SHALL NOT duplicate seed data."],
    "Low", 3, 7, "LongLP")

# --- E8 Research & Experimental Evaluation -----------------------------------
add("E8", "docs", "System",
    "Design RQ1/RQ2 connectivity-loss experiment protocol",
    "As the team, we want the RQ1/RQ2 experiment protocol documented (connectivity-loss "
    "matrix, trial counts, measured variables) before running it, so that results are "
    "reproducible and defensible at Review 3/Defense 1.",
    ["The protocol SHALL specify the connectivity-loss matrix exactly as registered: 0s/30s/2min/5min/10min/30min, 2 reconnection patterns, ≥20 trials/condition.",
     "The protocol SHALL specify delivery rate, data-loss rate, duplicate rate, sync latency (mean/median/P95), and priority-ordering compliance as the measured variables.",
     "The protocol SHALL be reviewed against 03-decisions-and-risk-register.md's risk mitigations before execution begins."],
    "High", 5, 5, "Khoa", reviewer="Khoa")

add("E8", "docs", "System",
    "Design RQ3 SOS-drill experiment protocol",
    "As the team, we want the RQ3 drill protocol documented (baseline vs. TrekLink condition, "
    "randomization, observer procedure), so that MTTA/MTTR/traceability comparisons are valid, "
    "not anecdotal.",
    ["The protocol SHALL define the uncoordinated baseline exactly as registered (verbal/text acknowledgment, independent observer, hardware stopwatch, 0% traceability by definition).",
     "The protocol SHALL specify ≥3 rotating participants, 15-20 drills per condition, randomized order, participants unaware of exact trigger time.",
     "The protocol SHALL specify network-latency variation (LAN and 4G hotspot) as a controlled variable."],
    "High", 5, 5, "Khoa", reviewer="Khoa")

add("E8", "docs", "System",
    "Execute RQ1/RQ2 physical Gateway experiments",
    "As the team, we want to execute the RQ1/RQ2 protocol against 3-5 physical TrekLink "
    "devices and collect the metrics, so that the register's delivery-rate/latency/priority "
    "NFRs have empirical evidence, not an assumption.",
    ["Physical devices SHALL be used for all mesh-to-gateway measurements; MQTT simulation may only supplement Gateway-to-Cloud load, never substitute for LoRa RF reliability claims.",
     "Results SHALL be logged per-trial (not just aggregated) so P95 latency and per-condition breakdowns can be recomputed.",
     "Raw results SHALL feed directly into US-087's evaluation report, not be re-summarized from memory afterward."],
    "High", 13, 6, "LongLP", secondary="Khoa", reviewer="Khoa")

add("E8", "docs", "System",
    "Execute RQ3 randomized SOS drills",
    "As the team, we want to execute the RQ3 drill protocol (baseline + TrekLink condition) "
    "and collect MTTA/MTTR/traceability/completion-rate data, so that the SOS-to-Incident "
    "pipeline's improvement over the status quo is measured, not assumed.",
    ["Drills SHALL run per the protocol from US-084 with an independent observer and randomized trigger timing.",
     "Both baseline and TrekLink-condition results SHALL be recorded with the same metrics for a like-for-like comparison.",
     "A reduction in MTTA SHALL NOT be assumed in advance — outcomes are reported as measured, per the register's own stated caution."],
    "High", 13, 6, "TanNB", secondary="Khoa", reviewer="Khoa")

add("E8", "docs", "System",
    "End-to-end integration test suite",
    "As the team, we want an integration suite covering idempotency (10x replay), concurrency "
    "(20x simultaneous), RBAC validation, and audit-log completeness, so that the NFRs graded "
    "at Review 3 are continuously verified, not manually re-checked before the defense.",
    ["The suite SHALL include the 10x-duplicate-eventId test (reuses US-052) and a 20-simultaneous-submission concurrency test with 0 duplicates asserted.",
     "The suite SHALL validate RBAC denial paths for at least one action per role boundary (Admin-only, Staff-only, Guide-ownership, Customer-ownership).",
     "The suite SHALL assert audit-log completeness: every FSM transition in a test run has a corresponding audit row."],
    "High", 8, 7, "Khoa", reviewer="Khoa")

add("E8", "docs", "System",
    "Compile evaluation report",
    "As the team, we want RQ1/RQ2/RQ3 results compiled into the evaluation report, so that "
    "Review 3 and Defense 1 have a single, complete, sourced document rather than scattered "
    "raw data.",
    ["The report SHALL present RQ1/RQ2 results (delivery/loss/duplicate rate, latency, priority compliance) against the register's NFR targets.",
     "The report SHALL present RQ3 results (MTTA/MTTR/traceability/completion rate) comparing baseline vs. TrekLink condition.",
     "The report SHALL be cross-referenced from 00-project-context/02-roadmap-and-milestones.md's Review 3 checklist as a completed deliverable."],
    "Medium", 5, 7, "Khoa", reviewer="Khoa")

print(f"Loaded {len(EPICS)} epics, {len(STORIES)} stories.")
print(f"Total story points: {sum(s['points'] for s in STORIES)}")

# ---------------------------------------------------------------------------
# 4. Derived data (epic rollups + per-person workload)
# ---------------------------------------------------------------------------
from collections import Counter, defaultdict

for e in EPICS:
    e_stories = [s for s in STORIES if s["epic"] == e["id"]]
    e["story_count"] = len(e_stories)
    e["points_total"] = sum(s["points"] for s in e_stories)
    cnt = Counter(s["assignee"] for s in e_stories)
    e["primary_owner"] = cnt.most_common(1)[0][0] if cnt else "—"
    sec_cnt = Counter(s["secondary"] for s in e_stories if s["secondary"])
    e["secondary_owner"] = sec_cnt.most_common(1)[0][0] if sec_cnt else "—"
    rev_cnt = Counter(s["reviewer"] for s in e_stories)
    e["reviewer_owner"] = rev_cnt.most_common(1)[0][0] if rev_cnt else "Khoa"

TOTAL_POINTS = sum(s["points"] for s in STORIES)

WORKLOAD = {
    k: {"primary_stories": 0, "primary_points": 0, "secondary_stories": 0,
        "secondary_points": 0, "modules": set()}
    for k in TEAM
}
for s in STORIES:
    a = s["assignee"]
    WORKLOAD[a]["primary_stories"] += 1
    WORKLOAD[a]["primary_points"] += s["points"]
    WORKLOAD[a]["modules"].add(s["module"])
    if s["secondary"]:
        WORKLOAD[s["secondary"]]["secondary_stories"] += 1
        WORKLOAD[s["secondary"]]["secondary_points"] += s["points"]

STATUS_OPTIONS = ["Backlog", "Ready", "In Progress", "In Review", "Done"]
PRIORITY_OPTIONS = ["High", "Medium", "Low"]
POINT_OPTIONS = ["1", "2", "3", "5", "8", "13"]
ISSUE_TYPE_OPTIONS = ["Epic", "Story"]
EPIC_MODULE_OPTIONS = [f'{e["id"]} - {e["name"]}' for e in EPICS]

# ---------------------------------------------------------------------------
# 5. Markdown generation
# ---------------------------------------------------------------------------
def render_epics_md():
    lines = []
    lines.append("# 01 — Epics")
    lines.append("")
    lines.append(
        "> Generated from `build_backlog.py` (kept alongside this file for regeneration) — "
        "the same data drives `02-user-stories.md` and `User_Story_Agile_TrekLink.xlsx`, so "
        "all three stay consistent. Epic taxonomy: the 7 epics locked in "
        "`02-templates/05-user-story-template.md`, plus **E8 (Research & Experimental "
        "Evaluation)**, added this session to home RQ1-RQ3/TP6 work that didn't fit the "
        "original 7."
    )
    lines.append("")
    lines.append(f"**Backlog totals**: {len(EPICS)} epics · {len(STORIES)} stories · {TOTAL_POINTS} story points.")
    lines.append("")
    lines.append("| Epic | Name | Module(s) | Stories | Points | Sprint range | Primary owner | Reviewer |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for e in EPICS:
        mods = ", ".join(f"`module:{m}`" for m in e["modules"])
        lines.append(
            f"| {e['id']} | {e['name']} | {mods} | {e['story_count']} | {e['points_total']} | "
            f"{e['sprint_range']} | {TEAM[e['primary_owner']]['full_name']} | "
            f"{TEAM[e['reviewer_owner']]['full_name']} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    for e in EPICS:
        lines.append(f"## {e['id']} — {e['name']}")
        lines.append("")
        lines.append(e["desc"])
        lines.append("")
        lines.append(f"- **Module label(s)**: {', '.join(f'`module:{m}`' for m in e['modules'])}")
        lines.append(f"- **Primary Prisma tables/entities**: {e['tables']}")
        lines.append(f"- **Sprint range**: {e['sprint_range']}")
        lines.append(f"- **Stories**: {e['story_count']} · **Points**: {e['points_total']}")
        lines.append(
            f"- **Primary owner**: {TEAM[e['primary_owner']]['full_name']} ({e['primary_owner']}) · "
            f"**Secondary**: {TEAM[e['secondary_owner']]['full_name'] if e['secondary_owner'] != '—' else '—'} · "
            f"**Reviewer/Architect**: {TEAM[e['reviewer_owner']]['full_name']} ({e['reviewer_owner']})"
        )
        lines.append("")
        e_stories = sorted([s for s in STORIES if s["epic"] == e["id"]], key=lambda s: s["points"])
        lines.append("| Story | Summary | Points | Sprint | Status |")
        lines.append("|---|---|---|---|---|")
        for s in e_stories:
            lines.append(f"| [{s['id']}](./02-user-stories.md#{s['id'].lower()}) | {s['summary']} | {s['points']} | Sprint {s['sprint']} | {s['status']} |")
        lines.append("")
    return "\n".join(lines) + "\n"


def render_stories_md():
    lines = []
    lines.append("# 02 — User Stories")
    lines.append("")
    lines.append(
        "> Generated from `build_backlog.py`. Story granularity is intentionally fine "
        "(one story per discrete actor-action) — coarser epics were assessed as creating "
        "development ambiguity and risking incomplete business-rule coverage. Each story's "
        "acceptance criteria are written EARS-style per "
        "`02-templates/01-requirements-template.md`; expand into the full "
        "`specs/{module}/requirements.md` EARS format only once that story's sprint actually "
        "starts (spec-before-code — see `01-conventions/02-spec-driven-development-workflow.md`)."
    )
    lines.append("")
    for e in EPICS:
        lines.append(f"## {e['id']} — {e['name']}")
        lines.append("")
        e_stories = sorted([s for s in STORIES if s["epic"] == e["id"]], key=lambda s: s["points"])
        for s in e_stories:
            lines.append(f"### {s['id']} — {s['summary']}")
            lines.append("")
            sec = f", Secondary: {TEAM[s['secondary']]['full_name']}" if s["secondary"] else ""
            lines.append(
                f"`module:{s['module']}` · Actor: **{s['actor']}** · Priority: **{s['priority']}** · "
                f"Points: **{s['points']}** · Sprint **{s['sprint']}** · Status: **{s['status']}**"
            )
            lines.append("")
            lines.append(
                f"**Owner**: {TEAM[s['assignee']]['full_name']} ({s['assignee']}){sec} · "
                f"**Reviewer**: {TEAM[s['reviewer']]['full_name']} ({s['reviewer']})"
            )
            lines.append("")
            lines.append(f"**User Story**: {s['story']}")
            lines.append("")
            lines.append("**Acceptance Criteria**:")
            for i, ac in enumerate(s["ac"], 1):
                lines.append(f"{i}. {ac}")
            lines.append("")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# 6. XLSX generation
# ---------------------------------------------------------------------------
HEADER_FILL = PatternFill("solid", fgColor="1F3864")
HEADER_FONT = Font(name="Arial", size=11, bold=True, color="FFFFFF")
EPIC_FILL = PatternFill("solid", fgColor="DCE6F1")
EPIC_FONT = Font(name="Arial", size=11, bold=True)
BODY_FONT = Font(name="Arial", size=10)
WRAP = Alignment(wrap_text=True, vertical="top")
WRAP_CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def style_header_row(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = WRAP_CENTER
        cell.border = BORDER


def autosize(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def build_workbook(path):
    wb = Workbook()

    # --- README sheet ---
    ws = wb.active
    ws.title = "README"
    readme_lines = [
        ("TrekLink — User Story Backlog", True, 14),
        ("", False, 11),
        ("Generated by build_backlog.py — regenerate this file from that script rather than", False, 11),
        ("hand-editing rows, so the docs (03-backlog/) and this workbook never drift apart.", False, 11),
        ("", False, 11),
        ("Sheets:", True, 11),
        ("  Backlog — every Epic + Story. Epics are grouped as section headers (light blue,", False, 11),
        ("  bold); each epic's child stories are sorted by Story Point Estimate ascending.", False, 11),
        ("  This was a deliberate choice over a flat global point-sort: it keeps epic", False, 11),
        ("  traceability intact while still ranking work-size within the group a team would", False, 11),
        ("  actually sprint-plan from. Flag it if a flat global sort was wanted instead.", False, 11),
        ("", False, 11),
        ("  Epic Summary & Traceability — one row per epic: story/point rollups, primary", False, 11),
        ("  Prisma tables touched, and Primary Owner / Secondary / Reviewer-Architect.", False, 11),
        ("", False, 11),
        ("  Workload Summary (Rebalanced) — one row per team member: story/point totals as", False, 11),
        ("  Primary owner and as Secondary contributor, modules touched, % of the 360-point", False, 11),
        ("  backlog they primary-own, and an allocation note tying it back to their skill", False, 11),
        ("  matrix (01-project-charter.md).", False, 11),
        ("", False, 11),
        ("Legend:", True, 11),
        ("  Priority: High / Medium / Low", False, 11),
        ("  Story Points: Fibonacci 1, 2, 3, 5, 8, 13", False, 11),
        ("  Status: Backlog -> Ready -> In Progress -> In Review -> Done", False, 11),
        ("  Sprint/Milestone: pre-mapped from 00-project-context/02-roadmap-and-milestones.md's", False, 11),
        ("  TP-to-week table. Status is 'Ready' only for Sprint 1 items (this week); everything", False, 11),
        ("  else is 'Backlog' pending your team's own sprint-planning adjustment.", False, 11),
        ("", False, 11),
        ("Team skill matrix (see 01-project-charter.md for the source):", True, 11),
    ]
    for name, info in TEAM.items():
        readme_lines.append((f"  {info['full_name']} ({name}, {info['mssv']}) — {info['role']} — {info['skills']}", False, 10))
    r = 1
    for text, bold, size in readme_lines:
        cell = ws.cell(row=r, column=1, value=text)
        cell.font = Font(name="Arial", size=size, bold=bold)
        r += 1
    ws.column_dimensions["A"].width = 110
    ws.sheet_view.showGridLines = False

    # --- Backlog sheet ---
    ws = wb.create_sheet("Backlog")
    headers = [
        "Issue Type", "Epic/Module", "Summary", "Description", "Issue Id", "Parent",
        "Priority", "Story Point Estimate", "Sprint/Milestone", "Status",
        "Assignee", "Secondary", "Reviewer", "GitHub Issue #",
    ]
    ws.append(headers)
    style_header_row(ws, 1, len(headers))
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}1"

    row_idx = 2
    for e in EPICS:
        epic_module_label = f'{e["id"]} - {e["name"]}'
        ws.append([
            "Epic", epic_module_label, e["name"],
            f'{e["desc"]}\n\nPrimary tables/entities: {e["tables"]}',
            e["id"], "", "", e["points_total"], e["sprint_range"], "",
            TEAM[e["primary_owner"]]["full_name"],
            TEAM[e["secondary_owner"]]["full_name"] if e["secondary_owner"] != "—" else "—",
            TEAM[e["reviewer_owner"]]["full_name"], "",
        ])
        for c in range(1, len(headers) + 1):
            cell = ws.cell(row=row_idx, column=c)
            cell.fill = EPIC_FILL
            cell.font = EPIC_FONT
            cell.alignment = WRAP
            cell.border = BORDER
        row_idx += 1

        e_stories = sorted([s for s in STORIES if s["epic"] == e["id"]], key=lambda s: s["points"])
        for s in e_stories:
            desc = s["story"] + "\n" + "\n".join(f"AC{i}: {ac}" for i, ac in enumerate(s["ac"], 1))
            ws.append([
                "Story", epic_module_label, s["summary"], desc, s["id"], e["id"],
                s["priority"], s["points"], f'Sprint {s["sprint"]}', s["status"],
                TEAM[s["assignee"]]["full_name"],
                TEAM[s["secondary"]]["full_name"] if s["secondary"] else "",
                TEAM[s["reviewer"]]["full_name"], "",
            ])
            for c in range(1, len(headers) + 1):
                cell = ws.cell(row=row_idx, column=c)
                cell.font = BODY_FONT
                cell.alignment = WRAP
                cell.border = BORDER
            row_idx += 1

    last_row = row_idx - 1
    autosize(ws, [10, 24, 30, 55, 9, 8, 9, 10, 14, 12, 16, 16, 16, 12])
    for r in range(2, last_row + 1):
        ws.row_dimensions[r].height = 60

    # Dropdown data validations
    def add_dv(formula, col_letter, allow_blank=True):
        dv = DataValidation(type="list", formula1=formula, allow_blank=allow_blank, showDropDown=False)
        ws.add_data_validation(dv)
        dv.add(f"{col_letter}2:{col_letter}{last_row}")
        return dv

    add_dv('"' + ",".join(ISSUE_TYPE_OPTIONS) + '"', "A")
    add_dv('"' + ",".join(EPIC_MODULE_OPTIONS) + '"', "B")
    add_dv('"' + ",".join(PRIORITY_OPTIONS) + '"', "G")
    add_dv('"' + ",".join(POINT_OPTIONS) + '"', "H")
    add_dv('"' + ",".join(STATUS_OPTIONS) + '"', "J")

    # --- Epic Summary & Traceability sheet ---
    ws2 = wb.create_sheet("Epic Summary & Traceability")
    headers2 = [
        "Epic", "Epic Name", "Module(s)", "Stories", "Total Story Points",
        "Primary Tables/Entities", "Primary Owner", "Secondary/Contributor",
        "Reviewer/Architect", "Allocation Notes",
    ]
    ws2.append(headers2)
    style_header_row(ws2, 1, len(headers2))
    ws2.freeze_panes = "A2"
    for e in EPICS:
        note = (
            f"Sprint range {e['sprint_range']}. "
            f"Owner chosen from the skill matrix in 01-project-charter.md."
        )
        ws2.append([
            e["id"], e["name"], ", ".join(e["modules"]), e["story_count"], e["points_total"],
            e["tables"], TEAM[e["primary_owner"]]["full_name"],
            TEAM[e["secondary_owner"]]["full_name"] if e["secondary_owner"] != "—" else "—",
            TEAM[e["reviewer_owner"]]["full_name"], note,
        ])
    total_row = len(EPICS) + 2
    ws2.append(["", "TOTAL", "", len(STORIES), TOTAL_POINTS, "", "", "", "", ""])
    for c in range(1, len(headers2) + 1):
        ws2.cell(row=total_row, column=c).font = Font(bold=True)
    for r in range(2, total_row + 1):
        for c in range(1, len(headers2) + 1):
            cell = ws2.cell(row=r, column=c)
            cell.alignment = WRAP
            cell.border = BORDER
            if not cell.font or not cell.font.bold:
                cell.font = BODY_FONT
        ws2.row_dimensions[r].height = 45
    autosize(ws2, [8, 26, 18, 9, 12, 34, 18, 18, 18, 40])

    # --- Workload Summary (Rebalanced) sheet ---
    ws3 = wb.create_sheet("Workload Summary (Rebalanced)")
    headers3 = [
        "Member", "Code", "Modules Touched (Primary)", "# Stories (Primary)",
        "Story Points (Primary)", "# Stories (Secondary)", "Story Points (Secondary)",
        "% of Backlog (Primary Points)", "Skill-Based Allocation Note",
    ]
    ws3.append(headers3)
    style_header_row(ws3, 1, len(headers3))
    ws3.freeze_panes = "A2"
    for name, info in TEAM.items():
        w = WORKLOAD[name]
        pct = round(100 * w["primary_points"] / TOTAL_POINTS, 1) if TOTAL_POINTS else 0
        note = f"Skills: {info['skills']}"
        ws3.append([
            info["full_name"], name, ", ".join(sorted(w["modules"])) or "—",
            w["primary_stories"], w["primary_points"], w["secondary_stories"],
            w["secondary_points"], f"{pct}%", note,
        ])
    total_row3 = len(TEAM) + 2
    ws3.append([
        "TOTAL", "", "", sum(w["primary_stories"] for w in WORKLOAD.values()),
        sum(w["primary_points"] for w in WORKLOAD.values()),
        sum(w["secondary_stories"] for w in WORKLOAD.values()),
        sum(w["secondary_points"] for w in WORKLOAD.values()), "100%", "",
    ])
    for c in range(1, len(headers3) + 1):
        ws3.cell(row=total_row3, column=c).font = Font(bold=True)
    for r in range(2, total_row3 + 1):
        for c in range(1, len(headers3) + 1):
            cell = ws3.cell(row=r, column=c)
            cell.alignment = WRAP
            cell.border = BORDER
            if not cell.font or not cell.font.bold:
                cell.font = BODY_FONT
        ws3.row_dimensions[r].height = 32
    autosize(ws3, [22, 10, 26, 12, 12, 12, 12, 14, 40])

    wb.save(path)
    print(f"Workbook written to {path}")


if __name__ == "__main__":
    import sys
    docs_dir = "/home/claude/treklink_work/treklink-docs/_docs/03-backlog"
    import os
    os.makedirs(docs_dir, exist_ok=True)
    with open(f"{docs_dir}/01-epics.md", "w", encoding="utf-8") as f:
        f.write(render_epics_md())
    with open(f"{docs_dir}/02-user-stories.md", "w", encoding="utf-8") as f:
        f.write(render_stories_md())
    print("Markdown written.")

    xlsx_out = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/treklink_work/User_Story_Agile_TrekLink.xlsx"
    build_workbook(xlsx_out)

