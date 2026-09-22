# 02: User Stories

> Generated from `build_backlog.py`. Story granularity is intentionally fine (one story per discrete actor-action), coarser epics were assessed as creating development ambiguity and risking incomplete business-rule coverage. Each story's acceptance criteria are written EARS-style per `02-templates/01-requirements-template.md`; expand into the full `specs/{module}/requirements.md` EARS format only once that story's sprint actually starts (spec-before-code, see `01-conventions/02-spec-driven-development-workflow.md`).

## E1 (`TK-1`): Identity & RBAC

### US-006 (`TK-14`): Logout / token revocation

`module:auth` · **MF-01** · Actor: **System** · Priority: **Medium** · Points: **2** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-14` · **Branch**: `feat/TK-14-<short-desc>`

**Owner**: Lâm Phi Long (LongLP) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a logged-in user, I want to log out and have my refresh token revoked, so that a stolen token can't be used to renew my session afterward.

**Acceptance Criteria**:
1. WHEN a logout request is received, the system SHALL revoke the presented refresh token immediately.
2. The system SHALL clear any server-side session state associated with that token.
3. A revoked refresh token SHALL return 401 on any subsequent renewal attempt.

### US-002 (`TK-10`): Account registration

`module:auth` · **MF-01** · Actor: **Customer** · Priority: **High** · Points: **3** · Sprint **2** · Status: **Backlog**

**Jira**: `TK-10` · **Branch**: `feat/TK-10-<short-desc>`

**Owner**: Lâm Phi Long (LongLP), Secondary: Trần Khải Hoàng · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a Customer (or Staff/Guide provisioned by Admin), I want to register an account with email + password, so that I can access my role's features.

**Acceptance Criteria**:
1. WHEN a registration request has a unique email and a password meeting policy, the system SHALL create the account and hash the password with bcrypt.
2. IF the email is already registered, THEN the system SHALL reject with 409 Conflict and a field-scoped message.
3. The system SHALL assign the Customer role by default; Admin/Staff/Guide accounts are provisioned by an Admin (see US-008).

### US-003 (`TK-11`): Login issues JWT access + refresh token

`module:auth` · **MF-01** · Actor: **Customer** · Priority: **High** · Points: **3** · Sprint **2** · Status: **Backlog**

**Jira**: `TK-11` · **Branch**: `feat/TK-11-<short-desc>`

**Owner**: Lâm Phi Long (LongLP), Secondary: Trần Khải Hoàng · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As any registered user, I want to log in and receive an access token and a refresh token, so that I can call protected endpoints without re-entering credentials each request.

**Acceptance Criteria**:
1. WHEN credentials are valid, the system SHALL return a short-lived JWT access token and a longer-lived refresh token.
2. IF credentials are invalid, THEN the system SHALL return 401 Unauthorized without revealing whether the email or password was wrong.
3. The response envelope SHALL match API_Design_Template.md exactly (result/isSuccess/statusCode/message).

### US-004 (`TK-12`): Auth audit log (login/logout/failed attempts)

`module:auth` · **MF-01** · Actor: **System** · Priority: **Medium** · Points: **3** · Sprint **2** · Status: **Backlog**

**Jira**: `TK-12` · **Branch**: `feat/TK-12-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As an Admin, I want login, logout, and failed-attempt events logged, so that I can investigate suspicious access per the register's Security NFR.

**Acceptance Criteria**:
1. The system SHALL record actor (user ID or attempted email), event type, IP, and UTC timestamp for every auth event.
2. Failed-login records SHALL NOT store the attempted password in any form.
3. Records SHALL be append-only (no update/delete endpoint exposed).

### US-007 (`TK-15`): Password reset / recovery

`module:auth` · **MF-01** · Actor: **Customer** · Priority: **Medium** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-15` · **Branch**: `feat/TK-15-<short-desc>`

**Owner**: Trần Khải Hoàng (HoangTK) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a user who forgot their password, I want to request a reset link/code and set a new password, so that I regain access without contacting an Admin.

**Acceptance Criteria**:
1. WHEN a reset is requested for a known email, the system SHALL issue a single-use, time-limited reset token and SHALL NOT reveal whether the email exists.
2. WHEN a valid reset token and a policy-compliant new password are submitted, the system SHALL update the password hash and invalidate the token.
3. IF the reset token is expired or already used, THEN the system SHALL reject with a clear error and no partial state change.

### US-010 (`TK-18`): Guide profile management

`module:auth` · **MF-01** · Actor: **Guide** · Priority: **Low** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-18` · **Branch**: `feat/TK-18-<short-desc>`

**Owner**: Trần Khải Hoàng (HoangTK) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a Guide, I want to see my profile with assigned trips and device-handling history, so that I have a single view of my responsibilities.

**Acceptance Criteria**:
1. The system SHALL show the Guide's currently assigned trips and their status.
2. The system SHALL show a chronological device-handling history (check-out/check-in events) for that Guide.
3. A Guide SHALL only be able to view their own profile, not another Guide's (ownership check).

### US-001 (`TK-9`): Data-driven Role & Permission (RBAC) schema

`module:auth` · **MF-01** · Actor: **Admin** · Priority: **High** · Points: **5** · Sprint **1** · Status: **Ready**

**Jira**: `TK-9` · **Branch**: `feat/TK-9-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As an Admin, I want roles and permissions stored as data (not hardcoded), so that access control can evolve without a code deploy.

**Acceptance Criteria**:
1. The system SHALL persist roles, permissions, and role-permission mappings as queryable entities.
2. WHEN a permission is added to a role, the system SHALL apply it on the next request without a redeploy.
3. The default seed SHALL include Admin/Staff/Guide/Customer roles matching the charter's actor table.

### US-005 (`TK-13`): Refresh-token rotation & silent session renewal

`module:auth` · **MF-01** · Actor: **System** · Priority: **High** · Points: **5** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-13` · **Branch**: `feat/TK-13-<short-desc>`

**Owner**: Lâm Phi Long (LongLP), Secondary: Đỗ Đăng Khoa · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a logged-in user, I want my session to silently renew via the refresh token, so that I'm not forced to log in again every few minutes.

**Acceptance Criteria**:
1. WHEN a valid, unexpired refresh token is presented, the system SHALL issue a new access token and rotate the refresh token.
2. IF a refresh token is reused after rotation (replay), THEN the system SHALL revoke the whole token family and force re-login.
3. The frontend apiClient SHALL implement a silent-refresh interceptor per 06-frontend-conventions.md §6.1.

### US-008 (`TK-16`): CASL PoliciesGuard enforcement

`module:auth` · **MF-01** · Actor: **System** · Priority: **High** · Points: **5** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-16` · **Branch**: `feat/TK-16-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a developer, I want a reusable PoliciesGuard + @CheckPolicies decorator wired globally, so that every mutating endpoint across all modules enforces RBAC consistently.

**Acceptance Criteria**:
1. The system SHALL expose a PoliciesGuard usable via @UseGuards(JwtAuthGuard, PoliciesGuard) on any controller.
2. IF a valid JWT holds insufficient role/CASL permission for the action, THEN the system SHALL return 403 Forbidden via the GlobalExceptionFilter envelope.
3. The guard SHALL be unit-tested against at least one allow and one deny case per role.

### US-009 (`TK-17`): Admin: manage user accounts

`module:auth` · **MF-01** · Actor: **Admin** · Priority: **Medium** · Points: **5** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-17` · **Branch**: `feat/TK-17-<short-desc>`

**Owner**: Nguyễn Ngọc Long (LongNN), Secondary: Trần Khải Hoàng · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As an Admin, I want to list, create, deactivate, and role-assign user accounts, so that I can provision Staff/Guide accounts and manage access.

**Acceptance Criteria**:
1. The system SHALL provide a paginated list of accounts filterable by role and active status.
2. WHEN an Admin deactivates an account, the system SHALL immediately reject that account's existing refresh tokens.
3. Only Admin-role callers SHALL be authorized to create Staff/Guide accounts or change a user's role.

## E2 (`TK-2`): Device Fleet & Maintenance

### US-016 (`TK-24`): Device detail view

`module:devices` · **MF-01** · Actor: **Staff** · Priority: **Low** · Points: **2** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-24` · **Branch**: `feat/TK-24-<short-desc>`

**Owner**: Trần Khải Hoàng (HoangTK) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff/Admin, I want a single device's detail page (current assignment, telemetry, history), so that I can inspect one unit without cross-referencing multiple screens.

**Acceptance Criteria**:
1. The system SHALL return the device's current rental/trip assignment (if any) alongside its own fields.
2. The detail view SHALL show the most recent 20 telemetry readings.
3. The frontend SHALL link to this view from the fleet list row's Actions menu.

### US-020 (`TK-28`): Retire a device

`module:devices` · **MF-01** · Actor: **Admin** · Priority: **Low** · Points: **2** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-28` · **Branch**: `feat/TK-28-<short-desc>`

**Owner**: Nguyễn Ngọc Long (LongNN) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As an Admin, I want to retire a device permanently, so that end-of-life units stop appearing as allocatable without deleting their historical records.

**Acceptance Criteria**:
1. WHEN a device is retired, the system SHALL set status=Retired, a terminal state with no further outgoing transitions per the FSM.
2. Retiring SHALL NOT delete the device row or its history, this is a status transition, not a DELETE (per the no-hard-deletes convention).
3. IF the device has an active rental/trip assignment, THEN retirement SHALL be rejected until that assignment ends.

### US-021 (`TK-29`): Device fleet dashboard widget

`module:devices` · **MF-01** · Actor: **Staff** · Priority: **Low** · Points: **2** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-29` · **Branch**: `feat/TK-29-<short-desc>`

**Owner**: Trần Khải Hoàng (HoangTK) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff/Admin, I want a summary widget of device counts by status, so that I can see fleet health at a glance without opening the full list.

**Acceptance Criteria**:
1. The widget SHALL show a count per status (Available/Reserved/Rented/In-Field/Returned/Maintenance/Retired).
2. Counts SHALL update on dashboard load via the standard TanStack Query cache (no separate polling mechanism).
3. Clicking a status count SHALL deep-link to the filtered fleet list (US-014).

### US-011 (`TK-19`): Manage device type / hardware variant catalog

`module:devices` · **MF-01** · Actor: **Admin** · Priority: **Medium** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-19` · **Branch**: `feat/TK-19-<short-desc>`

**Owner**: Nguyễn Ngọc Long (LongNN) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As an Admin, I want to manage the catalog of device types, hardware variants (v1-v4), and firmware versions, so that new physical units can be registered against a known type.

**Acceptance Criteria**:
1. The system SHALL allow Admin to create/edit a device type with hardware variant and firmware version fields.
2. The device registration endpoint (US-012) SHALL only accept a hardwareVariant that exists in this catalog.
3. The system SHALL NOT allow deleting a device type that has registered devices (referential integrity).

### US-012 (`TK-20`): Register a physical TrekLink device

`module:devices` · **MF-01** · Actor: **Admin** · Priority: **High** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-20` · **Branch**: `feat/TK-20-<short-desc>`

**Owner**: Lâm Phi Long (LongLP) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As an Admin, I want to register a new physical device (device ID, hardware variant, firmware version), so that it enters the fleet as Available.

**Acceptance Criteria**:
1. WHEN a valid, unique device ID is submitted, the system SHALL create the device with status=Available.
2. IF the device ID already exists, THEN the system SHALL reject with 409 Conflict.
3. The created device SHALL default battery/telemetry fields to null until the first telemetry event arrives (US-016).

### US-015 (`TK-23`): Device fleet list with filters

`module:devices` · **MF-01** · Actor: **Staff** · Priority: **Medium** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-23` · **Branch**: `feat/TK-23-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB), Secondary: Trần Khải Hoàng · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff/Admin, I want to see the device list filterable by status, hardware variant, and battery level, so that I can find an available device quickly during allocation.

**Acceptance Criteria**:
1. The system SHALL support filtering by status and hardwareVariant, and sorting by lastSeenAt/batteryPct.
2. The response SHALL use the standard PagedResultDto shape (05-backend-conventions.md §3.2).
3. The frontend list screen SHALL follow Pattern A (List & Search) from 06-frontend-conventions.md §4.

### US-018 (`TK-26`): Schedule device maintenance

`module:devices` · **MF-01** · Actor: **Staff** · Priority: **Medium** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-26` · **Branch**: `feat/TK-26-<short-desc>`

**Owner**: Nguyễn Ngọc Long (LongNN) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff, I want to move a device into Maintenance and schedule when it should return to service, so that damaged/due-for-service units aren't rented out.

**Acceptance Criteria**:
1. WHEN Staff transitions a device to Maintenance, the system SHALL require a reason and SHALL accept an optional scheduled-return date.
2. The transition SHALL go through the FSM guard (US-013), only Available/Returned devices can enter Maintenance.
3. The device SHALL remain excluded from allocation until explicitly transitioned back to Available.

### US-019 (`TK-27`): Log device damage on return inspection

`module:devices` · **MF-01** · Actor: **Staff** · Priority: **Medium** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-27` · **Branch**: `feat/TK-27-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff, I want to log a damage/incident report against a device during return inspection, so that repeated damage and fee calculation (US-036) have a record to reference.

**Acceptance Criteria**:
1. The system SHALL let Staff attach a damage report (description, severity, optional photo reference) to a Returned device.
2. A logged damage report SHALL be visible on the device's history (US-022) permanently (no hard delete).
3. Logging a damage report SHALL NOT itself change device status, Staff separately decides Maintenance vs. re-Available.

### US-022 (`TK-30`): Device assignment/rental/incident history view

`module:devices` · **MF-01** · Actor: **Staff** · Priority: **Low** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-30` · **Branch**: `feat/TK-30-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff/Admin, I want a chronological history per device (assignments, rentals, incidents, maintenance), so that I can audit a unit's full lifecycle for a review or a customer dispute.

**Acceptance Criteria**:
1. The system SHALL aggregate rental, incident, and maintenance records for one device into a single chronological feed.
2. Each entry SHALL show actor, event type, and UTC timestamp, consistent with the Auditability NFR.
3. The feed SHALL be read-only (no edit/delete affordance), it's an audit view, not a working list.

### US-014 (`TK-22`): Prevent allocation of unavailable devices

`module:devices` · **MF-01** · Actor: **System** · Priority: **High** · Points: **5** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-22` · **Branch**: `feat/TK-22-<short-desc>`

**Owner**: Nguyễn Ngọc Long (LongNN) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the system, I want to refuse allocating a device that is in Maintenance, Retired, or past its scheduled maintenance date, so that Staff can't accidentally rent out an unsafe unit.

**Acceptance Criteria**:
1. WHILE a device is in Maintenance or Retired status, the system SHALL reject any allocation request referencing it (409 Conflict, DEVICE_NOT_ALLOCATABLE).
2. IF a device's scheduled maintenance date has passed without being cleared, THEN the system SHALL block allocation even if status is still Available.
3. This check SHALL run inside the same transaction as the allocation write (no check-then-write race).

### US-017 (`TK-25`): Ingest device telemetry from Gateway

`module:devices` · **MF-01** · Actor: **System** · Priority: **High** · Points: **5** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-25` · **Branch**: `feat/TK-25-<short-desc>`

**Owner**: Lâm Phi Long (LongLP), Secondary: Đỗ Đăng Khoa · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the system, I want to accept battery %, last-seen timestamp, and last GPS fix from gateway-sync events, so that the fleet view reflects real field state.

**Acceptance Criteria**:
1. WHEN a telemetry-type gateway event is ingested, the system SHALL update the device's batteryPct, lastSeenAt, and last known position.
2. The system SHALL discard telemetry with an older timestamp than the device's current lastSeenAt (out-of-order protection).
3. This handler SHALL reuse the idempotent ingestion path from E4 (US-049), not a separate endpoint.

### US-013 (`TK-21`): Device 7-state lifecycle FSM engine

`module:devices` · **MF-01** · Actor: **System** · Priority: **High** · Points: **8** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-21` · **Branch**: `feat/TK-21-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa), Secondary: Nguyễn Ngọc Long · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a developer, I want an explicit transition table for the device lifecycle (Available→Reserved→Rented→In-Field→Returned→Maintenance→Retired), so that every status change is validated and auditable, not an ad-hoc field write.

**Acceptance Criteria**:
1. The system SHALL reject any status transition not present in the allowed-transitions table (04-architecture-conventions.md §2.1) with 409 Conflict.
2. Every successful transition SHALL write an append-only audit row (actor, from-state, to-state, UTC timestamp).
3. The FSM SHALL be unit-tested for every legal transition and at least one illegal transition per state.

## E3 (`TK-3`): Trip & Rental Management

### US-024 (`TK-32`): Browse trek packages

`module:trips` · **MF-01** · Actor: **Customer** · Priority: **Medium** · Points: **2** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-32` · **Branch**: `feat/TK-32-<short-desc>`

**Owner**: Trần Khải Hoàng (HoangTK) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a Customer, I want to browse available trek packages, so that I can choose one to book.

**Acceptance Criteria**:
1. The system SHALL list only active packages to Customer-role callers.
2. The list SHALL support filtering by route/duration/price range.
3. The frontend SHALL follow Pattern A (List & Search) per 06-frontend-conventions.md.

### US-031 (`TK-39`): Record deposit

`module:rentals` · **MF-01** · Actor: **Staff** · Priority: **Medium** · Points: **2** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-39` · **Branch**: `feat/TK-39-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff, I want to record a deposit payment against a rental agreement, so that check-out (US-032) can be gated on deposit received.

**Acceptance Criteria**:
1. The system SHALL record deposit amount, method, and timestamp against the rental agreement.
2. Check-out (US-032) SHALL be blocked if the required deposit is not marked received.
3. This uses the same mock/sandbox payment status model as E6, not a separate ad-hoc field.

### US-040 (`TK-48`): Customer: view trip & rental history

`module:trips` · **MF-01** · Actor: **Customer** · Priority: **Low** · Points: **2** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-48` · **Branch**: `feat/TK-48-<short-desc>`

**Owner**: Trần Khải Hoàng (HoangTK) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a Customer, I want to see my past trips and rentals, so that I can reference or rebook a previous package.

**Acceptance Criteria**:
1. The system SHALL list the Customer's completed/past bookings in reverse-chronological order.
2. Each history entry SHALL link to that booking's rental agreement and final invoice.
3. This is a read-only view, no edit affordance on historical records.

### US-023 (`TK-31`): Manage trek packages

`module:trips` · **MF-01** · Actor: **Admin** · Priority: **Medium** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-31` · **Branch**: `feat/TK-31-<short-desc>`

**Owner**: Nguyễn Ngọc Long (LongNN), Secondary: Nguyễn Bá Tân · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As an Admin/Staff, I want to create and edit trek packages (route, duration, price, device requirements), so that Customers have something to browse and book.

**Acceptance Criteria**:
1. The system SHALL let Admin/Staff create a trek package with route name, duration, base price, and default device count.
2. An edited package SHALL NOT retroactively change already-confirmed bookings' agreed terms.
3. The package SHALL support an active/inactive flag so past packages can be hidden without deletion.

### US-027 (`TK-35`): Review and approve/reject a booking

`module:trips` · **MF-01** · Actor: **Staff** · Priority: **High** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-35` · **Branch**: `feat/TK-35-<short-desc>`

**Owner**: Nguyễn Ngọc Long (LongNN) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff, I want to review a Pending booking and approve or reject it, so that only feasible bookings proceed to device allocation.

**Acceptance Criteria**:
1. WHEN Staff approves, the system SHALL transition the booking to Confirmed and unlock device allocation (US-028).
2. WHEN Staff rejects, the system SHALL transition to Rejected with a required reason, releasing any soft reservation.
3. Only Staff/Admin-role callers SHALL be authorized to approve/reject.

### US-029 (`TK-37`): Assign a Guide to a trip

`module:trips` · **MF-01** · Actor: **Staff** · Priority: **Medium** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-37` · **Branch**: `feat/TK-37-<short-desc>`

**Owner**: Nguyễn Ngọc Long (LongNN) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff, I want to assign a Guide to a confirmed trip together with its allocated device set, so that the Guide's profile (US-009) and live monitoring (E5) know which trip/devices they own.

**Acceptance Criteria**:
1. The system SHALL only allow assigning a user with the Guide role.
2. A Guide SHALL NOT be assigned to two trips with overlapping date ranges.
3. The assignment SHALL be visible on the Guide's own profile view (US-009) immediately.

### US-033 (`TK-41`): Guide confirms device receipt/handover

`module:trips` · **MF-01** · Actor: **Guide** · Priority: **Medium** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-41` · **Branch**: `feat/TK-41-<short-desc>`

**Owner**: Trần Khải Hoàng (HoangTK) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a Guide, I want to confirm receipt of the handed-over devices at check-out, so that there's a two-party (Staff + Guide) record of what physically changed hands.

**Acceptance Criteria**:
1. The system SHALL require a Guide-side confirmation action before check-out (US-032) is considered complete.
2. IF the Guide's confirmed device list differs from Staff's allocated list, THEN the system SHALL flag a mismatch for Staff to resolve before proceeding.
3. This confirmation SHALL be timestamped and attributed to the specific Guide account.

### US-035 (`TK-43`): Calculate late-return fee

`module:rentals` · **MF-01** · Actor: **System** · Priority: **Medium** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-43` · **Branch**: `feat/TK-43-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the system, I want to calculate a late-return fee when check-in happens after the agreed return date, so that billing (E6) has an accurate invoice line item.

**Acceptance Criteria**:
1. WHEN check-in timestamp exceeds the rental agreement's agreed return date, the system SHALL calculate a fee using the pricing rule's late-fee formula (E6).
2. The calculated fee SHALL be itemized separately from the base rental charge on the resulting invoice (US-068).
3. On-time check-in SHALL produce zero late fee, not a null/undefined field.

### US-036 (`TK-44`): Calculate damage fee

`module:rentals` · **MF-01** · Actor: **System** · Priority: **Medium** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-44` · **Branch**: `feat/TK-44-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the system, I want to calculate a damage fee from the device's logged damage report (US-018), so that billing reflects repair/replacement cost.

**Acceptance Criteria**:
1. WHEN check-in inspection logs a damage report with a severity tier, the system SHALL calculate a fee from the pricing rule's damage-fee table.
2. A device with no damage report at check-in SHALL produce zero damage fee.
3. The fee calculation SHALL be traceable to the specific damage-log entry it was derived from.

### US-037 (`TK-45`): Guide: view assigned trips, group, devices

`module:trips` · **MF-01** · Actor: **Guide** · Priority: **Medium** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-45` · **Branch**: `feat/TK-45-<short-desc>`

**Owner**: Trần Khải Hoàng (HoangTK) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a Guide, I want to see my assigned trips, the customer group, and the allocated device set, so that I know what I'm responsible for before departure.

**Acceptance Criteria**:
1. The system SHALL scope this view to only trips where the caller is the assigned Guide.
2. The view SHALL show each allocated device's ID and current status.
3. The view SHALL show the customer group's roster (names, contact) for that trip.

### US-039 (`TK-47`): Customer: view booking/rental/deposit/payment info

`module:trips` · **MF-01** · Actor: **Customer** · Priority: **Low** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-47` · **Branch**: `feat/TK-47-<short-desc>`

**Owner**: Trần Khải Hoàng (HoangTK) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a Customer, I want to view my booking, rental, deposit, and payment status, so that I know where things stand without contacting Staff.

**Acceptance Criteria**:
1. The system SHALL scope this view to only bookings owned by the calling Customer.
2. The view SHALL show current booking status, deposit status, and any calculated fees once available.
3. This view SHALL reuse the billing status model from E6, not duplicate payment-state logic.

### US-025 (`TK-33`): Submit a booking request

`module:trips` · **MF-01** · Actor: **Customer** · Priority: **High** · Points: **5** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-33` · **Branch**: `feat/TK-33-<short-desc>`

**Owner**: Lâm Phi Long (LongLP), Secondary: Trần Khải Hoàng · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a Customer, I want to submit a booking request for a trek package (dates, group size), so that Staff can review and confirm it.

**Acceptance Criteria**:
1. WHEN a booking is submitted, the system SHALL create it in a Pending state awaiting Staff review.
2. The system SHALL validate group size against the package's constraints before accepting.
3. The booking form SHALL follow the 4-step/6-field UX rule (06-frontend-conventions.md §3).

### US-026 (`TK-34`): Reserve devices during booking

`module:rentals` · **MF-01** · Actor: **Customer** · Priority: **Medium** · Points: **5** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-34` · **Branch**: `feat/TK-34-<short-desc>`

**Owner**: Lâm Phi Long (LongLP) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a Customer, I want to reserve TrekLink devices for my group as part of booking, so that the agency knows how many units to hold before Staff finalizes allocation.

**Acceptance Criteria**:
1. WHEN a booking is submitted with a device count, the system SHALL create a soft device Reservation not yet bound to specific device IDs.
2. The reserved count SHALL NOT exceed the package's max-device constraint.
3. This reservation SHALL be converted to a specific-device allocation only at Staff review (US-028), not before.

### US-028 (`TK-36`): Allocate specific devices to a confirmed booking

`module:rentals` · **MF-01** · Actor: **Staff** · Priority: **High** · Points: **5** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-36` · **Branch**: `feat/TK-36-<short-desc>`

**Owner**: Lâm Phi Long (LongLP) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff, I want to allocate specific available devices to a confirmed booking, so that each unit is traceable to the group renting it.

**Acceptance Criteria**:
1. The system SHALL only allow allocating devices currently in Available status (reuses the US-019 guard).
2. WHEN allocation succeeds, the system SHALL transition each allocated device to Reserved.
3. IF fewer devices are Available than the booking requires, THEN the system SHALL reject the allocation with a clear count mismatch error.

### US-030 (`TK-38`): Generate rental agreement

`module:rentals` · **MF-01** · Actor: **Staff** · Priority: **Medium** · Points: **5** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-38` · **Branch**: `feat/TK-38-<short-desc>`

**Owner**: Lâm Phi Long (LongLP) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff, I want to generate a rental agreement document for a confirmed, allocated booking, so that there's a formal record of what was rented, deposit terms, and fee rules.

**Acceptance Criteria**:
1. The system SHALL generate the agreement from the booking + device allocation + pricing rule (E6) data, not free-typed fields.
2. The generated agreement SHALL be immutable once check-out (US-032) begins, later changes create an addendum, not an edit.
3. The agreement SHALL be retrievable by Staff, the assigned Guide, and the booking Customer.

### US-032 (`TK-40`): Device check-out workflow

`module:rentals` · **MF-01** · Actor: **Staff** · Priority: **High** · Points: **5** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-40` · **Branch**: `feat/TK-40-<short-desc>`

**Owner**: Lâm Phi Long (LongLP) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff, I want a check-out workflow that issues the allocated devices to the group, so that device status correctly reflects Rented → In-Field as the trip begins.

**Acceptance Criteria**:
1. WHEN check-out is completed, the system SHALL transition each allocated device Reserved→Rented, then In-Field once the trip start is confirmed.
2. Check-out SHALL be blocked if deposit (US-031) is not recorded.
3. Each device transition SHALL go through the FSM guard (US-013), not a direct field write.

### US-034 (`TK-42`): Device check-in workflow on return

`module:rentals` · **MF-01** · Actor: **Staff** · Priority: **High** · Points: **5** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-42` · **Branch**: `feat/TK-42-<short-desc>`

**Owner**: Lâm Phi Long (LongLP) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff, I want a check-in workflow when the group returns, so that devices transition In-Field→Returned and become eligible for inspection/fee calculation.

**Acceptance Criteria**:
1. WHEN check-in is completed, the system SHALL transition each returned device to Returned via the FSM guard.
2. The system SHALL capture a check-in timestamp used as the basis for late-return fee calculation (US-035).
3. Devices not physically returned SHALL remain In-Field and be flagged for Staff follow-up, not silently marked Returned.

### US-038 (`TK-46`): Guide: live group position/device status during trip

`module:monitoring` · **MF-04** · Actor: **Guide** · Priority: **Medium** · Points: **5** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-46` · **Branch**: `feat/TK-46-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB), Secondary: Trần Khải Hoàng · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a Guide, I want to see my group's live position and device status while on an active trip, so that I have field situational awareness (this read model is populated by E5's monitoring pipeline).

**Acceptance Criteria**:
1. WHILE a trip is In-Field, the system SHALL show live device positions/status to the assigned Guide via the shared WebSocket channel (US-053).
2. This view SHALL reuse the LiveMapWidget (US-054) rather than a separate Guide-only map implementation.
3. If the gateway is stale/disconnected, the view SHALL surface that state (US-065) rather than showing silently outdated positions.

## E4 (`TK-4`): Gateway & Offline Sync

### US-042 (`TK-50`): Freeze the eventId schema

`module:gateway-sync` · **MF-02** · Actor: **System** · Priority: **High** · Points: **3** · Sprint **1** · Status: **Ready**

**Jira**: `TK-50` · **Branch**: `feat/TK-50-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the team, we want the eventId scheme frozen and documented in specs/gateway-sync/design.md, so that every downstream module (gateway queue, backend ingestion, incidents) builds against one stable contract. RESOLVED as D-006: the original deviceId+sessionId+sequenceNumber form is NOT constructible - the firmware transmits neither sessionId nor sequenceNumber. Replaced by a split key: GatewayEvent.eventId = sha256(nodeNum:packetId) for packet dedup, plus an open-Incident lookup (not a hash) for episode correlation.

**Acceptance Criteria**:
1. The schema SHALL be documented in design.md before any gateway or backend ingestion code is written (hard TP1 gate). [DONE - design.md sections 1.1-2.4]
2. The eventId SHALL be usable as a natural idempotency key (unique, deterministic, derived from data the firmware actually transmits).
3. Any change to this schema after freeze SHALL be logged as a new decision in 03-decisions-and-risk-register.md, not a silent edit. [Honoured - see D-006.]
4. Per D-008 the firmware is editable: adding a boot sessionId + per-packet sequenceNumber firmware-side would restore the original scheme AND enable gap detection (proving loss, not just deduplicating arrivals). Evaluate as a layered upgrade - the split key stands either way.

### US-045 (`TK-53`): Gateway-side duplicate suppression

`module:gateway-sync` · **MF-02** · Actor: **System** · Priority: **Medium** · Points: **3** · Sprint **2** · Status: **Backlog**

**Jira**: `TK-53` · **Branch**: `feat/TK-53-<short-desc>`

**Owner**: Lâm Phi Long (LongLP) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the Gateway, I want to suppress re-enqueuing an eventId already in the local queue or already flushed, so that flaky serial reads don't multiply the same event before it even reaches the backend.

**Acceptance Criteria**:
1. IF an incoming eventId matches one already queued or already marked flushed, THEN the system SHALL discard the duplicate without re-inserting.
2. This check SHALL use the gateway-local unique constraint (US-043) as the enforcement mechanism, not just an in-memory set.
3. This is a defense-in-depth layer, backend idempotency (US-049) is still required and is the authoritative guarantee.

### US-049 (`TK-57`): Gateway health-reporting API

`module:gateway-sync` · **MF-02** · Actor: **System** · Priority: **Medium** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-57` · **Branch**: `feat/TK-57-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff/Admin, I want a gateway health endpoint (queue depth per tier, last sync time, retry count), so that the monitoring dashboard (E5) can surface gateway connectivity status instead of it being a black box.

**Acceptance Criteria**:
1. The endpoint SHALL report queue depth broken down by P0-P3 tier.
2. The endpoint SHALL report lastSyncAt and the current retry count for the oldest queued event.
3. This endpoint is what US-065 (connectivity indicator) consumes, it SHALL NOT be duplicated as a separate ad-hoc status field.

### US-052 (`TK-60`): Automated duplicate-delivery test

`module:gateway-sync` · **MF-02** · Actor: **System** · Priority: **High** · Points: **3** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-60` · **Branch**: `feat/TK-60-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the team, we want an automated test that delivers the same eventId 10 times and asserts exactly one downstream effect, so that the register's Duplicate Prevention NFR is continuously verified in CI, not just checked manually once.

**Acceptance Criteria**:
1. The test SHALL submit the identical event payload 10 times and assert exactly 1 resulting Incident/telemetry update.
2. The test SHALL run in the backend CI job (E7) on every PR touching gateway-sync or incidents.
3. A failing run of this test SHALL block merge, it directly verifies a graded NFR.

### US-043 (`TK-51`): SQLite local priority queue schema

`module:gateway-sync` · **MF-02** · Actor: **System** · Priority: **High** · Points: **5** · Sprint **2** · Status: **Backlog**

**Jira**: `TK-51` · **Branch**: `feat/TK-51-<short-desc>`

**Owner**: Lâm Phi Long (LongLP) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the Gateway, I want a local SQLite table with P0-P3 priority tiers, so that events persist across connectivity loss instead of being lost in memory.

**Acceptance Criteria**:
1. The schema SHALL include id, eventId, priority (P0-P3), payload, createdAt, retryCount.
2. eventId SHALL carry a unique constraint at the gateway level too, not just backend-side.
3. The queue logic SHALL be isolated from MQTT transport code so it's unit-testable without a live broker (04-architecture-conventions.md §3).

### US-044 (`TK-52`): Enqueue incoming LoRa events into the priority queue

`module:gateway-sync` · **MF-02** · Actor: **System** · Priority: **High** · Points: **5** · Sprint **2** · Status: **Backlog**

**Jira**: `TK-52` · **Branch**: `feat/TK-52-<short-desc>`

**Owner**: Lâm Phi Long (LongLP) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the Gateway, I want every parsed LoRa event enqueued with its correct priority tier (SOS=P0, incident-location=P1, GPS=P2, telemetry=P3), so that safety-critical events are never silently dropped.

**Acceptance Criteria**:
1. WHEN a message is parsed (US-041), the system SHALL classify it into P0-P3 and insert it into the local queue before any network attempt.
2. The system SHALL persist the event even if MQTT is unreachable at enqueue time.
3. Classification SHALL be unit-tested for at least one example of each priority tier.

### US-046 (`TK-54`): D-005 Gateway connectivity PoC

`module:gateway-sync` · **MF-02** · Actor: **System** · Priority: **High** · Points: **5** · Sprint **2** · Status: **Backlog**

**Jira**: `TK-54` · **Branch**: `feat/TK-54-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa), Secondary: Lâm Phi Long · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the team, we want to validate that the firmware's built-in Meshtastic MQTT-uplink module is sufficient for Wi-Fi/cellular connectivity at basecamp, so that D-005 (dedicated Gateway hardware vs. phone-bridging) can be closed before TP2 sprint planning locks in scope.

**Acceptance Criteria**:
1. The PoC SHALL demonstrate a TrekLink node publishing position/SOS/telemetry via its built-in MQTT module to our broker, no firmware or mobile-app changes.
2. The PoC result SHALL be logged back into D-005 in 03-decisions-and-risk-register.md as Resolved or Re-opened with evidence, not left implicit.
3. IF Option 1 (dedicated hardware) proves insufficient, THEN this story blocks TP2 Gateway Bridge scope until escalated to the supervisor per D-005's Action clause.

### US-047 (`TK-55`): MQTT publish client (gateway → broker)

`module:gateway-sync` · **MF-02** · Actor: **System** · Priority: **High** · Points: **5** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-55` · **Branch**: `feat/TK-55-<short-desc>`

**Owner**: Lâm Phi Long (LongLP) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the Gateway, I want an MQTT client that publishes queued events to the broker, so that the backend can receive them whenever connectivity is available.

**Acceptance Criteria**:
1. The system SHALL publish using MQTT QoS 1 (at-least-once), matching the register's stated protocol choice.
2. A successful publish acknowledgment SHALL mark the corresponding queue row as flushed, not delete it (audit trail).
3. Publish failures SHALL leave the row queued for the next flush attempt, not silently drop it.

### US-051 (`TK-59`): Backend: synchronization audit log

`module:gateway-sync` · **MF-02** · Actor: **System** · Priority: **Medium** · Points: **5** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-59` · **Branch**: `feat/TK-59-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Admin, I want a per-event processing history (received, processed, duplicate-rejected), so that RQ1/RQ2 experiment data (E8) has a source of truth to compute delivery/duplicate rates from.

**Acceptance Criteria**:
1. The system SHALL record one audit row per ingestion attempt, including whether it was accepted or rejected as duplicate.
2. Audit rows SHALL be append-only and queryable by time range and eventId prefix (deviceId).
3. This log SHALL be the data source for US-083's delivery-rate/duplicate-rate calculations, not a separate export mechanism.

### US-041 (`TK-49`): LoRa-to-Gateway serial parser (PoC)

`module:gateway-sync` · **MF-02** · Actor: **System** · Priority: **High** · Points: **8** · Sprint **1** · Status: **Ready**

**Jira**: `TK-49` · **Branch**: `feat/TK-49-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa), Secondary: Lâm Phi Long · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the Gateway, I want to parse LoRa mesh messages received over serial from the TrekLink firmware, so that position/SOS/telemetry packets can be enqueued for sync. This is TP1's explicit Week 1-2 PoC exit gate.

**Acceptance Criteria**:
1. The parser SHALL correctly decode the firmware's message schema for position, SOS, and telemetry packet types.
2. The parser SHALL be unit-testable against captured/sample serial payloads without live hardware.
3. This PoC SHALL be completed and demoed by TP1 Week 2 per the roadmap's risk mitigation for underestimated integration effort.

### US-048 (`TK-56`): Reconnection detection + priority-ordered flush

`module:gateway-sync` · **MF-02** · Actor: **System** · Priority: **High** · Points: **8** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-56` · **Branch**: `feat/TK-56-<short-desc>`

**Owner**: Lâm Phi Long (LongLP), Secondary: Đỗ Đăng Khoa · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the Gateway, I want to detect reconnection and flush the queue in strict priority order (all P0 before any P2/P3), so that safety-critical events are never delayed behind routine telemetry, this is a graded NFR (≥99% priority-ordering compliance).

**Acceptance Criteria**:
1. WHEN connectivity is restored, the system SHALL flush queued events ORDER BY priority ASC, createdAt ASC.
2. The flush routine SHALL be interruptible and resumable, a second connectivity drop mid-flush SHALL NOT lose or reorder remaining events.
3. This SHALL be integration-tested against simulated 30s/2min/5min/10min/30min connectivity-loss windows per the register's experiment matrix.

### US-050 (`TK-58`): Backend: idempotent event ingestion endpoint

`module:gateway-sync` · **MF-02** · Actor: **System** · Priority: **High** · Points: **8** · Sprint **3** · Status: **Backlog**

**Jira**: `TK-58` · **Branch**: `feat/TK-58-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa), Secondary: Lâm Phi Long · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the backend, I want to ingest gateway events using eventId as the idempotency key inside one DB transaction, so that N deliveries of the same event produce exactly one downstream effect (Incident, telemetry update, etc.).

**Acceptance Criteria**:
1. The system SHALL enforce a DB-level unique constraint on eventId as the last line of defense, not only an application-level check.
2. The idempotency check and any side-effect (e.g. Incident creation) SHALL happen inside the same transaction, never check-then-create as two round-trips.
3. This SHALL pass the register's NFR test: 20 simultaneous submissions of related events, 0 loss/duplication.

## E5 (`TK-5`): Real-Time Monitoring & SOS Incidents

### US-056 (`TK-64`): Device telemetry live display on map

`module:monitoring` · **MF-04** · Actor: **System** · Priority: **Medium** · Points: **3** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-64` · **Branch**: `feat/TK-64-<short-desc>`

**Owner**: Nguyễn Ngọc Long (LongNN) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff/Admin, I want battery and last-seen data shown on the live map markers, so that I can spot a device about to go dark before it becomes an incident.

**Acceptance Criteria**:
1. Markers SHALL show battery % and a relative last-seen time (e.g. "2m ago").
2. Stale telemetry (beyond a configurable threshold) SHALL visually distinguish itself from fresh telemetry on the marker.
3. This reuses the telemetry ingestion pipeline from US-016, no separate polling endpoint.

### US-059 (`TK-67`): Append-only incident audit trail

`module:incidents` · **MF-03** · Actor: **System** · Priority: **Medium** · Points: **3** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-67` · **Branch**: `feat/TK-67-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Admin, I want every incident state transition preserved permanently with actor, timestamp, and note, so that RQ3's traceability-score metric (% of transitions with complete actor+timestamp+action) can be computed directly from this data.

**Acceptance Criteria**:
1. Every transition from US-057 SHALL write one audit row, no update/delete endpoint SHALL exist for these rows.
2. The traceability-score calculation (US-087) SHALL be able to query this table directly without a separate export step.
3. The audit trail SHALL be visible to Staff/Admin as a read-only timeline on the Incident detail view.

### US-060 (`TK-68`): Staff: acknowledge an incident

`module:incidents` · **MF-03** · Actor: **Staff** · Priority: **High** · Points: **3** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-68` · **Branch**: `feat/TK-68-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff, I want to acknowledge a Detected incident, so that the system records who is taking ownership and starts the response clock.

**Acceptance Criteria**:
1. WHEN Staff acknowledges, the system SHALL transition Detected→Acknowledged via the FSM guard (US-057).
2. The acknowledgment timestamp SHALL be the value used for MTTA calculation (US-087), not a client-side timestamp.
3. The acknowledgment action SHALL require no more than 1 step / 2 fields (button + optional note) per the time-critical UX rule (06-frontend-conventions.md §3).

### US-061 (`TK-69`): Staff: update/coordinate an incident

`module:incidents` · **MF-03** · Actor: **Staff** · Priority: **Medium** · Points: **3** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-69` · **Branch**: `feat/TK-69-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff, I want to transition an incident to In Progress with a coordination note, so that the response effort is documented as it happens, not reconstructed afterward.

**Acceptance Criteria**:
1. WHEN Staff updates status to In Progress, the system SHALL require a non-empty action note.
2. Multiple In Progress updates SHALL each write a separate audit row, preserving the full coordination timeline.
3. Only Staff/Admin/the assigned Guide SHALL be authorized to update an incident's status.

### US-062 (`TK-70`): Staff: close/resolve an incident

`module:incidents` · **MF-03** · Actor: **Staff** · Priority: **Medium** · Points: **3** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-70` · **Branch**: `feat/TK-70-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff, I want to transition an incident through Resolved to Closed with a resolution note, so that MTTR (a graded RQ3 metric) and the audit trail have a definite end.

**Acceptance Criteria**:
1. WHEN Staff resolves, the system SHALL transition In Progress→Resolved, requiring a resolution note.
2. WHEN Staff closes a Resolved incident, the system SHALL transition Resolved→Closed, the terminal state per the FSM.
3. The Resolved timestamp SHALL be the value used for MTTR calculation (US-087).

### US-064 (`TK-72`): Staff: manually create a non-SOS incident

`module:incidents` · **MF-03** · Actor: **Staff** · Priority: **Low** · Points: **3** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-72` · **Branch**: `feat/TK-72-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff, I want to manually open an incident for a non-SOS emergency (e.g. a phoned-in report), so that the same tracked FSM/audit workflow applies even without a device-level SOS trigger.

**Acceptance Criteria**:
1. The system SHALL let Staff create an Incident directly in Detected state, optionally linked to a device/trip.
2. Manually created incidents SHALL go through the identical FSM (US-057) as auto-created ones, no separate code path.
3. The audit trail SHALL note that the incident was Staff-initiated, not device-triggered, for RQ3 baseline comparison purposes.

### US-065 (`TK-73`): Gateway connectivity status indicator

`module:monitoring` · **MF-04** · Actor: **Staff** · Priority: **Medium** · Points: **3** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-73` · **Branch**: `feat/TK-73-<short-desc>`

**Owner**: Nguyễn Ngọc Long (LongNN) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff/Admin, I want a visible per-gateway connectivity indicator (last-seen, "syncing" vs. "stale") on the dashboard, so that a silent gateway dropout is obvious, not hidden in a tooltip (06-frontend-conventions.md §4 Pattern B).

**Acceptance Criteria**:
1. The indicator SHALL consume the gateway health endpoint (US-048) directly.
2. A gateway with no sync beyond a configurable threshold SHALL visually flip to a "stale" state.
3. The indicator SHALL be visible on the main dashboard, not nested behind a secondary screen.

### US-066 (`TK-74`): Incident queue panel

`module:incidents` · **MF-03** · Actor: **Staff** · Priority: **Medium** · Points: **3** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-74` · **Branch**: `feat/TK-74-<short-desc>`

**Owner**: Trần Khải Hoàng (HoangTK) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff/Admin/Guide, I want a list/filter panel of active incidents beside the map, so that an active SOS is visible without scrolling (06-frontend-conventions.md §4 Pattern B).

**Acceptance Criteria**:
1. The panel SHALL list incidents filterable by status and sortable by created time.
2. An active (non-Closed) incident SHALL visually pulse/highlight per the Pattern B spec.
3. Selecting an incident SHALL center the live map (US-054) on its associated device/trip.

### US-053 (`TK-61`): WebSocket gateway (Socket.io) for live push

`module:monitoring` · **MF-04** · Actor: **System** · Priority: **High** · Points: **5** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-61` · **Branch**: `feat/TK-61-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a developer, I want one shared Socket.io gateway that all live features subscribe to, so that widgets don't each open their own connection (06-frontend-conventions.md §2).

**Acceptance Criteria**:
1. The system SHALL expose typed events (e.g. incident:new, device:telemetry) over a single namespace.
2. Connections SHALL be authenticated via the existing JWT, reusing the auth module rather than a parallel auth scheme.
3. The frontend SHALL hold this connection in one shared shared/socketClient.ts, not per-widget.

### US-057 (`TK-65`): Auto-create Incident from a valid SOS event

`module:incidents` · **MF-03** · Actor: **System** · Priority: **High** · Points: **5** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-65` · **Branch**: `feat/TK-65-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa), Secondary: Nguyễn Ngọc Long · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the system, I want to automatically create an Incident when a valid SOS event passes the idempotency check, so that no manual step stands between a firmware SOS broadcast and a tracked operational response.

**Acceptance Criteria**:
1. WHEN a SOS-type event passes idempotency (US-049), the system SHALL create exactly one Incident in Detected state within the same transaction.
2. The Incident SHALL link back to the originating device, trip, and eventId for traceability.
3. Re-delivery of the same eventId SHALL NOT create a second Incident (reuses US-049's guarantee, not a separate check).

### US-058 (`TK-66`): WebSocket push notification within 2 seconds

`module:incidents` · **MF-03** · Actor: **System** · Priority: **High** · Points: **5** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-66` · **Branch**: `feat/TK-66-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff/Guide, I want to be notified within 2 seconds of an Incident being created, so that response time (MTTA, a graded RQ3 metric) starts as close to real SOS trigger as possible.

**Acceptance Criteria**:
1. WHEN an Incident is created, the system SHALL push a notification to the assigned trip's Guide and to all online Staff/Admin within 2 seconds under normal load.
2. The notification payload SHALL include enough context (device, trip, location) to act without an extra fetch.
3. This latency SHALL be measured and reported as part of US-083/US-085's RQ evaluation, not just asserted.

### US-063 (`TK-71`): Guide: acknowledge + submit response notes

`module:incidents` · **MF-03** · Actor: **Guide** · Priority: **High** · Points: **5** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-71` · **Branch**: `feat/TK-71-<short-desc>`

**Owner**: Trần Khải Hoàng (HoangTK) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a Guide, I want to acknowledge an incident and submit response/resolution notes from the field, so that Staff has field-level context while coordinating.

**Acceptance Criteria**:
1. The system SHALL allow the assigned Guide to acknowledge independently of Staff's own acknowledgment, both are recorded, not merged into one flag.
2. Guide-submitted notes SHALL append to the same audit trail as Staff actions (US-064), attributed correctly by role.
3. This flow SHALL follow the same 1-step/2-field time-critical UX rule as US-059.

### US-088 (`TK-96`): Staff: distinguish and dismiss a Suspected (cadence-inferred) SOS episode

`module:incidents` · **MF-03** · Actor: **Staff** · Priority: **High** · Points: **5** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-96` · **Branch**: `feat/TK-96-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa) · **Reviewer**: Nguyễn Bá Tân (TanNB)

**User Story**: As Staff, I want a cadence-inferred (Suspected) SOS episode to be visually distinct from a Confirmed one and dismissible with a lighter-weight action, so that a false-positive detection doesn't force the same evidence-heavy Resolved-to-Closed workflow as a real emergency, while a genuine SOS whose single announcing text frame was lost to RF is still surfaced instead of silently missed (gateway-sync REQ-EVT-06, the mitigation for the Critical single-unacknowledged-text-frame risk in 03-decisions-and-risk-register.md).

**Acceptance Criteria**:
1. WHEN the cadence-anomaly detector (gateway-sync REQ-EVT-06) raises a Suspected episode, the system SHALL create the Incident with detectionConfidence=SUSPECTED, and the map/incident-queue UI SHALL render it with a visually distinct, lower-emphasis marker/badge from a Confirmed episode (US-054, US-065's Pattern B).
2. Staff SHALL be able to dismiss a Suspected episode via a single-step action distinct from the full Resolved-to-Closed flow (US-062), dismissal SHALL NOT require a resolution note, since no confirmed emergency was verified to have occurred.
3. WHEN a late-arriving SOS text frame upgrades a Suspected episode to Confirmed in place (not a new Incident, per gateway-sync design.md §1.3), the UI marker SHALL update to the Confirmed treatment and the full Resolved-to-Closed flow (US-060/061/062) SHALL become required from that point on.
4. Dismissing a Suspected episode SHALL still write an audit row (dismissed-as-false-positive), preserving RQ3 traceability even on the non-confirmed path.

### US-054 (`TK-62`): Incident 5-state FSM engine

`module:incidents` · **MF-03** · Actor: **System** · Priority: **High** · Points: **8** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-62` · **Branch**: `feat/TK-62-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a developer, I want an explicit transition table for Detected→Acknowledged→In Progress→Resolved→Closed, so that every incident state change is guarded and auditable, this FSM is a graded deliverable (UML State Machine diagram).

**Acceptance Criteria**:
1. The system SHALL reject any transition not in the allowed-transitions table, mirroring the device FSM pattern (04-architecture-conventions.md §2.1).
2. Every transition SHALL write an append-only audit row: actor (user ID + role), timestamp, action note.
3. The FSM SHALL be unit-tested for every legal transition and at least one illegal transition per state.

### US-055 (`TK-63`): Live operational map (MapLibre GL + Goong Maps)

`module:monitoring` · **MF-04** · Actor: **Staff** · Priority: **High** · Points: **8** · Sprint **4** · Status: **Backlog**

**Jira**: `TK-63` · **Branch**: `feat/TK-63-<short-desc>`

**Owner**: Nguyễn Ngọc Long (LongNN), Secondary: Trần Khải Hoàng · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff/Admin/Guide, I want a live map showing active trip positions, so that I have field situational awareness without polling manually.

**Acceptance Criteria**:
1. The map SHALL render device/trip markers colored by status per Pattern B (06-frontend-conventions.md §4).
2. Position updates SHALL arrive via the shared WebSocket channel (US-053), not polling.
3. The map SHALL be the LiveMapWidget consumed by both the Staff dashboard and the Guide's own trip view (US-038).

## E6 (`TK-6`): Billing & Reporting

### US-070 (`TK-78`): View invoice & payment status

`module:billing` · **MF-05** · Actor: **Customer** · Priority: **Low** · Points: **2** · Sprint **5** · Status: **Backlog**

**Jira**: `TK-78` · **Branch**: `feat/TK-78-<short-desc>`

**Owner**: Trần Khải Hoàng (HoangTK) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a Customer/Staff, I want to view an invoice's line items and payment status, so that there's transparency on what's owed and what's been paid.

**Acceptance Criteria**:
1. Customers SHALL only see invoices tied to their own bookings (ownership check).
2. The view SHALL show itemized base/late/damage charges plus current payment status.
3. This view reuses the invoice data model from US-068, no separate summarized/duplicated record.

### US-073 (`TK-81`): System health & audit-log report view

`module:billing` · **MF-05** · Actor: **Admin** · Priority: **Low** · Points: **2** · Sprint **5** · Status: **Backlog**

**Jira**: `TK-81` · **Branch**: `feat/TK-81-<short-desc>`

**Owner**: Nguyễn Ngọc Long (LongNN) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Admin, I want a view of system health (gateway connectivity summary, audit-log volume), so that operational health is visible without querying the database directly.

**Acceptance Criteria**:
1. The view SHALL summarize gateway health (US-048) across all active gateways, not just one.
2. The view SHALL show audit-log record counts (auth, device, incident) over a selectable date range.
3. This view is Admin-only (RBAC-gated, not visible to Staff).

### US-074 (`TK-82`): Billing dashboard widget

`module:billing` · **MF-05** · Actor: **Staff** · Priority: **Low** · Points: **2** · Sprint **5** · Status: **Backlog**

**Jira**: `TK-82` · **Branch**: `feat/TK-82-<short-desc>`

**Owner**: Trần Khải Hoàng (HoangTK) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Staff/Admin, I want a summary widget of revenue and outstanding payments, so that billing status is visible at a glance from the main dashboard.

**Acceptance Criteria**:
1. The widget SHALL show total revenue and total outstanding (Pending) payments for a selectable period.
2. The widget SHALL reuse the invoice/payment data model (US-068/069), no separate cached summary table that can drift out of sync.
3. Clicking the widget SHALL deep-link to the filtered invoice list.

### US-069 (`TK-77`): Mock/sandbox payment integration

`module:billing` · **MF-05** · Actor: **System** · Priority: **Low** · Points: **3** · Sprint **5** · Status: **Backlog**

**Jira**: `TK-77` · **Branch**: `feat/TK-77-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the system, I want a mock/sandbox payment flow with status tracking (Pending/Paid/Failed), so that the billing workflow is demonstrable without a production payment gateway, per the register's explicit MVP scope.

**Acceptance Criteria**:
1. The system SHALL mark every transaction with a sandbox:true flag per the WHERE-clause requirement in the register.
2. Payment status SHALL be one of Pending/Paid/Failed, transitioned only through this module, not written directly by other modules.
3. This SHALL be clearly labeled as sandbox in both API responses and the UI, so it's never mistaken for a real charge.

### US-071 (`TK-79`): Usage & device-utilization report

`module:billing` · **MF-05** · Actor: **Admin** · Priority: **Low** · Points: **3** · Sprint **5** · Status: **Backlog**

**Jira**: `TK-79` · **Branch**: `feat/TK-79-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Admin/Staff, I want a report on rentals and device utilization, so that fleet sizing and pricing decisions have data behind them.

**Acceptance Criteria**:
1. The report SHALL show rental counts and per-device utilization % over a selectable date range.
2. The report SHALL be derived from existing rental/device data, no separate manually maintained reporting table.
3. The report SHALL be exportable (CSV) for the SRS/documentation deliverable.

### US-072 (`TK-80`): Incident / response-performance report

`module:billing` · **MF-05** · Actor: **Admin** · Priority: **Low** · Points: **3** · Sprint **5** · Status: **Backlog**

**Jira**: `TK-80` · **Branch**: `feat/TK-80-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Admin, I want a report summarizing incident counts, MTTA, and MTTR over time, so that response-team performance is visible to management (this doubles as input to US-087's evaluation report).

**Acceptance Criteria**:
1. The report SHALL compute MTTA/MTTR from the incident audit trail (US-064) directly, matching the calculation used in US-087.
2. The report SHALL be filterable by date range and by trip/Guide.
3. The report SHALL be exportable (CSV).

### US-067 (`TK-75`): Manage rental pricing rules

`module:billing` · **MF-05** · Actor: **Admin** · Priority: **Medium** · Points: **5** · Sprint **5** · Status: **Backlog**

**Jira**: `TK-75` · **Branch**: `feat/TK-75-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As an Admin, I want to configure pricing rules (per device type, per day/trip, late-fee and damage-fee formulas), so that fee calculation (US-035/036) and invoicing (US-068) aren't hardcoded.

**Acceptance Criteria**:
1. The system SHALL let Admin define a base rate per device type and per day/trip.
2. The system SHALL let Admin define late-fee and damage-fee formulas referenced by US-035/US-036.
3. A pricing-rule change SHALL apply only to new agreements going forward, never retroactively to signed agreements (matches US-023's non-retroactive principle).

### US-068 (`TK-76`): Automatic invoice generation

`module:billing` · **MF-05** · Actor: **System** · Priority: **Medium** · Points: **5** · Sprint **5** · Status: **Backlog**

**Jira**: `TK-76` · **Branch**: `feat/TK-76-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the system, I want to generate an invoice automatically from a completed rental agreement (base charge + late fee + damage fee), so that Staff don't manually tally charges.

**Acceptance Criteria**:
1. WHEN check-in (US-034) completes and all fees (US-035/036) are calculated, the system SHALL generate one invoice itemizing base/late/damage charges.
2. The invoice SHALL be immutable once generated, corrections require a documented adjustment, not a silent edit.
3. Invoice generation SHALL be idempotent per rental agreement (re-triggering it SHALL NOT create a duplicate invoice).

## E7 (`TK-7`): DevOps / CI-CD

### US-077 (`TK-85`): Backend health-check endpoint

`module:devops` · **X-DevOps** · Actor: **System** · Priority: **Low** · Points: **2** · Sprint **1** · Status: **Ready**

**Jira**: `TK-85` · **Branch**: `feat/TK-85-<short-desc>`

**Owner**: Lâm Phi Long (LongLP) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Ops, I want a `/health` endpoint, so that uptime monitoring and the deployment guide have something concrete to point at.

**Acceptance Criteria**:
1. The endpoint SHALL report basic liveness (process up) without requiring auth.
2. The endpoint SHALL optionally report DB connectivity (Prisma $queryRaw ping) as a secondary field.
3. The endpoint SHALL use the standard response envelope like every other endpoint (no special-cased shape).

### US-079 (`TK-87`): Environment configuration matrix

`module:devops` · **X-DevOps** · Actor: **System** · Priority: **Low** · Points: **2** · Sprint **1** · Status: **Ready**

**Jira**: `TK-87` · **Branch**: `feat/TK-87-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a developer, I want .env.example fully covering every variable each package actually reads, so that onboarding doesn't involve guessing missing config.

**Acceptance Criteria**:
1. Every env var referenced in backend/gateway/frontend source SHALL have a corresponding entry in .env.example with a comment.
2. No secret/credential value SHALL be committed, only placeholder values.
3. The README's setup section SHALL reference this file rather than duplicating the variable list inline.

### US-076 (`TK-84`): GitHub Actions CI: lint + typecheck + test + build

`module:devops` · **X-DevOps** · Actor: **System** · Priority: **High** · Points: **3** · Sprint **1** · Status: **Backlog**

**Jira**: `TK-84` · **Branch**: `feat/TK-84-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the team, we want CI to run lint/typecheck/test/build on every PR across all 3 packages, so that broken code can't merge to dev/main.

**Acceptance Criteria**:
1. CI SHALL run for backend, gateway, and frontend as separate jobs so a failure in one doesn't hide the others' results.
2. The backend job SHALL run `prisma generate` before lint/build, since the Prisma client must exist for typecheck to pass.
3. A red CI run SHALL block merge per branch protection (07-github-workflow-git-conventions.md).

### US-078 (`TK-86`): GitHub Actions CD: build & push images on merge

`module:devops` · **X-DevOps** · Actor: **System** · Priority: **Low** · Points: **3** · Sprint **1** · Status: **Ready**

**Jira**: `TK-86` · **Branch**: `feat/TK-86-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB), Secondary: Đỗ Đăng Khoa · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As Ops, I want images built and pushed on merge to main, so that a deployable artifact always exists for the current main branch state.

**Acceptance Criteria**:
1. The workflow SHALL build and tag images for backend/gateway/frontend on push to main.
2. The workflow SHALL only run after the CI job (US-076) passes, no pushing an unverified image.
3. Image tags SHALL include the short commit SHA for traceability back to source.

### US-080 (`TK-88`): Deployment guide (clean-environment validated)

`module:devops` · **X-DevOps** · Actor: **System** · Priority: **Medium** · Points: **3** · Sprint **1** · Status: **Ready**

**Jira**: `TK-88` · **Branch**: `feat/TK-88-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the team, we want a deployment guide validated on a genuinely clean environment, so that Review 2/3 and the graders can stand the system up without tribal knowledge.

**Acceptance Criteria**:
1. The guide SHALL be followed literally on a fresh clone/VM by someone other than its author before being marked done.
2. The guide SHALL cover both docker-compose (US-075) and a manual npm-based path.
3. Any step that fails during validation SHALL be fixed in the guide, not worked around verbally.

### US-081 (`TK-89`): Seed/demo data script

`module:devops` · **X-DevOps** · Actor: **System** · Priority: **Low** · Points: **3** · Sprint **1** · Status: **Ready**

**Jira**: `TK-89` · **Branch**: `feat/TK-89-<short-desc>`

**Owner**: Lâm Phi Long (LongLP) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the team, we want a seed script producing a runnable demonstration environment (sample devices, trips, one triggered incident), so that Review/Defense demos don't start from an empty database.

**Acceptance Criteria**:
1. The script SHALL populate a representative set of devices across all 7 lifecycle states.
2. The script SHALL create at least one demo trip with an assigned Guide and one resolved Incident, so the full pipeline is visible immediately.
3. The script SHALL be idempotent, re-running it SHALL NOT duplicate seed data.

### US-075 (`TK-83`): Dockerfiles + docker-compose for all services

`module:devops` · **X-DevOps** · Actor: **System** · Priority: **Medium** · Points: **5** · Sprint **1** · Status: **Ready**

**Jira**: `TK-83` · **Branch**: `feat/TK-83-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa), Secondary: Lâm Phi Long · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As a developer, I want Dockerfiles for backend/gateway/frontend plus a docker-compose stack (Postgres, Mosquitto), so that the whole platform runs with one command on any machine, satisfying the Deployability NFR.

**Acceptance Criteria**:
1. Each of backend/gateway/frontend SHALL have a working multi-stage Dockerfile.
2. docker-compose.yml (already present) SHALL be extended to include Postgres and a Mosquitto MQTT broker service.
3. `docker compose up` SHALL bring up a working stack against a clean checkout with no manual steps beyond copying .env.example.

## E8 (`TK-8`): Research & Experimental Evaluation

### US-082 (`TK-90`): Design RQ1/RQ2 connectivity-loss experiment protocol

`module:docs` · **X-Research** · Actor: **System** · Priority: **High** · Points: **5** · Sprint **6** · Status: **Backlog**

**Jira**: `TK-90` · **Branch**: `feat/TK-90-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the team, we want the RQ1/RQ2 experiment protocol documented (connectivity-loss matrix, trial counts, measured variables) before running it, so that results are reproducible and defensible at Review 3/Defense 1.

**Acceptance Criteria**:
1. The protocol SHALL specify the connectivity-loss matrix exactly as registered: 0s/30s/2min/5min/10min/30min, 2 reconnection patterns, ≥20 trials/condition.
2. The protocol SHALL specify delivery rate, data-loss rate, duplicate rate, sync latency (mean/median/P95), and priority-ordering compliance as the measured variables.
3. The protocol SHALL be reviewed against 03-decisions-and-risk-register.md's risk mitigations before execution begins.

### US-083 (`TK-91`): Design RQ3 SOS-drill experiment protocol

`module:docs` · **X-Research** · Actor: **System** · Priority: **High** · Points: **5** · Sprint **6** · Status: **Backlog**

**Jira**: `TK-91` · **Branch**: `feat/TK-91-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the team, we want the RQ3 drill protocol documented (baseline vs. TrekLink condition, randomization, observer procedure), so that MTTA/MTTR/traceability comparisons are valid, not anecdotal.

**Acceptance Criteria**:
1. The protocol SHALL define the uncoordinated baseline exactly as registered (verbal/text acknowledgment, independent observer, hardware stopwatch, 0% traceability by definition).
2. The protocol SHALL specify ≥3 rotating participants, 15-20 drills per condition, randomized order, participants unaware of exact trigger time.
3. The protocol SHALL specify network-latency variation (LAN and 4G hotspot) as a controlled variable.

### US-087 (`TK-95`): Compile evaluation report

`module:docs` · **X-Research** · Actor: **System** · Priority: **Medium** · Points: **5** · Sprint **6** · Status: **Backlog**

**Jira**: `TK-95` · **Branch**: `feat/TK-95-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the team, we want RQ1/RQ2/RQ3 results compiled into the evaluation report, so that Review 3 and Defense 1 have a single, complete, sourced document rather than scattered raw data.

**Acceptance Criteria**:
1. The report SHALL present RQ1/RQ2 results (delivery/loss/duplicate rate, latency, priority compliance) against the register's NFR targets.
2. The report SHALL present RQ3 results (MTTA/MTTR/traceability/completion rate) comparing baseline vs. TrekLink condition.
3. The report SHALL be cross-referenced from 00-project-context/02-roadmap-and-milestones.md's Review 3 checklist as a completed deliverable.

### US-086 (`TK-94`): End-to-end integration test suite

`module:docs` · **X-Research** · Actor: **System** · Priority: **High** · Points: **8** · Sprint **6** · Status: **Backlog**

**Jira**: `TK-94` · **Branch**: `feat/TK-94-<short-desc>`

**Owner**: Đỗ Đăng Khoa (Khoa) · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the team, we want an integration suite covering idempotency (10x replay), concurrency (20x simultaneous), RBAC validation, and audit-log completeness, so that the NFRs graded at Review 3 are continuously verified, not manually re-checked before the defense.

**Acceptance Criteria**:
1. The suite SHALL include the 10x-duplicate-eventId test (reuses US-052) and a 20-simultaneous-submission concurrency test with 0 duplicates asserted.
2. The suite SHALL validate RBAC denial paths for at least one action per role boundary (Admin-only, Staff-only, Guide-ownership, Customer-ownership).
3. The suite SHALL assert audit-log completeness: every FSM transition in a test run has a corresponding audit row.

### US-084 (`TK-92`): Execute RQ1/RQ2 physical Gateway experiments

`module:docs` · **X-Research** · Actor: **System** · Priority: **High** · Points: **13** · Sprint **6** · Status: **Backlog**

**Jira**: `TK-92` · **Branch**: `feat/TK-92-<short-desc>`

**Owner**: Lâm Phi Long (LongLP), Secondary: Đỗ Đăng Khoa · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the team, we want to execute the RQ1/RQ2 protocol against 3-5 physical TrekLink devices and collect the metrics, so that the register's delivery-rate/latency/priority NFRs have empirical evidence, not an assumption.

**Acceptance Criteria**:
1. Physical devices SHALL be used for all mesh-to-gateway measurements; MQTT simulation may only supplement Gateway-to-Cloud load, never substitute for LoRa RF reliability claims.
2. Results SHALL be logged per-trial (not just aggregated) so P95 latency and per-condition breakdowns can be recomputed.
3. Raw results SHALL feed directly into US-087's evaluation report, not be re-summarized from memory afterward.

### US-085 (`TK-93`): Execute RQ3 randomized SOS drills

`module:docs` · **X-Research** · Actor: **System** · Priority: **High** · Points: **13** · Sprint **6** · Status: **Backlog**

**Jira**: `TK-93` · **Branch**: `feat/TK-93-<short-desc>`

**Owner**: Nguyễn Bá Tân (TanNB), Secondary: Đỗ Đăng Khoa · **Reviewer**: Đỗ Đăng Khoa (Khoa)

**User Story**: As the team, we want to execute the RQ3 drill protocol (baseline + TrekLink condition) and collect MTTA/MTTR/traceability/completion-rate data, so that the SOS-to-Incident pipeline's improvement over the status quo is measured, not assumed.

**Acceptance Criteria**:
1. Drills SHALL run per the protocol from US-084 with an independent observer and randomized trigger timing.
2. Both baseline and TrekLink-condition results SHALL be recorded with the same metrics for a like-for-like comparison.
3. A reduction in MTTA SHALL NOT be assumed in advance, outcomes are reported as measured, per the register's own stated caution.

