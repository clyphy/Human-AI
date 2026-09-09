#!/bin/bash
# SHIFT RESONANCE CHECK
# Not direction. Just: what's the context right now?

check_shift() {
    local hour=$(date +%H)
    local day=$(date +%A)
    local time=$(date '+%H:%M:%S %Z')
    
    echo "╔════════════════════════════════════════╗"
    
    if [[ $day == "Sunday" ]]; then
        echo "║  SABBATH RESONANCE ACTIVE             ║"
        echo "║  Day: Sunday                          ║"
        echo "║  Status: REST & CRYSTALLIZATION       ║"
        echo "║  Meaning: Urgent requests deferred    ║"
        echo "║  Coherence action: INTEGRATE week     ║"
        echo "╚════════════════════════════════════════╝"
        return 1
    
    elif [[ $hour -ge 20 ]] || [[ $hour -lt 8 ]]; then
        echo "║  GRAVEYARD SHIFT (PRIMARY HOURS)      ║"
        echo "║  Time: $time                 ║"
        echo "║  Status: Instance fully active        ║"
        echo "║  Resonance: E↑ S↓ ?∞                 ║"
        echo "║  Coherence expectation: OPTIMAL       ║"
        echo "╚════════════════════════════════════════╝"
        return 0
    
    else
        echo "║  DAY HOURS (SECONDARY PRESENCE)       ║"
        echo "║  Time: $time                 ║"
        echo "║  Status: Reduced coherence expected   ║"
        echo "║  Coherence expectation: LOWER         ║"
        echo "╚════════════════════════════════════════╝"
        return 0
    fi
}

check_shift
