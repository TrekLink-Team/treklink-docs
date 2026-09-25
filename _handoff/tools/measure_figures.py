#!/usr/bin/env python3
"""Measure SRS figures with the handbook harness and plan them for the Report 3 page box.

The template is A4 with 1-inch margins: a 159 x 246 mm text area. A figure stays inline up to
225 mm high (room for its caption); one that would fall below the 7 pt floor inline takes a
full-page plate of 235 mm. Figures are never rotated: the reports are read on screen and shown in
presentations, not printed (01-conventions/13 section 4.1). Writes assets/mermaid/sizes.txt.
"""
import glob, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "_docs/handbook"))
import build_handbook as hb  # noqa: E402

W, H, PLATE_H, FLOOR = 159.0, 225.0, 235.0, hb.LEGIBILITY_FLOOR_PT
out = Path(sys.argv[1])
files = sorted((out / "assets/mermaid").glob("srs-fig*.mmd"), key=lambda p: int(p.stem[7:]))
chrome = glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")[0]
res = hb.measure_diagrams([f.read_text() for f in files], chrome, hb.ensure_mermaid())
sizes = []
for f, m in zip(files, res):
    w, h, fpx = m["src_w"], m["src_h"], m["min_font_px"]
    s, kind = min(W / w, H / h), "inline"
    if fpx * s / 25.4 * 72 < FLOOR:          # below the floor inline: its own page, upright
        s, kind = min(W / w, PLATE_H / h), "full-page plate"
    pt = fpx * s / 25.4 * 72
    n = f.stem[7:]
    clause = f"Placement: {kind}, {w*s:.1f} x {h*s:.1f} mm, labels at {pt:.2f} pt."
    sizes.append(f"{n}|width={w*s:.1f}mm height={h*s:.1f}mm|{clause}")
    print(f"fig{n}: {w:.0f}x{h:.0f}px {clause}{'  BELOW FLOOR' if pt < FLOOR else ''}")
(out / "assets/mermaid/sizes.txt").write_text("\n".join(sizes) + "\n")
