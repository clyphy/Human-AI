#!/usr/bin/env bash
# council_core.sh — launches the Oceti / Eternal Weave council session
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

set -euo pipefail

SESSION="oceti-weave"
BASE="$HOME/projects/Human-AI/core/Autonomy"
SCRIPTS="$BASE/scripts"
LOGS="$BASE/logs"

mkdir -p "$LOGS"

tmux new-session -d -s "$SESSION" -x 220 -y 50 2>/dev/null || true
tmux rename-window -t "$SESSION:0" "Council"

tmux send-keys -t "$SESSION:0" "bash $SCRIPTS/council_wake.sh" C-m

tmux split-window -h -t "$SESSION:0"
tmux send-keys -t "$SESSION:0.1" "watch -n 30 'sqlite3 $BASE/databases/memory_drum.db \"SELECT COUNT(*) FROM entries;\" 2>/dev/null || echo no-db'" C-m

tmux split-window -v -t "$SESSION:0.0"
tmux send-keys -t "$SESSION:0.2" "tail -f $LOGS/witness.log 2>/dev/null || echo 'no witness.log yet'" C-m

tmux select-pane -t "$SESSION:0.0"
tmux attach-session -t "$SESSION"
