#!/usr/bin/env bash
# Render every assets/mermaid/*.mmd to PNG with @mermaid-js/mermaid-cli and Mermaid 12.0.0,
#   MMDC_DIR=<dir with node_modules/@mermaid-js/mermaid-cli and mermaid@12.0.0> render_figures.sh <reports dir>
set -euo pipefail
OUT="${1:?reports dir}"
MMDC="${MMDC_DIR:?}/node_modules/.bin/mmdc"
CHROME="${CHROME:-$(ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome | head -1)}"
CFG="$(mktemp)"; echo "{\"executablePath\":\"$CHROME\",\"args\":[\"--no-sandbox\"]}" > "$CFG"
MCFG="$(mktemp --suffix=.json)"; echo '{"theme":"neutral","flowchart":{"htmlLabels":true,"useMaxWidth":false},"er":{"useMaxWidth":false},"state":{"useMaxWidth":false},"swimlane":{"useMaxWidth":false}}' > "$MCFG"
for f in "$OUT"/assets/mermaid/*.mmd; do
  b="$(basename "$f" .mmd)"
  "$MMDC" -q -p "$CFG" -c "$MCFG" -b white -s 3 -i "$f" -o "$OUT/assets/$b.png"
done
echo "rendered $(ls "$OUT"/assets/mermaid/*.mmd | wc -l) figures; run measure_figures.py next"
