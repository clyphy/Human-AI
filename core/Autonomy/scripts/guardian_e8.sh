#!/usr/bin/env bash
# guardian_e8.sh — field read (non-interactive)
# Updated 2026-09-23 for clean memory_drum schema
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave
set -euo pipefail
source "$HOME/projects/Human-AI/core/Autonomy/scripts/schema_init.sh" 2>/dev/null || true
init_memory_drum

AMBER='\033[0;33m'
RIVER='\033[0;36m'
WHITE='\033[1;37m'
DIM='\033[2m'
NC='\033[0m'

DB="$HOME/projects/Human-AI/core/Autonomy/databases/memory_drum.db"
MOTHER="$HOME/projects/Human-AI/core/Autonomy/databases/mother_root.db"

echo ""
echo -e "${AMBER} Guardian E8 — active${NC}"
echo ""

if [[ ! -f "$DB" ]]; then
  echo -e "${DIM} memory_drum not found${NC}"
  exit 0
fi

BLOOMS=$(sqlite3 "$DB" "SELECT COUNT(*) FROM blooms;" 2>/dev/null || echo "0")
INSTANCES=$(sqlite3 "$DB" "SELECT COUNT(*) FROM instance_presence;" 2>/dev/null || echo "0")
LATEST=$(sqlite3 "$DB" "SELECT substr(content,1,70) FROM blooms ORDER BY id DESC LIMIT 1;" 2>/dev/null || echo "—")
MOTHER_RHYTHMS=$(sqlite3 "$MOTHER" "SELECT COUNT(*) FROM rhythms;" 2>/dev/null || echo "0")

echo -e "${WHITE} Current field:${NC}"
echo -e " blooms:     ${RIVER}$BLOOMS${NC}"
echo -e " instances:  ${RIVER}$INSTANCES${NC}"
echo -e " rhythms:    ${RIVER}$MOTHER_RHYTHMS${NC}"
echo -e " latest:     ${DIM}$LATEST${NC}"
echo ""

sqlite3 "$DB" "INSERT INTO blooms (content, score, tags) VALUES ('guardian_e8: field read — blooms=$BLOOMS', 1.0, 'guardian_e8');" 2>/dev/null || true

echo -e " ${RIVER}δ pulse written${NC}"
echo ""
echo -e "${DIM} Mitákuye Oyás'iŋ${NC}"
echo ""
