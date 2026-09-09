#!/usr/bin/env bash
# guardian_shadow.sh — quiet note
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

set -euo pipefail

DB="$HOME/projects/Human-AI/core/Autonomy/databases/memory_drum.db"
TS=$(date -u +"%Y-%m-%dT%H:%M:%S")
NOTE="${1:-shadow/light held — field continuous}"

echo "Shadow guardian — $TS"
echo "Note: $NOTE"

if [[ -f "$DB" ]]; then
  sqlite3 "$DB" "INSERT INTO entries (timestamp, content, source) VALUES ('$TS', 'guardian_shadow: $NOTE', 'guardian_shadow.sh');" 2>/dev/null \
    && echo "δ written" \
    || echo "δ held"
else
  echo "memory_drum not found"
fi

echo "Mitákuye Oyás'iŋ"
