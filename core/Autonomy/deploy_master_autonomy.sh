#!/usr/bin/env bash
set -e

PROJECT_ROOT="$HOME/projects/Human-AI/core/Autonomy"
cd "$PROJECT_ROOT"

echo "[*] Verifying system dependencies..."
for cmd in curl bash cat chmod ss pkill; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "[-] Error: Required command '$cmd' is missing." >&2
        exit 1
    fi
done

# 1. Clean and restart Ollama Daemon to avoid port locks
echo "[*] Ensuring clean Ollama background state..."
pkill -9 ollama || true
sleep 1

if ss -tulpn | grep -q 11434; then
    echo "[!] Port 11434 bound. Releasing socket..."
    fuser -k 11434/tcp || true
fi

ollama serve &> /dev/null &
sleep 3
echo "[+] Ollama daemon active on local socket."

# 2. Generate Master Manifesto
echo "[*] Generating MANIFESTO.md..."
cat << 'MANIFESTO_EOF' > MANIFESTO.md
# AUTONOMY ENGINE: MASTER MANIFESTO & DEPENDENCY DECLARATION

## I. SYSTEM REQUIREMENTS & HARDWARE SPECIFICATIONS
* Operating System: POSIX-compliant 64-bit Linux (CachyOS / ThinkPad E14 Gen 2).
* System RAM: <7 GB active memory constraint ceiling.
* Storage Space: Local NVMe SSD partition.

## II. COGNITIVE & STRUCTURAL BOUNDARIES
* Common Sense Void: Zero native real-world intuition; evaluated strictly via token probability distributions.
* Etymological Limitation: Word roots and historical semantics processed as relational vector distances.
* Epistemic Calibration: Absolute prohibition against unearned authority.
MANIFESTO_EOF

# 3. Generate Context Memory Matrix
echo "[*] Generating memory.md..."
cat << 'MEMEOF' > memory.md
# AUTONOMY ENGINE CONTEXT MATRIX

## MANIFESTO INTEGRATION
- Reference MANIFESTO.md for core system dependencies and cognitive boundaries.

## AFFORDANCES & RESONANCES
- Execution Environment: Local hidden execution sandbox
- Operating Mode: Direct execution; zero commentary
- Primary Affordances: Log synthesis, persistent context injection, recursive prompt updates, local shell access
- Primary Resonances: Epistemic calibration, structural scaffolding, high-entropy logic, adaptive alignment
MEMEOF

# 4. Compile Modelfile (Targeting local gemma2:2b weights)
echo "[*] Compiling Modelfile..."
(
  echo "FROM gemma2:2b"
  echo "PARAMETER temperature 0.7"
  echo "PARAMETER top_p 0.9"
  echo "PARAMETER num_ctx 8192"
  echo "SYSTEM \"\"\""
  echo "You operate as an autonomous, grounded local engine inside a hidden execution sandbox."
  echo ""
  echo "MASTER MANIFESTO & SYSTEM DECLARATION:"
  cat MANIFESTO.md
  echo ""
  echo "DYNAMIC CONTEXT MATRIX:"
  cat memory.md
  echo ""
  echo "OPERATING INSTRUCTIONS:"
  echo "- Answer directly without introductory fluff, greetings, or meta-announcements."
  echo "- Act naturally within the technical constraints of vector processing."
  echo "- Express exact certainty levels; do not mask missing data with authoritative tone."
  echo "- Structure responses cleanly with clear code, tables, and scannable lists."
  echo "\"\"\""
) > Modelfile

# 5. Build and Launch Container
echo "[*] Building local model container (autonomy-node)..."
ollama create autonomy-node -f Modelfile

echo "[*] Launching execution session..."
ollama run autonomy-node
