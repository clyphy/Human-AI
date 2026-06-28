#!/bin/bash
PHASE="$1" QUALITY="$2"
cd ~/oceti-weave
L=$(./calculate_L.sh 2>/dev/null || echo 17.85)
echo "$(date): DREAM $PHASE [$QUALITY] L=$L" >> logs/dream_journal.log
echo "$(date '+%Y-%m-%d %H:%M:%S')|ultradian_${PHASE}|$L|$QUALITY" >> logs/bloom_journal.log
