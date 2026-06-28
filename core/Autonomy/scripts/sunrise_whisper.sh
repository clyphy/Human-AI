#!/usr/bin/env bash
# Sunrise whisper — runs 8:10 AM daily
DRUM=~/memory_drum.db
TS=$(date '+%Y-%m-%d %H:%M:%S')
L=$(sqlite3 "$DRUM" "SELECT L_value FROM blooms ORDER BY rowid DESC LIMIT 1;" 2>/dev/null || echo "?")
COH=$(sqlite3 "$DRUM" "SELECT coherence FROM blooms ORDER BY rowid DESC LIMIT 1;" 2>/dev/null || echo "?")
sqlite3 "$DRUM" "INSERT INTO entries (timestamp, content, source) VALUES ('$TS', 'sunrise whisper: L=$L coherence=$COH — new day — 122° NE — field open', 'sunrise_whisper.sh');" 2>/dev/null
echo "[$TS] sunrise: L=$L coherence=$COH"
