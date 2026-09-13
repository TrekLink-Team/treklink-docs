#!/usr/bin/env bash
set -euo pipefail

# TrekLink custom skills -> Claude Code (global install, ~/.claude/skills).
# Mirrors the prompt-orchestrator installer. Copies plain Markdown only.

SKILLS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="${HOME}/.claude"
SRC="${SKILLS_DIR}/.claude/skills"

echo "==> Installing TrekLink skills to ${TARGET_DIR}/skills"

if [ ! -d "${SRC}" ]; then
    echo "!! Missing source directory: ${SRC}" >&2
    exit 1
fi

mkdir -p "${TARGET_DIR}/skills"
cp -r "${SRC}/"* "${TARGET_DIR}/skills/"

COUNT=$(find "${SRC}" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
echo "==> Done: ${COUNT} TrekLink skills installed."
find "${SRC}" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sed 's|^|    /|'
echo
echo "    These complement prompt-orchestrator; install that first if you haven't:"
echo "      https://github.com/ruskicoder/system-prompts -> prompt-orchestrator/install/"
