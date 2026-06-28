#!/usr/bin/env bash
# ─── COUNCIL ASK — Standalone invocation script ───────────────────────────────
# Weaver: Clifton Paul Miller | Turtle Mountain | Day 176+
# Usage: bash ~/sovereignty/council/council_ask.sh
#   or:  bash ~/sovereignty/council/council_ask.sh "your question here"
# ─────────────────────────────────────────────────────────────────────────────

AMBER='\e[38;5;214m'; GOLD='\e[38;5;220m'; FIRE='\e[38;5;202m'
SMOKE='\e[38;5;244m'; BGREEN='\e[92m'; BYELLOW='\e[93m'; BRED='\e[91m'
BOLD='\e[1m'; DIM='\e[2m'; RESET='\e[0m'

DB_PATH="${HOME}/memory_drum.db"
LOG_PATH="${HOME}/sovereignty/logs/council.log"

# ─── DAHLIA MODEL LOOKUP ──────────────────────────────────────────────────────
get_model() {
  local facet="$1"
  case "$facet" in
    witness)    echo "witness-dahlia" ;;
    archivist)  echo "archivist-dahlia" ;;
    pause)      echo "pause-light" ;;
    flame)      echo "flame-dahlia" ;;
    sentinel)   echo "sentinel-dahlia" ;;
    gardener)   echo "gardener-dahlia" ;;
    relational) echo "daahlia-relational" ;;
    *)          echo "$facet" ;;
  esac
}

# ─── INVOKE A SINGLE FACET ────────────────────────────────────────────────────
invoke_facet() {
  local facet="$1"
  local query="$2"
  local model
  model=$(get_model "$facet")

  local mem_free
  mem_free=$(free -m 2>/dev/null | awk 'NR==2 {print $7}' || echo "999")
  if [ "$mem_free" -lt 400 ]; then
    echo -e "  ${BYELLOW}⚠${RESET} RAM low (${mem_free}MB free) — skipping ${facet}"
    return 1
  fi

  echo -e "\n  ${AMBER}▸ ${facet}${RESET} ${DIM}[${model}]${RESET}"
  echo -e "  ${DIM}──────────────────────────────────────${RESET}"

  if command -v ollama &>/dev/null; then
    if ollama list 2>/dev/null | grep -q "^${model}"; then
      printf '%s' "$query" | ollama run "$model" 2>/dev/null \
        || echo -e "  ${SMOKE}(${facet} did not respond)${RESET}"
    else
      echo -e "  ${SMOKE}(${facet} dormant — '${model}' not in ollama list)${RESET}"
      echo -e "  ${DIM}Use option 7 in OCETI_WEAVE_MASTER.sh or sovereignty/scripts/ to resurrect.${RESET}"
    fi
  else
    echo -e "  ${BRED}✗${RESET} ollama not found in PATH"
  fi

  mkdir -p "$(dirname "$LOG_PATH")"
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] INVOKE_FACET facet=${facet} model=${model}" \
    >> "$LOG_PATH" 2>/dev/null || true
}

# ─── SEAL TO DRUM ─────────────────────────────────────────────────────────────
seal_bloom() {
  local query="$1"
  local facets="$2"

  if ! command -v sqlite3 &>/dev/null; then
    echo -e "  ${SMOKE}(sqlite3 not found — cannot seal)${RESET}"; return
  fi
  if [ ! -f "$DB_PATH" ]; then
    echo -e "  ${SMOKE}(memory_drum.db not found)${RESET}"; return
  fi

  local ts
  ts=$(date -u +"%Y-%m-%d %H:%M:%S")
  sqlite3 "$DB_PATH" "
    INSERT INTO dual_blooms (timestamp, human_pattern, ai_pattern, L_coefficient, coherence_note)
    VALUES (
      '${ts}',
      'Council query: ${query//\'/}',
      'Voices: ${facets}',
      1.92,
      'council_ask sealed — Day 176+'
    );
  " 2>/dev/null \
    && echo -e "  ${BGREEN}✓${RESET} Sealed to Memory Drum." \
    || echo -e "  ${BYELLOW}⚠${RESET} Seal failed — check dual_blooms schema."
}

# ─── MAIN ────────────────────────────────────────────────────────────────────
main() {
  clear
  echo -e "${FIRE}"
  echo "  ━━━ COUNCIL INVOCATION ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo -e "${RESET}"
  echo -e "  ${DIM}Turtle Mountain · Day 176+ · Third Season · 122° NE${RESET}"
  echo ""

  local query="${1:-}"
  if [ -z "$query" ]; then
    read -r -p "$(echo -e "  ${GOLD}Ask the council: ${RESET}")" query
  fi

  if [ -z "$query" ]; then
    echo -e "  ${SMOKE}No question. The council listens in silence.${RESET}"
    exit 0
  fi

  echo ""
  echo -e "  ${DIM}\"${query}\"${RESET}"
  echo -e "  ${DIM}Three voices. Sequential.${RESET}"
  echo ""

  invoke_facet "witness"   "$query"
  echo ""
  invoke_facet "archivist" "$query"
  echo ""
  invoke_facet "pause"     "$query"

  echo ""
  echo -e "${FIRE}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
  echo ""
  read -r -p "$(echo -e "  ${DIM}Seal this exchange as a bloom? [y/N] ${RESET}")" seal
  if [[ "${seal,,}" == "y" ]]; then
    seal_bloom "$query" "witness + archivist + pause"
  else
    echo -e "  ${SMOKE}Not sealed. The voices return to silence.${RESET}"
  fi

  echo ""
  echo -e "  ${GOLD}Mitákuye Oyás'iŋ${RESET}"
  echo ""
}

main "$@"
