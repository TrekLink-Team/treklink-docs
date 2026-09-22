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
