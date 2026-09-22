#!/usr/bin/env python3
"""Build the TrekLink Developer Handbook PDF from the markdown SSOT.

The markdown in `_docs/` is the manual. This script renders it; it never authors
anything. If the PDF and the markdown disagree, the markdown wins, rebuild.

Pipeline
--------
    manifest.yaml
      -> concatenate chapters, in order
      -> preprocess  (GitHub alerts -> styled divs, mermaid extracted,
                      repo-relative links flattened, headings anchored)
      -> pandoc      (GFM -> HTML fragment)
      -> assemble    (title page + auto TOC + body + CSS + mermaid.js)
      -> headless Chrome --print-to-pdf   (mermaid renders natively in the browser)

Why Chrome and not LaTeX: Mermaid renders natively in a real browser, Vietnamese
diacritics need no font wrangling, and the styling is plain CSS. Chrome is
preinstalled on GitHub's ubuntu-latest runners, so CI needs no extra setup beyond
pandoc.

Requirements
------------
    pandoc >= 3.1, PyYAML, and a Chrome/Chromium binary.
    Network access on first run (mermaid.js is fetched and cached next to this file).

Usage
-----
    python3 build_handbook.py                 # -> _docs/<output from manifest>
    python3 build_handbook.py --out /tmp/x.pdf
    python3 build_handbook.py --html-only     # keep the intermediate HTML for debugging
    python3 build_handbook.py --check         # verify toolchain + manifest, build nothing
"""

from __future__ import annotations

import argparse
import base64
import json
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("!! PyYAML is required:  pip install pyyaml")

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent                      # _docs/
MERMAID_VERSION = "12.0.0"
MERMAID_URL = f"https://cdn.jsdelivr.net/npm/mermaid@{MERMAID_VERSION}/dist/mermaid.min.js"
MERMAID_CACHE = HERE / "assets" / f"mermaid-{MERMAID_VERSION}.min.js"

CHROME_CANDIDATES = [
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
    "chrome", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

# GitHub alert syntax:  > [!NOTE] / [!IMPORTANT] / [!WARNING] / [!TIP] / [!CAUTION]
ALERT_RE = re.compile(r"^> \[!(NOTE|IMPORTANT|WARNING|TIP|CAUTION)\]\s*$", re.MULTILINE)
MERMAID_RE = re.compile(r"^```mermaid\n(.*?)^```", re.MULTILINE | re.DOTALL)
HEADING_RE = re.compile(r"<h([1-3])[^>]*>(.*?)</h\1>", re.DOTALL)
CAPTION_RE = re.compile(r"^\*\*\*Figure (\d+)\*\*\*: (.*?)$", re.MULTILINE)
# Guarded so it cannot match the inner `**Figure N**` of a `***Figure N***` caption:
# without the guards a caption is remapped twice and its number silently drifts.
FIGREF_RE = re.compile(r"(?<!\*)\*\*Figure (\d+)\*\*(?!\*)")

# --- Figure geometry (01-conventions/13-diagram-and-figure-conventions.md) -----------
# A4 portrait minus the handbook's 15/14/16/14 mm margins.
PAGE_W_MM, PAGE_H_MM = 182.0, 266.0
MM_PER_PT = 25.4 / 72.0
LEGIBILITY_FLOOR_PT = 7.0


def plan_figure(w_px: float, h_px: float, min_font_px: float) -> dict:
    """Choose a placement for one diagram. Computed, never authored.

    Two candidates are considered: inline in the text column, and a plate page turned
    counter-clockwise. Whichever affords the larger scale wins, because scale is what
    label legibility is made of. Both axes are always constrained, so nothing clips.
    """
    def pt(scale: float) -> float:
        return (min_font_px * scale) / MM_PER_PT

    upright = min(PAGE_W_MM / w_px, PAGE_H_MM / h_px)
    turned = min(PAGE_H_MM / w_px, PAGE_W_MM / h_px)

    if turned > upright:
        kind, scale, w_mm, h_mm = "plate-rotated", turned, h_px * turned, w_px * turned
    else:
        kind, scale, w_mm, h_mm = "inline", upright, w_px * upright, h_px * upright

    effective = pt(scale)
    if kind == "inline" and effective < LEGIBILITY_FLOOR_PT:
        kind = "plate"          # keep it upright, but give it the whole page
    return {
        "kind": kind,
        "width_mm": round(w_mm, 2),
        "height_mm": round(h_mm, 2),
        "pt": round(effective, 2),
        "below_floor": effective < LEGIBILITY_FLOOR_PT,
        "src_w": round(w_px, 1), "src_h": round(h_px, 1),
        "min_font_px": round(min_font_px, 2),
    }


def rotate_svg_ccw(svg: str) -> str:
    """Turn an SVG counter-clockwise inside its own coordinate system.

    Never a CSS transform: a transformed box paints in one place and paginates in
    another, which prints content on the wrong page, clipped.
    """
    m = re.search(r'viewBox="([-\d.eE]+)\s+([-\d.eE]+)\s+([-\d.eE]+)\s+([-\d.eE]+)"', svg)
    if not m:
        return svg
    minx, miny, w, h = (float(x) for x in m.groups())
    # rotate(-90): (x, y) -> (y, -x); the content box maps to [miny, miny+h] x [-(minx+w), -minx]
    new_vb = f'viewBox="{miny} {-(minx + w)} {h} {w}"'
    svg = svg[:m.start()] + new_vb + svg[m.end():]
    open_end = svg.index(">") + 1
    close_start = svg.rindex("</svg>")
    return (svg[:open_end] + '<g transform="rotate(-90)">'
            + svg[open_end:close_start] + "</g></svg>")


MEASURE_BATCH = 3          # swimlanes are slow; keep each probe page small
MEASURE_FONT_PX = 16       # mermaid theme font used for both measuring and rendering


def measure_diagrams(sources: list[str], chrome: str, mermaid_js: str) -> list[dict]:
    """Measure in batches. One probe page per batch keeps each Chrome run inside its
    virtual-time budget; a page holding every diagram in the handbook does not finish."""
    if len(sources) > MEASURE_BATCH:
        out: list[dict] = []
        for i in range(0, len(sources), MEASURE_BATCH):
            out += _measure_batch(sources[i:i + MEASURE_BATCH], chrome, mermaid_js, i)
        return out
    return _measure_batch(sources, chrome, mermaid_js, 0)


def _measure_batch(sources: list[str], chrome: str, mermaid_js: str,
                   offset: int = 0) -> list[dict]:
    """Render every diagram headless and report geometry + smallest rendered label.

    Measurement has to happen in a real browser: label size depends on the font the
    renderer actually resolved, which cannot be predicted from the source text.
    """
    if not sources:
        return []
    panes = "\n".join(
        f'<pre class="mermaid" id="m{i}">{html.escape(src)}</pre>'
        for i, src in enumerate(sources)
    )
    probe = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{font-family:Inter,"Segoe UI",system-ui,sans-serif}</style></head>
<body><div id="out">PENDING</div>""" + panes + """
<script>""" + mermaid_js + r"""</script>
<script>
(async () => {
  const res = [];
  mermaid.initialize({ startOnLoad:false, theme:'neutral', securityLevel:'loose',
    fontFamily:'Inter, "Segoe UI", system-ui, sans-serif', themeVariables:{ fontSize:'""" + str(MEASURE_FONT_PX) + r"""px' } });
  for (const el of document.querySelectorAll('.mermaid')) {
    try {
      await mermaid.run({ nodes: [el] });
      // setTimeout, not requestAnimationFrame: under --virtual-time-budget the
      // frame callback may never fire, which hangs the probe silently.
      await new Promise(r => setTimeout(r, 30));
      const svg = el.querySelector('svg');
      if (!svg) { res.push({ err: 'NO_SVG' }); continue; }
      let min = Infinity;
      for (const t of svg.querySelectorAll('text,tspan,span,div,p')) {
        const fs = parseFloat(getComputedStyle(t).fontSize);
        if (fs && (t.textContent || '').trim()) min = Math.min(min, fs);
      }
      // Not every mermaid renderer emits a viewBox; fall back to the bounding box
      // so a missing attribute is a measurement detail, not a build failure.
      const vbAttr = svg.getAttribute('viewBox');
      let w, h;
      if (vbAttr) { const vb = vbAttr.trim().split(/\s+/).map(Number); w = vb[2]; h = vb[3]; }
      else {
        const bb = svg.getBBox();
        w = bb.width; h = bb.height;
        svg.setAttribute('viewBox', bb.x + ' ' + bb.y + ' ' + bb.width + ' ' + bb.height);
      }
      res.push({ w: w, h: h, minFont: (min === Infinity ? 13 : min),
                 svg: svg.outerHTML });
    } catch (e) { res.push({ err: String((e && e.message) || e).slice(0, 200) }); }
  }
  // Chunked: spreading a multi-megabyte Uint8Array into String.fromCharCode
  // exceeds the argument limit and throws, which looked like "no output at all".
  const bytes = new TextEncoder().encode(JSON.stringify(res));
  let bin = '';
  for (let i = 0; i < bytes.length; i += 0x8000) {
    bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  }
  document.getElementById('out').textContent = btoa(bin);
})();
</script></body></html>"""

    tmp = Path(tempfile.mkdtemp(prefix="treklink-measure-"))
    probe_path = tmp / "measure.html"
    probe_path.write_text(probe, encoding="utf-8")
    result = subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox",
         "--virtual-time-budget=120000", "--dump-dom", probe_path.as_uri()],
        capture_output=True, text=True, timeout=600,
    )
    shutil.rmtree(tmp, ignore_errors=True)
    m = re.search(r'<div id="out">([A-Za-z0-9+/=\s]*)</div>', result.stdout, re.S)
    if not m or not m.group(1).strip() or m.group(1).strip() == "PENDING":
        sys.exit("!! Could not measure diagrams, Chrome returned no probe output.\n"
                 + result.stderr[-1500:])
    data = json.loads(base64.b64decode(m.group(1).strip()).decode("utf-8"))

    out = []
    for i, d in enumerate(data):
        if "err" in d:
            sys.exit(f"!! Diagram {offset + i + 1} failed to render: {d['err']}\n"
                     f"   Source begins: {sources[i].splitlines()[0][:70]}")
        if not d.get("w") or not d.get("h"):
            sys.exit(f"!! Diagram {i} measured {d.get('w')}x{d.get('h')}, it rendered but "
                     f"reported no size.\n   Source begins: {sources[i].splitlines()[0][:70]}")
        plan = plan_figure(d["w"], d["h"], d["minFont"])
        plan["svg"] = d["svg"]
        out.append(plan)
    return out

# Repo-relative markdown links: [text](../path/file.md) or [text](file.md#anchor)
RELLINK_RE = re.compile(r"\[([^\]]+)\]\((?!https?://|#)([^)]*\.md)(#[^)]*)?\)")


# --------------------------------------------------------------------------- utils
def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        found = shutil.which(c) if not c.startswith("/") else (c if Path(c).exists() else None)
        if found:
            return found
    sys.exit("!! No Chrome/Chromium binary found. Install one, or set CHROME_BIN.")


def ensure_mermaid() -> str:
    """Fetch and cache mermaid.js so repeat builds and CI don't depend on the CDN."""
    if MERMAID_CACHE.exists() and MERMAID_CACHE.stat().st_size > 100_000:
        return MERMAID_CACHE.read_text(encoding="utf-8")
    MERMAID_CACHE.parent.mkdir(parents=True, exist_ok=True)
    print(f"    fetching mermaid {MERMAID_VERSION} ...")
    try:
        with urllib.request.urlopen(MERMAID_URL, timeout=60) as r:
            js = r.read().decode("utf-8")
    except Exception as exc:                                    # noqa: BLE001
        sys.exit(f"!! Could not fetch mermaid.js ({exc}).\n"
                 f"   Download {MERMAID_URL}\n   to {MERMAID_CACHE}")
    MERMAID_CACHE.write_text(js, encoding="utf-8")
    return js


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_]+", "-", text).strip("-") or "section"


# --------------------------------------------------------------- markdown preprocess
def preprocess(md: str, store: list[str], captions: list[str],
               fig_counter: list[int]) -> str:
    """Make one chapter's markdown safe and self-contained for print.

    Figures are numbered per source document so each file reads correctly standalone
    in the repository. Here they are renumbered continuously across the assembled PDF,
    and every in-text `**Figure N**` reference in the same chapter is rewritten to match.
    """
    # 0. Renumber this chapter's figures into the document-wide sequence.
    # Fenced blocks are masked first: a chapter that documents the caption format
    # contains a literal ***Figure 3*** inside a code fence, and renumbering that
    # rewrote the documentation instead of a figure.
    fences: list[str] = []

    def _mask(m: re.Match) -> str:
        fences.append(m.group(0))
        return f"\x00FENCE{len(fences) - 1}\x00"

    md = re.sub(r"^```.*?^```", _mask, md, flags=re.MULTILINE | re.DOTALL)

    local = [int(m.group(1)) for m in CAPTION_RE.finditer(md)]
    remap: dict[int, int] = {}
    for old_n in local:
        if old_n not in remap:
            fig_counter[0] += 1
            remap[old_n] = fig_counter[0]
    if remap:
        md = CAPTION_RE.sub(
            lambda m: f"***Figure {remap[int(m.group(1))]}***: {m.group(2)}", md)
        md = FIGREF_RE.sub(
            lambda m: f"**Figure {remap.get(int(m.group(1)), m.group(1))}**", md)

    md = re.sub(r"\x00FENCE(\d+)\x00", lambda m: fences[int(m.group(1))], md)

    # 1. Pull mermaid blocks out before pandoc so it can't mangle the syntax.
    #    The caption paragraph that follows a diagram is pulled with it, so the two
    #    end up inside one <figure> and no page break can separate them.
    def _stash(m: re.Match) -> str:
        store.append(m.group(1).rstrip())
        captions.append("")
        return f"\n<!--MERMAID:{len(store) - 1}-->\n"

    md = MERMAID_RE.sub(_stash, md)

    def _claim(m: re.Match) -> str:
        idx = int(m.group(1))
        captions[idx] = f"Figure {m.group(2)}: {m.group(3).strip()}"
        return f"\n<!--MERMAID:{idx}-->\n"

    md = re.sub(r"<!--MERMAID:(\d+)-->\s*\n\s*\*\*\*Figure (\d+)\*\*\*: ([^\n]*(?:\n(?!\n)[^\n]*)*)",
                _claim, md)

    # 2. GitHub alerts -> a marker pandoc passes through; styled by CSS later.
    md = ALERT_RE.sub(lambda m: f"> <!--ALERT:{m.group(1)}-->", md)

    # 3. Repo-relative .md links can't resolve in a PDF. Keep the label, drop the href,
    #    and render the target as a small monospace breadcrumb so the reader can find it.
    md = RELLINK_RE.sub(
        lambda m: f"{m.group(1)} (`{Path(m.group(2)).name}`)", md)

    return md


def postprocess(body: str, store: list[str], figures: list[dict],
                captions: list[str]) -> str:
    """Re-inject mermaid and convert alert markers into styled callouts."""
    # Alerts: pandoc wraps our marker inside the blockquote. Promote it to a class.
    def _alert(m: re.Match) -> str:
        kind = m.group(1).lower()
        return f'<blockquote class="alert alert-{kind}"><p class="alert-title">{m.group(1).title()}</p>'

    body = re.sub(r"<blockquote>\s*<p><!--ALERT:(\w+)--></p>", _alert, body)
    body = re.sub(r"<blockquote>\s*<p><!--ALERT:(\w+)-->\s*", _alert, body)

    # Mermaid: replace the placeholder with a measured, pre-rendered <figure>.
    def _mermaid(m: re.Match) -> str:
        i = int(m.group(1))
        plan = figures[i]
        svg = plan["svg"]
        if plan["kind"] == "plate-rotated":
            svg = rotate_svg_ccw(svg)
        # Both axes in millimetres. Never height:auto, it constrains one axis and lets
        # the other overflow the page box.
        open_tag = svg[:svg.index(">") + 1]
        stripped = re.sub(r'\s(?:width|height)="[^"]*"', "", open_tag)
        # mermaid stamps style="max-width: NNNpx" on the root svg. Left in place it is a
        # second, competing size constraint on an element we have already sized in mm.
        stripped = re.sub(r'max-width:\s*[^;"]*;?', "", stripped)
        stripped = stripped.replace(
            "<svg", f'<svg width="{plan["width_mm"]}mm" height="{plan["height_mm"]}mm"', 1)
        svg = stripped + svg[svg.index(">") + 1:]
        cap = captions[i]
        cap_html = f"<figcaption>{html.escape(cap)}</figcaption>" if cap else ""
        cls = "fig fig-plate" if plan["kind"].startswith("plate") else "fig fig-inline"
        return f'<figure class="{cls}">{svg}{cap_html}</figure>'

    body = re.sub(r"<p><!--MERMAID:(\d+)--></p>", _mermaid, body)
    body = re.sub(r"<!--MERMAID:(\d+)-->", _mermaid, body)
    return body


# ------------------------------------------------------------------------- assembly
def build_markdown(manifest: dict) -> tuple[str, list[str], list[str], list[dict]]:
    chunks: list[str] = []
    store: list[str] = []
    captions: list[str] = []
    fig_counter = [0]
    outline: list[dict] = []
    missing: list[str] = []

    for part in manifest["parts"]:
        # The part title carries its own page-break-before/after in CSS; emitting a
        # separate .page-break div here as well is what produced blank pages.
        chunks.append(
            f'\n\n<h1 class="part-title" id="{slugify(part["part"])}">'
            f'{html.escape(part["part"])}</h1>\n\n'
        )
        outline.append({"level": 0, "title": part["part"], "id": slugify(part["part"])})

        for i, rel in enumerate(part["chapters"]):
            path = DOCS / rel
            if not path.exists():
                missing.append(rel)
                continue
            # First chapter of a part already starts on a fresh page (part title
            # breaks after it); only subsequent chapters need their own break.
            if i > 0:
                chunks.append('\n\n<div class="page-break"></div>\n\n')
            chunks.append(preprocess(path.read_text(encoding="utf-8"), store,
                                     captions, fig_counter))

    if missing:
        sys.exit("!! Manifest references files that do not exist:\n   " + "\n   ".join(missing))
    return "\n".join(chunks), store, captions, outline


def render_toc(body: str) -> tuple[str, str]:
    """Give every h1/h2 a stable id and build a linked table of contents."""
    items: list[str] = []
    seen: dict[str, int] = {}

    def _anchor(m: re.Match) -> str:
        level, inner = int(m.group(1)), m.group(2)
        base = slugify(inner)
        seen[base] = seen.get(base, 0) + 1
        anchor = base if seen[base] == 1 else f"{base}-{seen[base]}"
        text = re.sub(r"<[^>]+>", "", inner).strip()
        if level <= 2:
            cls = "toc-part" if "part-title" in m.group(0) else f"toc-h{level}"
            items.append(f'<li class="{cls}"><a href="#{anchor}">{text}</a></li>')
        return f'<h{level} id="{anchor}"{" class=\"part-title\"" if "part-title" in m.group(0) else ""}>{inner}</h{level}>'

    body = HEADING_RE.sub(_anchor, body)
    return body, '<ul class="toc">' + "\n".join(items) + "</ul>"


def title_page(m: dict) -> str:
    rows = "\n".join(
        f"<tr><td>{html.escape(t['name'])}</td><td><code>{html.escape(t['code'])}</code></td>"
        f"<td>{html.escape(t['role'])}</td></tr>"
        for t in m.get("team", [])
    )
    return f"""
<section class="title-page">
  <div class="title-mark">TrekLink</div>
  <h1 class="doc-title">{html.escape(m['title'])}</h1>
  <p class="doc-subtitle">{html.escape(m['subtitle'])}</p>
  <p class="doc-version">Version {html.escape(str(m['version']))} &middot; {date.today().isoformat()}</p>
  <table class="team-table">
    <thead><tr><th>Member</th><th>Code</th><th>Role</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <p class="doc-meta">
    {html.escape(m['project'])} &middot; {html.escape(m['org'])}<br>
    Supervisor: {html.escape(m.get('supervisor', ''))}
  </p>
  <p class="doc-warning">
    Generated from the markdown in <code>_docs/</code>. Do not edit this PDF &mdash;
    edit the source and rebuild.
  </p>
</section>
"""


def assemble(manifest: dict, body: str, toc: str, css: str) -> str:
    """Diagrams are already inline, measured SVG, nothing renders at print time.

    Rendering in the browser during --print-to-pdf meant layout could not know a
    figure's size until after pagination had been decided. Pre-rendering is what makes
    computed placement possible at all.
    """
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(manifest['title'])} v{manifest['version']}</title>
<style>{css}</style>
</head><body>
{title_page(manifest)}
<section class="toc-page"><h1 class="part-title">Contents</h1>{toc}</section>
<main>{body}</main>
</body></html>"""


# ----------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, help="output PDF path")
    ap.add_argument("--html-only", action="store_true", help="write the HTML and stop")
    ap.add_argument("--check", action="store_true", help="verify toolchain + manifest only")
    ap.add_argument("--measure", type=Path, metavar="FILE",
                    help="measure every diagram in one markdown file and report placement")
    ap.add_argument("--measure-all", action="store_true",
                    help="measure every diagram in the manifest (run after a Mermaid bump)")
    args = ap.parse_args()

    manifest = yaml.safe_load((HERE / "manifest.yaml").read_text(encoding="utf-8"))

    if not shutil.which("pandoc"):
        sys.exit("!! pandoc not found.  apt install pandoc  /  brew install pandoc")
    chrome = os.environ.get("CHROME_BIN") or find_chrome()

    if args.check:
        missing = [c for p in manifest["parts"] for c in p["chapters"]
                   if not (DOCS / c).exists()]
        if missing:
            print("!! missing chapters:\n   " + "\n   ".join(missing))
            return 1
        n = sum(len(p["chapters"]) for p in manifest["parts"])
        print(f"ok: pandoc + chrome present; {n} chapters in "
              f"{len(manifest['parts'])} parts all resolve.")
        return 0

    if args.measure or args.measure_all:
        if args.measure_all:
            targets = [DOCS / c for p_ in manifest["parts"] for c in p_["chapters"]]
        else:
            targets = [args.measure]
        js = ensure_mermaid()
        rows, low = [], 0
        for t in targets:
            if not t.exists():
                print(f"!! missing: {t}")
                continue
            srcs = MERMAID_RE.findall(t.read_text(encoding="utf-8"))
            if not srcs:
                continue
            for i, plan in enumerate(measure_diagrams([x.rstrip() for x in srcs], chrome, js)):
                low += plan["below_floor"]
                rows.append((t.name, i + 1, plan))
        print(f"{'file':44} {'#':>2}  {'source px':>13}  {'placement':<14} "
              f"{'box mm':>15}  {'pt':>6}")
        for name, i, pl in rows:
            flag = "  BELOW FLOOR" if pl["below_floor"] else ""
            print(f"{name[:44]:44} {i:>2}  {pl['src_w']:>6.0f}x{pl['src_h']:<6.0f} "
                  f"{pl['kind']:<14} {pl['width_mm']:>6.1f}x{pl['height_mm']:<7.1f} "
                  f"{pl['pt']:>6.2f}{flag}")
        print(f"\n{len(rows)} figures, {low} below the {LEGIBILITY_FLOOR_PT} pt floor.")
        return 0

    print(f"==> Building {manifest['title']} v{manifest['version']}")
    md, store, captions, _ = build_markdown(manifest)
    print(f"    {sum(len(p['chapters']) for p in manifest['parts'])} chapters, "
          f"{len(store)} mermaid diagrams, {len(md):,} chars")

    print("    measuring diagrams (headless) and planning placement ...")
    figures = measure_diagrams(store, chrome, ensure_mermaid())
    below = [i for i, f in enumerate(figures) if f["below_floor"]]
    for i in below:
        print(f"    note: figure {i + 1} prints at {figures[i]['pt']}pt "
              f"({figures[i]['src_w']:.0f}x{figures[i]['src_h']:.0f}px), below the "
              f"{LEGIBILITY_FLOOR_PT}pt floor; re-source or carry by decision")

    proc = subprocess.run(
        ["pandoc", "--from=gfm+definition_lists", "--to=html5", "--wrap=none"],
        input=md, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        sys.exit(f"!! pandoc failed:\n{proc.stderr}")

    body = postprocess(proc.stdout, store, figures, captions)
    body, toc = render_toc(body)
    css = (HERE / "assets" / "handbook.css").read_text(encoding="utf-8")
    doc = assemble(manifest, body, toc, css)

    out_pdf = args.out or (DOCS / manifest["output"])
    tmp = Path(tempfile.mkdtemp(prefix="treklink-handbook-"))
    html_path = tmp / "handbook.html"
    html_path.write_text(doc, encoding="utf-8")

    if args.html_only:
        keep = out_pdf.with_suffix(".html")
        shutil.copy(html_path, keep)
        print(f"==> HTML written: {keep}")
        return 0

    print("    paginating via headless Chrome (diagrams already inline) ...")
    result = subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
         "--run-all-compositor-stages-before-draw", "--virtual-time-budget=60000",
         f"--print-to-pdf={out_pdf}", html_path.as_uri()],
        capture_output=True, text=True, timeout=300,
    )
    if not out_pdf.exists():
        sys.exit(f"!! Chrome produced no PDF.\n{result.stderr[-2000:]}")

    shutil.rmtree(tmp, ignore_errors=True)
    print(f"==> {out_pdf}  ({out_pdf.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
