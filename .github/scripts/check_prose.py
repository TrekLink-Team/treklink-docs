#!/usr/bin/env python3
"""Fail on prose that breaks 01-conventions/14-prose-and-wording.md (D-024).

Checks the two rules that are reliably detectable by regex:

    * an em dash used as prose punctuation
    * a banned generic opener

Everything else in chapter 14, aphorism formulas, two-beat antithesis,
unverified claims, fabricated precision, is review-enforced. A checker that
guesses at those produces false positives, and a check that cries wolf gets
ignored.

Not flagged, because they are data rather than prose:

    * anything inside a fenced code block
    * anything inside an inline code span
    * a table cell whose entire content is an em dash, the "not applicable"
      placeholder
    * any path under EXCLUDE

Usage:
    python3 check_prose.py                 # scan the repository
    python3 check_prose.py path/to/file.md # scan named files
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Course-issued and officially submitted documents. The registered project
# title is frozen; rewording it here would desynchronise it from the form the
# school holds. Generated artifacts are excluded because the fix belongs in the
# generator, not the output.
EXCLUDE = (
    "topics/",
    ".git/",
    "node_modules/",
    "ignore/",                       # gitignored personal scratch, not a deliverable
    "_docs/03-backlog/01-epics.md",
    "_docs/03-backlog/02-user-stories.md",
)

SUFFIXES = (".md", ".py", ".yml", ".yaml")

FENCE = re.compile(r"^\s*(```|~~~)")
CODESPAN = re.compile(r"`[^`\n]*`")
NA_CELL = re.compile(r"(?<=\|)\s*\u2014\s*(?=\|)")
# Only at the start of a sentence. Mid-sentence these phrases are usually a
# quotation or an ordinary clause, and flagging those trains people to ignore
# the check.
OPENERS = re.compile(
    r"(?:^|(?<=[.!?]\s)|(?<=[.!?]\s\s))"
    r"[\s>*\-#|]*"
    r"(Let's|In order to|It's worth noting|Needless to say|"
    r"At the end of the day|It goes without saying|Simply put)\b",
)


def strip_data(line: str) -> str:
    return CODESPAN.sub("``", NA_CELL.sub("", line))


def scan(path: Path) -> list[tuple[int, str, str]]:
    found: list[tuple[int, str, str]] = []
    in_fence = False
    for n, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        prose = strip_data(line)
        if "\u2014" in prose:
            found.append((n, "em dash", line.strip()))
        hit = OPENERS.search(prose)
        if hit:
            found.append((n, f"banned opener: {hit.group(1)}", line.strip()))
    return found


def targets(argv: list[str]) -> list[Path]:
    if argv:
        return [Path(a) for a in argv]
    root = Path(__file__).resolve().parents[2]
    return sorted(
        p for p in root.rglob("*")
        if p.suffix in SUFFIXES
        and p.is_file()
        and not any(x in p.relative_to(root).as_posix() for x in EXCLUDE)
    )


def main(argv: list[str]) -> int:
    total = 0
    for path in targets(argv):
        for n, rule, text in scan(path):
            total += 1
            print(f"{path}:{n}: {rule}: {text[:110]}")
    if total:
        print(f"\n{total} violation(s). See _docs/01-conventions/14-prose-and-wording.md.")
        return 1
    print("prose check clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
