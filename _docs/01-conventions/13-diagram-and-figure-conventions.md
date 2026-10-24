# 13: Diagram & Figure Conventions

How diagrams are authored, how figures are placed, and what the build enforces. These rules exist
because these documents are **printed and photocopied** for a council, and because the most common
grading outcome in this faculty is *"passed but must revise and resubmit documentation."*

---

## 1. Mermaid only

Mermaid is the only diagram language. Never PlantUML, never a drawing tool, never a screenshot of a
diagram pasted back into a document. Diagrams are source, so they regenerate instead of rotting.

> **Exception (D-065, 2026-10-24)**: diagrams in graded reports, the Design Brief and review decks are
> PlantUML, because the course grades UML notation that Mermaid does not draw. Activity (swimlane)
> and state machine diagrams in reports are Mermaid first (D-065 as amended 2026-10-25). Specs and this handbook stay Mermaid. Still never a drawing tool and never a pasted screenshot.
>
> **What a PlantUML diagram may contain and where each element goes is chapter 16 (D-069).** Start
> every report figure from its skeleton in `_docs/02-templates/puml/`.

**Pinned version: Mermaid 12.0.0**, cached at `_docs/handbook/assets/`. The pin is in
[`build_handbook.py`](../handbook/build_handbook.py) (`MERMAID_VERSION`). Bumping it requires
re-rendering every diagram in the corpus and checking none regressed, there is a harness for this,
see §6.

---

## 1.1 The handbook gate: check, look, cross-check (D-067)

> **Every diagram, and every spec or report section a diagram is drawn from, passes three checks
> before it is called done: it is checked against the course mistakes handbook, its rendered image is
> looked at, and it is cross-checked against the other diagrams and the code.** Writing the source is
> not the same as finishing the figure.

The handbook is `capstone/Documents/templates/Cam-nang-tranh-loi-Capstone-SE.pdf` ("Cẩm nang tránh
lỗi khi làm Capstone Project ngành Kỹ thuật phần mềm"), issued by the course. The supervisor asked on
2026-10-24 whether the team had read it, after rejecting diagrams that broke its §2 rules. Reports are
graded on notation, so this gate is part of the definition of done.

### Check 1: re-read the handbook section, every time

Before drafting or editing a figure, open the handbook section for its type and work from it, not from
memory. A paraphrase cannot replace the source. An agent that cannot read the PDF extracts it first
(`pdftotext -layout`); if it cannot do that either, it stops and says so.

| Writing | Handbook sections to re-read |
|---|---|
| Use case diagram | §2.1, §2.6, §1.5 (two versions of one diagram, include and extend direction) |
| ERD, database design | §2.2 |
| Architecture, deployment, IoT hardware | §2.3, §1.5 |
| Class, state machine | §2.4 |
| Sequence | §2.5 |
| Context, activity, product overview, process model | §2.6 |
| Any figure in a graded document | §1.3, §1.6 (captions below figures, cross-references, legibility) |
| Requirements, business rules, specs (`requirements.md`, `design.md`, SRS, SDD text) | §1.4, §1.5, §3, §4 |

The most frequent violations, in the team's own words; the handbook stays authoritative:

- **Context**: one external entity per box, never two merged; one arrow per direction, never a
  bidirectional arrow; flow labels are nouns; the system is a single process.
- **Use case**: one overview diagram that fits one page, CRUD folded into `Manage X`; detail
  diagrams are extra, never a replacement. Stick-figure actors; plain lines between actor and use
  case; `include` and `extend` as dashed open arrows in the right direction; names are verb plus
  object; a use case is a function, not a step of a flow.
- **ERD**: one notation for the whole document (crow's foot or Chen) with its legend; one overall
  diagram; main entities at an abstract level; cardinality decided in both directions; 0..n and 1..n
  distinguishable. Report 4 also shows the real installed database.
- **Architecture**: overview and detail in separate figures; frontend, backend, database and every
  third party as separate blocks; both request and response paths; components inside the framework
  that contains them; every queue, socket or cache traceable to code; for IoT, a hardware diagram
  with each device, its specifications and its protocol.
- **Class and state machine**: class diagrams for the complex main use cases only, with correct
  multiplicities; every transition names its trigger; state machines in the design body, not an
  appendix.
- **Sequence**: numbered messages, activation bars, `:Object` names, a named page (`Login Page`, not
  `UI`), actor to page to controller to service to repository, `alt` split into labelled lanes,
  exception paths, one use case per diagram.
- **Activity**: decisions are diamonds; multi-actor flows use swimlanes (§2).
- **Every figure**: a title and caption below it, a cross-reference in the text before it, legible
  at print size, and the same names, actors and flows as every other figure.

### Check 2: look at the rendered image

Render the figure and look at the image itself. Reading the source does not count, because layout,
arrowheads, overlaps and clipped labels only exist in the render.

- An agent with image input opens the rendered PNG (or the page of the built PDF) and checks it
  against the Check 1 list.
- An agent without image input says so, and a human opens the image instead. The figure is not done
  until one of the two has looked.
- After the document is built, sample the built PDF pages that carry figures; a figure that rendered
  correctly alone can still be scaled below legibility in the document (§4).

### Check 3: cross-check

- The same use case, actor, entity and state names across the use case, sequence, class, state,
  ERD and architecture figures and the SRS and SDD text (handbook §2.6, §12 D-7 checklist).
- Each architecture block points to a real path in `treklink-web` (handbook §2.3, §1.5); a block with
  no code yet is marked planned or left out (Review 2 checklist, roadmap).
- Each entity and attribute matches `backend/prisma/schema.prisma`; each state machine matches the
  state enum and the transition table in the module's `design.md`.

### Record

The PR body, or the session file for `capstone` work, carries one line per changed figure: the
handbook sections re-read, who looked at the render (agent or member name), and what it was
cross-checked against. A figure without that line is not done, and a reviewer sends it back.

---

## 2. Process flows are swimlanes

> **A flow that involves more than one actor is a `swimlane-beta` diagram, not a `flowchart`.**

This is the format the course itself supplies as the worked example
(`Documents/templates/Main flows_ex02.jpg`), and it is what the supervisor used for the TrekLink
Main Flow set. A `flowchart` with `subgraph` blocks *looks* like lanes and is not, the lanes do not
constrain layout, so the actor partition is decorative rather than structural.

```
swimlane-beta TB
    subgraph customer["Customer"]
        c1[Submit booking request]
    end
    subgraph staff["Staff"]
        t1[Confirm booking]
    end
    c1 --> t1
```

Rules:

- **One `subgraph` per actor.** Top-level subgraphs render as lanes. A lane is an actor or a system,
  never a phase, phases are the flow direction.
- **Orientation `TB`.** Lanes become columns and the flow runs down the page, which is what fits A4
  portrait. `LR` swimlanes routinely render four to five thousand pixels wide and print at 2–3 pt.
- Node and edge syntax is flowchart syntax: `id[Rect]`, `id{Decision}`, `A --> B`, `A -->|label| B`.
- **Requires Mermaid ≥ 11.16.0.** `swimlane-beta` does not exist below that and renders as an error
  block. Our pin at 12.0.0 satisfies this; do not downgrade.

Use a plain `flowchart` only for structures that have no actors: context diagrams, feature trees,
decision trees, architecture diagrams.

---

## 3. Numbering and captions

Every figure and table carries a number and a caption, and is referenced in the body as
`See Figure N` or `See Table N` **before** it appears. No orphaned visuals.

Numbering is **per source document**, starting at 1. The handbook build renumbers continuously
across the assembled PDF and rewrites the in-text references to match, so a document reads correctly
both standalone in the repository and bound into the handbook.

Caption format, immediately after the diagram block:

```
***Figure 3***: What the figure shows, and the one thing the reader should take from it.
Placement: rotated plate, 182.0 x 249.5 mm, labels at 7.52 pt.
```

> [!IMPORTANT]
> **The separator is a colon, and it is parsed.** `build_handbook.py` matches
> `^\*\*\*Figure (\d+)\*\*\*: ` to renumber captions and to pull each one into its figure element,
> and the handbook workflow's sanity check counts `Figure N: ` in the rendered PDF text. A caption
> written with any other separator is silently dropped from the handbook. The form was an em dash
> until 2026-09-22 and changed with the prose sweep (D-024).

The placement clause is written by the author from the measurement harness output (§6). It is how a
reviewer can tell at a glance that the figure was fitted rather than dropped in and hoped for.

---

## 4. Figure placement

Placement is **computed, not authored**. `plan_figure` in
[`build_handbook.py`](../handbook/build_handbook.py) renders each diagram headless, measures its
viewBox and its smallest rendered label, and places it accordingly.

| Rule | Value |
|---|---|
| Page orientation | A4 portrait, always. A wide diagram is turned, never the sheet |
| Page box | 182 × 266 mm (A4 minus the handbook's 15/14/16/14 mm margins) |
| Legibility floor | 7 pt. Above it a figure stays inline in the text column |
| Below the floor | The figure takes a plate page, turned counter-clockwise if turning gives it more room |
| Rotation | Inside the SVG coordinate system. Never a CSS transform |
| Caption | Upright, and inside the `figure` element so a break cannot separate the two |
| Sizing | Width and height both set, in millimetres. Never `height: auto` |

Do not force a page break before a figure. The break is what strands captions on near-empty pages.
`break-inside: avoid` moves the figure on its own and lets the text above it keep flowing.

If the build reports a figure below the floor, layout has done what it can. **Re-source the
diagram**, change a `flowchart LR` to `TB`, shorten labels, reduce the chain depth, or split it into
two or three figures. A figure below the floor is a *note, not a build failure*: fitting the page
without clipping matters more than reaching 7 pt.

### 4.1 Graded documents: upright figures, the page turns instead

**Leader instructions, 2026-09-25.** These apply to every graded document under
`capstone/Documents/reports/` (SRS, SDD, test documents, the final report) and to their slides.

1. **Every diagram is upright. Never rotate a diagram.** A page shown on a projector must not need
   the viewer to tilt their head.
2. **The page fits the diagram.** A wide diagram gets a landscape page of its own, as a separate
   landscape section; a tall one gets a portrait page of its own. The surrounding text stays
   portrait.
3. **Nothing is clipped or overflows.** A figure fits the page box on both axes. This is the hard
   requirement.
4. **The 7 pt floor is best practice, not a gate.** Aim for it; re-source or split a diagram when
   that is cheap. A figure that fits its page without clipping but stays below 7 pt is acceptable.
5. **The caption is the figure's title only.** No placement clause, no measurement, no status note,
   no explanatory second sentence. The handbook keeps its placement clause (§3); graded documents
   do not.
6. **A diagram carries the full information** (leader, 2026-10-19). A sequence message keeps its
   whole call, arguments and result; a long one is pre-broken with `<br/>` rather than shortened.
   Explanation that is not a message, a guard or a state (why a step exists, which rule it
   enforces) goes into a Mermaid `Note`, never into the message text and never only into the
   surrounding prose.

| Rule | Value |
|---|---|
| Page box | The report template's text area: A4, 1-inch margins; 159 x 246 mm portrait, 246 x 159 mm landscape |
| Inline | Up to 159 x 225 mm in the text column, leaving room for the caption |
| Own page | A figure below 7 pt inline gets a page of its own: portrait up to 159 x 235 mm, or landscape up to 246 x 150 mm, whichever gives it the larger scale |
| Rotation | None, in any graded document |
| Caption | Below the figure, title only (chapter 15) |

The handbook PDF (§4 above) keeps its rotated plates, because the handbook is built for print and
is not graded. The report generator lives in `capstone/scripts/srs/` (`measure_figures.py` computes
the placement, `build_srs.py` emits the landscape sections).

### Figures currently below the floor

**Handbook: none.** As of 2026-09-17 the corpus is 27 figures and every one clears the floor; the lowest is
7.40 pt.

**Report 3 (SRS), measured 2026-10-14.** Each fits its page without clipping (rule 3), so each is
acceptable under rule 4. The Entity Relationship Diagram is drawn left to right, which measured higher
than top to bottom; it keeps its key attributes because the SRS cites them.

| Report figure | Diagram | Source size | Placement | Labels |
|---|---|---|---|---|
| SRS Figure 13 | Feature Tree, part 1 of 4: Identity and Organizations, Asset Management, Rental Contracts | 572 x 1664 px | portrait page, 81 x 235 mm | 6.41 pt |
| SRS Figure 17 | MF-01 Organization onboarding to Rental contract to Handover | 1070 x 1001 px | landscape page, 160 x 150 mm | 6.80 pt |
| SRS Figure 18 | MF-02 Field data to Field Station to Cloud synchronization | 816 x 1608 px | portrait page, 119 x 235 mm | 6.63 pt |
| SRS Figure 19 | MF-03 SOS to Tiered alert to Escalation | 1070 x 1218 px | portrait page, 159 x 181 mm | 6.74 pt |
| SRS Figure 22 | Entity Relationship Diagram of the core entities | 1973 x 1211 px | landscape page, 244 x 150 mm | 4.92 pt |
| SRS Figure 23 | Device lifecycle state machine | 954 x 1709 px | portrait page, 131 x 235 mm | 6.24 pt |

**Report 4 (SDD), measured 2026-10-18** (75 figures, rebuilt on the SEP490 Report 4 template; 41 below the floor, 30 of 73 on 2026-10-14). Each fits its page without clipping (rule 3), so each is
acceptable under rule 4. The rise comes from two changes of 2026-10-18: the hardware view, and sequence messages pre-broken with `<br/>` so that Mermaid no longer hyphenates long tokens, which makes those diagrams taller. The re-sourcing already done: message numbers written into the text instead
of Mermaid's `autonumber`, whose 12 px labels set the floor; the `PostgreSQL` lane folded into the
repository; long sequences split into parts; `wrap` on; layout direction chosen per figure by measuring
both; ERD parts and the overall ERD drawn without attribute blocks; class diagrams that grew past one concern
split into core, maintenance, loss-case or compliance-case views. What remains is height or lane count: the sequence
diagrams with seven lanes (page, controller, service, repository and the services of other modules)
would need a third part each, which splits one use case's transaction across figures.

| Report figure | Diagram | Source size | Placement | Labels |
|---|---|---|---|---|
| SDD Figure 1 | Context diagram of the TrekLink Rental Platform | 1740 x 630 px | landscape page, 246 x 89 mm | 6.41 pt |
| SDD Figure 2 | System architecture | 1048 x 1881 px | portrait page, 131 x 235 mm | 5.67 pt |
| SDD Figure 3 | Deployment view | 1663 x 714 px | landscape page, 246 x 106 mm | 6.71 pt |
| SDD Figure 4 | Hardware connections of the IoT part | 2640 x 346 px | landscape page, 246 x 32 mm | 4.23 pt |
| SDD Figure 5 | Package diagram: backend modules and their dependencies | 1688 x 1380 px | landscape page, 183 x 150 mm | 4.93 pt |
| SDD Figure 7 | Entity Relationship Diagram of the main entities | 1636 x 696 px | landscape page, 246 x 105 mm | 5.97 pt |
| SDD Figure 10 | Physical schema, part 3 of 9: organizations | 1434 x 785 px | landscape page, 246 x 135 mm | 6.81 pt |
| SDD Figure 11 | Physical schema, part 4 of 9: devices | 1202 x 1550 px | portrait page, 159 x 205 mm | 5.25 pt |
| SDD Figure 13 | Physical schema, part 6 of 9: billing | 987 x 911 px | landscape page, 163 x 150 mm | 6.54 pt |
| SDD Figure 17 | Class diagram of the organizations module | 1663 x 862 px | landscape page, 246 x 127 mm | 6.71 pt |
| SDD Figure 18 | Class diagram of the rentals module | 1906 x 1103 px | landscape page, 246 x 142 mm | 5.85 pt |
| SDD Figure 19 | Sequence diagram of UC-01 Register Organization | 1098 x 1393 px | portrait page, 159 x 202 mm | 6.57 pt |
| SDD Figure 22 | Sequence diagram of UC-15 Request Rental Contract | 1283 x 1133 px | landscape page, 170 x 150 mm | 6.00 pt |
| SDD Figure 23 | Sequence diagram of UC-17 Approve Rental Contract | 1273 x 1093 px | landscape page, 175 x 150 mm | 6.22 pt |
| SDD Figure 25 | Sequence diagram of UC-20 Hand Over Devices, part 2 of 2: signed handover | 1320 x 1253 px | portrait page, 159 x 151 mm | 5.46 pt |
| SDD Figure 28 | Class diagram of the gateway-sync module | 1593 x 1060 px | landscape page, 226 x 150 mm | 6.42 pt |
| SDD Figure 29 | Sequence diagram of UC-06 Manage API Keys and Field Station Credentials, part 1 of 2: credential and download | 1053 x 1393 px | portrait page, 159 x 210 mm | 6.85 pt |
| SDD Figure 30 | Sequence diagram of UC-06 Manage API Keys and Field Station Credentials, part 2 of 2: broker check | 1157 x 983 px | landscape page, 177 x 150 mm | 6.92 pt |
| SDD Figure 31 | Sequence diagram of UC-26 Ingest Field Event, part 1 of 2: receive and attribute | 1073 x 1403 px | portrait page, 159 x 208 mm | 6.72 pt |
| SDD Figure 32 | Sequence diagram of UC-26 Ingest Field Event, part 2 of 2: persist and hand off | 1048 x 1300 px | portrait page, 159 x 197 mm | 6.88 pt |
| SDD Figure 37 | Sequence diagram of UC-29 Create Incident, part 1 of 2: correlation and routing | 1094 x 1055 px | portrait page, 159 x 153 mm | 6.59 pt |
| SDD Figure 40 | Sequence diagram of UC-32 Acknowledge Incident | 1125 x 1353 px | portrait page, 159 x 191 mm | 6.41 pt |
| SDD Figure 41 | Sequence diagram of UC-33 Report Incident Status | 932 x 1573 px | portrait page, 139 x 235 mm | 6.78 pt |
| SDD Figure 42 | Sequence diagram of UC-35 Report to Authorities | 1139 x 1183 px | portrait page, 159 x 165 mm | 6.33 pt |
| SDD Figure 45 | Class diagram of the monitoring module | 1805 x 994 px | landscape page, 246 x 135 mm | 6.18 pt |
| SDD Figure 53 | Class diagram of the devices module for loss cases | 1616 x 854 px | landscape page, 246 x 130 mm | 6.90 pt |
| SDD Figure 54 | Class diagram of the billing module | 1431 x 1068 px | landscape page, 201 x 150 mm | 6.37 pt |
| SDD Figure 56 | Sequence diagram of UC-43 Check In Device | 1345 x 1247 px | landscape page, 162 x 150 mm | 5.46 pt |
| SDD Figure 58 | Sequence diagram of UC-44 Reset and Inspect Device, part 2 of 2: inspection | 1299 x 1340 px | portrait page, 159 x 164 mm | 5.55 pt |
| SDD Figure 59 | Sequence diagram of UC-65 Scan for Due Service | 1109 x 1118 px | portrait page, 159 x 160 mm | 6.50 pt |
| SDD Figure 60 | Sequence diagram of UC-52 Record Maintenance, part 1 of 2: open and estimate | 1173 x 1483 px | portrait page, 159 x 201 mm | 6.15 pt |
| SDD Figure 61 | Sequence diagram of UC-52 Record Maintenance, part 2 of 2: completion | 1255 x 1418 px | portrait page, 159 x 180 mm | 5.75 pt |
| SDD Figure 62 | Sequence diagram of UC-64 Approve Maintenance Cost | 1072 x 1113 px | portrait page, 159 x 165 mm | 6.73 pt |
| SDD Figure 63 | Sequence diagram of UC-49 Report Lost Device | 1068 x 1133 px | portrait page, 159 x 169 mm | 6.75 pt |
| SDD Figure 64 | Sequence diagram of UC-60 Resolve Loss Case, part 1 of 2: triage | 1234 x 1270 px | portrait page, 159 x 164 mm | 5.84 pt |
| SDD Figure 65 | Sequence diagram of UC-60 Resolve Loss Case, part 2 of 2: confirmation and settlement | 1077 x 1270 px | portrait page, 159 x 187 mm | 6.70 pt |
| SDD Figure 66 | Sequence diagram of UC-61 Replace Device on Contract | 1076 x 1350 px | portrait page, 159 x 199 mm | 6.70 pt |
| SDD Figure 70 | Sequence diagram of UC-48 Approve Damage Charge | 1170 x 1303 px | portrait page, 159 x 177 mm | 6.16 pt |
| SDD Figure 71 | Sequence diagram of UC-63 Handle Compliance Case | 1295 x 1473 px | portrait page, 159 x 181 mm | 5.57 pt |
| SDD Figure 72 | Sequence diagram of UC-51 Close Rental Contract | 1174 x 1423 px | portrait page, 159 x 193 mm | 6.14 pt |
| SDD Figure 73 | Device lifecycle | 954 x 1709 px | portrait page, 131 x 235 mm | 6.24 pt |


If a figure ever has to be carried below the floor, record it here with its measurement and the
reason the obvious fix was worse. This table is a record of deliberate exceptions, not a place to
park failures, anything below 7 pt that is not listed here is a defect.

---

## 5. Hard rules for every figure

Enforced by the generator. Do not work around them in a source document.

1. A figure fits inside its page box on **both** axes. Nothing is clipped, cropped, or allowed to
   run past a margin.
2. Width and height are both set, in millimetres. Never `height: auto`, which constrains one axis
   and lets the other overflow.
3. A wide figure is turned counter-clockwise, **inside the SVG coordinate system**. Never with a CSS
   transform: a transformed box paints in one place and paginates in another, which prints content
   on the wrong page, clipped.
4. The caption stays upright and lives inside the `figure` element, so no break can separate it from
   what it names.
5. No figure forces a page break. `break-inside: avoid` moves it on its own and lets the text above
   keep flowing into the space.
6. **Monochrome.** A figure must not depend on hue to be understood, because these documents are
   printed and photocopied. Use hatching, dashes, or line weight. In Mermaid that means
   `style X stroke-width:3px` to emphasise a node, and `-.->` versus `-->` to distinguish edge
   kinds, never `fill:#1e40af`.

### Raster figures

A drawn or scanned figure is placed by the same rules, fitted rather than judged, because label size
cannot be measured in a bitmap.

| Rule | Value |
|---|---|
| Minimum resolution | 200 dpi at final print size. Below that it is not print quality |
| Format | PNG, tracked in `_docs/assets/` |
| Rotation | Not supported. A raster has no coordinate system to turn inside |
| Colour | Subject to the monochrome rule above |

---

## 6. The measurement harness

Before committing a new or re-sourced diagram, measure it:

```bash
python3 _docs/handbook/build_handbook.py --measure _docs/00-project-context/05-main-flows.md
```

For each diagram it reports source size in pixels, smallest rendered label, the chosen placement,
the final millimetre box, and the effective point size, the same computation the build uses. Paste
the placement and point size into the caption.

To check the whole corpus, including after a Mermaid version bump:

```bash
python3 _docs/handbook/build_handbook.py --measure-all
```

A diagram that fails to render at all is a hard error and blocks the build. A diagram that renders
below the floor is reported and the build continues.

---

## 7. Practical guidance

Rules of thumb that come from actually fitting this project's diagrams:

- **Chain depth drives height.** In a `TB` swimlane the page height is the longest path, not the
  node count. Merging two sequential steps buys about 100 px.
- **Lane count drives width**, at roughly 260–270 px per lane regardless of label length. Five lanes
  is about the practical maximum for A4 portrait. Shortening node text does *not* narrow a lane.
- **A tree with more than ~16 leaves will not fit.** Split it by branch. The TrekLink feature tree is
  three figures for this reason, as one diagram it renders 6696 px wide and prints at 1.58 pt.
- **`<br/>` inside a label is free vertically** and cheap horizontally. Prefer two short lines over
  one long one.
- **Emoji inflate width** and do not survive photocopying. Do not use them in figures.
