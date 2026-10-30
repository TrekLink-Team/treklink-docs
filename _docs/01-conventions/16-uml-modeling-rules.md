# 16: UML Modeling Rules for Report Diagrams

What each diagram type may contain, where each element goes, and how to write that in PlantUML.
Chapter 13 governs rendering, captions and placement in a document; this chapter governs the
diagram itself. Recorded as **D-069**. Every diagram also passes the handbook gate of chapter 13
§1.1 (D-067): re-read the course handbook section, look at the render, cross-check.

---

## 1. Sources and tags

Each rule carries a tag naming where it comes from. When two sources disagree, the order is: course
handbook, then UML, then the rest.

| Tag | Source |
|---|---|
| `[HB]` | Course mistakes handbook, `capstone/Documents/templates/Cam-nang-tranh-loi-Capstone-SE.pdf` §2. It is what the reviewers grade. |
| `[UML]` | OMG UML 2.5 specification (ISO/IEC 19505 for 2.4.1). What is legal notation. |
| `[AMB]` | Scott W. Ambler, *The Elements of UML 2.0 Style* (Cambridge University Press, 2005). Layout and naming. |
| `[WB]` | Karl Wiegers and Joy Beatty, *Software Requirements*, 3rd ed. (Microsoft Press, 2013), chapter 8. The book the handbook cites for use cases. |
| `[PU]` | PlantUML language reference, plantuml.com. How to write it. |
| `[TL]` | A TrekLink decision where the sources are silent or leave a choice. |

---

## 2. Every diagram

1. Source is a `.puml` file next to the document that uses it, rendered by the pinned jar
   (`capstone/tools/plantuml-1.2026.9.jar`) through `capstone/scripts/srs/render_puml.py`, which needs
   Java 21 and Inkscape. Start from the skeleton for its type in `_docs/02-templates/puml/` and keep its
   `!include _treklink-style.puml`. State machine diagrams are Mermaid (§8), and sequence diagrams stay
   Mermaid in the reports until the leader rules on the PlantUML trial at final delivery (§6, D-065 as
   amended 2026-10-26): their `.mmd` sources are rendered by `capstone/scripts/srs/render_figures.sh`
   (Mermaid 12.0.0, neutral theme). `[TL]`
2. The shared style is monochrome, Arial, square corners, no shadows (chapter 13 §5 rule 6), with
   16 px text and 15 px labels so a wide figure stays near the 7 pt floor (chapter 13 §4.1). Do not
   override it per diagram. `[TL]`
3. Every diagram has a title naming its kind and subject, in UML frame style: `uc`, `class`, `sd`,
   `act`, `stm`, `cmp`, `ERD`. Sequences use `mainframe sd ...`. `[UML]` `[HB]`
4. Names are identical across every diagram, the SRS and SDD text, `schema.prisma` and the module
   `design.md`: the same actor, use case, entity and state is spelled the same everywhere. `[HB]`
5. Every line expresses a deliberate meaning. Two relationships of different kinds are never drawn
   with the same line style, and no line is drawn just because two things are related somehow. `[TL]`
6. Layout is part of correctness. A render with an element outside where its rule puts it, a label
   on top of another label, or a line crossing the whole figure fails Check 2 of chapter 13 §1.1.
   Fix the source, using the layout recipes in this chapter, before calling the figure done. `[TL]`
7. Three failed renders of the same figure trip the circuit breaker (`AGENTS.md` §5): stop and ask
   the leader instead of trying a fourth arrangement. `[TL]`
8. A large figure whose Graphviz render runs lines through boxes or titles may use
   `!pragma layout elk` (Java 21). It suits the deployment and IoT hardware diagrams; it tangled the
   package and architecture figures, which stay on Graphviz. An ERD never uses PlantUML's ELK: §9 rule 3.
   The leader vets each ELK render. `[PU]` `[TL]`
9. A figure carries no legend or explanatory note. Notation is explained once in the document's text
   or notation table, before or next to the first figure that uses it. A note inside a figure is kept
   only when it states a fact of the modelled system that no element can show. `[TL]`

---

## 3. Context diagram (Level-0 DFD)

Skeleton: `context.puml`.

1. The system is one process, drawn as a circle (Yourdon notation). Nothing of the system appears
   outside it; the Field Station and the MQTT broker are inside (D-068). PlantUML draws a `usecase`
   as an ellipse about 1.24 times wider than tall; write the process as a `usecase` and add the comment
   `' treklink: circle-process <alias>`, and `render_puml.py` redraws it as a circle with every flow cut
   back to its border. `[HB]` `[TL]`
2. Each external entity is a plain rectangle, one entity per box. Never merge two entities into one
   box, even when they send similar flows. `[HB]`
3. Each entity has one arrow into the system and one arrow out of it, drawn as separate arrows. Never
   a bidirectional arrow. An entity with no real flow in one direction is checked again: it usually
   has one (an SMTP server returns a delivery status). `[HB]` `[TL]`
4. Flow labels are nouns or noun phrases (`payment confirmation`), never verbs. `[HB]`
5. Layout: organization-side entities left, TrekLink-side entities and external services right. In
   PlantUML write a left entity's flows as `ENT --> SYS` and `ENT <-- SYS`, a right entity's as
   `SYS --> ENT` and `SYS <-- ENT`, under `left to right direction`. `[TL]` `[PU]`
6. Every flow in the diagram has a row in the SRS data-flow table with the same words. `[HB]`

---

## 4. Use case diagram

Skeleton: `usecase.puml`.

### 4.1 Notation

1. Actors are stick figures. A system actor carries `<<system>>`. Scheduled behaviour is started by
   a time actor; TrekLink's is named `Scheduler <<system>>`. `[UML]` `[AMB]`
2. An actor has binary associations only to use cases. Actors never connect to each other except by
   generalization. There is no aggregation or composition between actors: a "member of an
   organization" fact belongs in the class diagram and the ERD. `[UML]` `[AMB]`
3. Actor-to-use-case lines are plain lines with no arrowheads. `[AMB]` `[HB]`
4. `include` is a dashed open arrow from the base to the included use case; `extend` is a dashed open
   arrow from the extending use case to its base. Never a filled arrowhead. `[UML]` `[HB]`
5. Generalization is a solid line with a hollow triangle at the parent. Use it between actors when the
   child "is like" the parent and inherits every use case of the parent. `[UML]` `[AMB]`
6. An abstract actor (never instantiated, here `User`, `Organization Member`, `TrekLink Employee`)
   has its name in italics (`<i>User</i>`) and no association of its own. `[UML]` `[TL]`
7. Use case names are verb plus object (`Approve Rental Contract`). A use case is a function, never
   a step of a flow. `[HB]` `[AMB]`
8. At most two levels of include or extend. `[AMB]`

### 4.2 The TrekLink actor tree (D-069 rule 1)

```
User (abstract)
├── Organization Member (abstract)
│   └── Org Operator
│       └── Org Manager
└── TrekLink Employee (abstract)
    └── TrekLink Staff
        └── TrekLink Admin
Guest                       (not signed in, outside the tree)
Organization System, Payment Gateway, Email Service, TrekLink Device, Scheduler   (<<system>>)
```

Every use case diagram that shows an actor of the tree shows its parents up to the first abstract
level, so the inherited use cases are visible.

### 4.3 Layout

1. Primary actors (those who start the use case and get its value) on the left, primary first at the
   top. Secondary actors, TrekLink actors and `<<system>>` actors on the right. Never above or below
   the system boundary. `[AMB]` `[WB]`
2. All actors outside the boundary rectangle; all use cases inside. `[AMB]` `[HB]`
3. Actor trees are vertical, parent above child. Under `left to right direction` write
   `Child -left-|> Parent`; this is the form that renders vertically (verified 2026-10-25). `[AMB]` `[PU]`
4. A left actor's association is `ACTOR -- UC`. A right actor's is `UC --- ACTOR`: the extra dash
   puts it one rank further right, so it lands right of the boundary instead of under it. `[PU]` `[TL]`
5. An included use case sits right of its base; an extending use case below its base. Earlier steps
   of a process sit above later ones. `[AMB]`

### 4.4 Overview and detail

1. The SRS has exactly one overview use case diagram that fits one page: the main use cases, with
   related ones folded into `Manage X`, each oval listing the `UC-nn` it covers. `[HB]` (supervisor,
   2026-10-24)
2. Detail diagrams per Main Flow follow the overview and are never a replacement for it. One version
   of each diagram exists in a document. `[HB]`
3. A use case that cannot be reached from an actor through lines does not belong on the overview. `[TL]`

---

## 5. Class diagram

Skeleton: `class.puml`.

1. Draw class diagrams for the main, complex use cases, not for every function. `[HB]`
2. Show visibility (`+` public, `-` private, `#` protected) and the types of attributes,
   parameters and return values. Static members underlined (`{static}`). `[UML]`
3. Choose each relationship by its meaning, and label it with a role or a verb and multiplicity on
   both ends where it is an association:

   | Relationship | Line | Use when |
   |---|---|---|
   | Dependency | dashed open arrow `..>` | A uses B only while running an operation (a parameter, a local variable, a call). |
   | Association | solid line `--`, optional open arrow for navigability | A keeps a lasting reference to B. |
   | Aggregation | hollow diamond at the whole `o--` | B is a part of A but can outlive it (a device outlives a contract). |
   | Composition | filled diamond at the whole `*--` | B is created and destroyed with A (a contract's terms). |
   | Generalization | hollow triangle at the parent `<|--` | B is a kind of A and can stand in for A anywhere. |
   | Realization | dashed line, hollow triangle at the interface `<|..` | B fills the role an interface defines. |

   `[UML]` `[HB]` `[TL]`
4. Inheritance is never a way to share code. If a subclass would throw where the parent does not, or
   need a call the parent does not, use delegation instead. `[TL]`
5. Names follow the code (`RentalContract`, `ContractsService`), never a pattern name for its own
   sake. `[TL]`
6. The class diagram and the sequence diagrams of the same use case are drawn together and agree:
   every message in a sequence is an operation of the receiving class. `[HB]` `[TL]`

---

## 6. Sequence diagram

Skeleton: `sequence.puml`. In the reports the sequences stay Mermaid until the leader rules on the
PlantUML trial at final delivery (D-065 as amended 2026-10-26); the rules below hold in either tool.

1. One use case per diagram, framed `mainframe sd UC-nn Name`. `[HB]` `[UML]`
2. It shows the main success path plus as many `alt` fragments as it takes to convey what the use
   case does (D-083, superseding D-069 rule 3). Each `alt` is split into labelled branches (success,
   failure), and each failure returns to the page. A branch the reader does not need stays in the
   activity diagram of the flow. `[HB]` `[TL]`
3. Lifelines left to right: the human actor, the named page (`boundary "Incident Alert Banner"`,
   never `UI` or `Browser`), the controller, the service, the repository, the database; reactive
   system actors on the far right. `[HB]` `[AMB]`
4. Object lifelines are named `:ClassName` and match the class diagram. `[HB]` `[AMB]`
5. `autonumber` on every diagram; activation bars on every receiving lifeline (`++` on the call,
   `return` or `--` to close). `[HB]` `[PU]`
6. A synchronous call has a filled arrowhead `->` and a dashed return `-->`; an asynchronous message
   has an open arrowhead `->>`. Draw a return only when the value is used later or is not obvious. `[UML]` `[AMB]`
7. Messages to and from humans are prose (`tap Acknowledge`); messages between software objects are
   operation signatures (`acknowledge(id, expectedVersion, caller)`). `[AMB]`
8. Stereotype icons: `boundary` for pages, `control` for controllers and services, `participant` for
   repositories, `database` for the database, `queue` for the broker. `entity` is reserved for a domain
   object. `[PU]` `[TL]`
9. Prefer several small sequences with few lifelines over one large one. `[TL]`

---

## 7. Activity diagram

Skeleton: `activity.puml` (PlantUML, the default in reports, D-065 as amended 2026-10-26).
`activity.mmd` (Mermaid `swimlane-beta`) stays for specs. In PlantUML swimlane mode, `repeat while`
drops its guard labels; write a loop as `while (question?) is ([no]) ... endwhile ([yes])` instead
(verified with 1.2026.9 on 2026-10-26). Wrap an action at about 24 characters with `\n`, so lanes stay
narrow enough for the 7 pt floor.

1. A flow with more than one actor uses swimlanes (`|Lane|`), one per actor, in a logical order: the
   initiating actor first, the system in the middle. Fewer than five lanes; more means split the
   diagram. `[AMB]` (chapter 13 §2)
2. Decision and merge nodes are diamonds. Set `skinparam conditionStyle diamond`; the default
   renders a hexagon, which the handbook marks wrong. `[HB]` `[PU]`
3. Every exit from a decision carries a guard in brackets (`([yes])`, `([no])`). Guards do not overlap
   and cover every case; use `[otherwise]` for the rest. The question sits beside the diamond. `[AMB]`
4. One start node and at least one end node; no action without an incoming flow. `[AMB]` `[UML]`
5. Each main flow has exactly one owner and one activity diagram in the SDD (Review 2 guide §9.1). `[HB]`

---

## 8. State machine diagram

Skeleton: `state.mmd` (Mermaid `stateDiagram-v2`, the default). `state.puml` is the fallback, used
only when Mermaid cannot draw the machine (D-065 as amended 2026-10-25). The rules below hold in
either tool.

1. Draw one for every entity with a lifecycle in the module `design.md`, and keep its states identical
   to the Prisma enum. `[HB]` `[TL]`
2. Initial state at the top (top-left or top-centre), final state at the bottom. A top-level machine
   has both. `[AMB]` `[UML]`
3. Every transition names its trigger, as `event [guard] / action`; events in the past tense
   (`Staff approved`). `[HB]` `[AMB]`
4. No state without an exit unless it is final, and no state without an entry unless it is initial. `[AMB]`
5. State machines sit in the design body of the SDD, never in an appendix. `[HB]`

---

## 9. Entity relationship diagram

Skeleton: `erd.puml`, drawn by `render_erd.py` (rule 3).

1. One notation in the whole document: **crow's foot (IE)**. Never mixed with Chen. `[HB]` (D-069 rule 4)
2. One overall ERD; split views only as additions to it. Main entities at an abstract level. `[HB]`
3. Lines are straight and orthogonal: horizontal and vertical segments only, never a curve or a
   diagonal, each relationship on its own track. Where two lines cross, the horizontal one carries a
   semicircle jump. Each foot reads as three straight strokes ending on the entity border, never a
   curved leaf (supervisor, 2026-10-24), and the end marks of two relationships never touch. PlantUML
   cannot draw this: Graphviz `ortho` puts two relationships on one track and drifts their labels,
   PlantUML's ELK adapter sets no port spacing, and neither draws jumps (leader reviews 2026-10-25 and
   2026-10-26). So an ERD keeps PlantUML's entity syntax, carries the comment `' treklink: erd`, and is
   drawn by `capstone/scripts/srs/render_erd.py`: ELK layered layout with orthogonal routing and an
   explicit port per line end (elkjs), SVG drawn by the script. A self-reference is a loop right of its
   box. Check the render at 4x zoom. `[TL]`
4. Cardinality is decided in both directions, and 0..n is visibly different from 1..n (`o{` versus
   `|{`). `[HB]`
5. Names are the database names from `schema.prisma`: table names from `@@map` (`rental_contracts`),
   column names as declared, since no field carries `@map` (`organizationId`). Types are the database
   types (`uuid`, `text`, `timestamptz`) and enum names as declared (`ContractStatus`). `[HB]`
6. The document explains each end symbol in words, once, in a notation table cited before the first
   ERD (rule 9 of §2: no legend inside the figure). `[HB]`
7. Report 4 also shows a screenshot of the real installed database schema; it never repeats the ERD. `[HB]`

---

## 10. Architecture diagram

Skeleton: `architecture.puml`.

1. Overview and detail are separate figures. `[HB]`
2. Frontend, backend, database, broker and every third party are separate blocks, each inside the
   node it runs on (browser, cloud host, organization laptop, trail). `[HB]`
3. Every interaction has a request arrow and a response arrow (including the MQTT `PUBACK` and the
   payment webhook). `[HB]`
4. Third parties connect to whichever side really calls them: map tiles come from the browser, not the
   backend. `[HB]`
5. Every block points to a real path in `treklink-web` or the firmware; a block with no code yet is
   left out. `[HB]`
6. An IoT hardware diagram accompanies it, listing each device, its specifications and its protocol. `[HB]`
7. Layout: columns left to right in the order data travels (trail, laptop, cloud, third parties). A
   response is written `A <-- B` so the caller stays left of the callee. `[TL]` `[PU]`

---

## 11. Review checklist

Run before a figure is called done, together with chapter 13 §1.1.

- [ ] Started from the skeleton; style include intact
- [ ] Every rule of its section above holds; the tagged `[HB]` ones are re-read in the handbook
- [ ] Rendered and looked at: nothing outside its region, no overlapping labels, no line across the
      whole figure
- [ ] Names match the other figures, the SRS and SDD, `schema.prisma` and `design.md`
- [ ] The PR body or session file records the sections re-read, who looked, what it was checked against
