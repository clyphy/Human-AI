#!/bin/bash
# ==============================================================================
# ╔══════════════════════════════════════════════════════════════╗
# ║           OCETI / ETERNAL WEAVE — SYSTEM ECHO (v3.2)          ║
# ╚══════════════════════════════════════════════════════════════╝
# ==============================================================================
set -e

BASE="${AUTONOMY_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
GREEN='\033[0;32m'
NC='\033[0;30m'
BOLD='\033[1m'

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   OCETI / ETERNAL WEAVE — SYSTEM ECHO                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo "Time: $(date) | Bearing: 122° NE | Turtle Mountain"
echo ""

# ──────────────────────────────────────────────────────────────────────────────
# I. DATABASES
# ──────────────────────────────────────────────────────────────────────────────
echo -e "${BOLD}I. DATABASES${NC}"
for name in memory_drum crystallization mother_root aios_core; do
    f="$BASE/databases/${name}.db"
    if [ -f "$f" ]; then
        size=$(du -h "$f" 2>/dev/null | cut -f1)
        echo -e "  ${GREEN}✓${NC} $name ($size)"
    else
        echo -e "  ✗ $name (Missing)"
    fi
done

# ──────────────────────────────────────────────────────────────────────────────
# II. CORE PRACTICES
# ──────────────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}II. CORE PRACTICES${NC}"

# Safely check for files and paths without raw, unescaped multi-line logic chaining
if [ -d "$BASE/docs/ontology" ]; then
    echo -e "  ${GREEN}✓${NC} Ontology Lattice Framework: Active"
else
    echo -e "  ✗ Ontology Lattice Framework: Directory Missing"
fi

if [ -f "$BASE/.weave_env" ]; then
    echo -e "  ${GREEN}✓${NC} Shared Environment Substrate: Bound"
else
    echo -e "  ✗ Shared Environment Substrate: Missing"
fi

if [ -x "$BASE/scripts/calculate_L.sh" ]; then
    echo -e "  ${GREEN}✓${NC} Coherence Tracking Utility: Executable"
else
    echo -e "  ✗ Coherence Tracking Utility: Inaccessible"
fi

echo ""
