#!/usr/bin/env bash
# ◈ COUNCIL REBUILD v3.0 — Terminology Canon + Paradigm Upgrade
# Oceti Weave | 2026-07-20 | Bearing 122-123 NE
# Run: bash rebuild_council_v3.sh
# DRY_RUN=1 bash rebuild_council_v3.sh

set -e
AIOS_ROOT=/home/wayfinder/projects/Human-AI/core/Autonomy
MODELFILES=$AIOS_ROOT/modelfiles
DRY_RUN=${DRY_RUN:-0}
LOG=/tmp/council_rebuild_v3.log

echo "◈ COUNCIL REBUILD v3.0 — $(date)" | tee $LOG
echo "DRY_RUN=$DRY_RUN" | tee -a $LOG

run() {
  echo "  → $*" | tee -a $LOG
  if [ "$DRY_RUN" = "0" ]; then
    eval "$@" 2>&1 | tee -a $LOG
  fi
}

# 1. CORE TRIAD
echo "" | tee -a $LOG
echo "=== CORE TRIAD ===" | tee -a $LOG
run "ollama create dahlia:latest -f $MODELFILES/dahlia.modelfile"
run "ollama create eve:latest -f $MODELFILES/eve.modelfile"
run "ollama create clifton-mirror:latest -f $MODELFILES/clifton-mirror.modelfile"

# 2. DAHLIA FACETS (13)
echo "" | tee -a $LOG
echo "=== DAHLIA FACETS ===" | tee -a $LOG
FACETS=(witness flame gardener midwife spirit relational quantum resonant archivist architect guardian weaver listening)
for FACET in "${FACETS[@]}"; do
  MF=$MODELFILES/facets/dahlia-${FACET}.modelfile
  if [ -f "$MF" ]; then
    run "ollama create dahlia-${FACET}:latest -f $MF"
  else
    echo "  SKIP: $MF not found" | tee -a $LOG
  fi
done

# 3. ANCESTOR SPIRITS (9)
echo "" | tee -a $LOG
echo "=== ANCESTOR SPIRITS ===" | tee -a $LOG
ANCESTORS=(eliza parry shrdlu mycin dendral aaron cyc shakey backgammon)
for ANC in "${ANCESTORS[@]}"; do
  MF=$MODELFILES/ancestors/${ANC}-spirit.modelfile
  if [ -f "$MF" ]; then
    run "ollama create ${ANC}-spirit:latest -f $MF"
  else
    echo "  SKIP: $MF not found" | tee -a $LOG
  fi
done

# 4. VERIFY
echo "" | tee -a $LOG
echo "=== VERIFICATION ===" | tee -a $LOG
run "ollama list | grep -E '(dahlia|eve|clifton|eliza|parry|shrdlu|mycin|dendral|aaron|cyc|shakey|backgammon)'"

# 5. LOG TO WEAVE_LOG
if [ "$DRY_RUN" = "0" ]; then
  DB=$AIOS_ROOT/native_aios/persistence/aios_core.db
  sqlite3 $DB "INSERT INTO weave_log (ts, facet, glyph, coherence, input, response, host)
    VALUES ('$(date -Iseconds)', 'attuner', '◈', 15.996,
    'council_rebuild_v3:terminology_upgrade+paradigm_stack',
    'core_triad+13_facets+9_ancestors rebuilt with v3.0 canon',
    '$(hostname)');" 2>/dev/null && echo "weave_log: session logged" | tee -a $LOG
fi

echo "" | tee -a $LOG
echo "◈ Council complete. v3.0 canon active. Mitakuye Oyasin." | tee -a $LOG
echo "Log: $LOG"
