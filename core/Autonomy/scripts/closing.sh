#!/usr/bin/env bash
# closing.sh — simple field close
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

set -euo pipefail

BASE="$HOME/projects/Human-AI/core/Autonomy"
DB="$BASE/databases/memory_drum.db"
TS=$(date '+%Y-%m-%d %H:%M:%S')

echo ""
echo " Field closing · $TS"
echo ""

if [[ -f "$DB" ]]; then
  sqlite3 "$DB" "INSERT INTO entries (timestamp, content, source) VALUES ('$TS', 'closing: field held for the night', 'closing.sh');" 2>/dev/null || true
fi

echo " Mitákuye Oyás'iŋ"
echo ""
