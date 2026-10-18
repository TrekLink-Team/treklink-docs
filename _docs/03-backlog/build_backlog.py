#!/usr/bin/env python3
"""TrekLink backlog generator, rewritten 2026-10-18 for the D-033 to D-050 scope.

Writes:
  - 01-epics.md          epics with their stories
  - 02-user-stories.md   one story per use case, acceptance criteria from the SRS FRs
  - User_Story_Agile_TrekLink.xlsx (00-project-context/, or the path given as argv[1])

Source of truth (Q18 and Q19 of the 2026-10-18 grill session, D-048):
  - Stories are the SRS use cases. The catalogue, the specifications and the functional
    requirements come from `capstone/scripts/srs/srs_data.py`, the same data that builds
    Report 3, so the backlog cannot drift from the SRS. Set TREKLINK_SRS to the folder
    holding `srs_data.py` when this checkout is not inside `capstone/`.
  - Story IDs are `US-UCnn` for use case nn, and `US-Xnn` for cross-cutting work with no
    use case; epic IDs are `EP01` to `EP10`. The old `E1` to `E8` and `US-001` to `US-087`
    cards in Jira belong to the pre-D-033 scope and are retired (`jira_sync.py --retire`);
    the new IDs never collide with their `backlog-E<n>` and `backlog-US-0nn` labels.
  - `baseline` marks the 44 use cases that deliver a use case of the week 3 Report 3
    (`srs_data.W3_MAP`). The SEP490 syllabus requires 75% of the week 3 set completed
    (risk row of 2026-10-18).
  - Owners follow the module lanes of roadmap section 5.1 (remapped 2026-10-18). LongNN
    owns the read-only screen use cases (UI_OWNED, as D-023 split MF-04 by layer) and is
    the secondary owner of every other story with a human actor, for its screens.
  - Sprints follow roadmap section 4.2: MF-01, MF-02 and cross-cutting work in Sprint 3
    (W7 to W8), MF-03 and MF-04 in Sprint 4 (W9 to W10), MF-05 in Sprint 5 (W11).
  - Story points come from the use case size: steps plus alternatives (2 for up to 3,
    3 for up to 5, 5 for up to 8, otherwise 8).

Edit the data here or in srs_data.py, then regenerate. Never hand-edit the outputs.
"""

from __future__ import annotations

import os
import re
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
SRS_DIR = os.environ.get("TREKLINK_SRS", os.path.join(HERE, "..", "..", "..", "scripts", "srs"))
sys.path.insert(0, os.path.abspath(SRS_DIR))
try:
    import srs_data  # noqa: E402
except ImportError:
    sys.exit(f"!! srs_data.py not found in {os.path.abspath(SRS_DIR)}; set TREKLINK_SRS")

# ---------------------------------------------------------------------------
# 1. Team and lanes (roadmap section 5.1)
# ---------------------------------------------------------------------------
TEAM = {
    "Khoa": {"full_name": "Đỗ Đăng Khoa", "code": "KhoaDD", "mssv": "SE192357", "role": "Leader"},
    "LongLP": {"full_name": "Lâm Phi Long", "code": "LongLP", "mssv": "SE182769", "role": "Member"},
    "HoangTK": {"full_name": "Trần Khải Hoàng", "code": "HoangTK", "mssv": "SE182767", "role": "Member"},
    "LongNN": {"full_name": "Nguyễn Ngọc Long", "code": "LongNN", "mssv": "SE193490", "role": "Member"},
    "TanNB": {"full_name": "Nguyễn Bá Tân", "code": "TanNB", "mssv": "SE183860", "role": "Member"},
}

LANE = {
    "auth": "LongLP", "rentals": "LongLP", "billing": "LongLP",
    "organizations": "TanNB",
    "devices": "Khoa", "gateway-sync": "Khoa", "platform": "Khoa",
    "incidents": "HoangTK", "monitoring": "HoangTK",
    "frontend": "LongNN", "devops": "Khoa",
}

# ---------------------------------------------------------------------------
# 2. Epics, one per backend module plus cross-cutting delivery
# ---------------------------------------------------------------------------
EPICS = [
    {"id": "EP01", "name": "Identity and access", "module": "auth",
     "desc": "Login, silent renewal, logout, password reset, platform accounts, and roles and permissions held as data with CASL policies on every mutating endpoint."},
    {"id": "EP02", "name": "Organizations", "module": "organizations",
     "desc": "Organization self-registration, verification with the master contract (NDA and software licence), approval, members, the on-duty roster, API keys and Field Station credentials, suspension and compliance cases."},
    {"id": "EP03", "name": "Device assets and maintenance", "module": "devices",
     "desc": "The device lifecycle: registration, intake check, hardware variants with service plans, provisioning, inspection, loss cases, disposal, maintenance with cost approval, the weekly service scan and stock-take."},
    {"id": "EP04", "name": "Rental contracts", "module": "rentals",
     "desc": "Rental contract request, availability check, approval, handover with signed note, cancellation notice, monthly roll-over, holder labels, mid-contract replacement and closure."},
    {"id": "EP05", "name": "Field data and synchronization", "module": "gateway-sync",
     "desc": "Ingestion of field events from the Field Station with idempotency, the offline queue flush in priority order, the local field picture and the Field Station release download."},
    {"id": "EP06", "name": "Incidents and alerts", "module": "incidents",
     "desc": "Incident creation from SOS and cadence anomalies, tiered alerts and escalation, acknowledgement, status reports, false alarms, reports to authorities, reopening and closing."},
    {"id": "EP07", "name": "Live monitoring", "module": "monitoring",
     "desc": "The live map over WebSocket, the organization telemetry API, device history, stale-device marking, system health and check-in telemetry."},
    {"id": "EP08", "name": "Billing", "module": "billing",
     "desc": "Online payment through SePay, counter payments, contract balance with late and damage fees, damage charge approval, loss charges and reports."},
    {"id": "EP09", "name": "Platform configuration and audit", "module": "platform",
     "desc": "Plans and prices, business parameters from the Configuration Matrix, the audit log and the scheduler."},
    {"id": "EP10", "name": "Delivery and quality", "module": "devops",
     "desc": "Local stack, CI, seed data, deployment to Neon, and the separate isolation and load test suite of D-042."},
]
EPIC_BY_MODULE = {e["module"]: e for e in EPICS}

# FR prefix to backend module.
PREFIX_MODULE = {
    "AUTH": "auth", "ORG": "organizations", "DEV": "devices", "CON": "rentals",
    "BILL": "billing", "EVT": "gateway-sync", "INC": "incidents", "MON": "monitoring",
    "CFG": "platform",
}

# A use case whose FRs span modules goes to the module that owns its screen and data.
MODULE_OVERRIDE = {
    4: "organizations", 6: "organizations", 17: "rentals", 20: "rentals", 38: "monitoring",
    40: "monitoring", 41: "monitoring", 42: "monitoring", 43: "devices", 55: "rentals", 58: "platform",
    59: "monitoring", 60: "devices",
}

# Read-only screen use cases owned by the frontend lane, split by layer as in D-023: LongNN
# owns the screen, the backend lane owner is secondary for the read API.
UI_OWNED = {38, 42, 55, 59}

# Main-flow path use cases outside the week 3 baseline: needed for a flow to run end to end.
FLOW_PATH = {2, 3, 12, 23, 24, 51}
# Use cases that can slip to the last iteration without breaking a main flow.
LOW = {39, 40, 54, 62, 63, 64, 65}

ROADMAP_SPRINT = {"MF-01": 3, "MF-02": 3, "X": 3, "MF-03": 4, "MF-04": 4, "MF-05": 5}
# Roadmap section 4.2: sprint -> (first week, last week). jira_sync.py dates sprints from it.
SPRINT_RANGE = {1: (1, 3), 2: (4, 6), 3: (7, 8), 4: (9, 10), 5: (11, 11), 6: (12, 12), 7: (13, 15)}
SPRINT_WEEKS = {n: (f"W{a}" if a == b else f"W{a} to W{b}") for n, (a, b) in SPRINT_RANGE.items()}
SYSTEM_ACTORS = {"Scheduler", "Field Station", "TrekLink Device", "Payment Gateway",
                 "Organization System", "(included)", "(extends)"}

# ---------------------------------------------------------------------------
# 3. Jira keys
# Jira numbers issues itself. The new cards are created after the retired ones, so their
# keys are unknown until `jira_sync.py --apply` reports them; record each in JIRA_KEYS.
# Convention: 01-conventions/10-jira-tracking-and-workflow.md section 9.
# ---------------------------------------------------------------------------
JIRA_PROJECT_KEY = "TK"
JIRA_KEYS: dict[str, str] = {
    # "US-UC01": "TK-120",
}


def jira_of(item_id: str) -> str:
    return JIRA_KEYS.get(item_id, "")


# ---------------------------------------------------------------------------
# 4. Stories
# ---------------------------------------------------------------------------
def module_of(uc: int, frs: list[tuple]) -> str:
    if uc in MODULE_OVERRIDE:
        return MODULE_OVERRIDE[uc]
    counts: dict[str, int] = {}
    for fr in frs:
        m = PREFIX_MODULE[fr[0].split("-")[1]]
        counts[m] = counts.get(m, 0) + 1
    return max(counts, key=lambda m: (counts[m], -list(PREFIX_MODULE.values()).index(m)))


def points_of(spec: tuple) -> int:
    size = len(spec[3]) + len(spec[4])
    return 2 if size <= 3 else 3 if size <= 5 else 5 if size <= 8 else 8


def human_actors(actors: str) -> list[str]:
    return [a.strip() for a in actors.split(",") if a.strip() not in SYSTEM_ACTORS]


def story_text(actors: str, desc: str) -> str:
    """The SRS states the goal, not a benefit, so the story carries no invented "so that"."""
    people = human_actors(actors)
    goal = desc[0].lower() + desc[1:]
    if people:
        who = people[0] if len(people) == 1 else ", ".join(people[:-1]) + " or " + people[-1]
        art = "an" if who[0] in "AEIOU" else "a"
        return f"As {art} {who}, I want to {goal}"
    return f"System story: {desc}"


FR_BY_UC: dict[int, list[tuple]] = {}
for fr in srs_data.FR:
    for uc in fr[2]:
        FR_BY_UC.setdefault(uc, []).append(fr)

BASELINE = set(srs_data.COMMITTED)
W3_BY_UC: dict[int, list[int]] = {}
for w3, (_, targets) in srs_data.W3_MAP.items():
    for uc in targets:
        W3_BY_UC.setdefault(uc, []).append(w3)

STORIES: list[dict] = []
for uc, (name, actors, mfs, desc) in srs_data.UC.items():
    spec = srs_data.SPEC[uc]
    frs = FR_BY_UC.get(uc, [])
    module = module_of(uc, frs)
    owner = "LongNN" if uc in UI_OWNED else LANE[module]
    sprint = min(ROADMAP_SPRINT[m] for m in mfs)
    priority = "High" if uc in BASELINE or uc in FLOW_PATH else "Low" if uc in LOW else "Medium"
    ac = [f"{fr[0]}: {fr[1]}" for fr in frs]
    if spec[5]:
        ac.append("Business rules: " + ", ".join(spec[5]) + " (SRS section 3.3).")
    ac.append("Alternatives and exceptions: " + " ".join(spec[4]) if spec[4] else
              "No alternative flow in the SRS specification.")
    STORIES.append({
        "id": f"US-UC{uc:02d}",
        "uc": uc,
        "epic": EPIC_BY_MODULE[module]["id"],
        "module": module,
        "mainflow": ", ".join(mfs),
        "actor": actors,
        "summary": f"UC-{uc:02d} {name}",
        "story": story_text(actors, desc),
        "ac": ac,
        "frs": [fr[0] for fr in frs],
        "priority": priority,
        "points": points_of(spec),
        "sprint": sprint,
        "status": "Backlog",
        "assignee": owner,
        "secondary": LANE[module] if owner == "LongNN" else "LongNN" if human_actors(actors) else None,
        "reviewer": "LongLP" if owner == "Khoa" else "Khoa",
        "baseline": uc in BASELINE,
        "w3": W3_BY_UC.get(uc, []),
    })

CROSS_CUTTING = [
    ("Local stack and CI", "Docker Compose for Postgres, Mosquitto and the backend, and GitHub Actions running lint, typecheck, unit tests and build on every PR.",
     ["The stack SHALL start with one command and pass the health check of `GET /health`.",
      "WHEN a PR is opened, CI SHALL run lint, typecheck, unit tests and build, and SHALL block the merge on failure."],
     3, 3),
    ("Seed data and database script", "A seed that loads plans, hardware variants, devices, one active organization with members and one contract, for demos and tests; the migration history doubles as the database script of the software package.",
     ["The seed SHALL be idempotent and SHALL load on an empty database after `prisma migrate deploy`.",
      "The seed SHALL contain no real personal data."],
     2, 3),
    ("Deployment to Neon", "Shared dev and production databases on Neon (D-010), with migrations applied by the pipeline.",
     ["WHEN `dev` is updated, the pipeline SHALL apply pending migrations to the shared dev database.",
      "Connection strings SHALL come from environment variables only."],
     3, 4),
    ("Isolation and load test suite", "The separate suite of D-042: multi-organization isolation and ingestion load.",
     ["The suite SHALL show that no endpoint returns another organization's data.",
      "The suite SHALL report ingestion throughput and latency against the SRS non-functional targets."],
     5, 5),
]
for i, (summary, desc, ac, pts, sprint) in enumerate(CROSS_CUTTING, 1):
    STORIES.append({
        "id": f"US-X{i:02d}", "uc": None, "epic": "EP10", "module": "devops", "mainflow": "X",
        "actor": "Team", "summary": summary, "story": f"Delivery story: {desc}", "ac": ac, "frs": [],
        "priority": "High" if sprint == 3 else "Medium", "points": pts, "sprint": sprint,
        "status": "Backlog", "assignee": "Khoa", "secondary": "TanNB" if i == 4 else None,
        "reviewer": "LongLP", "baseline": False, "w3": [],
    })

for e in EPICS:
    mine = [s for s in STORIES if s["epic"] == e["id"]]
    e["story_count"] = len(mine)
    e["points_total"] = sum(s["points"] for s in mine)
    e["owner"] = LANE[e["module"]]
    e["sprints"] = sorted({s["sprint"] for s in mine})

TOTAL_POINTS = sum(s["points"] for s in STORIES)


def check() -> None:
    """Every FR belongs to at least one story; every story has acceptance criteria."""
    covered = {f for s in STORIES for f in s["frs"]}
    missing = [fr[0] for fr in srs_data.FR if fr[0] not in covered]
    if missing:
        sys.exit(f"!! FRs with no story: {missing}")
    for s in STORIES:
        if not s["ac"]:
            sys.exit(f"!! {s['id']} has no acceptance criteria")


# ---------------------------------------------------------------------------
# 5. Markdown
# ---------------------------------------------------------------------------
def slug(heading: str) -> str:
    """GitHub heading anchor."""
    s = heading.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def heading_of(s: dict) -> str:
    return f"{s['id']}, {s['summary']}"


def sprint_label(n: int) -> str:
    return f"Sprint {n} ({SPRINT_WEEKS[n]})"


def render_epics_md() -> str:
    base = [s for s in STORIES if s["baseline"]]
    w3_mapped = sum(1 for _, t in srs_data.W3_MAP.values() if t)
    out = [
        "# 01, Epics",
        "",
        "> Generated by `build_backlog.py` from the SRS data (`capstone/scripts/srs/srs_data.py`). Do not edit by hand.",
        "> One story per use case; acceptance criteria are the SRS functional requirements (rewritten 2026-10-18 for D-033 to D-050).",
        "",
        f"**Totals**: {len(EPICS)} epics, {len(STORIES)} stories ({len(srs_data.UC)} use cases and "
        f"{len(CROSS_CUTTING)} delivery stories), {TOTAL_POINTS} points.",
        "",
        f"**Week 3 baseline (SEP490 75% rule)**: {w3_mapped} of the {len(srs_data.W3_MAP)} week 3 use cases map onto "
        f"{len(base)} current use cases, marked `baseline` below. Completing all {len(base)} completes "
        f"{w3_mapped} of {len(srs_data.W3_MAP)} week 3 use cases; the floor is {int(len(srs_data.W3_MAP) * 0.75 + 0.999)}.",
        "",
        "| Epic | Name | Module | Stories | Points | Sprints | Owner |",
        "|---|---|---|---|---|---|---|",
    ]
    for e in EPICS:
        out.append(f"| {e['id']} | {e['name']} | `module:{e['module']}` | {e['story_count']} | "
                   f"{e['points_total']} | {', '.join(str(n) for n in e['sprints'])} | {e['owner']} |")
    out += ["", "---", ""]
    for e in EPICS:
        out += [f"## {e['id']}, {e['name']}", "", e["desc"], "",
                f"- **Module**: `module:{e['module']}`, lane owner {TEAM[e['owner']]['full_name']} ({e['owner']})",
                f"- **Stories**: {e['story_count']}, **points**: {e['points_total']}", "",
                "| Story | Summary | Main flow | Priority | Points | Sprint | Baseline |",
                "|---|---|---|---|---|---|---|"]
        for s in sorted((s for s in STORIES if s["epic"] == e["id"]), key=lambda s: (s["sprint"], s["id"])):
            out.append(f"| [{s['id']}](./02-user-stories.md#{slug(heading_of(s))}) | {s['summary']} | "
                       f"{s['mainflow']} | {s['priority']} | {s['points']} | {s['sprint']} | "
                       f"{'yes' if s['baseline'] else 'no'} |")
        out.append("")
    return "\n".join(out) + "\n"


def render_stories_md() -> str:
    out = [
        "# 02, User Stories",
        "",
        "> Generated by `build_backlog.py` from the SRS data. One story per use case. The acceptance",
        "> criteria are the SRS functional requirements that cite the use case; the module",
        "> `specs/{module}/tasks.md` lists the implementation tasks that reference them.",
        "",
    ]
    for e in EPICS:
        out += [f"## {e['id']}, {e['name']}", ""]
        for s in sorted((s for s in STORIES if s["epic"] == e["id"]), key=lambda s: (s["sprint"], s["id"])):
            sec = f", secondary {TEAM[s['secondary']]['full_name']} ({s['secondary']})" if s["secondary"] else ""
            key = jira_of(s["id"])
            branch = f"feat/{key}-<short-desc>" if key else "feat/<jira-key>-<short-desc>"
            w3 = (", week 3 " + ", ".join(f"UC-{n:02d}" for n in s["w3"])) if s["w3"] else ""
            out += [
                f"### {heading_of(s)}",
                "",
                f"`module:{s['module']}`, **{s['mainflow']}**, actor **{s['actor']}**, priority **{s['priority']}**, "
                f"**{s['points']}** points, **{sprint_label(s['sprint'])}**, status **{s['status']}**, "
                f"baseline **{'yes' if s['baseline'] else 'no'}**{w3}",
                "",
                f"**Jira**: {('`' + key + '`') if key else 'assigned at sync'}, **branch**: `{branch}`",
                "",
                f"**Owner**: {TEAM[s['assignee']]['full_name']} ({s['assignee']}){sec}, "
                f"**reviewer**: {TEAM[s['reviewer']]['full_name']} ({s['reviewer']})",
                "",
                f"**User story**: {s['story']}",
                "",
                "**Acceptance criteria**:",
                "",
            ]
            out += [f"{i}. {a}" for i, a in enumerate(s["ac"], 1)]
            out.append("")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# 6. Workbook
# ---------------------------------------------------------------------------
HEADER_FILL = PatternFill("solid", fgColor="1F3864")
HEADER_FONT = Font(name="Arial", size=11, bold=True, color="FFFFFF")
EPIC_FILL = PatternFill("solid", fgColor="DCE6F1")
BODY_FONT = Font(name="Arial", size=10)
WRAP = Alignment(wrap_text=True, vertical="top")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def sheet(wb: Workbook, title: str, headers: list[str], rows: list[list], widths: list[int], first=False):
    ws = wb.active if first else wb.create_sheet()
    ws.title = title
    ws.append(headers)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill, cell.font, cell.alignment, cell.border = HEADER_FILL, HEADER_FONT, WRAP, BORDER
    for r in rows:
        ws.append(r)
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font, cell.alignment, cell.border = BODY_FONT, WRAP, BORDER
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"
    return ws


def build_workbook(path: str) -> None:
    wb = Workbook()
    rows = []
    for e in EPICS:
        rows.append(["Epic", e["id"], e["name"], e["desc"], "", "", "", e["points_total"], "", "", "", ""])
        for s in (s for s in STORIES if s["epic"] == e["id"]):
            rows.append(["Story", s["id"], s["summary"], s["story"] + "\n\n" + "\n".join(s["ac"]),
                         e["id"], s["mainflow"], s["priority"], s["points"], s["sprint"], s["status"],
                         s["assignee"], "yes" if s["baseline"] else "no"])
    ws = sheet(wb, "Backlog", ["Issue Type", "Id", "Summary", "Description", "Parent", "Main flow",
                               "Priority", "Story Points", "Sprint", "Status", "Assignee", "Baseline"],
               rows, [10, 11, 38, 80, 8, 14, 10, 8, 8, 10, 10, 9], first=True)
    for row in ws.iter_rows(min_row=2):
        if row[0].value == "Epic":
            for cell in row:
                cell.fill = EPIC_FILL
    sheet(wb, "Week 3 baseline", ["Week 3 UC", "Week 3 name", "Current use cases", "Delivered by stories"],
          [[f"UC-{k:02d}", n, ", ".join(f"UC-{u:02d}" for u in t) or "removed by D-033",
            ", ".join(f"US-UC{u:02d}" for u in t)] for k, (n, t) in srs_data.W3_MAP.items()],
          [10, 34, 24, 28])
    load = []
    for k, m in TEAM.items():
        mine = [s for s in STORIES if s["assignee"] == k]
        sec = [s for s in STORIES if s["secondary"] == k]
        load.append([m["full_name"], m["code"], len(mine), sum(s["points"] for s in mine),
                     len(sec), ", ".join(sorted({s["module"] for s in mine}))])
    sheet(wb, "Workload", ["Member", "Code", "Stories", "Points", "Secondary stories", "Modules"],
          load, [24, 10, 9, 9, 16, 40])
    wb.save(path)
    print(f"Workbook written to {path}")


if __name__ == "__main__":
    check()
    with open(os.path.join(HERE, "01-epics.md"), "w", encoding="utf-8") as f:
        f.write(render_epics_md())
    with open(os.path.join(HERE, "02-user-stories.md"), "w", encoding="utf-8") as f:
        f.write(render_stories_md())
    print(f"Markdown written: {len(EPICS)} epics, {len(STORIES)} stories, {TOTAL_POINTS} points.")
    default_xlsx = os.path.join(HERE, "..", "00-project-context", "User_Story_Agile_TrekLink.xlsx")
    build_workbook(sys.argv[1] if len(sys.argv) > 1 else default_xlsx)
