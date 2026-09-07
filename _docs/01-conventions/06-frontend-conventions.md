# Frontend Code & UI/UX Conventions (React + TypeScript)

> A client application is the bridge between human intention and backend systems. TrekLink's frontend serves four different roles (Admin/Staff/Guide/Customer) on one responsive web app — UI code must be structured, accessible, resilient to gateway/network latency, and intuitive under field conditions (Guides may be on a phone browser at a trailhead).

---

## 1. Architectural Layout (Feature-Sliced Design)

See `04-architecture-conventions.md` §5 for the folder layout. Same dependency rule: `shared → entities → features → widgets → pages → app`.

---

## 2. State Management: The Triad Standard

| State Type | Responsibility | Standard Tooling | TrekLink example |
|---|---|---|---|
| **Server state** | Cached remote API data, refetch, mutation | **TanStack Query** | Device list, trip roster, incident list |
| **Client/UI state** | Ephemeral, local presentation | `useState` / **Zustand** | Map zoom level, active dashboard tab, modal open/close |
| **Live/streaming state** | Real-time push data, not a cache-and-refetch fit | **Socket.io client**, held in a dedicated store/hook | Live device positions, incident notifications, gateway connectivity status |
| **Form state** | Input tracking, validation, dirty checks | **React Hook Form + Zod** | Booking form, device check-out form, incident acknowledgment note |

### Invariants
- Never duplicate server state fetched via TanStack Query into a global store.
- **Live/streaming state is its own category** (not server state, not client state) — Socket.io events (`incident:new`, `device:telemetry`) update a small dedicated store (Zustand) that widgets subscribe to; don't force WebSocket pushes through TanStack Query's refetch model, and don't let every widget open its own socket connection — one shared `socketClient.ts` in `shared/`.

---

## 3. The Core UX Rule: 4 Steps, 6 Fields

- **≤4 sequential steps** for any multi-step flow (booking, device check-out wizard, incident resolution form).
- **≤6 fields per step** (ideal: 3–4).
- **Single-column by default.** Labels above fields, never placeholder-as-label. Consistent required-field marking.

TrekLink-specific: the **incident acknowledgment** flow (Guide/Staff side) is time-critical — keep it to a single step, 2 fields max (acknowledge button + optional note), since the NFR target is a WebSocket-to-acknowledgment path measured in seconds (MTTA), and every extra field/step adds real seconds to that metric.

---

## 4. Reusable Screen Patterns

### Pattern A: List & Search (Device Fleet, Bookings, Incident Queue)
```
+-----------------------------------------------------------------------+
| Search & Filters: [ Q Search device ID... ] [ Status v ] [+ Register]|
+-----------------------------------------------------------------------+
| [ ] Device ID    Variant   Status      Battery   Last Seen  Actions  |
| [ ] TL-0042      v3        In-Field    68%       2m ago      [... v] |
+-----------------------------------------------------------------------+
| Showing 1-20 of 57 devices                          < [ 1 ] 2 3 ... > |
+-----------------------------------------------------------------------+
```
Destructive/state-changing actions (retire a device, cancel a rental) open a confirmation modal first. Empty states get an informative message + CTA, never a blank table.

### Pattern B: Live Monitoring Dashboard (Staff/Admin/Guide)
- Leaflet.js map as the primary widget; device/trip markers colored by status; incident markers pulse/highlight.
- A connectivity indicator per gateway (last-seen timestamp, "syncing" vs "stale") — this directly surfaces the NFR the register cares about, don't hide it in a tooltip.
- Incident queue panel sits beside the map, not below the fold — an active SOS should be visible without scrolling.

### Pattern C: Add/Edit Form
Field order identical between Add (empty) and Edit (pre-filled) modes. Primary submit bottom-right; ghost-styled Cancel.

---

## 5. Keyboard Navigation & Accessibility (WCAG 2.1 AA)

1. Tab/Shift+Tab in logical visual order — never `tabindex > 0`.
2. Enter submits the focused form.
3. Escape closes the active modal/drawer, returns focus to the trigger.
4. Space toggles checkboxes/switches.
5. Arrow keys navigate composite controls (data grids, tabs, the incident queue list).
6. Every interactive element has a visible focus ring, ≥3:1 contrast — never `outline: none` without a replacement.

---

## 6. Client API & Validation Contract Mirroring

### 6.1 Centralized API Client
No raw `fetch`/`axios` in components. `shared/apiClient.ts` owns:
- Base URL/env config, Bearer token injection.
- **Silent refresh interceptor**: intercepts 401, calls `/api/auth/refresh`, replays the original request.
- Unwraps the standard envelope (`{ result, isSuccess, statusCode, message }`) once, centrally — components consume `result` directly, they never see the envelope.

### 6.2 Validation Schema Parity (Zod ↔ class-validator)
Mirror the backend DTO exactly:
```typescript
export const CreateDeviceSchema = z.object({
  hardwareVariant: z.string().min(1, { message: 'Hardware variant is required' }),
  status: z.enum(['AVAILABLE', 'MAINTENANCE']).optional(),
});
```

### 6.3 Inline Error Mapping
Since the backend envelope's failure `message` is a single string (not a field-scoped array — see `05-backend-conventions.md` §2), field-level mapping happens **client-side first** via the mirrored Zod schema before submission; a server-side 400 falls back to a form-level (not per-field) error banner using `message`.
