# TrekLink — Engineering Documentation Set

> **Capstone FA26SE159** · TrekLink Team · GitHub Org: [`github.com/TrekLink-Team`](https://github.com/TrekLink-Team)  
> **Supervisor:** Đặng Ngọc Minh Đức  
> **Team Members:** Đỗ Đăng Khoa (Leader), Trần Khải Hoàng, Lâm Phi Long, Nguyễn Bá Tân, Nguyễn Ngọc Long  

> [!NOTE]
> **Terminology Notice:** The terms **Pull Requests (PRs)** and **Merge Requests (MRs)** are used *concurrently* throughout this codebase and documentation. A mention of either terminology refers to the other respectively and follows the exact same Git review workflow.

---

## 1. Initialization & Document-as-Code

This repository is the **Single Source of Truth (SSOT)** for the TrekLink capstone project, structured as **Document as Code** and backed by **Obsidian** and **GitHub**:
- **Prerequisite:** Users must install **Obsidian** and configure **Git / GitHub** to participate in versioning this repository.
- **Git Conventions:** This documentation repository strictly adheres to Git conventions. **Never push directly to a remote production/main branch.** If a decision, requirement, or convention is not written here, it does not exist for grading, review, or AI-agent-assisted development purposes.
- **Personal Workspace:** Make any local changes or private working notes by creating your own dedicated folder within `ignore/[your_name]`.

To eliminate Git merge conflicts while maintaining a fully searchable wiki across the entire team, we use a **Single-Branch (`main`), Dedicated-Folder** architecture.

### 1.1 Repository Structure

* **`/_docs/`**: Finalized company processes, system architectures, engineering conventions, reusable templates, and official SOPs. **Read-only on `main`.** All modifications must go through a formal branch and Pull Request / Merge Request.
* **`/topics/`**: Project topics, thesis registration proposals, supervisor submission documents (`.docx`), and Markdown conversions (`Phieu_FA26SE159.md`, `Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.md`).
* **`/ignore/[your_name]/`**: Your personal digital garden, scratchpad, daily notes, ongoing project drafts, and individual tasks. **You have total write-privilege here.** This folder is git-ignored by the main repository.

---

### 2. Vault Golden Rules

1. **Write Freely in Your Folder:** You can create, edit, or destroy notes inside your own named folder at any time.
2. **Read-Only Outside Your Folder:** You are encouraged to read and search through other team members' folders. **Never edit a file inside another teammate's folder or `_docs` directly on the `main` branch.**
3. **Commit conventions**: You Must do the following flow when editing this repository:
   - `git fetch origin` and `git pull origin`. If there is unstaged changes or ongoing work OUTSIDE the /ignore folder, `git stash` it.
   - **Recommended**: *Git version* your folders in /ignore as a new, separate locally Git versioned repository. Push frequently your updates to ***THAT*** repo only. This ensures the main document repository does **NOT** get cluttered by Git Obsidian plugin **AND** your local edits.
     ```text
     treklink-docs:       unchanged (clean remote tracking)
     /ignore/[your-name]: git versioned separately (private repository)
     ```
   - Any other changes in this repository must follow this exact steps:
     - Branch out to a feature branch.
     - Implement & Commit your changes
     - Push origin to the feature branch
     - Create a PR to the parent branch of that feature branch (e.g. if you branch out your feature branch edits from dev branch, you must create a PR from /dev/your-feature branch to /dev branch)
     - Wait for approval.

---

## 3. Repo Scope & Obsidian Vault Compatibility

This is a **docs-only** repository — it holds no application code. It is designed to be directly usable as an **Obsidian vault** (simply open this root repository in Obsidian) while maintaining 100% native readability on GitHub. This constrains authoring choices across the vault:

- **Relative Standard Markdown Links:** Use standard Markdown links (`[text](_docs/folder/file.md)`) for all official documentation under `_docs/`. This guarantees links resolve correctly on both GitHub web UI and inside Obsidian without broken references.
- **Internal Wikilinks in Personal Folders:** Standard wiki-links (`[[Note Name]]` or `[[Folder/Note Name]]`) are supported and encouraged within your private digital garden (`/ignore/[your_name]/`).
- **Mermaid Diagrams:** Use native **Mermaid** blocks for architecture, sequence, and flow diagrams (rendered natively by both GitHub and Obsidian ≥0.9). PlantUML is avoided except where preserving legacy upstream templates.
- **Numbered Folder/File Prefixes:** Prefixes (`00-`, `01-`, `02-`) ensure identical, predictable sort orders across Obsidian's file tree and GitHub's repository browser.
- **Clean Markdown Standard:** Avoid Obsidian-only proprietary syntax (such as Dataview queries or custom plugin codeblocks) in `_docs/` so documents remain readable with zero plugins required.
- **Application Repo Drop-ins (`_docs/.github/`):** Files under `_docs/.github/` (PR/Issue templates, label taxonomies) exist to be copied directly into the roots of the actual application repositories (`treklink-gateway`, `treklink-backend`, `treklink-web`).

---

## 4. How This Doc Set Is Organized

| Folder / Path | Purpose | Read this when… |
|---|---|---|
| [`_docs/00-project-context/`](_docs/00-project-context/) | What we're building, why, the roadmap against capstone milestones, and open decisions | Onboarding, before Review 1/2/3 prep |
| [`_docs/01-conventions/`](_docs/01-conventions/) | How we work: session-based dev, spec-driven workflow, architecture, backend/frontend code rules, Git/GitHub flow, AI agent discipline | Before writing any code or spec |
| [`_docs/02-templates/`](_docs/02-templates/) | Blank, reusable templates: requirements (EARS), design, tasks, API endpoint spec, user story backlog | Starting a new module/feature/spec |
| [`_docs/.github/`](_docs/.github/) | Drop-in GitHub repo config: PR templates, Issue templates, label taxonomy | Copy directly into the actual code repo's root |
| [`topics/`](topics/) | Capstone registration documents, supervisor review forms, and foundational project background | Reviewing project scope and academic deliverables |
| [`ignore/`](ignore/) | Local team-member gardens and uncommitted working drafts | Conducting personal research and scratch work |

---

## 5. Quick Start for a New Session (Human or AI Agent)

1. Read [`_docs/00-project-context/01-project-charter.md`](_docs/00-project-context/01-project-charter.md) once, fully.
2. Check [`_docs/00-project-context/02-roadmap-and-milestones.md`](_docs/00-project-context/02-roadmap-and-milestones.md) to know which capstone milestone/sprint is active **today**.
3. Check [`_docs/00-project-context/03-decisions-and-risk-register.md`](_docs/00-project-context/03-decisions-and-risk-register.md) for anything marked `OPEN` that blocks your task.
4. Follow [`_docs/01-conventions/02-spec-driven-development-workflow.md`](_docs/01-conventions/02-spec-driven-development-workflow.md): write/read `requirements.md` → `design.md` → `tasks.md` for the module under `specs/{module}/` in the code repo **before** touching code.
5. Branch, code, and open a PR per [`_docs/01-conventions/07-github-workflow-git-conventions.md`](_docs/01-conventions/07-github-workflow-git-conventions.md).
6. **For AI Coding Agents (Claude Code, Cursor, Copilot, Antigravity):** Load [`_docs/01-conventions/08-ai-agent-steering-and-discipline.md`](_docs/01-conventions/08-ai-agent-steering-and-discipline.md) into your system/rules file.

---

## 6. Document Authority Hierarchy

When two documents conflict, the higher tier wins until an Architecture Decision Record (ADR) in [`_docs/00-project-context/03-decisions-and-risk-register.md`](_docs/00-project-context/03-decisions-and-risk-register.md) formally supersedes it:

1. **Tier 1 — Project Charter & Capstone Register** ([`_docs/00-project-context/01-project-charter.md`](_docs/00-project-context/01-project-charter.md), and the two submitted `Phieu_*.docx` register forms it reconciles)
2. **Tier 2 — Module specs** (`specs/{module}/requirements.md`, `design.md` in the code repo)
3. **Tier 3 — Conventions** ([`_docs/01-conventions/*`](_docs/01-conventions/))
4. **Tier 4 — Templates** ([`_docs/02-templates/*`](_docs/02-templates/)) — starting points only, not binding once filled in
5. **Tier 5 — Source code & tests**

---

## 7. Source Documents This Set Reconciles

- [`Phieu_FA26SE159.docx`](topics/docx/Phieu_FA26SE159.docx) (Markdown: [`topics/Phieu_FA26SE159.md`](topics/Phieu_FA26SE159.md)) — The individually-submitted, detailed capstone register (formal RQs, NFRs, experiment protocol, TP1–TP6 task packages). Treated as the **primary/authoritative** spec.
- [`Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.docx`](topics/docx/Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.docx) (Markdown: [`topics/Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.md`](topics/Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.md)) — The team's earlier draft register (same project, 5-module framing, M1–M5). Used as a cross-check; where it differs from FA26SE159, FA26SE159 wins (Decision D-000).
- `Git_Lab_Guide.pdf` — The school's GitLab/PR convention (v1.0, Aug 2025). Re-expressed for GitHub in [`_docs/01-conventions/07-github-workflow-git-conventions.md`](_docs/01-conventions/07-github-workflow-git-conventions.md), preserving the same core philosophy.
- `API_Design_Template.md` — The team's API documentation format. Adopted as [`_docs/02-templates/04-api-endpoint-template.md`](_docs/02-templates/04-api-endpoint-template.md); its response envelope (`result` / `isSuccess` / `statusCode` / `message`) is the **binding contract** for all TrekLink backend endpoints.
- `User_Story_Agile.xlsx` — The team's Jira-style backlog format. Extended as a blank template in [`_docs/02-templates/User_Story_Backlog_TEMPLATE.xlsx`](_docs/02-templates/User_Story_Backlog_TEMPLATE.xlsx).
- `dev-flow.zip` — A session-driven + spec-driven engineering framework ported to the TrekLink stack (NestJS/TypeScript backend, React frontend, Node.js gateway, PostgreSQL) in [`_docs/01-conventions/`](_docs/01-conventions/).

---

## 8. 🔗 Linking, File & Asset Conventions

To ensure links never break when pushed to a remote server, viewed on GitHub, or compiled via static web-viewers:
* **Internal Links:** Use relative Markdown links (`[Label](_docs/path/file.md)`) for shared docs. Within personal ignore folders, standard wiki-links (`[[Note]]`) may be used.
* **File Naming:** Use kebab-case or Title-Case with hyphens for filenames (e.g., `project-x-spec.md` or `Project-X-Spec.md`). **Strictly avoid spaces or special characters (`?, !, @`)** in filenames, as they break URL paths if this vault is ever deployed as a website.
* **Attachments:** Drop personal images, PDFs, or diagrams directly into your personal `/ignore/[your_name]/_assets/` folder. Global project attachments belong in [`topics/Attachments/`](topics/Attachments/). Do not clutter the root directory.

---

## 9. 🌿 The Pull Request (PR) Workflow

When does a note leave your personal folder and become official documentation?

```text
[Your /ignore Folder] ──> Create Feature Branch ──> Edit _docs/ ──> Push Branch ──> Open PR ──> Peer Review ──> Squash & Merge to main
```

1. **The Draft Phase:** Keep the working document inside your personal folder (e.g., `/ignore/[your_name]/onboarding-guide-v2.md`).
2. **The Proposal:** When ready to publish to the team, update your local base branch and create a feature branch:
   ```bash
   git checkout develop && git pull origin develop
   git checkout -b features/Doc_OnboardingUpdate
   ```
3. **The Move / Edit:** Copy or create the file in its designated location inside `/_docs/` on your branch.
4. **The Review:** Push your branch and open a Pull Request (or Merge Request):
   ```bash
   git push -u origin features/Doc_OnboardingUpdate
   gh pr create --base develop --title "[Docs] Add onboarding guide v2"
   ```
   Tag relevant team members for review. Once approved, **Squash and Merge** the PR into the parent branch.

---

## 10. ⚙️ Metadata & Frontmatter Standard

Every note intended for team consumption must begin with a standardized frontmatter YAML block at the very top of the file:

```yaml
---
status: draft # Options: draft, under-review, approved, deprecated
owner: [Your Name]
last_updated: YYYY-MM-DD
tags:
  - project/alpha
  - docs/sop
---
```

---

## 11. 🚀 Getting Started (New Team Members)

1. **Clone this repository** locally:
   ```bash
   git clone https://github.com/TrekLink-Team/treklink-docs.git
   cd treklink-docs
   ```
2. **Open in Obsidian**: Click **"Open folder as vault"**, and select this repository's root folder.
3. **Recommended Community Plugins**:
   - **Obsidian Git**: Automated backup/sync (configured for your personal folder).
   - **Importer**: For importing external docs.
   - **Docxer**: For reading `.docx` files natively within Obsidian.
4. **Create your personal folder**: Add your workspace folder under `/ignore/[your_name]`.
5. **(Recommended) Git Version Your Personal Folder**:
   ```bash
   cd ignore/[your_name]
   git init
   git remote add origin git@github.com:[your-username]/[your-private-garden].git
   ```
   Now you can push and pull freely inside your own garden without dirtying the root `treklink-docs` repository!
