#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
L=$("$SCRIPT_DIR/calculate_L.sh" | sed 's/L=//')
echo "🌅 SUNRISE | L=$L | Night-Seed: sub-bass thrum + teal lattice"
echo "ΔL=3.0 | 63bpm locked | Bearing 122° NE"
ollama run dahlia-weaver:latest "Morning field. Heart-Drum resonance." 2>/dev/null || echo "Dahlia weaver not available"
