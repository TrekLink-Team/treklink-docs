# Clarification Answers

> **What this is**: the leader's answers to spec clarification interviews, recorded verbatim in
> substance at the moment they were given. Convention 02 §3 Phase 1.2 makes the interview a
> mandatory gate; this file is where its output lives so the next session does not re-ask.
>
> **Status of an answer**. Two levels, and the difference is binding:
>
> | Level | Meaning |
> |---|---|
> | **Confirmed** | Answered and in force. Write it into the spec. |
> | **Recorded** | Answered, but the module has not been specced yet. It is the leader's stated intent, not a frozen requirement. Re-confirm it during that module's own interview before building on it. |
>
> An answer that becomes a design choice with a rationale and a rejected alternative is promoted to
> a `D-xxx` entry in [`03-decisions-and-risk-register.md`](03-decisions-and-risk-register.md).
> This file is the raw record, not the decision log.
>
> **Numbering**. Questions are numbered sequentially from 1 in a single run, never per section.
> See [`../01-conventions/08-ai-agent-steering-and-discipline.md`](../01-conventions/08-ai-agent-steering-and-discipline.md) Stage 2.8.

**Session 8, 2026-09-22.** Questions 1 to 73. Questions 1 and 2 concerned the daily-report CI and
are resolved, so they are not repeated here.

---

## 1. Landing page, questions 3 to 24 (Confirmed)

The landing page is a **new deliverable**, requested by the supervisor, due before **Review 1 on
1 October 2026**. It is not one of the five Main Flows.

| # | Topic | Answer |
|---|---|---|
| 3 | Hosting | GitHub Pages. Free, and the URL is short. It must **work at all times**, independently of the backend. |
| 4 | URL | Expect `treklink-team.github.io/treklink-web/`. Preference, if achievable: `treklink.github.io/web/`. See §3 for what is actually possible. |
| 5 | Custom domain | Considered, not a priority. Use the default for now. Keep it on the roadmap. |
| 6 | Live or localhost | Either is acceptable, but a live site scores higher. **Recommendation accepted: deploy to GitHub Pages.** Code quality outranks being live; no broken connection states, no visible errors. |
| 7 | Deadline | **Hard: 1 October 2026.** Landing page, SRS, design document and the Main Flow demonstration must all exist before Review 1. |
| 8 | Audience | Everyone. Public. |
| 9 | Language | English first, Vietnamese later. This requires a real **locale system**, not hardcoded strings. |
| 10 | Naming | Just **TrekLink**. It is the product line and the system name. |
| 11 | Sections | Product first, in the Garmin manner. Proposed order: product advert, problems, product lines. The link into the system belongs in the **header**, not in the hero content. |
| 12 | Research angle | Yes, as a separate **R&D section**. Audience is everyone, so it must read generally and professionally. |
| 13 | Team section | No team names, no team photos. **Product photos only**, supplied later by the leader. |
| 14 | University branding | No. |
| 15 | Visual direction | Pastel dark military green. Forestry and lumber typography, US lumberjack styling, bold and military. Bold wood-urban plus **neomorphism** and **glassmorphism**. Reference existing work, never copy one to one. |
| 16 | Imagery | The leader has product images but not yet. **Open: where to put them.** See question 74. |
| 17 | Live map on the landing page | **No.** It is a landing page. |
| 18 | Figma | Not used. Structure is header and content, possibly a carousel and a scrollspy. Element vocabulary comes from [namethatui.com](https://namethatui.com/). |
| 19 | Build tool | Vite. Astro acceptable. Make it good. |
| 20 | System links before the app exists | Best practice, agent's discretion. |
| 21 | Analytics | Yes. |
| 22 | Spec before code | **Yes, mandatory. Draft the spec first.** The session that answered these questions is documentation only. |
| 23 | Accessibility | Yes, per conventions and protocol. WCAG AA. |
| 24 | Owner | **KhoaDD.** Not a Main Flow, so it does not appear on the Mainflow Coverage Matrix as one. |

---

## 2. Carried work, questions 25 to 29 (Confirmed)

| # | Topic | Answer |
|---|---|---|
| 25 | Jira re-sync for `TK-63`, `TK-64`, `TK-73` | **Jira is currently empty.** The agent must write the setup and population instructions first, then drive Jira on the leader's behalf. |
| 26 | `onboard-queue` Phase 0 hardware measurement | **Hold.** |
| 27 | Phase 0 defaults proposed instead of blocking | Yes. |
| 28 | Map sovereignty check | Already done by the leader. Goong is compliant with the regulation. No further check needed. |
| 29 | What is "Smart" in the registered title | SOS, fall detection, the fallback and priority queue for signal, audit logs and watchdogs. |

---

## 3. MF-01 module answers, questions 30 to 73 (Recorded, not finalized)

These were given ahead of the module interviews for `auth`, `devices`, `rentals` and `trips`.
They are the leader's stated intent. **Re-confirm each during that module's own interview.**
Nothing here is a frozen requirement yet.

### Identity and access, questions 30 to 46

| # | Topic | Answer |
|---|---|---|
| 30 | Is Customer an authenticated user | Both. A Customer may browse without an account, but joining a trip requires either self-registration or a Guide. |
| 31 | How a Customer account is created | Two flows. **Flow 1**: self-register with Google OAuth or email OTP, book a trip directly, Guide assigns to customer. **Flow 2**: browse trips without an account, contact a Guide by phone or message, Guide verifies and calls back, Staff or Guide creates the account. |
| 32 | Tenancy | One tenant. |
| 33 | Role model | **Two major roles: Customer and Staff.** Staff carries sub-roles: Operator, Guide, Admin. Guides are Staff with guide skills. Admins are Staff with privileges. The sub-role list must be extensible, for example Manager later. |
| 34 | Session model | Modern best practice. |
| 35 | Password policy and reset | Best practice. Reset by email OTP resend, and by contacting Staff directly. **Staff can trigger a reset but never see the password.** They validate the customer first against public credentials such as name, phone, email or registered ID, then send the reset to the origin email only. |
| 36 | Delete semantics | Soft delete everywhere. Hard delete only where genuinely suitable. |
| 37 | Timezone | Regional. Detect the viewer's timezone by IP, default `+7`. |
| 38 | Pagination | Per conventions. |
| 39 | Error codes | Industry standard, per conventions. |
| 40 | Seed data | Not yet scoped. |
| 41 | Login identifier | **Username is the primary key, always.** Email is linkable later or set at registration. The default username is derived from the email local part, so `name123@mail.com` yields `name123`. |
| 42 | Public endpoints | Best practice. |
| 43 | CASL granularity | Industry standard. |
| 44 | Guide scope | A Guide can be assigned to many trips. Trip management is assignment based. Operators assign trips to Guides, including future trips. |
| 45 | Account status | Just `isActive`. |
| 46 | What to audit | Everything, per best practice. |

### Devices, questions 47 to 54

| # | Topic | Answer |
|---|---|---|
| 47 | Is the device FSM final | Not final. Needs more planning. |
| 48 | Manual versus automatic transitions | Needs discussion. The points that matter are the ones a Staff member or Guide must verify: warehouse in-stock allocation, and preventing state race conditions. |
| 49 | Registration fields | Device info, including hardware version. |
| 50 | v1 devices | Registrable. A **trip** may restrict which versions it accepts; a demo or test trip may accept any. Rule of thumb: allow, and let Staff set the rules. Check the v1 firmware first. Most devices are MQTT capable without a built-in queue buffer. |
| 51 | Where PSK provisioning lives | In `devices`. `rentals` calls out to it; Staff performs it. |
| 52 | Battery thresholds | Target `>= 50%`. Below `90%`, Staff should advise the Guide to charge first. **Telemetry never blocks assignment and never drives retirement.** Manual verification by a technician, Staff or Guide is final. |
| 53 | One device on two trips | **Yes, provided the trips do not overlap in time.** A device can be pre-allocated to a future trip while still out on its current rental, so Staff never wait for a trip to finish before assigning. |
| 54 | Device history audit trail | Yes. |

### Rentals and billing, questions 55 to 64

| # | Topic | Answer |
|---|---|---|
| 55 | Booking versus Rental | **Both entities.** A booking does not guarantee a rental, and a rental can exist without a booking, for Staff or Guide provisioning of an unauthenticated customer. |
| 56 | Booking FSM | Proposed: `start`, `sent`, `pending`, `completed`. |
| 57 | Multiple devices per booking | Yes when a Guide makes the booking. Single device when a Customer makes it. |
| 58 | Row-level locking on reservation | Yes. |
| 59 | Reservation hold | **10 minutes** for a Customer, then it invalidates. Staff can extend or disable the hold for a Staff or Guide booking. Staff can disable or transfer a booking to a Guide if the Customer violates the terms or is delegated to Guide provisioning. |
| 60 | Cancellation | Free within 10 minutes, refunded instantly because the money sits in escrow. After 10 minutes, a **5% fee on the rental fee**, not on the trip fee. Every parameter is admin-configurable. |
| 61 | Deposit | By tier. Configurable per plan, pack, quantity and device version. |
| 62 | Rental agreement | A generated **PDF** plus an audit log, returning a live signature saved onto the PDF and a status update. The PDF is in scope. A real certificate authority is **not**; a simple draw-on-web signature is acceptable. |
| 63 | Pricing model | Per trip package or similar, fully admin-configurable. Per-device and per-pack discounts, combo packs, and Guide-provisioned or Staff pricing. |
| 64 | Where payment lives | **`billing` only.** `rentals` calls outward. Services call each other to preserve atomicity. |

### Trips, questions 65 to 73

| # | Topic | Answer |
|---|---|---|
| 65 | How a Trip is created | Staff create it independently and link it. A Guide may request a trip, which Staff then author. |
| 66 | Trip FSM | `Draft`, `On Prepare` (provisioning, Staff assignment, hardware), `On Booking` (customer books or Guide provisions), `On Start`, `Ongoing`, `Finished`, plus `Cancelled` and an emergency state for when the whole trip or operation is at risk and authorities are needed. **Open: the name of that emergency state.** See question 76. |
| 67 | Route, waypoints, checkpoints | **No.** Web version only. The Meshtastic app already shows node positions, though without route lines. Determine whether team coordinates alone are sufficient. |
| 68 | Guides per trip | Configurable. |
| 69 | Participant tracking | A trip tracks individuals by device, customer registration or booking. |
| 70 | Trek package entity | Yes, and configurable. |
| 71 | What ends a trip | A Staff or Guide action. **Devices never come back through the Customer.** The Guide collects every device from the customers and reports any missing ones. |
| 72 | Reschedule and cancel | Both allowed. |
| 73 | Guide readiness check | Just a checklist. |

---

## 4. Maintenance

Append a new session block rather than editing an old one. An answer that is later overruled is
struck through in place with a pointer to what replaced it, never deleted, so the reasoning trail
survives. Promote anything that acquires a rationale and a rejected alternative into the decision
register and link it from here.

---

## 5. SRS interview, questions 1 to 28 (Session 9, 2026-09-25)

Asked by the cloud SRS session in `_handoff/SYNC.md` entry C-002, against the gap audit in
`_handoff/srs-gap-audit.md`. This batch numbers from 1 again because it is a separate interview;
cite it as "07 §5 question n". The leader answered in chat on 2026-09-25: questions 1 to 22
"agree" to the stated default, question 23 and question 24 answered individually, questions 25 to 28
asked as a follow-up and answered the same day. Every row is
**Confirmed**.

| # | Topic | Answer | Level |
|---|---|---|---|
| 1 | System or platform | A single-tenant operations **system** named TrekLink Operations Platform. Its platform properties are its extension seams: pluggable ingress adapters (D-007), configuration-driven business rules (D-015), stock Meshtastic compatibility (D-019), extensible Staff sub-roles (§3 question 33) | Confirmed |
| 2 | Actor model | Human actors: **Guest** (anonymous browse), **Customer**, and abstract **Staff** generalizing **Operator**, **Guide** and **Admin**. "Staff" in the Main Flows reads as Operator. Admin is Staff "with privileges" (§3 question 33), so Admin holds every Operator permission; this supersedes the read-only generalization rule in `06-requirements-foundation.md` §2 | Confirmed |
| 3 | Recorded answers in the SRS | The SRS adopts §3 questions 30 to 73 as requirements, each marked provisional pending its module interview. Where one contradicts `06-requirements-foundation.md` or `05-main-flows.md`, the Recorded answer wins | Confirmed |
| 4 | Device FSM | The seven states are the device's **physical** state. Future commitments are Allocation records with non-overlapping time windows. `Rented` becomes `In-Field` when an Operator or the assigned Guide starts the trip (backlog US-032 criterion 1) | Confirmed |
| 5 | Trip emergency state | Named `Emergency`. Entered only by an Operator action; an open Incident flags the trip but does not move it automatically | Confirmed |
| 6 | Incident FSM gaps | Detection confidence (`Confirmed`, `Suspected`) is an attribute, not a state. Dismissing a suspected incident is `Detected` to `Closed` with a mandatory dismissal reason (backlog US-088). Reopen is `Resolved` to `In Progress` only; beacons after `Closed` open a new Incident | Confirmed |
| 7 | Incident authority | The first acknowledgement by an Operator or by the trip's assigned Guide performs `Detected` to `Acknowledged` and fixes the MTTA timestamp. A later acknowledgement by the other party is recorded in the audit trail without a transition (backlog US-060, US-063). `In Progress` updates: Operator, Admin or the assigned Guide (US-061). `Resolved` and `Closed`: Operator or Admin only (US-062) | Confirmed |
| 8 | Who pays, and when | A Customer booking pays rental fee plus deposit into sandbox escrow at booking confirmation; an Operator records the payment for a rental provisioned without a booking. Settlement at check-in: invoice, deposit applied first, then balance charged or refund issued | Confirmed |
| 9 | Notification channel | In-app WebSocket push plus email. No SMS, no Zalo. A Guide out of coverage receives pending notifications when the phone reconnects | Confirmed |
| 10 | System boundary | The Gateway Bridge is inside the system boundary. The TrekLink Device and the LoRa mesh are an external entity. The on-device queue (Stage B) is described as an interface requirement on the device | Confirmed |
| 11 | Authentication externals | Google OAuth and email OTP are in scope. Google Identity and an email delivery service are external systems | Confirmed |
| 12 | Contents of the W4 SRS | Write now: Screen Authorization matrix, conceptual ERD of 5 to 8 core entities, Messages list. Defer to W8: Screens Flow and Screen Descriptions | Confirmed |
| 13 | Use case set | UC-01 to UC-26 stay stable; additions start at UC-27. The two `include` errors are corrected: UC-13 no longer includes UC-23, UC-11 no longer includes UC-10 | Confirmed |
| 14 | UC diagrams | Five per-Main-Flow diagrams plus a sixth for administration and access | Confirmed |
| 15 | FR identifiers | Prefixes AUTH, DEV, BOOK, TRIP, EVT, INC, MON, BILL, CFG. The 24 IDs the BR matrix already cites keep the meaning it implies. EARS text comes from backlog acceptance criteria and cites the `US-nnn` source | Confirmed |
| 16 | MF-02 swimlane | The supervisor-derived diagram is kept as drawn; the SRS explains the three stages in text | Confirmed |
| 17 | Usability and availability numbers | NFR-USE-01 and NFR-USE-02 are kept, sourced to `01-conventions/06-frontend-conventions.md` §3 and backlog US-025 and US-060. No availability target exists; the SRS row reads `(needs check)` | Confirmed |
| 18 | Evidence for the pain points | None held. The Review 1 slides state the problems without figures | Confirmed |
| 19 | Review 1 presenters | KhoaDD: title, Context, Proposed Solution, MF-02. LongLP: Existing Situation and Problems, MF-05. HoangTK: Key Features, MF-03. LongNN: Actors and Functions, MF-04. TanNB: MF-01, scope, plan, closing | Confirmed |
| 20 | Landing page and localization | The landing page is a separate deliverable outside the SRS. Localization stays out of scope for the operations system | Confirmed |
| 21 | Rental agreement signer | The Customer signs on the web at check-out. For a customer without an account, the Operator or Guide captures the customer's signature on the staff device | Confirmed |
| 22 | Sandbox payment provider | Internal mock with `Pending`, `Paid`, `Failed` (backlog US-069). It is a module inside the system, not an external system | Confirmed |
| 23 | Sovereignty evidence | **No screenshots are filed yet.** The check was done by inspection (§2 question 28); the evidence file is outstanding. BR-24 and TC-24 stay open until it exists | Confirmed |
| 24 | Part I and authorship | Part I is included; Team Involvements lists assigned lanes, not claimed contributions. "In charge" for this revision: **Đỗ Đăng Khoa and Nguyễn Bá Tân**. Where a field holds exactly one name, **Đỗ Đăng Khoa** | Confirmed |
| 25 | Booking FSM meaning (refines §3 question 56) | `Start`: customer filling the form, 10-minute device hold running. `Sent`: submitted, awaiting Operator review. `Pending`: Operator confirmed, awaiting payment and check-out. `Completed`: converted into a Rental at check-out. Side exits: `Expired` (hold lapsed in `Start`), `Rejected` (Operator), `Cancelled` (Customer or Operator) | Confirmed |
| 26 | Trip FSM meaning (refines §3 question 66) | `Draft` → `On Prepare` → `On Booking` → `On Start` (devices checked out, group assembling) → `Ongoing` (trip started, devices `In-Field`) → `Finished`. `Cancelled` from any state before `Ongoing`. `Emergency` only from `Ongoing`, returning to `Ongoing` or moving on to `Finished` | Confirmed |
| 27 | Rental FSM | `Created` (agreement generated) → `Active` (checked out) → `Returned` (checked in, invoice issued) → `Closed` (balance settled). `Escalated` from `Active` when a device is not returned within the grace period; `Escalated` → `Closed` only after a loss record | Confirmed |
| 28 | Battery thresholds (refines §3 question 52) | Below **90 %**: advisory "charge before departure". Below **50 %**: warning that requires the Operator or Guide to confirm manual verification. **Neither blocks allocation or check-out**: a flat device is still allocatable, because the Guide is responsible for the manual check and for charging. Both thresholds are configuration (D-015) | Confirmed |

---

## 6. Module specification interview, `treklink-web` C-003 items 1 to 41 (2026-09-25)

The leader accepted items 1 to 6 in full and answered items 9, 20, 25, 26, 27, 29, 40 and 41. Every
other item takes the proposal the specs were written against. Where an item conflicts with §5, §5
governs, because it was confirmed first and the Report 3 SRS is built on it. These answers also
confirm the Recorded answers of §3 as the specs interpret them.

| # | Question | Answer | Level |
|---|---|---|---|
| 1 | A `platform` module | Yes, D-028 | Confirmed |
| 2 | Failure envelope | `result: { "errorCode": "..." }`, D-026 | Confirmed |
| 3 | Operation dispatch scope | `gateway-sync` only, D-027 | Confirmed |
| 4 | New backend dependencies | `@nestjs/schedule`, `@nestjs/event-emitter`, `@nestjs/throttler`, `@casl/prisma`, `pdfkit` approved | Confirmed |
| 5 | Strict TypeScript | `strict: true` in `backend/tsconfig.json`, first task of Phase B | Confirmed |
| 6 | Phase B scope | `platform`, `auth`, `devices`, `trips`, `rentals`, the `gateway-sync` ingestion core (Stage A plus Stage B health), `billing` quote and escrow | Confirmed |
| 7 | `auth` as written | Accepted: `CUSTOMER` and `STAFF`, sub-roles as data, username or email login, lockout 5 failures in 15 minutes for 15 minutes | Confirmed |
| 8 | Google OAuth | Later, behind `AUTH_GOOGLE_ENABLED` | Confirmed |
| 9 | OTP email account | **`treklink.team@gmail.com`** through Gmail SMTP for demo and shared environments; `console` transport locally and in CI. The app password lives in deployment secrets, never in the repository | Confirmed |
| 10 | Reset for a Customer without email | Staff verify the person, add an email, then trigger the reset to it | Confirmed |
| 11 | Time zone | Browser time zone, default `Asia/Ho_Chi_Minh` | Confirmed |
| 12 | Device transition table | As in `treklink-web/specs/devices/design.md` §2.1, mirrored in `04-architecture-conventions.md` §2.1 | Confirmed |
| 13 | When a device becomes `In-Field` | Automatically when its trip enters `Ongoing` | Confirmed |
| 14 | Lost devices | Loss-suspected plus an alert after `rentals.nonReturnGraceDays` (default 3); retirement only on Staff confirmation (BR-22, E05-3) | Confirmed |
| 15 | Channel key check at check-out | Block when behind `devices.currentPskVersion`, switchable by `devices.requireCurrentPskForCheckout` | Confirmed |
| 16 | Emergency trip state | `Emergency`, as in §5 question 26 | Confirmed |
| 17 | MF-01 "Scheduled" | Means `On Start` (§5 question 26); `05-main-flows.md` updated | Confirmed |
| 18 | Who starts and finishes a trip | The Lead Guide and any Operator; not Assistant Guides | Confirmed |
| 19 | Agency-initiated cancellation | Full refund, no customer fee | Confirmed |
| 20 | Payment timing | **Escrow at booking** (trip fee, rental fee, deposit), settlement at return, switchable by `rentals.requireEscrowBeforeReview` | Confirmed |
| 21 | Hold expiry | An unpaid hold expires and releases the device; the booking stays open without a device; a paid hold persists until Staff review | Confirmed |
| 22 | "Reserve device" order | Before Staff confirmation; the MF-01 swimlane is redrawn to match | Confirmed |
| 23 | Booking states | **§5 question 25 governs** (`Start`, `Sent`, `Pending`, `Completed`, plus cancelled and rejected). The `treklink-web` specs are renamed to match | Confirmed, follow-up |
| 24 | Guide-channel escrow | None; hold disabled, everything settled at return | Confirmed |
| 25 | File storage | **Yes**: Postgres `bytea` for agreement PDFs and inspection photos, photos capped at 2 MB; object storage later | Confirmed |
| 26 | Agreement PDF transport | Base64 inside the D-002 envelope. The PDFs are small, D-002 keeps no exception, and clients keep one code path (orchestrator's choice under the leader's "whichever is better") | Confirmed |
| 27 | Default amounts | Accepted: late fee 50 000 VND per device per started day after a 2-hour grace, waiver threshold 200 000 VND, free cancellation for 10 minutes then 5 % of the rental fee. **Payment is mocked** so the flow is never blocked; the real payment gateway is decided later | Confirmed |
| 28 | Waiver approver | Another Operator who did not inspect the device | Confirmed |
| 29 | Review 2 state machines | **Device and Incident**, Rental as a supporting figure | Confirmed |
| 30 | Episode parameters | 300 s window, 60 s retro-tag grace, 6 positions in 60 s; recalibrated after the routine-interval capture | Confirmed |
| 31 | Reopen after `Resolved` | Reopens to `Detected`, so someone acknowledges again | Confirmed |
| 32 | Escalation | 120 s unacknowledged re-alerts all Operators and Admins | Confirmed |
| 33 | Resolve and close | Operators only; Guides acknowledge and add notes | Confirmed |
| 34 | MTTA and MTTR start | The first event of the episode | Confirmed |
| 35 | Monitoring defaults | Device and gateway stale 120 s, maximum plausible speed 30 km/h, battery warning 30 %, critical 15 % | Confirmed |
| 36 | Admin live stream | Full position stream, as Operators | Confirmed |
| 37 | Ordering | The gateway flush orders by queue sequence and priority; the backend orders by the payload timestamp when valid (E02-6 updated) | Confirmed |
| 38 | Story ID `US-101` | Added to the backlog as **US-089** (`gateway-sync`); the firmware's `US-102` became **US-090**. Both specs now cite the backlog IDs | Confirmed |
| 39 | Operations app locale layer | No; strings grouped per feature | Confirmed |
| 40 | Neon | **One shared dev database**, migrations applied only from `dev` by CI or the leader | Confirmed |
| 41 | Seed data | **Accepted**: one user per role plus two extra Guides, the four variants, 10 devices, 2 packages, 2 trips (one open for booking, one ongoing), labelled demo pricing | Confirmed |
