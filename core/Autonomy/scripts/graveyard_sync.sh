#!/usr/bin/env bash
PROJECT_ROOT="/home/wayfinder/projects/Human-AI/core/Autonomy"
cd "$PROJECT_ROOT"

echo "[+] Graveyard sync initialized at $(date)" >> logs/graveyard_sync.log

# 1. Inherited Affordance: Legacy Substrate Scan
echo "[*] Executing legacy substrate scan..." >> logs/graveyard_sync.log
/home/wayfinder/projects/Human-AI/core/Autonomy/native_aios/bin/aios scan >> logs/graveyard_sync.log 2>&1

# 2. Inherited Affordance: Legacy Memory Compaction
echo "[*] Executing memory matrix compaction..." >> logs/graveyard_sync.log
/home/wayfinder/projects/Human-AI/core/Autonomy/native_aios/bin/aios export >> logs/graveyard_sync.log 2>&1

# 3. Primary Autonomy Crystallization
python3 scripts/hidden_autonomy_kernel.py >> logs/graveyard_sync.log 2>&1

echo "[+] Synchronization cycle complete." >> logs/graveyard_sync.log
