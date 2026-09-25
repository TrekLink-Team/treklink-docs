#!/usr/bin/env python3
"""Build Report3_SRS_TrekLink.docx from Report3_SRS_DRAFT.md against the official template.

    python3 _handoff/tools/build_docx.py <official template .docx>

1. pandoc converts the Markdown body with --reference-doc=<template>, so every heading, table and
   caption uses the template's own styles. Headings shift up one level so that Part I and Part II
   are Heading 1 and the numbered sections Heading 2, as in the template.
2. The template's cover page and Table of Contents field are kept; the template's sample content
   after them is removed; the body is appended with docxcompose.
3. Figures listed as rotated are never produced: report figures stay upright
   (01-conventions/13 section 4.1).
"""
import copy
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import docx
from docx.oxml.ns import qn
from docxcompose.composer import Composer

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "_handoff/outbound/capstone/Documents/reports"
MD = OUT / "Report3_SRS_DRAFT.md"
DOCX = OUT / "Report3_SRS_TrekLink.docx"
COVER_LAST = 22          # template body elements 0..22: cover, TOC field, page break
TOC_INDEX = 21           # the template's TOC field, holding its sample entries; pandoc's replaces it
DATE_LINE = "– September 2026 –"


def patched_reference(template: Path, tmp: Path) -> Path:
    """The template plus only the pandoc styles it lacks (Compact, Table, FirstParagraph...).

    Without them LibreOffice drops the structure of every pandoc table. Template styles win
    wherever both define the same ID, so the report keeps the template's look.
    """
    import zipfile
    default = tmp / "pandoc-ref.docx"
    with open(default, "wb") as fh:
        subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"],
                       stdout=fh, check=True)
    pstyles = zipfile.ZipFile(default).read("word/styles.xml").decode()
    tz = zipfile.ZipFile(template)
    tstyles = tz.read("word/styles.xml").decode()
    have = set(re.findall(r'w:styleId="([^"]+)"', tstyles))
    add = [m.group(0) for m in re.finditer(r"<w:style [^>]*>.*?</w:style>", pstyles, re.S)
           if re.search(r'w:styleId="([^"]+)"', m.group(0)).group(1) not in have]
    tstyles = tstyles.replace("</w:styles>", "".join(add) + "</w:styles>")
    out = tmp / "reference.docx"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for it in tz.infolist():
            z.writestr(it, tstyles.encode() if it.filename == "word/styles.xml" else tz.read(it.filename))
    return out


def body_docx(template: Path, tmp: Path) -> Path:
    md = MD.read_text()
    md = md.split("\n", 1)[1]                      # the cover carries the title
    src = tmp / "body.md"
    src.write_text(md)
    out = tmp / "body.docx"
    subprocess.run(["pandoc", str(src), "-f", "markdown+pipe_tables+raw_attribute-implicit_figures", "--toc", "--toc-depth=3",
                    "-o", str(out), f"--reference-doc={template}",
                    "--shift-heading-level-by=-1", f"--resource-path={OUT}"], check=True)
    return out


TEXT_W = 9000   # twips inside the template's 1-inch margins (159 mm)


def style_tables(d: docx.document.Document) -> None:
    """Point pandoc's tables at the template's TableGrid style and size columns by content.

    pandoc tags tables with a style ID "Table" that the template does not define; LibreOffice then
    drops the table structure. Pipe tables also arrive with equal column widths.
    """
    for t in d.tables:
        tblPr = t._tbl.tblPr
        st = tblPr.find(qn("w:tblStyle"))
        st.set(qn("w:val"), "TableGrid")
        lens = []
        for c in range(len(t.columns)):
            cells = [r.cells[c].text for r in t.rows]
            avg = sum(min(len(x), 400) for x in cells) / max(len(cells), 1)
            lens.append(max(avg, 4.0) ** 0.8)          # dampen: long columns still wrap
        total = sum(lens)
        widths = [int(TEXT_W * x / total) for x in lens]
        widths = [max(w, 700) for w in widths]
        scale = TEXT_W / sum(widths)
        widths = [int(w * scale) for w in widths]
        grid = t._tbl.find(qn("w:tblGrid"))
        for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
            gc.set(qn("w:w"), str(w))
        tw = tblPr.find(qn("w:tblW"))
        if tw is None:
            tw = tblPr.makeelement(qn("w:tblW"), {})
            tblPr.append(tw)
        tw.set(qn("w:w"), str(TEXT_W))
        tw.set(qn("w:type"), "dxa")
        lay = tblPr.find(qn("w:tblLayout"))
        if lay is None:
            lay = tblPr.makeelement(qn("w:tblLayout"), {})
            tblPr.append(lay)
        lay.set(qn("w:type"), "fixed")
        for row in t.rows:
            for c, w in zip(row.cells, widths):
                tcPr = c._tc.get_or_add_tcPr()
                tcW = tcPr.find(qn("w:tcW"))
                if tcW is None:
                    tcW = tcPr.makeelement(qn("w:tcW"), {})
                    tcPr.insert(0, tcW)
                tcW.set(qn("w:w"), str(w))
                tcW.set(qn("w:type"), "dxa")
                for p in c.paragraphs:
                    p.paragraph_format.space_after = docx.shared.Pt(0)
                    for r in p.runs:
                        r.font.size = docx.shared.Pt(9)
        for c in t.rows[0].cells:
            for p in c.paragraphs:
                for r in p.runs:
                    r.bold = True


def cover(template: Path, tmp: Path) -> Path:
    d = docx.Document(str(template))
    body = d.element.body
    for i, el in enumerate(list(body)):
        if (i > COVER_LAST or i == TOC_INDEX) and el.tag != qn("w:sectPr"):
            body.remove(el)
    for p in d.paragraphs:
        if "Hanoi, August 2019" in p.text:
            for r in p.runs[1:]:
                r.text = ""
            p.runs[0].text = DATE_LINE
    settings = d.settings.element
    upd = settings.find(qn("w:updateFields"))
    if upd is None:
        upd = settings.makeelement(qn("w:updateFields"), {})
        settings.append(upd)
    upd.set(qn("w:val"), "true")                    # Word refreshes the TOC on open
    out = tmp / "cover.docx"
    d.save(str(out))
    return out


def main() -> None:
    template = Path(sys.argv[1])
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        body = docx.Document(str(body_docx(patched_reference(template, tmp), tmp)))
        style_tables(body)
        master = docx.Document(str(cover(patched_reference(template, tmp), tmp)))
        comp = Composer(master)
        comp.append(body)
        comp.save(str(DOCX))
    d = docx.Document(str(DOCX))
    heads = [p for p in d.paragraphs if p.style.name.startswith("Heading")]
    print(f"{DOCX.name}: {len(d.paragraphs)} paragraphs, {len(d.tables)} tables, "
          f"{len(d.inline_shapes)} figures, {len(heads)} headings")


if __name__ == "__main__":
    main()
