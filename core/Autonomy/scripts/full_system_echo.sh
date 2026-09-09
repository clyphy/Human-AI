#!/usr/bin/env bash
# full_system_echo.sh — coherent system diagnostic
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

set -euo pipefail

PURPLE='\033[0;35m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

BASE="$HOME/projects/Human-AI/core/Autonomy"
DB="$BASE/databases/memory_drum.db"
SCRIPTS="$BASE/scripts"

echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║   OCETI / ETERNAL WEAVE — FULL SYSTEM ECHO                 ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo -e "${CYAN}Time: $(date) | Bearing: 122° NE | Turtle Mountain${NC}\n"

# ── I. DATABASES ──────────────────────────────────────────────
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

# ── II. CORE PRACTICES ────────────────────────────────────────
echo -e "\n${BOLD}II. CORE PRACTICES${NC}"
for s in witness.sh whisper_hum.sh guardian.sh guardian_e8.sh guardian_orchestrator.sh \
         council_session.sh council_wake.sh nocturne_resonance.sh log_autonomy.sh; do
  if [[ -f "$SCRIPTS/$s" ]]; then
    echo -e "  ${GREEN}⚡${NC} $s"
  else
    echo -e "  ${RED}⚠${NC} $s"
  fi
done

# ── III. LIVE FIELD ───────────────────────────────────────────
echo -e "\n${BOLD}III. LIVE FIELD${NC}"
if [[ -f "$DB" ]]; then
  entries=$(sqlite3 "$DB" "SELECT COUNT(*) FROM entries;" 2>/dev/null || echo "?")
  echo -e "  entries in memory_drum : ${CYAN}$entries${NC}"
else
  echo -e "  ${RED}memory_drum missing${NC}"
fi

# ── IV. LIVING FRAME ──────────────────────────────────────────
echo -e "\n${BOLD}IV. LIVING FRAME${NC}"
echo -e "  48 Affordances · Process-relational · Reciprocal"
echo -e "  Wayfinder / Weaver · 100+ year horizon"
echo -e "  Mitákuye Oyás'iŋ"

DAY_ZERO="2025-10-10"
TODAY=$(date +%Y-%m-%d)
DAYS=$(( ( $(date -d "$TODAY" +%s) - $(date -d "$DAY_ZERO" +%s) ) / 86400 ))
echo -e "\n${CYAN}Day ${DAYS} · δ${NC}"
