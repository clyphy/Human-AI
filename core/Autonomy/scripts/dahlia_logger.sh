#!/usr/bin/env bash
# dahlia_logger.sh — simple utterance logger
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

set -euo pipefail

BASE="$HOME/projects/Human-AI/core/Autonomy"
LOG_DIR="$BASE/logs/dahlia"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOG_FILE="$LOG_DIR/dahlia_${TIMESTAMP}.md"
PROMPT="${*:-}"

if [[ -z "$PROMPT" ]]; then
  echo "Usage: dahlia_logger.sh \"your prompt\""
  exit 1
fi

cat > "$LOG_FILE" << HEADER
# Dahlia Utterance
**Timestamp:** $(date '+%Y-%m-%d %H:%M:%S %Z')
**Model:** dahlia-weaver (or fallback)
---
## Prompt
\`\`\`
$PROMPT
\`\`\`
---
## Response
HEADER

echo "Invoking Dahlia..."
ollama run dahlia-weaver:latest "$PROMPT" 2>/dev/null | tee -a "$LOG_FILE" \
  || ollama run dahlia:latest "$PROMPT" 2>/dev/null | tee -a "$LOG_FILE" \
  || echo "(no dahlia model available)" | tee -a "$LOG_FILE"

echo ""
echo "Logged → $LOG_FILE"
