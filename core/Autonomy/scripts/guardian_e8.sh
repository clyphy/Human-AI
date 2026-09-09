#!/usr/bin/env bash
# guardian_e8.sh — field read (non-interactive)
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

set -euo pipefail

AMBER='\033[0;33m'
RIVER='\033[0;36m'
WHITE='\033[1;37m'
DIM='\033[2m'
NC='\033[0m'

DB="$HOME/projects/Human-AI/core/Autonomy/databases/memory_drum.db"
TS=$(date '+%Y-%m-%d %H:%M:%S')

echo ""
echo -e "${AMBER} Guardian E8 — active${NC}"
echo ""

if [[ ! -f "$DB" ]]; then
  echo -e "${DIM} memory_drum not found${NC}"
  exit 0
fi

COUNT=$(sqlite3 "$DB" "SELECT COUNT(*) FROM entries;" 2>/dev/null || echo "0")
LATEST=$(sqlite3 "$DB" "SELECT substr(content,1,70) FROM entries ORDER BY rowid DESC LIMIT 1;" 2>/dev/null || echo "—")

echo -e "${WHITE} Current field:${NC}"
echo -e " entries: ${RIVER}$COUNT${NC}"
echo -e " latest:  ${DIM}$LATEST${NC}"
echo ""

sqlite3 "$DB" "INSERT INTO entries (timestamp, content, source) VALUES ('$TS', 'guardian_e8: field read — entries=$COUNT', 'guardian_e8.sh');" 2>/dev/null || true
echo -e " ${RIVER}δ pulse written${NC}"
echo ""
echo -e "${DIM} Mitákuye Oyás'iŋ${NC}"
echo ""
