#!/usr/bin/env fish
# inversion_cascade.sh — Real-time state signature extraction

echo "=================================================="
echo " 🌀 EXECUTING INVERSION CASCADE STATE QUERY      "
echo "=================================================="

# Query 1: Extract latest weave entry
echo "▸ Extraction 1/2: Core Heartbeat Ledger..."
if test -f databases/aios_core.db
    sqlite3 databases/aios_core.db "SELECT ts, facet, coherence, host FROM weave_log ORDER BY rowid DESC LIMIT 1;" 2>/dev/null
else
    echo "  [Core Weave Log]: Closed"
end

# Query 2: Extract latest reflection entry
echo "▸ Extraction 2/2: Living Reflection Log..."
if test -f databases/memory_drum.db
    sqlite3 databases/memory_drum.db "SELECT timestamp, l_coeff, content FROM ai_reflections ORDER BY rowid DESC LIMIT 1;" 2>/dev/null
else
    echo "  [Memory Drum]: Rested"
end

echo "=================================================="
echo " ✓ INVERSION CASCADE COMPLETE · ROOT FLAT        "
echo "=================================================="
