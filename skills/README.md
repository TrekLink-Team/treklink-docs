# TrekLink Custom Skills

Project-specific agent skills that encode **this** project's workflow. They complement
[`prompt-orchestrator`](https://github.com/ruskicoder/system-prompts), which carries the generic
engineering ruleset, rather than replacing it.

**Install both. Every member, every machine.** Plain Markdown only: no binaries, no daemons,
nothing that touches system config.

---

## 1. Install

### Linux / macOS
```bash
cd treklink-docs/skills
bash install/install-all.sh          # every supported agent
bash install/install-claude.sh       # Claude Code only
```

### Windows (PowerShell)
```powershell
cd treklink-docs\skills
.\install\install-all.ps1
.\install\install-claude.ps1
```

Verify:
```bash
ls ~/.claude/skills | grep treklink
```

> Install `prompt-orchestrator` **first** if you haven't, these skills assume its ruleset is
> already loaded. See `_docs/01-conventions/11-ai-first-doctrine-and-toolchain.md` §3.1.

---

## 2. The skills

| Skill | Use when |
|---|---|
| **`/treklink-session`** | **Every session, at the start.** Drives the mandatory nine-step workflow: context ingestion → clarification gate → approval gate → implement → doc sync → wrap up. |
| **`/treklink-pr`** | Opening, reviewing, fixing, or merging a PR. `open` / `review <N>` / `fix <N>` / `merge <N>`. |
| **`/treklink-spec`** | A module needs `requirements.md` → `design.md` → `tasks.md` before any code exists. |

They trigger automatically on description match, or explicitly as `/name`.

---

## 3. Scaffold your personal garden

Every member needs an `ignore/{your_name}/` garden in each repo they work in, it is where session
files, scratch notes, and env templates live, and where an agent looks to resume your context.

```bash
# Linux / macOS
bash install/scaffold-garden.sh khoa ~/capstone/treklink-web
bash install/scaffold-garden.sh khoa ~/capstone/treklink-docs
```

```powershell
# Windows
.\install\scaffold-garden.ps1 -Name khoa -Repo C:\capstone\treklink-web
```

Idempotent, re-running never overwrites an existing garden.

**Recommended**: version it as its own **private** repo so you get history without dirtying the
project repo:
```bash
cd ignore/khoa && git init && git remote add origin git@github.com:you/your-private-garden.git
```

---

## 4. Editing a skill

Skill sources are `.claude/skills/{name}/SKILL.md` in this folder, tracked, reviewed, and part of
the SSOT like any other convention.

1. Branch: `docs/TK-nn-skill-change`
2. Edit the `SKILL.md`
3. Re-run the installer to pick it up locally
4. PR to `dev`, skills are team-wide, so they get reviewed like anything else

Keep them consistent with `_docs/01-conventions/`. **A skill that contradicts the conventions is a
bug in the skill**, not a variant workflow, the conventions are Tier 3 authority, these are an
execution aid.
