# Capstone project register (FA26SE159): moved

Every version of the register now lives in the capstone repository, under
`capstone/Documents/submissions/register/`, one folder per version (`register-v1.0/` to
`register-v4.0/`). The index of versions, dates and upload status is
`capstone/Documents/submissions/README.md`. Rule: `_docs/01-conventions/15-graded-report-conventions.md`
section 5 (leader instruction of 2026-11-08).

| Former path in `topics/` | New path under `capstone/Documents/submissions/register/` |
|---|---|
| `docx/Phieu_FA26SE159.docx` (registered form, the template for every later version) | `register-v1.0/FA26SE159_Register-v1.0.docx` |
| `.deprecated/Phieu_FA26SE159.md` | `register-v1.0/FA26SE159_Register-v1.0.md` |
| `Attachments/*.png` (form logo and checkboxes) | `register-v1.0/media/` |
| `Phieu_FA26SE159_v1.1_2026-10-15.*` and `_highlighted` copies | `register-v1.1/` |
| `Phieu_FA26SE159_v2_2026-10-29.*` and `_highlighted` copies | `register-v2.0/` |
| `Phieu_FA26SE159_v3_2026-11-07.*` (branch `docs/register-v3-wording`) | `register-v3.0/` |
| `Phieu_FA26SE159_v4_2026-11-08.*` (branch `docs/register-v4`) | `register-v4.0/` |

No Markdown source is kept here. The register builder, `capstone/scripts/srs/build_form.py`,
reads the v4 source and the v1 form template from the capstone folders above.

The pre-registration drafts that sat in `topics/.deprecated/`
(`Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.md` and `.docx`, `Phieu_dang_ky_de_tai_TrekLink_FA26_draft.docx`)
were never submitted, so they were not moved. Read them from this repository's history, at the
parent of the commit that added this README.
