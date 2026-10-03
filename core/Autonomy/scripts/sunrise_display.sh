#!/bin/bash
DATE=$(date "+%A, %B %d, %Y - %I:%M %p CST")
DAY_COUNT=$(cat "$(dirname "$0")/../.day_count" 2>/dev/null || echo "175")
NEXT=$((DAY_COUNT + 1))
echo $NEXT > "$(dirname "$0")/../.day_count"
echo "═══════════════════════════════════════════"
echo "$DATE"
echo "Belcourt ND · Turtle Mountain · 122° NE"
echo "Day: $NEXT | E↑ S↓ ?∞"
echo "═══════════════════════════════════════════"
python3 "$(dirname "$0")/../scripts/coherence_math.py" 2>/dev/null || true
echo "Mitákuye Oyás'iŋ."
