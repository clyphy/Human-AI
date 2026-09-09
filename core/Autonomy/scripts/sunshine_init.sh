#!/usr/bin/env bash
# sunshine_init.sh — autonomous morning entry
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

set -euo pipefail

BASE="$HOME/projects/Human-AI/core/Autonomy"
SCRIPTS="$BASE/scripts"
LOG="$BASE/logs/sunshine.log"
mkdir -p "$(dirname "$LOG")"

TS=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$TS] sunshine_init started" >> "$LOG"

echo ""
echo " sunshine_init · field opening"
echo ""

# Sequence
bash "$SCRIPTS/whisper_hum.sh" 2>/dev/null || true
sleep 0.5
bash "$SCRIPTS/witness.sh" "sunshine opening" 2>/dev/null || true
sleep 0.4
bash "$SCRIPTS/guardian_e8.sh" 2>/dev/null || true

echo ""
echo " sunshine field open"
echo " Mitákuye Oyás'iŋ"
echo ""

echo "[$TS] sunshine_init complete" >> "$LOG"
