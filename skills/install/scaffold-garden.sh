#!/usr/bin/env bash
set -euo pipefail

# Scaffold a personal SSOT garden inside a repo's gitignored ignore/ folder.
# Convention: _docs/01-conventions/09-doc-driven-scaffold-and-ssot-conventions.md
#
# Usage: bash scaffold-garden.sh <your_name> [/path/to/repo]

NAME="${1:-}"
REPO="${2:-$(pwd)}"

if [ -z "${NAME}" ]; then
    echo "Usage: bash scaffold-garden.sh <your_name> [/path/to/repo]" >&2
    echo "  e.g. bash scaffold-garden.sh khoa ~/capstone/treklink-web" >&2
    exit 1
fi
if [ ! -d "${REPO}/.git" ]; then
    echo "!! Not a git repository: ${REPO}" >&2
    exit 1
fi

ROOT="${REPO}/ignore/${NAME}"
if [ -e "${ROOT}" ]; then
    echo "==> ${ROOT} already exists — leaving it alone (nothing overwritten)."
    exit 0
fi

echo "==> Scaffolding personal garden: ${ROOT}"
mkdir -p "${ROOT}"/{docs/{sessions,diagrams,flows},scripts,envs}
touch "${ROOT}/docs/diagrams/.gitkeep" "${ROOT}/docs/flows/.gitkeep"

cat > "${ROOT}/docs/00-index.md" <<EOF
# ${NAME} — Personal Garden

Gitignored. Total write privilege. Nothing here is authoritative.

- \`current-progress.md\` — rolling POINTER to the latest session file (not a write target)
- \`sessions/\` — one file per session instance: \`YYYY-MM-DD-HHMM-topic.md\`
- \`diagrams/\`, \`flows/\` — Mermaid \`.mmd\`
- \`../scripts/\` — local tooling and scratch scripts
- \`../envs/\` — env templates. **Never committed anywhere.**

Authoritative docs live in \`treklink-docs/_docs/\`. If this and a tracked doc disagree,
the tracked one wins.
EOF

cat > "${ROOT}/docs/current-progress.md" <<EOF
# ${NAME} — Current Progress (pointer only)

> This file is a **pointer**, not a write target. High-frequency notes go in a per-session
> file under \`sessions/\` — one shared rolling file is what caused lost findings under
> concurrent sessions.

**Latest**: _(none yet)_

**Active branches**: _(none)_
EOF

cat > "${ROOT}/scripts/README.md" <<EOF
# ${NAME} — Local scripts

Scratch tooling: seeders, data mappers, one-off analysis. Never application code —
that belongs in the tracked tree.
EOF

cat > "${ROOT}/envs/README.md" <<EOF
# ${NAME} — Environment templates

Local \`.env\` files and connection strings (including Neon — see D-010).

**Never commit these. Not here, not anywhere.**
EOF

echo "==> Done."
find "${ROOT}" -type f | sed "s|${REPO}/|    |"
echo
echo "    Optional but recommended: version this garden as its own PRIVATE repo:"
echo "      cd ${ROOT} && git init && git remote add origin <your-private-repo>"
