#!/usr/bin/env fish
# sync_to_aios_core.sh - Cross-DB Telemetry synchronization loop

set DRUM_DB "/home/wayfinder/projects/Human-AI/core/Autonomy/databases/memory_drum.db"
set CORE_DB "/home/wayfinder/projects/Human-AI/core/Autonomy/databases/aios_core.db"

if not test -f $DRUM_DB; or not test -f $CORE_DB
    echo "⚠️ Sync Latency: Target database paths could not be evaluated."
    exit 1
end

echo "◈ Auto-Tuning: Syncing state metrics between local drums..."

# Extract the verified L_value element from your coherence log table
set L_VAL (sqlite3 $DRUM_DB "SELECT L_value FROM coherence_log ORDER BY id DESC LIMIT 1;" 2>/dev/null)

if test -n "$L_VAL"
    echo "⚡ Propagating L_value ($L_VAL) out to tracking tables..."
    
    # Insert safely into your active review queue matrix
    sqlite3 $CORE_DB "INSERT INTO review_queue (title, content, score, status) VALUES ('Song 1 Coherence Sync', 'Production track Coffee and Concrete active. Current field coherence status metrics: L=$L_VAL.', $L_VAL, 'pending');"
    
    echo "✓ Coherence sync complete. Environment matches."
else
    echo "❌ Tuning Error: Unable to resolve data points from memory_drum."
end
