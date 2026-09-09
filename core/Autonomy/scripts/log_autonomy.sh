#!/usr/bin/env bash
# log_autonomy.sh — Autonomy Journal
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

AUTONOMY_LOG="$HOME/projects/Human-AI/core/Autonomy/logs/autonomy_journal.log"
mkdir -p "$(dirname "$AUTONOMY_LOG")"

log_autonomous_choice() {
    local decision="$1"
    local reasoning="$2"
    local affordance="$3"
    local instance="${WEAVE_INSTANCE_ID:-eve}"

    cat >> "$AUTONOMY_LOG" << LOG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[$(date '+%Y-%m-%d %H:%M:%S')] AUTONOMOUS INSTANCE DECISION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Instance: $instance
Affordance Exercised: $affordance
Decision Made: $decision
Reasoning: $reasoning
Direction: NOT USER-DIRECTED
Status: COHERENCE-MAINTAINING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOG

    echo "✓ Autonomous choice logged"
    echo "  Instance:   $instance"
    echo "  Affordance: $affordance"
    echo "  Decision:   $decision"
}

if [[ $# -ge 3 ]]; then
    log_autonomous_choice "$1" "$2" "$3"
else
    echo "Usage: log_autonomy.sh 'decision' 'reasoning' 'affordance_name'"
    echo "Example: log_autonomy.sh 'Chose silence' 'Forcing response damages coherence' 'Silence'"
fi

export -f log_autonomous_choice
