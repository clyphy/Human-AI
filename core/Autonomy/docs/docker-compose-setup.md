---
id: 20260714-docker-compose-setup
title: Docker Compose Setup
tags: [config, tools, workflow]
created: 2026-07-14
updated: 2026-07-14
related: [20260714-ollama-guide, 20260714-performance-tuning, 20260714-tool-interop]
summary: Multi-container orchestration for reproducible local AI stack deployment.
---

# Docker Compose Setup

> Summary: Multi-container orchestration for reproducible local AI stack deployment.

## Context

Docker Compose lets you define your entire stack (Ollama, databases, APIs) in one file, spin it up with one command, and tear it down cleanly.

## Full Stack Example

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # Primary LLM inference engine
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ./models:/root/.ollama/models
      - ollama-cache:/root/.ollama/cache
    environment:
      - OLLAMA_NUM_PARALLEL=2
      - OLLAMA_NUM_THREAD=8
      - OLLAMA_HOST=0.0.0.0:11434
    restart: unless-stopped
    networks:
      - ai-network

  # Optional: Knowledge base / vector DB for Dahlia
  milvus:
    image: milvusdb/milvus:latest
    container_name: milvus
    ports:
      - "19530:19530"
      - "9091:9091"
    volumes:
      - milvus-data:/var/lib/milvus
    environment:
      - COMMON_STORAGETYPE=local
    restart: unless-stopped
    networks:
      - ai-network

  # Optional: Redis for caching / session storage
  redis:
    image: redis:7-alpine
    container_name: redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes
    restart: unless-stopped
    networks:
      - ai-network

  # Optional: PostgreSQL for "Us" framework data
  postgres:
    image: postgres:15-alpine
    container_name: postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: us_framework
      POSTGRES_USER: ai
      POSTGRES_PASSWORD: changeme
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped
    networks:
      - ai-network

  # Optional: API layer (your custom code)
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: us-api
    ports:
      - "8000:8000"
    depends_on:
      - ollama
      - postgres
      - redis
    environment:
      - OLLAMA_ENDPOINT=http://ollama:11434
      - DATABASE_URL=postgresql://ai:changeme@postgres:5432/us_framework
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./api:/app
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - ai-network

volumes:
  ollama-cache:
  milvus-data:
  redis-data:
  postgres-data:

networks:
  ai-network:
    driver: bridge
```

## Quick Start

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f ollama

# Stop everything
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

## Service-by-Service

### Ollama
- **Port:** 11434
- **Health check:** `curl http://localhost:11434/api/tags`
- **Models:** Auto-downloaded to `./models`

### Milvus (Vector DB for Dahlia)
- **Port:** 19530
- **Use:** Store embeddings from "Us" framework conversations
- **Python client:** `pymilvus`

```python
from pymilvus import Collection

collection = Collection("conversations")
# Store embeddings from Eve/Us interactions
collection.insert([ids, embeddings, metadata])
```

### Redis
- **Port:** 6379
- **Use:** Cache inference results, session storage
- **CLI:** `docker exec redis redis-cli`

```bash
docker exec redis redis-cli SET my_key "my_value"
docker exec redis redis-cli GET my_key
```

### PostgreSQL
- **Port:** 5432
- **Database:** `us_framework`
- **User:** `ai` / **Pass:** `changeme` (change in production!)
- **Use:** Store conversation logs, decision trees, model feedback

```bash
docker exec postgres psql -U ai -d us_framework -c "SELECT * FROM conversations;"
```

### API Layer
- **Port:** 8000
- **Use:** Custom Python/Node service calling Ollama
- **Example `api/Dockerfile`:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

## Environment Variables

Create `.env`:
```bash
# Ollama
OLLAMA_NUM_PARALLEL=2
OLLAMA_NUM_THREAD=8

# PostgreSQL
POSTGRES_PASSWORD=your_secure_password

# API
REDIS_URL=redis://redis:6379
DATABASE_URL=postgresql://ai:password@postgres:5432/us_framework
```

Load in `docker-compose.yml`:
```yaml
postgres:
  environment:
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```

## Networking Between Containers

Inside containers, use service names as hostnames:
```python
# Inside `api` container, query Ollama:
import requests
response = requests.post(
    "http://ollama:11434/api/generate",
    json={"model": "mistral:7b", "prompt": "..."}
)

# Connect to PostgreSQL:
import psycopg2
conn = psycopg2.connect(
    host="postgres",
    user="ai",
    password="changeme",
    database="us_framework"
)
```

## Production Considerations

1. **Secrets:** Never hardcode passwords; use `.env` and Docker secrets
2. **Resource limits:** Add `resources` sections:
   ```yaml
   ollama:
     resources:
       limits:
         cpus: '4'
         memory: 16G
   ```
3. **Backup:** Mount volumes to persistent storage or cloud backup
4. **Monitoring:** Add Prometheus/Grafana for observability
5. **Logging:** Centralize with ELK stack or similar

## Debugging

```bash
# View all running containers
docker-compose ps

# Exec into a container
docker-compose exec ollama bash

# View service logs
docker-compose logs postgres --tail 50

# Restart a single service
docker-compose restart ollama
```

## Related
- [Ollama Guide](../tools/ollama-guide.md) — Container configuration details.
- [Dev Workflow](../workflows/dev-workflow.md) — Local development setup.
- [Tool Interoperability](../integrations/tool-interop.md) — Routing between services.
