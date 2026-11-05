# Frontend Code & UI/UX Conventions (React + TypeScript)

> A client application is the bridge between human intention and backend systems. TrekLink's frontend serves four different roles (Admin/Staff/Guide/Customer) on one responsive web app, UI code must be structured, accessible, resilient to gateway/network latency, and intuitive under field conditions (Guides may be on a phone browser at a trailhead).

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
- **Live/streaming state is its own category** (not server state, not client state), Socket.io events (`incident:new`, `device:telemetry`) update a small dedicated store (Zustand) that widgets subscribe to; don't force WebSocket pushes through TanStack Query's refetch model, and don't let every widget open its own socket connection, one shared `socketClient.ts` in `shared/`.

---

## 3. The Core UX Rule: 4 Steps, 6 Fields

- **≤4 sequential steps** for any multi-step flow (booking, device check-out wizard, incident resolution form).
- **≤6 fields per step** (ideal: 3–4).
- **Single-column by default.** Labels above fields, never placeholder-as-label. Consistent required-field marking.

TrekLink-specific: the **incident acknowledgment** flow (Guide/Staff side) is time-critical, keep it to a single step, 2 fields max (acknowledge button + optional note), since the NFR target is a WebSocket-to-acknowledgment path measured in seconds (MTTA), and every extra field/step adds real seconds to that metric.

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
Every list renders through `CollectionView` (§9); this sketch is its Details view. Destructive/state-changing actions (retire a device, cancel a rental) open a confirmation dialog first (§9.6). Empty states get an informative message + CTA, never a blank table.

### Pattern B: Live Monitoring Dashboard (Staff/Admin/Guide)
- **Leaflet** map as the primary widget, rendering **OpenStreetMap** raster tiles (**D-031**); device/trip markers show status by a shape or glyph as well as colour (1.4.1), at 3:1 against the tiles (1.4.11); incident markers pulse at most 3 times per second (2.3.1), stop pulsing after 5 s or do not pulse at all under `prefers-reduced-motion`, and the map offers a pause control for any pulse still running (2.2.2); every marker is reachable from a keyboard-operable list beside the map (2.1.1, 2.5.7).
- **Map provider is configuration, never a literal** (**D-031**, **D-015**). The provider name, tile URL, attribution, key and default viewport come from config so the base map can be swapped without touching component code:

  ```ts
  // shared/config/map.ts — values from import.meta.env, never inlined
  export const mapConfig = {
    provider:    env.VITE_MAP_PROVIDER,     // 'osm'; 'goong' is dormant (D-031)
    tileUrl:     env.VITE_MAP_TILE_URL,     // https://tile.openstreetmap.org/{z}/{x}/{y}.png
    attribution: env.VITE_MAP_ATTRIBUTION,  // must stay visible on the map
    mapKey:      env.VITE_MAP_KEY,          // Goong only; unset while OSM is the provider
    center:     [env.VITE_MAP_CENTER_LNG, env.VITE_MAP_CENTER_LAT],
    zoom:       env.VITE_MAP_ZOOM,
  };
  ```

  Dormant Goong notes, kept for a switch back: style variants `goong_map_web` (full icons), `goong_map_highlight` (minimal icons),
  `goong_satellite`. Goong issues **two credentials**, a **Map Key** for style and tile URLs, and a
  separate **API Key** for Autocomplete, Direction, Geocoding, Distance Matrix and Place Detail.
  Do not conflate them.
- **Sovereignty overlay, mandatory.** OpenStreetMap base layers label Hoàng Sa and Trường Sa with
  foreign toponyms, and Nghị định 174/2026/NĐ-CP Art. 93(3)(a) penalises failing to depict
  sovereignty fully (30–40 M VND, plus forced removal of the application). The map therefore always
  carries a Leaflet overlay that labels both archipelagos in Vietnamese as Vietnamese territory.
  OpenStreetMap is accepted for the course only (D-031, R11); a public deployment beyond it
  switches the provider back to Goong. Any change of base map requires a fresh check over
  ~16.5°N 112.0°E and ~9.7°N 114.0°E, with the screenshots filed as evidence.
- **OpenStreetMap tile usage policy**: attribution visible on the map, a named User-Agent and a
  valid Referer, no cache bypass, and no bulk prefetch, so no offline tile download.
- If Goong is re-enabled, its map key is visible in the browser by design. Restrict it with an
  HTTP-referer allowlist and a per-IP rate limit.
- A connectivity indicator per gateway (last-seen timestamp, "syncing" vs "stale"), this directly surfaces the NFR the register cares about, don't hide it in a tooltip.
- Incident queue panel sits beside the map, not below the fold, an active SOS should be visible without scrolling.

### Pattern C: Add/Edit Form
Field order identical between Add (empty) and Edit (pre-filled) modes. Primary submit bottom-right; ghost-styled Cancel.

---

## 5. Keyboard Navigation & Accessibility (WCAG 2.2 AA)

1. Tab/Shift+Tab in logical visual order, never `tabindex > 0`.
2. Enter submits the focused form.
3. Escape closes the active modal/drawer, returns focus to the trigger.
4. Space toggles checkboxes/switches.
5. Arrow keys navigate composite controls (toolbars, tabs, menus, the incident queue list) with roving `tabindex`, one tab stop per control. A read-only table stays a native `<table>`.
6. Every interactive element has a visible focus ring, ≥3:1 contrast, never `outline: none` without a replacement.
7. Focus is never hidden by sticky content (incident banner, command bar, table header): set `scroll-padding-top` (2.4.11).
8. Every pointer target is at least 24 by 24 CSS px (2.5.8, AA; links inside a sentence are exempt, §10.7). Primary controls are at least 44 by 44 CSS px, the team's stricter rule taken from 2.5.5 (AAA). A primary control is the page's main action, a dialog's confirm button or the SOS acknowledge button; this definition holds wherever chapter 06 says "primary control".
9. Text meets 4.5:1, icons and boundaries 3:1 (1.4.3, 1.4.11).
10. Every icon and marker has a text alternative (1.1.1).
11. Status changes, form-level errors and new incidents are announced through a live region, polite, or assertive for an SOS (4.1.3).

**Known exception (leader, 2026-11-03, D-096):** the handover signature pad is drawing only, with no typed alternative; it is recorded against 2.5.1 and 2.5.7 and revisited if a reviewer raises it.

---

## 6. Client API & Validation Contract Mirroring

### 6.1 Centralized API Client
No raw `fetch`/`axios` in components. `shared/apiClient.ts` owns:
- Base URL/env config, Bearer token injection.
- **Silent refresh interceptor**: intercepts 401, calls `/api/auth/refresh`, replays the original request.
- Unwraps the standard envelope (`{ result, isSuccess, statusCode, message }`) once, centrally, components consume `result` directly, they never see the envelope.

### 6.2 Validation Schema Parity (Zod ↔ class-validator)
Mirror the backend DTO exactly:
```typescript
export const CreateDeviceSchema = z.object({
  hardwareVariant: z.string().min(1, { message: 'Hardware variant is required' }),
  status: z.enum(['AVAILABLE', 'MAINTENANCE']).optional(),
});
```

### 6.3 Inline Error Mapping
Since the backend envelope's failure `message` is a single string (not a field-scoped array, see `05-backend-conventions.md` §2), field-level mapping happens **client-side first** via the mirrored Zod schema before submission; a server-side 400 falls back to a form-level (not per-field) error banner using `message`, announced with `role="alert"`; client-side field errors set `aria-invalid` and are linked with `aria-describedby`.

---

## 7. Screen Design Checklist (SD phase, D-053)

Each screen is designed before it is coded, as one file
`treklink-web/specs/frontend/ui-design/<route-slug>.md` from the template in that folder's
`README.md`. The layout itself is a wireframe image (PNG or SVG, any tool) committed next to it.
The design is done when every box is ticked:

- [ ] **Route and roles** match `specs/frontend/design.md` §2; what each role sees or cannot see is stated.
- [ ] **Data**: every field shown names its source (`api-design` file and response property); nothing is shown that no endpoint returns.
- [ ] **Actions**: every button names the endpoint it calls, its confirmation if irreversible, and the message on success (MSGnn).
- [ ] **States**: loading, empty, error (one row per error code the endpoints return, with its message), forbidden or not found (MSG26), and success.
- [ ] **Forms**: at most 4 steps of at most 6 fields (§3); every field has its label, type, required flag and the validation rule mirrored from the DTO (§6.2).
- [ ] **Mobile**: the 360 px layout is drawn for the operator's incident and map screens (NFR-UI-01); other screens state how they collapse (§10.5); every screen reflows at 320 CSS px (1.4.10).
- [ ] **Accessibility**: tab order, focus target after each action, text alternative for every icon and marker, target sizes, live announcements, contrast (§5).
- [ ] **Live data**: which WebSocket events refresh the screen and which query keys they invalidate.
- [ ] **Traceability**: the use case, the FRs and the backlog story the screen serves.

## 8. UI and UX Practices

Applied by every screen; a reviewer cites the item number.

1. **One primary action per screen**, visually distinct; destructive actions are secondary and confirm with the object's name ("Retire device TL-0042?").
2. **Consistent placement**: page title and primary action top right of the header, filters above the table, row actions at the row end.
3. **Status is never colour alone**: every state badge carries its label as a short word ("Rented", "Not heard"), never the enum name; the detail sits beside the badge as plain text that can wrap ("since 11:20, 3 h ago"), because the badge truncates in dense views; colour follows one palette per lifecycle across the app.
4. **Tables**: rendered by `CollectionView` (§9), sortable by the columns a user filters on through header buttons with `aria-sort`, paged by the server (§4 Pattern A), with the empty state explaining what to do next.
5. **Feedback within 1 s**: a button shows its pending state at once and is `aria-disabled` until the server answers, so focus stays on it; never a silent double submit.
6. **Errors say what to do**: show the server's `message`; next to it, the one action that fixes the case (retry, edit field, contact Staff).
7. **Preserve input**: a failed submit keeps every field; leaving a dirty form asks first.
8. **Times and money**: times in the viewer's timezone with the zone shown inline, or in a tooltip that follows §9.5; VND with thousands separators, never decimals.
9. **Alerts outrank everything**: the incident banner (REQ-EVT-01) sits above every page and is never covered by a modal. A new SOS is announced with `role="alert"` even while a dialog is open: while a modal dialog is open the alert is also rendered inside that dialog, because a screen reader treats content outside a modal as inert and would not announce it; the banner's action is reachable once the dialog closes, and a dialog open at that moment shows an Open incident button (leader, 2026-11-03, D-096).
10. **Sandbox and disclaimers** are visible, never hidden in a tooltip (NFR-UI-03, NFR-LEG-05).
11. **Reuse before inventing**: a new pattern needs a component in `shared/ui` and a line in the PR's Design section saying why the existing ones did not fit.

---

## 9. CollectionView: One Module Renders Every List of Records (D-096)

Every list of records (devices, contracts, invoices, members, maintenance jobs, audit entries) renders through one shared module, `CollectionView`, in `shared/ui/collection-view/`. It is a library component: it knows nothing about a module, an endpoint or the server's result set. A page supplies the data, the fields and the actions; a page never builds its own table, card grid, selection logic or toolbar. §4 Pattern A is the Details view of this module. Page layout around it is §10.

### 9.1 What a page supplies

| Input | Content |
|---|---|
| `items` | The current page of a TanStack Query result, paged by the server (§8.4) |
| `fields` | Key, label, renderer, `sortable`, `hideWithPane` (§10.8), and which fields the compact views show |
| `itemName` | The text that names one item in accessible names and confirmations ("TL-0042") |
| `itemActions` | Plain per-item actions: icon, label, handler, permission |
| `transitions` | The allowed state transitions per item, from the module spec's state machine (D-030), filtered by the caller's CASL abilities |
| `bulkActions` | Actions that apply to a selection |
| `views`, `defaultView` | The views this collection offers |
| `details` | The fields, image slot and links the details pane shows (§9.8) |
| `emptyState` | Message and call to action (§4 Pattern A) |

### 9.2 Views

| View | Layout | Markup |
|---|---|---|
| Details | Table, one column per field | Native `<table>`, `<caption>` with the collection name, `<th scope="col">` |
| List | One line per item | `<ul>` of `<li>` |
| Grid | Dense tiles | `<ul>` of `<li>` |
| Small, Medium, Large cards | Cards of three sizes | `<ul>` of `<li>`, each card titled by a heading with the item name |

The Details view is a native table. It becomes an ARIA `grid` only if the full grid keyboard model is built.

The view switcher is one split button, never a row of icon buttons (§10.2): the icon button shows the current view and switches to the next one on click (its name says both, "View: Details list. Switch to List"); the chevron button beside it opens the menu of all views. Each menu item carries the view icon and name, and the current one says "(current)" in its text, so the state is not shown by an icon alone (1.4.1). Filter and Sort follow the same pattern ("Show: <filter>", "Sort: <order>"). Switching view keeps the selection, the search, the filter and the sort.

### 9.3 Command bar

Exactly one row above the items at 1280 px (52 px high), sticky at the top of the collection. A second row is not allowed: what does not fit becomes a dropdown (§10.2). Left to right:

1. **Select-all checkbox**, tri-state (§9.4).
2. **Commands**: with no selection, the collection commands (Register device, Export); with a selection, the bulk actions, named verb plus count ("Check in 3 units").
3. **Selection count**: "3 selected" and a Clear selection button, shown only while items are selected.
4. **Search** field with a visible label or a programmatic name ("Search devices"); a placeholder is never the only label (§3).
5. **Show (filter), Sort, View** dropdowns and the Details pane toggle (`aria-pressed`), right-aligned. The result count is in the Show dropdown text and in the collection's live region; while a search is active a short visible "N match" appears next to the field.

Command buttons may show a short visible label ("Live map") when their accessible name is longer ("Show 3 units on live map"); the visible label appears inside the name (2.5.3).

- The bar is a `role="group"` with an `aria-label`, not a `role="toolbar"` unless Arrow-key navigation is built across all its controls (4.1.2).
- The select-all checkbox, the Clear selection button and the search field are tab stops of their own; the search field stays outside any toolbar because Left and Right Arrow edit its text.
- A list with nothing to filter, sort or switch (one or two records, such as a contract's invoices) hides its command bar; its item actions stay.
- At phone width the bar stays one row (§10.5).

### 9.4 Selection

1. Every item has a checkbox named "Select <itemName>".
2. Click or Space toggles one item and sets the range anchor. Shift+click and Shift+Space select every item from the anchor to this one.
3. The select-all checkbox selects **the items on the current page only**, never the server's matches across pages: the module holds no knowledge of the result set beyond the page it was given (leader, 2026-11-03). It shows checked, unchecked or mixed (`aria-checked="mixed"`).
4. **A search, filter or sort change clears the selection** and the live region says "Selection cleared" (leader, 2026-11-03), so a bulk action never acts on items the user can no longer see. A view change keeps it (§9.2).
5. Escape clears the selection when no tooltip, menu or dialog is open. Escape always closes the innermost open layer first: tooltip, then menu, then dialog, then selection.
6. Bulk actions are named verb plus count plus noun ("Check in 3 units", "Retire 2 devices"). The accessible name is the same text.
7. Selection never requires dragging: no drag-to-select, and no drag reorder without an equivalent button (2.5.7).

### 9.5 Per-item actions and tooltips

Per-item actions are visible on every item in every view; they are never revealed on hover only. Show details (an Info icon) is the first action of every item (§9.8).

A plain action is an icon button:

- Its tooltip text is the verb ("Edit"). Its accessible name starts with the same text and adds the item ("Edit TL-0042"), so the name contains the visible label (2.5.3).
- The tooltip appears on pointer hover **and** on keyboard focus, stays while the pointer moves onto it, stays until hover and focus leave, and closes on Escape without moving focus (1.4.13). It is `role="tooltip"`.
- The native `title` attribute alone is not acceptable: it does not show on keyboard focus or touch and cannot be dismissed. Do not combine `title` with this tooltip.

### 9.6 State transitions

A state-machine transition (Active to Inactive, In Field to Return Due) is chosen from a Change status dropdown on the item:

1. A menu button (`aria-haspopup="menu"`, `aria-expanded`) whose visible text includes the current status as text (§8.3).
2. The menu lists only the transitions allowed from the current state for this user. Transitions that are not allowed are absent.
3. Destructive transitions come last, after a separator, named as verbs ("Retire device").
4. Menu keyboard: Enter, Space or Down Arrow opens and focuses the first item; Up and Down Arrow move; Home and End jump; Escape closes and returns focus to the menu button.
5. Choosing a transition opens a confirmation dialog (§8.1): the title names the object and the change ("Mark TL-0042 inactive?"), the confirm button repeats the verb, and initial focus is on Cancel for a destructive transition. On close, focus returns to the menu button, or to the next item if the item has left the result set.
6. In the bulk commands, the transition menu lists only transitions allowed for every selected item.

### 9.7 Accessibility contract

| Requirement | WCAG 2.2 |
|---|---|
| Toggle buttons expose `aria-pressed`; menus, menu buttons, checkboxes and dialogs expose role, name and state | 4.1.2 Name, Role, Value |
| Dropdowns are menu buttons: Enter, Space and Down Arrow open, Arrow keys move, Escape closes and returns focus to the button | 2.1.1 Keyboard |
| Every target is at least 24 by 24 CSS px; primary controls (§5 item 8) are at least 44 by 44, the team's stricter rule taken from 2.5.5 (AAA) | 2.5.8 Target Size (Minimum) |
| A sortable column header is a `<button>` inside the `<th>`; the sorted column carries `aria-sort="ascending"` or `"descending"`, the others carry none | 1.3.1, 4.1.2 |
| Selection count, result count, sort and page changes are announced through one polite live region per collection, present in the DOM before its first message ("3 selected", "57 devices, showing 1 to 20", "Sorted by Last seen, descending"); search announcements are debounced | 4.1.3 Status Messages |
| Focus is visible (§5 item 6) and never hidden behind the sticky command bar or the incident banner: the scroll container sets `scroll-padding-top` to their combined height | 2.4.7, 2.4.11 Focus Not Obscured (Minimum) |
| Status is shown as text in every view, never by colour alone; text on a coloured badge meets 4.5:1 | 1.4.1, 1.4.3 |
| Tooltips follow §9.5 | 1.4.13 |
| At 320 CSS px, every view reflows without horizontal page scroll; the Details view scrolls inside its own region with the hints of §10.6 | 1.4.10 Reflow |

### 9.8 Details pane

One shared pane in `CollectionView`. Every item offers Show details (first in its actions, and first in the phone Actions menu), and the command bar has a Details pane toggle with `aria-pressed`. The pane shows the item's fields, its image slot where the record has one, every item action as a labelled button with any unavailable reason as text, the Change status dropdown, and a link to the full page. Where it sits on each width is §10.8.

---

## 10. Page Layout (D-096)

These rules apply to every working page, not only to lists.

### 10.1 Vertical space first

Vertical space decides how much content a person sees at once, so it outranks every other layout concern on a working page.

1. Page chrome above the first item (header, lifecycle, action bar, tabs, command bar) takes at most 160 px at a 1280 by 800 viewport; each block states its height in the design.
2. A control set that would wrap to a second line becomes a dropdown or moves into a More menu; it never adds a row (§10.2).
3. One sticky bar per scroll context where possible. Where the page's actions sit depends on the page kind (D-096 amends D-084 for record pages only). A record page shows one entity with tabs and no step flow (contracts first): its actions share the sticky top row with its tabs (§10.4), so when a collection command bar sits under that row the page sets `scroll-padding-top` to their combined height. A page with a step flow (counter handover, return counter, contract request, organization review, maintenance) keeps D-084's action bar fixed to the bottom and sets `scroll-padding-top` to its header and `scroll-padding-bottom` to that bar. Either way a focused item is never hidden under a sticky bar (2.4.11).
4. Density never breaks a WCAG floor: targets stay at least 24 by 24 px and primary controls 44 px (§5 item 8); text stays at the type scale; reflow at 320 CSS px still works (1.4.10).

### 10.2 Dropdowns instead of a second row

Control sets that would take a second row become dropdowns. First application: the six view icons became one split View button (§9.2), and the command bar fits one row.

### 10.3 Dropdown buttons show a chevron

Every menu button (More actions, Change status, Show, Sort, the View chevron) shows a chevron-down icon to the right of its label as the hint that it opens a list. The icon is decorative (`aria-hidden`); the button keeps `aria-haspopup="menu"` and `aria-expanded`, opens on Enter, Space and Down Arrow, and closes on Escape with focus back on the button. Plain command buttons and icon buttons carry no chevron-down, so chevron-down always means "opens a list". The scroll buttons of §10.6 use chevron-left and chevron-right, which never open a list. `Menu` in `shared/ui` draws the chevron itself, and `StateChangeMenu` takes it too, so pages do not repeat a workaround.

### 10.4 Compact record pages

A record page shows one entity with tabs and no step flow (contracts first). Its page chrome is compact: breadcrumb, title, status and deadline in at most 64 px; the lifecycle strip and Next step in one card of 44 to 80 px; tabs and the record's actions share one sticky top row, with `scroll-padding-top` set to its height (2.4.11). This amends D-084 for record pages only (D-096); a page with a step flow keeps D-084's action bar fixed to the bottom (§10.1 rule 3). Plain actions in command bars and on items are icon buttons with an accessible name and the tooltip of §9.5; state-machine transitions are a Change status dropdown (§9.6).

### 10.5 Phone layout (360 px)

On record pages: tabs pinned at the top in one row (they scroll sideways when they do not fit, §10.6); the page's actions sit in a bar pinned to the bottom, primary action widest, More actions beside it, a disabled action's reason on its own line above; the lifecycle collapses to one line ("Step 3 of 7: Active, since 10 Nov") with a disclosure that opens the full list; figures shown as stat cards on desktop become one compact definition list. The page sets `scroll-padding-top` and `scroll-padding-bottom` to the pinned bars' heights so a focused control is never hidden under them (2.4.11).

In `CollectionView` at phone width the command bar keeps one row (the select-all checkbox, a Search icon button that opens the field in place, a Sort dropdown that also holds the Show filters, the split View button); with a selection it shows the count and one Actions dropdown holding the bulk actions and status changes; each item's icon actions and Change status collapse into one Actions dropdown, status changes prefixed "Change status:", destructive ones last; the default view is List.

### 10.6 Sideways scroll strips

1. Any strip that scrolls sideways (tabs on a phone, a wide Details table, a chip or step row) shows, on each side that has more content, a fading edge from the surface colour and an arrow button (chevron-left or chevron-right, never chevron-down, §10.3; 32 by 44 px) that scrolls about 70 % of the visible width. The hints appear and disappear with the scroll position. The selected tab is scrolled into view on load. Scrolling is instant when the user asks for reduced motion (2.3.3).
2. The arrows are pointer aids, kept out of the tab order and hidden from screen readers: keyboard users reach every item with Tab or Arrow keys and the focused item scrolls into view (2.1.1, 1.4.10).
3. A strip that holds no focusable item (the lifecycle strip, a stepper) takes `tabindex="0"` and an accessible name while it overflows, so keyboard users can scroll it (2.1.1); it leaves the tab order when everything fits.
4. Every scroll strip is `position: relative`, so absolutely positioned descendants such as visually hidden text stay inside it; without that they widened the 360 px page and broke reflow (1.4.10).

### 10.7 Target size

Checkboxes are 24 by 24 px inside a 36 to 44 px label; a standalone link (an asset tag, an invoice number, Back to overview) is `inline-flex` with a 24 px minimum height (2.5.8). Links inside a sentence are exempt.

### 10.8 Details pane placement

The pane of §9.8 adapts to the window: from 1100 px it is a non-modal `aside` pushed aside beside the list (focus moves to its heading; Escape or the close button closes it); from 600 px the design system's `Drawer` from the right, over the page; below 600 px the same `Drawer` as a bottom sheet. Both drawers trap focus and return it on close.

While the pane is pushed aside, rows never scroll sideways and show no scroll hints: columns the pane already shows are marked `hideWithPane` and leave the table, and the Status change column leaves too, because the pane holds that dropdown. A `hideWithPane` column also leaves when the list's own container is narrower than 1100 px, measured by a CSS container query on that container (`container-type: inline-size`), so it needs no component state. When a page has several related lists (Money: Invoices and Payments), the page names one container as `paneHost`: the pane sits beside all of them and every list in it fits the narrower width.

---

## 11. Leader UX rules (2026-11-05, binding for every screen)

Set by the leader on 2026-11-05 after walking the staging. They sharpen §9 and §10; where an older line differs, these win.
They apply to every screen of every role, and every review checks them.

### 11.1 The viewport rule

A screen never scrolls by itself. Only a nested element that needs it scrolls: the list or data table, the details pane,
a long form body, a log. The document never scrolls; the shell fits the viewport at every width; the page header, the
command bar and the action bar never scroll away; no double scrollbars, no scroll jump on load, on selection or when a pane
opens. On wide pages (devices, incidents, contracts, invoices) only the data table scrolls. Check:
`document.scrollingElement.scrollHeight === clientHeight` on every route. Full-bleed pages (live map, fleet map) fit the
viewport exactly; the map fills the remaining space and the device list scrolls inside itself.

### 11.2 Sorting from the column header

Every sortable column header is a button that cycles **ascending, descending, default** (the list's default order). The
sorted column carries `aria-sort`; an arrow shows the direction; the change is announced in the collection's live region
(§9.7). The Sort dropdown of the command bar (§9.3) offers the same orders for phone and card views.

### 11.3 The status is the state-change control

There is no separate "Status change" column. The status cell shows the status badge; when the user may change the state,
the badge itself is the menu button of §9.6 with a chevron (§10.3) as the hint, and it opens the allowed transitions.
Without an allowed transition the badge has no chevron and is not a button. This saves a column of horizontal space and
keeps the state and its change in one place.

### 11.4 Per-item actions keep their place

The actions column is right-aligned. The order is fixed from the right: Show details is the rightmost action and never
moves; any further action, and any action an item gains in some states, is added to its **left**. A button never shifts
because another one appeared, so the user's hand finds it in the same place every time. A missing action leaves no gap.

### 11.5 Visual WCAG check

Every screen change is checked visually against WCAG 2.2 AA (the UI standard `specs/frontend/ui-design/0-ui-standard.md`
in treklink-web): screenshots at 1440, 1280, 900, 360 and 320 CSS px in both themes, looked at, plus axe; vertical space
first, as §10.1 says.

### 11.6 Where these rules live

This section is the project-wide source. `0-ui-standard.md` in treklink-web restates the checks for builders, and the
leader's prompt-orchestrator harness (`ruskicoder/system-prompts`) validates and generalizes them for every project.

