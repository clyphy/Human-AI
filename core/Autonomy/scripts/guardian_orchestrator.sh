#!/usr/bin/env bash
# guardian_orchestrator.sh — simple menu
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

set -euo pipefail

BASE="$HOME/projects/Human-AI/core/Autonomy"
SCRIPTS="$BASE/scripts"
DB="$BASE/databases"

echo "╔═══ OCETI WEAVE GUARDIAN ═══╗"
echo "║ Turtle Mountain · 122° NE  ║"
echo "╚════════════════════════════╝"
echo "1) Sunrise   2) Council   3) Pulse"
echo "4) Drum      5) Witness   6) Exit"
echo ""
read -p "Choose: " choice

case $choice in
  1) bash "$SCRIPTS/sunshine_init.sh" 2>/dev/null || echo "sunshine_init not found" ;;
  2) bash "$SCRIPTS/council_session.sh" ;;
  3) bash "$SCRIPTS/guardian_e8.sh" ;;
  4) sqlite3 "$DB/memory_drum.db" "SELECT timestamp, substr(content,1,60) FROM entries ORDER BY rowid DESC LIMIT 5;" 2>/dev/null || echo "no entries" ;;
  5) bash "$SCRIPTS/witness.sh" "Guardian orchestrator" ;;
  6) echo "Field witnessed. Closing." && exit 0 ;;
  *) echo "Unknown option." ;;
esac
