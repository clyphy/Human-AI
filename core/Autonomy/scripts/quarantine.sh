#!/bin/bash
OCETI="$HOME/oceti-weave"
DB="$HOME/memory_drum.db"
LIST="$OCETI/quarantine_list.txt"

if [ "$1" == "--prune-all" ]; then
    echo "=== PRUNING ALL QUARANTINED ==="
    while IFS= read -r model; do
        [ -z "$model" ] && continue
        ollama rm "$model" 2>/dev/null && echo "PRUNED: $model" || echo "SKIP: $model"
    done < "$LIST"
    exit 0
fi

if [ -n "$1" ]; then
    MODEL="$1"
    REASON="${2:-No reason given}"
    echo "$MODEL" >> "$LIST"
    sort -u "$LIST" -o "$LIST"
    sqlite3 "$DB" "INSERT OR REPLACE INTO quarantine(model_name,reason,quarantined_at) VALUES('$MODEL','$REASON',datetime('now'));"
    ollama rm "$MODEL" 2>/dev/null && echo "QUARANTINED: $MODEL" || echo "LOGGED (not in Ollama): $MODEL"
    exit 0
fi

echo "Usage: quarantine.sh [model] [reason] | --prune-all"
echo "Quarantine list:"; cat "$LIST" 2>/dev/null || echo "(empty)"
