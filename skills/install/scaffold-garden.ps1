#Requires -Version 5.1
param(
    [Parameter(Mandatory = $true)][string]$Name,
    [string]$Repo = (Get-Location).Path
)
$ErrorActionPreference = 'Stop'

# Scaffold a personal SSOT garden inside a repo's gitignored ignore/ folder.
# Convention: _docs/01-conventions/09-doc-driven-scaffold-and-ssot-conventions.md

if (-not (Test-Path (Join-Path $Repo '.git'))) {
    Write-Error "!! Not a git repository: $Repo"
}

$Root = Join-Path $Repo "ignore\$Name"
if (Test-Path $Root) {
    Write-Host "==> $Root already exists - leaving it alone (nothing overwritten)."
    exit 0
}

Write-Host "==> Scaffolding personal garden: $Root"
'docs\sessions', 'docs\diagrams', 'docs\flows', 'scripts', 'envs' | ForEach-Object {
    New-Item -ItemType Directory -Force -Path (Join-Path $Root $_) | Out-Null
}
'docs\diagrams\.gitkeep', 'docs\flows\.gitkeep' | ForEach-Object {
    New-Item -ItemType File -Force -Path (Join-Path $Root $_) | Out-Null
}

@"
# $Name - Personal Garden

Gitignored. Total write privilege. Nothing here is authoritative.

- ``current-progress.md`` - rolling POINTER to the latest session file (not a write target)
- ``sessions/`` - one file per session instance: ``YYYY-MM-DD-HHMM-topic.md``
- ``diagrams/``, ``flows/`` - Mermaid ``.mmd``
- ``../scripts/`` - local tooling and scratch scripts
- ``../envs/`` - env templates. **Never committed anywhere.**

Authoritative docs live in ``treklink-docs/_docs/``. If this and a tracked doc disagree,
the tracked one wins.
"@ | Set-Content -Path (Join-Path $Root 'docs\00-index.md') -Encoding UTF8

@"
# $Name - Current Progress (pointer only)

> This file is a **pointer**, not a write target. High-frequency notes go in a per-session
> file under ``sessions/`` - one shared rolling file is what caused lost findings under
> concurrent sessions.

**Latest**: _(none yet)_

**Active branches**: _(none)_
"@ | Set-Content -Path (Join-Path $Root 'docs\current-progress.md') -Encoding UTF8

"# $Name - Local scripts`n`nScratch tooling only. Never application code." |
    Set-Content -Path (Join-Path $Root 'scripts\README.md') -Encoding UTF8

"# $Name - Environment templates`n`nLocal .env files and connection strings (including Neon, D-010).`n`n**Never commit these. Not here, not anywhere.**" |
    Set-Content -Path (Join-Path $Root 'envs\README.md') -Encoding UTF8

Write-Host "==> Done."
Get-ChildItem -Path $Root -Recurse -File | ForEach-Object { Write-Host "    $($_.FullName.Replace($Repo, '').TrimStart('\'))" }
Write-Host ""
Write-Host "    Optional but recommended: version this garden as its own PRIVATE repo:"
Write-Host "      cd $Root; git init; git remote add origin <your-private-repo>"
