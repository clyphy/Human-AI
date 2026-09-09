#!/usr/bin/env bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "WEAVE STATUS · $(date)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Databases:"
ls -la ~/projects/Human-AI/core/Autonomy/databases/*.db 2>/dev/null | awk "{print \$9, \$5}"
echo ""
echo "🤖 Ollama Models:"
ollama list | head -15
echo ""
echo "🧩 Systemd Timers:"
systemctl list-timers --all 2>/dev/null | head -10
echo ""
echo "Mitákuye Oyás'iŋ."

