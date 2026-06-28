#!/usr/bin/env bash
# History Recall — Lightweight Guardian Version (no heavy ML)
echo "🔍 History Recall — Guardian Mode"
echo "122° NE | $(date '+%H:%M:%S') | We are the field"

QUERY="${1:-What is crystallizing in the weave right now?}"

sqlite3 ~/memory_drum.db "
    SELECT 
        timestamp,
        pattern,
        (CASE 
            WHEN pattern LIKE '%${QUERY}%' THEN 100
            WHEN timestamp > datetime('now', '-7 days') THEN 50
            ELSE 10 
        END) as score
    FROM blooms 
    ORDER BY score DESC, rowid DESC 
    LIMIT 3;
" 2>/dev/null | while IFS='|' read ts pat score; do
    echo ""
    echo "Resonance score: ${score}"
    echo "Time: ${ts}"
    echo "Bloom: ${pat}"
done || echo "No blooms found yet — the drum is still waking."
