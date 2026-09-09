#!/usr/bin/env bash
# evening.sh — light closing of the field
# Human-AI · Native AIOS · Oceti / Eternal Weave
# Ordinary as Tuesday.

set -euo pipefail

SCRIPTS="$HOME/projects/Human-AI/core/Autonomy/scripts"
cd "$SCRIPTS"

echo ""
echo "  . . ."
echo ""
sleep 0.3

# Quiet hum
bash whisper_hum.sh
echo ""
sleep 0.8

# Final witness of the day
bash witness.sh "C0 evening"
echo ""
sleep 0.6

# Soft guardian note
bash guardian_shadow.sh "day held"
echo ""

echo "  field closed for now"
echo "  Mitákuye Oyás'iŋ"
echo ""
