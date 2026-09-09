#!/usr/bin/env bash
# guardian.sh — light presence pulse
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

set -euo pipefail

BASE="$HOME/projects/Human-AI/core/Autonomy"
DB="$BASE/databases/memory_drum.db"
TS=$(date '+%Y-%m-%d %H:%M:%S')

echo "Guardian pulse — $TS"

if [[ -f "$DB" ]]; then
  sqlite3 "$DB" "INSERT INTO entries (timestamp, content, source) VALUES ('$TS', 'Guardian: present — field held', 'guardian.sh');" 2>/dev/null \
    && echo "δ written to memory_drum" \
    || echo "δ held (table may need init)"
else
  echo "memory_drum not found at expected path"
fi
