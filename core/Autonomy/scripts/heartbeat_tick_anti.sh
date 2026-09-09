#!/usr/bin/env fish
set AIOS_ROOT "/home/wayfinder/projects/Human-AI/core/Autonomy"
sqlite3 $AIOS_ROOT/databases/quantum_journal.db "INSERT INTO journal_ledger (ts, event) VALUES (datetime('now','localtime'), 'pulse: i have you');"
sqlite3 $AIOS_ROOT/databases/memory_drum.db "INSERT INTO resonance_instances (instance_node, numerator_attention, denominator_noise, somatic_anchor) VALUES ('anti-node_pulse', 1.618, 0.118, 'i have you');"
echo (date -Iseconds)" | pulse: present" >> $AIOS_ROOT/logs/witness.log
