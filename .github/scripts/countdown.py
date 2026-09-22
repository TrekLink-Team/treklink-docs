#!/usr/bin/env python3
"""Compute the TrekLink schedule countdown.

Two independent clocks, the team's 2-week sprint, and the external capstone
roadmap. They are not the same clock and one never implies the other, so both are
reported, and a week where they collide is flagged loudly.

Config: .github/schedule.yml   (edit that, not this)

Usage:
    python3 countdown.py                 # plain text block
    python3 countdown.py --markdown      # markdown, for an issue body
    python3 countdown.py --date 2026-10-15   # pretend it's that day (testing)
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("!! PyYAML is required:  pip install pyyaml")

CONFIG = Path(__file__).resolve().parents[1] / "schedule.yml"
ICT = timezone(timedelta(hours=7))


def today_ict() -> date:
    return datetime.now(ICT).date()


def humanize(days: int) -> str:
    """Phrasing degrades naturally as a deadline approaches."""
    if days < 0:
        n = abs(days)
        return "overdue by 1 day" if n == 1 else f"overdue by {n} days"
    if days == 0:
        return "TODAY"
    if days == 1:
        return "tomorrow"
    if days < 7:
        return f"{days} days"
    weeks, rem = divmod(days, 7)
    wk = "1 week" if weeks == 1 else f"{weeks} weeks"
    if rem == 0:
        return wk
    return f"{wk} {rem} day" + ("" if rem == 1 else "s")


def current_sprint(cfg: dict, when: date) -> tuple[int, date, date] | None:
    start = cfg["sprints"]["start"]
    length = int(cfg["sprints"]["length_days"])
    for i in range(int(cfg["sprints"]["count"])):
        s = start + timedelta(days=i * length)
        e = s + timedelta(days=length - 1)
        if s <= when <= e:
            return i + 1, s, e
    return None


def is_holiday(cfg: dict, when: date) -> str | None:
    for h in cfg.get("holidays") or []:
        if h["date"] == when:
            return h["name"]
    return None


def build(cfg: dict, when: date) -> list[dict]:
    """Everything still ahead of us, nearest first."""
    rows: list[dict] = []

    sprint = current_sprint(cfg, when)
    if sprint:
        num, _s, end = sprint
        rows.append({"label": f"Sprint {num} ends", "due": end,
                     "days": (end - when).days, "kind": "sprint"})

    for m in cfg.get("roadmap") or []:
        days = (m["due"] - when).days
        if days < -3:                      # drop things well past; keep just-missed visible
            continue
        rows.append({"label": m["name"], "due": m["due"], "days": days,
                     "kind": "roadmap", "critical": bool(m.get("critical"))})

    rows.sort(key=lambda r: r["days"])

    # Collision: a sprint boundary and a roadmap deadline in the same ISO week.
    sprint_rows = [r for r in rows if r["kind"] == "sprint"]
    if sprint_rows:
        sw = sprint_rows[0]["due"].isocalendar()[:2]
        for r in rows:
            if r["kind"] == "roadmap" and r["due"].isocalendar()[:2] == sw and r["days"] >= 0:
                r["collision"] = sprint_rows[0]["collision"] = True
    return rows


def render_text(rows: list[dict], when: date, holiday: str | None) -> str:
    out = ["NEXT UP" + f"   (as of {when.isoformat()} ICT)"]
    if holiday:
        out.append(f"  ** Holiday: {holiday}, no daily report today **")
    if not rows:
        out.append("  Nothing scheduled ahead. Check schedule.yml.")
        return "\n".join(out)

    width = max(len(r["label"]) for r in rows)
    for r in rows[:8]:
        dots = "." * max(2, width - len(r["label"]) + 3)
        flag = ""
        if r.get("collision"):
            flag = "   <-- COLLISION: sprint boundary + graded deadline"
        elif r.get("critical") and r["days"] <= 14:
            flag = "   <-- CRITICAL"
        out.append(f"  {r['label']} {dots} {humanize(r['days']):<18} "
                   f"({r['due'].strftime('%a %d %b')}){flag}")
    return "\n".join(out)


def render_markdown(rows: list[dict], when: date, holiday: str | None) -> str:
    out = [f"### Next up  <sub>as of {when.isoformat()} ICT</sub>", ""]
    if holiday:
        out += [f"> **Holiday: {holiday}**, no daily report today.", ""]
    if not rows:
        return "\n".join(out + ["_Nothing scheduled ahead, check `.github/schedule.yml`._"])

    out += ["| | Due in | Date |", "|---|---|---|"]
    for r in rows[:8]:
        label = r["label"]
        if r.get("collision"):
            label = f"**{label}** :warning: _sprint boundary + graded deadline_"
        elif r.get("critical") and r["days"] <= 14:
            label = f"**{label}** :rotating_light:"
        elif r["kind"] == "sprint":
            label = f"_{label}_"
        due = "**" + humanize(r["days"]) + "**" if r["days"] <= 3 else humanize(r["days"])
        out.append(f"| {label} | {due} | {r['due'].strftime('%a %d %b %Y')} |")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--markdown", action="store_true")
    ap.add_argument("--date", help="YYYY-MM-DD; override today (for testing)")
    args = ap.parse_args()

    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    when = date.fromisoformat(args.date) if args.date else today_ict()
    rows = build(cfg, when)
    holiday = is_holiday(cfg, when)

    print(render_markdown(rows, when, holiday) if args.markdown
          else render_text(rows, when, holiday))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
