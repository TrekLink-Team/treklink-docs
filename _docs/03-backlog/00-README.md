# 03: Backlog

Single source of truth for the epic and user-story backlog. **Do not hand-edit `01-epics.md` or
`02-user-stories.md`.** Edit `build_backlog.py`, or the SRS data it reads, and regenerate, so this
folder, `User_Story_Agile_TrekLink.xlsx` and Jira never drift apart. Leader only.

```bash
cd 03-backlog
python3 build_backlog.py                       # 01-epics.md, 02-user-stories.md, the xlsx
python3 build_backlog.py /path/to/out.xlsx      # the xlsx somewhere else
python3 jira_sync.py                            # dry run of the Jira plan
```

Requires `openpyxl` and the SRS data `capstone/scripts/srs/srs_data.py`. Outside `capstone/`, set
`TREKLINK_SRS` to the folder holding `srs_data.py`.

## Files

- `build_backlog.py`, the generator: epics, lanes, priorities and delivery stories. Use cases,
  specifications and FRs come from `srs_data.py`.
- `01-epics.md`, generated. 10 epics with their stories.
- `02-user-stories.md`, generated. 69 stories with acceptance criteria.
- `jira_sync.py`, creates the epics, stories and roadmap sprints in Jira, and retires the
  pre-D-033 cards (`--retire`).

## Rewrite of 2026-10-18

- One story per SRS use case (`US-UCnn`), plus delivery stories (`US-Xnn`); the acceptance
  criteria are the FRs that cite the use case. The generator stops if an FR has no story.
- `baseline` marks the use cases that deliver a use case of the week 3 Report 3 (`srs_data.W3_MAP`),
  for the SEP490 75% rule (D-048 and its risk row).
- Owners follow the lanes of roadmap section 5.1; sprints follow roadmap section 4.2.
- The pre-D-033 backlog (8 epics, 87 stories on the booking scope) is in git history.
