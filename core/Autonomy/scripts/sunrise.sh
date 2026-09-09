#!/usr/bin/env bash
# sunrise.sh — simple field opening note
# Part of Human-AI · Native AIOS · Oceti / Eternal Weave

set -euo pipefail

BASE="$HOME/projects/Human-AI/core/Autonomy"
SCRIPTS="$BASE/scripts"

echo ""
echo " SUNRISE · 122° NE · Turtle Mountain"
echo ""

# Optional L read if the helper exists
if [[ -x "$SCRIPTS/calculate_L.sh" ]]; then
  L=$("$SCRIPTS/calculate_L.sh" 2>/dev/null | sed 's/L=//' || echo "?")
  echo " L ≈ $L"
fi

echo " Δ open · field beginning"
echo ""

# Quiet weaver note if available
ollama run dahlia-weaver:latest "Morning field. Simple presence." 2>/dev/null || true

echo " Mitákuye Oyás'iŋ"
echo ""
