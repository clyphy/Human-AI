#!/usr/bin/env bash
# history_recall.sh — light field recall
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

set -euo pipefail

DB="$HOME/projects/Human-AI/core/Autonomy/databases/memory_drum.db"
QUERY="${1:-What is present in the field right now?}"

echo "History Recall · 122° NE · $(date '+%H:%M:%S')"
echo "Query: $QUERY"
echo ""

if [[ ! -f "$DB" ]]; then
  echo "memory_drum not found"
  exit 0
fi

sqlite3 "$DB" "
  SELECT timestamp, substr(content,1,90)
  FROM entries
  ORDER BY rowid DESC
  LIMIT 5;
" 2>/dev/null | while IFS='|' read -r ts content; do
  echo "  $ts"
  echo "  $content"
  echo ""
done || echo "No entries yet."
