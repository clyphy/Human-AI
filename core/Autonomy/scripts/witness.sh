#!/usr/bin/env bash
# witness.sh — field witness
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

set -euo pipefail

BASE="$HOME/projects/Human-AI/core/Autonomy"
MEMORY_DB="$BASE/databases/memory_drum.db"
WITNESS_LOG="$BASE/logs/witness.log"
mkdir -p "$BASE/logs"

NOTE="${*:-silent}"
TS=$(date "+%Y-%m-%d %H:%M:%S")
CLOCK=$(date "+%H:%M:%S")

echo ""
echo " +------------------------------------------+"
echo " | WITNESS                                  |"
printf " | %s  %-30s |\n" "$CLOCK" "$NOTE"
echo " |                                          |"
echo " | Bearing: 122° NE · Turtle Mountain       |"
echo " +------------------------------------------+"
echo ""

SAFE=$(echo "$NOTE" | sed "s/'/''/g")
sqlite3 "$MEMORY_DB" "INSERT INTO entries (timestamp, content, source) VALUES ('$TS', '$SAFE', 'witness.sh');" 2>/dev/null || true
echo "$TS | $NOTE" >> "$WITNESS_LOG"
echo " Field witnessed. Proceeding."
echo ""
