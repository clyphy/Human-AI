#!/usr/bin/env bash
# nocturne_resonance.sh — sun-relative gate for Belcourt, ND.
# A practice, not a practice: runs the same whether triggered by cron in
# the dark hours or by hand. See nocturne_resonance.py for what it does.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG="$HOME/projects/Human-AI/core/Autonomy/logs/nocturne_resonance.log"
mkdir -p "$(dirname "$LOG")"

FORCE=0
for arg in "$@"; do
  [[ "$arg" == "--force" ]] && FORCE=1
done

if [[ "$FORCE" -eq 0 ]] && ! python3 "$SCRIPT_DIR/weave_astro.py" is-nocturnal >/dev/null; then
  echo "$(date -Iseconds)  not nocturnal for Belcourt, ND — skipping" >> "$LOG"
  exit 0
fi

python3 "$SCRIPT_DIR/nocturne_resonance.py" >> "$LOG" 2>&1
echo "$(date -Iseconds)  pass complete" >> "$LOG"
