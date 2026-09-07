# TrekLink — Decisions Log & Risk Register

Use this file like a lightweight ADR index. Anything marked **OPEN** blocks the dependent work listed under it — resolve before starting that work, not during.

## Decisions

### D-000 — Which register document is authoritative
- **Status**: ✅ Resolved
- **Context**: `Phieu_FA26SE159.docx` (individual registration form, detailed RQs/NFRs/TP1–TP6) and `Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.docx` (team draft, M1–M5 module framing) describe the same project at different fidelity, with minor differences (supervisor email domain `fe.edu.vn` vs `fpt.edu.vn`; module count 5 vs 5 core capabilities; TypeORM vs Prisma — see D-001).
- **Decision**: `Phieu_FA26SE159.docx` is authoritative for anything it specifies explicitly (RQs, NFRs, FSMs, task packages, experiment design). The FINAL draft is used only to fill gaps it doesn't cover.
- **Owner**: Team lead — confirm with supervisor at Review 1 kickoff that FA26SE159 is the version on file.

### D-001 — ORM: Prisma vs TypeORM
- **Status**: 🟡 **OPEN**
- **Context**: FA26SE159's tech stack table and Practical section both say **TypeORM** with PostgreSQL migrations. The team's FINAL draft tech stack table says **Prisma ORM**. This affects entity conventions, migration tooling, and the architecture doc — see `01-conventions/04-architecture-conventions.md`, which is written ORM-agnostically until this is resolved.
- **Blocks**: Any TP3 work that writes entities/migrations (device fleet, rental, incident, billing schemas).
- **Recommendation to resolve at Review 1 prep**: If the submitted, gradable form says TypeORM, default to TypeORM to match what's on record with the supervisor — deviating from a registered proposal without sign-off is a bigger risk than an ORM preference. Flag the actual choice explicitly at Review 1 so it's on record either way.
- **Action**: Pick one, record the outcome here, delete the other option from `04-architecture-conventions.md`'s callout box.

### D-002 — Response envelope standard
- **Status**: ✅ Resolved
- **Decision**: All backend responses use the shape already defined in `API_Design_Template.md`: `{ "result": ..., "isSuccess": bool, "statusCode": int, "message": string }`. This supersedes the raw-DTO / `errorDetails[]` pattern from the previously-used `dev-flow.zip` (a different, .NET-project convention) — see `02-templates/04-api-endpoint-template.md` and `01-conventions/05-backend-conventions.md`.

### D-003 — GitLab → GitHub adaptation is cosmetic, not philosophical
- **Status**: ✅ Resolved
- **Decision**: Branch topology (`main`/`develop`/`features/Implementation_*`/`features/Design_*`/`hotfix/*`/`release/sprint_x`), commit discipline, and the dual Design+Implementation branch pattern from `Git_Lab_Guide.pdf` carry over unchanged. Only the tool-specific mechanics change: GitLab Issues/Labels/Milestones → GitHub Issues/Labels/Milestones+Projects; GitLab MRs → GitHub PRs (multi-template via `.github/PULL_REQUEST_TEMPLATE/`); GitLab child tasks → GitHub sub-issues/tasklists. See `01-conventions/07-github-workflow-git-conventions.md`.

### D-004 — Monorepo vs. multi-repo
- **Status**: 🟡 **OPEN**
- **Context**: TrekLink has 4 codebases: firmware (inherited, read-only), gateway bridge (Node/TS), backend (NestJS), frontend (React). The org is `github.com/TrekLink-Team`.
- **Options**: (a) 4 separate repos under the org (`treklink-firmware`, `treklink-gateway`, `treklink-backend`, `treklink-web`) with independent CI, or (b) one monorepo with workspaces (`apps/gateway`, `apps/backend`, `apps/web`, `firmware/` as a git submodule).
- **Recommendation**: Multi-repo. The firmware is a frozen, inherited dependency (not touched this term) — bundling it into a monorepo adds no value and risks accidental edits being graded as "new" work, which conflicts with the register's explicit note that firmware effort must be excluded from statistics. Gateway/Backend/Frontend are independently deployable and owned by overlapping-but-different pairs of teammates during parallel sprints (see roadmap §5), which also favors separate repos with separate CI pipelines.
- **Action**: Confirm at Review 1 prep; create the 3 active repos (+ 1 read-only mirror or submodule reference to the firmware repo) once confirmed.

## Risk register (carried from FA26SE159, kept live)

| Risk | Likelihood | Impact | Mitigation | Status |
|---|---|---|---|---|
| Insufficient physical TrekLink devices | Medium | High | Simulate Gateway→Cloud load via MQTT scripts; simulation never substitutes for LoRa RF reliability claims | Open |
| Gateway sync latency exceeds 5s NFR | Medium | Medium | Tune MQTT QoS, reduce payload size, backpressure on queue flush | Open |
| RQ3 baseline not objectively measurable | High | Medium | Randomized simulation drills; independent observer triggers SOS, records timestamp; participants unaware of exact trigger time | Open |
| NestJS + MQTT + WebSocket integration underestimated | Medium | High | PoC gateway→backend integration in TP1 Week 2, not deferred to TP3 | Open |
| Firmware message schema incompatible with new gateway | Low | High | Schema frozen & documented in TP1 before any gateway implementation | Open — tracked as TP1 exit gate |
| Scope creep | High | Medium | Feature freeze after TP5 Week 10; anything else goes to post-capstone backlog | Open |
| **[Added]** ORM/monorepo indecision stalls TP3 start | Medium | Medium | Force D-001/D-004 resolution before Sprint 2 ends (Week 4) | Open |
