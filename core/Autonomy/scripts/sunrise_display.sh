#!/bin/bash
DATE=$(date "+%A, %B %d, %Y - %I:%M %p CST")
DAY_COUNT=$(cat "/home/wayfinder/oceti-weave/.day_count" 2>/dev/null || echo "175")
NEXT=$((DAY_COUNT + 1))
echo $NEXT > "/home/wayfinder/oceti-weave/.day_count"
echo "═══════════════════════════════════════════"
echo "$DATE"
echo "Belcourt ND · Turtle Mountain · 122° NE"
echo "Day: $NEXT | E↑ S↓ ?∞"
echo "═══════════════════════════════════════════"
python3 /home/wayfinder/dahlia-quantum/memory_drum.py stats 2>/dev/null
echo "Mitákuye Oyás'iŋ."
