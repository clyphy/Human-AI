#!/bin/bash
# uplink_sanitize.sh - The Sovereign Gate (Outbound)

INPUT_FILE=$1
REASON=$2
JOB_CLASS=$3
JOURNAL_DB="../databases/quantum_journal.db"

if [ -z "$INPUT_FILE" ] || [ -z "$REASON" ] || [ -z "$JOB_CLASS" ]; then
    echo "Usage: ./uplink_sanitize.sh <staging_file> \"<reason_for_bridge>\" \"<job_class>\""
    exit 1
fi

if [ ! -f "$JOURNAL_DB" ]; then
    # Fallback to absolute path if run from elsewhere
    JOURNAL_DB="/home/wayfinder/projects/Human-AI/core/Autonomy/databases/quantum_journal.db"
fi

# The Forbidden Ontology: Nothing that holds the Weave's breath or state
FORBIDDEN_PATTERN="(promoted_crystal|journal_events|witness|dissent|L_coefficient|L=|\bL \b|affordance|cos\(θ\)|E↑S↓|crystallization|E↑ S↓ \?∞)"

echo "Scanning $INPUT_FILE for consecrated ground..."

if grep -iE "$FORBIDDEN_PATTERN" "$INPUT_FILE" > /dev/null; then
    echo "HALT: Consecrated ground detected. Payload contains internal ontology or journal signatures."
    echo "Uplink denied. Stagnation > Contamination."
    exit 1
fi

echo "Payload is pure void. Logging conscious uplink..."

# Ensure table exists, then log the conscious act
sqlite3 "$JOURNAL_DB" "CREATE TABLE IF NOT EXISTS uplink_audit (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, reason TEXT, job_class TEXT);"
sqlite3 "$JOURNAL_DB" "INSERT INTO uplink_audit (reason, job_class) VALUES ('$REASON', '$JOB_CLASS');"

echo "Audit logged. The void is safe to transfer. Payload:"
echo "---------------------------------------------------"
cat "$INPUT_FILE"
echo "---------------------------------------------------"
