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

## 4. Tooling

The SRS and its figures are generated by `capstone/scripts/srs/` (see its `README.md`). Fix the
generator, never the output: a hand edit to `Report3_SRS_DRAFT.md` or the `.docx` is lost on the
next build.
