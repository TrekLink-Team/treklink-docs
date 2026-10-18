#!/usr/bin/env python3
"""Create the backlog's epics, stories and sprints in Jira Cloud.

    python3 _docs/03-backlog/jira_sync.py            # dry run: print the plan
    python3 _docs/03-backlog/jira_sync.py --apply    # create in Jira
    python3 _docs/03-backlog/jira_sync.py --retire   # label and close the pre-D-033 cards

Reads EPICS and STORIES from build_backlog.py, so Jira mirrors the backlog one for one
(10-jira-tracking-and-workflow.md section 2.1). Credentials come from the environment and are never
stored:

    JIRA_BASE_URL   https://<site>.atlassian.net
    JIRA_EMAIL      the leader's Atlassian account email
    JIRA_API_TOKEN  an API token from https://id.atlassian.com/manage-profile/security/api-tokens
    JIRA_BOARD_ID   the Scrum board of project TK (the number in the board URL)

Safe to re-run. Every card carries the label `backlog-<ID>` (for example `backlog-US-UC08`); a card
that already exists is skipped, never duplicated. Cards are created epics first, then stories, in
backlog order. Jira assigns the keys; the run prints them so they can be recorded in
`build_backlog.JIRA_KEYS`.

Sprints are the roadmap sprints of section 4.2 (`build_backlog.SPRINT_RANGE`), dated from the
week 1 Monday in .github/schedule.yml. Stories planned for a sprint that has already ended carry
into the current sprint, per section 7.1 step 4.

`--retire` handles the pre-D-033 backlog (2026-10-18 rewrite): every card labelled `backlog-E1`
to `backlog-E8` or `backlog-US-001` to `backlog-US-087` gets the label `retired-d033` and is moved
to the board's Done transition when one exists.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_backlog as bb  # noqa: E402

WEEK_ONE = dt.date(2026, 9, 7)        # .github/schedule.yml sprints.start, Monday of week 1


class Jira:
    def __init__(self) -> None:
        self.base = os.environ["JIRA_BASE_URL"].rstrip("/")
        auth = f'{os.environ["JIRA_EMAIL"]}:{os.environ["JIRA_API_TOKEN"]}'.encode()
        self.headers = {"Authorization": "Basic " + base64.b64encode(auth).decode(),
                        "Accept": "application/json", "Content-Type": "application/json"}

    def call(self, method: str, path: str, body: dict | None = None) -> dict:
        req = urllib.request.Request(self.base + path, method=method, headers=self.headers,
                                     data=json.dumps(body).encode() if body is not None else None)
        try:
            with urllib.request.urlopen(req) as r:
                raw = r.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            sys.exit(f"!! {method} {path}: HTTP {e.code}: {e.read().decode()[:400]}")

    def find(self, label: str) -> str | None:
        jql = urllib.parse.quote(f'project = {bb.JIRA_PROJECT_KEY} AND labels = "{label}"')
        hits = self.call("GET", f"/rest/api/3/search/jql?jql={jql}&fields=key&maxResults=1")
        issues = hits.get("issues", [])
        return issues[0]["key"] if issues else None

    def points_field(self) -> str | None:
        for f in self.call("GET", "/rest/api/3/field"):
            if f.get("name") in ("Story point estimate", "Story Points"):
                return f["id"]
        return None


def adf(text: str) -> dict:
    """Plain paragraphs in Atlassian Document Format."""
    return {"type": "doc", "version": 1, "content": [
        {"type": "paragraph", "content": [{"type": "text", "text": p}]}
        for p in text.split("\n\n") if p.strip()]}


def sprint_dates(n: int) -> tuple[dt.date, dt.date]:
    first, last = bb.SPRINT_RANGE[n]
    return (WEEK_ONE + dt.timedelta(weeks=first - 1),
            WEEK_ONE + dt.timedelta(weeks=last, days=-1))


def current_sprint(today: dt.date) -> int:
    for n in sorted(bb.SPRINT_RANGE):
        if today <= sprint_dates(n)[1]:
            return n
    return max(bb.SPRINT_RANGE)


def plan(today: dt.date) -> tuple[list[tuple[int, dt.date, dt.date]], dict[int, list[dict]]]:
    now = current_sprint(today)
    last = max(s["sprint"] for s in bb.STORIES)
    first = max(now, min(s["sprint"] for s in bb.STORIES))
    sprints = [(n, *sprint_dates(n)) for n in range(first, last + 1)]
    by_sprint: dict[int, list[dict]] = {}
    for s in bb.STORIES:
        by_sprint.setdefault(max(s["sprint"], now), []).append(s)
    return sprints, by_sprint


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--apply", action="store_true", help="create the cards and sprints in Jira")
    ap.add_argument("--retire", action="store_true", help="label and close the pre-D-033 cards")
    args = ap.parse_args()
    if args.retire:
        return retire(Jira())
    today = dt.date.today()
    sprints, by_sprint = plan(today)
    print(f"{len(bb.EPICS)} epics, {len(bb.STORIES)} stories; current sprint {current_sprint(today)}")
    for n, a, b in sprints:
        print(f"  Sprint {n}: {a} to {b}, {len(by_sprint.get(n, []))} stories")
    if not args.apply:
        print("dry run; add --apply to create them")
        return 0

    board_id = os.environ.get("JIRA_BOARD_ID", "")
    if not board_id.isdigit():
        sys.exit(f"!! JIRA_BOARD_ID must be the board number from the board URL, got {board_id!r}")
    j = Jira()
    pts = j.points_field()
    keys: dict[str, str] = {}
    for e in bb.EPICS:
        label = f"backlog-{e['id']}"
        key = j.find(label) or j.call("POST", "/rest/api/3/issue", {"fields": {
            "project": {"key": bb.JIRA_PROJECT_KEY}, "issuetype": {"name": "Epic"},
            "summary": f"{e['id']}: {e['name']}", "labels": [label]}})["key"]
        keys[e["id"]] = key
        print(f"{e['id']} -> {key}")
    for s in bb.STORIES:
        label = f"backlog-{s['id']}"
        key = j.find(label)
        if not key:
            fields = {"project": {"key": bb.JIRA_PROJECT_KEY}, "issuetype": {"name": "Story"},
                      "summary": f"{s['id']}: {s['summary']}", "labels": [label, s["mainflow"]],
                      "parent": {"key": keys[s["epic"]]},
                      "description": adf(s["story"] + "\n\nAcceptance criteria:\n\n"
                                         + "\n\n".join(s["ac"]))}
            if pts:
                fields[pts] = s["points"]
            key = j.call("POST", "/rest/api/3/issue", {"fields": fields})["key"]
        s["jira_live"] = key
        print(f'    "{s["id"]}": "{key}",')
    board = int(board_id)
    existing = {sp["name"]: sp["id"] for sp in
                j.call("GET", f"/rest/agile/1.0/board/{board}/sprint?maxResults=50").get("values", [])}
    for n, a, b in sprints:
        name = f"TK Sprint {n}"
        sid = existing.get(name) or j.call("POST", "/rest/agile/1.0/sprint", {
            "name": name, "originBoardId": board,
            "startDate": f"{a}T09:00:00.000+07:00", "endDate": f"{b}T18:00:00.000+07:00"})["id"]
        issues = [s["jira_live"] for s in by_sprint.get(n, [])]
        for i in range(0, len(issues), 50):
            j.call("POST", f"/rest/agile/1.0/sprint/{sid}/issue", {"issues": issues[i:i + 50]})
        print(f"{name}: {len(issues)} stories")
    print("done. Record the keys above in build_backlog.JIRA_KEYS, then start the sprint from the Backlog view.")
    return 0


def retire(j: Jira) -> int:
    labels = [f"backlog-E{i}" for i in range(1, 9)] + [f"backlog-US-{i:03d}" for i in range(1, 88)]
    for label in labels:
        key = j.find(label)
        if not key:
            continue
        j.call("PUT", f"/rest/api/3/issue/{key}", {"update": {"labels": [{"add": "retired-d033"}]}})
        done = [t for t in j.call("GET", f"/rest/api/3/issue/{key}/transitions").get("transitions", [])
                if t["to"]["statusCategory"]["key"] == "done"]
        if done:
            j.call("POST", f"/rest/api/3/issue/{key}/transitions", {"transition": {"id": done[0]["id"]}})
        print(f"{label} {key}: retired{'' if done else ' (no Done transition, label only)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
