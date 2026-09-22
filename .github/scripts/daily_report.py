#!/usr/bin/env python3
"""Open and close the TrekLink daily-report issue.

Convention: 01-conventions/12-communication-and-daily-reports.md §3

    open   08:00 ICT, Mon-Fri, create "DAILY REPORT DD/MM/YYYY", @-mention the team
                                 (which sends everyone the notification email), attach
                                 the schedule countdown.
    close  12:00 ICT, same day, hard cutoff. Post who reported and who didn't, then
                                 close. A late member REOPENS, reports, closes again,
                                 and the timeline is the lateness log.

Skips weekends and any date listed in .github/schedule.yml `holidays`.

Auth: GITHUB_TOKEN (the workflow's default token is sufficient, same-repo issues).

Usage:
    python3 daily_report.py open
    python3 daily_report.py close
    python3 daily_report.py open --dry-run --date 2026-09-14
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("!! PyYAML is required:  pip install pyyaml")

HERE = Path(__file__).resolve().parent
CONFIG = HERE.parent / "schedule.yml"
ICT = timezone(timedelta(hours=7))
API = "https://api.github.com"
LABEL = "type:daily-report"


# ------------------------------------------------------------------------- github
def gh(path: str, method: str = "GET", payload: dict | None = None) -> dict | list:
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        sys.exit("!! GITHUB_TOKEN and GITHUB_REPOSITORY must be set.")
    url = path if path.startswith("http") else f"{API}/repos/{repo}{path}"
    req = urllib.request.Request(
        url, method=method,
        data=json.dumps(payload).encode() if payload else None,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
            "User-Agent": "treklink-daily-report",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read() or "{}")
    except urllib.error.HTTPError as e:
        sys.exit(f"!! GitHub API {e.code} on {method} {url}\n{e.read().decode()[:800]}")


# -------------------------------------------------------------------------- utils
def load_cfg() -> dict:
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def today_ict() -> date:
    return datetime.now(ICT).date()


def should_skip(cfg: dict, when: date) -> str | None:
    if when.weekday() >= 5:
        return "weekend"
    for h in cfg.get("holidays") or []:
        if h["date"] == when:
            return f"holiday: {h['name']}"
    return None


def title_for(when: date) -> str:
    return f"DAILY REPORT {when.strftime('%d/%m/%Y')}"


def countdown_md(when: date) -> str:
    try:
        out = subprocess.run(
            [sys.executable, str(HERE / "countdown.py"), "--markdown", "--date", when.isoformat()],
            capture_output=True, text=True, timeout=30,
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except Exception:                                           # noqa: BLE001
        return ""


def mention(cfg: dict, code: str) -> str:
    handle = (cfg.get("github_handles") or {}).get(code, "")
    # An unconfigured placeholder must not render as a broken @-mention.
    if not handle or handle.startswith("TODO"):
        return f"**{code}**"
    return f"@{handle}"


def mention_with_code(cfg: dict, code: str) -> str:
    """`@handle (KhoaDD)`, the roll-call form.

    A bare @handle notifies but does not say whose report it is, because the
    handles do not resemble the team codes. Carrying both means the roll-call is
    readable and the notification still fires. A markdown link would render
    identically and notify nobody, so never write one here.
    """
    rendered = mention(cfg, code)
    return rendered if rendered == f"**{code}**" else f"{rendered} ({code})"


def find_issue(when: date) -> dict | None:
    issues = gh(f"/issues?state=all&labels={LABEL}&per_page=50")
    want = title_for(when)
    for i in issues:                                            # type: ignore[union-attr]
        if i.get("title") == want:
            return i
    return None


# --------------------------------------------------------------------------- open
def do_open(cfg: dict, when: date, dry: bool) -> int:
    skip = should_skip(cfg, when)
    if skip:
        print(f"==> Skipping {when} ({skip}). No issue created.")
        return 0
    if not dry and find_issue(when):
        print(f"==> {title_for(when)} already exists. Nothing to do.")
        return 0

    checklist = "\n".join(f"- [ ] {mention_with_code(cfg, c)}" for c in cfg["team"])
    body = f"""Report **before 12:00 ICT**. This issue closes automatically at midday.

### Format: exactly three fields

```markdown
YourCode

Yesterday: what you did (link the PR / issue)
Today: what you will do

Issues: blocker, or None
```

English is required. Vietnamese is tolerated by exception **here only**, when English
would cost you clarity about a blocker.

---

### Reported

{checklist}

---

{countdown_md(when)}

---

> **The 12:00 cutoff is hard.** Missed it? **Reopen** this issue, post your report, close it
> again. The reopen is deliberately visible, this timeline is the lateness log.
>
> <sub>Opened automatically · convention: `01-conventions/12-communication-and-daily-reports.md` §3</sub>
"""

    if dry:
        print(f"--- would create: {title_for(when)}\n{body}")
        return 0

    issue = gh("/issues", "POST", {"title": title_for(when), "body": body, "labels": [LABEL]})
    print(f"==> Created #{issue['number']}: {issue['title']}")  # type: ignore[index]
    return 0


# -------------------------------------------------------------------------- close
def do_close(cfg: dict, when: date, dry: bool) -> int:
    skip = should_skip(cfg, when)
    if skip:
        print(f"==> Skipping {when} ({skip}).")
        return 0

    issue = find_issue(when)
    if not issue:
        print(f"==> No issue found for {when}. Nothing to close.")
        return 0
    if issue["state"] == "closed":
        print(f"==> #{issue['number']} already closed.")
        return 0

    comments = gh(f"/issues/{issue['number']}/comments?per_page=100")
    # Exclude this script's own comments. The close comment now carries every
    # member code (see mention_with_code), so on a reopen-report-reclose cycle an
    # unfiltered blob would read its own previous roll-call back and credit
    # everyone. No human member has a `[bot]` login.
    human = [c for c in comments                                # type: ignore[union-attr]
             if not c.get("user", {}).get("login", "").endswith("[bot]")]
    blob = "\n".join(c.get("body", "") for c in human)
    authors = {c.get("user", {}).get("login", "").lower() for c in human}

    reported, missing = [], []
    for code in cfg["team"]:
        handle = (cfg.get("github_handles") or {}).get(code, "")
        # Count a member as reported if their code appears in any comment, or if their
        # GitHub account authored one. The code check is what actually works day to day,
        # since several members may share one account early on.
        seen = bool(re.search(rf"\b{re.escape(code)}\b", blob, re.IGNORECASE)) or (
            handle and not handle.startswith("TODO") and handle.lower() in authors)
        (reported if seen else missing).append(code)

    lines = [f"**Cutoff reached, 12:00 ICT {when.strftime('%d/%m/%Y')}.**", ""]
    lines.append(f"Reported ({len(reported)}/{len(cfg['team'])}): "
                 + (", ".join(mention_with_code(cfg, c) for c in reported)
                    if reported else "_nobody_"))
    if missing:
        lines += ["", "**Did not report before the cutoff:** "
                  + ", ".join(mention(cfg, c) for c in missing),
                  "",
                  "Reopen this issue, post your report, and close it again. "
                  "The reopen is the record."]
    else:
        lines += ["", "Full attendance. Closing."]

    if dry:
        print(f"--- would comment on #{issue['number']} and close:\n" + "\n".join(lines))
        return 0

    gh(f"/issues/{issue['number']}/comments", "POST", {"body": "\n".join(lines)})
    gh(f"/issues/{issue['number']}", "PATCH", {"state": "closed"})
    print(f"==> Closed #{issue['number']}, reported: {reported}, missing: {missing}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["open", "close"])
    ap.add_argument("--date", help="YYYY-MM-DD; override today (for testing)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = load_cfg()
    when = date.fromisoformat(args.date) if args.date else today_ict()
    return (do_open if args.action == "open" else do_close)(cfg, when, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
