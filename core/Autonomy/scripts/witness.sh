#!/usr/bin/env bash
# witness.sh — read-only observer
# Updated 2026-09-23 for clean memory_drum schema + coherence
set -euo pipefail
source "$HOME/projects/Human-AI/core/Autonomy/scripts/schema_init.sh" 2>/dev/null || true
init_memory_drum

AUTONOMY_ROOT="${AUTONOMY_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
DB="$AUTONOMY_ROOT/databases/memory_drum.db"
MOTHER="$AUTONOMY_ROOT/databases/mother_root.db"
LOG_DIR="$AUTONOMY_ROOT/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/witness.jsonl"

ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)

bloom_count=$(sqlite3 "$DB" "SELECT COUNT(*) FROM blooms;" 2>/dev/null || echo 0)
instance_count=$(sqlite3 "$DB" "SELECT COUNT(*) FROM instance_presence;" 2>/dev/null || echo 0)
top_affordance=$(sqlite3 "$DB" "SELECT affordance_id FROM affordance_freq ORDER BY count DESC LIMIT 1;" 2>/dev/null || echo none)
mother_blooms=$(sqlite3 "$MOTHER" "SELECT COUNT(*) FROM blooms;" 2>/dev/null || echo 0)

[ -z "$top_affordance" ] && top_affordance=none

printf "{\"ts\":\"%s\",\"bloom_count\":%s,\"instance_count\":%s,\"top_affordance\":\"%s\",\"mother_blooms\":%s}\n" \
  "$ts" "${bloom_count:-0}" "${instance_count:-0}" "${top_affordance}" "${mother_blooms:-0}" >> "$LOG"

echo "+------------------------------------------+"
echo "| WITNESS                                  |"
echo "| $(date +%H:%M:%S)  silent                         |"
echo "|                                          |"
echo "| Bearing: 122° NE · Turtle Mountain       |"
echo "+------------------------------------------+"
echo ""
echo " Field witnessed. Proceeding."
