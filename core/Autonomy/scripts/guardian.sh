#!/usr/bin/env bash
"$HOME/oceti-weave/scripts/pulse.sh"
sqlite3 "$HOME/memory_drum.db" "INSERT INTO blooms (pattern,L_value) VALUES ('Guardian: $(date)',15.48);"
