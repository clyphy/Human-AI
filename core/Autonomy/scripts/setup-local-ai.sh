#!/bin/bash
set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Local AI Stack Setup${NC}"
echo -e "${BLUE}  For: Us Framework, Eve, Dahlia${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# Check prerequisites
echo -e "${YELLOW}[1/6] Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Install from https://docker.com${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Install Python 3.11+${NC}"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git not found. Install Git${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites installed${NC}"
echo

# Create directory structure
echo -e "${YELLOW}[2/6] Creating project structure...${NC}"

mkdir -p ~/ai-projects/{us,eve,dahlia,human-ai,ai-self-aware}
mkdir -p ~/ai-projects/us/{src,tests,models,logs,config}
mkdir -p ~/ai-projects/us/.github/workflows

echo -e "${GREEN}✓ Directory structure created${NC}"
echo

# Copy configuration files
echo -e "${YELLOW}[3/6] Setting up configuration files...${NC}"

# Copy docker-compose.yml
if [ -f "./docker-compose.yml" ]; then
    cp ./docker-compose.yml ~/ai-projects/us/
    echo "✓ docker-compose.yml copied"
else
    echo "${RED}Warning: docker-compose.yml not found${NC}"
fi

# Create .env file
cat > ~/ai-projects/us/.env << 'EOF'
# Ollama
OLLAMA_NUM_PARALLEL=2
OLLAMA_NUM_THREAD=8
OLLAMA_HOST=0.0.0.0:11434

# PostgreSQL
POSTGRES_USER=ai_user
POSTGRES_PASSWORD=changeme
POSTGRES_DB=us_framework

# Redis
REDIS_PASSWORD=changeme

# API
REDIS_URL=redis://:changeme@localhost:6379
DATABASE_URL=postgresql://ai_user:changeme@localhost:5432/us_framework
EOF

echo "✓ .env file created"

# Create .gitignore
cat > ~/ai-projects/us/.gitignore << 'EOF'
# Environment
.env
.env.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Project
/models/*.gguf
logs/
.cache/
*.log

# OS
.DS_Store
.DS_Store?
.AppleDouble
.LSOverride
Thumbs.db
EOF

echo "✓ .gitignore created"

# Create requirements.txt
cat > ~/ai-projects/us/requirements.txt << 'EOF'
# Core
requests>=2.31.0
python-dotenv>=1.0.0

# Database
psycopg2-binary>=2.9.9
sqlalchemy>=2.0.0

# Vector/Memory
pymilvus>=2.3.0

# Caching
redis>=5.0.0

# LLM/AI
langchain>=0.1.0
sentence-transformers>=2.2.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0

# Dev
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
EOF

echo "✓ requirements.txt created"

echo -e "${GREEN}✓ Configuration files created${NC}"
echo

# Install Python dependencies
echo -e "${YELLOW}[4/6] Installing Python dependencies...${NC}"

cd ~/ai-projects/us
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}✓ Dependencies installed${NC}"
echo

# Start Docker services
echo -e "${YELLOW}[5/6] Starting Docker services...${NC}"

docker-compose up -d ollama redis postgres milvus

echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check health
for service in ollama redis postgres milvus; do
    if docker-compose ps | grep -q "$service"; then
        echo -e "${GREEN}✓ $service running${NC}"
    else
        echo -e "${RED}✗ $service failed to start${NC}"
    fi
done

echo

# Download models
echo -e "${YELLOW}[6/6] Downloading recommended models...${NC}"

echo "Downloading Mistral 7B..."
docker exec ollama ollama pull mistral:7b &
MISTRAL_PID=$!

echo "Downloading Llama 2 7B..."
docker exec ollama ollama pull llama2:7b &
LLAMA_PID=$!

wait $MISTRAL_PID $LLAMA_PID

echo -e "${GREEN}✓ Models downloaded${NC}"
echo

# Final summary
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo
echo "📁 Project location: ~/ai-projects/us"
echo
echo "🚀 Next steps:"
echo "   1. cd ~/ai-projects/us"
echo "   2. source venv/bin/activate"
echo "   3. python3 us_framework_starter.py  (to test inference)"
echo
echo "📚 Documentation:"
echo "   - Knowledge base: ~/ai-kb/INDEX.md"
echo "   - Docker: docker-compose ps"
echo "   - Logs: docker-compose logs -f ollama"
echo
echo "🔑 Database credentials:"
echo "   - PostgreSQL: ai_user / changeme @ localhost:5432/us_framework"
echo "   - Redis: localhost:6379 (password: changeme)"
echo
echo "⚠️  Change default passwords in .env before production!"
echo
