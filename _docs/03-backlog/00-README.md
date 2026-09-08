# 03 — Backlog

Single source of truth for the epic/user-story backlog. **Don't hand-edit
`01-epics.md` or `02-user-stories.md` directly** — edit the data in
`build_backlog.py` and regenerate, so this folder and
`User_Story_Agile_TrekLink.xlsx` (repo root of the deliverable zip / your
project's chosen location for it) never drift apart.

```bash
cd 03-backlog
python3 build_backlog.py                       # writes 01-epics.md + 02-user-stories.md
python3 build_backlog.py /path/to/out.xlsx      # also (re)writes the xlsx at that path
```

Requires `openpyxl` (`pip install openpyxl`).

## Files

- `build_backlog.py` — the data (`TEAM`, `EPICS`, `STORIES`) and the generator. This is the thing to edit.
- `01-epics.md` — generated. 8 epics, rollup tables, story lists.
- `02-user-stories.md` — generated. All 87 stories with EARS-flavored acceptance criteria.

## Key decisions made this session (see the module docstring in `build_backlog.py` for the full rationale)

- Epic taxonomy: the 7 epics from `02-templates/05-user-story-template.md` + a new **E8 (Research & Experimental Evaluation)** for RQ1-RQ3/TP6.
- Granularity: fine — one story per discrete actor-action (~87 stories, 360 points), per the explicit call that coarse epics create development ambiguity.
- Sprints are pre-mapped from `00-project-context/02-roadmap-and-milestones.md`'s TP-to-week table; `Status` is `Ready` only for the 4 Sprint-1 stories, everything else is `Backlog` pending your own sprint-planning pass.
- Assignment is skill-matrix-driven (`01-project-charter.md`), not an even split — see the Workload Summary sheet in the xlsx for the per-person rationale and the flagged NestJS skill-gap risk in `00-project-context/03-decisions-and-risk-register.md`.
