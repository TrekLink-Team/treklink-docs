#!/usr/bin/env bash
set -euo pipefail

# Installs TrekLink skills for every agent that reads the open Agent Skills
# layout or ~/.claude. Add per-agent targets here as the team adopts them.

HERE="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$(cd "${HERE}/.." && pwd)"
SRC="${SKILLS_DIR}/.claude/skills"

bash "${HERE}/install-claude.sh"

# Open Agent Skills standard (.agents/skills) — read by Codex, Cursor, OpenCode, etc.
for target in "${HOME}/.agents/skills" "${HOME}/.config/agents/skills"; do
    parent="$(dirname "${target}")"
    if [ -d "${parent}" ]; then
        echo "==> Also installing to ${target}"
        mkdir -p "${target}"
        cp -r "${SRC}/"* "${target}/"
    fi
done

echo "==> All done."
