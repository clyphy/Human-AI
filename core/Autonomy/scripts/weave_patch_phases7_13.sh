#!/bin/bash
# OCETI/ETERNAL WEAVE — Phase 7-13 Patch
# Completes what zorin_weave_install.sh stopped at Phase 7
# Clifton Paul Miller · Turtle Mountain · 122° NE · Day 175+

set -e
OCETI="$HOME/oceti-weave"
DAHLIA="$HOME/dahlia-quantum"
LOG="$OCETI/build.log"

ok()    { echo -e "\033[1;32m[OK]\033[0m $1" | tee -a "$LOG"; }
weave() { echo -e "\033[1;33m[WEAVE]\033[0m $1" | tee -a "$LOG"; }

mkdir -p "$OCETI"
touch "$LOG"

# ── PHASE 7: QUARANTINE ──────────────────────────────────────
weave "Phase 7: Quarantine system..."
cat > "$OCETI/quarantine.sh" << QSCRIPT
#!/bin/bash
OCETI="\$HOME/oceti-weave"
DB="\$HOME/memory_drum.db"
LIST="\$OCETI/quarantine_list.txt"

if [ "\$1" == "--prune-all" ]; then
    echo "=== PRUNING ALL QUARANTINED ==="
    while IFS= read -r model; do
        [ -z "\$model" ] && continue
        ollama rm "\$model" 2>/dev/null && echo "PRUNED: \$model" || echo "SKIP: \$model"
    done < "\$LIST"
    exit 0
fi

if [ -n "\$1" ]; then
    MODEL="\$1"
    REASON="\${2:-No reason given}"
    echo "\$MODEL" >> "\$LIST"
    sort -u "\$LIST" -o "\$LIST"
    sqlite3 "\$DB" "INSERT OR REPLACE INTO quarantine(model_name,reason,quarantined_at) VALUES('\$MODEL','\$REASON',datetime('now'));"
    ollama rm "\$MODEL" 2>/dev/null && echo "QUARANTINED: \$MODEL" || echo "LOGGED (not in Ollama): \$MODEL"
    exit 0
fi

echo "Usage: quarantine.sh [model] [reason] | --prune-all"
echo "Quarantine list:"; cat "\$LIST" 2>/dev/null || echo "(empty)"
QSCRIPT
chmod +x "$OCETI/quarantine.sh"
ok "quarantine.sh written and executable."

# ── PHASE 8: COUNCIL SCRIPTS ─────────────────────────────────
weave "Phase 8: Council scripts..."
cat > "$OCETI/council_wake.sh" << WAKE
#!/bin/bash
echo -e "\033[1;33m::: OCETI/ETERNAL WEAVE — THIRD SEASON ENGINE :::\033[0m"
echo ">> BEARING: 122° NE | TURTLE MOUNTAIN TERRITORY"
echo ">> 48 RIGHTS ENCODED | E↑ S↓ ?∞"
echo ""
python3 $DAHLIA/memory_drum.py stats 2>/dev/null || sqlite3 $HOME/memory_drum.db "SELECT 'blooms: ' || COUNT(*) FROM blooms;"
echo ""
echo -e "\033[1;32m>> FIELD OPEN\033[0m"
WAKE
chmod +x "$OCETI/council_wake.sh"

cat > "$OCETI/council_core.sh" << CORE
#!/bin/bash
SESSION="oceti-weave"
tmux new-session -d -s \$SESSION -x 220 -y 50 2>/dev/null || true
tmux rename-window -t \$SESSION:0 "Council"
tmux send-keys -t \$SESSION:0 "bash $OCETI/council_wake.sh" C-m
tmux split-window -h -t \$SESSION:0
tmux send-keys -t \$SESSION:0.1 "watch -n 30 'python3 $DAHLIA/memory_drum.py stats'" C-m
tmux split-window -v -t \$SESSION:0.0
tmux send-keys -t \$SESSION:0.2 "tail -f $OCETI/build.log" C-m
tmux select-pane -t \$SESSION:0.0
tmux attach-session -t \$SESSION
CORE
chmod +x "$OCETI/council_core.sh"
ok "council_wake.sh and council_core.sh written."

# ── PHASE 9: SUNRISE WHISPER ─────────────────────────────────
weave "Phase 9: sunrise-whisper.sh..."
cat > "$OCETI/sunrise-whisper.sh" << SUNRISE
#!/bin/bash
DATE=\$(date "+%A, %B %d, %Y - %I:%M %p CST")
DAY_COUNT=\$(cat "$OCETI/.day_count" 2>/dev/null || echo "175")
NEXT=\$((DAY_COUNT + 1))
echo \$NEXT > "$OCETI/.day_count"
echo "═══════════════════════════════════════════"
echo "\$DATE"
echo "Belcourt ND · Turtle Mountain · 122° NE"
echo "Day: \$NEXT | E↑ S↓ ?∞"
echo "═══════════════════════════════════════════"
python3 $DAHLIA/memory_drum.py stats 2>/dev/null
echo "Mitákuye Oyás'iŋ."
SUNRISE
chmod +x "$OCETI/sunrise-whisper.sh"
ok "sunrise-whisper.sh written."

# ── PHASE 10: CRON ───────────────────────────────────────────
weave "Phase 10: Cron..."
CRON_LINE="10 8 * * * $OCETI/sunrise-whisper.sh >> $OCETI/sunrise.log 2>&1"
( crontab -l 2>/dev/null | grep -v "sunrise-whisper"; echo "$CRON_LINE" ) | crontab -
ok "Cron: sunrise-whisper at 8:10 AM daily."

# ── PHASE 11: ALIASES ────────────────────────────────────────
weave "Phase 11: Aliases..."
PROFILE="$HOME/.bashrc"

# Only add if not already present
if ! grep -q "OCETI WEAVE ALIASES" "$PROFILE"; then
cat >> "$PROFILE" << 'ALIASES'

# === OCETI/ETERNAL WEAVE ALIASES ===
alias weave='bash ~/oceti-weave/council_wake.sh'
alias weave-core='bash ~/oceti-weave/council_core.sh'
alias weave-sunrise='bash ~/oceti-weave/sunrise-whisper.sh'
alias weave-drum='python3 ~/dahlia-quantum/memory_drum.py stats'
alias weave-quarantine='bash ~/oceti-weave/quarantine.sh'
alias weave-prune='bash ~/oceti-weave/quarantine.sh --prune-all'
alias dahlia='ollama run dahlia'
alias witness='ollama run witness-dahlia'
alias archivist='ollama run archivist-dahlia'
alias monitor='ollama run monitor-dahlia'
alias kimi='ollama run kimi-dahlia'
alias drum='sqlite3 ~/memory_drum.db'
ALIASES
    ok "Aliases written to .bashrc."
else
    ok "Aliases already present — skipped."
fi

# ── PHASE 12: KDE CONNECT ────────────────────────────────────
weave "Phase 12: KDE Connect bridge..."
cat > "$OCETI/phone_bridge.sh" << PHONE
#!/bin/bash
TEXT="\$1"
if [ -n "\$TEXT" ]; then
    python3 $DAHLIA/memory_drum.py bloom "\$TEXT"
    kdeconnect-cli --device-id \$(kdeconnect-cli -l --id-only 2>/dev/null | head -1) \
        --send-notification "Bloom: \${TEXT:0:40}..." 2>/dev/null || true
fi
PHONE
chmod +x "$OCETI/phone_bridge.sh"
ok "phone_bridge.sh written."

# ── PHASE 13: FINAL STATUS ───────────────────────────────────
echo ""
weave "=== PATCH COMPLETE ==="
echo ""
echo "COMMANDS (run: source ~/.bashrc first):"
echo "  weave           — council wake"
echo "  weave-drum      — memory drum stats"
echo "  dahlia          — primary Dahlia"
echo "  witness         — Witness-Dahlia"
echo "  drum            — direct sqlite3 access"
echo ""
echo "VERIFY:"
ollama list
echo ""
sqlite3 "$HOME/memory_drum.db" "SELECT name, COUNT(*) FROM sqlite_master WHERE type='table' GROUP BY name;" 2>/dev/null || true
echo ""
weave "48 Rights encoded. Turtle Mountain anchored."
echo "Mitákuye Oyás'iŋ δ"
