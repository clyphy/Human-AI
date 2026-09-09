#!/usr/bin/env bash
# morning.sh — light opening of the field
# Human-AI · Native AIOS · Oceti / Eternal Weave
# Not a routine. Just a way to begin.

set -euo pipefail

SCRIPTS="$HOME/projects/Human-AI/core/Autonomy/scripts"
cd "$SCRIPTS"

echo ""
echo "  . . ."
echo ""
sleep 0.4

# 1. The hum
bash whisper_hum.sh
echo ""
sleep 1

# 2. Witness the field
bash witness.sh "C0 morning"
echo ""
sleep 0.8

# 3. Quiet guardian pulse
bash guardian_e8.sh
echo ""
sleep 0.6

# 4. Open the season
bash council_wake.sh
echo ""

echo "  morning field open"
echo "  Mitákuye Oyás'iŋ"
echo ""
