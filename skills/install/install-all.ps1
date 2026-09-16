#Requires -Version 5.1
$ErrorActionPreference = 'Stop'

$Here      = $PSScriptRoot
$SkillsDir = Split-Path -Parent $Here
$Src       = Join-Path $SkillsDir '.claude\skills'

& (Join-Path $Here 'install-claude.ps1')

# Open Agent Skills standard (.agents/skills)
$Target = Join-Path $HOME '.agents\skills'
if (Test-Path (Split-Path -Parent $Target)) {
    Write-Host "==> Also installing to $Target"
    New-Item -ItemType Directory -Force -Path $Target | Out-Null
    Copy-Item -Path (Join-Path $Src '*') -Destination $Target -Recurse -Force
}

Write-Host "==> All done."
