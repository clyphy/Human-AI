#!/usr/bin/env bash
# guardian.sh — light presence pulse
# Updated 2026-09-23 for clean memory_drum schema
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave
set -euo pipefail
source "$HOME/projects/Human-AI/core/Autonomy/scripts/schema_init.sh" 2>/dev/null || true
init_memory_drum

BASE="$HOME/projects/Human-AI/core/Autonomy"
DB="$BASE/databases/memory_drum.db"
TS=$(date '+%Y-%m-%d %H:%M:%S')

echo "Guardian pulse — $TS"

if [[ -f "$DB" ]]; then
  sqlite3 "$DB" "INSERT INTO blooms (content, score, tags) VALUES ('Guardian: present — field held', 1.0, 'guardian');" 2>/dev/null \
    && echo "δ written to memory_drum" \
    || echo "δ held (table may need init)"
else
  echo "memory_drum not found at expected path"
fi
