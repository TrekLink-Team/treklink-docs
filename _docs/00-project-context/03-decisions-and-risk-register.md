# TrekLink: Decisions Log & Risk Register

Use this file like a lightweight ADR index. Anything marked **OPEN** blocks the dependent work listed under it, resolve before starting that work, not during.

## Decisions

### D-000: Which register document is authoritative
- **Status**: ✅ Resolved
- **Context**: `Phieu_FA26SE159.docx` (individual registration form, detailed RQs/NFRs/TP1–TP6) and `Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.docx` (team draft, M1–M5 module framing) describe the same project at different fidelity, with minor differences (supervisor email domain `fe.edu.vn` vs `fpt.edu.vn`; module count 5 vs 5 core capabilities; TypeORM vs Prisma, see D-001).
- **Decision**: `Phieu_FA26SE159.docx` is authoritative for anything it specifies explicitly (RQs, NFRs, FSMs, task packages, experiment design). The FINAL draft is used only to fill gaps it doesn't cover.
- **Owner**: Team lead, confirm with supervisor at Review 1 kickoff that FA26SE159 is the version on file.

### D-001: ORM: Prisma vs TypeORM
- **Status**: ✅ **Resolved** (Prisma ORM)
- **Decision**: Prisma ORM is locked as the team mandate for maximum productivity and type safety across backend services. PostgreSQL schema models and migrations are maintained in `backend/prisma/schema.prisma`.

### D-002: Response envelope standard
- **Status**: ✅ Resolved
- **Decision**: All backend responses use the shape already defined in `API_Design_Template.md`: `{ "result": ... "isSuccess": bool, "statusCode": int, "message": string }`. This supersedes the raw-DTO / `errorDetails[]` pattern from the previously-used `dev-flow.zip` (a different, .NET-project convention), see `02-templates/04-api-endpoint-template.md` and `01-conventions/05-backend-conventions.md`.

### D-003: GitLab → GitHub adaptation is cosmetic, not philosophical
- **Status**: ⛔ **SUPERSEDED by D-009** (2026-09-13). Kept verbatim below for history, do not follow it.
- **Decision** *(superseded)*: Branch topology (`main`/`develop`/`features/Implementation_*`/`features/Design_*`/`hotfix/*`/`release/sprint_x`), commit discipline, and the dual Design+Implementation branch pattern from `Git_Lab_Guide.pdf` carry over unchanged. Only the tool-specific mechanics change: GitLab Issues/Labels/Milestones → GitHub Issues/Labels/Milestones+Projects; GitLab MRs → GitHub PRs (multi-template via `.github/PULL_REQUEST_TEMPLATE/`); GitLab child tasks → GitHub sub-issues/tasklists. See `01-conventions/07-github-workflow-git-conventions.md`.

### D-004: Monorepo vs. multi-repo
- **Status**: ✅ **Resolved** (updated Sep 7, Session 2, repos exist and this is what's actually cloned)
- **Context**: TrekLink has 4 codebases: firmware (inherited, read-only), gateway bridge (Node/TS), backend (NestJS), frontend (React). The org is `github.com/TrekLink-Team`. The original sketch (below, kept for history) considered 4 separate app repos.
- **Original options considered**: (a) 4 separate repos under the org (`treklink-firmware`, `treklink-gateway`, `treklink-backend`, `treklink-web`) with independent CI, or (b) one monorepo with workspaces (`apps/gateway`, `apps/backend`, `apps/web`, `firmware/` as a git submodule).
- **Decision actually taken**: a **hybrid**, 3 repos total under `TrekLink-Team`:
  - `treklink-docs`, this repo (SSOT, docs-only).
  - `treklink-firmware`, inherited SU26 firmware, frozen/read-only this term.
  - `treklink-web`, **one** active application repo containing the Gateway Bridge, NestJS backend, and React frontend as workspace packages (`gateway/`, `backend/`, `frontend/`), rather than 3 separate repos.
- **Rationale**: The firmware is a frozen, inherited dependency, keeping it fully separate avoids accidental edits being graded as "new" work, matching the register's note that firmware effort must be excluded from statistics. Splitting the *active* code further into 3 repos (original option a) was reconsidered: for a 5-person/13-week term, one repo with workspace packages keeps shared TypeScript types (e.g. the `eventId`/DTO shapes gateway and backend both touch), a single CI pipeline, and a single `npm install`, at the cost of coarser per-package branch protection, which `module:*` labels and path-scoped PR reviews (see `01-conventions/07-github-workflow-git-conventions.md`) substitute for.
- **Consequence**: `treklink-web/specs/{module}/` is the one spec root for gateway, backend, and frontend modules alike, see `01-conventions/02-spec-driven-development-workflow.md`. Update that doc's example paths if this ever splits back into separate repos.

### D-005: Field-to-cloud bridge topology
- **Status**: ✅ **Resolved and closed** (2026-09-16, Session 6), staged rollout, **both stages in permanent scope**. Supersedes the earlier "Stage B is tradeable" framing.
- **Context**: The register describes the Gateway/Bridge as **dedicated TrekLink hardware with its own Wi-Fi/cellular uplink** (charter §2, FA26SE159 §b). Session 3 established the physical constraint that closes this: **the Gateway Bridge machine is not carried during the trek.** It sits at basecamp. The guide carries a node, not a laptop.
- **Options considered**:
  1. **Basecamp-fixed bridge**, a designated node USB-tethered to the basecamp machine running `gateway/src`; the SQLite P0–P3 queue buffers the machine's intermittent Wi-Fi uplink. Requires no firmware work.
  2. **Node's built-in MQTT uplink, no bridge**, the guide's node publishes to Mosquitto over its own Wi-Fi using the stock Meshtastic MQTT module already compiled into the frozen firmware. Simplest possible path; **has no buffer anywhere.**
  3. **Fork the Meshtastic mobile apps**, rejected outright. iOS requires Xcode on macOS, which the team does not have; an Android-only fork would split Guide/Customer behavior by platform, and mobile apps are explicitly out of charter scope.
- **Decision**: Build **Option 2 first (Stage A, TP1)**, then **add Option 1 on top (Stage B, TP2)** as an additional ingress adapter plus a hard-wired gateway node. Option 3 stays rejected.
- **Rationale**: Option 2 is the shortest path to an end-to-end demo and needs no serial parser, no hardware tether, and no protobuf decoding. It is only non-throwaway because of the ingress-adapter seam defined in **D-007**, Stage B reuses the entire normalizer and ingestion pipeline and contributes only a new adapter in front of it.
- **⚠️ Known gap, deliberately accepted for Stage A**: Option 2 has **zero offline buffering**. Stock Meshtastic MQTT drops packets when the uplink is down (verified Session 2), and Store & Forward is a mesh-internal, PSRAM-only, ~30-packet chat replay, not a cloud-sync buffer. Therefore, **while only Stage A exists**, the following charter §5 NFRs are unmeasurable and RQ1/RQ2 are unanswerable:
  - Offline recovery delivery rate ≥99% after reconnection (30s–30min loss)
  - Priority-ordering compliance ≥99%, all P0 flushed before P2/P3 on reconnect
  - Gateway→cloud sync ≤5s *when uplink returns* (the ≤5s steady-state figure is still measurable)

  These are restored by Stage B, where the SQLite queue sits in the uplink path and loss is induced by killing the bridge's Wi-Fi.
- **Scoping note that makes Stage B sufficient**: every offline NFR in charter §5 is scoped to the **gateway→cloud** leg, not the **node→gateway** mesh leg. Charter §1 gap #1 reads *"no store-and-forward path to the cloud… there is no Gateway between the mesh and a backend."* Mesh-range loss (a node out of LoRa range of any relay) is an RF-coverage problem, already carried as an RF-reliability caveat in the risk table below, and is **not** claimed as in scope. A basecamp-fixed bridge therefore exercises exactly the leg the research questions measure.
- **Hardware scope** (settled Session 3): **Stage A targets v2/v3/v4 only. v1 is out of the demo set.** v1 compiles MQTT out entirely (`-D MESHTASTIC_EXCLUDE_MQTT=1`, `variants/esp32/treklink_v1_0/platformio.ini:10`), the module is removed at build time, so no runtime configuration can enable it. v2/v3/v4 omit that flag and all carry Wi-Fi silicon, so any of them can serve as the uplink node. Were v1 ever needed, deleting the build flag is a one-line change now that D-008 permits firmware edits.
- ~~**Stage B is tradeable scope**~~, **struck (Session 6).** Stage B is permanent scope. Two independent reasons, either of which alone is sufficient:
  1. **The supervisor put it in the mainflow set.** `Documents/course-material/TrekLink-proposed-mainflow-ducndm.png` defines **MF-02, Field Data → Offline Gateway → Cloud Synchronization**, and draws the Gateway Bridge (Node.js) with its SQLite offline queue and priority-ordered reconnection flush as the substance of that flow. Dropping Stage B would delete a supervisor-specified mainflow. See **D-016**.
  2. **The scope constraint that motivated the trade is gone.** At the 2026-09-13 meeting the supervisor granted the team latitude to set its own scope and tech stack, subject to pitching and defending it. There is no longer a scope-reduction pressure to spend Stage B on.
- **Consequence**: charter §5's offline-recovery and priority-ordering NFRs and **RQ1/RQ2 stay binding and must be delivered.** Stage A remains the first increment, not a substitute, never present Stage A as satisfying the offline-recovery NFR.
- **Blocks**: nothing, `specs/gateway-sync/{requirements,design,tasks}.md` are written against this decision. Stage B's isolation in Phase 9 is retained as sequencing, no longer as a removal seam.

### D-006: `eventId` redefinition: the charter's scheme is not constructible
- **Status**: ✅ **Resolved** (Session 3), supersedes charter §2 and `01-conventions/04-architecture-conventions.md` §3
- **Context**: Charter §2 and the architecture conventions both specify `eventId = DeviceID + SessionID + SequenceNumber` as the backend idempotency key. Direct inspection of the frozen firmware shows **neither `SessionID` nor `SequenceNumber` exists anywhere**, not in the TrekLink modules, not in the Meshtastic packet format. The only per-packet identifier transmitted is `MeshPacket.id`, and `Router.cpp:168` (`generatePacketId()`) shows it is a 10-bit rolling counter OR'd with 22 random high bits, re-seeded randomly at every boot. It is a flood-dedup token, **not** a monotonic sequence. The charter's key cannot be built from what the hardware actually sends.
- **Options considered**:
  1. **Split the key** into a packet-level dedup key and an episode-level correlation key.
  2. **Single content-addressed key**, `hash(from : rx_time : portnum : payload)`, rejected: the SOS beacon retransmits every 5s (then 30s) with a fresh `rx_time`, so one SOS episode would mint a new key per tick and create N Incidents from one fall.
  3. **Bridge synthesizes session + sequence**, rejected: the key would then describe the *bridge*, not the device. Restart the bridge, replay the same packets, and every key is new; deduplication becomes a silent no-op, which is precisely the failure the 10× replay NFR exists to catch.
- **Decision** (Option 1):
  - **Packet dedup key**, `GatewayEvent.eventId = sha256(nodeNum : packetId)`. Satisfies charter §5's *"0 duplicate Incidents for repeated eventId delivery (10× replay test)."* Enforced by a unique index; conflict is a no-op insert inside the ingestion transaction.
  - **Episode correlation**, *not* a hash. On SOS ingest, look up an open `Incident` for the same device whose `lastEventAt` falls inside the episode window; append if found, create if not. An earlier draft used `hash(nodeNum : timeBucket)`, which was discarded: a bucket boundary falling mid-episode splits one SOS into two Incidents, the exact failure the key exists to prevent.
- **Consequences**:
  - `backend/prisma/schema.prisma`: `Incident.eventId @unique` currently serves as *both* keys and must be split, `Incident` gains `lastEventAt` and an index on `(deviceId, status, lastEventAt)`, and references its originating `GatewayEvent` by FK rather than carrying a duplicate unique string.
  - **`01-conventions/04-architecture-conventions.md` §3 still states the old formula and is now contradicted by this decision. It must be updated before any `gateway-sync` implementation branch opens.**
  - Charter §2's wording stands as the *intent* (a natural, device-derived idempotency key); this decision records the constructible form of it.
- **Reopened by D-008** (firmware is editable): adding a boot-`sessionId` and a per-packet `sequenceNumber` firmware-side would make the charter's original formula constructible and would give a genuinely monotonic sequence, strictly better than hashing a randomized packet id, and it would let the platform *detect gaps* (a missing sequence number proves loss) rather than merely deduplicating what arrives. **The split key above remains correct and functional with or without it**; treat a firmware sequence as a layered upgrade to evaluate next session, not a prerequisite for TP1.

### D-007: Canonical event envelope + Strategy-based normalizer (the ingress seam)
- **Status**: ✅ **Resolved** (Session 3)
- **Context**: Stage A (node MQTT) and Stage B (serial bridge) do **not** speak the same wire format. The node's MQTT module publishes to a hardcoded topic shape, `<root>/2/e/<channelId>/<nodeId>` carrying a `ServiceEnvelope` protobuf, or `<root>/2/json/<channelId>/<nodeId>` carrying JSON when `json_enabled` (`src/mqtt/MQTT.cpp:423–430`, `:798`). `<root>` is configurable; `/2/e/` and the payload type are not. Meanwhile `gateway/src/mqtt/mqtt-client.ts` publishes `treklink/events/priority/{0..3}` with a TrekLink-shaped payload. If the backend parses Stage A's format directly, Stage B's arrival forces a rewrite of the ingestion layer, and D-005's staged plan quietly becomes throwaway work.
- **Decision**: The backend ingests exactly one internal type, **`TrekLinkEvent`**. Between the wire and the domain sit two seams:
  1. **Ingress adapters** (`MeshIngressAdapter`), one per topology, responsible only for getting bytes off a transport and producing a `RawMeshPacket`. Stage A ships `MqttJsonIngressAdapter`; Stage B adds `SerialBridgeIngressAdapter`. Adapters hold no domain logic.
  2. **Normalizer** (`MeshNormalizerService`), the Strategy-pattern context. It resolves a `PacketNormalizationStrategy` by PortNum from an injected registry and delegates. Strategies are pure (no I/O, no Prisma) and each owns one PortNum's mapping to a domain event kind and priority tier. Adding a PortNum means adding a strategy class and registering it; the normalizer itself never changes (Open/Closed).
- **Rationale**: the normalizer holds ~all the genuinely hard logic (SOS prefix parsing, priority assignment, `eventId` derivation, episode correlation) and is 100% shared between stages. Purity makes it unit-testable without a broker, a device, or a database, which is what makes the charter's dedup/ordering/concurrency NFRs cheap to test rather than integration-only.
- **Stage A transport config, frozen**: `json_enabled = true`, `encryption_enabled = false`, `root = "treklink"`. JSON removes any protobuf dependency from NestJS, and the JSON serializer covers the three PortNums TrekLink actually emits, `TEXT_MESSAGE_APP`, `POSITION_APP`, `TELEMETRY_APP` (`src/serialization/MeshPacketSerializer.cpp:28`, `:208`, `:56`). `encryption_enabled = false` is required so the broker receives decrypted packets; the field's own comment in `module_config.pb.h` notes decrypted output exists for exactly this purpose. The alternative is reimplementing Meshtastic's AES-CTR channel crypto in NestJS.
- **Known limitation of the JSON path**: the JSON envelope (`MeshPacketSerializer.cpp:410–424`) carries `id`, `timestamp`, `to`, `from`, `channel`, `type`, `sender`, `payload`, `rssi`, `snr`, `hops_away`, but **not `MeshPacket.priority`**. The SOS position packet is sent with `priority = MAX` (`TrekLinkSOSHelper.cpp:119`) and is therefore indistinguishable from a routine position report on this path. Handled by backend episode correlation with a backward grace window (see `specs/gateway-sync/design.md` §2.4). Switching to the `/2/e/` protobuf topic would recover `priority` directly and is logged as the deferred precision upgrade.

### D-008: The firmware is editable this term (supersedes the "frozen / read-only" framing)
- **Status**: ✅ **Resolved and closed** (2026-09-16, Session 6). All three sub-questions answered; no part of this decision remains open.
- **Context**: `README.md` §1, charter §2, and D-004's rationale all describe `treklink-firmware` as *"Frozen / read-only this term. Branch-protected. Not a deliverable."* Sessions 1–3 reasoned under that constraint and, on its strength, classified several firmware-rooted defects as unfixable-by-design. **The team lead has confirmed this is wrong**: the team owns the repo, can modify and build it, and can reflash the physical units.
- **Decision**: firmware modification is **technically available** and may be used to fix defects that cannot be worked around from the platform side. All prior "unfixable without touching frozen firmware" conclusions are void and must be re-derived.
- **The distinction that still matters**, three separate claims were bundled under one word:
  1. *Can we edit it?*, **Yes.** Settled.
  2. *Is firmware work in scope?*, **Yes** (answered 2026-09-13, supervisor). Firmware **enhancement and integration** is an accepted development path, not the out-of-scope "firmware redesign." Extending the firmware so the platform integrates with it more deeply, a custom PortNum, an explicit SOS discriminator, a boot `sessionId` + per-packet `sequenceNumber`, beacon priority, is treated as building the product, not rebuilding the inherited component. The charter's exclusion is read narrowly, as prohibiting a rearchitecture of the mesh stack.
  3. *Does firmware effort count toward graded deliverables?*, **Yes** (answered 2026-09-13, supervisor), with the caveat that assessment is not code volume alone. This supersedes D-004's rationale citing "the register's note that firmware effort must be excluded from statistics"; that note is treated as an accounting convention for source statistics, not as a bar on credit.
- **Working rule (Session 6)**: firmware changes are a **first-class option**, evaluated on merit against the platform-side alternative rather than treated as a last resort. Prefer whichever is more robust for the same cost; where the firmware fix is strictly better, as with the SOS discriminator and beacon priority, take it. Keep each change individually justified and logged here. Still excluded: rearchitecting the Meshtastic mesh stack.
- **Reopens**:
  - **D-006**, a firmware-side boot-`sessionId` + per-packet `sequenceNumber` would make the charter's original `eventId` formula constructible. The split key stays valid regardless; this would be a layered upgrade.
  - **The Critical SOS risk below**, the single-unacknowledged-text-frame failure is now firmware-fixable (custom PortNum, `want_ack`, or retransmitting the discriminator with each beacon) rather than mitigable only by heuristic.
  - **D-007's SOS discrimination**, a real custom PortNum would retire the `printf`-format string parser entirely.
  - **v1 MQTT exclusion**, a one-line build-flag removal, though v1 is now out of the demo set anyway (see D-005).
  - **New (Session 4), SOS beacon priority.** `TrekLinkSOSHelper::broadcastPosition()` retransmits via `PositionModule::sendOurPosition()`, which sets `priority = BACKGROUND` for a handheld role (`PositionModule.cpp:377–380`), only the very first position packet at trigger time is `MAX`. Every beacon for the rest of an episode is the *lowest*-priority traffic on the mesh. Candidate fix: have the beacon path set `priority = MAX` (or at least `RELIABLE`) explicitly instead of delegating to the generic broadcast method. See `04-firmware-ground-truth.md` §2.
- **Action** (owner: team lead): none outstanding, both questions answered. Continue to log every firmware change in this register, and carry the firmware work in the same backlog and Progress Log as platform work so the contribution evidence is uniform.

### D-009: Git, tracking & review model v2 (supersedes D-003)
- **Status**: ✅ **Resolved** (2026-09-13, Session 5)
- **Context**: D-003 ratified the school's `Git_Lab_Guide.pdf` model wholesale. Auditing it against reality found it was never actually implemented and could not be: **no repository has ever had a `develop` branch**, yet `develop` appeared in 34 documentation files, making every documented git command broken. Three documents disagreed with each other on the branch model (`07-*.md` §3.2 and D-003 mandated dual Design/Implementation branches; `09-*.md` §1 said they were "not adopted"). The GitHub-Issues-as-tracker assumption conflicted with the team's actual use of Jira.
- **Options considered**:
  1. **Fix reality to match the docs**, create `develop`, adopt dual branches, drop Jira. Rejected: dual branches double PR overhead for a 5-person/13-week term, and the team already runs Jira.
  2. **Fix the docs to match reality, keeping GitLab's philosophy**, chosen.
  3. Leave the contradiction and rely on tribal knowledge. Rejected: agents read the docs literally and will follow the broken commands.
- **Decision**:
  - Integration branch is **`dev`**. Branches: `main`, `dev`, `feat/*`, `fix/*`, `hotfix/*`, `docs/*`, `chore/*`.
  - **`release/*` dropped**, `main` is the release.
  - **Dual Design/Implementation branches killed.** One branch per unit of work; spec commits land before implementation commits on the same branch, which preserves review independence at half the overhead.
  - Branch naming: `{type}/{JIRA-KEY}-{short-kebab-desc}`, e.g. `feat/TK-45-device-registration`. The Jira key is what makes the org-level Jira↔GitHub integration auto-populate each card's Development panel.
  - Commits: **Conventional Commits**, all standard types, Jira key as scope, `feat(TK-45): ...`. Scope omitted when genuinely general. **Not CI-enforced**: commit hygiene must never block a delivery.
  - Merge: **Rebase & merge** default, **Squash & merge** when multi-commit, **merge commits prohibited**. Delete source branch except `dev` → `main`.
  - **No direct pushes to any branch, by anyone, including the leader.**
  - **Jira is the single work tracker.** GitHub Issues hold daily reports and standalone bugs only. GitHub Milestones retired; `points:*` labels retired in favour of Jira story points on the **Fibonacci** scale (1/2/3/5/8/13/21), corrected 2026-09-17; an earlier revision published a non-standard base-5 scale that the backlog was never estimated against.
  - Bugs route three ways: Jira `BUG` **status** (defect found reviewing an active story) / GitHub Issue `type:bug` (standalone, never enters Jira) / Jira `Bug` **work item** (only if >0.5 day or it changes a spec).
  - CI is an **indicator, not a gate**, red CI does not block merge, but the leader must approve any red merge and the reason goes in the PR.
  - PR self-approval permitted **only** for <50-line, non-behavioural housekeeping. The PO is not exempt and must run an independent AI review pass on their own non-trivial PRs.
  - **English only** in every repository artifact. Vietnamese permitted when prompting an AI agent, and by exception in daily reports.
- **Consequence**: `01-conventions/` rewritten as Conventions v2; `07-*.md` fully rewritten; new chapters `10` (Jira), `11` (AI-first), `12` (communication). Two PR templates collapsed into one. `treklink-web/docs/conventions/` deleted (D-011). The generated Developer Handbook PDF is built from these files.
- **Owner**: Team lead.

### D-010: Neon as the shared managed Postgres
- **Status**: ✅ **Resolved** (2026-09-13)
- **Context**: `docker-compose.yml` provisions a local Postgres per developer, which is correct for isolated unit/integration work but gives the team no common database to co-develop against. Integration bugs that only appear with shared data (FK collisions, migration ordering, seed drift) surface late, typically during demo prep.
- **Decision**: Adopt **Neon** as the managed Postgres for shared **dev** and **prod/demo** environments. Local Docker Postgres remains the default for unit tests and CI (fast, hermetic, no network).
- **Consequence**: Each member installs the **Neon MCP connector** from the Claude skills store and authorises it under their own account. Connection strings live in each developer's `ignore/envs/` and are **never committed**. `DATABASE_URL` in CI continues to point at the ephemeral service container, not Neon.
- **Open**: branch-per-developer Neon databases vs. one shared dev database, decide before the first cross-module integration sprint.
  - **Update 2026-10-24**: provisioned. Shared development runs on the Neon branch `dev` of project `damp-queen-78476528`, Postgres only (D-062).
  - **Update 2026-10-04**: the Neon project has still never been provisioned, so no shared database holds applied migrations. The migration baseline is therefore rewritten in place for the rescope rather than migrated forward (D-036).
  - **Update 2026-09-29**: settled by `07-clarification-answers.md` §6 question 40, one shared dev database with migrations applied only from `dev`, by CI or the leader. The Neon project is **not provisioned yet**; until it is, every member develops against local Docker Postgres from `.env.example`. The leader distributes the team `.env` privately (Zalo), never through a repository.
- **Owner**: Team lead + LongLP (data lane).

### D-011: Single canonical convention set; vendored copies deleted
- **Status**: ✅ **Resolved** (2026-09-13)
- **Context**: `treklink-web/docs/conventions/` held a verbatim, unreconciled copy of the author's generic `dev-flow` template, 12 files with zero TrekLink-specific content, still teaching `develop`, bracket-tag commits, and the dual-branch model. `treklink-web/AGENTS.md` explicitly directed agents to **fall back to it**, so an agent opened on `treklink-web` alone would have been actively taught the wrong rules.
- **Decision**: **Delete it.** `treklink-docs/_docs/01-conventions/` is the single canonical convention set for all three repositories. No repo vendors a second copy. A single `AGENTS.md`, identical in content, is placed in `capstone/`, `treklink-docs/`, `treklink-web/`, and `treklink-firmware/`, and points at the canonical folder.
- **Rationale**: A duplicated convention set does not merely drift, it drifts *silently*, and the copy is what gets read when the sibling layout isn't present. The previous fallback was worse than having no fallback, because a wrong answer delivered confidently costs more than a missing one.
- **Consequence**: Agents must be opened on the `capstone/` parent folder. An agent opened on a single repo will find `AGENTS.md` pointing at a path it cannot resolve, and must say so rather than guessing, which is the intended failure mode.
- **Owner**: Team lead.

### D-012: Map provider: Goong Maps over MapLibre GL; OpenStreetMap tiles prohibited

- **Status**: ⛔ **Superseded by D-031** (2026-09-29). Resolved 2026-09-16, Session 6
- **Context**: `frontend/src/widgets/LiveMapWidget/LiveMapWidget.tsx:18-19` renders the standard
  OpenStreetMap tile server (`https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`). The team lead
  inspected every OSM base layer and confirmed each renders the Hoàng Sa and Trường Sa archipelagos
  under Chinese toponyms. Under Vietnamese law that makes the rendered product unlawful to publish.
- **Legal basis**: **Nghị định 174/2026/NĐ-CP, Điều 93 khoản 3 điểm a**, in force **1 July 2026**,
  fine **30–40 million VND** for *"Đăng, phát, sử dụng hình ảnh bản đồ Việt Nam không thể hiện đầy
  đủ hoặc thể hiện sai chủ quyền quốc gia."* It raises the 20–30M VND of Decree 15/2020/NĐ-CP Art.
  99(3)(b). Ancillary sanctions include confiscation of the equipment used, forced takedown of the
  content and its links, and **forced removal of the application**. Note the wording penalises
  *failing to represent fully* as well as *misrepresenting*, omission is sufficient; a nine-dash
  line is not required for liability. Enforcement against software and devices is established
  practice (imported-vehicle GPS confiscations, Hải Phòng 2019; 25M VND fine to the Oceanman 2023
  organiser under the predecessor article).
- **Options considered**:
  1. **Goong Maps via MapLibre GL**, chosen. Vietnamese provider (IMAP JSC), servers in VN and SG,
     free tier of $100 standing credit with 30,000 requests/month, 180 req/min and 1,000 map loads.
  2. **VietMap**, rejected on cost. Technically the closest fit (it publishes a documented
     `@vietmap/vietmap-gl-leaflet` wrapper that would have preserved the Leaflet API and a raster
     XYZ satellite endpoint), but it is not free.
  3. **Viettel Maps**, rejected on capability. Its public documentation exposes only a Static Map
     image endpoint, an `<iframe>` embed, Place and Routing. No XYZ tile layer and no GL style are
     documented, so it cannot back an interactive operations map.
  4. **Self-hosted sovereignty-corrected tiles**, rejected. Tile pipeline and storage cost far
     exceed a 13-week budget for no graded benefit.
- **Decision**: **Goong Maps rendered through MapLibre GL JS.** This replaces Leaflet as the map
  rendering library, Goong publishes GL styles, not an XYZ raster layer, so Leaflet is no longer
  the right host. Style URL form:
  `https://tiles.goong.io/assets/goong_map_web.json?api_key={MAP_KEY}`; variants
  `goong_map_web` (full icons), `goong_map_highlight` (minimal icons), `goong_satellite`.
  Integration is via the `maplibre-gl` CDN bundle, Goong documents no npm package of its own.
- **Two distinct credentials**: a **Map Key** authenticates style/tile URLs; a separate **API Key**
  authenticates Autocomplete, Direction, Geocoding, Distance Matrix and Place Detail. Do not
  conflate them.
- **Provider-agnostic by construction** (team lead, Session 6): the map layer must not hardcode
  Goong. Provider identity, style URL, key and default viewport are configuration, so a future
  swap to another GL-style provider is a config change and not a code change. See **D-015**.
- **Consequences**:
  - Leaflet is removed from the stack. Ten documents name it, `01-project-charter.md` (×2),
    `01-conventions/00-index.md`, `04-architecture-conventions.md`, `06-frontend-conventions.md`,
    `02-roadmap-and-milestones.md`, `AGENTS.md` (×4 copies), backlog story **US-055** via
    `build_backlog.py`, and `Documents/reports/Report1_Project_Introduction_DRAFT.md` §6.1, all must be
    updated in the same pass.
  - The API key is visible in the browser by design. Mitigate with an HTTP-referer allowlist and a
    per-IP rate limit on the key, and record that mitigation, it is the direct answer to the
    "API key exposed in source" failure mode in the faculty fault handbook §10.
  - **Acceptance test, mandatory before Review 1**: load the operations map over Hoàng Sa
    (~16.5°N, 112.0°E) and Trường Sa (~9.7°N, 114.0°E), confirm Vietnamese toponyms and correct
    sovereignty depiction, and file the screenshots as evidence. This is a team-performed check;
    it has **not** been carried out yet.
  - **Update 2026-09-25**: `07-clarification-answers.md` question 28 (Session 8, Confirmed) records
    that the team lead has performed the sovereignty check and found Goong compliant. Whether the
    screenshots are filed as evidence is not recorded (needs check).
  - **Update 2026-09-25, later**: the team lead confirms no screenshots are filed yet
    (`07-clarification-answers.md` §5 question 23). The acceptance test's evidence is outstanding.
  - **Update 2026-09-25, evidence filed**: the leader captured Goong Maps over Hoàng Sa and Trường Sa, both labelled in Vietnamese, and OpenStreetMap over the same area, labelled with foreign names and boundaries. Filed in `capstone/Documents/evidence/map-sovereignty/`. TC-24 passes for Goong; OpenStreetMap stays prohibited.
- **Owner**: Team lead (schema/UI layout lane) + LongNN (frontend lane).

### D-013: Execution model: SEP490 2026 mainflow-incremental, retaining SWP490 practice

- **Status**: ✅ **Resolved** (2026-09-16, Session 6)
- **Context**: `02-roadmap-and-milestones.md` was derived from `SWP490_Lo-trinh-Capstone_v1.0.pdf`.
  The Fall 2026 course issues `SEP490_Student_Project_Execution_Schedule.pdf` (50pp) and
  `SEP490_Huong_dan_nhanh_cho_sinh_vien.pdf`, which describe a materially different model: gates at
  W4/W8/W13 plus final submission at W15, four Common Meetings (W1, W3, W7, W12), a weekly Group
  Meeting, and **incremental delivery per Mainflow** rather than by TP package or Iteration.
- **Decision**: the **SEP490 schedule is the spine**. TP1–TP6 and the Iteration 1/2/3 framing are
  demoted to a historical appendix and mapped onto mainflow ownership; they no longer drive planning.
  Practices from SWP490 that the SEP490 documents do not contradict are **retained deliberately**
  because they are good practice, the phase discipline, the deliverable ledger shape, and the
  Week-6 scope lock (which SEP490 does not mention but which remains real).
- **The dual council is real but informal** (team lead, Session 6): "Hội đồng 1.1 / 1.2" is the
  *Hội đồng kín* naming, never published as an official document and conveyed only through the
  supervisor's outline. It maps cleanly onto the SEP490 calendar and is **not** a separate pair of
  events: **Hội đồng 1.1 = Faculty Council, W13** (Gate 3, defence eligibility);
  **Hội đồng 1.2 = Final Submission & Defense, W15**. Record it in internal planning; cite only the
  SEP490 names in graded documents.
- **Retake path**: failure at either council moves the group to a council in the following term,
  ~March 2027. This is why the registration form's stated duration reads 09/2026 – 03/2027 while
  the working plan ends in December 2026. **Plan for December.**
- **Known contradictions inside the SEP490 source**, resolved as follows and flagged wherever cited:
  - Review 1 at **W4** (Roadmap table, Master Schedule 5.2, quick guide) vs W3 (§4 prose item 2)
    → **W4** adopted, two sources to one.
  - "Two mainflows complete at W7" (§4, Master Schedule 5.1) vs "Sprint 1 (W8) → MF-01, MF-02"
    (Sprint Plan) → the **stricter W7** reading adopted; W8 is the confirmation demo.
- **Owner**: Team lead.

### D-014: Tracking artifacts: the SEP490 workbook and Progress Log

- **Status**: ✅ **Resolved** (2026-09-16, Session 6)
- **Context**: SEP490 §§27–37 name ten tracking artifacts and recommend consolidating them into one
  8-sheet workbook. `Documents/tracking/Report3_Project Tracking.xlsx` (WBS / Issues / Defects / Q&A) is the
  2021 artifact and covers a strict subset. The course also ships
  `templates/Mã nhóm_Progress_Log.xlsx`, named as **the** primary evidence for Individual
  Contribution, a dimension on which an individual member can fail even when the group passes.
- **Decision**: adopt both.
  1. **`GFA26SE55_Progress_Log.xlsx`**, one file for the whole term, from the course template.
     Updated **before every Group Meeting**. Per-member, per-week, tied to a named deliverable;
     "continued working on the project" is not an entry.
  2. **An 8-sheet tracking workbook**, `01_MASTER_SCHEDULE`, `02_WEEKLY_TASK_TRACKER`,
     `03_DELIVERABLE_TRACKER`, `04_TRACEABILITY_MATRIX`, `05_REVIEW_ACTION_TRACKER`,
     `06_RISK_ISSUE_CONFIG`, `07_FINAL_READINESS_CHECKLIST`, `08_INDIVIDUAL_CONTRIBUTION_LOG`.
  3. The **Mainflow Coverage Matrix** is the single sprint-tracking instrument the supervisor uses
     to confirm progress in the weekly Group Meeting. It is authoritative over any other view.
- **Risk register interface**: the Risk & Issue Log sheet adopts **the school's columns**
  (`ID · Risk/Issue · Impact · Probability · Mitigation/Action · Owner · Deadline · Status`) rather
  than a composite exposure score. The register below stays the engineering source of truth; the
  workbook sheet is its reporting projection and must be regenerated from it, never edited apart.
- **Consequence**: `Project Weekly Report_GroupName.xlsx` is retired. The old Project Tracking
  sheets fold into `02` and `06`.
- **Owner**: Team lead.

### D-015: Business parameters are configuration, never constants

- **Status**: ✅ **Resolved** (2026-09-16, Session 6)
- **Context**: the faculty fault handbook ranks hardcoded business parameters the **#2 cause of
  failure**, and its list of most-asked council questions opens with *"can this number be changed?
  Demo it for me now."* SEP490's W11 Definition of Done requires "tham số nghiệp vụ cấu hình được"
  and a maintained **Configuration Matrix**.
- **Values already hardcoded** (found by inspection, Session 6):
  `gateway/src/queue/priority-queue.ts:50` peek limit `10` · `gateway/src/mqtt/mqtt-client.ts:20`
  `reconnectPeriod: 3000` · `:41` flush batch `20` · `:49` topic prefix
  `treklink/events/priority/` · `frontend/src/widgets/LiveMapWidget/LiveMapWidget.tsx:6`
  `DEFAULT_CENTER`.
- **Values that must be born configurable** (not yet written): SOS beacon cadence (5 s for the first
  minute, then 30 s), episode-correlation window and backward grace, cadence-anomaly threshold
  (N positions in window W), P0–P3 tier mapping, gateway→cloud sync target (≤5 s), battery warning
  thresholds, rental rate, deposit, late fee, damage fee, and the map provider/style/viewport
  (D-012).
- **Decision**: no business parameter appears as a literal in source. Each is registered in the
  Configuration Matrix with parameter, current value, location, configurable (Y/N), tested, and a
  demo path. A parameter that cannot be changed and shown changing during a demo is treated as a
  defect, not as a style preference.
- **Owner**: Team lead (schema) + each module owner for their own parameters.

### D-016: The five Main Flows are supervisor-specified and binding

- **Status**: ✅ **Resolved** (2026-09-16, Session 6). ⛔ **Superseded by D-033 (2026-10-03)**: the five Main Flows are now the D-033 set. The flow identifiers and owners are kept; MF-01, MF-03, MF-04 and MF-05 change substance.
- **Context**: SEP490 organises all delivery from W3 to W12 around Mainflows, and the supervisor
  supplied the set for this project directly as `Documents/course-material/TrekLink-proposed-mainflow-ducndm.png`.
  They are not a format suggestion; they are the units the Mainflow Coverage Matrix tracks, the
  units demoed at each Iteration review, and the units the council evaluates.
- **Decision**: adopt exactly these five, with these identifiers.

  | MF | Name | Substance |
  |---|---|---|
  | **MF-01** | Booking → Rental → Trip Preparation | Customer browses package, submits booking, reserves device → Staff reviews, confirms, allocates device, assigns guide, generates rental agreement, checks out device → Guide receives device and prepares |
  | **MF-02** | Field Data → Offline Gateway → Cloud Sync | Device (SOS/GPS/telemetry) over LoRa mesh → Gateway Bridge with SQLite priority queue while offline → MQTT → NestJS; P0–P3 processing with idempotency; priority-ordered flush on reconnection |
  | **MF-03** | SOS → Incident → Emergency Response | SOS broadcast → gateway → idempotency check on `eventId` → Incident created if absent → FSM Detected → Acknowledged → In Progress → Resolved → Closed, each transition recording actor, timestamp and note → WebSocket notification to Staff and Guide |
  | **MF-04** | Real-Time Trip Monitoring | Device → gateway → MQTT → backend → WebSocket → dashboard showing active trips, device positions, battery status, incident alerts, last-seen time, for Admin / Staff / Guide |
  | **MF-05** | Return → Inspection → Billing → Maintenance | Check-in, return inspection, charge calculation, payment, rental close; device FSM Available → Reserved → Rented → In-Field → Returned → Maintenance → Retired |

- **Backlog mapping**: MF-01 ← E3 + E2 + E1 · MF-02 ← E4 · MF-03 ← E5 · MF-04 ← E5 (frontend) ·
  MF-05 ← E6 + E2. **E7 (DevOps) and E8 (Research & Evaluation) are cross-cutting and are
  deliberately not mainflows**, state this explicitly wherever the Coverage Matrix is presented,
  so the omission does not read as an oversight.
- **Consequences**:
  - MF-02 makes the offline buffer non-negotiable, see D-005.
  - MF-03 prints "idempotency check (using eventId)" on the supervisor's own diagram, which turns
    D-006's split key from an internal design note into a **demo obligation**: a replay must be
    shown producing exactly one Incident.
  - MF-05 and MF-01 together make the 7-state device lifecycle and the rental lifecycle
    demonstrable end-to-end, which is what the W13 council grades.
- **Owner**: Team lead.

### D-017: Diagram and figure conventions; Mermaid pinned at 12.0.0

- **Status**: ✅ **Resolved** (2026-09-17, Session 6)
- **Context**: the Main Flow diagrams were authored as `flowchart` blocks with `subgraph` groupings.
  That *looks* like a swimlane and is not, the groups do not constrain layout, so the actor
  partition is decorative. The course supplies actor-partitioned swimlanes as its worked example
  (`Documents/templates/Main flows_ex02.jpg`) and the supervisor's own TrekLink diagram uses that
  form. Separately, nothing in the pipeline checked whether a diagram was *legible once printed*:
  the handbook carried figures that render at 1.58 pt on A4.
- **Decision**:
  1. **Multi-actor process flows are Mermaid `swimlane-beta`**, one `subgraph` per actor lane,
     orientation `TB`. Plain `flowchart` is reserved for structures with no actors, context
     diagrams, feature trees, architecture diagrams.
  2. **Mermaid is pinned at 12.0.0.** `swimlane-beta` requires ≥ 11.16.0 and did not exist in the
     previous pin of 10.9.1. All 12 pre-existing diagrams were re-rendered at 12.0.0 and none
     regressed.
  3. **Figure placement is computed, not authored.** `plan_figure` in `build_handbook.py` renders
     each diagram headless, measures its viewBox and smallest rendered label, and chooses inline or
     a counter-clockwise rotated plate, whichever affords the larger scale. Both axes are always
     constrained, so nothing clips.
  4. **A 7 pt legibility floor**, with the escape hatch that a figure below it is a note rather than
     a build failure; the fix is to re-source the diagram, and any carried exception is recorded in
     `01-conventions/13-diagram-and-figure-conventions.md`.
  5. **Monochrome.** No figure may depend on hue, these documents are printed and photocopied.
  6. Every figure carries a number and a caption and is referenced before it appears. Numbering is
     per source document; the build renumbers continuously across the handbook and rewrites the
     in-text references.
- **Consequences**:
  - Diagrams are **pre-rendered to inline SVG** before pagination. Previously mermaid rendered in
    the browser during `--print-to-pdf`, which meant layout could not know a figure's size until
    after pagination had been decided, computed placement is impossible that way.
  - Rotation happens **inside the SVG coordinate system**, never as a CSS transform: a transformed
    box paints in one place and paginates in another, which prints content on the wrong page.
  - Three pre-existing figures were below the floor and were re-sourced by splitting: the session
    lifecycle sequence diagram, the Jira delivery loop, and the AI session workflow. The corpus is
    now **27 figures, all above the floor**, lowest 7.40 pt.
  - The CI "raw mermaid source" text check was removed. Its markers (`commit id:`, `[*] -->`,
    `-->|`) now all appear in the conventions prose that documents them, so they false-positive.
    CI validates figure numbering instead; an unrenderable diagram is already a hard build error.
- **Owner**: Team lead.

### D-018: Three-tier buffering topology; the on-device durable queue is inserted as Stage B

- **Status**: ✅ **Resolved** (2026-09-17, Session 7), **refines D-005, does not supersede it.** D-005's staged-rollout principle and its permanent-scope conclusion both stand.
- **Context**: D-005 described two stages, node MQTT with no buffer (A), then a basecamp bridge holding the SQLite queue (B). Session 7 inspection of `src/mqtt/MQTT.{h,cpp}` found that **the node already has a queue**, and that it is actively harmful: 16 entries, RAM-only, strict FIFO, **discard-oldest** on overflow (`MQTT.cpp:821–823`). Because eviction takes the oldest entry, the single `"SOS - …"` text frame that identifies an episode is **the first thing dropped** during an outage, the exact inverse of MF-02's binding priority rule. Full evidence: `04-firmware-ground-truth.md` §4.1.
- **Decision**, three tiers, delivered in this order:

  | Stage | Where | Buffer | Status |
  |---|---|---|---|
  | **A** | Guide's node publishes direct to MQTT over its own Wi-Fi | the stock 16-entry RAM FIFO, i.e. effectively none | **already exists, pure configuration, nothing to build** |
  | **B** | **On the device (firmware)**, RAM tier, then a flash tier | priority-ordered, reboot-proof, bounded, shed-aware | **built now; this term's focus** |
  | **C** | Basecamp gateway, node tethered to a laptop or phone | the large central queue, aggregating the whole local mesh | built after B; form settled by **D-020** |

- **Naming note, to stop a rename from creating drift**: what documents written before Session 7 call *"Stage B, the basecamp bridge with the SQLite queue"* is **now Stage C**. Stage B is the new on-device work. Every `[B]`-tagged requirement in `gateway-sync/requirements.md` predating this decision refers to Stage C and is retagged in the same pass.
- **Rationale**: Stage B is chosen ahead of Stage C on three independent grounds.
  1. **It fixes a defect rather than adding a layer.** Stage C buffers the gateway→cloud leg; it does nothing about a node that evicts its own SOS 80 seconds into an outage. Those are different failures and only Stage B addresses the second.
  2. **It needs no hardware the team does not already have.** Stage C needs a basecamp machine plus a tether; Stage B needs a node and a broker.
  3. **It is the strongest available answer to the council's individual-contribution question.** A cited before/after on inherited firmware is a materially better claim than new application code.
- **What Stage B does not do, stated so it is never overclaimed**: an on-device queue buffers only *that node's own* events. It cannot buffer for peer nodes that never reach Wi-Fi. Multi-node aggregation is Stage C's job and Stage B is not a substitute for it, the same relationship D-005 established between A and B.
- **Consequences**:
  - RQ1/RQ2 become answerable **this term, against a real baseline**, the unmodified firmware at its current commit (see D-019's preservation requirement, which is what makes the baseline reproducible).
  - The risk row *"Stage A has no offline buffer, so RQ1/RQ2 cannot be evaluated until Stage B lands"* is downgraded: Stage B lands first and is the smaller of the two.
  - `specs/gateway-sync/*` gains Stage-B requirements; `treklink-firmware/specs/onboard-queue/*` is created as the firmware-side spec suite, following the convention that specs live in `specs/{module}/` inside the repo that holds the code (`01-conventions/02-spec-driven-development-workflow.md` §2).
- **Owner**: KhoaDD (MF-02 owner).

### D-019: Firmware changes are additive and non-destructive; stock behaviour is preserved and must keep working

- **Status**: ✅ **Resolved** (2026-09-17, Session 7)
- **Context**: D-008 established that the firmware is editable. It did not say *how*. The queue work in D-018 touches `src/mqtt/MQTT.{h,cpp}`, stock Meshtastic files on the critical path of the app-pairing and MQTT-uplink features the product depends on. Overwriting them in place would destroy the measurement baseline RQ1/RQ2 need, and would risk the two integrations the demo cannot lose.
- **Decision**, three binding constraints on every firmware change this term:
  1. **Never delete or overwrite stock logic. Preserve it and branch around it.** The replaced stock path is kept intact and reachable, either behind a compile-time flag defaulting to the TrekLink path or extracted verbatim into a clearly-named function that the new code can call. A reviewer must be able to read what upstream did without consulting git history.
  2. **Stock Meshtastic mobile-app compatibility is a hard requirement.** The phone app pairs over BLE and, with `proxy_to_client_enabled`, carries the MQTT uplink itself (`MQTT.cpp:800`, `:607`). That path must keep working unmodified, it is how a guide with a phone and no laptop reaches the backend at all, and it is Stage C's mobile ingress.
  3. **The stock MQTT endpoint stays the publish target.** TrekLink does not invent a wire format here. Events still leave as `ServiceEnvelope` on `<root>/2/e/<channelId>/<nodeId>` and JSON on `<root>/2/json/...` (`MQTT.cpp:423–430`). The queue changes *which event leaves next and whether it survives a reboot*, never what it looks like on the wire. This keeps `gateway-sync`'s normalizer (D-007) unchanged and keeps the units legible to any stock Meshtastic tooling.
- **Rationale**: constraint 1 is what makes the D-018 baseline reproducible, "unmodified firmware" must be a build the team can still produce on demand, not a git tag nobody can flash. Constraints 2 and 3 protect the two integrations whose loss would cost the demo, for no benefit: nothing about a durable queue requires a new wire format or a forked app protocol.
- **Consequence**: a firmware PR that deletes stock code, changes a published topic shape, or breaks app pairing is rejected on this decision regardless of how well the queue works.
- **Owner**: KhoaDD.

### D-020: Basecamp gateway (Stage C) delivery form: browser-first, native desktop as fallback, no iOS

- **Status**: 🟡 **Decided in principle, build deferred** (2026-09-17, Session 7). Stage C is scheduled after Stage B; this records the form so Stage B's interfaces do not foreclose it. **Form superseded by D-033 (2026-10-03)**: Stage C ships as the Field Station, a single bundled executable on the renter's own laptop with a local browser UI.
- **Context**: Stage C needs a machine at basecamp with more storage than a node and an intermittent internet uplink. Three delivery forms were considered, against a guide who is not a technician.
- **Options considered**:
  1. **Purely web-based**, the guide opens a tab. The page reaches the node over **Web Serial** (tethered laptop) or **Web Bluetooth** (phone or laptop), holds the queue in browser-local storage (IndexedDB), and forwards upstream when the network returns. No install, cross-platform by construction, one artifact to maintain.
  2. **Native cross-platform desktop app** (Windows/Linux/macOS), or the `server.sh` / `server.bat` one-click equivalent over the existing `gateway/src`. Full serial access, no browser-permission friction, real filesystem storage. Three build targets and a signing/distribution problem.
  3. **A second Android app running alongside Meshtastic**, rejected. iOS is unviable without macOS/Xcode (already established in D-005), so this splits guide behaviour by platform, and it duplicates the pairing the stock app already does.
- **Decision**: **Option 1 is the target form**, with Option 2 retained as the documented fallback for any venue where browser device APIs are unavailable. Option 3 stays rejected, consistent with D-005.
- **Rationale**: Option 1's install cost is zero, which is the only property a non-technical guide actually experiences. `gateway/src` is not wasted under it, the queue policy, priority tiers and flush ordering are the substance and port directly; only the transport and storage adapters differ, which is the same ingress-adapter seam D-007 already defines.
- **⚠️ Known risks, accepted and carried** (see the risk table):
  - **Web Serial and Web Bluetooth are Chromium-only**, no Safari, no Firefox. On iOS this means *no browser at all* can reach the node, so an iPhone guide is served only by the stock Meshtastic app path (D-019 constraint 2), not by Stage C.
  - **A tab is a fragile host for a durable queue.** Backgrounded tabs get throttled, and a closed tab stops forwarding. IndexedDB survives the close, so nothing is lost, but delivery stalls until the tab is reopened. This must be surfaced in the UI and stated honestly at the council, not presented as an always-on service.
  - **WebRTC is not the mechanism.** It was raised as a candidate; it addresses peer-to-peer transport, not device access or storage, and is not required by Option 1. Recorded here so it is not reintroduced as an assumption.
- **Owner**: KhoaDD; revisit at Stage C kick-off.

### D-021: Encryption: provision a custom channel PSK; keep the MQTT hop plaintext behind TLS

- **Status**: ✅ **Resolved** (2026-09-17, Session 7)
- **Context**: "turn on end-to-end encryption" was raised as a requirement. Inspection shows the premise needs splitting, because two independent switches were being treated as one.
  - **LoRa channel PSK.** `Channels::initDefaultChannel()` (`Channels.cpp:128–134`) already sets `psk.bytes[0] = 1`, which `:238` documents as *"no change vs defaultPSK"*. So RF traffic **is** AES-encrypted out of the box, with **Meshtastic's published default key**. Any stock client in range decrypts it, SOS positions included. Encryption is present; confidentiality is not.
  - **`moduleConfig.mqtt.encryption_enabled`.** Controls only whether the packet handed to the broker stays encrypted. D-007 froze it `false` so the backend receives decoded payloads.
- **Decision**:
  1. **Provision a custom per-fleet PSK on the primary channel**, replacing the default key, as part of device provisioning in MF-01. This is the change that delivers actual confidentiality on the RF hop, and it is configuration, not code.
  2. **`encryption_enabled` stays `false`** (D-007 unchanged). The gateway→cloud hop is secured by **TLS plus a per-gateway API key** instead.
- **Rationale**: setting `encryption_enabled = true` would force reimplementing Meshtastic's AES-CTR channel crypto inside NestJS *and* would eliminate the JSON topic entirely (`MeshPacketSerializer` needs a decoded payload), taking out the whole Stage A ingress path, to protect a hop that TLS already protects. The real exposure was never the broker hop; it was the well-known RF key, which item 1 closes for the cost of a provisioning step.
- **Consequences**:
  - Device provisioning acquires a new mandatory step, and the PSK becomes a managed secret, never committed, never printed in a graded document, distributed per D-015 as configuration.
  - A custom PSK means a **stock Meshtastic app must be given the channel** to pair usefully. This does not violate D-019 constraint 2, the app path still works, it just needs the channel QR like any Meshtastic channel.
  - Losing the PSK bricks the fleet's interoperability until every unit is re-provisioned. Treat it as a recovery-critical secret with an escrowed copy.
- **Owner**: KhoaDD; provisioning step to be written into `specs/devices/`.

### D-022: `capstone` is a live auto-sync repository; the no-direct-push rule is scoped to the code repos

- **Status**: ✅ **Resolved** (2026-09-17, Session 7)
- **Context**: `capstone/` was already a local git repository with no remote, tracking `AGENTS.md`, `CLAUDE.md` and `Documents/`, the three sibling repos are gitignored. The team needs graded paperwork (progress log, reports, diagrams, meeting notes) to move between members continuously, edited from Obsidian. That is incompatible with `01-conventions/07-github-workflow-git-conventions.md` §3, which requires every change to arrive by PR and forbids direct pushes to any branch.
- **Options considered**:
  1. Fold `Documents/` into `treklink-docs`, one repo, but every progress-log edit becomes a PR, which defeats the purpose and would make the workbook a merge-conflict generator.
  2. `capstone` with the three siblings as submodules, rejected: detached HEADs and stale checkouts are a known failure mode for a team under deadline, and it solves nothing here.
  3. Give the existing `capstone` repo a remote and let it auto-sync.
- **Decision** (Option 3): `capstone` is published as a **private** repository and runs **auto-commit / auto-push to `main`**. The no-direct-push rule is explicitly **scoped to `treklink-docs`, `treklink-web` and `treklink-firmware`**, which keep full PR discipline.
- **Rationale**: PR review exists to gate code that can break a build or a contract. Meeting notes and a progress log cannot. Applying the same ceremony to both makes the ceremony get skipped for the thing that actually needs it. Separating them keeps the gate credible where it matters.
- **Scope limits, all three are load-bearing**:
  1. **`capstone` only.** A change to a sibling repo is still a PR, always.
  2. **`_docs/` stays read-only in the vault.** `treklink-docs` is a nested repository that `capstone/.gitignore` excludes, so Obsidian can read and link conventions while edits to them still go through a PR. This is a feature, not a limitation.
  3. **History stays linear.** `pull.rebase = true` is set in the repo config; merge commits remain prohibited everywhere (§3).
- **Consequences**: the repo is private, because `Documents/` holds supervisor meeting notes and course-issued PDFs. Auto-commit intervals must exceed a typical agent session, or in-progress edits get committed mid-work.
- **Owner**: KhoaDD.

### D-023: A Main Flow owner is not the assignee of every story in that flow

- **Status**: ✅ **Resolved** (2026-09-17, Session 7)
- **Context**: raised by LongLP, the charter (`01-project-charter.md:14`) and roadmap (`02-roadmap-and-milestones.md:164`, `:249`) name **LongNN** as the frontend/FSD, map-and-monitoring-UI member and **MF-04 owner**, while the generated backlog assigned every `module:monitoring` story to TanNB. Verified by inspection, and the report was correct on MF-04 and over-generalised beyond it.
- **What the audit actually found**:
  - LongNN held **zero** monitoring and **zero** frontend stories, his nine were devices ×4, trips ×3, auth ×1, billing ×1. He did not own `TK-63`, the MapLibre/Goong live map, despite being the designated map member.
  - Load was skewed: TanNB 28 stories across nine modules, LongNN 9.
  - Cross-tabulating all 75 MF-tagged stories showed 66 "mismatches" *if* one assumes the flow owner owns every story in it. **That assumption is wrong**, MF-01's stories are spread across all five members by design.
  - **MF-04 was the only flow whose named owner held none of its stories.** That is what made it a real defect rather than a naming artifact.
  - It was **not a generator bug**: `build_backlog.py` documented a deliberate Session-2 rearrangement that was never reflected back into the charter.
- **Decision**, two parts:
  1. **The roles are distinct and both are kept.** A **Main Flow owner** (D-016) is accountable for that flow reaching Demo Ready on the Mainflow Coverage Matrix. A **story owner** implements one story. A flow legitimately spans several implementers. Do not reassign a whole flow to its owner.
  2. **MF-04 is corrected by layer, not by flow.** UI stories → **LongNN** (`TK-63` live map, `TK-64` telemetry display, `TK-73` gateway connectivity indicator, exactly the "map and monitoring UI" the charter names). Backend infrastructure stays with **TanNB** (`TK-61` Socket.io gateway, `TK-46` monitoring read API). Session 2's reasoning for placing infrastructure there is unchanged.
- **Rationale**: this satisfies the charter's *skill* basis and the Session-2 risk weighting simultaneously, the frontend member gets the frontend work, the riskiest backend infrastructure stays where it was deliberately put. No charter or roadmap edit is needed, because the charter was already right.
- **Consequence, individual contribution**: the register already carries the risk that a member with thin visible contribution fails individually even when the group passes. LongNN listed as MF-04 owner while another member demos MF-04 is exactly the *"which part did you do?"* failure the faculty handbook describes. This correction is as much about defensible individual evidence as about tidy assignment. New balance: TanNB 25, LongLP 20, Khoa 18, HoangTK 13, LongNN 12.
- **Also corrected in the same pass**: `build_backlog.py` carried an assignment rationale naming a teammate as unreliable. That file is tracked and forms part of the graded documentation set. The rationale is rewritten in terms of layer and track record; person-level judgements belong in `ignore/`, not in a graded repository.
- **Follow-up**: Jira must be re-synced for `TK-63`, `TK-64`, `TK-73` before implementation starts.
- **Owner**: KhoaDD.

### D-024: Prose conventions are binding, and Jira keys are scoped to Epics and User Stories

- **Status**: ✅ **Resolved** (2026-09-22, Session 8). Two rulings recorded together because both were issued in the same instruction and both touch `01-conventions/07`.
- **Context**: two separate wording and tracking defects were raised by the leader.
  1. Every tracked document, and every AI chat reply, was using the em dash as a general-purpose clause separator. At volume it reads as machine-generated, it is inconsistent with the graded reports' register, and it hides the sentence boundary a reader under time pressure needs.
  2. `07-github-workflow-git-conventions.md` §2.2 said a branch without a Jira key was *"rare, prefer creating the card."* Followed literally, that mints a Jira card for every CI fix, tooling change and conventions edit, which pollutes the backlog, the Mainflow Coverage Matrix and the burndown. Those three are exactly what the supervisor reads at the weekly Group Meeting.
- **Decision**, two parts:
  1. **Prose conventions are binding**, published as [`01-conventions/14-prose-and-wording.md`](../01-conventions/14-prose-and-wording.md). No em dash in prose anywhere, no en dash as a clause separator, no banned openers, no aphorism formulas, no two-beat antithesis, no unverified claims, no fabricated precision. Code fences, inline code spans, "not applicable" table cells and verbatim quotations are exempt as data. Every AI assistant loads the `prose-and-wording` skill and `caveman` level `full` at session start, without being asked; chat is compressed, anything persisted to a repository stays normal prose. *(The `caveman` clause is superseded by D-043.)*
  2. **A Jira key belongs to an Epic or a User Story and to nothing else.** A branch and a commit scope carry a key only when the unit of work is one of those cards. Housekeeping, CI, automation, tooling, conventions and non-deliverable documentation carry no key and use a plain descriptive branch. Task and Subtask breakdown is tracked inside the parent story card, not as its own keyed branch. Do not create a card so that a branch can have a key.
- **Rationale**: part 1 is a register decision, and the register of a graded artifact is not cosmetic, because the Faculty Council reads the reports. Part 2 restores the backlog's meaning: a card should represent delivered product scope, so that the Coverage Matrix stays an honest instrument.
- **Consequences**:
  - `07-github-workflow-git-conventions.md` §2.2 and §3.1 are amended in the same pass.
  - `00-index.md` gains row 14.
  - The four canonical `AGENTS.md` copies gain §2.7 and a line in §6.
  - A **mechanical sweep ran on 2026-09-22** across `treklink-docs`, replacing 1230 em dashes in 54 files. It was verified by diff sampling, `git diff --check` for the trailing whitespace a blind join leaves behind, and the new checker, per chapter 14 §6.2. `treklink-web` and `treklink-firmware` are **not** swept; chapter 14 §6 corrects a file when it is next edited for another reason.
  - **`.github/scripts/check_prose.py` and `.github/workflows/prose-check.yml` are built and green.** They enforce the two regex-detectable rules, the em dash in prose and a banned opener at the start of a sentence, on every pull request and push to `dev` and `main`. The rest of chapter 14 stays review-enforced, because a checker that guesses at aphorism formulas or unverified claims produces false positives.
  - **Never swept, and skipped by the checker**: `topics/`, `ignore/`, and the two generated backlog files. Chapter 14 §6.1 carries the list.
- **Incident recorded in the same pass**: the first run of the sweep had an exclusion filter for `topics/` that silently failed. It reworded the **registered capstone project title**, in English and in Vietnamese, in both `topics/Phieu_FA26SE159.md` and `topics/Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.md`. Caught by sampling the diff, reverted with `git checkout` before any commit, net change zero. Those forms are the version the school holds and the title is frozen until the Week 6 scope lock. The rule that came out of it is `08-ai-agent-steering-and-discipline.md` Stage 2.7: print the file list a sweep will touch and confirm the exclusion held, do not assume the filter worked.
- **Two further standing rules were issued in the same instruction** and are recorded as `08-ai-agent-steering-and-discipline.md` Stages 2.6 and 2.7:
  - **Stage 2.6**: a standing instruction from the leader is written into the conventions in the same pass, routed by kind. An instruction that lives only in a chat transcript is lost at the next session boundary.
  - **Stage 2.7**: correct before polished. A document that is factually right, cites its evidence and contradicts nothing is done, even if its wording is plain. This does not license an unverified claim; Evidence Completeness still outranks Resource Efficiency.
- **Owner**: KhoaDD.

### D-025: `dev` reaches `main` by fast-forward push, and the handbook PDF is committed on the PR branch

- **Status**: ✅ **Resolved** (2026-09-25). Leader-approved.
- **Context**: `main` and `dev` diverged in `TrekLink-Team.github.io` and in this repository, although neither held content the other lacked. Three mechanisms caused it. (1) GitHub's "Rebase and merge" re-creates each commit with a new SHA, even when a fast-forward is possible, so after landing landing-site PR #12 `main` and `dev` each held 9 commits the other lacked, with byte-identical trees. (2) "Squash and merge" of a `dev` → `main` PR creates one new commit on `main`. (3) `.github/workflows/handbook.yml` tried to commit the rebuilt PDF to whichever of `dev` or `main` it ran on, so every push to `main` could add a bot commit that existed on `main` alone. Since branch protection was applied on 2026-09-22 that push has been rejected on both branches (the workflow token cannot bypass protection), so every handbook run on `dev` failed and the committed PDF stopped at `eb033a7`. In this repository `main` carried 6 such commits: resync copies of older `dev` states, a PDF rebuild, and the retired `mermaid-10.9.1.min.js` cache. Every file they changed has a newer version on `dev`.
- **Decision**:
  1. The `dev` → `main` release PR is opened and approved as before, then landed by the leader with `git push origin origin/dev:main` after `git merge-base --is-ancestor origin/main origin/dev` succeeds. Never with the merge button. `07-github-workflow-git-conventions.md` §5.7 carries the command.
  2. `handbook.yml` commits the rebuilt PDF to the head branch of a same-repository pull request, so the PDF reaches `dev` inside the reviewed PR and `main` through the release fast-forward. On pushes to `dev` and `main` it only validates. `_docs/handbook/README.md` describes the flow.
  3. Existing divergence is repaired once per repository. Where `dev` already contains all of `main`'s content, `main` is moved to `dev`'s tip. Where `main` holds content `dev` lacks, `dev`'s own commits are replayed onto `main` and `dev` is pointed at the result. Both need a temporary `allow_force_pushes` on the target branch, restored immediately after a push leased on the old SHA.
- **Rejected**: (c) commit the PDF on pushes to `dev` only. It fails for the same protection reason. (d) Give the workflow a token that bypasses protection. It reopens the direct-push path that protection exists to close. (a) keep releasing with "Rebase and merge" and realign after each release. It needs a force-push on a protected branch every time. (b) Allow merge commits for `dev` → `main` only. It breaks the linear-history rule in §5.7 for the one PR where traceability matters most.
- **Consequences**: a hotfix landed on `main` (§2.4) is the only way `main` gains a commit `dev` lacks, and §2.4 already requires syncing it into `dev`. Everyone with a local `dev` or `main` in a realigned repository runs `git reset --hard origin/<branch>`, announced in Zalo.
- **Owner**: KhoaDD.

### D-026: A failure response carries its error code in `result`

- **Status**: ✅ **Resolved** (2026-09-25). Leader-approved (treklink-web C-003 item 2).
- **Decision**: on failure the D-002 envelope keeps its four keys and sets `result` to `{ "errorCode": "..." }`, a stable machine-readable code such as `DEVICE_NOT_AVAILABLE`; `message` stays human text.
- **Rejected**: `result: null` with the code prefixed in `message` (parsing text is fragile); a fifth key (breaks D-002).
- **Consequence (2026-09-29, TK-90, `07-clarification-answers.md` §7 questions 1 and 7)**: from TK-90 on, the global exception filter sets `result.errorCode` on every failure. A `DomainException` carries its own code; a Nest `HttpException` maps by status to the catalogue code for 400, 401, 403, 404, 413 and 503, and any other 4xx keeps its status with the generic `CLIENT_ERROR`; an unhandled exception is a 500 with `INTERNAL_ERROR`, which is never used for a client error.
- **Owner**: KhoaDD.

### D-027: One-endpoint operation dispatch is limited to `gateway-sync`

- **Status**: ✅ **Resolved** (2026-09-25). Leader-approved (C-003 item 3).
- **Decision**: `gateway-sync` keeps its single `POST /api/gateway-sync` route with an `op` discriminator (Session 7). Every other module uses REST routes as in `05-backend-conventions.md` §5.
- **Rejected**: reverting `gateway-sync` to REST (its design already relies on the dispatch); extending dispatch to all modules (loses per-route policy and HTTP caching).
- **Owner**: KhoaDD.

### D-028: A cross-cutting `platform` module

- **Status**: ✅ **Resolved** (2026-09-25). Leader-approved (C-003 item 1).
- **Decision**: `backend/src/modules/platform/` and `specs/platform/` hold the response envelope, configuration, runtime parameters (UC-19), the audit sink and viewer (UC-20), the scheduler and health.
- **Rejected**: folding them into `auth`, which would make every module import `auth` for reasons unrelated to identity.
- **Owner**: KhoaDD.

### D-029: Backlog Jira keys follow the keys Jira issued, offset by five

- **Status**: ✅ **Resolved** (2026-09-25).
- **Context**: the first `jira_sync.py --apply` run found `TK-1` to `TK-5` already in the project. The epics were issued `TK-6` to `TK-13` and the stories `TK-14` to `TK-103`, five above every key the backlog had predicted.
- **Decision**: `build_backlog.py` sets `JIRA_EPIC_BASE = 6` and `JIRA_STORY_BASE = 14`, and the backlog is regenerated. Every `TK-nn` cited before this entry, for example `TK-63`, `TK-64` and `TK-73` in the MF-04 correction above, refers to the old prediction; add five to find the live card. `TK-45` in branch and commit examples is illustrative and unchanged.
- **Rejected**: deleting and recreating the cards to reach `TK-1`, because Jira never reuses an issue number.
- **Owner**: KhoaDD.

### D-030: The module specs govern the device, incident and rental state machines

- **Status**: ✅ **Resolved** (2026-09-26). **Superseded by D-034 and D-035 (2026-10-03)**: the booking, trip and rental machines it reconciled no longer exist after the D-033 rescope.
- **Context**: the Report 4 SDD draft (capstone PR 1) follows `treklink-web` specs and `schema.prisma`, which disagree with the SRS state machines drawn from `07-clarification-answers.md` §5. Incident: §5 question 6 reopens `Resolved` to `In Progress` and dismisses only from `Detected`; `specs/incidents/design.md` §2 reopens to `DETECTED` and dismisses from `DETECTED` or `ACKNOWLEDGED`. Rental: §5 question 27 has `Created`, `Active`, `Returned`, `Closed`, `Escalated`; `specs/rentals/design.md` has `DRAFT`, `READY`, `CHECKED_OUT`, `OVERDUE`, `RETURNED`, `CLOSED`, `CANCELLED`. Device: SRS Figure 22 failed the handover check from `Reserved`, while §6 question 12 already made `specs/devices/design.md` §2.1 authoritative (`RENTED` to `MAINTENANCE`). Trip: the same eight states under different names (§5 question 26 `On Prepare`, `On Booking`, `On Start`, `Ongoing`; the schema `PREPARING`, `BOOKING_OPEN`, `READY`, `IN_PROGRESS`).
- **Decision**: the specs and the schema govern the device, incident and rental machines. The SRS is amended to match (Record of Changes 2026-09-26): rental `Overdue` replaces `Escalated` and is entered at the return time plus the late-fee grace; a device still out after `rentals.nonReturnGraceDays` is flagged loss-suspected (§6 question 14). §5 questions 6 and 27 are superseded. Trip names stay as they are on both sides: the SRS keeps the display names of §5 question 26, and the SDD maps each to its stored value. Booking names are unchanged by this entry; §6 question 23 still governs them.
- **Rejected**: renaming the specs and the schema to the §5 answers, because the seven-state rental covers cancellation before check-out and the late state that merged code already uses, and it would need a forward migration of three enums. Renaming the trip enum, because a mapping costs no code.
- **Owner**: KhoaDD.

### D-031: The map reverts to Leaflet over OpenStreetMap, with a Vietnamese sovereignty overlay (supersedes D-012)

- **Status**: ✅ **Resolved** (2026-09-29).
- **Context**: D-012 moved the map to Goong Maps over MapLibre GL because every OpenStreetMap base layer labels Hoàng Sa and Trường Sa with foreign toponyms; the leader's screenshots in `capstone/Documents/evidence/map-sovereignty/` confirm it. The leader asked the supervisor, who accepts OpenStreetMap for this university project as an educational use.
- **Decision**: Leaflet renders OpenStreetMap raster tiles. Goong stays dormant: its configuration keys and the D-012 integration notes are kept, no code path calls Goong, and no Goong key is required. A small Leaflet overlay labels Hoàng Sa and Trường Sa in Vietnamese as Vietnamese territory, because Nghị định 174/2026/NĐ-CP Art. 93(3)(a) penalises failing to depict sovereignty fully as well as depicting it wrongly. Provider, tile URL, attribution and default viewport stay configuration (**D-015**), so a return to Goong is a configuration and renderer change.
- **Residual risk**: OpenStreetMap's own foreign labels still render beneath the overlay. The supervisor's acceptance covers the course; it does not change the decree. R11 is reopened as an accepted risk within educational scope: nothing built on OpenStreetMap tiles is deployed publicly beyond the course, and any such deployment first switches the provider back to Goong and re-runs TC-24.
- **OpenStreetMap tile usage policy** (<https://operations.osmfoundation.org/policies/tiles/>): attribution visible on the map, a named User-Agent and a valid Referer, no cache bypass, and no bulk prefetch. The last rule means OpenStreetMap tiles cannot be cached for offline field use by the Basecamp gateway (D-020).
- **Rejected**: keeping Goong as the renderer (leader decision); OpenStreetMap without the overlay, because it leaves the omission clause open for the cost of one layer; a viewport that excludes the archipelagos, because the user can still pan to them.
- **Consequences**: D-012 is superseded. The conventions, charter, roadmap, Main Flows, requirements foundation and the canonical `AGENTS.md` are updated in this pass. Queued: the graded reports and their generators in `capstone`, and the `treklink-web` specs (`frontend`, `monitoring`, `platform`) and code (`shared/config/map.ts`, `widgets/LiveMapWidget`, the `maplibre-gl` dependency), which go to the frontend lane as a spec change first. TC-24 now tests the overlay.
- **Owner**: KhoaDD; LongNN (frontend lane).

### D-032: The health endpoint reads MQTT state through an optional probe that `gateway-sync` registers

- **Status**: ✅ **Resolved** (2026-09-29). Leader-approved in [TrekLink-Team/treklink-web#15](https://github.com/TrekLink-Team/treklink-web/issues/15), recorded in `07-clarification-answers.md` §7 questions 2 and 9.
- **Context**: `specs/platform/api-design/01-get-health.md` reports MQTT broker reachability by calling `MqttIngressAdapter.isConnected()` (REQ-EVT-04, US-077). `specs/gateway-sync/design.md` §2.1 defines `MeshIngressAdapter` with only `path`, `start()` and `stop()`, and the adapter (gateway-sync task 5.1) is not built. `platform` depends on no other module (`treklink-web` `specs/platform/requirements.md:28`, "Depends on: nothing"; the module itself is D-028), so the health service cannot import `gateway-sync`.
- **Decision**: `platform` defines an optional `MqttHealthProbe` interface, `isConnected(): boolean`, and the injection token `MQTT_HEALTH_PROBE`. The health service injects it as optional. While no implementation is registered, `components.mqtt` is `unknown` and does not change `status`. A registered probe reporting a lost connection makes `status` `degraded`. `MqttJsonIngressAdapter` implements the probe and registers the token when `gateway-sync` builds it.
- **Rejected**: omitting `mqtt` from the response until `gateway-sync` Phase 5, because the response shape would change later and clients would code against both shapes; a broker connection owned by `platform`, because it duplicates the ingress connection and reports the reachability of a second client, not of the path events actually arrive on.
- **Consequences**: TK-90 amends `api-design/01-get-health.md` (the `mqtt` value set and the `status` rule), `specs/platform/requirements.md` REQ-EVT-04 and `specs/gateway-sync/design.md` §2.1.
- **Owner**: KhoaDD; LongLP (TK-90).

### D-033: TrekLink is an enterprise device-rental platform built on asset management (rescope after Review 1)

- **Status**: ✅ **Resolved by the leader** (2026-10-03). Supervisor sign-off of the adjusted registration form is pending (co-supervisor Bùi Văn Phúc, 2026-10-04; then Đặng Ngọc Minh Đức). Supersedes the booking scope of **D-016**, the Stage C form of **D-020** and the state machines of **D-030**. Rule 3 amended by **D-074** (generic device groups) and rule 8 by **D-073** (device first) on 2026-10-28.
- **Context**: at Review 1 (2026-10-01) the reviewers held that the registered title, "Smart Device Rental Management **Platform for Trekking Agencies**", contradicts the presented scope, which worked like one tour agency taking customer bookings. Report 3 SRS §1 called the product "a single-tenant operations system for one trekking agency". The registered form body (`treklink-docs/topics/Phieu_FA26SE159.md:111-153`, `:285`, `:305`) and the supervisor's flow image (`Documents/course-material/TrekLink-proposed-mainflow-ducndm.png`, MF-1 "Booking → Rental → Trip Preparation") both carry the booking flow, so the contradiction sits inside the registration, between its title and its body. Reviewer Lâm Hữu Khánh Phương asked for an IoT solution provider renting equipment with a management platform by package and monthly payment; the Review 1 minutes listed multi-tenancy as out of scope. At the 2026-10-02 meeting the supervisor ruled that the title cannot change, that the registration form may be adjusted one last time with changes highlighted, and that the product must be a platform, renting to a single company being a system (`capstone/Documents/meetings/2026-10-02_Rescope_Meeting_and_Review_Guidance_Summary.md`). The course defines a platform as one whose services come partly from the operator and partly from partners.
- **Decision**:
  1. **TrekLink is the sole provider** of the devices, the firmware, the Field Station software and the cloud platform, and it is the **asset manager** of every device. There are no third-party device providers.
  2. **Renters are corporate organizations only.** An organization self-registers, is verified in person or by phone at TrekLink, signs a master contract and is approved by a TrekLink Admin. Many organizations use one platform and each manages its own members, on-duty roster, rented devices, alerts and API keys: that is the platform. **The partners' part stays outside the system**: each organization's trips, customers and emergency response are its own business and are not modelled. Inside the system it has only what alert routing needs.
  3. **No individual renters, no bookings, no trips, no trek packages.** The website sells rental plans, nothing else.
  4. **Plans**, priced per device by hardware variant, with a minimum order quantity per contract that TrekLink sets:
     - **Monthly plan**: the term is one month and renews until the organization gives notice during a running term. Each term opens with a holding fee of half the term fee, which is part of the fee and not refundable, and closes with the other half. Mid-contract, a month boundary therefore carries a full term fee; the final term ends with only the second half.
     - **Day plan**: a fixed length from a configurable list (3, 4, 7 days); the per-day rate is the monthly rate divided by 30 times a premium of at least 1, so a day plan always costs more per day. Paid in full at handover. Never renewed or extended.
     - **No change once a contract is running**: no added or removed devices, no variant change. An organization that needs more opens an additional contract. A device never passes from one contract to the next without being returned and inspected.
     - **Charges outside the plan**: late return per device per day after a grace period; damage from inspection, with charges above a threshold approved by a TrekLink Admin; loss at the device's remaining value.
  5. **Handover and return happen in person at the TrekLink counter**, with identity, signature and payment checked there. No shipping.
  6. **Monitoring is always on** for every rented device; it is what the organization rents. Alerts go first to the organization's on-duty member, then its backup member, then its Manager; if nobody acknowledges, TrekLink logs it and reports to the authorities (**D-034**). TrekLink never coordinates a rescue.
  7. **Live telemetry reaches the organization** on the TrekLink web platform and through a REST plus WebSocket API with one key per organization, on every plan.
  8. **Field side**: device holders use the stock Meshtastic app only and need no TrekLink account. The organization runs the **Field Station**, a single bundled executable on its own laptop, with one of its rented nodes on a USB serial port and a local browser UI (for example `localhost:4321`). It shows everything locally while offline, queues events durably, and uploads when the laptop has internet. Organization operators are trained from the TrekLink manuals and handbook before deployment. The Field Station is Stage C of **D-018**.
  9. **Payments** are recorded in the platform. SePay (VietQR with a confirming webhook, sandbox environment) is the third-party payment gateway; cash and bank transfer at the counter are recorded by Staff.
  10. **The five Main Flows**, numbered so that each owner keeps their flow:

      | MF | Name | Owner |
      |---|---|---|
      | **MF-01** | Organization onboarding → Rental contract → Handover | TanNB |
      | **MF-02** | Field data → Field Station → Cloud synchronization | KhoaDD |
      | **MF-03** | SOS → Tiered alert → Escalation | HoangTK |
      | **MF-04** | Live telemetry: web map and organization API | LongNN |
      | **MF-05** | Term end → Return → Inspection → Billing → Maintenance | LongLP |

      Device intake and provisioning are supporting use cases that feed MF-01 and close MF-05's loop.
- **Rejected**: (a) keep the single-agency booking system and argue the title; the supervisor ruled the title fixed and the reviewers rejected the scope. (b) Third-party device providers listing fleets on the platform, the supervisor's reading of "platform"; it would reduce TrekLink's own hardware, firmware and gateway work to one listing among many and invite the reviewer's "what is unique here" objection. (c) Selling device packages with a maintenance fee; it drops "Rental Management" from a fixed title. (d) Individual renters; they force TrekLink to coordinate rescues and add a second payment model, and the title names trekking agencies. (e) Organization-created groups or trips inside the platform (create a group, add people and devices, pair them, export), raised by the supervisor at Review 1 (`ignore/khoa/docs/rescope/review-1-panel-transcript.md`); the leader ruled on 2026-10-04 that it contradicts the supervisor's own "device management platform, not a trekking management platform" in the same review. A device carries a holder label for alert routing; trips stay in the organization's own systems.
- **Consequences**: Report 1 background and vision, Report 2 scope, Report 3 SRS, Report 4 SDD, `05-main-flows.md`, `06-requirements-foundation.md`, the adjusted registration form (`treklink-docs/topics/`), the backlog, and the `treklink-web` specs and schema for `rentals`, `trips`, `billing`, `auth`, `incidents`, `monitoring` and `frontend`. Multi-tenancy moves from out of scope to in scope; Review 2 must say so against the Review 1 minutes.
- **Owner**: KhoaDD.

### D-034: Incident lifecycle with tiered notification and escalation

- **Status**: ✅ **Resolved by the leader** (2026-10-03; the leader delegated the design to the orchestrator with "multiple states, transient and atomic, a fallback for every edge case"). Replaces the five-state incident machine of the registration form and of `specs/incidents/design.md` §2.
- **States**:

  | State | Kind | Meaning |
  |---|---|---|
  | `DETECTED` | transient | Created from a confirmed SOS, a fall SOS or a suspected cadence episode; routed inside the same transaction, never observed at rest |
  | `NOTIFY_PRIMARY` | timed | The on-duty member is alerted |
  | `NOTIFY_BACKUP` | timed | The primary did not acknowledge in time; the backup member is alerted |
  | `NOTIFY_MANAGER` | timed | The backup did not acknowledge in time; the organization Manager is alerted |
  | `UNROUTED` | stable | No organization to route to (device not on a running or overdue contract, or the organization has no reachable member); TrekLink Staff own it |
  | `ESCALATED` | stable | Nobody acknowledged, or an acknowledged response went silent too long; TrekLink Staff own it |
  | `REPORTED` | stable | TrekLink Staff recorded a report to the authorities (agency, reference, time) |
  | `ACKNOWLEDGED` | timed | An organization member owns the response |
  | `RESPONDING` | timed | The organization reported a response under way; status updates are due on a cadence |
  | `RESOLVED` | timed | The organization reported the outcome |
  | `FALSE_ALARM` | timed | The organization, or Staff for an unrouted incident, declared it false with a reason |
  | `CLOSED` | terminal | Nothing further is accepted |

- **Transitions**:

  | From | Event | To |
  |---|---|---|
  | (none) | SOS, fall or suspected episode with no open incident for the device | `DETECTED` |
  | `DETECTED` | routed to a running or overdue contract with a reachable primary | `NOTIFY_PRIMARY` |
  | `DETECTED` | no contract, or no reachable member | `UNROUTED` |
  | `NOTIFY_PRIMARY` | acknowledge timeout; or no primary on the roster | `NOTIFY_BACKUP` |
  | `NOTIFY_BACKUP` | acknowledge timeout; or no backup | `NOTIFY_MANAGER` |
  | `NOTIFY_MANAGER` | acknowledge timeout | `ESCALATED` |
  | `NOTIFY_*`, `ESCALATED`, `REPORTED` | a member acknowledges | `ACKNOWLEDGED` |
  | `ACKNOWLEDGED` | the owner reports a response under way | `RESPONDING` |
  | `ACKNOWLEDGED`, `RESPONDING` | no status update within the stale limit | `ESCALATED` (owner kept, Manager notified) |
  | `ACKNOWLEDGED`, `RESPONDING` | the owner is deactivated or leaves the organization | `NOTIFY_BACKUP` |
  | `ACKNOWLEDGED`, `RESPONDING` | the owner reports the outcome | `RESOLVED` |
  | `NOTIFY_*`, `ACKNOWLEDGED`, `RESPONDING` | a member declares a false alarm with a reason | `FALSE_ALARM` |
  | `UNROUTED`, `ESCALATED` | Staff record an authority report | `REPORTED` |
  | `UNROUTED` | Staff declare a false alarm with a reason | `FALSE_ALARM` |
  | `REPORTED` | Staff record that the authority case is closed | `CLOSED` |
  | `RESOLVED`, `FALSE_ALARM` | a new SOS episode from the same device within the reopen window | `NOTIFY_PRIMARY` (reopen count + 1) |
  | `RESOLVED`, `FALSE_ALARM` | the reopen window elapses | `CLOSED` |

- **Rules**:
  1. **Atomic.** Each transition is one database transaction: a compare-and-set on the incident's state and version, plus one append-only audit row (actor or `SYSTEM`, from, to, reason, UTC time). A losing concurrent writer reads the current state and the actor who won.
  2. **Idempotent timers.** Timeout jobs re-read state and deadline inside the transaction and do nothing when the incident has moved on, so a retried or duplicated job cannot double-escalate.
  3. **Notification never gates state.** Alerts are written to an outbox in the same transaction and delivered after commit (web, WebSocket, email, API event); a failed delivery is retried and logged, and the state machine continues on its timers.
  4. **Safety first.** An incident is created and routed even when the contract is overdue or the organization is suspended. An episode is one incident (correlation window, `gateway-sync`); ~~a device's cancel gesture is recorded on the incident and prompts the owner to confirm a false alarm~~ (withdrawn by D-038: the device never changes an incident).
  5. **Device silent during an incident**: the incident keeps its state and is flagged stale with the last position; the owner is notified.
  6. **A contract cannot be settled while one of its devices has an incident that is not `CLOSED`.**
  7. Timeouts, the stale limit and the reopen window are business parameters (D-015).
- **Owner**: HoangTK; KhoaDD.

### D-035: Device, organization and rental-contract lifecycles

- **Status**: ✅ **Resolved by the leader** (2026-10-03). Replaces the seven-state device machine of the registration form and the booking, trip and rental machines of D-030. *The device lifecycle is amended by D-045 (loss from any in-service state, `DISPOSED`) and D-047 (a passed inspection of a unit due for service or firmware goes to `MAINTENANCE`; the weekly scan opens scheduled service).*
- **Device** (asset): `IN_INTAKE → AVAILABLE` (quality check passed) `→ RESERVED` (allocated to an approved contract) `→ RENTED` (handover signed) `→ RETURNED` (checked in) `→ AVAILABLE` (reset and inspection passed) or `MAINTENANCE` (inspection failed). Also `RESERVED → AVAILABLE` (contract cancelled before handover), `RESERVED → MAINTENANCE` (fails its check at the counter and is swapped, E01-5; edge added 2026-10-04 when the devices spec found it missing), `RENTED → LOST` (reported lost on a `RETURN_DUE`, `OVERDUE` or `DEFAULTED` contract, or unrecovered after default; amended by D-038), `LOST → RETURNED` (recovered), `LOST → RETIRED` (written off), `AVAILABLE → MAINTENANCE` (scheduled service), `MAINTENANCE → AVAILABLE` or `RETIRED`. `IN_FIELD` is dropped: telemetry gives last seen, not trail versus storage. Every device carries two identities registered at intake, a printed asset tag and the radio `nodeNum`, never reused. A returned device is reset (channel key, node database, owner name) before it can be `AVAILABLE` again, and the reset is logged.
- **Organization**: `PENDING` (self-registered) `→ ACTIVE` (verified at the counter, master contract signed, Admin approved) or `REJECTED`; `ACTIVE → SUSPENDED` (a contract defaulted, or Admin action) `→ ACTIVE` (settled); `ACTIVE → CLOSED` (no open contract). A `SUSPENDED` organization cannot open a contract; its running devices stay monitored.
- **Rental contract**: `REQUESTED` (the Manager submits plan, variant, quantity, start date) `→ APPROVED` (Staff confirm stock; devices `RESERVED`) or `REJECTED`; `APPROVED → ACTIVE` (first payment recorded and handover signed at the counter) or `CANCELLED` (before handover; devices released); `ACTIVE → ENDING` (monthly: notice given, ends at the current term end) `→ RETURN_DUE`; a day plan goes `ACTIVE → RETURN_DUE` at its end date; `RETURN_DUE → RETURNED` (every device checked in or recorded lost) `→ CLOSED` (every charge paid, no open incident); `RETURN_DUE → OVERDUE` (grace not yet elapsed, late fees accrue) `→ DEFAULTED` (grace elapsed: the organization is suspended, devices are tracked, Staff report to the authorities with the audit log as evidence) `→ RETURNED` once devices are recovered or recorded lost.
- **Monthly terms** are child records of a monthly contract: each term holds its holding-fee and balance payments and its due dates; a term's balance is due at its end, the next term's holding fee at the same boundary.
- **Owner**: TanNB (contract), LongLP (device, billing), KhoaDD (organization).

### D-036: Stale artefacts move to `.deprecated/`; the specs and the schema are rewritten from the SRS

- **Status**: ✅ **Resolved by the leader** (2026-10-04).
- **Context**: after D-033 to D-035 every `treklink-web` spec suite and `schema.prisma` describe the booking scope. The specs index marked them stale (treklink-web PR 26), but stale files left in place are what an agent or a member builds against by mistake, and deleting them loses the reference that the rewrite reuses (gateway-sync, platform). The Neon database was never provisioned (D-010), and only `platform` holds code.
- **Decision**:
  1. **A stale artefact moves, whole, into a `.deprecated/` folder at the root of its own repository, keeping its original path** (`treklink-web/specs/rentals/` becomes `treklink-web/.deprecated/specs/rentals/`). Nothing under `.deprecated/` is built, linked from a live document, or cited as a requirement. Each `.deprecated/README.md` states what moved, when, and why.
  2. **Every `treklink-web` spec suite is rewritten** from Report 3 SRS (2026-10-04) and D-033 to D-035, in the full form: `requirements.md` in EARS traced to SRS FR, UC and BR identifiers, `design.md`, `tasks.md`, and one `api-design/` file per endpoint. `trips` is not rewritten; `organizations` is new.
  3. **The state machines are D-034 (incident) and D-035 (device, organization, rental contract).** Where an old spec or the old schema disagrees, the decision wins.
  4. **The migration baseline is rewritten**, not migrated forward: a new initial migration and seed replace the 2026-09-25 pair, which move to `.deprecated/`. Every member drops and recreates the local database once.
- **Rejected**: deleting the stale suites (loses the reuse source; history is a poor reading surface); a forward migration with drops (protects data that does not exist).
- **Consequences**: unmerged branches built on the old schema (the booking-state rename, `feat/TK-22-admin-manage-user-account`) rebase onto the new baseline. Spec approval per module still goes through its owner's review before implementation (AGENTS.md §2.1).
- **Owner**: KhoaDD.

### D-037: Field Station credentials are self-service; one invoice per term; handover notes are signed on screen

- **Status**: ✅ **Resolved by the leader** (2026-10-04), during the spec rewrite of D-036.
- **Decision**:
  1. **Field Station credentials are self-service.** An Org Manager creates, names and revokes the organization's Field Station credentials in the portal, the way API keys work (UC-06); each credential is shown once and stored only as a hash. TrekLink Staff and Admin may revoke one for support but never see it. TrekLink provides the service; how the organization deploys its stations is its own business.
  2. **One invoice per monthly term with two dated lines**: the holding fee due at the term start and the balance due at the term end (FR-BILL-01, FR-BILL-06). Payments apply line by line.
  3. **The handover note is signed on screen** at the counter; the drawn signature is stamped into the generated PDF and the PDF's hash is stored (FR-CON-06).
- **Rejected**: Staff-issued Field Station credentials only (puts routine operations on TrekLink); two invoices per term (contradicts FR-BILL-06); a scanned paper signature (needs document storage and is weaker evidence of what was signed).
- **Owner**: KhoaDD.

### D-038: SePay webhook answers SePay's own body; no on-device SOS cancel; a device may be recorded lost from RETURN_DUE

- **Status**: ✅ **Resolved by the leader** (2026-10-04), during the spec rewrite of D-036. *Rule 3 is superseded by D-045: a loss may be reported from any in-service state.*
- **Decision**:
  1. **`POST /api/payments/sepay/webhook` is the one exception to D-002.** It answers HTTP 200 with the bare body `{"success": true}`, because SePay treats any other body as a failure and retries up to 7 times over 5 hours (https://docs.sepay.vn/tich-hop-webhooks.html, read 2026-10-04). Every other endpoint keeps the envelope.
  2. **An incident is never ended or changed by the device.** The firmware transmits nothing on cancel (`04-firmware-ground-truth.md` §2, `TrekLinkSOSHelper.cpp:49-53`), and even if it did, a cancel pressed on the device cannot be told apart from one pressed under duress. FR-INC-09 and exception E03-8 are withdrawn from the SRS; D-034 rule 4's sentence on the cancel gesture is withdrawn with them. A false alarm is declared only by a person (FR-INC-08).
  3. **D-035 amended**: Staff may record a device `LOST` on a contract in `RETURN_DUE`, `OVERDUE` or `DEFAULTED` when the organization reports the loss or the device is unrecovered after default. The loss is charged at the device's remaining value (FR-BILL-05) and counts as returned for closing the contract.
- **Rule 2 confirmed** (2026-10-29, leader ruling on treklink-web PR 114): a person ends every incident, the organization's staff, TrekLink Staff or the primary responder, never a device packet. An SOS that arrives after the reopen window of a `RESOLVED` or `FALSE_ALARM` episode closes that episode as `SYSTEM` under the normal window guard, the same close the timer of incidents task 3.1 makes, and opens a new incident. Inside the window, an SOS, attributed or not, reopens the episode, routed as at creation. REQ-UBI-05 and REQ-EVT-10 stand unchanged.
- **Rejected**: the envelope on the webhook (relies on undocumented SePay behaviour); a firmware cancel text that only logs (no consumer, and it still invites trusting the device over a person); inferring cancel from beacons stopping (indistinguishable from a dead battery); keeping `LOST` after default only (an honest report would suspend the organization and trigger an authority report).
- **Owner**: KhoaDD.

### D-039: Where the platform runs, and how software on the organization's side is updated

- **Status**: ✅ **Resolved by the leader** (2026-10-13): (a) option 1, (b) option 2. Raised 2026-10-11.
- **Context**: D-033 rule 1 makes TrekLink the sole provider of the devices, the firmware, the Field Station software and the cloud platform; rule 2 has many organizations on one platform; rule 8 puts the Field Station on the organization's own laptop. D-010 hosts the database on Neon. Nothing records whether the backend could also run on an organization's own infrastructure (the self-hosted GitLab model), and nothing records how the Field Station, which runs at the customer end, receives new versions. That answer decides whether TrekLink has to ship over-the-air updates to customer infrastructure at all.
- **Options**, two independent parts (split 2026-10-13 after review of PR 60):
  - **(a) Where the backend runs**
    1. **One TrekLink-hosted, multi-organization backend; organizations integrate only through the web platform and their API key.** The only TrekLink software on the organization's side is the Field Station.
    2. **Self-hosted backend option**: an organization may run the TrekLink backend on its own infrastructure, with TrekLink shipping versioned backend releases and updates to it, alongside the Field Station.
    3. **Hybrid**: hosted by default, with a self-hosted tier for organizations that require data residency.
  - **(b) How the Field Station receives new versions**, needed under every option of (a), because the Field Station always runs on the organization's laptop (D-033 rule 8)
    1. **Self-update**: the Field Station checks a TrekLink release endpoint and installs a new version itself.
    2. **Re-download**: the organization downloads the new version from the portal and replaces the executable by hand.
  - **Device firmware**, the same under every option: updated at the counter during intake, reset or inspection, because every device passes through the counter between contracts (D-033 rules 4 and 5).
- **Recommendation (not a decision)**: (a) option 1. No recommendation yet for (b). Tier 3 of D-034 escalates unacknowledged alerts to TrekLink Staff, which needs every organization's incidents in TrekLink's own backend; the platform definition the supervisor accepted (many organizations on one platform) is a single deployment; options 2 and 3 add release management, version skew between installations and remote support of customer infrastructure inside a capstone schedule. Option 1 keeps the update problem to one artefact, the Field Station executable.
- **Decision**:
  - **(a)** The leader preferred the hybrid model (hosted by default, fully self-hostable, as GitLab offers) on condition that it fits the four implementation weeks (W9 to W12), and option 1 otherwise. It does not fit, so **(a) is option 1: one TrekLink-hosted backend for every organization.** Evidence: on 2026-10-13 the backend holds 17 TypeScript files with only the health and Prisma services written (`treklink-web/backend/src`). Hybrid would add, on top of option 1: two deployment profiles of one codebase, because assets, contracts and billing are TrekLink's own records and cannot move to a customer server; a synchronization channel between installations for contracts and devices one way and D-034 tier-3 escalations the other; D-040 attribution across installations; and every flow tested under both profiles.
  - **(b) Option 2, re-download.** The portal offers the current Field Station release with its version; the Field Station reports its version in every health message, and an older version is shown as outdated to the Manager and TrekLink Staff (SRS FR-EVT-13, FR-EVT-18, constraint 6).
- **Rejected**: (a) 2 and 3, for the scope above; hybrid is recorded as future work, not a capstone deliverable. (b) 1, self-update, which adds a release endpoint, signed binaries and a rollback path to design and test in W7 and W8.
- **Consequences**: SRS constraint 6, FR-EVT-13 and FR-EVT-18, out of scope widened, all 2026-10-13. The Report 4 SDD deployment view shows one cloud deployment plus a Field Station per organization. `treklink-web` specs gain the release download and the version in the health report.
- **Owner**: KhoaDD.

### D-040: A field event belongs to the custody interval that contains its occurrence time

- **Status**: ✅ **Resolved by the leader** (2026-10-13). SRS edited 2026-10-13: FR-EVT-15 to FR-EVT-17, BR-36, E02-7, E02-8, FR-EVT-14, FR-INC-03, FR-MON-02, FR-MON-06 and FR-MON-08, ERD attributes. Adjusted form edited 2026-10-13: §3.2 b states time-based attribution. `treklink-web` edited 2026-10-13: `gateway-sync`, `incidents`, `monitoring`, `rentals` (`custodyAt` replaces `contractHolding`) and the Configuration Matrix (late-upload grace, attribution margin, device-time skew); `schema.prisma` gains `FieldEvent.capturedAt`, `occurredAt`, `timeSource`, `attribution` and `contractDeviceId`, with migration `20261013120000_field_event_attribution`.
- **Context**: co-supervisor Bùi Văn Phúc, reviewing the adjusted form and the SRS (Discord, 2026-10-12): organization A rents a device on 10/10 and raises an SOS at 16:00 while its Field Station is offline; the device is returned on 11/10 and rented to B; on 12/10 A's old SOS syncs. Routing by the device's current holder would send A's data to B. He asks for an assignment history over time linking Device, contract, Organization and FieldEvent, and for a rule when the device clock is unreliable or the timestamp is missing. Verified: the history exists (`ContractDevice.handedOverAt`, `checkedInAt`, `lostAt`), but FR-INC-03 routes to "the contract holding the device" at creation and FR-MON-02 and FR-MON-06 scope by what the organization rents now, so his scenario leaks. FR-EVT-14 accepts a Field Station's publishes only for devices its organization rents now, so after the return A's late SOS is refused and lost. The device `rx_time` is 0 without a valid RTC (`04-firmware-ground-truth.md`). Every device is reset and re-keyed at the counter between contracts (D-033 rule 5), so a late event for a returned device can only come from the previous renter's Field Station queue.
- **Decision**:
  1. **Occurrence time** is derived per event with its source recorded: the Field Station's capture time, corrected by the clock offset the station reports at each sync; the device `rx_time` only when non-zero and plausible; the server `receivedAt` always, as the upper bound.
  2. **Attribution**: the event belongs to the `ContractDevice` custody interval (handover to check-in or loss) that contains its occurrence time, and the uploading Field Station's organization must match that interval's organization. Incidents route, and telemetry streams, by the attributed contract and organization, never by the current holder.
  3. **No match**, or an occurrence time too close to a handover boundary to decide: the event is `UNATTRIBUTED` and goes to TrekLink Staff only.
  4. **Late uploads** from a Field Station are accepted for a configurable grace period after the device's return (D-015).
- **Rejected**: (b) attribution by the uploading credential alone, which checks no clock and cannot tell two contracts of one organization apart; (c) rejecting events older than the current custody, which drops SOS messages; (d) attribution by channel-key version, kept as a later hardening because whether the key version reaches the cloud is unverified (needs check against the firmware).
- **Consequences**: SRS: occurrence-time and attribution requirements, FR-INC-03, FR-MON-02, FR-MON-06 and FR-EVT-14 rewritten, exception E02-7 (the supervisor's scenario), a business rule for `UNATTRIBUTED`, ERD attributes. Form §3.2 b: one sentence. Schema: `FieldEvent` gains a capture time, a time source and an attribution state. Evaluation: the scenario becomes an isolation test (D-042).
- **Owner**: KhoaDD.

### D-041: The device lifecycle is a state graph; the form lists states and transitions

- **Status**: ✅ **Resolved by the leader** (2026-10-13). Adjusted form edited 2026-10-13: the asset management item and the functional requirement list the eight states and the main transitions. *The state list grows to nine with `DISPOSED`, and `LOST` is reachable from every in-service state (D-045).*
- **Context**: Bùi Văn Phúc (2026-10-12) read the form's "In Intake → Available → Reserved → Rented → Returned → Maintenance → Lost → Retired" as one sequential path, and noted that a returned device that passes inspection goes back to Available and that a rented device can be lost. The SRS state machine (Figure 22) already has those transitions; the arrow chain in the adjusted form (§3.2 b and the products list) causes the misreading.
- **Decision**: keep the eight states and transitions of D-035 and the SRS. The form lists the states and names the main transitions instead of chaining them. The whiteboard names of 2026-10-11 (`08-whiteboard-target-flows.md` §1) are mapped in the SDD: Registered is In Intake, Liquidate is the disposal step after Retired.
- **Rejected**: adopting the whiteboard states in the SRS one week before Review 2 (requirements, ERD enum, specs and schema all change); replacing the arrows with commas only (the transitions stay unstated).
- **Owner**: KhoaDD.

### D-042: Multi-organization isolation and load are evaluated by a separate test suite

- **Status**: ✅ **Resolved by the leader** (2026-10-13). SRS edited 2026-10-13: NFR-SEC-04 names at least two organizations per module and the late-event test, NFR-PERF-02 and NFR-PERF-03 name a simulated load test. Adjusted form edited 2026-10-13: TP6, Experiment 2 (two organizations at once, at least 4 participants, cross-organization leakage measured) and Integration & System Testing (isolation suite and simulated load test).
- **Context**: Bùi Văn Phúc (2026-10-12): the RQ3 drill uses one organization, which fits the incident workflow but does not test the many-organization requirement. He asks for integration and security tests with at least two tenants and a load test matching the multi-organization, multi-device NFRs. NFR-SEC-04 asks for a cross-organization test per module without a tenant count; NFR-PERF-02 and NFR-PERF-03 have no planned test.
- **Decision**:
  1. An isolation test suite with **at least two tenants** for every module, including the late-event scenario of D-040.
  2. A **load test** with simulated devices and Field Stations at the NFR-PERF-02 and NFR-PERF-03 levels, stated as simulated because only 3 to 5 physical devices exist.
  3. The **RQ3 drill runs with two organizations** at once.
  RQ1 to RQ3 stay unchanged in substance.
- **Rejected**: a new RQ4 (breaks the stated stability of the research questions); rewording NFR-SEC-04 only (no load test).
- **Owner**: KhoaDD.

### D-043: Chat register follows `communication-tone`; the `caveman` skill is retired

- **Status**: ✅ **Resolved by the leader** (2026-10-13). Supersedes the `caveman` clause of D-024 part 1; the rest of D-024 stands.
- **Context**: D-024 made every AI assistant load `caveman` level `full` at session start to compress chat replies. The leader's prompt-orchestrator has since made `communication-tone` the single communication rule (`system-prompts/prompt-orchestrator/skills/communication-tone.md`, commit `a587916`, 2026-10-08). Its writing register forbids the compression `caveman` produces: "Do not invent abbreviations or arrows to save tokens" (§8). The skill is uninstalled on the leader's machine, so the conventions told every agent to load a skill that does not exist and contradicts the governing rule.
- **Decision**: every AI assistant loads `prose-and-wording`, `communication-tone` and `human` at session start, without being asked.
  1. `prose-and-wording` governs what any written text may contain (chapter 14).
  2. `communication-tone` governs chat replies: the four-part status (asked, done, state, next), settle scope then execute in one pass, and a plain technical register.
  3. `human` is the pass every submitted document goes through (chapter 15 §4).
  `caveman` is not loaded, and no chat reply is written in a compressed register.
- **Rejected**: keeping `caveman` for chat only (conflicts with `communication-tone` §8, which wins over any other file); dropping a named chat rule altogether (the four-part status would then be unenforced).
- **Consequences**: chapter 14 §5, the 00-index row 14 and §2.7 and §6 of the five canonical `AGENTS.md` copies are amended in the same pass.
- **Owner**: KhoaDD.

### D-044: Report 4 SDD is generated from the specs; SRS lifecycles are authoritative

- **Status**: ✅ **Resolved by the leader** (2026-10-13).
- **Context**: `Documents/reports/Report4_SDD_DRAFT.md` predates the rescope (D-033): its detailed design covers booking, trips and customer billing, and its 20 diagrams under `sdd-diagrams/` were copied by hand from specs that have since been rewritten (D-036). The whiteboard flows of 2026-10-11 (`08-whiteboard-target-flows.md`) name some states differently from the SRS. Chapter 15 §2 requires numbered sequence diagrams across page, controller, service and repository, labelled state machines inside the design section, an architecture diagram that matches the repository and a physical schema.
- **Decision**:
  1. **Lifecycles**: the SDD state machines are the SRS ones (D-034, D-035, SRS Figures 22 to 24). The whiteboard names are mapped in a table: Registered is In Intake, Liquidate is the disposal step after Retired. This extends D-041 to every lifecycle.
  2. **Build**: a generator, `capstone/scripts/srs/build_sdd.py`, on the SRS pipeline (figure sizing, captions, table styling). Diagrams are read from `treklink-web/specs/*/design.md` and `schema.prisma`, never copied, so the SDD cannot drift from the specs. The old draft and `sdd-diagrams/` move to `.deprecated/` (D-036).
  3. **Depth**: per Main Flow, the class diagrams of the modules it touches, the state machine where the flow owns one, and three to five sequence diagrams for the key use cases that cross page, controller, service and repository. Each new diagram is written into the owning module's `design.md` first, marked `<!-- sdd: ... -->`, so the specs stay the source.
  4. **Layering**: every module gains a `*.repository.ts`, the only class that touches Prisma; the call order is controller, service, repository (`04-architecture-conventions.md` §1).
- **Rejected**: merging the whiteboard extras into the SRS a week before Review 2; a hand-written SDD (diagrams drift from the specs, captions and sizing by hand); one sequence diagram per swimlane step (40 or more diagrams, several sessions); one per Main Flow (too thin to code from).
- **Consequences** (2026-10-13, counts as of 2026-10-14 after D-045 and D-046): sequence diagrams for 29 use cases in 38 figures (UC-27 existed; long ones split for legibility) and 9 class diagrams in the `treklink-web` module designs; the platform design gains the third-party services and a deployment view; `capstone/scripts/srs/build_sdd.py` builds `Report4_SDD_DRAFT.md` and `Report4_SDD_TrekLink.docx`, 66 figures and 62 tables; 25 figures carried below 7 pt are recorded in `13-diagram-and-figure-conventions.md`. (needs check) No Report 4 template exists in `capstone/Documents/templates/`; the SDD is built on the Report 3 template with its cover title replaced until FLM's Report 4 template is found.
- **Owner**: KhoaDD (with HoangTK, reviewer LongLP, per the roadmap).

### D-045: Device asset management: a lost device opens a loss case from any in-service state; replacement and disposal

- **Status**: ✅ **Resolved by the leader** (2026-10-14). *Design corrected 2026-10-18: `devices` reaches custody and loss charges through the ports `CUSTODY_RESOLVER` (provided by `rentals`) and `LOSS_CASE_LISTENERS` (provided by `billing` and `rentals`), because both modules import `devices` and direct calls would form import cycles (`platform` design §2.1).* Amends D-035, D-038 rule 3 and D-041. Applied 2026-10-14: SRS (UC-49 rewritten, UC-60 to UC-62, FR-DEV-12 to FR-DEV-16, FR-CON-15, FR-BILL-05 and FR-BILL-11, BR-25 and BR-37 to BR-42, E05-3 and E05-8 to E05-10, Figures 23 and 24, ERD), adjusted form, `devices`, `rentals`, `billing`, `organizations` specs and API catalog, `schema.prisma` with migration `20261014090000_asset_loss_and_compliance`, Report 4.
- **Context**: the leader compared the device lifecycle with an enterprise asset management practice (FSOFT Guideline_Physical Asset Management v1.6 and the Regulation on compensation for damaged or lost company assets, summarised in the leader's `ignore/khoa/docs/FSOFT_Asset_Management_Flows.md`). Verified gaps in the current design:
  1. A renter cannot report a loss during a running contract: `LOST` is reachable only from `RENTED` on a `RETURN_DUE`, `OVERDUE` or `DEFAULTED` contract (D-035 as amended by D-038; SRS UC-49 precondition; SRS Figure 22).
  2. A loss in TrekLink's own custody, a theft from the depot or a unit missing at stock-take, has no transition; UC-54 lists unconfirmed units and stops (FR-DEV-10).
  3. A loss is one state change with an immediate charge (UC-49, FR-BILL-05, BR-25): no case record, search window, police reference, waiver or recovery path.
  4. A lost renter device still holds the organization's channel key (D-021), and devices keep the key version they were given until the next handover (`organizations` design §1), so whoever finds the device can read that organization's mesh.
  5. The charge does not depend on custody: BR-25 charges the renter even for a loss in TrekLink's custody.
  6. There is no disposal after `RETIRED`; the whiteboard of 2026-10-11 shows "Liquidate".
  7. A faulty or lost unit cannot be replaced during a running contract; the only swap is at handover (E01-5).
- **Decision**:
  1. **Device lifecycle as a composite.** `IN_INTAKE`, `AVAILABLE`, `RESERVED`, `RENTED`, `RETURNED` and `MAINTENANCE` form the superstate **In service**. From any of them a reported loss moves the device to `LOST` and opens a loss case. `LOST` goes to `RETURNED` when the device is recovered at the counter, never straight back into use, because a device out of custody may have been altered and holds a channel key; it is reset and inspected like any return (BR-28). `LOST` goes to `RETIRED` when the loss is confirmed. A new terminal state **`DISPOSED`** follows `RETIRED` once the device is verified wiped (key, node database, owner name), matching the whiteboard's "Liquidate". Device states: nine.
  2. **Loss case**, an entity of the `devices` module, separate from the SOS incident of D-034, whose tiers and timers serve safety alerts. States: `REPORTED` (by the Org Manager for a rented device, or by Staff for any device, including a unit missing at stock-take) to `SEARCHING` (Staff triage: custody decided, last seen time and position recorded from telemetry, key exposure flagged) to `RECOVERED` (device back at the counter) or `CONFIRMED` (Staff confirm, or the search window `devices.lossSearchDays` elapses) to `SETTLED` (charge applied, reduced, waived or written off; device `RETIRED`).
  3. **Liability by custody.** The custody interval of D-040 that contains the time the device was last seen decides who bears the loss: renter custody charges the device's remaining value to that contract on confirmation (amends BR-25); TrekLink custody is an internal write-off with no charge.
  4. **Waiver**: an Admin other than the Staff member who triaged the case may reduce or waive the charge, with a reason, as for damage charges (BR-24).
  5. **Key exposure**: a loss in renter custody marks the organization's channel key as exposed and notifies the Manager; the key is rotated and the organization's devices re-provisioned at their next counter visit. The platform cannot revoke a key on a device it cannot reach, and the documents say so.
  6. **Police reference**: optional on every loss case; required when the case is flagged as suspected theft or fraud (D-046).
  7. **Mid-contract replacement**: at the counter Staff replace a faulty unit, or a unit with an open loss case, on an `ACTIVE` or `ENDING` contract with an `AVAILABLE` unit of the same variant. The quantity, plan and variant stay unchanged (BR-05 holds); the replacement gets its own `ContractDevice` row, so its own custody interval; it is provisioned and the replacement is signed on screen like a handover. The faulty unit is checked in and inspected (damage charge rules apply).
- **Rejected**: widening `RENTED` to `LOST` only (leaves gaps 2 to 7); asset loss as a type of the SOS incident (D-034 routes to on-duty members with tier timeouts, which an asset case does not need); recovering a lost device straight into use (key and tamper risk); charging every loss to the renter (contradicts custody).
- **Consequences**: SRS device state machine redrawn as a composite with `DISPOSED`; a loss-case state machine; UC-49 rewritten as Report Lost Device, new use cases for resolving a loss case, replacing a device and disposing of a device; FR-DEV, FR-CON and FR-BILL requirements, BR-25 amended and new business rules; exception scenarios for a mid-term loss, a unit missing at stock-take and a recovery after settlement; ERD gains `LOSS_CASE`. Adjusted form: the lifecycle sentence. Specs and schema: `LossCase`, `DeviceStatus.DISPOSED`, replacement in `rentals`, charge by custody and waiver in `billing`, `channelKeyExposedAt` in `organizations`. Report 4: the new state machines and sequences.
- **Owner**: KhoaDD (device and billing lane: LongLP).

### D-046: Contractual compliance: NDA and software licence in the master contract; a compliance case for fraud, theft and IP or NDA breaches

- **Status**: ✅ **Resolved by the leader** (2026-10-14). Applied 2026-10-14: SRS (UC-63, FR-ORG-02, FR-ORG-08, FR-ORG-09, BR-40, BR-43, E05-11, ERD), adjusted form, `organizations` spec and API catalog (verification terms, compliance cases, key rotation), `schema.prisma`, Report 4.
- **Context**: TrekLink installs proprietary software on the customer's premises, the Field Station executable on the organization's laptop (D-033 rule 8, D-039), and rents physical devices that hold its firmware. The design records the master contract only as a reference at verification (UC-02) and has no record for a suspected fraud, scam or theft of devices, for an intellectual-property violation such as copying or leaking the Field Station's code, or for a breach of a non-disclosure agreement. The leader ruled these in scope (2026-10-14).
- **Decision**:
  1. **Master contract terms**: verification (UC-02) records that the master contract includes a non-disclosure agreement and the Field Station software licence (no copying, redistribution, reverse engineering or disclosure of the software or the firmware). An organization cannot be approved without them.
  2. **Compliance case**, an entity of the `organizations` module, opened by TrekLink Staff or an Admin against an organization, with a type: `SUSPECTED_FRAUD`, `SUSPECTED_THEFT`, `IP_VIOLATION`, `NDA_BREACH` or `OTHER_BREACH`; evidence notes; linked loss cases or contracts; an authority reference. States: `OPEN` to `CLOSED` with an outcome; every action is audited.
  3. **Police report**: a case of type `SUSPECTED_FRAUD` or `SUSPECTED_THEFT` (signs of fraud, scams or theft of TrekLink devices) cannot close without a police report reference. A loss case flagged as suspected theft or fraud opens or links such a case.
  4. **Actions** available from a case are the existing ones, recorded on the case: an Admin suspends the organization (FR-ORG-07), and Staff or an Admin revoke its Field Station credentials and API keys.
- **Rejected**: handling breaches outside the platform (no audit trail, and a suspended organization would have no recorded reason); a separate legal module (the actions are the existing suspension and revocations).
- **Consequences**: SRS: FR-ORG requirements for the contract terms and the compliance case, business rules for the NDA and licence precondition and the police reference, a use case for handling a compliance case, ERD gains `COMPLIANCE_CASE`. `organizations` spec and schema. Report 4.
- **Owner**: KhoaDD.

### D-047: Periodic maintenance: a service plan per hardware variant, a weekly scan, cost approval and firmware updates

- **Status**: ✅ **Resolved by the leader** (2026-10-14). Amends D-035 (device lifecycle labels) and D-045 rule 1 (the In service superstate is unchanged). Applied 2026-10-14: SRS (UC-13 and UC-52 rewritten, UC-64, UC-65, FR-DEV-04, FR-DEV-08, FR-DEV-17 to FR-DEV-21, BR-44, BR-45, E05-12, E05-13, Figures 23 and 25, ERD), adjusted form, `devices` spec and API catalog, `platform` configuration matrix and scheduler, `schema.prisma` with migration `20261014150000_periodic_maintenance`, Report 4.
- **Context**: the leader compared maintenance with FSOFT Guideline_Physical Asset Management v1.6 section 2.6, periodic maintenance (summarised in `ignore/khoa/docs/FSOFT_Periodic_Maintenance_Flow.md`), and section 2.5, repair, replace or upgrade. Verified gaps in the current design:
  1. A scheduled service exists only as the reason string `SCHEDULED` on `MaintenanceRecord` (`schema.prisma`); there is no interval, no due date and nothing that opens a scheduled record (SRS UC-52, FR-DEV-08).
  2. No advance notice before a service falls due (FSOFT step 1, five days ahead).
  3. A maintenance record carries no cost, no in-house or vendor distinction, no warranty and no approval (FSOFT steps 3, 4.1, 4.2 and form 23v).
  4. The firmware version is recorded only at registration (FR-DEV-02), although D-039 updates device firmware at the counter, so the device record drifts from the hardware.
  5. SRS UC-52 asks for "an expected date" that the schema does not hold.
  FSOFT step 5, the acceptance test after the work, is already the intake check that every maintained device must pass again (UC-12, FR-DEV-08). FSOFT step 6, the payment to the supplier, stays outside the platform.
- **Decision**:
  1. **Service plan per hardware variant.** An Admin sets a service interval in days and a service checklist on each hardware variant (UC-13). A variant without an interval has no periodic service. Each device holds a service due date: set from the variant interval when it first passes the intake check, and moved forward by the interval each time a `SCHEDULED` record is completed. Unscheduled repairs do not move it.
  2. **Weekly scan.** A scheduled job runs once a week. It selects every device whose service is due before the next run plus `devices.maintenanceLeadDays` (default 5, FSOFT's lead time), and every device whose firmware version differs from its variant's firmware baseline. For an `AVAILABLE` device it opens a maintenance record with reason `SCHEDULED` or `FIRMWARE_UPDATE` and moves the device to `MAINTENANCE`. A `RESERVED` or `RENTED` device is never pulled from a contract; at check-in, an inspection that passes routes it to `MAINTENANCE` with that record instead of `AVAILABLE`. Staff receive the week's list.
  3. **Record contents.** A record carries an expected completion date, whether the work is in-house or by a vendor (with the vendor's name), the estimated and the actual cost in VND, a warranty-until date for vendor work, and, for `SCHEDULED`, a result for each checklist item of the variant.
  4. **Cost approval.** IF the estimate exceeds `devices.maintenanceApprovalThresholdVnd`, THEN the record is `PENDING_APPROVAL` and cannot be completed until an Admin other than the person who recorded the estimate approves it or rejects it with a reason. A rejected record returns to `OPEN`, to be re-estimated or closed `UNREPAIRABLE`. An actual cost above the approved amount returns the record to `PENDING_APPROVAL`. Paying the vendor happens outside the platform; the cost is recorded, never invoiced to an organization, and the renter's share of a repair remains the damage charge of BR-24.
  5. **Firmware update.** Any record may record a new firmware version on completion; a `FIRMWARE_UPDATE` record must. Completion updates the device's firmware version; the intake check then accepts the unit as for any maintenance.
  6. **Maintenance record lifecycle**: `OPEN` to `PENDING_APPROVAL` and back, `OPEN` to `COMPLETED` or `UNREPAIRABLE`.
- **Rejected**: manual scheduling only (a "scheduled service" with no schedule behind it); an annual calendar of maintenance campaigns as in FSOFT (built for a multi-site office estate, too heavy for one depot in four build weeks); pulling a rented device mid-contract when it falls due (breaks the contract for a non-urgent service; a faulty unit already has replacement, D-045 rule 7); a daily scan (the leader prefers weekly; the look-ahead of the run period plus the lead days keeps a weekly run from missing a due date); recording cost without approval (FSOFT's authority level is the step a council is most likely to ask about); firmware version left as registered.
- **Consequences**: SRS: UC-13 and UC-52 rewritten, new use cases for the weekly scan and for approving a maintenance cost, FR-DEV requirements for the plan, scan, cost approval and firmware update, new business rules, an exception scenario for a rented unit falling due, the device state machine labels and a maintenance record state machine. Adjusted form: the maintenance sentence. `devices` spec, API catalog and `schema.prisma` (variant interval and checklist, device service due date, record fields and `PENDING_APPROVAL`) with a migration; `platform` scheduler registration; Report 4.
- **Owner**: KhoaDD (device lane: LongLP).

### D-048: The subject is SEP490; its syllabus, Student Guide and templates are the governing sources

- **Status**: ✅ **Resolved by the leader** (2026-10-18).
- **Context**: the team's planning drew on several course documents with different subject codes. The roadmap was first derived from `SWP490_Lo-trinh-Capstone_v1.0.pdf` (D-013), and Report 4 was built on the Report 3 template because no Report 4 template was in `Documents/templates/` (session 2026-10-14, needs check). The leader's local course folder (`/mnt/DATA/DATA/FPTU/Subjects/KLTN/SEP490/`) holds the SEP490 Student Guide (Fall 2023) and the official templates for Reports 1 to 7, Project Tracking, Test Report and Unit Test. The FLM syllabus 14065 (decision 377/QĐ-ĐHFPT, 2026-09-04) names SEP490 and lists the Student Guide and the project templates as its main materials.
- **Decision**:
  1. TrekLink's subject is **SEP490**, SE Capstone Project. It is not SWP490, SET or any other code. Documents of other codes are background only and never override SEP490.
  2. The governing sources, in order: the FLM syllabus 14065 (copy `capstone/Documents/course-material/SEP490_Syllabus_FLM_14065.md`), the SEP490 Student Guide (`capstone/Documents/course-material/SEP490 StudentGuide_Fall 2023.docx`), the SEP490 execution schedule and quick guide already listed in D-013, and the templates in `capstone/Documents/templates/`.
  3. Every graded report uses its own SEP490 template. Report 4 moves to `Report4_Software Design Document.docx`; Report 5 uses `Report5_Test Documentation.docx`, `Report5_Test Report.xlsx` and `Report5_Unit Test.xls`; tracking uses `Report3_Project Tracking.xlsx` (WBS, Issues, Defects, Q&A).
  4. D-013 stands: SWP490 practices that SEP490 does not contradict stay as practice, never as a source of requirements.
- **Rejected**: keeping the Report 3 template for Report 4 (a template mismatch is visible to the supervisor, and Report 4 carries 18% of OGA); treating the SWP490 roadmap as co-equal (the cause of the D-013 rework).
- **Consequences**: Report 4 is re-skinned onto its template; Report 5 is built on its three templates. The syllabus eligibility rule (at least 75% of the use cases submitted in Report 3 completed, and at least 20 medium use cases) is recorded as a risk row below. Roadmap and chapter 15 references to course sources cite SEP490.
- **Owner**: KhoaDD.

### D-049: No AI co-author, author or contributor in any TrekLink repository

- **Status**: ✅ **Resolved by the leader** (2026-10-18). Scope widened the same day from `treklink-web` to all four code repositories and `capstone`, going forward. History cleanup: `treklink-web` `dev` is rewritten (rule 5); history in the other repositories stays as it is.
- **Context**: the SEP490 syllabus (D-048) fails a member who cannot prove they built the software, and sends the team to the second defence round if it cannot prove it prepared the software package itself. `treklink-web` is the graded software package. On 2026-10-18 `origin/dev` held 53 `Co-Authored-By: Claude` trailers and 15 commits authored as `Claude <noreply@anthropic.com>`; `origin/main` held none, and the GitHub contributor list (default branch) showed only `ruskicoder`. The next `dev` to `main` merge would add an AI account to the contributors.
- **Decision**:
  1. No commit in `treklink-web` carries a `Co-Authored-By` trailer naming an AI model.
  2. No commit in `treklink-web` is authored by an AI identity. The member who owns the work is the author.
  3. No AI account appears among the repository's contributors.
  4. Rules 1 to 3 apply to `treklink-web`, `treklink-docs`, `treklink-firmware`, `TrekLink-Team.github.io` and `capstone` for every new commit. Agents strip their default attribution lines before committing. Conventions chapter 07 §3.4 rule 7.
  5. `treklink-web` `dev` is rewritten before it next reaches `main`: on a backup clone, `git filter-repo` drops the AI trailers and re-authors the AI-authored commits to their human owner (the leader by default); `dev` and the open feature branches are force-pushed and members re-clone or reset. The force-push runs only on the leader's explicit go at execution time.
  6. The PR template's `Model used:` field (chapter 11 §2) stays. It declares a tool; it does not make a contributor.
- **Rejected**: keeping attribution for transparency (it becomes evidence against authorship at the defence); relying on squash merges alone (a squash commit lists every co-author unless the message is edited).
- **Consequences**: chapter 07 §3.4 rule 7; the `treklink-web` history rewrite of rule 5, announced in Zalo before the force-push. Rejected for the cleanup: squashing at release only, which leaves the AI history visible on `dev` to anyone browsing branches.
- **Owner**: KhoaDD.

### D-050: The Progress Log and Project Tracking workbooks are dropped; contribution evidence is daily reports, commits and Jira

- **Status**: ✅ **Resolved by the leader** (2026-10-18).
- **Context**: the roadmap (§3.2) named `GFA26SE55_Progress_Log.xlsx` the primary evidence of individual contribution, taken from the SEP490 execution schedule, and the Student Guide (D-048) suggests a tracking database with WBS, Issues, Defects and Q&A sheets (`Report3_Project Tracking.xlsx`), adding that any team-convenient tool may be used instead. Both workbooks were last committed on 2026-09-17. The team already records the same facts in daily reports (chapter 12), commits and PRs, and Jira (chapter 10).
- **Decision**: the two workbooks are no longer maintained. Contribution and progress evidence is the daily reports, the git history and Jira. If the supervisor or a council asks for a workbook, it is produced from those records at that time.
- **Rejected**: rebuilding both workbooks for W1 to W7 before Review 2 (duplicate bookkeeping of facts already recorded elsewhere).
- **Consequences**: roadmap §3.2, §3.3 and the deliverable ledger updated. Risk: the SEP490 execution schedule names the Progress Log as evidence; if a reviewer asks for it at Review 2, it must be generated on short notice.
- **Owner**: KhoaDD.

### D-051: The backlog is one story per SRS use case, generated from the SRS data, with new IDs

- **Status**: ✅ **Resolved by the leader** (2026-10-18).
- **Context**: `build_backlog.py` still modelled the pre-D-033 scope (8 epics, 87 stories on trips, bookings, the seven-state rental machine, `device_types` and `maintenance_logs`). The SEP490 syllabus counts use cases (D-048), and Jira already holds the old cards with labels `backlog-E1` to `backlog-E8` and `backlog-US-001` to `backlog-US-087`, which `jira_sync.py` skips on sight.
- **Decision**:
  1. One story per SRS use case, generated from `capstone/scripts/srs/srs_data.py`; the acceptance criteria are the FRs that cite the use case, plus its business rules and exceptions. Four delivery stories cover work with no use case (local stack and CI, seed data, Neon deployment, the D-042 suite). The generator stops if an FR has no story.
  2. IDs: epics `EP01` to `EP10`, stories `US-UCnn` and `US-Xnn`. The old cards are retired (`jira_sync.py --retire`, label `retired-d033`, Done transition); new Jira keys are recorded after the sync in `JIRA_KEYS`.
  3. The week 3 baseline is `srs_data.W3_MAP`: 51 of the 58 week 3 use cases map onto 44 current use cases (flag `baseline`); 7 were removed by D-033. Completing the 44 completes 51 of 58 (88%); the floor is 44 of 58.
  4. Owners follow the lanes of roadmap §5.1; LongNN owns the read-only screen use cases (UC-38, UC-42, UC-55, UC-59), split by layer as in D-023, and is secondary on every other story with a human actor. Sprints follow roadmap §4.2, and `jira_sync.py` now dates Jira sprints from that table.
- **Rejected**: one story per FR (110 stories, and the 75% rule counts use cases); hand-written stories (they drifted from the SRS once already); reusing `US-001` (collides with the stale Jira cards); continuing at `US-088` (the ID no longer names its use case).
- **Consequences**: `03-backlog/` regenerated (10 epics, 69 stories, 192 points), `User_Story_Agile_TrekLink.xlsx` rebuilt, chapter 10 §2.1 table, §7.1a and §9 updated, `_docs/README.md` updated. Jira sync and retirement wait for the leader's review (outward action).
- **Owner**: KhoaDD.

### D-052: The leader writes every spec; members study, own, defend and implement their lane

- **Status**: ✅ **Resolved by the leader** (2026-10-19).
- **Context**: on 2026-10-18 the leader asked whether the specs were ready for members to design. Every `design.md`, `api-design` source and `tasks.md` in `treklink-web/specs/` was written by the leader with an agent; members appear only as small edits. The SEP490 syllabus fails a member who cannot prove they built the software (D-048, D-049). Report 4 (SDD) is generated from the `design.md` files (D-044), and the Review 2 package is due 2026-10-25. SRS §3.1.2 Screens Flow and §3.1.3 Screen Descriptions are still empty.
- **Decision**:
  1. The leader decides scope, FRs and stories, and writes `requirements.md`, `design.md`, the `api-design` sources and `tasks.md` of every module, kept in sync with the SRS data (`capstone/scripts/srs/srs_data.py`).
  2. Each member takes the suites of their lane (roadmap §5.1), studies them, owns them and must defend their domain at every review, then implements from `tasks.md`. A member who finds a defect raises it; the leader decides the change.
  3. Screen layouts are delegated to members by the leader, each assignment with a deadline of 2 to 3 days. The leader finishes whatever is not done by the deadline, in about 2 to 3 further days.
  4. A spec change is a pull request to `dev` reviewed by the leader; the merge is the approval. Each `design.md` carries a `Status` line.
  5. No design stories are added. A story is ready when its suite is approved and its owner has studied it (chapter 10 §2.1, Definition of Ready); in Jira this is a subtask of the `US-UCnn` card.
- **Rejected**: members design the backend from `requirements.md` alone (cannot meet 2026-10-25, and the SDD would be rebuilt from new designs); one design story per module (breaks D-051, one story per use case); approval recorded in Jira only (leaves no evidence in git).
- **Consequences**: `treklink-web/specs/README.md` §6, chapter 02 tenet 7, chapter 10 §2 and §2.1 updated; `Status` line added to every `design.md`. Supersedes the wording of D-051 rule 4 only where it implied members design.
- **Owner**: KhoaDD.

### D-053: Every story runs SD, CO, UT and RV in one pull request; pages belong to their module's lane

- **Status**: ✅ **Resolved by the leader** (2026-10-19).
- **Context**: a review after each phase (V-model style) costs the leader a review per phase per story. Members must design, code and test reliably on their own. The frontend task list gave all 39 page tasks to LongNN while LongLP held 58 tasks.
- **Decision**:
  1. A story runs four mini-phases, SD (specification and design), CO (code), UT (unit test) and RV (review), all in one pull request; the leader reviews the whole PR once. A finding reopens the phase it belongs to, on the same PR (chapter 10 §7.1b).
  2. UT is done at **at least 80% branch coverage and 100% line coverage** of the files the PR changes, by the CI coverage report.
  3. Effort is story points, a measure of complexity, never lines of code.
  4. Each module's pages are built by that module's lane owner. LongNN owns the shell, shared components, maps, plans, administration, monitoring pages and the journeys, and reviews every page PR for consistency. Screens are designed in `specs/frontend/ui-design/` against chapter 06 §7 (checklist) and §8 (practices).
  5. `requirements.md` holds requirements only, in EARS (functional, including endpoint behaviour and error codes, and NFRs); detail lives in `api-design/`, `ui-design/` and `design.md` (chapter 02 tenet 8).
  6. Software Package 1 runs on local Docker Postgres; Neon waits for Sprint 4 (D-010). *Superseded by D-062 on 2026-10-24: shared development runs on the Neon `dev` branch.*
- **Rejected**: a review per phase (leader effort); counting lines of code; LongNN building every page; a separate "requirement details" file.
- **Owner**: KhoaDD.

### D-054: Every member commit carries a sealed Checksum trailer declaring the model and stage

- **Status**: ✅ **Resolved by the leader** (2026-10-20). Rules 4 and 5 amended by D-070 (2026-10-25): an explicit model allowlist with the variant sealed; an unsealed commit stays a label.
- **Context**: the PR template's free-text `Model used:` line (chapter 11 §2.4) can be edited after the fact and says nothing per commit. The Review 2 guide asks for the AI tools, models and stages to be declared in Report 4 (risk row of 2026-10-20), and D-049 removes AI attribution from commits. The leader wants a per-commit declaration that cannot be altered after it is written.
- **Decision**:
  1. Every commit a member makes in `treklink-docs`, `treklink-web`, `treklink-firmware` and `TrekLink-Team.github.io` carries one trailer, `Checksum: <64 hex>`, written by a commit-msg hook (`treklink-docs/.github/scripts/tk_checksum.py install`).
  2. The token is AES-256-GCM under the member's own key. It holds the model family and version and the stage (SD, CO, UT, RV, DOC or CHORE), bound to the member code and the commit subject. The model is readable only with the keys.
  3. All member keys live in `capstone/.provenance/keys.json`, committed to the private `capstone` repository, and in the organisation secret `TK_CHECKSUM_KEYS` for CI. Any member can read every key. Forgery is prevented by rule: an AI agent refuses to seal with another member's key or to write a token by any means other than the hook (AGENTS.md §6, chapter 08 §3.1).
  4. CI (`checksum.yml` on `pull_request`, calling the reusable `checksum-verify.yml` at treklink-docs `dev`) fails on a token no key opens, a token sealed by another member than the commit's GitHub author, a model outside chapter 11 §2.1, or a restricted model on a feat or fix commit. An unsealed commit is a hand-typed commit: it gets the `provenance-review` label and a manual review, no failure. AI attribution (D-049) gets the same label.
  5. Approved for sealing: Claude Opus and Sonnet from 4.8, Claude Fable from 5.1, GPT from 5.6. Restricted (chores only): Gemini and Claude Haiku. `human` declares a hand-written commit.
  6. The `Model used:` line is removed from AGENTS.md and the PR templates; the trailer replaces it.
  7. The mechanism is documented in chapter 07 §3.6, visible to every member. Report 4 declares it with the AI tools, models and stages.
- **Rejected**: a `pull_request_target` trigger (GitHub reads it from the default branch `main`, and disables it on public repositories from 2026-11-02; it shielded only a secret members can already read); keys held by the leader only with one private key per member (more distribution work; the leader accepted the forgery risk under rule 3); failing CI on an unsealed commit (a hand-typed commit is legitimate and is reviewed instead); a plaintext model trailer (the leader keeps the model inside the token); a manual seal command (easy to forget).
- **Consequences**: chapter 07 §3.4 rule 7 and new §3.6; chapter 08 §3.1; chapter 11 §2.1 and §2.4; the five AGENTS.md copies §6; the PR templates of treklink-docs, treklink-web and TrekLink-Team.github.io. The token proves who sealed it and that the declaration is unchanged; it does not prove which model wrote the code.
- **Owner**: KhoaDD.

### D-055: Review 2 package: no registration change, grouped features, AWS staging, one decision per member

- **Status**: ✅ **Resolved by the leader** (2026-10-20).
- **Context**: the course's Review 2 guide (`capstone/Documents/course-material/SWP490_R2_Huong-dan-chuan-bi-Review-2_1.pdf`) asks for the final registration form with a Record of Changes (BM03), Reports 1 to 5 and Project Tracking, a self-review (BM02) on tag `review-2`, and a Design Brief (BM01) with Defense 1.1 targets. A main workflow must change the state of a main entity; mandatory features set the committed test count (3 per feature, 1 per workflow, per state transition and per NFR); demos run on a staging environment declared in Report 4.
- **Decision**:
  1. The adjusted registration form submitted to F-CAPS after Review 1 is the approved current version. BM03 records "No changes".
  2. MF-04 stays as defined. Ingested telemetry updates the device's battery and last-seen time (FR-DEV-06), and UC-41 flags a device stale when silent beyond its threshold and clears the flag when it reports (FR-MON-03). Report 4 draws this as a Device connectivity state machine (Reporting, Stale) so the workflow's state change is traceable.
  3. Mandatory features group the 44 baseline use cases (D-051) into about 20 features, each with measurable acceptance criteria. Every baseline use case still ships (D-048).
  4. Environments: development on local Docker Postgres (D-053); staging and production on AWS for the backend and an MQTT broker, with Neon Postgres (D-010), ready by Sprint 4. Iteration 1 at Review 2 runs locally. *Development superseded by D-062 on 2026-10-24.*
  5. Report 4 declares the AI tools, models and stages, and states that every commit declares its model and stage (D-054), without the sealing detail.
  6. Design Brief section 3, one key decision per member: three-tier field buffering with event idempotency (D-018, D-006, D-040), KhoaDD; organization-scoped isolation of every request and API key (FR-AUTH-11, D-042), TanNB; tiered incident notification and escalation (D-034), HoangTK; Leaflet over OpenStreetMap with the sovereignty overlay and one live WebSocket stream (D-031), LongNN; device and contract lifecycles as state graphs with custody intervals and loss cases (D-035, D-040, D-045), LongLP.
  7. Twenty mandatory features cover the 44 baseline use cases plus the six flow-path use cases (2, 3, 12, 23, 24, 51). Feature owners: LongLP 7, KhoaDD 4, HoangTK 3, LongNN 4 (platform accounts, device holder labels, system health, administration), TanNB 2. A feature owner answers for it at review; others may code parts of it.
  8. Every transition of all eight lifecycles is a main-entity transition with one test: 80 tests. With 60 feature tests, 5 workflow tests and 6 NFR tests the Defense 1.1 commitment is 151 test cases, at least 76 automated in CI.
  9. Design Brief section 7 NFRs: NFR-REL-01, NFR-REL-03, NFR-REL-04, NFR-PERF-01, NFR-PERF-04, NFR-SEC-04.
- **Rejected**: one feature per use case (132 to 195 feature tests, a commitment the Defense 1.1 count check could fail); Render or Vercel for the backend (the leader chose AWS; Vercel functions cannot hold the WebSocket and MQTT connections); a plaintext account of the commit seal in Report 4.
- **Owner**: KhoaDD.

### D-056: The MF-04 owner takes the monitoring backend; HoangTK keeps incidents

- **Status**: ✅ **Resolved by the leader**. LongNN drafted it at his own request (PR #78, merged 2026-10-22); the leader reviewed the content and confirmed it on 2026-10-22, adding rules 5 and 6 and the task 2.3 wording of rule 2.
- **Context**: roadmap §5.1 gave LongNN MF-04 but only its screens (`frontend` tasks 9.1 to 9.4), while every `specs/monitoring/tasks.md` task except 5.1 was HoangTK's. LongNN's lane was thin (14 tagged tasks, all frontend, against HoangTK's 30), and Review 2 requires each member to own two to three parts and at least one main workflow they can defend (Design Brief section 8, D-052 rule 2); at the review each member opens and explains the code they own (roadmap, "Before Review 2"). An owner who builds no part of the flow's backend cannot defend the Organization API or the tenancy tests. The page rule of D-053 rule 4 also had an exception here: the monitoring pages were LongNN's while the module was HoangTK's.
- **Decision**:
  1. LongNN owns the `monitoring` backend: tasks 1.1, 2.1, 2.2, 2.4, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2 and 6.1 of `specs/monitoring/tasks.md`, plus the screens of `specs/frontend/tasks.md` 9.1 to 9.4. MF-04 is therefore LongNN's end to end, backend and UI.
  2. HoangTK keeps the `incidents` module. Task 2.3 (`incident.alert` publishing) is the one task of `monitoring` with another owner: it is a single synchronous listener that delivers an MF-03 alert, and it sits in `monitoring` only because the `user:<id>` rooms of `LiveGateway` do, so HoangTK owns it and answers for alert delivery. LongNN answers for the stream, the rooms and every other task of the module. HoangTK is the secondary reviewer of LongNN's monitoring PRs because MF-03 consumes `LiveGateway`.
  3. D-053 rule 4 is unchanged: each module's pages belong to that module's lane owner, and LongNN owns the shell, shared components, maps, plans, administration, monitoring pages and the journeys. The monitoring pages now follow that rule with no exception.
  4. Feature owners of D-055 rule 7 are unchanged (LongNN 4, HoangTK 3).
  5. **Fallback**: tasks 1.1 and 2.1 are the ones Review 2 needs (MF-02 events on a map). If task 1.1 has no open pull request two working days after `platform` Phase 1 merges to `dev`, or 1.1 and 2.1 are not merged before the `review-2` tag is cut, the leader moves 1.1 and 2.1 back to HoangTK and LongNN keeps the rest. The clock starts at the platform merge, so a delay in the leader's lane does not count against LongNN.
  6. HoangTK acknowledges the change on `treklink-web` PR #37, which moves the owner tags, before Sprint 4 starts. The acknowledgement does not block the merge (leader, 2026-10-23).
- **Rejected**: splitting the monitoring tasks half and half (two owners in one module, no one answers for the stream); moving MF-04 to HoangTK (LongNN would lose the flow presented at Review 1); adding backend work from another lane (LongLP already holds `auth`, `rentals` and `billing`).
- **Consequences**: roadmap §5.1 and the charter team matrix updated (PR #78). Follow-ups done on 2026-10-22: `build_backlog.py` sets `LANE["monitoring"] = "LongNN"` with HoangTK as the secondary owner of monitoring stories, and the backlog is regenerated; `treklink-web/specs/monitoring/tasks.md` and `specs/README.md` carry the new owners; the Report 2 RACI and the Design Brief Ownership Map are updated and rebuilt; the lane table of chapter 11 §3.4 is brought in line with roadmap §5.1. Jira assignees follow on the next `jira_sync.py` run by the leader. Residual exposure: LongNN is IC-track, so the backend ramp-up of register row "NestJS is a skill only for Khoa" applies to monitoring; the reviewer is KhoaDD.
- **Owner**: KhoaDD.

### D-057: Rulings on the LongNN screen designs: permission catalog, audit routes, telemetry routes, health rows, report shapes, messages

- **Status**: ✅ **Resolved by the leader** (2026-10-23), from the open items O-1 to O-10 of `treklink-web` PR #36 and its notes for the SRS owner.
- **Context**: the nine screen designs of the LongNN lane found gaps in the endpoint catalogs, the route table of `specs/frontend/design.md` §2 and the SRS message list. A screen cannot be built against an endpoint that does not return what it shows.
- **Decision**:
  1. **Accounts (O-1)**: `GET /api/accounts` returns `phoneNumber`. "Invitation pending" is `lastLoginAt` null; no new field.
  2. **Permission catalog (O-2)**: new `GET /api/permissions`, gated by `role.manage`. Each item: `key`, `action`, `subject`, `scope` (`own` or `any`), `accountType` (`TREKLINK` or `ORGANIZATION`), `description`, `protected` (ADMIN cannot lose it). Raw CASL `conditions`, `fields` and `inverted` are not returned. The catalog is read-only and comes from the seed only. `PUT /api/roles/:id/permissions` keeps rejecting a key not in the catalog (400 `UNKNOWN_PERMISSION`) and also rejects a permission whose account type differs from the role's (400 `PERMISSION_SCOPE_MISMATCH`), so an organization role can never receive a platform permission. `GET /api/roles` returns permission keys only, joined to the catalog on screen. `Permission` gains a non-null `accountType` column, filled by a new migration from the role grants of `scripts/specs/catalog.py`; `build_seed.py` refuses a permission granted to no role or to roles of two account types. That check split the three permissions shared by Staff and Org Manager into a TrekLink key and an organization key with the suffix `.org` (organization data no tenant owns): `hardwareVariant.read` and `hardwareVariant.read.org` (active variants, no counts), `device.availability` and `device.availability.org`, `plan.quote` and `plan.quote.org` (formerly `plan.quote.own`, which carried no condition).
  3. **Audit routes (O-3)**: two sub-routes, `/t/admin/audit/changes` (`AuditLog`, `auditLog.read`) and `/t/admin/audit/sign-ins` (`AuthEvent`, `authEvent.read`); `/t/admin/audit` redirects to the first. Each tab checks its own permission and is hidden without it; filters live in the URL query. The parameters page links to the change log filtered to the parameter.
  4. **Sign-in filter (O-4)**: `GET /api/auth-events?organizationId=<uuid>`, a query filter, never an authorization input (`authEvent.read` decides access). The server resolves the organization through the user's membership; an attempt that matched no account never matches the filter. A malformed UUID is 400 `VALIDATION_FAILED`, an unknown organization an empty page. Each row returns `organization {id, name}` or null.
  5. **Messages**: MSG35 for an invalid period (O-5), MSG36 for `STALE_VERSION` (a dialog with Reload that keeps the user's input), MSG37 `LAST_ADMIN`, MSG38 `ADMIN_LOCKOUT`, MSG39 `SELF_DEMOTION`. Success of account, role and parameter actions is MSG03. The client maps `errorCode` to a message; the server `message` is a fallback only.
  6. **Empty states (O-6)**: screen copy, no MSG code. 9.3 keeps "No Field Stations are registered yet." 2.3 reads "No plans are available right now. Contact TrekLink to ask about renting." with the footer contact link.
  7. **Admin routes (O-7)**: TrekLink Admin inherits every TrekLink Staff route (FR-AUTH-10, auth REQ-UBI-05); `design.md` §2 states it once.
  8. **Telemetry routes (O-8)**: `/o/devices/:id/telemetry` and `/t/devices/:id/telemetry`, period in the query. Named telemetry so it never collides with the lifecycle history of `/t/devices/:id` (monitoring api-design 07).
  9. **Health rows (O-9)**: `GET /api/system-health` returns `fieldStations.items[]` (`id`, `name`, `organization`, `lastSyncAt`, `stale`, `queueDepth`, `oldestRetryCount`, `version`, `outdated`), excluding revoked stations, plus `fieldStations.currentRelease`. Queue depths are named objects `{p0, p1, p2, p3}`; the column stays `Int[]`.
  10. **Reports (O-10)**: a row shape per kind (`utilization`, `revenue`, `overdue`, `lost`, `incident-times`); a period of at most 366 days (`monitoring.reportMaxRangeDays`), 400 `VALIDATION_FAILED` beyond it or when reversed.
  11. **Who changes what**: the leader edits the catalogs, schema, `design.md` and the SRS (D-052 rule 2); LongNN updates his screen files in PR #36.
- **Rejected**: the union of role permissions as the checkbox universe (a permission removed from every role could never be granted again); inferring a permission's account type from its condition (a security check must not rest on an inference); one audit route with client-only tabs (no deep link, one permission for two data sets); a path segment `/auth-events/<organizationId>` (a filter, not a resource); "history" for the telemetry route; MSG28 for the three Admin lockout rules (its text explains none of them).
- **Consequences**: `treklink-web` spec PR (catalogs, schema and migration, `design.md` §2, regenerated api-design and permission matrix); SRS messages MSG35 to MSG39 and Report 3 rebuilt; PR #36 changes requested.
- **Owner**: KhoaDD.

### D-058: Review 2 on Tue 2026-10-27; Iteration 1 is the platform slice with MF-02 by fixture replay; fixed cutoffs

- **Status**: ✅ **Resolved by the leader** (2026-10-23), in a question round on Software Package 1.
- **Context**: the official Review 2 session is Tue 2026-10-27, not the end of W8, and the leader wants every deliverable done one day earlier. That leaves Fri 2026-10-23 to Mon 2026-10-26. The working-day clocks of D-056 rule 5 and of the auth cover would expire after the review.
- **Decision**:
  1. **Dates**: tag `review-2` on Sun 2026-10-25 at 22:00 ICT; BM02, the team response per finding, Design Brief §5 and the PDF rebuild on Mon 2026-10-26; review Tue 2026-10-27.
  2. **Iteration 1 scope**: `platform` Phases 1 and 2 with the demo seed (1.12), sign-in, CI, and MF-02 shown by replaying the golden fixtures through the local Mosquitto into `gateway-sync` and onto the TrekLink fleet map. Events land `UNATTRIBUTED` (no `rentals` yet), so they reach the `fleet` room only. Iteration 1 runs locally (D-055 rule 4). The Field Station executable (`gateway-sync` 5.1) and live hardware move to Sprint 4. MF-01 is shown from the specs and the screen designs.
  3. **LongLP, sign-in**: `auth` 1.1 to 1.4, 2.1 to 2.4, the login, refresh, logout and me endpoints of 6.1 (api-design 01 to 04) and the sign-in page of `frontend` 2.1, in a PR by Sat 2026-10-24 20:00 ICT; `auth` 4.1 and 4.2 (CASL guards) by Sun 2026-10-25 12:00 ICT. Missed, the leader covers (roadmap §5.1 emergency cover).
  4. **LongNN, map**: `frontend` 1.1 to 1.4 (shell, `apiClient`, Leaflet with the overlay, `socketClient`), `monitoring` 1.1, 2.1 and 3.1, and `frontend` 9.1, in PRs by Sun 2026-10-25 12:00 ICT. Missed, HoangTK takes `monitoring` 1.1 and 2.1 and the leader takes 9.1. This replaces the clock of D-056 rule 5 for Iteration 1; D-056 rule 5 applies again from Sprint 4.
  5. **Leader lane**: `platform` 1.7, 1.11, 1.12 and 2.2 to 2.10; the `devices` reads that ingestion needs; `gateway-sync` 1.1, 1.2, 2.1 to 2.3 and the replay harness of 4.2.
  6. **TanNB** (QA lead) runs the demo on the seed on Sun 2026-10-25 from 18:00 ICT and logs defects as issues. **HoangTK** stands by for the rule 4 fallback.
  7. **Release**: `dev` was released to `main` in all four repositories on 2026-10-23 and is released again at the tag.
  8. The study's open questions (credentials with queued SOS, Socket.io or WebSocket for the organization API, the two graces, the broker host, invoice lines, organization closing, partial handover, the lifecycle count) are deferred to Sprint 4; none of them shapes the Iteration 1 slice.
- **Rejected**: the full MF-01 and MF-02 build (needs every member coding at once in three days); the live Field Station path for the review (every leg would have to land by Sunday); the leader building every lane (destroys the commit evidence the register already flags); working-day clocks (they expire after the review).
- **Consequences**: `.github/schedule.yml` and roadmap rows updated; notice issue to the team; the W7 milestone "MF-01 complete" is not met and is stated at the review.
- **Owner**: KhoaDD.

### D-059: Rulings on the LongLP, LongNN and HoangTK screen designs: landing routes, uncoded messages, report row ids, incident order

- **Status**: ✅ **Resolved by the leader** (2026-10-23), in a live question round on the reviews of `treklink-web` #42 (LongLP), #43 (LongNN, D-057 follow-up) and #45 (HoangTK).
- **Context**: the three screen-design PRs raised open questions under D-052 rule 2. The review confirmed several against the specs: `auth` api-design 05 names `auth.otpResendCooldownSeconds` while the catalog and auth REQ-ERR-08 name `auth.codeResendCooldownSeconds`; `billing` 15 does not return the VietQR block, so the payment page cannot redraw the QR after a reload; `billing` 02 samples only a day-plan quote; an organization member whose invitation code expired has no way to get a new one; `monitoring` 08 report rows carry codes but no ids; per-organization percentiles cannot be combined into a platform figure; `incidents` 01 and 11 page without a documented order; `incidents` 02 samples `statusUpdates[]` and `authorityReports[]` only as empty arrays; `incidents` 03 requires `expectedVersion` but lists no `STALE_VERSION`. LongLP's question 11 was withdrawn: `billing` 17 has listed 403 `SEPARATION_OF_DUTY` since the rescoped specs.
- **Decision**:
  1. **Landing after sign-in**: a same-origin `?next=` path wins. Otherwise the Org Manager lands on a new organization home dashboard at `/o` (contract summary, balance due, open incidents, devices out), the Org Operator on `/o/map`, TrekLink Staff and Admin on `/t/map`. The dashboard is designed and built by LongLP in Sprint 4; until it exists the Org Manager lands on `/o/contracts`.
  2. **Closed organizations**: a member of a `CLOSED` or `REJECTED` organization who signs in gets 401 `INVALID_CREDENTIALS` (MSG09), the same answer as an unknown account, so closed organizations cannot be probed (auth REQ-STA-03).
  3. **Errors without an SRS message code** (`ACCOUNT_LOCKED`, `OTP_COOLDOWN`, `BEFORE_START_DATE`, `SIGNER_NOT_MANAGER`, `RESET_REQUIRED`, `VARIANT_MISMATCH`, `UNKNOWN_DAMAGE_CODE`, `NOTHING_DUE`, `PAYMENT_PENDING`, `EFFECTIVE_IN_PAST`, and the browser-only "Passwords do not match."): the screen shows the server `message`, the SRS §5.3 fallback, through Iteration 1. New MSG codes come with the Sprint 4 SRS revision.
  4. **Contract approval**: the server picks the reserved units; screen 5.3 does not offer `deviceIds`. The counter swaps a unit at handover when needed.
  5. **Placement**: the account menu is a header menu with a change-password dialog and has no route; damage rates are a section of `/t/admin/prices`.
  6. **Spec additions, generated from the catalogs**: `auth` 05 uses `auth.codeResendCooldownSeconds`, and a forgot-password request for an active account that never set a password sends a `SET_PASSWORD` code, which renews an expired invitation through `/forgot` without a new endpoint; `auth` 01 states the rule 2 answer; `billing` 02 adds a `MONTHLY` sample with `termFeeVnd` and `firstPaymentVnd`; `billing` 15 returns `vietQr` while the payment is `PENDING`; `billing` 08 and 09 return `organization { id, code }`; `monitoring` 08 adds `contractId` to `overdue` rows, `contractId` and `lossCaseId` to `lost` rows, and one `incident-times` row with `organization` null computed over all incidents of the period.
  7. **Incidents**: `incidents` 01 returns rows by `tierDeadlineAt` ascending with nulls last, then `firstEventAt` newest first; `incidents` 11 keeps open cases first, then `reportedAt` newest first; neither takes a sort parameter. `incidents` 02 samples non-empty `statusUpdates[]` and `authorityReports[]`. `incidents` 03 adds 409 `STALE_VERSION` (MSG36); `ALREADY_OWNED` (MSG27) is checked first, so a second member acknowledging still learns who owns the incident.
  8. **Study fixes** from HoangTK's result on issue 59: MF-03 and MF-04 step 2 route and scope by the custody interval of the occurrence time (D-040); E03-1 states that a fall SOS sends no beacons, so cadence detection cannot recover it; the study brief records that issue 59 is open.
- **Rejected**: a sort parameter on the incident lists (more backend and test work for no demo gain); new MSG codes before Review 2 (reopens Report 3 two days before the review); landing every organization account on the map (not the control view the leader wants for the Org Manager); building the dashboard inside Iteration 1 (D-058 fixed the scope); a dedicated `ORGANIZATION_CLOSED` code (confirms the email exists); dropping `expectedVersion` from acknowledge (the other incident mutations all carry it).
- **Consequences**: `treklink-web` #46 edits the catalogs, regenerates the api-design files and updates `specs/frontend/design.md` §2 (landing rules, the Sprint 4 `/o` route) and `specs/frontend/tasks.md` (task 5.6, the dashboard, for LongLP). Reviews: #43 approved, #42 changes requested for the `billing` 17 error and the 6.1 error placement, #45 commented with these rulings.
- **Owner**: KhoaDD.

### D-060: Sign-in rulings for Iteration 1: organization sign-in through a real provider, the port carries the organization name, 14-day refresh, strict rotation

- **Status**: ✅ **Resolved by the leader** (2026-10-23), in a question round on the review of `treklink-web` #48 (LongLP, TK-121) and the three questions of treklink-docs#87.
- **Context**: #48 delivers the D-058 sign-in slice. The review ran it against Postgres 16 with the demo seed: every flow matches the specs, with these gaps. `ACCOUNT_CONTEXT_PROVIDER` has no provider, so organization accounts are refused; the spec cited `organizations` 2.9 as the provider, but the provider task is `organizations` 1.3 (2.9 is channel key rotation). `auth` api-design 01 and 04 show `organization.code` and `legalName`, which the port does not return. `JWT_REFRESH_TTL` defaults to `7d` in `environment-variables.ts` while `auth` requirements §4 and api-design 01 say `14d`. `JWT_REFRESH_SECRET` is validated but unused, because the refresh token is opaque and stored as SHA-256. Refresh returns `user`, which api-design 02 does not show. A concurrent rotation of one refresh token is treated as reuse and revokes the family.
- **Decision**:
  1. **Organization sign-in**: the leader builds the `ACCOUNT_CONTEXT_PROVIDER` half of `organizations` 1.3 now, in the `organizations` module, so the seeded Manager and Operator sign in for Iteration 1. `API_KEY_RESOLVER` and the exit-check port of 1.3 stay with TanNB. Until the provider merges, `auth` refuses organization accounts with MSG09.
  2. **Environment**: `BCRYPT_COST`, `MAIL_TRANSPORT`, `MAIL_FROM` and `SMTP_URL` are validated in `platform/config/environment-variables.ts` next to `JWT_*` (#87 item 2).
  3. **Sign-in page** on the existing router and `apiClient`, tokens in memory only; `frontend` 1.1 and 1.2 build the auth context and silent refresh on top (#87 item 3).
  4. **`JWT_REFRESH_TTL` defaults to `14d`**, as the spec says; the code default is corrected.
  5. **The port carries the organization name**: `AccountMembership` gains `organizationCode` and `legalName`, and login and `me` return them as api-design 01 and 04 show.
  6. **`JWT_REFRESH_SECRET` stays, optional and unused**, reserved in case refresh tokens become signed tokens.
  7. **Refresh returns tokens only**, as api-design 02 shows, the shape of a standard token response; a client reads `GET /api/auth/me` for fresh roles and membership.
  8. **Strict rotation**: two rotations of one refresh token at once count as reuse and revoke the family (REQ-ERR-02). `frontend` 1.2 runs one refresh at a time and shares its result between callers.
  9. **Lockout counting**: `LOGIN_FAILED` events count inside `auth.loginFailureWindowMinutes`, excluding events before the last successful sign-in and before the end of the last lock. The failure that reaches `auth.loginMaxFailures` already answers 423 `ACCOUNT_LOCKED`.
- **Rejected**: a stub provider inside `auth` (it would read `OrganizationMember`, a table `organizations` owns, and the module-boundary check rejects it); refusing organization accounts until Sprint 4; TanNB coding 1.3 before the Sunday demo run; dropping the organization name from the API; removing `JWT_REFRESH_SECRET`; a grace window for concurrent refresh (a requirements change, a new parameter and weaker reuse detection); adding `user` to api-design 02.
- **Consequences**: #48 is sent back for items 5 and 7, the `organizations` 1.3 comment and a backslash guard on `?next=`; `auth` design §2 and the lockout rule, `auth` tasks 1.2, `organizations` 1.3 ownership, `frontend` 1.2 and `platform` configuration are updated in `treklink-web`.
- **Owner**: KhoaDD.

### D-061: Every route is guarded globally; `@Public()` opts out and `@CheckPolicies` lives in `common`

- **Status**: ✅ **Resolved by the leader** (2026-10-24), in a question round while building `platform` task 4.2.
- **Context**: `platform` task 4.2 told `ParametersController` and `AuditLogController` to use `auth`'s `JwtAuthGuard` and `PoliciesGuard`, but `platform` may not import `auth` (`platform` design Figure 3, enforced by the module-graph check of `platform` 1.11). Every module below `auth` in Figure 3 has the same problem, and a route that forgets `@UseGuards` is open.
- **Decision**:
  1. `auth` registers `JwtAuthGuard` and then `PoliciesGuard` as global guards (`APP_GUARD`). Every route requires a valid access token and a passing policy unless it opts out.
  2. `@Public()` opts a route out of both guards: sign-in, refresh, health, the SePay webhook and the broker hooks. `@Authenticated()` requires a token but no permission: sign-out and `GET /api/auth/me`.
  3. A route with neither `@Public()`, `@Authenticated()` nor `@CheckPolicies` is refused with 403, so a forgotten policy fails closed.
  4. `@Public()`, `@Authenticated()`, `@CheckPolicies` and `@Caller()` live in `backend/src/common/decorators`, which every module may import; `auth` re-exports `CheckPolicies` so existing imports keep working. The CASL ability, the guards and `scopeWhere` stay in `auth`.
- **Rejected**: hosting `platform`'s controllers in `monitoring` (endpoints in another module's folder, ownership of api-design 02 to 05 unclear); deferring 4.2 to Sprint 4; a guard port declared by `platform` (a second mechanism for what `APP_GUARD` does natively); per-controller `@UseGuards` (open by default).
- **Consequences**: the `auth` controller drops its `@UseGuards` and gains `@Public()` and `@Authenticated()`; `HealthController` gains `@Public()`; `platform` 4.2 is built on this. `auth` design §3 and `platform` design §2.1 record the rule.
- **Owner**: KhoaDD.

### D-062: Shared development moves to Neon now, on a `dev` branch, Postgres only

- **Status**: ✅ **Resolved by the leader** (2026-10-24), in a question round before the CO phase.
- **Context**: the team starts the CO phase of D-053 for Iteration 1 (D-058). D-053 rule 6 and D-055 rule 4 kept development on local Docker Postgres until Sprint 4, so every member codes against a private database with a private seed, and a cross-module integration fault surfaces only on the leader's machine. The Neon project of D-010 had never been provisioned. `neon init` offers Postgres, Neon Auth, the Data API, functions, object storage, an AI gateway and realtime, and its starter `neon.ts` expires every new branch after 7 days.
- **Decision**:
  1. Shared development runs on Neon from 2026-10-24, project `damp-queen-78476528`. This supersedes D-053 rule 6 and the development half of D-055 rule 4.
     **[Amended 2026-10-24]** The project is named `Treklink-web_001`. When a free-plan limit is reached, the leader duplicates the project under the next number (`Treklink-web_002`, then `_003`), applies the migrations and the demo seed to its `dev` branch, and sends a new team env zip; the connection strings change with each project. Each member replaces `.env` from the new zip and changes nothing else. Members receive only the `dev` strings; the `production` string stays with the leader and CI (rule 2).
  2. The team codes against the Neon branch `dev`, a child of `production`. `production` is kept for staging and production. `treklink-web/neon.ts` exempts `dev` from the 7-day expiry; any other new branch is a personal scratch branch and expires.
  3. Postgres only. Neon Auth is not used, because identity is JWT, bcrypt and CASL by the architecture contract (chapter 04). No other Neon service is provisioned; one is added only through a spec and a decision.
  4. Migrations reach the Neon `dev` branch only from the git `dev` branch, by CI or the leader (D-010, question 40, unchanged).
  5. Local Docker Postgres stays the database of unit tests, `test:db` and CI.
  6. The leader sends the team env file privately in Zalo as a zip. Each member keeps it in `ignore/{name}/envs/` and copies it to `.env`; it is never committed. `DATABASE_URL` is the pooled string and `DATABASE_DIRECT_URL` the direct one (`treklink-web/.env.example`).
- **Rejected**: local Docker until Sprint 4 (no shared data during the CO phase); coding against `production` (member migrations and seed rows would land in what becomes production); provisioning every offered service (Neon Auth duplicates the auth module, the rest has no spec); one Neon branch per member (question 40 settled one shared database).
- **Consequences**: `treklink-web` gains `neon.ts`, the `@neon/config` and `@neon/env` packages and a `.neon` ignore line; D-053 rule 6 and D-055 rule 4 carry a superseded note; the demo seed runs on the Neon `dev` branch. Verified 2026-10-24: the 8 migrations and the demo seed applied to `dev`; the backend reported the database up, signed in a seeded account and ingested 12 replayed MQTT fixtures as 12 `field_events` rows. Neon runs Postgres 18.6 while local Docker and CI run 16, so a migration that passes CI is applied to a newer server.
- **Owner**: KhoaDD.

### D-063: Password-flow rulings for US-UC09: one session rule, silent forgot cooldown, SMTP now, cooldown on the Staff trigger

- **Status**: ✅ **Resolved by the leader** (2026-10-24), in a question round on the seven defaults of treklink-docs#96 and the review of treklink-web#61.
- **Context**: LongLP built `auth` 3.1, 3.2 and the password routes of 6.1 (treklink-web#61) on seven stated defaults where the specs were silent or contradicted each other (treklink-docs#96), and added an eighth after review. The review reproduced a race: 40 concurrent wrong codes and the right one, with `auth.codeMaxAttempts` 5, ended in "Password changed" and 40 counted attempts. The backend has no request throttling; `@nestjs/throttler` was approved on 2026-09-25 and never installed.
- **Decision**:
  1. Changing the password ends every session of the account, the caller's included. api-design 08 says "every session" instead of "other sessions".
  2. Inside `auth.codeResendCooldownSeconds`, `forgot` answers 200 with the usual message and sends nothing, so a registered email cannot be told from an unknown one (FR-AUTH-05; OWASP Forgot Password Cheat Sheet, "Return a consistent message for both existent and non-existent accounts"). REQ-ERR-08 and api-design 05 drop the 429 for `forgot`.
  3. `nodemailer` is approved. LongLP builds the `smtp` transport of `auth` 1.3 before the `review-2` tag, configured by `SMTP_URL` and `MAIL_FROM`.
  4. The `console` transport is exempt from AC-06 (REQ-OPT-01). The backend refuses to start when `MAIL_TRANSPORT` is `console` and `NODE_ENV` is `production`, with a test; AC-06 carries the note.
  5. An invited member of a `CLOSED` or `REJECTED` organization who sets a password keeps it, the code is spent, and the answer is 401 `INVALID_CREDENTIALS` (D-059 rule 2).
  6. Sending a code spends the account's earlier live codes of the same purpose; only the newest works.
  7. The Staff-triggered reset (api-design 14) respects the same cooldown and answers 429 `OTP_COOLDOWN`.
  8. The Staff-triggered reset refuses a deactivated account with 409 `INVALID_STATE_TRANSITION`, because `reset` would refuse its code.
  9. The attempt limit is enforced by the database: an attempt is counted with a conditional update before the code is compared, and a `test:db` case fires more than `auth.codeMaxAttempts` concurrent wrong codes and the right one.
  10. The team SMTP account is `treklink.team@gmail.com`, authenticated by a Google app password. **[Amended 2026-10-24]** Google issues an app password only after 2-Step Verification is on (support.google.com/accounts/answer/185833), so the leader turns on 2-Step Verification with the leader's own authenticator app, holds that device alone, and creates the app password; no member signs in to the inbox. The app password reaches the team only through the team env zip (`SMTP_URL`, `MAIL_FROM`), the D-062 path, and is never committed. The account's own sign-in password is never placed in an env file. The shared team env keeps `MAIL_TRANSPORT=console`; a member switches to `smtp` locally to test delivery.
  11. Request throttling is a `platform` task for Sprint 4: a global `@nestjs/throttler` with stricter limits on the `@Public` auth routes, answering 429 `RATE_LIMITED`.
- **Rejected**: an optional `refreshToken` in the change-password body (catalog change for little gain); the 429 on `forgot` as specified (it reveals registered emails); SMTP in Sprint 4 (the leader wants real delivery in Iteration 1); masking the code in the console transport (local development could not finish a reset); refusing set-password for a closed organization (the member would need a new invitation after a reopen); several live codes (wider guessing space); no cooldown on the Staff trigger (repeated clicks flood the inbox and spend the code the user is typing); sending a code to a deactivated account; a sandbox inbox or a transactional provider for SMTP; `treklink.dev@gmail.com` as the sender (it reads as a test account); a shared authenticator key (a team password that cannot be taken back from one member); console-only delivery until Sprint 4 (the leader wants real delivery in Iteration 1); throttling inside treklink-web#61 (three items for one member before the tag).
- **Consequences**: in treklink-web#61, per D-053 rule 1, LongLP updates `specs/auth/requirements.md` (REQ-ERR-08, REQ-OPT-01 with the production guard, AC-06), `scripts/specs/endpoints/auth.py` and the regenerated api-design 05, 08 and 14. The dependency row of 2026-09-25 adds `nodemailer`. A risk row tracks the missing throttling until Sprint 4.
- **Owner**: KhoaDD.

### D-064: Account administration defaults for US-UC10 (treklink-docs#98)

- **Status**: ✅ **Resolved by the leader** (2026-10-24), accepting all six defaults LongLP stated in treklink-docs#98 for treklink-web#63.
- **Context**: `auth` 5.1 and 5.3 (TK-123) left six points open: two fields api-design 18 returns without a column, self-deactivation, repeated state changes, a missing error row, organization accounts on the account routes, and the auth-event route.
- **Decision**:
  1. `protected` in api-design 18 comes from a code constant holding `role.manage`, the only key the permission matrix marks protected; `description` is `null` until a migration adds both columns.
  2. An Admin may deactivate their own account while another Admin stays active; only `LAST_ADMIN` applies.
  3. Deactivating an inactive account or reactivating an active one answers 200 with the account unchanged, and writes no auth event and no audit row.
  4. `PERMISSION_SCOPE_MISMATCH` (api-design 16, D-057 rule 2) gets its row in auth design §4.
  5. `PATCH`, `deactivate` and `reactivate` on the account routes answer 404 for an organization account; its Manager handles it through `organizations`.
  6. `GET /api/auth-events` (api-design 17, UC-58) is not part of treklink-web#63.
- **Rejected**: a migration adding `description` and `protected` before the `review-2` tag (schema churn for a read-only field); forbidding self-deactivation (no rule needs it while `LAST_ADMIN` holds); 409 on a repeated state change (a retried click would show an error for a state the user wanted).
- **Consequences**: in treklink-web#63, per D-053 rule 1, LongLP adds the §4 row and states rules 2, 3 and 5 in api-design 11 and 12. A later migration adds the two `Permission` columns, filled by `build_seed.py`.
- **Owner**: KhoaDD.

### D-065: Graded reports draw their diagrams in PlantUML; Mermaid stays for repository specs

- **Status**: ✅ **Resolved by the leader** (2026-10-24), after the supervisor meeting of 2026-10-24 (`capstone/Documents/meetings/Supervisor Meeting 2026 10 24 091511.txt`).
- **Context**: Mr. Duc rejected the report diagrams as not following notation: the context diagram merges each actor's inflow and outflow into one bidirectional arrow, the use case model is split over about ten figures instead of one overview on an A4 page, the architecture diagram does not separate frontend, backend and third parties, and the ERD's crow's-foot style was unfamiliar. The course handbook `Documents/templates/Cam-nang-tranh-loi-Capstone-SE.pdf` §2 grades eight diagram types on notation. The SRS use case figures are Mermaid `flowchart`s with rectangles for actors, and the context diagram merges two entities into one box, which §2.6 forbids.
- **Decision**:
  1. Every diagram in a graded report (Reports 1 to 7, the Design Brief, review decks) is PlantUML source rendered by the PlantUML jar, kept next to the report as `.puml`.
     **[Amended 2026-10-25]** Except activity (swimlane) and state machine diagrams, which are Mermaid first (`swimlane-beta`, `stateDiagram-v2`), rendered by the pinned `mmdc` with Mermaid 12.0.0 (`capstone/scripts/srs/render_figures.sh`). An activity diagram may also be PlantUML; a state machine falls back to PlantUML only when Mermaid cannot draw it. The leader ruled after comparing ten demo figures drawn in both tools (`capstone/Documents/reports/assets/puml/review/`): Mermaid drew the ERD crow's foot as the curved leaf the supervisor rejected, put filled heads on `include` arrows and tangled the architecture, so use case, class, sequence, ERD, context and architecture stay PlantUML.
     **[Amended 2026-10-26]** The tool per diagram type, ruled by the leader after the 2026-10-25 grill on the
     comparison renders (`capstone/Documents/reports/assets/puml/review/compare/`): **PlantUML** for context,
     use case, class, ERD and physical schema, activity (swimlane), architecture, deployment, IoT hardware and
     package diagrams; **Mermaid** for state machines. **Sequence diagrams stay Mermaid for now**: every SDD
     sequence is also rendered in PlantUML (`capstone/Documents/reports/assets/puml/review/sequence-trial/`),
     and the leader picks one tool for all of them at final delivery. The context diagram stays PlantUML
     because its process now renders as a true circle (`capstone/scripts/srs/render_puml.py` redraws the
     ellipse PlantUML 1.2026.9 always draws for a `usecase`). Large figures may use `!pragma layout elk`,
     which needs Java 21, except an ERD. **ERDs are not drawn by PlantUML** (leader review 2026-10-26): the leader requires straight
     orthogonal lines, no curves or diagonals, and a jump where two lines cross. Graphviz `ortho` shares tracks and
     drifts labels, PlantUML's ELK adapter exposes no spacing, and neither draws jumps, so an ERD keeps PlantUML's
     entity syntax and is drawn by `capstone/scripts/srs/render_erd.py` (elkjs layered layout, orthogonal routing,
     one port per line end, SVG and jumps drawn by the script). Rejected: Graphviz polyline (diagonal lines). The leader vets each ELK render. No figure carries a
     legend or an explanatory note; the document's text or notation table explains the notation. The shared style's fonts rise to 16 px (labels
     15 px) so wide figures stay closer to the 7 pt floor of chapter 13 §4.1. Visual Paradigm is not used.
  2. Mermaid stays the diagram language of `treklink-docs` and `treklink-web/specs` (chapter 13); a spec diagram is not copied into a report as Mermaid.
  3. Before the Review 2 package (2026-10-26), every report figure is redrawn and checked against handbook §2 for its type: the context diagram with one arrow per direction per entity, nouns as flow labels and no merged entities; one use case overview with CRUD folded into `Manage X`, the per-flow diagrams kept as detail; the architecture with frontend, backend and every third party as separate blocks and both request and response paths, plus the IoT hardware diagram with specifications and protocols; one overall ERD in one notation with its legend; sequences numbered, with activation bars, `:Object` names, named pages and two-lane `alt` boxes.
- **Rejected**: keeping Mermaid and fixing content only (no stick-figure actors, `include` and `extend` or activation styling the reviewers recognise); Modelio or Umbrello (hand-drawn binary models, not regenerable); Enterprise Architect under Wine (paid after the trial, hand-drawn); fixing only the three figures named in the meeting (the ERD and sequences would carry known handbook violations into the review).
- **Consequences**: chapter 13 §1 carries the exception. The SRS and SDD figure build moves from `.mmd` to `.puml`. **[2026-10-26]** Report 4 is rebuilt: 30 figures in PlantUML (context, architecture, deployment, IoT hardware, package, overall ERD, nine physical schema parts, five activity diagrams, ten class diagrams), 8 state machines and 42 sequences in Mermaid. Chapter 16 §2, §6 and §7 and `AGENTS.md` §2.8 and §4 follow the amendment. Report 3's figure swap reuses the same `.puml` sources.
- **Owner**: KhoaDD.

### D-066: Five main flows run their happy path end to end by Saturday 2026-10-31

- **Status**: ✅ **Resolved by the leader** (2026-10-24), on the supervisor's demand of 2026-10-24.
- **Context**: at the 2026-10-24 meeting the team could not demo anything; Mr. Duc required all five main flows runnable by the weekend of 2026-10-31. On 2026-10-24, 44 of 209 tasks were ticked and `organizations`, `rentals` and `billing` had no code.
- **Decision**:
  1. By Saturday 2026-10-31 each of MF-01 to MF-05 runs its main success scenario through the real screens and the real API on the seed data. Alternate and exception paths wait.
  2. The leader and the agent own the documents and diagrams (D-065) and review every PR the day it opens; the four members own the code, one or more flows each, end to end.
  3. The per-flow cut list and lane plan are published as a session file before Monday 2026-10-26.
- **Rejected**: every step and alternate of each drawn flow by 2026-10-31 (not reachable with 165 tasks open); asking the supervisor to restate the bar first (costs a day).
- **Owner**: KhoaDD.

### D-067: Every diagram and spec passes the handbook gate: check, look, cross-check

- **Status**: ✅ **Resolved by the leader** (2026-10-24), a standing instruction after the supervisor meeting of 2026-10-24.
- **Context**: the diagrams the supervisor rejected broke rules the course handbook `capstone/Documents/templates/Cam-nang-tranh-loi-Capstone-SE.pdf` states plainly (§2.1, §2.6). Agents generated report figures and specs without re-reading it, checked the source but rarely the rendered image, and did not compare figures with each other, so notation and naming drifted between documents.
- **Decision**:
  1. Before writing or editing a diagram, or a spec or report section a diagram is drawn from, the author re-reads the handbook sections for that artifact (chapter 13 §1.1 table), from the PDF, every time.
  2. The rendered image is looked at before the figure is done: by the agent when it has image input, otherwise by a member.
  3. The figure is cross-checked against the other figures, the SRS and SDD text, `schema.prisma`, the module `design.md` and the code paths it claims.
  4. The PR body or session file records, per figure, the sections re-read, who looked at the render and what it was cross-checked against. A figure without that record is sent back in review.
  5. The rule is in `AGENTS.md` §2.8 in all five copies, so every agent loads it at session start.
- **Rejected**: a one-time audit before Review 2 only (the drift returns with the next generated figure); relying on source review (layout faults exist only in the render); copying the handbook into the repository (it is course material; the PDF stays the source and chapter 13 keeps a short paraphrase).
- **Owner**: KhoaDD.

### D-068: The Field Station is part of the system, not an actor

- **Status**: ✅ **Resolved by the leader** (2026-10-25), during the D-065 redraw.
- **Context**: the SRS said the Field Station is TrekLink software "inside the boundary", but Table 11 listed it as an actor and UC-26 and UC-27 named it as their actor; the old context diagram drew it outside the system process. A UML actor is outside the system by definition, so the three statements could not all hold, and handbook §2.6 and §1.5 grade diagrams that disagree with each other.
- **Decision**:
  1. The Field Station and the MQTT broker are inside the system boundary. Neither is an actor or an external entity.
  2. The TrekLink Device is the external actor of UC-26 Ingest Field Event and UC-27 Flush Offline Queue; UC-28 keeps the Org Operator.
  3. SRS Table 11 drops the Field Station row and renumbers; Table 12 and the UC-26 and UC-27 specifications name the TrekLink Device; §2.1 explains why the Field Station is not an actor.
- **Rejected**: the Field Station as an external secondary actor (it is TrekLink's own executable, shipped and versioned with the platform, and the context diagram would show part of the system as outside it).
- **Owner**: KhoaDD.

### D-069: UML modeling rules for every PlantUML diagram (chapter 16)

- **Status**: ✅ **Resolved by the leader** (2026-10-25), after rejecting the first PlantUML use case overview.
- **Context**: the first PlantUML use case overview had no actor generalization and put actors above and below the system boundary. The agent had drawn without a rule set saying what each diagram type may contain and where each element goes, so layout was decided by trial renders. D-067 checks a figure against the handbook, but the handbook lists mistakes, not a full notation and layout standard.
- **Decision**:
  1. Chapter 16 is the rule set for every PlantUML diagram: each rule tagged with its source (course handbook, the UML 2.5 specification, Ambler's *The Elements of UML 2.0 Style*, Wiegers and Beatty, the PlantUML reference, or a TrekLink choice), and a skeleton per diagram type in `_docs/02-templates/puml/` with a shared monochrome style. Each skeleton was rendered and inspected on 2026-10-25.
  2. The actor tree is `User` (abstract) with `Organization Member` (abstract) above `Org Operator` above `Org Manager`, and `TrekLink Employee` (abstract) above `TrekLink Staff` above `TrekLink Admin`. `Guest` stays outside the tree. Actors have no aggregation; organization membership is shown in the class diagram and the ERD.
  3. A sequence diagram shows one use case's main success path plus at most one `alt` for the failure its specification names; every other branch is in the activity diagram.
  4. The ERD notation is crow's foot (IE), drawn with orthogonal lines and square corners so each foot is three straight strokes ending on the entity border.
  5. Training material the leader holds in confidence informed some rules; it is not cited, quoted or stored in any repository, and the rules it alone supports are stated as TrekLink choices.
- **Rejected**: Chen notation for the ERD (PlantUML's Chen syntax not verified, and the course accepts either); every exception as an `alt` in the sequence (unreadable, and the activity diagram already carries the branches); no `alt` at all (the handbook asks for exception paths); a section of chapter 13 instead of a new chapter (mixes notation with print layout).
- **Owner**: KhoaDD.

### D-070: The commit model check is an explicit allowlist with the variant sealed

- **Status**: ✅ **Resolved by the leader** (2026-10-25). Amends D-054 rules 4 and 5.
- **Context**: the leader saw every pull request pass the Commit Checksum check and asked whether it compares values. An audit of `tk_checksum.py` on 2026-10-25 confirmed the AES-GCM seal works (a token edited, moved to another subject or pushed by another member fails), and found the model check unsafe: approval was `(major, minor) >= floor` per family, so `claude-opus-9-9`, `claude-fable-7`, `gpt-9-9` and `gpt-5-7` passed; the token stored no variant, so `gpt-5-6-luna` and `gpt-5-6-terra` were sealed as plain `gpt-5.6` and passed, and Gemini 4 Argon was sealed as "gemini-flash 4.0"; a restricted model failed only on `feat`, `fix` and `hotfix`, so it passed on `refactor` and `test`. Every commit then on `dev` and in open pull requests declared Claude Opus 5.5, Claude Sonnet 5.5 or 5, or GPT 6, all approved under either rule, which is why everything passed.
- **Decision**:
  1. The allowlist names each model: Claude Opus 4.6, 4.7, 4.8, 5, 5.5; Claude Sonnet 4.6, 4.8, 5, 5.5; Claude Haiku 5, 5.5; GPT 5.6 Sol, 5.6 Cyber, 6, 6 Sol, 6 Luna, 6 Astra, 6.1 Sol; Gemini 4 Argon. It lives in chapter 11 §2.1 and in `ALLOWLIST` of `tk_checksum.py`, edited together. No version comparison: a later model fails until it is added.
  2. Ingest only, failing on every commit whatever its type: Gemini 3.8 Flash, GPT 5.6 Luna, GPT 5.6 Terra. Every model not listed fails as well.
  3. Claude Fable is approved at every version, the one family-wide entry, by the leader's choice.
  4. A commit with no `Checksum` trailer, or an empty one, is a manual commit: a member typing by hand never sets a model. It gets the `provenance-review` label for a review by hand, and the check passes, as D-054 rule 4 already said. Bot and merge commits stay exempt. AI attribution (D-049) stays a label.
  5. The hook writes token format tk2 (66 hex), which seals the variant with the model. A tk1 token (64 hex) still verifies; when its family and version need a variant to decide (today only `gpt-5.6`), it is labelled for a manual audit instead of failing.
  6. `tk_checksum.py selftest` checks every list entry, the near misses and the token rules offline; run it after any change to the list.
- **Rejected**: keeping the version floors (a future or unvetted model passes silently); listing Fable versions one by one (the leader allows the whole family); failing a commit with no trailer (a manual commit carries none, and members do not set a model by hand); failing every tk1 token (forces every member onto the new hook at once, for no gain on the models in use); passing a tk1 `gpt-5.6` token (reopens the Luna and Terra hole).
- **Consequences**: `treklink-docs/.github/scripts/tk_checksum.py`; chapter 07 §3.6; chapter 08 §3.1; chapter 11 §2.1, §2.2 and §2.4; the five AGENTS.md copies §6. Members pull `treklink-docs` `dev` so their hook writes tk2. The check's member-key and subject binding is unchanged; a commit with the identical subject would accept the same token, because the seal does not cover the diff.
- **Owner**: KhoaDD.

### D-071: The live map uses the CyclOSM style, for terrain (amends D-031)

- **Status**: ⛔ **Superseded by D-072** (2026-10-27). Resolved by the leader 2026-10-26.
- **Context**: the plain OpenStreetMap style draws no contour lines or hillshading, and trekking staff read slope, ridges and valleys from the map. The leader asked for a terrain map before Review 2 and pointed at the CyclOSM style. A tile comparison over the default viewport (11.6°N 108.5°E, zoom 13) confirmed it: CyclOSM draws contours, hillshading, streams and forest cover.
- **Decision**: the three map parameters change to provider `cyclosm`, tiles `https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png` and attribution `© OpenStreetMap contributors, style CyclOSM, tiles by OpenStreetMap France` (treklink-web `scripts/specs/catalog.py` and a forward migration, because the seed is already applied, D-036). Leaflet, the endpoint and the sovereignty overlay stay as D-031 set them. CyclOSM is hosted by OpenStreetMap France under a fair-use tile policy with no key (<https://www.cyclosm.org>); the D-031 usage rules carry over: attribution on the map, no bulk prefetch, no offline caching for the Field Station.
- **Sovereignty**: CyclOSM draws OpenStreetMap data, so its base labels over the archipelagos are the same as OpenStreetMap's. TC-24 was re-run on 2026-10-26 with the overlay present over both; the screenshots are in `capstone/Documents/evidence/map-sovereignty/` (`2026-10-26-cyclosm-*.png`). R11 keeps its D-031 standing: accepted within educational scope, no public deployment.
- **Rejected**: OpenTopoMap (it also draws terrain, but it is not the style the leader chose); Thunderforest Outdoors and Tracestrack Topo (need an API key held in the browser); keeping the plain OpenStreetMap style (no terrain).
- **Consequences**: treklink-web `scripts/specs/catalog.py`, `specs/platform/configuration-matrix.md`, `specs/monitoring/api-design/01-get-map-config.md` and migration `20261026170000_map_cyclosm_terrain` (treklink-web#83). An Admin can still change the three values through the parameters API.
- **Owner**: KhoaDD; LongNN (monitoring).

### D-072: The live map offers switchable keyless basemaps, OpenTopoMap by default (supersedes D-071)

- **Status**: ✅ **Resolved by the leader** (2026-10-27).
- **Context**: CyclOSM (D-071) serves no tile above zoom 13 over Vietnam. On 2026-10-27 every subdomain answered HTTP 404 at zoom 14 to 17 over the default viewport (11.56°N 108.54°E), while the same zooms loaded over Paris; zooming in replaced the map with MSG33. The leader asked for several topographic maps instead of one.
- **Decision**:
  1. The live map offers four basemaps in a Leaflet layer control, none needing a key: Topographic (OpenTopoMap), the default; Terrain (Stadia Stamen Terrain); Topographic (Esri World Topo); OpenStreetMap.
  2. `monitoring.mapBasemaps` holds the list (id, name, tile URL, attribution, `maxZoom`, `maxNativeZoom`) and replaces `monitoring.mapTileUrl` and `monitoring.mapAttribution`; `monitoring.mapProvider` names the default entry. `GET /api/map/config` returns the list and still describes the default in `provider`, `tileUrl` and `attribution`.
  3. `maxNativeZoom` is the deepest zoom each provider drew over the default viewport on 2026-10-27: OpenTopoMap 17, Stadia 18, Esri 16, OpenStreetMap 19. Above it Leaflet enlarges the deepest tiles up to `maxZoom` (18; OpenStreetMap 19), so no zoom requests a tile that does not exist.
  4. The sovereignty overlay is drawn on every basemap and is never in the layer control (D-031, BR-30).
- **Sovereignty**: TC-24 re-run on 2026-10-27 for all four basemaps over both archipelagos; the overlay is present on each. Three basemaps draw OpenStreetMap-derived data and carry its foreign labels beneath the overlay; Esri showed no foreign archipelago label at zoom 7, other zooms not checked. Evidence: `capstone/Documents/evidence/map-sovereignty/2026-10-27-*.png`. R11 keeps its D-031 standing: accepted within educational scope, no public deployment.
- **Usage terms (unverified in detail)**: OpenTopoMap and OpenStreetMap run volunteer servers under fair-use policies; Stadia accepts keyless requests from localhost, and a deployed domain needs a Stadia account; Esri's terms for World Topo Map were not reviewed. Re-check all four before any deployment beyond the course.
- **Rejected**: keeping CyclOSM (empty above zoom 13 here); CyclOSM enlarged past zoom 13 (blurry exactly where trekkers zoom); providers that need a key in the browser (Thunderforest, Tracestrack, MapTiler).
- **Consequences**: treklink-web#88: `scripts/specs/catalog.py`, the configuration matrix and parameter registry, migration `20261027090000_map_basemaps`, `LiveMapService`, `LiveMapWidget`, api-design 01, monitoring REQ-UBI-02, frontend REQ-UBI-06.
- **Owner**: KhoaDD; LongNN (monitoring and frontend lane).

### D-073: Review 2 field-side rulings: device first, relays are rented nodes the organization places, no SIM master node, register Context from the approved slide (amends D-033 rule 8)

- **Status**: ✅ **Resolved by the leader** (2026-10-28).
- **Context**: Review 2 (2026-10-27), panel note `capstone/Documents/feedback/Note-review2.txt`. The panel approved the Context on slide 2 of the Canva deck "Treklink Review 2" (DAHZFEHnKsU) and asked that the registration form carry it unchanged. It asked the team to stop leaning on phones and the Meshtastic phone app, to say who pays for and who installs relays, and suggested a master node with a SIM card. The adjusted form (`topics/Phieu_FA26SE159_adjusted_2026-10.md` §3.2 a) still names three routes (Tà Năng–Phan Dũng, Tả Liên Sơn, Bạch Mộc Lương Tử), while the approved context covers every organization nationwide.
- **Decision**:
  1. **Register Context**: §3.2 a) of the adjusted form takes the slide 2 text word for word, grammar fixes only, and drops the route names.
  2. **Device first** (amends D-033 rule 8): a device holder works the device itself (SOS button, screen, preset messages) and needs no phone and no TrekLink account. The stock Meshtastic app is mentioned only as an optional backup, never as the holder interface.
  3. **Relays are ordinary rented nodes.** Any rented node can run in the Meshtastic relay role. The nodes have no solar supply, so a relay is a temporary checkpoint: the organization's staff place it on site for an operation and retrieve it. It is part of the same contract at the normal per-device price; TrekLink installs nothing on site. A node not returned at the end of the contract is a loss under D-033 rule 4.
  4. **No SIM master node.** Phones stay the backup uplink for the Field Station, since one LTE plan covers a whole team.
- **Rejected**: a separately priced relay kit (new billing rule and variant for no new capability); permanent relays installed by TrekLink (no solar, no maintenance model); a SIM master node (new device development, SIM allocation and SIM management do not fit the remaining term); keeping the stock app as the holder interface (contradicts the panel).
- **Files moved** (2026-10-28): the registered form `topics/Phieu_FA26SE159.md` and the pre-registration draft `topics/Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.md` with its two .docx files now live in `topics/.deprecated/`; older entries in this register cite their former paths. The style template `topics/docx/Phieu_FA26SE159.docx` stays in place.
- **Grammar fix confirmed** (2026-10-29): the slide's "with room of potential" reads "with room for growth" in the register, confirmed by the leader under rule 1. The Review 2 submission carries the register as .docx and .pdf, clean and highlighted, with BM03 appended to each PDF; `topics/pdf/` holds the register-only PDFs.
- **Consequences**: adjusted form §3.2 a) and BM03 Record of Changes; SRS context, constraints and the field-side narrative; the scope disclaimer on connectivity loss (still to be ruled). The 2026-10-02 field-test risk row ("plan a repeater node as optional equipment") now reads as rule 3.
- **Owner**: KhoaDD.

### D-074: Organizations group their rented devices; the platform offers generic grouping, not trips (amends D-033 rule 3)

- **Status**: ✅ **Resolved by the leader** (2026-10-28).
- **Context**: Review 2 asked for tours or journeys so holder data can be attached, and gave a case: an organization rents 20 devices on one contract, sends 12 to one site and 8 to a distant site, each with its own group and chat channel, and a site may split into smaller groups. D-033 rule 3 excluded trips, and `schema.prisma` has no group model; devices hang only off contracts. Too specific a feature (tour trips) draws the panel's scope objection; too little leaves the gap it named.
- **Decision**:
  1. **Generic Group.** An organization creates groups with a name, an optional free-text label (for example "ranger patrol", "tour"), optional dates and an optional area note. TrekLink models no trip, tour, booking or customer; the label lets each organization fit groups to its own purpose.
  2. **One sub-level in business rules, unlimited in the data model.** A group may hold subgroups one level down. The two-level cap is a business rule held in configuration; the entity is self-referencing so a later term can lift the cap without a schema change.
  3. **Membership across contracts.** A group draws from every device the organization currently holds, across its contracts. A device sits in at most one group at a time and leaves it when it is returned.
  4. **Holder data**: per assignment, a holder display name and one free-text field. No holder accounts.
  5. **Platform grouping first.** Groups filter the live map, alerts and reports; every device still shares the organization's channel. Per-group mesh channels synced from the platform (through the Field Station over USB serial, or over the mesh) are a later stage, attempted only if time allows, and need firmware work (D-008). Since separate sites are out of radio range of each other, a shared channel is an accepted trade-off until then.
- **Rejected**: keeping D-033 rule 3 and only explaining it (the panel asked directly); full tour management (contradicts the device-rental scope and the title); groups bound to one contract (breaks the second-contract case); holder name plus emergency contact fields (the leader chose one free-text field).
- **Consequences**: new `Group` entity and assignment in the ERD and `schema.prisma`; Org Manager screens; SRS use cases; the live map and alert filters. Per-group channels, if attempted, touch D-021 key provisioning and the firmware.
- **Owner**: KhoaDD.

### D-075: Review 2 scope rulings: connectivity disclaimer and operating envelope, Field Station at a fixed base point, a rented-device console for the Org Manager, plan prices and events in the register

- **Status**: ✅ **Resolved by the leader** (2026-10-28).
- **Context**: Review 2 panel note (`capstone/Documents/feedback/Note-review2.txt`): what happens when every link is cut, the three loss cases (out of range, dead battery, unheard SOS), what GPS is for, how the laptop is used, product management for the Org Manager, and a price table with rules and events per rental package.
- **Decision**:
  1. **Disclaimer up front.** The register scope opens with a short disclaimer: TrekLink is a supplementary safety and coordination tool that works within mesh range of a node, a relay or the Field Station; it is not a guaranteed rescue link.
  2. **Operating envelope in the SRS**, one table: (a) out of range: the device keeps beaconing and its on-device queue (D-018) delivers once a node or the Field Station hears it; (b) dead battery: the organization gets a stale-device alert with the last known position and the trail, and nothing after that; (c) unheard SOS: the device repeats until heard and the platform raises a suspected episode from the beacon cadence (REQ-EVT-06); plus the rain, ridge and indoor limits of the 2026-10-02 field test. Each row states what the device does and what it cannot.
  3. **GPS** fixes the position on the device and shares it over LoRa only. There is no satellite uplink.
  4. **Field Station at a fixed base point.** The laptop stays at a base point the organization picks (basecamp, vehicle, ranger station, trailhead) with one rented node on USB serial. It reaches groups through the mesh and relay checkpoints (D-073 rule 3) and uploads over any internet it finds, site Wi-Fi or a phone hotspot; offline, it queues (D-068).
  5. **Rented-device console for the Org Manager**: every device the organization holds across its contracts, with variant, asset tag, status, battery, last seen, group and holder (D-074). From it the Manager assigns devices to groups, reports a fault or a loss, and gives return notice. Devices still enter the fleet only through TrekLink Staff intake and reach an organization only at counter handover (D-033 rules 1 and 5).
  6. **Register price table and plan events.** The register gains a compact table marked as configurable sample values, taken from the existing seed and parameter registry, not new figures: monthly price per variant (`seed-demo.ts`: v2 400,000, v3 450,000, v4 480,000 VND), day-plan rate as monthly divided by 30 times `billing.dayPremium` (1.5), day-plan lengths `rentals.dayPlanLengths` (3, 4, 7), `rentals.minOrderQuantity` (5), `billing.holdingFeeRatio` (0.5), `billing.lateFeePerDevicePerDayVnd` (50,000), `billing.damageApprovalThresholdVnd` (500,000), loss at remaining value. It also lists events per plan: monthly (open with holding fee, term close, renewal, notice, final close); day (payment at handover, due date, late, return).
- **Rejected**: the disclaimer in the SRS only (the panel asked for it up front); a laptop carried with the group (the case the panel mocked); a laptop placement left to the organization (weaker answer); an organization-owned product catalog (TrekLink is the only asset owner); rules without prices (the panel asked for prices).
- **Consequences**: adjusted form (scope disclaimer, price table, Field Station wording, BM03); SRS operating envelope, Org Manager use cases and screens; architecture and use case diagrams to be redrawn under D-069; the IoT hardware drawing (power, screen, ports, principle) is a separate figure still to be planned.
- **Owner**: KhoaDD.

### D-076: Firmware variant identity and the treklink-firmware documentation layout

- **Status**: ✅ **Resolved by the leader** (2026-10-29).
- **Context**: `treklink-firmware` used "v3" and "v4" for two different things. Its code, `README.md` and variant specs mean the LilyGo T-Beam v1.2 and T-Beam Supreme (`variants/esp32/treklink_v3_tbeam/`, `variants/esp32s3/treklink_v4_supreme/`), while `.kiro/specs/roadmap.md` described v3 and v4 as custom pre-production PCBs and v5 as mass production. Its documentation was spread over `.kiro/specs/`, `.kiro/docs/`, `.kiro/guidelines/`, `.agents/rules/`, `_handoff/`, `docs/` and a 2615-line root `specifications.md` that is a drafting prompt plus a pasted methodology. `docs/commit-rules.md` allowed `dev/<username>-<feature>` branch names that chapter 07 does not, and `.agents/rules/save-your-tokens.md` imposed the compressed reply register that D-043 retired.
- **Decision**:
  1. **v3 is the LilyGo T-Beam v1.2 and v4 is the LilyGo T-Beam Supreme.** `treklink-firmware/docs/variants.md` is the single source for what each variant is. The custom-PCB tier roadmap is deprecated.
  2. **v1 is deprecated.** It still builds (`treklink`) and works as a mesh node; treklink-web does not cater for it, because its image compiles MQTT out (D-005). v1's requirements stay the base set the v2 to v4 specs carry forward.
  3. **Layout** (option A of the 2026-10-29 audit): one spec root, `specs/` (`variants/v1` to `v4`, `variants/shared`, and module folders `onboard-queue`, `sos`, `fall-detection`); `docs/` for the variant matrix, build and flash, coding conventions, hardware records, roadmap, dated hardware test runs, closed work records, and `docs/.deprecated/` with a reason per item. Rules: chapter 09 §1.1.
  4. **Nothing is deleted.** Every moved file goes through `git mv`; superseded and wrong documents go to `docs/.deprecated/YYYY-MM-DD-<slug>/`.
- **Rejected**: the full `docs-scaffold` layout (`10-context` to `90-meta`), strongest drift detection but the only repository shaped that way; a minimal cleanup that keeps two spec roots; keeping the specs in `.kiro/specs/` for Kiro IDE, which the team no longer uses; renaming the LilyGo envs so v3 and v4 could stay roadmap tiers (touches env names and flash instructions for no gain).
- **Consequences**: `04-firmware-ground-truth.md` §5 marks v1 deprecated; chapter 09 §1.1 brings `treklink-firmware` into scope; the firmware restructure lands as one `docs/*` PR there. Hardware-verified status is now recorded per behaviour in `treklink-firmware/docs/test-runs/`.
- **Owner**: KhoaDD.

## Risk register (carried from FA26SE159, kept live)

| Risk | Likelihood | Impact | Mitigation | Status |
|---|---|---|---|---|
| Insufficient physical TrekLink devices | Medium | High | Simulate Gateway→Cloud load via MQTT scripts; simulation never substitutes for LoRa RF reliability claims | Open |
| Gateway sync latency exceeds 5s NFR | Medium | Medium | Tune MQTT QoS, reduce payload size, backpressure on queue flush | Open |
| RQ3 baseline not objectively measurable | High | Medium | Randomized simulation drills; independent observer triggers SOS, records timestamp; participants unaware of exact trigger time | Open |
| NestJS + MQTT + WebSocket integration underestimated | Medium | High | PoC gateway→backend integration in TP1 Week 2, not deferred to TP3 | Open |
| Firmware message schema incompatible with new gateway | Low | High | Schema frozen & documented in TP1 before any gateway implementation | Open, tracked as TP1 exit gate |
| **[Added 2026-10-18, D-048]** The SEP490 syllabus sends the team to the second defence round if it completes less than 75% of the use case functions or screens submitted in Report 3 at the end of week 3, or fewer than 20 medium use cases (3 to 7 transactions). The SRS now lists 65 use cases, so 75% is 49. The week 3 draft committed on 2026-09-27 (`capstone` 4a7a135) lists 58 use cases under the pre-D-033 booking scope; which version the supervisor holds as the week 3 submission is unverified | High | Critical | Week 3 set mapped to today (D-051): the 44 `baseline` use cases deliver 51 of the 58 week 3 use cases; 44 of 58 is the floor. Task lists and the Coverage Matrix track the baseline flag | Open |
| **[Added 2026-10-21, Project Tracking]** Commit evidence from 2026-09-01: KhoaDD 203 commits; LongLP 6, HoangTK 3, LongNN 2, TanNB 0 across the five repositories. Review 2 part 5 and Defense 1.1 verify each member against their own repository work; the study phase (D-052) explains part of the gap | High | High | Every member commits their screen designs from 2026-10-21 and their story code from 2026-10-23 under their own GitHub account, sealed (D-054); Project Tracking is regenerated before submission by `capstone/scripts/srs/build_tracking.py` | Open |
| **[Added 2026-10-20, Review 2 guide]** The course's Review 2 guide requires Iteration 1 code, tests and CI under the tag `review-2`, Project Tracking among the submissions, and the AI tools, models and stages declared in Report 4 (guide §3, §10). Software Package 1 is not built; D-050 dropped the Project Tracking workbook; D-049 removes AI attribution from commits. An undeclared or disguised AI marker would contradict guide §10, which also penalises concealment in the self-review | High | High | Code Iteration 1 from 2026-10-22; restore a Project Tracking deliverable; declare AI use in Report 4 §technology; the commit Checksum trailer (D-054) is documented in chapter 07 §3.6 and declared in Report 4 | Open |
| **[Added 2026-10-23, gateway-sync 1.2]** The MQTT "golden" fixtures that drive the MF-02 replay are synthesized from `MeshPacketSerializer.cpp` and `TrekLinkSOSHelper.h`, not captured from real v2, v3 and v4 devices (treklink-web#55). A difference between the serializer source and what a flashed node actually publishes (a member name, the channel name in the topic, the telemetry variant) would pass every test and fail on hardware | Medium | High | Capture one publish of each fixture type from a real node on the local Mosquitto before Sprint 4 and replace the files, putting the captured node numbers on TL-0009 and TL-0010 of the demo seed in the same change; state at Review 2 that the Iteration 1 replay uses synthesized fixtures | Open |
| **[Added 2026-10-24, treklink-web#61 review]** The backend has no request throttling. The one-time-code race (D-063 rule 9) let 40 concurrent guesses through a limit of 5; the database fix closes that hole, but nothing limits request volume on `forgot`, `reset`, `set` or `login`, which OWASP's Forgot Password Cheat Sheet asks for | Medium | High | `platform` task for Sprint 4: global `@nestjs/throttler` with stricter limits on the `@Public` auth routes (D-063 rule 11); until then the per-account cooldown and the database-enforced attempt limit bound guessing per code | Open |
| **[Added 2026-10-24, treklink-web#63 review]** `PermissionCache` (`auth` 4.1) keeps permission rows until an in-process `policy.changed` event. Since D-062 several members run their own backend against the shared Neon `dev` database, and the staging plan of D-055 rule 4 may run more than one instance, so a permission change made through one backend leaves every other one on stale rules until it restarts (AC-03 holds only on the instance that made the change) | Medium | Medium | Before Sprint 4 staging: a cache TTL as a parameter, or a version read from the database on each policy check, or a Postgres `LISTEN`/`NOTIFY` on `policy.changed`; until then, restart a local backend after changing role permissions on the shared database | Open |
| Scope creep | High | Medium | Feature freeze after TP5 Week 10; anything else goes to post-capstone backlog | Open |
| ~~ORM indecision stalls TP3 start~~ | Medium | Medium | D-001 resolved (Prisma) ahead of the Week 4 target | **Mitigated** |
| **[Added]** Field connectivity may need phone-based bridging instead of a dedicated Gateway node (D-005) | Medium | High | Validate dedicated Gateway (Wi-Fi/cellular node, native Meshtastic MQTT module) in TP1 PoC before committing to it; mobile-app forking treated as out of scope given no macOS/Xcode access | **Mitigated**, D-005 resolved as a staged rollout (Stage A node-MQTT, Stage B basecamp bridge); app forking formally rejected |
| **[Added]** ~~NestJS is a skill only for Khoa~~, **corrected Session 6.** The enrolment framework codes show **LongLP and HoangTK are both `BIT_SE_NJS_18D` (Node.js)**; NestJS is a framework over Node and is treated as covered by that training. Backend capability is therefore **3 of 5**, not 1 of 5. Residual exposure is the two IC-track members (LongNN, TanNB) picking up backend stories solo | Low | Medium | Ramp LongNN and TanNB on `01-conventions/05-backend-conventions.md` module conventions during W2–W5, mentored by Khoa/LongLP. Lane assignment already routes core backend to the two NJS-track members. This is the substance of the Report 2 §2.3 Training Plan | **Downgraded** (Session 6) |
| **[Added S3] SOS is announced by exactly one unacknowledged text packet.** `TrekLinkSOSHelper::triggerSOS()` sends the `"SOS - …"` text once with `want_ack = false` (`TrekLinkSOSHelper.cpp:157–160`); `tickBeacon` then retransmits **position only**. If that single text frame is lost over RF, the episode is invisible to the backend, the beacons that follow look like routine position reports. | Medium | **Critical** | **Two layers, per D-008.** *Platform side (built now)*: cadence-anomaly detector, the beacon runs 5s for the first minute then 30s (`TrekLinkSOSHelper.cpp:181`), far denser than routine reporting, so ≥N positions in window W raises a *suspected* episode at lower confidence (REQ-EVT-06, `design.md` §2.4). *Firmware side (now available, preferred)*: retransmit the SOS discriminator with each beacon, and/or set `want_ack`, and/or introduce a real custom PortNum so SOS stops depending on a `printf` string. The platform mitigation is defence-in-depth and should be kept even after a firmware fix. | Open, **firmware fix candidate #1** |
| **[Added S3]** Stage A (node MQTT, D-005) has no offline buffer, so charter §5's offline-recovery and priority-ordering NFRs and RQ1/RQ2 cannot be evaluated until Stage B lands | High | Medium | **Stage B is permanent scope** (D-005 closed, Session 6), it is the substance of supervisor-specified **MF-02** (D-016), so it cannot be traded away. Residual risk is now schedule, not scope: Stage B must land early enough for RQ1/RQ2 evaluation in W9–W12. Do not present Stage A as satisfying the offline NFR at any point. **Further reduced (Session 7, D-018)**: the buffer work is now split, and the *smaller* half, the on-device queue, is sequenced first and needs no basecamp hardware, so a usable offline buffer exists well before the basecamp gateway (now Stage C) is built. | Open, **schedule risk only**, scope question closed, exposure reduced by D-018 |
| ~~**[Added S3]** `treklink_v1_0` compiles MQTT out, so v1 units cannot act as the Stage A uplink node~~ | Medium | High | v1 is **out of the demo set** (team lead, Session 3), Stage A targets v2/v3/v4, all of which leave MQTT compiled in and carry Wi-Fi silicon. Were v1 ever needed, removing `-D MESHTASTIC_EXCLUDE_MQTT=1` is a one-line build-flag change now that D-008 permits it. | **Closed** |
| **[Added S3]** Stage A's JSON MQTT path omits `MeshPacket.priority`, making the SOS position packet indistinguishable from a routine one (D-007) | High | Medium | Backend episode correlation with a backward grace window (`design.md` §2.4). Two upgrades now available: switch to the `/2/e/` protobuf topic to recover `priority`, or emit an explicit SOS marker firmware-side (D-008). | Open, accepted for Stage A |
| ~~**[Added S3]** `04-architecture-conventions.md` §3 still publishes the old `deviceId:sessionId:sequenceNumber` formula~~ | High | Medium | §3 rewritten to the D-006 split key, with the D-008 firmware-sequence option noted as a layered upgrade. | **Closed** (Session 3) |
| **[Added S3]** Sessions 1–3 reasoned under a false "firmware is frozen" premise (D-008); several conclusions were shaped by a constraint that does not exist | High | Medium | D-008 logs the correction and lists every decision it reopens. Re-derive the affected conclusions next session before they harden into implementation. | Open, **re-derivation pending** |
| ~~**[Added S3]** Firmware changes may earn no graded credit (D-008 question 3)~~ | Medium | Medium | Supervisor confirmed 2026-09-13 that **firmware commits do earn credit**, and that firmware enhancement is in scope rather than the excluded "redesign". D-008 closed. Firmware work is planned, assigned and evidenced on the same footing as platform work. | **Closed** (Session 6) |
| **[Added S4]** SOS beacon retransmits (all but the very first position packet of an episode) are sent at `BACKGROUND` mesh priority, not `MAX`, `PositionModule::sendOurPosition()` sets priority by device role, and a handheld unit isn't `TRACKER`/`TAK_TRACKER`. Under mesh congestion, an ongoing emergency's beacon trail is currently the least-protected traffic class on the network after its opening packet. | Medium | High | Firmware-fix candidate under D-008: set `priority = MAX` (or `RELIABLE`) explicitly on the beacon send path rather than delegating to the generic broadcast method. Platform-side, the episode-correlation logic in `gateway-sync` already doesn't rely on `MeshPacket.priority` at all, so this doesn't block TP1/TP2, it's a firmware-side robustness gap, not a backend defect. | Open, **firmware fix candidate** |
| **[Added S6] Map tiles rendering foreign toponyms over Hoàng Sa / Trường Sa are unlawful to publish in Vietnam.** `LiveMapWidget.tsx:18-19` ships the default OpenStreetMap tile server; the team lead verified every OSM base layer labels the archipelagos with Chinese names. Nghị định 174/2026/NĐ-CP Art. 93(3)(a), in force 1 Jul 2026, fines 30–40M VND and permits forced removal of the application | High | **Critical** | Migrate to **Goong Maps over MapLibre GL** (D-012), provider and style held in configuration so the layer is swappable. Referer-allowlist and rate-limit the browser-visible key. **Acceptance test before Review 1**: load the map over ~16.5°N 112.0°E and ~9.7°N 114.0°E, confirm Vietnamese toponyms, file screenshots as evidence | **Accepted, educational scope** (2026-09-29, D-031): the map reverts to OpenStreetMap under the supervisor's acceptance, with a Vietnamese overlay over both archipelagos. No public deployment on OpenStreetMap tiles beyond the course. 2026-10-26 (D-071): the CyclOSM style draws the same OpenStreetMap data; TC-24 re-run with the overlay present, evidence filed. 2026-10-27 (D-072): four switchable basemaps, TC-24 re-run on each. Previously mitigated 2026-09-25 by Goong Maps, evidence in `capstone/Documents/evidence/map-sovereignty/` |
| **[Added S6] The registered English title contains "Smart Device Rental Management" but the system has no AI/ML component.** The faculty fault handbook devotes a whole section to projects whose name promises "AI / smart / thông minh" and whose demo reduces to CRUD, and states plainly that rule-based systems must be called rule-based | High | Medium | Prepare and rehearse the honest answer: the "smart" is **device-level autonomy**, IMU fall detection, autonomous SOS broadcast, multi-hop mesh routing, priority-ordered store-and-forward, not machine learning. Never use "AI" for the platform in any graded document or slide. Every member must be able to give this answer; it is a near-certain council question | Open, **answer to be drafted and rehearsed before W12 Mock Council** |
| **[Added S6] Business parameters hardcoded as literals.** Ranked #2 cause of failure in the faculty fault handbook, and the first entry in its most-asked-questions list is "can this number be changed? demo it now." Five instances already exist in a codebase with no business logic written yet | High | High | D-015: every business parameter in configuration, registered in the Configuration Matrix with a demo path. Fix the five existing instances now, before the pattern is copied into the modules that carry the real parameters (fees, deposits, thresholds, episode windows) | Open, **task queued this session** |
| **[Added S6] Individual-contribution evidence.** A member with few commits and thin meeting presence fails individually even when the group passes; Git organisation and the Progress Log are the named evidence. Implementation currently stands at zero across all modules, so no member has contribution evidence yet | Medium | High | D-014: Progress Log updated before every Group Meeting, per-member and tied to a named deliverable; `08_INDIVIDUAL_CONTRIBUTION_LOG` maintained from W1. Lane assignment gives every member an owned mainflow so commits distribute by construction | Open |
| **[Added S7] The node's own MQTT queue discards an SOS before it discards telemetry.** `mqttQueue` is 16 entries, RAM-only, strict FIFO, and evicts the **oldest** entry on overflow (`MQTT.h:27`, `MQTT.cpp:821–823`). An SOS beacon trail plus routine telemetry fills it in ~80 s of outage, and the single `"SOS - …"` text frame that identifies the episode is the oldest entry, so it goes first. A reboot loses the queue entirely. The eviction is a serial-console `LOG_WARN`, invisible to the platform, so the loss is also unmeasurable. | High | **Critical** | **D-018 Stage B**, an on-device priority-ordered, flash-backed, shed-aware queue, built additively per D-019 and following the `MessageStore` precedent (`04-firmware-ground-truth.md` §4.1). Publish per-tier drop counters so the loss becomes observable and RQ1 gets a device-side denominator. | Open, **this is the term's primary firmware deliverable** |
| **[Added S7] v3 has no PSRAM, and a flash-sized queue bound must not be derived from PSRAM.** `treklink-v3-tbeam` is ESP32 LX6 with ~4 MB flash shared with two OTA app slots; v2 (S3 N8R8) and v4 (Supreme S3) both carry 8 MB PSRAM. The existing `StoreForwardModule` already branches `ps_calloc`/`calloc` on PSRAM presence (`StoreForwardModule.cpp:80–85`), so a queue sized the same way would silently collapse to near-zero capacity on v3 while tests pass on v2. | Medium | High | Size the durable tier off **remaining LittleFS space**, per variant, with the bound as a `build_flags` override exactly as `MESSAGE_HISTORY_LIMIT` already is (`MessageStore.h:22–24`). Capacity is a Configuration Matrix entry per D-015. Test the bound on v3 hardware specifically, not only on v2. | Open, **v3 is in the demo set** (D-018) |
| **[Added 2026-09-25] Correction to the S7 row "v3 has no PSRAM".** The build contradicts it: `treklink-v3-tbeam` inherits `-DBOARD_HAS_PSRAM -mfix-esp32-psram-cache-issue` from `env:tbeam` (`variants/esp32/tbeam/platformio.ini:19-20`), while `treklink-v2` enables no PSRAM (`treklink_v2_0/platformio.ini:19-24`, board `esp32-s3-devkitc-1` declares none). (unverified) physical PSRAM population on the v2 and v3 units. LittleFS is 1 MiB on v3 and 1.5 MiB on v2/v4 (`04-firmware-ground-truth.md` §5). | Medium | High | The S7 mitigation stands unchanged: size the durable tier off remaining LittleFS space, never PSRAM. The per-variant PSRAM column in `onboard-queue/design.md` §4 is corrected in the firmware repo. | Open |
| **[Added 2026-09-25] Correction to the S7 row "The node's own MQTT queue discards an SOS".** Two facts in it were incomplete. (1) In direct Wi-Fi mode stock firmware drains **one** queued entry per successful reconnect and nothing while the link stays up (`MQTT.cpp:604-636`, `:699-709`), so the baseline is worse than drop-oldest alone. (2) The queue also holds **peer** packets the node hears (`Router.cpp:767-769`), so it fills faster than the "~80 s" estimate, which was never measured. | High | **Critical** | Same mitigation, D-018 Stage B. `onboard-queue` must add a drain on the connected branch of `MQTT::runOnce()` (`MQTT.cpp:624-632`), a third stock call site the design did not list. | Open |
| **[Added 2026-09-25] A fall auto-SOS never beacons.** `FallDetectionModule::triggerAutoSOS()` sends one `BACKGROUND` position and one text frame (`FallDetectionModule.cpp:144-145`) and never calls `tickBeacon()`, which only the button and gesture modules call (`TrekLinkButtonModule.cpp:312`, `TrekLinkSOSGesture.cpp:116`). A fall episode is two packets and then silence, so the cadence-anomaly detector (REQ-EVT-06) cannot fire for it, and losing the single text frame makes a fall invisible. | Medium | **Critical** | Firmware fix under D-008: have the fall path enter the same beacon loop as a button SOS and send its opening position at `MAX`. Sequence with `onboard-queue` Phase 9 so each change stays separately measurable. | Open, **firmware fix candidate** |
| **[Added 2026-09-25] An SOS raised before the first GPS fix produces no beacons.** `PositionModule::sendOurPosition()` returns without sending when there is no fixed position and no local position since boot (`PositionModule.cpp:352-355`). Only the trigger-time packets leave the node. | Medium | High | Firmware fix under D-008: the beacon path builds its own position packet (as `sendPositionPacket()` already does) instead of delegating to `sendOurPosition()`. The same change can carry `priority = MAX` (REQ-OPT-02). | Open, **firmware fix candidate** |
| **[Added 2026-09-25] The on-device queue-health report cannot be read on the JSON topic.** `PRIVATE_APP` (256) has no case in `MeshPacketSerializer`, so it falls to `default` (`MeshPacketSerializer.cpp:403-404`) and the JSON message has no `payload`. `gateway-sync` Stage A ingests only `<root>/2/json/...` (REQ-EVT-01), so its REQ-EVT-12/13 are unreachable as specified. | High | Medium | Decide the transport before `onboard-queue` Phase 6: an additive `PRIVATE_APP` case in the serializer, or a `/2/e/` subscription for port 256 in the backend. Define the payload schema in both specs. | Open, **question raised by the firmware session** |
| **[Added S7] The default LoRa channel PSK is Meshtastic's published key**, so RF traffic is encrypted but not confidential, any stock client in radio range decrypts SOS positions (`Channels.cpp:128–134`, `:238`). | High | High | **D-021**, provision a custom per-fleet PSK during device provisioning in MF-01; treat it as a recovery-critical escrowed secret. Distinct from `mqtt.encryption_enabled`, which stays `false` per D-007 with the broker hop secured by TLS + per-gateway API key. | Open, **provisioning step not yet written into `specs/devices/`** |
| **[Added S7]** Stage C's browser form (D-020) relies on **Web Serial / Web Bluetooth, which are Chromium-only**, and on iOS no browser can reach the node at all, so an iPhone guide is served only by the stock Meshtastic app path. A backgrounded or closed tab also stalls forwarding, though IndexedDB means nothing is lost. | Medium | Medium | Document the supported-host matrix before Stage C kick-off; surface forwarding state in the UI; retain the native-desktop fallback (D-020 Option 2) for unsupported venues. State the tab dependency honestly at the council rather than presenting Stage C as an always-on service. | Open, **Stage C deferred; decision recorded so Stage B does not foreclose it** |
| **[Added S4]** No backlog user story exists for the cadence-inferred `SUSPECTED` SOS episode path (`gateway-sync/design.md` §1.3/§2.4, REQ-EVT-06), the primary mitigation for the Critical single-unacknowledged-text-frame risk above has no corresponding Staff-facing workflow story yet | Medium | Medium | US-088 added (`03-backlog/02-user-stories.md`), assigned Khoa, Staff sees a Suspected episode visually distinct from Confirmed and can dismiss it with a lighter action than the full Resolved→Closed flow. | **Mitigated** (Session 4) |
| **[Added 2026-09-25, web session]** `Device.nodeNum Int?` overflows above 2147483647, and node numbers are unsigned 32-bit values from the MAC. Ingestion would fail for about half of all units. | High | High | Type `BigInt` (04-architecture-conventions §3, platform design §3.3); test with `4294967295`. | Mitigated in spec |
| **[Added 2026-09-25, web session]** `gateway-sync` queried the `Incident` table directly (a module-isolation breach) and ignored `RESOLVED` incidents in the episode lookup, which would create a second Incident where E03-6 requires a reopen. | High | Medium | Lookup moved behind `IncidentsService.correlateSos`; a `RESOLVED` incident in the window reopens. | Mitigated in spec |
| **[Added 2026-09-25, web session]** Stock firmware drains a queued backlog one entry per reconnect, so an arrival-time episode window could split one SOS into several Incidents. | Medium | High | Windows and ordering use the event timestamp when valid (`gateway-sync` REQ-UBI-02). | Mitigated in spec |
| **[Added 2026-09-25, web session]** A fall auto-SOS, or an SOS before the first GPS fix, sends no beacons, so losing its single text frame loses the episode and cadence detection cannot fire. | Medium | **Critical** | Firmware `onboard-queue` Phase 9 adds beacons. | Open |
| **[Added 2026-09-25]** New backend dependencies: `@nestjs/schedule`, `@nestjs/event-emitter`, `@nestjs/throttler`, `@casl/prisma`, `pdfkit`. | Medium | Low | Approved by the leader for Phase B (C-003 item 4); frontend test dependencies are approved when the frontend work starts. **2026-10-24**: `nodemailer` approved for the `smtp` transport of `auth` 1.3 (D-063 rule 3). | Resolved |
| **[Added 2026-09-25, leader field report]** Fall detection does not work on v1 (MPU6050) or v2 (ICM-20948), and some v2 units stay stuck in SOS. Root cause not established: IMU driver or HAL wiring, value scaling, thresholds, or a race between the fall, button and gesture SOS owners. | High | **Critical** | Reproduce on hardware with serial logs of raw IMU readings and SOS state transitions before designing a fix (`04-firmware-ground-truth.md` §2). | Open |
| **[Added 2026-09-25, code-verified]** On v3 and v4 the 3-second SOS hold shares `BUTTON_PIN` with the stock user button, which fires SELECT at 500 ms and SHUTDOWN on a longer hold (`InputBroker.cpp:290-306`). Button SOS on T-Beam boards is unreliable and can shut the unit down. | High | **Critical** | Move SOS to a dedicated input or disable the stock long press on TrekLink variants; decide before the demo. | Open |
| **[Added 2026-10-02, code-verified plus regulation]** Transmit settings likely exceed Vietnamese licence-exempt limits. Every variant defaults to `MY_433` (433.0 to 435.0 MHz, 20 dBm conducted, `RadioInterface.cpp:158`, `:847-848`); Circular 08/2021/TT-BTTTT Article 5 licenses 433 MHz LPWAN above 25 mW ERP, so the exempt ceiling is 25 mW ERP in 433.05 to 434.79 MHz (inferred, appendix not read). With the 6 dBi antenna the radiated power is well above that. A reviewer asking "is this legal?" has no clean answer yet. | High | High | Confirm the appendix limit; add a TrekLink Vietnam region or a per-variant power cap so conducted power plus antenna gain stays within 25 mW ERP inside 433.05 to 434.79 MHz; re-measure range at the compliant power, because it will shorten. Firmware ground truth §5.1 | Open |
| **[Added 2026-10-02, leader field test]** No link across a ridge without a relay on the crest, and range collapses in rain (below 100 m) and inside thick concrete. Typical trekking range is 1 to 3 km. | High | High | Accepted physical limit. Disclose to renters and users: the device is not a sole means of communication; move to high ground or place a repeater. Plan a repeater node as optional equipment. Second field test pending. Firmware ground truth §5.1 | Accepted |
| **[Added 2026-10-14, D-045]** A lost renter device keeps the organization's channel key and can read that organization's mesh until the key is rotated, which happens only at the next counter visit. | Medium | High | Loss case flags the key as exposed and notifies the Manager; rotation and re-provisioning at the next counter visit; the limit is stated in the master contract and the documents. | Open, **accepted limit** |
| **[Added 2026-10-14, D-046]** The Field Station executable runs on the customer's laptop, so its code is in the customer's hands. (unverified) How easily the code can be extracted depends on the packager chosen in `gateway-sync` task 5.1. | Medium | Medium | NDA and software licence required at verification; compliance case for an IP violation with suspension and revocation; secrets never ship in the executable (credentials are per station, D-037). | Open |
| **[Added 2026-10-14, D-047]** The weekly scan takes units due for service out of `AVAILABLE` up to a week plus the lead days before their due date, so a contract approval can be refused for want of units that are not yet due. | Medium | Low | `devices.maintenanceLeadDays` is configurable; the weekly list lets Staff complete services early; approval reports the shortfall as today (`INSUFFICIENT_DEVICES`). | Open |
| **[Added 2026-10-29, code-verified]** The v3 and v4 specs promise "position broadcast + alarms" (REQ-V3-SOS-01.1, REQ-V4-SOS-01), but `TrekLinkSOSHelper::activateAlarms()` drives only the buzzer and vibrator pins a variant defines (`TrekLinkSOSHelper.cpp:66-78`), and the T-Beam variants define neither. A v3 holder gets an LED blink and the screen banner (`TrekLinkSOSGesture.cpp:118-120`); a v4 holder gets only the banner, so a holder may not know the SOS fired. | High | High | Decide whether the requirement changes (screen and LED only) or the firmware adds feedback (screen flash, external buzzer on a free GPIO); record the ruling in the v3 and v4 specs. | Open |
| **[Added 2026-10-29, leader field report]** v2 SOS trigger works on hardware (leader, 2026-10-29), but cancel and the stuck-in-SOS case are unverified: a cancel transmits nothing (`TrekLinkSOSHelper.cpp:49-53`), so neither can be seen from the platform, and the flashed commit was not recorded. Does not close the 2026-09-25 field-report row above. | Medium | High | Next v2 run captures the serial log and the flashed commit, and exercises cancel and a repeated trigger; record it in `treklink-firmware/docs/test-runs/`. | Open |
