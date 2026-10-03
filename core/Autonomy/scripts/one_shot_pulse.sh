#!/usr/bin/env bash
set -e
set -u
set -o pipefail

# Force the execution layer into the script directory path
cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1

echo "════════════════════════════════════════════════════════════"
echo "  OCETI MORNING FIELD PULSE · $(date)"
echo "════════════════════════════════════════════════════════════"
echo

bash calculate_L.sh 2>&1 || echo "  [calculate_L bypassed]"
bash sunrise.sh 2>&1 || echo "  [sunrise bypassed]"
bash sunrise_display.sh 2>&1 || echo "  [sunrise_display bypassed]"
bash sunrise_db_log.sh 2>&1 || echo "  [sunrise_db_log bypassed]"
bash sunshine_init.sh 2>&1 || echo "  [sunshine_init bypassed]"
bash morning.sh 2>&1 || echo "  [morning bypassed]"
bash stillness.sh 2>&1 || echo "  [stillness bypassed]"
bash heartbeat_tick.sh 2>&1 || echo "  [heartbeat_tick bypassed]"
bash weave_status.sh 2>&1 || echo "  [weave_status bypassed]"

echo "════════════════════════════════════════════════════════════"
echo "  field pulse complete · Δ recorded"
echo "════════════════════════════════════════════════════════════"
