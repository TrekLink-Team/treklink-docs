# Graded Report Conventions

> **Scope**: every graded document under `capstone/Documents/reports/` (Reports 1 to 7, the SDD,
> the test documents and the Excel workbooks) and the review slides. Recorded from leader
> instructions of 2026-09-25. Sources: the school's common-flaws handbook
> `capstone/Documents/templates/Cam-nang-tranh-loi-Capstone-SE.pdf` and the review guidelines in
> `capstone/Documents/course-material/`.

Chapter 14 governs wording everywhere. This chapter adds what the school grades on top of it.

---

## 1. Write only the deliverable

A graded document states what the system is and does. It does not narrate how the team got there.

| Never in a graded document | Instead |
|---|---|
| Why a decision was taken, why it matters, which alternative lost | The decision itself. The rationale lives in the decision register (`D-xxx`) |
| Status notes: "draft", "provisional", "needs check", "decided", "not shown here", "deferred because" | Nothing, or the plain fact ("Specified in the Final SRS") |
| Change history inside the body: "corrected here", "was inverted in the draft" | The Record of Changes table |
| Internal markers: `(P)`, `(unverified)` | Nothing |
| References to the team's internal records: decision IDs (`D-xxx`), clarification answer IDs (`Qnn`), ground-truth sections, repository paths, session names | Nothing. The grader cannot open them. Only codes the document itself defines stay (UC, FR, NFR, BR, E, MSG) plus backlog stories (US-nnn), which are in Jira. `capstone/scripts/srs/build_srs.py` scrubs the internal codes automatically |
| Measurements of the document itself: point sizes, millimetres, placement notes | Nothing |
| Template guidance or placeholder text left in place | The real content, or the section removed if the template allows it |

A sentence that exists to justify the document to its authors is cut. A sentence the grader needs to
understand the system stays.

## 2. The school's rules

From the common-flaws handbook, section by section. Check every graded document against these
before each submission.

**Template and structure (1.1 to 1.3)**
- Use the latest official template from FLM. Keep its section structure; do not add or drop
  sections it defines.
- Include the mandatory pages: Acknowledgement on its own page naming the supervisor, page numbers,
  List of Tables and List of Figures separate from the contents, an abbreviations table sorted
  alphabetically and limited to terms the project uses, mentor and member details, and the Feature
  Tree in Report 1.
- Each major part starts on a new page. Heading levels are consistent. One font family.
- No Vietnamese left in an English document. Glossary entries are project terms only.

**Honesty (1.4, 1.5)**
- Write only what exists: "có làm mới ghi, không làm đừng ghi". Every NFR and business rule must
  point to the code that implements it or the test that checks it.
- The document matches the software and the repository. One version of each diagram.
- An IoT project documents its hardware: devices, specifications and connection protocols.
- Embed figures and submit files, never links.

**Captions and cross-references (1.6)**
- A figure caption goes **below** the figure. A table caption goes **above** the table.
- Every figure and table is cited in the text **before** it appears, by number ("see Figure 3"),
  never "the figure below".
- Captions describe the content. Numbering is automatic (Word Insert Caption and Cross-reference);
  update all fields before submitting.

**Diagrams (2.1 to 2.6)**
- Use case names are verb plus object. `include` and `extend` follow Wiegers and Beatty chapter 8,
  with open arrowheads. A use case describes a function, not a sequence of steps.
- The ERD is **one** overall diagram, named "Entity Relationship Diagram", in one notation (Crow's
  foot here) with cardinality read in both directions. Main entities at an abstract level; the
  physical schema, with a screenshot of the real database, belongs in Report 4.
- The architecture diagram shows request and response paths, every third-party service and who
  calls it, and must match the repository. Every member must be able to point at a block and open
  its code.
- State machines label every transition with its trigger and sit in the design section, not an
  appendix. Sequence diagrams number every message and show page, controller, service and
  repository objects.
- Activity decision nodes are diamonds. Context diagram flow labels are nouns.
- Figures are upright and fit their page (`13-diagram-and-figure-conventions.md` §4.1).

**Business analysis (3.2 to 3.4)**
- Exception scenarios cover at least: payment failing part-way, two users acting at once,
  cancellation after approval, out-of-range data, one role attempting another role's action.
- Every number on screen can be explained, and every business parameter is configuration (D-015).

## 3. Review slides

- Follow the school's slide template for the review in slide order.
- Every member presents (Review 1 rule); name the presenter on each slide.
- Review 1 distinguishes "building a system" from "building a platform". Review 2 opens with what
  changed since Review 1.
- **System or platform, stated on the slide.** A system is run by one company's internal staff and
  serves that company's own customers. A platform is also run by internal staff, but the services
  on it come partly from the operator and partly from partners (the instructors' example is Shopee
  or Lazada). The TrekLink title says platform; the deck must show who the partners are. Source:
  pre-Review-1 briefing, `capstone/Documents/meetings/2026-10-02_Rescope_Meeting_and_Review_Guidance_Summary.md`
  Part B.3. TrekLink failed Review 1 on exactly this point.
- **Review 1 content**, in order: the exact registered title, members and every mentor; context as
  bullets (never the registration-form paragraph pasted); problems; solution as bullets; key
  features that cover the whole scope (features, not use cases); users and their functions,
  presenting only the complex ones; 5 to 6 Main Flows as high-level steps. **No activity diagram on
  review slides**, no product demo and no progress report at Review 1. Slides are in English,
  spoken in Vietnamese. Non-functional requirements are optional.
- **Delivery.** About 15 minutes of slides, then 15 to 20 minutes of questions. No phone in hand
  while presenting: each presenter rehearses a script. Arrive before the slot.
- **Feedback.** Listen and record; do not deny or argue a reviewer down. Answer on the spot what can
  be answered, take the rest away, and close it with evidence at the next gate. **Ask to photograph
  the reviewer's minutes**, because the team's notes and the official record can differ. The
  minutes of each review are tracked at the next review and at the faculty council.
- **Scope size.** The scope must fit 15 weeks. A panel pushes an oversized scope to future work and
  adds requirements to an undersized one.
- Every element stays inside the slide and clear of the template's fixed shapes (presenter bar,
  footer). A table that would run past them is resized by the deck generator, never left to
  overflow: rows are fitted into the space between the table's top and the next shape below it.
  Check the rendered slide (for example a LibreOffice PDF export), not the file's nominal sizes,
  because text wrapping is only visible after rendering. Too much content for that space means
  splitting the table across slides, not shrinking the font below 12 pt.

## 4. Tooling

The SRS and its figures are generated by `capstone/scripts/srs/` (see its `README.md`). Fix the
generator, never the output: a hand edit to `Report3_SRS_DRAFT.md` or the `.docx` is lost on the
next build.

Every document that is submitted or sent to a supervisor or the panel (the reports, the
registration form, the slides and any report-style file) passes the `human` skill before it goes
out: audit, then a span-minimal repair of confirmed findings only, then its preservation gate.
Conventions, session files and other internal documents are exempt. Leader instruction of
2026-10-07, confirmed 2026-10-09.

## 5. Submissions folder

Every document the team submits lives once, in its own folder, under `capstone/Documents/submissions/`, and
every version has its own sub-folder and file suffix `-vX.Y`. Leader instruction of 2026-11-08; it replaces the
`release/` folder rule of 2026-10-29.

```text
Documents/submissions/
├── README.md                 every version: date, what changed, where it was uploaded
├── register/                 outside the review folders
│   ├── register-v1.0/        the form submitted on 2026-07-25
│   ├── register-v1.1/        2026-10-15, clean and highlighted copies
│   ├── register-v2.0/        2026-10-29
│   └── ...                   one folder per version, never overwritten
├── reports/                  the SEP490 Reports 1 to 7 (D-048)
│   ├── report1/report1-v1.0/ ...
│   └── report7/
└── review1/, review2/, ...   one folder per review round
    └── review2-v1.0/ ...     the review-only forms (design brief, self review, record of changes,
                              commitment, slides, tracking) and a manifest naming the report and
                              register versions uploaded with them
```

- Files are named `FA26SE159_<Document>-vX.Y.<ext>`, for example `FA26SE159_Register-v4.0.pdf`. A version folder
  holds the clean DOCX and PDF, the highlighted copy when one was sent, and the Markdown source when the document
  is built from one.
- A new version is a new folder. Earlier versions are never edited or deleted.
- A review folder never copies a report or the register; its manifest points to the version folders.
- Working sources and builders stay in `Documents/reports/` and `scripts/`; only submitted or submittable builds
  go under `submissions/`. `treklink-docs/topics/` keeps a README that points here.

## 6. The register is fixed once written

What the register (registration form) states is never changed later, not even by one line. A design or
build choice that the register does not name stays out of it, and a document must not describe a
register-level choice as easy to reverse ("removal is one line"). Interim or reversible choices, such as
the station topic rule of the AWS field host (treklink-web#431), are recorded in the specs and the
decision register only. Leader instruction of 2026-11-07.

**Leave a way back (có đường lùi).** Because the register cannot change, it states the scope in general
terms that the team can still meet if a design choice moves, and that it can fall back to at the defence
without being judged over-scoped. Leader instruction of 2026-11-08:
- No price, fee, plan length, minimum order or other business number. Say that rental terms and prices are
  configured per device and per plan; the values live in the specs and the seed.
- No payment brand or provider name (VietQR, SePay). Say "an online payment gateway in its sandbox" or
  "online or at the counter".
- Name the target hosting (AWS) and never a stand-in used only for supervisor demos (Vercel).
- Follow the structure and proportions of the original register submitted on 2026-07-25
  (`capstone/Documents/submissions/register/register-v1.0/FA26SE159_Register-v1.0.docx`), the format the supervisor vetted: short sections and
  bullet lists, no long prose.

## 7. Every submitted file passes these checks

Leader instructions of 2026-11-09, after the Review 2 resubmission v4.0 was rejected before upload. Each rule
holds for every report, form and workbook that goes up, and is checked on the exported PDF.

- **Contents filled, no blank page.** A plain LibreOffice export leaves the contents page empty. Export every
  report with `capstone/scripts/srs/export_pdf.py`, which updates the contents and the lists of figures and
  tables first. The SEP490 covers fill page 1 exactly, so `build_docx.py` removes one empty cover paragraph
  (`fix_cover_break.py`); without it page 2 prints blank. Look at the first pages of every PDF.
- **No AI text.** No tool, model, vendor, agent or prompt is named in a submitted document, except where the
  course requires it: the SDD declares the tools, model families and stages in one short table under the line
  "an assisted agentic AI workflow with human-driven reviews" (Review 2 guide, section 10), and Form BM02 keeps the
  fields its template asks for (tool and model, the standard prompt, the findings as produced, unedited).
- **Abbreviations declared.** A document that refers to members by abbreviation (KhoaDD, TanNB, HoangTK, LongLP,
  LongNN) declares them once before first use: "Hereinafter, the team members are referred to by the following
  abbreviations", with each full name. A workbook declares them on each sheet that uses them.
- **No reference to an unsubmitted file.** A document names no file, folder or path that is not in the same
  upload. A file the reader needs goes up with the document under its submitted name; anything else is not
  mentioned at all. Code and test names in the repository linked at the review tag are part of the submission.
- **One diagram style across reports.** The diagram style applies to every graded report:
  the SRS uses the same PlantUML style, ERD style and activity diagram style as the SDD
  (D-065, chapter 16).
- **No backlog material.** No session record, model list, dated capture of a local installation or internal
  decision code appears in an SRS or SDD.
- The Review 2 guide's page limit for the Design Brief (four A4 pages) is advisory; the brief keeps every
  required section.
