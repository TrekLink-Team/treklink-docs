# 13 — Diagram & Figure Conventions

How diagrams are authored, how figures are placed, and what the build enforces. These rules exist
because these documents are **printed and photocopied** for a council, and because the most common
grading outcome in this faculty is *"passed but must revise and resubmit documentation."*

---

## 1. Mermaid only

Mermaid is the only diagram language. Never PlantUML, never a drawing tool, never a screenshot of a
diagram pasted back into a document. Diagrams are source, so they regenerate instead of rotting.

**Pinned version: Mermaid 12.0.0**, cached at `_docs/handbook/assets/`. The pin is in
[`build_handbook.py`](../handbook/build_handbook.py) (`MERMAID_VERSION`). Bumping it requires
re-rendering every diagram in the corpus and checking none regressed — there is a harness for this,
see §6.

---

## 2. Process flows are swimlanes

> **A flow that involves more than one actor is a `swimlane-beta` diagram, not a `flowchart`.**

This is the format the course itself supplies as the worked example
(`Documents/templates/Main flows_ex02.jpg`), and it is what the supervisor used for the TrekLink
Main Flow set. A `flowchart` with `subgraph` blocks *looks* like lanes and is not — the lanes do not
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
  never a phase — phases are the flow direction.
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
***Figure 3*** — What the figure shows, and the one thing the reader should take from it.
Placement: rotated plate, 182.0 x 249.5 mm, labels at 7.52 pt.
```

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
diagram** — change a `flowchart LR` to `TB`, shorten labels, reduce the chain depth, or split it into
two or three figures. A figure below the floor is a *note, not a build failure*: fitting the page
without clipping matters more than reaching 7 pt.

### Figures currently carried below the floor, by decision

**None.** As of 2026-09-17 the corpus is 27 figures and every one clears the floor; the lowest is
7.40 pt. Three that did not were re-sourced rather than excused: the session-lifecycle sequence
diagram and the two eleven-step process flows were each split into two figures.

If a figure ever has to be carried below the floor, record it here with its measurement and the
reason the obvious fix was worse. This table is a record of deliberate exceptions, not a place to
park failures — anything below 7 pt that is not listed here is a defect.

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
   kinds — never `fill:#1e40af`.

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
the final millimetre box, and the effective point size — the same computation the build uses. Paste
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
  three figures for this reason — as one diagram it renders 6696 px wide and prints at 1.58 pt.
- **`<br/>` inside a label is free vertically** and cheap horizontally. Prefer two short lines over
  one long one.
- **Emoji inflate width** and do not survive photocopying. Do not use them in figures.
