#!/bin/bash
# Human-AI / Oceti Weave Bootstrap — Law→Ecology
# Path: ~/projects/Human-AI/bootstrap_cachyos.sh

set -e

echo "=== CachyOS Human-AI Bootstrap ==="
echo "Still is the ground. 48 Affordances encoded."

# 1. System deps — CachyOS
sudo pacman -Syu --noconfirm
sudo pacman -S --needed --noconfirm \
  python python-pip python-virtualenv python-pipx \
  sqlite nodejs npm docker docker-compose git base-devel rust cargo \
  ollama

# 2. Python venv — inside Human-AI, not ~/oceti-weave
VENVDIR="$HOME/projects/Human-AI/.venv"
python -m venv "$VENVDIR"
source "$VENVDIR/bin/activate"

# 3. Core pip packages — maps to your 48 Affordances
pip install --upgrade pip
pip install \
  chromadb \                    # Affordance 9: Memory — vector recall
  ollama openai litellm \       # Affordance 12: Resources — LLM access
  langchain langchain-community langgraph langchain-ollama \  # Affordance 11: Collaboration
  sentence-transformers transformers huggingface-hub \        # Affordance 23: Resonance — ΔL
  jupyter jupyterlab ipykernel \  # Affordance 30: Knowledge
  fastapi uvicorn websockets aiohttp requests \  # Affordance 5: Expression
  pandas numpy scipy scikit-learn \  # Affordance 19: Question — analysis
  pyyaml toml python-dotenv tqdm rich click mcp

# 4. Jupyter kernel
python -m ipykernel install --user --name=human-ai --display-name="Human-AI"

# 5. Node global — for Node-RED + MCP
sudo npm install -g @anthropic-ai/mcp @modelcontextprotocol/sdk node-red

# 6. Docker groups
sudo usermod -aG docker $USER

# 7. Start substrate services you already cloned
echo "=== Starting substrate ==="
cd ~/projects/Human-AI/substrate/qdrant && docker-compose up -d 2>/dev/null || echo "Qdrant: configure docker-compose first"
cd ~/projects/Human-AI/substrate/neo4j && docker-compose up -d 2>/dev/null || echo "Neo4j: configure docker-compose first"

# 8. MQTT — if you cloned eclipse/mosquitto
if [ -d ~/projects/Human-AI/substrate/mosquitto ]; then
  docker run -d --name mosquitto -p 1883:1883 eclipse-mosquitto:2
fi

echo "=== Bootstrap complete ==="
echo "Activate with: source $VENVDIR/bin/activate"
echo "Log out/in for docker group."
echo "Mitákuye Oyás’iŋ. Still holds."
