#!/usr/bin/env python3
"""Replace em dashes in prose with commas, under the same exemptions as check_prose.py.

    python3 .github/scripts/fix_prose.py [--root DIR] [--write] [FILE ...]

Dry run by default: lists every file that would change and how many dashes each loses. With
--write it edits them in place. Only Markdown is touched, and only lines outside code fences.
Inline code spans, "not applicable" table cells and files whose first line is the marker
`<!-- prose: keep-dashes -->` are left alone, so a document that genuinely needs the dash keeps it.

Convention: _docs/01-conventions/14-prose-and-wording.md section 6.3 (D-024). A mechanical pass is
reviewed by sampling its diff (section 6.2); run check_prose.py afterwards.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from check_prose import CODESPAN, EXCLUDE, FENCE, NA_CELL

KEEP_MARKER = "<!-- prose: keep-dashes -->"   # honoured only as the first line of a file
DASH = re.compile(r"\s*\u2014\s*")


def fix_segment(text: str) -> str:
    # A spaced, unspaced or half-spaced dash becomes ", "; a doubled comma collapses.
    out = DASH.sub(", ", text)
    return re.sub(r",\s*,", ",", out)


def fix_line(line: str) -> str:
    if "\u2014" not in line:
        return line
    keep = [(m.start(), m.end()) for m in CODESPAN.finditer(line)]
    keep += [(m.start(), m.end()) for m in NA_CELL.finditer(line)]
    keep.sort()
    out, pos = [], 0
    for a, b in keep:
        if a < pos:
            continue
        out.append(fix_segment(line[pos:a]))
        out.append(line[a:b])
        pos = b
    out.append(fix_segment(line[pos:]))
    fixed = "".join(out)
    # A dash that opened a line (list item, quotation attribution) must not leave a leading comma.
    m = re.match(r"^(\s*[-*>|]?)\s*,\s*", fixed)
    if m:
        lead = m.group(1)
        fixed = (lead + " " if lead.strip() else lead) + fixed[m.end():]
    # A dash that ended a line leaves ", " behind; keep the comma, drop the trailing space.
    return fixed.rstrip(" ") if not line.endswith(" ") else fixed


def fix_text(text: str) -> tuple[str, int]:
    if text.startswith(KEEP_MARKER):
        return text, 0
    lines, in_fence, n = text.split("\n"), False, 0
    for i, line in enumerate(lines):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            new = fix_line(line)
            if new != line:
                n += line.count("\u2014") - new.count("\u2014")
                lines[i] = new
    return "\n".join(lines), n


def targets(root: Path, files: list[str]) -> list[Path]:
    if files:
        return [Path(f) for f in files]
    return sorted(
        p for p in root.rglob("*.md")
        if p.is_file() and not any(x in p.relative_to(root).as_posix() for x in EXCLUDE)
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=Path(__file__).resolve().parents[2], type=Path)
    ap.add_argument("--write", action="store_true", help="edit files in place")
    ap.add_argument("files", nargs="*")
    args = ap.parse_args()
    total = 0
    for p in targets(args.root, args.files):
        text = p.read_text(encoding="utf-8")
        new, n = fix_text(text)
        if n:
            total += n
            print(f"{p}: {n}")
            if args.write:
                p.write_text(new, encoding="utf-8")
    verb = "replaced" if args.write else "would replace"
    print(f"{verb} {total} em dash(es)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
