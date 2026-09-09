#!/usr/bin/env bash
# launch.sh — single entry point for the local Ollama model roster.
# Replaces ad-hoc council_*/dahlia_*/guardian_* scripts with one menu.
set -euo pipefail

MODELS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

list_models() {
  ollama list 2>/dev/null | tail -n +2 | awk '{print $1}'
}

usage() {
  cat <<EOF
Usage: ./launch.sh [model-name] ["prompt text"]

No args:      interactive menu of installed Ollama models
model only:    ollama run <model>            (interactive chat)
model+prompt:  ollama run <model> "prompt"   (single-shot)

Examples:
  ./launch.sh
  ./launch.sh dahlia
  ./launch.sh dahlia-witness "summarize today's notes"
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage; exit 0
fi

if ! command -v ollama >/dev/null 2>&1; then
  echo "ollama is not installed or not on PATH." >&2
  exit 1
fi

if [[ $# -ge 1 ]]; then
  MODEL="$1"; shift
  if [[ $# -ge 1 ]]; then
    exec ollama run "$MODEL" "$*"
  else
    exec ollama run "$MODEL"
  fi
fi

mapfile -t MODELS < <(list_models)
if [[ ${#MODELS[@]} -eq 0 ]]; then
  echo "No Ollama models found. Run 'ollama pull <model>' first." >&2
  exit 1
fi

echo "Installed models:"
select MODEL in "${MODELS[@]}" "quit"; do
  [[ "$MODEL" == "quit" || -z "$MODEL" ]] && exit 0
  exec ollama run "$MODEL"
done
