# Handbook Build Pipeline

Renders [`../TrekLink_Developer_Handbook_v1.0.pdf`](../TrekLink_Developer_Handbook_v1.0.pdf) from
the markdown in `_docs/`.

> [!IMPORTANT]
> **The markdown is the manual. The PDF is a render of it.**
> Never hand-edit the PDF, the next build overwrites it. To change the handbook, edit the
> convention files and rebuild.

---

## Build

```bash
cd _docs/handbook
python3 build_handbook.py
```

| Flag | Effect |
|---|---|
| *(none)* | Build to the `output:` path in `manifest.yaml` |
| `--out PATH` | Build somewhere else |
| `--html-only` | Emit the intermediate HTML instead of a PDF, use this to debug layout |
| `--check` | Verify toolchain and that every manifest chapter resolves. Builds nothing. |

## Requirements

| | |
|---|---|
| **pandoc** ≥ 3.1 | `sudo apt install pandoc` · `brew install pandoc` · `winget install JohnMacFarlane.Pandoc` |
| **PyYAML** | `pip install pyyaml` |
| **Chrome / Chromium** | Any recent build. Override detection with `CHROME_BIN=/path/to/chrome`. |

Network is needed on the **first** run only, `mermaid.min.js` is downloaded once and cached in
`assets/`. Commit that cache so CI and offline builds never touch the CDN.

---

## How it works

```
manifest.yaml
  │
  ├─ concatenate chapters in order, grouped into parts
  ├─ preprocess:  mermaid blocks extracted   (pandoc must not touch the syntax)
  │               GitHub alerts → markers    (> [!NOTE] etc.)
  │               repo-relative .md links flattened to breadcrumbs
  ├─ pandoc:      GFM → HTML5 fragment
  ├─ measure:     every diagram rendered headless; viewBox + smallest label
  │                measured, then plan_figure() picks inline vs rotated plate
  ├─ postprocess: each diagram re-injected as inline <svg> inside a <figure>,
  │                sized in mm, rotated inside the SVG coordinate system if turned,
  │                caption pulled in so a page break cannot separate the two
  │               alert markers → styled callout blockquotes
  ├─ assemble:    title page + auto-generated linked TOC + CSS
  └─ Chrome --print-to-pdf   ← diagrams are already inline SVG; nothing renders here
```

**Why Chrome rather than LaTeX**: Mermaid renders in a real browser, so diagrams are true vectors
with selectable text and no separate diagram toolchain. Vietnamese diacritics need no font
wrangling. Styling is plain CSS. And Chrome is preinstalled on GitHub's `ubuntu-latest` runners, so
CI only has to add pandoc.

**Trade-off accepted**: Chrome cannot compute printed page numbers for the table of contents (no
CSS `target-counter` support), so the TOC uses clickable internal links instead. For a document
read on screen that is arguably better. If printed page numbers ever become a requirement, the
upgrade path is a two-stage render, Chrome to inline the Mermaid SVGs, then WeasyPrint (which does
support `target-counter`) for pagination.

---

## Changing what's in the handbook

Edit `manifest.yaml`. Chapter paths are relative to `_docs/`.

```yaml
parts:
  - part: Delivery
    chapters:
      - 01-conventions/07-github-workflow-git-conventions.md
```

Run `python3 build_handbook.py --check` after editing, it fails loudly on a path that doesn't
resolve, rather than silently omitting a chapter.

**Bump the version** in `manifest.yaml` (`version:` and `output:`) for any substantive revision, so
a teammate holding an old PDF can tell it apart.

---

## Styling

All of it is [`assets/handbook.css`](assets/handbook.css), a normal print stylesheet.

Debugging layout is much faster in a browser than in a PDF:

```bash
python3 build_handbook.py --html-only
# then open the emitted .html and use DevTools' print-preview
```

---

## CI

[`.github/workflows/handbook.yml`](../../.github/workflows/handbook.yml) rebuilds the PDF on every
pull request that touches `_docs/**`, and commits it to the PR branch if it changed. The PDF then
reaches `dev` inside the reviewed PR, and `main` through the release fast-forward (D-025).
Teammates get the current handbook by pulling, no manual build required.

On a push to `dev` or `main` the workflow only validates. It never commits there: both branches
are protected, the workflow token cannot bypass that, and a bot commit on `main` alone would split
`main` from `dev`. A PR from a fork is validated but not committed to.

---

## Authoring notes

Things that affect the rendered output:

- **Mermaid only** for diagrams. Fenced ` ```mermaid ` blocks. No PlantUML, no images.
- **Multi-actor process flows are `swimlane-beta`**, not `flowchart`, see
  `01-conventions/13-diagram-and-figure-conventions.md`. Requires Mermaid >= 11.16.0;
  the pin is 12.0.0.
- **Figures are measured, not eyeballed.** `--measure FILE` reports placement and the
  effective point size for one file; `--measure-all` does the whole manifest. Run
  `--measure-all` after any Mermaid version bump.
- Figures are numbered per source document and renumbered continuously by the build.
- **GitHub alerts** (`> [!NOTE]`, `[!IMPORTANT]`, `[!WARNING]`, `[!TIP]`, `[!CAUTION]`) become
  styled callouts. Use them for genuine emphasis, a page of callouts emphasises nothing.
- **Wide tables** get tight in A4. Prefer 4–5 columns; beyond that, consider a definition list.
- **Long code lines** wrap rather than overflow, but wrapping hurts readability, keep shell
  examples under ~90 characters.
- **Relative `.md` links** are flattened to a plain-text breadcrumb, since they can't resolve in a
  PDF. They still work normally in GitHub and Obsidian, so keep writing them.
