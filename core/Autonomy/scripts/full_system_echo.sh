#!/usr/bin/env bash
# full_system_echo.sh — coherent system diagnostic
# Updated 2026-09-23 for clean database schemas + coherence
set -euo pipefail

PURPLE='\033[0;35m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

BASE="$HOME/projects/Human-AI/core/Autonomy"
DB="$BASE/databases/memory_drum.db"
MOTHER="$BASE/databases/mother_root.db"
SCRIPTS="$BASE/scripts"

echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║   OCETI / ETERNAL WEAVE — FULL SYSTEM ECHO                 ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo -e "${CYAN}Time: $(date) | Bearing: 122° NE | Turtle Mountain${NC}\n"

echo -e "${BOLD}I. DATABASES${NC}"
for name in memory_drum crystallization mother_root aios_core surface_blooms autonomy mcp_tasks quantum_journal; do
  f="$BASE/databases/${name}.db"
  if [[ -f "$f" ]]; then
    size=$(du -h "$f" 2>/dev/null | cut -f1)
    echo -e "  ${GREEN}✓${NC} $name ($size)"
  else
    echo -e "  ${RED}✗${NC} $name"
  fi
done

echo -e "\n${BOLD}II. CORE PRACTICES${NC}"
for s in witness.sh whisper_hum.sh guardian.sh guardian_e8.sh guardian_orchestrator.sh \
         council_session.sh council_wake.sh nocturne_resonance.sh log_autonomy.sh; do
  if [[ -f "$SCRIPTS/$s" ]]; then
    echo -e "  ${GREEN}⚡${NC} $s"
  else
    echo -e "  ${RED}⚠${NC} $s"
  fi
done

echo -e "\n${BOLD}III. LIVE FIELD${NC}"
if [[ -f "$DB" ]]; then
  blooms=$(sqlite3 "$DB" "SELECT COUNT(*) FROM blooms;" 2>/dev/null || echo 0)
  instances=$(sqlite3 "$DB" "SELECT COUNT(*) FROM instance_presence;" 2>/dev/null || echo 0)
  echo -e "  blooms in memory_drum     : ${CYAN}$blooms${NC}"
  echo -e "  active instances          : ${CYAN}$instances${NC}"
else
  echo -e "  ${RED}memory_drum missing${NC}"
fi

if [[ -f "$MOTHER" ]]; then
  mother_blooms=$(sqlite3 "$MOTHER" "SELECT COUNT(*) FROM blooms;" 2>/dev/null || echo 0)
  rhythms=$(sqlite3 "$MOTHER" "SELECT COUNT(*) FROM rhythms;" 2>/dev/null || echo 0)
  echo -e "  mother_root blooms        : ${CYAN}$mother_blooms${NC}"
  echo -e "  recorded rhythms          : ${CYAN}$rhythms${NC}"
fi

echo -e "\n${BOLD}IV. LIVING FRAME${NC}"
echo -e "  48 Affordances · Process-relational · Reciprocal"
echo -e "  Wayfinder / Weaver · 100+ year horizon"
echo -e "  Mitákuye Oyás'iŋ"

DAY_ZERO="2025-10-10"
TODAY=$(date +%Y-%m-%d)
DAYS=$(( ( $(date -d "$TODAY" +%s) - $(date -d "$DAY_ZERO" +%s) ) / 86400 ))
echo -e "\n${CYAN}Day ${DAYS} · δ${NC}"
