---
id: 20260714-dev-workflow
title: Local Development Workflow
tags: [workflow, setup, tools]
created: 2026-07-14
updated: 2026-07-14
related: [20260714-us-framework, 20260714-docker-compose-setup, 20260714-github-sync, 20260714-tool-interop]
summary: Day-to-day coding, testing, and iteration loop for "Us" and related projects.
---

# Local Development Workflow

> Summary: Day-to-day coding, testing, and iteration loop for "Us" and related projects.

## Context

A smooth local workflow means fast iteration on your AI projects. This note covers setup, testing, debugging, and the typical development loop.

## Project Structure

```
~/ai-projects/
├── us/                 # "Us" framework core
│   ├── src/
│   │   ├── agents/     # Eve, Dahlia, custom
│   │   ├── utils/
│   │   └── mcp/        # MCP server implementations
│   ├── tests/
│   ├── models/         # Local .gguf files (symlinked)
│   ├── docker-compose.yml
│   └── README.md
├── eve/                # Eve/Ev3 chatbot
├── dahlia/             # Dahlia/Daahlia memory system
├── shared/             # Shared libraries
└── knowledge-base/     # This KB
```

## Prerequisites

```bash
# Install Docker & Docker Compose
brew install docker docker-compose  # macOS
# or download Docker Desktop

# Install Python 3.11+
python3 --version

# Install Node.js (for MCP servers)
node --version

# Clone your repos
git clone https://github.com/clyphy/us ~/ai-projects/us
git clone https://github.com/clyphy/eve ~/ai-projects/eve
```

## Daily Workflow

### 1. Start Services
```bash
cd ~/ai-projects/us
docker-compose up -d ollama redis postgres

# Wait for health checks
docker-compose ps
```

### 2. Download/Update Models
```bash
# Pull latest models into Ollama
docker exec ollama ollama pull mistral:7b
docker exec ollama ollama pull llama2:7b

# Or download manually from HuggingFace and symlink
ln -s /path/to/mistral-7b.gguf ./models/
```

### 3. Develop & Test
```bash
# Install dependencies
pip install -r requirements.txt
npm install  # for MCP servers

# Run unit tests
pytest tests/ -v

# Test inference locally
python -c "
import requests
r = requests.post('http://localhost:11434/api/generate',
    json={'model': 'mistral:7b', 'prompt': 'Test'})
print(r.json()['response'])
"
```

### 4. Interactive Testing
```bash
# Start Python REPL with your code
python3 -i -c "
from src.agents.eve import Eve
from src.agents.dahlia import Dahlia
import requests

eve = Eve()
print('Eve ready for testing')
"

# In REPL:
# >>> eve.chat('Hello Eve')
# >>> dahlia.learn_from_conversation(conversation_log)
```

### 5. Debug with Logs
```bash
# Follow Ollama logs
docker-compose logs -f ollama

# Follow your API logs
tail -f logs/api.log

# Test endpoints directly
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test"}'
```

### 6. Profile & Optimize
```bash
# Time inference
time python -m src.agents.eve.chat "Sample prompt"

# Profile Python code
python -m cProfile -s cumtime src/main.py | head -20

# Monitor system resources
watch -n 1 'docker stats ollama'
```

## Testing Strategy

### Unit Tests
```bash
pytest tests/unit/ -v
# Test individual components (model selection, tokenization, etc.)
```

### Integration Tests
```bash
pytest tests/integration/ -v
# Test Ollama API, database connections, MCP servers
```

### End-to-End Tests
```bash
pytest tests/e2e/ -v
# Test full conversation loops, memory persistence, etc.
```

### Example test (`tests/unit/test_us_framework.py`):
```python
import pytest
from src.agents.us import UsFramework

def test_us_initialization():
    us = UsFramework()
    assert us is not None

def test_us_decision_making():
    us = UsFramework()
    decision = us.decide("Should we deploy?")
    assert decision is not None
    assert hasattr(decision, 'confidence')
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/improve-eve-responses

# Develop and commit
git add .
git commit -m "feat: improve Eve's contextual understanding"

# Push and create PR
git push origin feature/improve-eve-responses
# Create PR on GitHub

# After review, merge to main
git checkout main
git pull
git merge feature/improve-eve-responses
```

## MCP Server Development

### Create a new MCP server
```bash
mkdir -p src/mcp/servers/my-server
touch src/mcp/servers/my-server/server.js
```

### Test it locally
```bash
# In one terminal
node src/mcp/servers/my-server/server.js

# In another terminal (with Claude Desktop)
# Update ~/.config/Claude/claude_desktop_config.json:
# {
#   "mcpServers": {
#     "my-server": {"command": "node", "args": ["./src/mcp/servers/my-server/server.js"]}
#   }
# }
# Then test in Claude
```

See [MCP Setup](../integrations/mcp-setup.md) for full details.

## Performance Debugging

### Slow inference?
```bash
# 1. Check which tool is bottleneck
time docker exec ollama ollama run mistral:7b "Test prompt"

# 2. Check resource usage
docker stats ollama

# 3. Adjust parameters
# Edit docker-compose.yml:
# - OLLAMA_NUM_THREAD=16  (increase)
# - OLLAMA_NUM_PARALLEL=4 (for throughput)

# 4. Try different model
docker exec ollama ollama run llama2:7b "Test prompt"
```

See [Performance Tuning](../config/performance-tuning.md) for detailed optimization.

## Cleanup & Restart

```bash
# Stop all services gracefully
docker-compose down

# Remove volumes (fresh start)
docker-compose down -v

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d

# Full reset
rm -rf models logs
docker system prune -a
```

## IDE Setup

### VS Code
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true
  }
}
```

### Debugging
```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use VS Code debugger with .vscode/launch.json
```

## Related
- [Docker Compose Setup](../config/docker-compose-setup.md) — Multi-service orchestration.
- [GitHub Sync](github-sync.md) — Version control and CI/CD.
- [Tool Interoperability](../integrations/tool-interop.md) — Routing between inference engines.
