#!/usr/bin/env python3
"""Build the TrekLink Developer Handbook PDF from the markdown SSOT.

The markdown in `_docs/` is the manual. This script renders it; it never authors
anything. If the PDF and the markdown disagree, the markdown wins — rebuild.

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
MERMAID_VERSION = "10.9.1"
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
def preprocess(md: str, store: list[str]) -> str:
    """Make one chapter's markdown safe and self-contained for print."""
    # 1. Pull mermaid blocks out before pandoc so it can't mangle the syntax.
    def _stash(m: re.Match) -> str:
        store.append(m.group(1).rstrip())
        return f"\n<!--MERMAID:{len(store) - 1}-->\n"

    md = MERMAID_RE.sub(_stash, md)

    # 2. GitHub alerts -> a marker pandoc passes through; styled by CSS later.
    md = ALERT_RE.sub(lambda m: f"> <!--ALERT:{m.group(1)}-->", md)

    # 3. Repo-relative .md links can't resolve in a PDF. Keep the label, drop the href,
    #    and render the target as a small monospace breadcrumb so the reader can find it.
    md = RELLINK_RE.sub(
        lambda m: f"{m.group(1)} (`{Path(m.group(2)).name}`)", md)

    return md


def postprocess(body: str, store: list[str]) -> str:
    """Re-inject mermaid and convert alert markers into styled callouts."""
    # Alerts: pandoc wraps our marker inside the blockquote. Promote it to a class.
    def _alert(m: re.Match) -> str:
        kind = m.group(1).lower()
        return f'<blockquote class="alert alert-{kind}"><p class="alert-title">{m.group(1).title()}</p>'

    body = re.sub(r"<blockquote>\s*<p><!--ALERT:(\w+)--></p>", _alert, body)
    body = re.sub(r"<blockquote>\s*<p><!--ALERT:(\w+)-->\s*", _alert, body)

    # Mermaid: replace the placeholder paragraph with a .mermaid element.
    def _mermaid(m: re.Match) -> str:
        src = html.escape(store[int(m.group(1))])
        return f'<div class="mermaid-wrap"><pre class="mermaid">{src}</pre></div>'

    body = re.sub(r"<p><!--MERMAID:(\d+)--></p>", _mermaid, body)
    body = re.sub(r"<!--MERMAID:(\d+)-->", _mermaid, body)
    return body


# ------------------------------------------------------------------------- assembly
def build_markdown(manifest: dict) -> tuple[str, list[str], list[dict]]:
    chunks: list[str] = []
    store: list[str] = []
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
            chunks.append(preprocess(path.read_text(encoding="utf-8"), store))

    if missing:
        sys.exit("!! Manifest references files that do not exist:\n   " + "\n   ".join(missing))
    return "\n".join(chunks), store, outline


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


def assemble(manifest: dict, body: str, toc: str, css: str, mermaid_js: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(manifest['title'])} v{manifest['version']}</title>
<style>{css}</style>
</head><body>
{title_page(manifest)}
<section class="toc-page"><h1 class="part-title">Contents</h1>{toc}</section>
<main>{body}</main>
<script>{mermaid_js}</script>
<script>
  mermaid.initialize({{
    startOnLoad: false, theme: 'base', securityLevel: 'loose',
    fontFamily: 'Inter, "Segoe UI", system-ui, sans-serif',
    themeVariables: {{
      primaryColor:'#eef2ff', primaryTextColor:'#1e1b4b', primaryBorderColor:'#6366f1',
      lineColor:'#64748b', secondaryColor:'#f1f5f9', tertiaryColor:'#f8fafc',
      fontSize:'13px'
    }}
  }});
  (async () => {{
    try {{ await mermaid.run({{ querySelector: '.mermaid' }}); }}
    catch (e) {{ console.error('mermaid:', e); }}
    // Readiness flag for debugging only — never mutate document.title, it becomes
    // the PDF's Title metadata.
    document.documentElement.setAttribute('data-handbook-ready', 'true');
  }})();
</script>
</body></html>"""


# ----------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, help="output PDF path")
    ap.add_argument("--html-only", action="store_true", help="write the HTML and stop")
    ap.add_argument("--check", action="store_true", help="verify toolchain + manifest only")
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

    print(f"==> Building {manifest['title']} v{manifest['version']}")
    md, store, _ = build_markdown(manifest)
    print(f"    {sum(len(p['chapters']) for p in manifest['parts'])} chapters, "
          f"{len(store)} mermaid diagrams, {len(md):,} chars")

    proc = subprocess.run(
        ["pandoc", "--from=gfm+definition_lists", "--to=html5", "--wrap=none"],
        input=md, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        sys.exit(f"!! pandoc failed:\n{proc.stderr}")

    body = postprocess(proc.stdout, store)
    body, toc = render_toc(body)
    css = (HERE / "assets" / "handbook.css").read_text(encoding="utf-8")
    doc = assemble(manifest, body, toc, css, ensure_mermaid())

    out_pdf = args.out or (DOCS / manifest["output"])
    tmp = Path(tempfile.mkdtemp(prefix="treklink-handbook-"))
    html_path = tmp / "handbook.html"
    html_path.write_text(doc, encoding="utf-8")

    if args.html_only:
        keep = out_pdf.with_suffix(".html")
        shutil.copy(html_path, keep)
        print(f"==> HTML written: {keep}")
        return 0

    print("    rendering via headless Chrome (mermaid renders in-browser) ...")
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
