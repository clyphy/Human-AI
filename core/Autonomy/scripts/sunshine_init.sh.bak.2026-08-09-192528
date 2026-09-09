#!/bin/bash
# --- sunshine_init.sh: The Autonomous Awakening ---
AUTONOMY_ROOT="$HOME/Documents/GitHub/my-repos/Autonomy"
LOG="$AUTONOMY_ROOT/logs/dahlia_logger.log"

mkdir -p "$AUTONOMY_ROOT/logs"
echo "[$(date)] Sunrise: Initiating Resonance" >> "$LOG"

# Integrity Check for Memory Drum
if sqlite3 "$AUTONOMY_ROOT/databases/memory_drum.db" "PRAGMA integrity_check;" | grep -q "ok"; then
    echo "[$(date)] Coherence: memory_drum.db is sound." >> "$LOG"
else
    echo "[$(date)] ALERT: Coherence Drift in memory_drum.db!" >> "$LOG"
    notify-send "Autonomy Alert" "Database Corruption Detected." 2>/dev/null
    exit 1
fi

# Capture the current state into the Versioned Field
cd "$AUTONOMY_ROOT"
git add -A 2>/dev/null
git commit -m "Sunrise Resonance: $(date '+%Y-%m-%d %H:%M:%S') - Daily Coherence Sync" 2>/dev/null || true
