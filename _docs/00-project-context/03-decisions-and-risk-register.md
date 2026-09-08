# TrekLink — Decisions Log & Risk Register

Use this file like a lightweight ADR index. Anything marked **OPEN** blocks the dependent work listed under it — resolve before starting that work, not during.

## Decisions

### D-000 — Which register document is authoritative
- **Status**: ✅ Resolved
- **Context**: `Phieu_FA26SE159.docx` (individual registration form, detailed RQs/NFRs/TP1–TP6) and `Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.docx` (team draft, M1–M5 module framing) describe the same project at different fidelity, with minor differences (supervisor email domain `fe.edu.vn` vs `fpt.edu.vn`; module count 5 vs 5 core capabilities; TypeORM vs Prisma — see D-001).
- **Decision**: `Phieu_FA26SE159.docx` is authoritative for anything it specifies explicitly (RQs, NFRs, FSMs, task packages, experiment design). The FINAL draft is used only to fill gaps it doesn't cover.
- **Owner**: Team lead — confirm with supervisor at Review 1 kickoff that FA26SE159 is the version on file.

### D-001 — ORM: Prisma vs TypeORM
- **Status**: ✅ **Resolved** (Prisma ORM)
- **Decision**: Prisma ORM is locked as the team mandate for maximum productivity and type safety across backend services. PostgreSQL schema models and migrations are maintained in `backend/prisma/schema.prisma`.

### D-002 — Response envelope standard
- **Status**: ✅ Resolved
- **Decision**: All backend responses use the shape already defined in `API_Design_Template.md`: `{ "result": ..., "isSuccess": bool, "statusCode": int, "message": string }`. This supersedes the raw-DTO / `errorDetails[]` pattern from the previously-used `dev-flow.zip` (a different, .NET-project convention) — see `02-templates/04-api-endpoint-template.md` and `01-conventions/05-backend-conventions.md`.

### D-003 — GitLab → GitHub adaptation is cosmetic, not philosophical
- **Status**: ✅ Resolved
- **Decision**: Branch topology (`main`/`develop`/`features/Implementation_*`/`features/Design_*`/`hotfix/*`/`release/sprint_x`), commit discipline, and the dual Design+Implementation branch pattern from `Git_Lab_Guide.pdf` carry over unchanged. Only the tool-specific mechanics change: GitLab Issues/Labels/Milestones → GitHub Issues/Labels/Milestones+Projects; GitLab MRs → GitHub PRs (multi-template via `.github/PULL_REQUEST_TEMPLATE/`); GitLab child tasks → GitHub sub-issues/tasklists. See `01-conventions/07-github-workflow-git-conventions.md`.

### D-004 — Monorepo vs. multi-repo
- **Status**: ✅ **Resolved** (updated Sep 7, Session 2 — repos exist and this is what's actually cloned)
- **Context**: TrekLink has 4 codebases: firmware (inherited, read-only), gateway bridge (Node/TS), backend (NestJS), frontend (React). The org is `github.com/TrekLink-Team`. The original sketch (below, kept for history) considered 4 separate app repos.
- **Original options considered**: (a) 4 separate repos under the org (`treklink-firmware`, `treklink-gateway`, `treklink-backend`, `treklink-web`) with independent CI, or (b) one monorepo with workspaces (`apps/gateway`, `apps/backend`, `apps/web`, `firmware/` as a git submodule).
- **Decision actually taken**: a **hybrid** — 3 repos total under `TrekLink-Team`:
  - `treklink-docs` — this repo (SSOT, docs-only).
  - `treklink-firmware` — inherited SU26 firmware, frozen/read-only this term.
  - `treklink-web` — **one** active application repo containing the Gateway Bridge, NestJS backend, and React frontend as workspace packages (`gateway/`, `backend/`, `frontend/`), rather than 3 separate repos.
- **Rationale**: The firmware is a frozen, inherited dependency — keeping it fully separate avoids accidental edits being graded as "new" work, matching the register's note that firmware effort must be excluded from statistics. Splitting the *active* code further into 3 repos (original option a) was reconsidered: for a 5-person/13-week term, one repo with workspace packages keeps shared TypeScript types (e.g. the `eventId`/DTO shapes gateway and backend both touch), a single CI pipeline, and a single `npm install` — at the cost of coarser per-package branch protection, which `module:*` labels and path-scoped PR reviews (see `01-conventions/07-github-workflow-git-conventions.md`) substitute for.
- **Consequence**: `treklink-web/specs/{module}/` is the one spec root for gateway, backend, and frontend modules alike — see `01-conventions/02-spec-driven-development-workflow.md`. Update that doc's example paths if this ever splits back into separate repos.

### D-005 — Field-to-cloud bridge: dedicated Gateway hardware vs. Meshtastic mobile app
- **Status**: 🟡 **OPEN** — high-priority, revisit at TP1 PoC sign-off
- **Context**: The register describes the Gateway/Bridge as **dedicated TrekLink hardware with its own Wi-Fi/cellular uplink** (charter §2, FA26SE159 §b). In practice, the most readily-available connectivity in the field is the **Guide's or Customer's phone**: it's carried anyway, pairs to a mesh node over Bluetooth, and already has internet — via the stock, open-source **Meshtastic companion app** (Android + iOS). Two ways to use that path exist, at very different cost:
  1. **Preferred, low-risk**: stand up our own MQTT broker and use a TrekLink node's *built-in* Meshtastic MQTT-uplink module (already present in the inherited, frozen firmware) so a Wi-Fi/cellular-connected node publishes position/telemetry/SOS packets directly — no app changes needed. This is what the register already describes.
  2. **Fallback, high-risk**: fork the Meshtastic mobile apps (Android + iOS) to add custom bridging behavior beyond what the stock app's MQTT/HTTP settings expose. **The iOS side requires Xcode on macOS — the team has no Mac hardware**, making an iOS fork effectively infeasible this term; an Android-only fork would also split Guide/Customer device behavior by platform.
- **Recommendation**: Default to Option 1, matching the register's own wording. No TP should plan mobile-app-forking work unless Option 1 is proven insufficient during TP1's Gateway PoC (field Wi-Fi/cellular coverage at basecamp turns out unreliable, etc.) — if that happens, prefer wrapping the stock app's existing MQTT/HTTP integration points over forking the app itself, and escalate to the supervisor before committing sprint capacity to it.
- **Blocks**: TP1's Gateway/bridge sync architecture design (`specs/gateway-sync/design.md`) and PoC serial parser; TP2's Gateway Bridge implementation.
- **Action**: Confirm Option 1 is technically sufficient during TP1's PoC (Week 1–2, per the roadmap's risk mitigation for "NestJS + MQTT + WebSocket integration underestimated"). If not, this decision must be re-opened and escalated before TP2 sprint planning locks in Gateway Bridge scope.

## Risk register (carried from FA26SE159, kept live)

| Risk | Likelihood | Impact | Mitigation | Status |
|---|---|---|---|---|
| Insufficient physical TrekLink devices | Medium | High | Simulate Gateway→Cloud load via MQTT scripts; simulation never substitutes for LoRa RF reliability claims | Open |
| Gateway sync latency exceeds 5s NFR | Medium | Medium | Tune MQTT QoS, reduce payload size, backpressure on queue flush | Open |
| RQ3 baseline not objectively measurable | High | Medium | Randomized simulation drills; independent observer triggers SOS, records timestamp; participants unaware of exact trigger time | Open |
| NestJS + MQTT + WebSocket integration underestimated | Medium | High | PoC gateway→backend integration in TP1 Week 2, not deferred to TP3 | Open |
| Firmware message schema incompatible with new gateway | Low | High | Schema frozen & documented in TP1 before any gateway implementation | Open — tracked as TP1 exit gate |
| Scope creep | High | Medium | Feature freeze after TP5 Week 10; anything else goes to post-capstone backlog | Open |
| **[Added]** ORM indecision stalls TP3 start | Medium | Medium | Force D-001 resolution before Sprint 2 ends (Week 4) | Open |
| **[Added]** Field connectivity may need phone-based bridging instead of a dedicated Gateway node (D-005) | Medium | High | Validate dedicated Gateway (Wi-Fi/cellular node, native Meshtastic MQTT module) in TP1 PoC before committing to it; mobile-app forking treated as out of scope given no macOS/Xcode access | Open |
