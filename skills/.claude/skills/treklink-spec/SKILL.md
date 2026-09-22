---
name: treklink-spec
description: Author or update a TrekLink module spec suite, requirements.md (EARS), design.md, tasks.md, api-design/. Trigger with "write the spec for", "we need requirements for", "design the X module", or whenever implementation is requested for a module whose spec suite does not yet exist.
argument-hint: <module name, e.g. "incidents" or "gateway-sync">
---

# /treklink-spec

Runs the spec-before-code gate from `_docs/01-conventions/02-spec-driven-development-workflow.md`.

> **No production code, database migration, or UI view exists before this suite does.** If someone
> asks you to implement a module with no spec, **the spec is the work.** Say so and start here.

## Usage

```
/treklink-spec $ARGUMENTS
```

Target: `treklink-web/specs/{module}/`, tracked at the repo root, **not** under `ignore/`, and not
stack-partitioned. TrekLink splits by module first; each module's spec states which layers it
covers.

```
specs/{module}/
├── requirements.md
├── design.md
├── tasks.md
└── api-design/
    ├── 00-api-testing-guide.md
    └── 01-post-devices-register.md
```

---

## Phase 1A: Clarification interview: HARD STOP

Read first: the charter section for this module, the backlog stories for it
(`_docs/03-backlog/02-user-stories.md`), the entities in dependent modules' `design.md`, and any
`OPEN` decision that touches it.

Then ask **5+ questions** targeting:

- **Domain edge cases**, e.g. what happens to an in-field device's rental record if a Guide
  reports it lost mid-trip?
- **Authorization**, which of Admin/Staff/Guide/Customer may trigger each action, and what
  ownership checks apply (a Guide sees only their assigned trips).
- **Reliability**, for `gateway-sync` and `incidents`: does this interact with idempotency or
  priority ordering?
- **Failure behaviour**, what the system does on each error condition.
- **Boundaries**, which other modules' exported services this will call.

**Stop. Wait. Write nothing until answered.**

## Phase 1B: `requirements.md` (EARS)

| Pattern | Template | TrekLink example |
|---|---|---|
| Ubiquitous | The system SHALL [response] | The system SHALL record actor and UTC timestamp on every incident state transition. |
| Event-driven | WHEN [trigger], the system SHALL [response] | WHEN a valid SOS event passes the idempotency check, the system SHALL create exactly one Incident and notify Staff + Guide within 2 seconds. |
| State-driven | WHILE [state], the system SHALL [response] | WHILE a device is in `Maintenance`, the system SHALL reject any rental allocation referencing it. |
| Unwanted | IF [condition], THEN the system SHALL [response] | IF the same `eventId` is delivered more than once, THEN the system SHALL discard the duplicate without creating a second Incident. |
| Optional | WHERE [feature/flag], the system SHALL [response] | WHERE sandbox payment mode is enabled, the system SHALL mark transactions `sandbox: true`. |

Number criteria `AC-01`, `AC-02`, … They are what the PR is reviewed against, so they must be
testable. **Stop for approval before Phase 2.**

## Phase 2: `design.md`

- Domain and data model: entities, enums, FK constraints.
- **Mermaid only** for every diagram. `stateDiagram-v2` for any FSM, the Device 7-state and
  Incident 5-state machines are **graded deliverables**, get them exactly right.
- `sequenceDiagram` for interaction flows.
- Service architecture: NestJS providers, MQTT topics, SQLite queue schema for `gateway-sync`.
- One `api-design/*.md` per endpoint from `_docs/02-templates/04-api-endpoint-template.md`, with
  full request/response samples, the response envelope, and a failure-case table.
- Frontend: FSD component architecture, server/client/form state, Zod schemas mirroring backend
  `class-validator` DTOs 1:1.

**Stop for approval before Phase 3.**

## Phase 3: `tasks.md`

Phased checklist. Every task references the requirement it satisfies.

```markdown
## Phase 1: Foundation & Domain Modeling
- [ ] 1.1 Define entities/enums (Prisma) — _AC-01, AC-02_
- [ ] 1.2 Write migration(s)
- [ ] 1.3 Add DTOs and error codes

## Phase 2: Core Service / Mutation Logic
- [ ] 2.1 Service methods with class-validator DTO input — _AC-03_
- [ ] 2.2 Wrap multi-table writes in a transaction
- [ ] 2.3 Unit test success + failure paths

## Phase 3: Query / Retrieval
## Phase 4: API Presentation Layer (Controller + JwtAuthGuard + PoliciesGuard + Swagger)
## Phase 5: Frontend Integration
## Phase 6: End-to-End Verification & DoD Audit
```

**Stop for approval.** Then, and only then, implementation may begin, via `/treklink-session`.

---

## Rules that apply throughout

- **Check the firmware ground truth** before specifying anything that touches a device.
  `_docs/00-project-context/04-firmware-ground-truth.md` records what is actually on the wire;
  several charter assumptions have already been disproven by it (see D-006).
- **Sync at the moment of discovery.** If implementation later reveals a requirement or design
  assumption was wrong, fix the spec in that same working pass, never queued for a later
  "update the docs" step.
- Specs are **tracked and committed**, never left in `ignore/`.
- English only.
