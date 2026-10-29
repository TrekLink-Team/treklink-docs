# Capstone project register (FA26SE159)

Every version uploaded to the school portal is kept here under its own name. Nothing is
overwritten: a new version gets new files, and the older ones stay.

| Version | Date | Trigger | Files |
|---|---|---|---|
| v1 | in the repository since 2026-09-07 (portal upload date not recorded here) | Original registration | `.deprecated/Phieu_FA26SE159.md`, `docx/Phieu_FA26SE159.docx` |
| v1.1 | 2026-10-15, portal upload 23:49, "Phieu dang ky cap nhat v1.1" | The 02/10 rescope and the 12/10 supervisor review | `Phieu_FA26SE159_v1.1_2026-10-15.md`, `docx/Phieu_FA26SE159_v1.1_2026-10-15.docx`, `docx/Phieu_FA26SE159_v1.1_2026-10-15_highlighted.docx`, `pdf/Phieu_FA26SE159_v1.1_2026-10-15.pdf`, `pdf/Phieu_FA26SE159_v1.1_2026-10-15_highlighted.pdf` |
| v2 (current) | 2026-10-29, portal upload 16:30, "Phieu dang ky cap nhat v2" | Review 2 | `Phieu_FA26SE159_v2_2026-10-29.md`, `docx/Phieu_FA26SE159_v2_2026-10-29.docx`, `docx/Phieu_FA26SE159_v2_2026-10-29_highlighted.docx`, `pdf/Phieu_FA26SE159_v2_2026-10-29.pdf`, `pdf/Phieu_FA26SE159_v2_2026-10-29_highlighted.pdf` |

**v2 is the current register.** The clean copies are what the portal holds; the `_highlighted`
copies show the changed text in yellow, for the supervisors.

`docx/Phieu_FA26SE159.docx` is the registered v1 form and also the style template every later
version is built from. Keep it where it is.

v1.1 was restored from commit `023cb90`, the last commit before the v2 edits. Its two PDFs were
converted from those `.docx` files with `soffice --headless --convert-to pdf`.

## Renamed file

Until 2026-10-29 the current form lived at `Phieu_FA26SE159_adjusted_2026-10.md`, with matching
`.docx` and `.pdf` names. On 2026-10-29 those files were renamed to the v2 names above. Older
entries in the decision register still cite the old path; read it as the v2 file.

## Build

From the `capstone/` workspace root:

```sh
scripts/srs/.venv/bin/python scripts/srs/build_form.py
```

It reads the v2 Markdown and writes both v2 `.docx` files into `docx/` and both PDFs into `pdf/`.
Earlier versions are frozen and are not rebuilt.
