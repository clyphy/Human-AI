#!/usr/bin/env bash
# quarantine.sh — simple model quarantine / prune
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

set -euo pipefail

BASE="$HOME/projects/Human-AI/core/Autonomy"
DB="$BASE/databases/memory_drum.db"
LIST="$BASE/logs/quarantine_list.txt"
mkdir -p "$(dirname "$LIST")"

if [[ "${1:-}" == "--prune-all" ]]; then
    echo "=== PRUNING ALL QUARANTINED ==="
    if [[ -f "$LIST" ]]; then
        while IFS= read -r model; do
            [[ -z "$model" ]] && continue
            ollama rm "$model" 2>/dev/null && echo "PRUNED: $model" || echo "SKIP: $model"
            done < "$LIST"
            else
        echo "(list empty)"
        fi
        exit 0
        fi
        
        if [[ -n "${1:-}" ]]; then
            MODEL="$1"
            REASON="${2:-No reason given}"
            echo "$MODEL" >> "$LIST"
            sort -u "$LIST" -o "$LIST"
            if [[ -f "$DB" ]]; then
                sqlite3 "$DB" "INSERT OR REPLACE INTO quarantine(model_name,reason,quarantined_at) VALUES('$MODEL','$REASON',datetime('now'));" 2>/dev/null || true
                fi
                ollama rm "$MODEL" 2>/dev/null && echo "QUARANTINED: $MODEL" || echo "LOGGED (not in Ollama): $MODEL"
                exit 0
                fi
                
                echo "Usage: quarantine.sh [model] [reason] | --prune-all"
                echo "Quarantine list:"
