#Requires -Version 5.1
$ErrorActionPreference = 'Stop'

# TrekLink custom skills -> Claude Code (global install, ~\.claude\skills).

$SkillsDir = Split-Path -Parent $PSScriptRoot
$TargetDir = Join-Path $HOME '.claude'
$Src       = Join-Path $SkillsDir '.claude\skills'

Write-Host "==> Installing TrekLink skills to $TargetDir\skills"

if (-not (Test-Path $Src)) {
    Write-Error "!! Missing source directory: $Src"
}

$SkillTarget = Join-Path $TargetDir 'skills'
New-Item -ItemType Directory -Force -Path $SkillTarget | Out-Null
Copy-Item -Path (Join-Path $Src '*') -Destination $SkillTarget -Recurse -Force

$Skills = Get-ChildItem -Path $Src -Directory
Write-Host "==> Done: $($Skills.Count) TrekLink skills installed."
$Skills | ForEach-Object { Write-Host "    /$($_.Name)" }
Write-Host ""
Write-Host "    These complement prompt-orchestrator; install that first if you haven't:"
Write-Host "      https://github.com/ruskicoder/system-prompts -> prompt-orchestrator/install/"
