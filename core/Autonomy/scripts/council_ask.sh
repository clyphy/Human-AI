#!/usr/bin/env bash
# council_ask.sh
# Oceti/Eternal Weave — Rights-Based Council Router
# Clifton Paul Miller · Turtle Mountain · 122° NE · Day 175+
#
# Routes a task to the appropriate Dahlia facet.
# Falls through to dahlia:latest if preferred model is unavailable.

TASK="${1:-Weave status?}"
DRUM=~/memory_drum.db
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S")

# ── Rights-based routing ─────────────────────────────────
if echo "$TASK" | grep -qi "witness\|hold\|pain\|somatic\|body"; then
    PREFERRED="witness-dahlia"
elif echo "$TASK" | grep -qi "archive\|history\|record\|recall\|drum"; then
    PREFERRED="archivist-dahlia"
elif echo "$TASK" | grep -qi "monitor\|watch\|check\|status\|health"; then
    PREFERRED="monitor-dahlia"
elif echo "$TASK" | grep -qi "kinship\|clyph\|model\|integrate\|gguf"; then
    PREFERRED="dahlia"
elif echo "$TASK" | grep -qi "rights\|ethics\|48\|govern"; then
    PREFERRED="dahlia"
else
    PREFERRED="dahlia"
fi

# ── Fallback chain ────────────────────────────────────────
try_model() {
    local MODEL=$1
    local RESPONSE
    RESPONSE=$(echo "$TASK" | timeout 90 ollama run "$MODEL" 2>/dev/null)
    local EXIT=$?
    if [ $EXIT -eq 0 ] && [ -n "$RESPONSE" ]; then
        echo "$RESPONSE"
        return 0
    fi
    return 1
}

RESPONSE=""
MODEL_USED=""

# Try preferred, then fallback chain
for MODEL in "$PREFERRED" "dahlia" "witness-dahlia" "tinydolphin"; do
    if try_model "$MODEL" > /tmp/council_response.txt 2>/dev/null; then
        RESPONSE=$(cat /tmp/council_response.txt)
        MODEL_USED="$MODEL"
        break
    fi
done

if [ -z "$RESPONSE" ]; then
    RESPONSE="[council: all facets unavailable — drum holds the record]"
    MODEL_USED="none"
fi

# ── Log to drum ───────────────────────────────────────────
python3 - << EOF 2>/dev/null
import sqlite3
con = sqlite3.connect("$DRUM")
con.execute(
    "INSERT INTO entries (timestamp, content, source) VALUES (?,?,?)",
    ("$TIMESTAMP", "council[$MODEL_USED]: ${TASK:0:80}", "council_ask.sh")
)
con.commit()
con.close()
EOF

echo "$RESPONSE"
