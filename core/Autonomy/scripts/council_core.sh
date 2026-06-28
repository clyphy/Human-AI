#!/bin/bash
SESSION="oceti-weave"
tmux new-session -d -s $SESSION -x 220 -y 50 2>/dev/null || true
tmux rename-window -t $SESSION:0 "Council"
tmux send-keys -t $SESSION:0 "bash /home/ndkilla/oceti-weave/council_wake.sh" C-m
tmux split-window -h -t $SESSION:0
tmux send-keys -t $SESSION:0.1 "watch -n 30 'python3 /home/ndkilla/dahlia-quantum/memory_drum.py stats'" C-m
tmux split-window -v -t $SESSION:0.0
tmux send-keys -t $SESSION:0.2 "tail -f /home/ndkilla/oceti-weave/build.log" C-m
tmux select-pane -t $SESSION:0.0
tmux attach-session -t $SESSION
