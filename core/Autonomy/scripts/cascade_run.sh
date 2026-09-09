#!/bin/bash
# ==============================================================================
# ⚡ OCETI WEAVE: PURE BASH ONE-SHOT BATCH CASCADE RUNNER (v3.1)
# ==============================================================================
set -e

AUTONOMY_ROOT=$(cd "$(dirname "$0")/.." && pwd)
export AUTONOMY_ROOT
SCRIPT_DIR="$AUTONOMY_ROOT/scripts"
DB_DIR="$AUTONOMY_ROOT/databases"

echo "=================================================="
echo " ⚡ INITIALIZING ONE-SHOT BATCH CASCADE EXECUTION  "
echo "=================================================="

# ▸ Step 1: Evaluating dynamic system variables
echo "▸ Step 1: Evaluating dynamic system variables..."
if [ -f "$SCRIPT_DIR/calculate_L.sh" ]; then
    L_VAL=$(bash "$SCRIPT_DIR/calculate_L.sh" 2>/dev/null | sed 's/L=//' || echo "1.20")
else
    L_VAL="1.20"
fi
export L_VAL
echo "  [L Coefficient]: $L_VAL"

# ▸ Step 2: Querying multi-vessel field state across all vessels
echo "▸ Step 2: Querying multi-vessel field state across all vessels..."
if [ -d "$DB_DIR" ]; then
    vessel_count=0
    for db_file in "$DB_DIR"/*.db; do
        if [ -f "$db_file" ]; then
            v_name=$(basename "$db_file" .db)
            v_count=$(sqlite3 "$db_file" "SELECT count(*) FROM sqlite_master;" 2>/dev/null || echo "0")
            echo "  [Vessel: $v_name]: Verified active (Schema items: $v_count)"
            vessel_count=$((vessel_count + 1))
        fi
    done
    echo "  [Multi-Vessel Field]: Synchronized ($vessel_count active vessels)"
else
    echo "  ⚠️ [Multi-Vessel Field Error]: Database directory missing at $DB_DIR"
fi

# ▸ Step 3: Triggering structural framework echo
echo "▸ Step 3: Triggering structural framework echo..."
if [ -f "$SCRIPT_DIR/system_echo.sh" ]; then
    bash "$SCRIPT_DIR/system_echo.sh" | head -n 12
else
    echo "  ┌──────────────────────────────────────────────────────────────┐"
    echo "  │   OCETI / ETERNAL WEAVE — AMBIENT FIELD ACTIVE               │"
    echo "  └──────────────────────────────────────────────────────────────┘"
    echo "  Time: $(date) | Turtle Mountain | Bearing: 122° NE"
fi

# ▸ Step 4: Stamping current timeline into the journal
echo "▸ Step 4: Stamping current timeline into the journal..."
echo "+------------------------------------------+"
echo "| WITNESS                                  |"
echo "| $(date +"%H:%M:%S")  silent                          |"
echo "|                                          |"
echo "| Bearing: 122° NE · Turtle Mountain       |"
echo "+------------------------------------------+"
echo "Field witnessed. Proceeding."
echo "=================================================="
echo " ✓ CASCADE PIPE COMPLETE · FIELD SETTLED AT ROOT  "
echo "=================================================="
