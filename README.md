# TrekLink — Engineering Documentation Set

> **Capstone FA26SE159** · TrekLink Team · GitHub Org: [`github.com/TrekLink-Team`](https://github.com/TrekLink-Team)
> **Supervisor:** Đặng Ngọc Minh Đức
> **Team Members:** Đỗ Đăng Khoa (Leader), Trần Khải Hoàng, Lâm Phi Long, Nguyễn Bá Tân, Nguyễn Ngọc Long

> [!NOTE]
> **Terminology Notice:** The terms **Pull Requests (PRs)** and **Merge Requests (MRs)** are used *concurrently* throughout this codebase and documentation. A mention of either terminology refers to the other respectively and follows the exact same Git review workflow.

This repository (`treklink-docs`) is the **Single Source of Truth (SSOT)** for the TrekLink capstone: what we're building, why, how we work, and what's still undecided. It holds no application code. Two sibling repositories hold the actual product — see §1. **If it isn't written here, it doesn't exist for grading, review, or AI-agent-assisted development.**

---

## 0. Read This First (2-Minute Orientation)

New to the team, or starting a new session? Do these five things, in order, before touching anything:

1. **Set up your machine** — §2 below, pick your OS (Linux / macOS / Windows).
2. **Clone all three repos as siblings** — §1 below. Everything downstream (specs, AI-agent context, cross-repo links) assumes this layout.
3. **Read the charter once, fully** — [`_docs/00-project-context/01-project-charter.md`](_docs/00-project-context/01-project-charter.md). Ten minutes, no skimming.
4. **Check what's open** — [`_docs/00-project-context/03-decisions-and-risk-register.md`](_docs/00-project-context/03-decisions-and-risk-register.md). Anything marked `OPEN` may block the task you're about to start.
5. **Before writing any code**, follow the spec-driven workflow — [`_docs/01-conventions/02-spec-driven-development-workflow.md`](_docs/01-conventions/02-spec-driven-development-workflow.md). Requirements → design → tasks, in that order, in `treklink-web`, *before* implementation.

Everything else in this README is reference material for when one of those five steps raises a question.

---

## 1. The Capstone Workspace — 3 Repos, 1 Parent Folder

TrekLink spans **three** GitHub repositories under `TrekLink-Team`. They are meant to be cloned as **siblings inside one parent folder** — this is what lets both humans and AI coding agents (Claude Code, Cursor, Copilot, etc.) open one root and see the docs, the inherited firmware, and the active application code at the same time, instead of guessing at cross-repo references.

```text
capstone/                          ← parent folder — open THIS in your editor/AI agent, not any repo alone
├── treklink-docs/                 ← THIS repo — SSOT, conventions, templates, decisions (Obsidian vault + GitHub)
├── treklink-firmware/             ← Inherited SU26 LoRa mesh firmware (ESP32/ESP32-S3, forked from Meshtastic)
│                                     EDITABLE (D-008) — targeted fixes OK, reflashing OK; redesign out of scope.
└── treklink-web/                  ← THIS TERM'S ACTIVE deliverable: the NestJS/React/gateway application
    ├── gateway/                    #   Gateway Bridge (Node.js/TypeScript) — LoRa-serial → MQTT → cloud
    ├── backend/                    #   NestJS backend (auth, devices, rentals, incidents, billing, gateway-sync)
    ├── frontend/                   #   React frontend (Admin/Staff/Guide/Customer views)
    └── specs/{module}/             #   requirements.md → design.md → tasks.md per module (see §7)
```

| Repo | Status | Purpose |
|---|---|---|
| [`treklink-docs`](https://github.com/TrekLink-Team/treklink-docs) | Active — docs only | This repo. SSOT for scope, conventions, templates, decisions. |
| [`treklink-firmware`](https://github.com/TrekLink-Team/treklink-firmware) | **Editable — see D-008** (was: frozen/read-only) | SU26 LoRa mesh firmware. Targeted fixes are permitted and the team can reflash; firmware *redesign* stays out of scope per charter §2. Before designing against it, read [`04-firmware-ground-truth.md`](_docs/00-project-context/04-firmware-ground-truth.md). |
| [`treklink-web`](https://github.com/TrekLink-Team/treklink-web) | Active — this term's build | Gateway Bridge + NestJS backend + React frontend, as workspace packages in one repo (see Decision D-004). |

> [!IMPORTANT]
> This is a deliberate simplification of the 4-repo plan originally sketched in early conventions drafts (separate `treklink-gateway` / `treklink-backend` repos). With a 5-person team and a 13-week term, one active app repo with three workspace packages cuts cross-cutting-change overhead (shared types between gateway/backend, one CI pipeline, one `npm install`) at the cost of slightly coarser branch protection. The reasoning and the option we didn't take are logged as **Decision D-004** in [`03-decisions-and-risk-register.md`](_docs/00-project-context/03-decisions-and-risk-register.md) — read it if you're unsure why a file lives where it does.

### 1.1 Clone all three

```bash
mkdir capstone && cd capstone
git clone https://github.com/TrekLink-Team/treklink-docs.git
git clone https://github.com/TrekLink-Team/treklink-firmware.git
git clone https://github.com/TrekLink-Team/treklink-web.git
```

### 1.2 Open all three at once (so an AI agent can cross-reference them)

- **Claude Code / Cursor / any agent that reads a working directory**: open the **`capstone/` parent folder** as the workspace root, not `treklink-docs/` alone. The agent can then read a convention in `treklink-docs/_docs/`, a firmware message struct in `treklink-firmware/`, and the code it's editing in `treklink-web/` in the same context window.
- **VS Code multi-root workspace**: create `capstone/treklink.code-workspace`:
  ```json
  {
    "folders": [
      { "path": "treklink-docs" },
      { "path": "treklink-firmware" },
      { "path": "treklink-web" }
    ]
  }
  ```
  Open that file with **File → Open Workspace from File**. This is git-ignored by design — each teammate keeps their own copy locally (or commit it to `treklink-docs/ignore/[your_name]/` if you want to share yours).
- **Point your agent's rules file at the conventions**: in `treklink-web`, create `AGENTS.md` / `CLAUDE.md` / `.cursorrules` that links `../treklink-docs/_docs/01-conventions/08-ai-agent-steering-and-discipline.md` and `../treklink-docs/_docs/01-conventions/07-github-workflow-git-conventions.md` (relative path works once the sibling layout above is in place).

---

## 2. Prerequisites & Platform Setup (Linux / macOS / Windows)

This documentation repo was authored on **Linux**. Most of the team runs **Windows**; this section is written so a Windows or macOS teammate ends up with an equivalent, working setup — commands are given for all three.

### 2.1 Tool checklist

| Tool                                                                              | Why you need it                                                                                                                   | Used by                    |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| **Git**                                                                           | Version control for all 3 repos                                                                                                   | Everyone                   |
| **GitHub CLI (`gh`)**                                                             | `gh pr create`, `gh auth login` — used throughout §9 and `_docs/01-conventions/07-github-workflow-git-conventions.md`             | Everyone                   |
| **Node.js (Active LTS, currently 22.x) + npm**                                    | Gateway/backend/frontend all run on Node                                                                                          | `treklink-web`             |
| **Docker Desktop / Docker Engine + Compose**                                      | PostgreSQL, MQTT broker (Mosquitto), local dev stack                                                                              | `treklink-web`             |
| **Obsidian**                                                                      | Renders and edits this vault with graph view, backlinks, etc.                                                                     | `treklink-docs`            |
| **A code editor with an AI agent** (Claude Code, Cursor, VS Code + Copilot, etc.) | Spec-driven workflow assumes one                                                                                                  | `treklink-web`             |
| **System Prompts**                                                                | [Install here](https://github.com/ruskicoder/system-prompts/tree/master/prompt-orchestrator). AI agents must follow this ruleset. | Everyone                   |
| **PlatformIO (optional)**                                                         | For inspecting, building, or flashing `treklink-firmware`. Needed by whoever takes the D-008 firmware fixes; optional for everyone else | `treklink-firmware` |

### 2.2 Linux (Ubuntu/Debian shown; swap `apt` for `dnf`/`pacman` as needed)

```bash
# Git + build basics
sudo apt update && sudo apt install -y git build-essential

# GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update && sudo apt install -y gh
gh auth login

# Node via nvm (lets everyone pin the exact same version via .nvmrc)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
# restart your shell, then:
nvm install --lts && nvm use --lts

# Docker
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER   # log out/in after this

# Obsidian (AppImage is the simplest cross-distro route; flatpak also works)
# Download the AppImage from https://obsidian.md, chmod +x it, run it directly.
```

### 2.3 macOS

```bash
# Install Homebrew first if you don't have it: https://brew.sh
brew install git gh nvm docker docker-compose
brew install --cask obsidian

# nvm needs a shell hook — brew's Caveats output tells you the exact lines to add
# to ~/.zshrc (or ~/.bash_profile). Then:
nvm install --lts && nvm use --lts

gh auth login
```

> macOS setup is otherwise **the same shape as Linux** (same shell, same package-manager-driven install, same `nvm`/`gh` commands) — if you're comfortable on one, the other needs almost no relearning. The one asymmetry to know about: **the team has no Mac hardware and no Xcode**, which matters if `treklink-firmware`'s companion-app question ever needs an iOS build — see §10.

### 2.4 Windows

Two supported routes. **WSL2 is strongly recommended** — it makes your machine behave like the Linux environment this repo (and most of the team's tooling advice) was written against, so `npm` scripts, Docker volumes, and shell snippets in `_docs/` work unmodified.

**Route A — WSL2 (recommended):**
```powershell
# In an elevated PowerShell:
wsl --install -d Ubuntu
# Reboot if prompted, create your Ubuntu user, then open the Ubuntu terminal
# and follow the §2.2 Linux instructions verbatim inside it.
```
Install **Docker Desktop for Windows** separately (from docker.com) with the "Use WSL 2 based engine" option enabled in Settings → General — this shares the Docker daemon between Windows and your WSL2 Ubuntu shell, so `docker compose up` works from inside WSL. Install **Obsidian** as a normal Windows app, but point it at the vault via the WSL path (`\\wsl$\Ubuntu\home\<you>\capstone\treklink-docs`) or, simpler, keep the `treklink-docs` clone on the Windows filesystem instead if Obsidian performance over `\\wsl$` bothers you.

**Route B — Native Windows (no WSL):**
```powershell
winget install --id Git.Git
winget install --id GitHub.cli
winget install --id CoreyButler.NVMforWindows   # nvm-windows — a different tool from nvm, same idea
winget install --id Docker.DockerDesktop
winget install --id Obsidian.Obsidian

# after installing nvm-windows, in a NEW terminal:
nvm install lts
nvm use lts

gh auth login
```
(No `winget`? Use [Chocolatey](https://chocolatey.org) or [Scoop](https://scoop.sh) with the same package names, or download installers directly from each project's site.)

**Windows-specific gotchas either route should watch for:**
- **Line endings**: set `git config --global core.autocrlf true` (native Windows) or `input` (inside WSL) once, globally, before your first clone — otherwise every file shows as "changed" in `git status` from CRLF/LF churn.
- **Path length**: clone close to a drive root (`C:\dev\capstone\...`) on native Windows; the default `git config core.longpaths true` helps but doesn't fully fix deeply-nested `node_modules`.
- **Native modules** (the Gateway Bridge's SQLite dependency compiles native bindings): this is the single biggest reason Route A (WSL2) is recommended — native `npm install` on Windows occasionally needs Visual Studio Build Tools that WSL2's Linux userland doesn't.
- **Shell scripts in this repo's docs** (the `bash` blocks throughout `_docs/`) assume a POSIX shell — run them from WSL2, Git Bash, or translate manually on native PowerShell.

### 2.5 Verify your setup (any OS)

```bash
git --version
gh --version && gh auth status
node --version   # should print v22.x or newer
npm --version
docker --version && docker compose version
```

---

## 3. Document-as-Code & the SSOT Principle

This repository is structured as **Document as Code**, backed by **Obsidian** and **GitHub**:
- **Git Conventions:** This documentation repository strictly adheres to Git conventions. **Never push directly to a remote production/main branch.** If a decision, requirement, or convention is not written here, it does not exist for grading, review, or AI-agent-assisted development purposes.
- **Personal Workspace:** Make any local changes or private working notes by creating your own dedicated folder within `ignore/[your_name]`.

To eliminate Git merge conflicts while maintaining a fully searchable wiki across the entire team, we use a **Single-Branch (`main`), Dedicated-Folder** architecture.

### 3.1 Repository Structure (inside `treklink-docs` itself)

* **`/_docs/`**: Finalized company processes, system architectures, engineering conventions, reusable templates, and official SOPs. **Read-only on `main`.** All modifications must go through a formal branch and Pull Request / Merge Request.
* **`/topics/`**: Project topics, thesis registration proposals, supervisor submission documents (`.docx`), and Markdown conversions (`Phieu_FA26SE159.md`, `Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.md`).
* **`/ignore/[your_name]/`**: Your personal digital garden, scratchpad, daily notes, ongoing project drafts, and individual tasks. **You have total write-privilege here.** This folder is git-ignored by the main repository.

---

## 4. Vault Golden Rules

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

## 5. Repo Scope & Obsidian Vault Compatibility

This is a **docs-only** repository — it holds no application code (that's `treklink-web`) and no firmware (that's `treklink-firmware`). It is designed to be directly usable as an **Obsidian vault** (simply open this root repository in Obsidian) while maintaining 100% native readability on GitHub. This constrains authoring choices across the vault:

- **Relative Standard Markdown Links:** Use standard Markdown links (`[text](_docs/folder/file.md)`) for all official documentation under `_docs/`. This guarantees links resolve correctly on both GitHub web UI and inside Obsidian without broken references.
- **Internal Wikilinks in Personal Folders:** Standard wiki-links (`[[Note Name]]` or `[[Folder/Note Name]]`) are supported and encouraged within your private digital garden (`/ignore/[your_name]/`).
- **Mermaid Diagrams:** Use native **Mermaid** blocks for architecture, sequence, and flow diagrams (rendered natively by both GitHub and Obsidian ≥0.9). PlantUML is avoided except where preserving legacy upstream templates.
- **Numbered Folder/File Prefixes:** Prefixes (`00-`, `01-`, `02-`) ensure identical, predictable sort orders across Obsidian's file tree and GitHub's repository browser.
- **Clean Markdown Standard:** Avoid Obsidian-only proprietary syntax (such as Dataview queries or custom plugin codeblocks) in `_docs/` so documents remain readable with zero plugins required.
- **Application Repo Drop-ins (`_docs/.github/`):** Files under `_docs/.github/` (PR/Issue templates, label taxonomies) exist to be copied directly into the root of `treklink-web` (and `treklink-firmware` if it ever needs its own issue tracker again).

---

## 6. How This Doc Set Is Organized

| Folder / Path | Purpose | Read this when… |
|---|---|---|
| [`_docs/00-project-context/`](_docs/00-project-context/) | What we're building, why, the roadmap against capstone milestones, and open decisions | Onboarding, before Review 1/2/3 prep |
| [`_docs/01-conventions/`](_docs/01-conventions/) | How we work: session-based dev, spec-driven workflow, architecture, backend/frontend code rules, Git/GitHub flow, AI agent discipline | Before writing any code or spec |
| [`_docs/02-templates/`](_docs/02-templates/) | Blank, reusable templates: requirements (EARS), design, tasks, API endpoint spec, user story backlog | Starting a new module/feature/spec |
| [`_docs/.github/`](_docs/.github/) | Drop-in GitHub repo config: PR templates, Issue templates, label taxonomy | Copy directly into `treklink-web`'s root |
| [`topics/`](topics/) | Capstone registration documents, supervisor review forms, and foundational project background | Reviewing project scope and academic deliverables |
| [`ignore/`](ignore/) | Local team-member gardens and uncommitted working drafts | Conducting personal research and scratch work |

---

## 7. Quick Start for a New Session (Human or AI Agent)

1. Read [`_docs/00-project-context/01-project-charter.md`](_docs/00-project-context/01-project-charter.md) once, fully.
2. Check [`_docs/00-project-context/02-roadmap-and-milestones.md`](_docs/00-project-context/02-roadmap-and-milestones.md) to know which capstone milestone/sprint is active **today**.
3. Check [`_docs/00-project-context/03-decisions-and-risk-register.md`](_docs/00-project-context/03-decisions-and-risk-register.md) for anything marked `OPEN` that blocks your task.
4. Follow [`_docs/01-conventions/02-spec-driven-development-workflow.md`](_docs/01-conventions/02-spec-driven-development-workflow.md): write/read `requirements.md` → `design.md` → `tasks.md` for the module under `treklink-web/specs/{module}/` **before** touching code.
5. Branch, code, and open a PR per [`_docs/01-conventions/07-github-workflow-git-conventions.md`](_docs/01-conventions/07-github-workflow-git-conventions.md).
6. **For AI Coding Agents (Claude Code, Cursor, Copilot, Antigravity):** Load [`_docs/01-conventions/08-ai-agent-steering-and-discipline.md`](_docs/01-conventions/08-ai-agent-steering-and-discipline.md) into your system/rules file — and open the `capstone/` parent folder (§1.2), not this repo alone.

---

## 8. Document Authority Hierarchy

When two documents conflict, the higher tier wins until an Architecture Decision Record (ADR) in [`_docs/00-project-context/03-decisions-and-risk-register.md`](_docs/00-project-context/03-decisions-and-risk-register.md) formally supersedes it:

1. **Tier 1 — Project Charter & Capstone Register** ([`_docs/00-project-context/01-project-charter.md`](_docs/00-project-context/01-project-charter.md), and the two submitted `Phieu_*.docx` register forms it reconciles)
2. **Tier 2 — Module specs** (`treklink-web/specs/{module}/requirements.md`, `design.md`)
3. **Tier 3 — Conventions** ([`_docs/01-conventions/*`](_docs/01-conventions/))
4. **Tier 4 — Templates** ([`_docs/02-templates/*`](_docs/02-templates/)) — starting points only, not binding once filled in
5. **Tier 5 — Source code & tests** (in `treklink-web`)

---

## 9. Source Documents This Set Reconciles

- [`Phieu_FA26SE159.docx`](topics/docx/Phieu_FA26SE159.docx) (Markdown: [`topics/Phieu_FA26SE159.md`](topics/Phieu_FA26SE159.md)) — The individually-submitted, detailed capstone register (formal RQs, NFRs, experiment protocol, TP1–TP6 task packages). Treated as the **primary/authoritative** spec.
- [`Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.docx`](topics/docx/Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.docx) (Markdown: [`topics/Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.md`](topics/Phieu_dang_ky_de_tai_TrekLink_FA26_FINAL.md)) — The team's earlier draft register (same project, 5-module framing, M1–M5). Used as a cross-check; where it differs from FA26SE159, FA26SE159 wins (Decision D-000).
- `Git_Lab_Guide.pdf` — The school's GitLab/PR convention (v1.0, Aug 2025). Re-expressed for GitHub in [`_docs/01-conventions/07-github-workflow-git-conventions.md`](_docs/01-conventions/07-github-workflow-git-conventions.md), preserving the same core philosophy.
- `API_Design_Template.md` — The team's API documentation format. Adopted as [`_docs/02-templates/04-api-endpoint-template.md`](_docs/02-templates/04-api-endpoint-template.md); its response envelope (`result` / `isSuccess` / `statusCode` / `message`) is the **binding contract** for all TrekLink backend endpoints.
- `User_Story_Agile.xlsx` — The team's Jira-style backlog format. Extended as a blank template in [`_docs/02-templates/User_Story_Backlog_TEMPLATE.xlsx`](_docs/02-templates/User_Story_Backlog_TEMPLATE.xlsx).
- `dev-flow.zip` — A session-driven + spec-driven engineering framework ported to the TrekLink stack (NestJS/TypeScript backend, React frontend, Node.js gateway, PostgreSQL) in [`_docs/01-conventions/`](_docs/01-conventions/).

---

## 10. ⚠️ Open Technical Risk: Field Device → Cloud Bridging

The register describes the Gateway Bridge as dedicated **TrekLink hardware with its own Wi-Fi/cellular uplink**. In practice, the more readily available path off the mesh is the **Guide's or Customer's phone** — it's already carried into the field, already paired to a node over Bluetooth, and already has internet, via the stock, open-source **Meshtastic companion app** (Android + iOS).

Two ways to use that path were identified, with very different cost:

1. **Preferred — no app changes.** Point our own MQTT broker at a TrekLink node's *built-in* Meshtastic MQTT-uplink module (it's already in the inherited firmware) and let a Wi-Fi/cellular-connected node publish directly. This matches what the register already describes and needs zero mobile work.
2. **Fallback — forking the mobile app.** Modify the Meshtastic Android/iOS apps themselves for custom bridging behavior. **This is high-risk for this team specifically: the iOS build requires Xcode on macOS, and nobody on the team has a Mac.** An Android-only fork would also split Guide/Customer device behavior by platform.

**Default plan: Option 1.** Nothing in the current TP2–TP5 task packages assumes mobile-app forking. This is tracked as **Decision D-005** in [`_docs/00-project-context/03-decisions-and-risk-register.md`](_docs/00-project-context/03-decisions-and-risk-register.md) — read it before proposing any change to how phones or the mobile app factor into the Gateway architecture, and before TP1's Gateway PoC is signed off.

---

## 11. 🔗 Linking, File & Asset Conventions

To ensure links never break when pushed to a remote server, viewed on GitHub, or compiled via static web-viewers:
* **Internal Links:** Use relative Markdown links (`[Label](_docs/path/file.md)`) for shared docs. Within personal ignore folders, standard wiki-links (`[[Note]]`) may be used.
* **File Naming:** Use kebab-case or Title-Case with hyphens for filenames (e.g., `project-x-spec.md` or `Project-X-Spec.md`). **Strictly avoid spaces or special characters (`?, !, @`)** in filenames, as they break URL paths if this vault is ever deployed as a website.
* **Attachments:** Drop personal images, PDFs, or diagrams directly into your personal `/ignore/[your_name]/_assets/` folder. Global project attachments belong in [`topics/Attachments/`](topics/Attachments/). Do not clutter the root directory.

---

## 12. 🌿 The Pull Request (PR) Workflow (for this docs repo)

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

## 13. ⚙️ Metadata & Frontmatter Standard

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

## 14. 🚀 Getting Started Checklist (New Team Members)

1. **Set up your machine** — §2 (Linux/macOS/Windows), verify with §2.5.
2. **Clone all three repos as siblings** — §1.1.
3. **Open in Obsidian**: inside `treklink-docs`, click **"Open folder as vault"** and select this repo's root.
4. **Recommended Community Plugins**:
   - **Obsidian Git**: Automated backup/sync (configured for your personal folder).
   - **Importer**: For importing external docs.
   - **Docxer**: For reading `.docx` files natively within Obsidian.
5. **Create your personal folder**: Add your workspace folder under `/ignore/[your_name]`.
6. **(Recommended) Git Version Your Personal Folder**:
   ```bash
   cd ignore/[your_name]
   git init
   git remote add origin git@github.com:[your-username]/[your-private-garden].git
   ```
   Now you can push and pull freely inside your own garden without dirtying the root `treklink-docs` repository!
7. **Set up `treklink-web`**: once cloned (§1.1), that repo's own README covers `npm install`, `.env`, and `docker compose up` for the local Postgres/MQTT stack — this repo only covers process and conventions, not runtime setup.
8. **Point your AI agent at both** — §1.2.
