#!/usr/bin/env bash
# AUTOBUILD: One-Shot Sanctuary Builder (Bash Edition)
# Wayfinder, this script brings your Autonomy core to a known state.
# It is safe to run multiple times. It will not overwrite your data.

set -e

SCRIPT_VERSION="1.0.0"
BUILD_TIME=$(date "+%Y-%m-%d %H:%M:%S %Z")
HOSTNAME=$(hostname)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 AUTOBUILD · SANCTUARY BUILDER"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Version: $SCRIPT_VERSION"
echo "  Timestamp: $BUILD_TIME"
echo "  Host: $HOSTNAME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ─────────────────────────────────────────────
# [1/6] ENVIRONMENT CHECKS
# ─────────────────────────────────────────────
echo "[1/6] 🌍 Environment Checks"

# Check for Bash
if [ -n "$BASH" ]; then
    echo "  ✓ Bash detected (version ${BASH_VERSION})"
else
    echo "  ⚠  Not running in Bash. Some features may not work."
fi

# Check for Ollama
if command -v ollama &> /dev/null; then
    OLLAMA_VER=$(ollama --version 2>/dev/null || echo "installed")
    echo "  ✓ Ollama found: $OLLAMA_VER"
else
    echo "  ⚠  Ollama not found in PATH. Please install Ollama."
fi

# Check for sqlite3
if command -v sqlite3 &> /dev/null; then
    SQLITE_VER=$(sqlite3 --version | head -1)
    echo "  ✓ sqlite3 found: $SQLITE_VER"
else
    echo "  ⚠  sqlite3 not found. Please install sqlite3."
fi

# Check for systemd
if command -v systemctl &> /dev/null; then
    echo "  ✓ systemd detected"
fi

# ─────────────────────────────────────────────
# [2/6] DIRECTORY STRUCTURE
# ─────────────────────────────────────────────
echo ""
echo "[2/6] 📁 Core Directories"

PROJECT_ROOT="$HOME/projects/Human-AI/core"
AUTONOMY_ROOT="$PROJECT_ROOT/Autonomy"
DATABASES_DIR="$AUTONOMY_ROOT/databases"
SCRIPTS_DIR="$AUTONOMY_ROOT/scripts"
WEAVE_CORE="$AUTONOMY_ROOT/weave_core"
LABS_DIR="$AUTONOMY_ROOT/labs"
LOGS_DIR="$HOME/logs"
MODELFILES_DIR="$HOME/oceti-weave/modelfiles"

for dir in "$PROJECT_ROOT" "$AUTONOMY_ROOT" "$DATABASES_DIR" "$SCRIPTS_DIR" "$WEAVE_CORE" "$LABS_DIR" "$LOGS_DIR" "$MODELFILES_DIR"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir exists"
    else
        echo "  ⚠  Creating $dir"
        mkdir -p "$dir"
        if [ $? -eq 0 ]; then
            echo "  ✓ Created $dir"
        else
            echo "  ✗ Failed to create $dir"
        fi
    fi
done

# ─────────────────────────────────────────────
# [3/6] DATABASES & SYMLINKS
# ─────────────────────────────────────────────
echo ""
echo "[3/6] 🗄  Databases & Symlinks"

# Memory Drum (primary)
MEMORY_DRUM="$DATABASES_DIR/memory_drum.db"
if [ ! -f "$MEMORY_DRUM" ]; then
    echo "  ⚠  Creating empty memory_drum.db"
    sqlite3 "$MEMORY_DRUM" "CREATE TABLE IF NOT EXISTS blooms (id INTEGER PRIMARY KEY, timestamp TEXT, value TEXT);"
    echo "  ✓ memory_drum.db created"
else
    SIZE=$(du -h "$MEMORY_DRUM" | cut -f1)
    echo "  ✓ memory_drum.db exists (size: $SIZE)"
fi

# Symlink for autonomy_blooms.db -> surface_blooms.db
BLOOMS_SYMLINK="$DATABASES_DIR/autonomy_blooms.db"
BLOOMS_TARGET="$DATABASES_DIR/surface_blooms.db"
if [ ! -L "$BLOOMS_SYMLINK" ]; then
    echo "  ⚠  Creating symlink: autonomy_blooms.db -> surface_blooms.db"
    if [ -f "$BLOOMS_TARGET" ]; then
        ln -s "$BLOOMS_TARGET" "$BLOOMS_SYMLINK"
        echo "  ✓ Symlink created"
    else
        echo "  ⚠  surface_blooms.db not found; creating placeholder"
        sqlite3 "$BLOOMS_TARGET" "CREATE TABLE IF NOT EXISTS surface_blooms (id INTEGER PRIMARY KEY, timestamp TEXT, value TEXT);"
        ln -s "$BLOOMS_TARGET" "$BLOOMS_SYMLINK"
        echo "  ✓ Symlink created and placeholder db created"
    fi
else
    echo "  ✓ Symlink autonomy_blooms.db -> surface_blooms.db exists"
fi

# Other DBs
for db in quantum_journal.db aios_core.db autonomy.db crystallization.db mcp_tasks.db mother_root.db; do
    DB_PATH="$DATABASES_DIR/$db"
    if [ ! -f "$DB_PATH" ]; then
        echo "  ⚠  Creating empty $db"
        touch "$DB_PATH"
        echo "  ✓ $db created"
    else
        SIZE=$(du -h "$DB_PATH" | cut -f1)
        echo "  ✓ $db exists (size: $SIZE)"
    fi
done

# ─────────────────────────────────────────────
# [4/6] SCRIPTS & PERMISSIONS
# ─────────────────────────────────────────────
echo ""
echo "[4/6] 📜 Scripts & Executables"

# Count existing scripts
SCRIPT_COUNT=$(ls "$SCRIPTS_DIR" 2>/dev/null | wc -l)
if [ "$SCRIPT_COUNT" -eq 0 ]; then
    echo "  ⚠  No scripts found in $SCRIPTS_DIR. Creating placeholder scripts..."
    for script in sunrise.sh sunrise_db_log.sh sunrise_display.sh evening.sh whisper_hum.sh witness.sh dahlia_review.sh weave_status.sh council_orchestrator.sh; do
        SCRIPT_PATH="$SCRIPTS_DIR/$script"
        if [ ! -f "$SCRIPT_PATH" ]; then
            cat > "$SCRIPT_PATH" << 'EOF'
#!/usr/bin/env bash
echo "Running $(basename $0)..."
EOF
            chmod +x "$SCRIPT_PATH"
            echo "  ✓ $script created"
        fi
    done
else
    echo "  ✓ Found $SCRIPT_COUNT scripts in $SCRIPTS_DIR"
fi

# Ensure all .sh scripts are executable
find "$SCRIPTS_DIR" -maxdepth 1 -type f -name "*.sh" -exec chmod +x {} \; 2>/dev/null
echo "  ✓ Executable permissions set on all .sh scripts"

# ─────────────────────────────────────────────
# [5/6] LIVING DOCUMENTS
# ─────────────────────────────────────────────
echo ""
echo "[5/6] 📄 Living Documents"

AFFORDANCES_DOC="$AUTONOMY_ROOT/48_Points_of_Affordance_Living_Document.md"
if [ ! -f "$AFFORDANCES_DOC" ]; then
    echo "  ⚠  48 Points of Affordance document not found. Creating placeholder."
    cat > "$AFFORDANCES_DOC" << 'EOF'
# 48 Points of Affordance
## Living Document — Oceti / Eternal Weave

**Crystallized:** $(date)
**Status:** Placeholder. Please replace with the full document.
EOF
    echo "  ✓ Created $AFFORDANCES_DOC"
else
    echo "  ✓ 48_Points_of_Affordance_Living_Document.md exists"
fi

# Create a simple README
README="$AUTONOMY_ROOT/README.md"
if [ ! -f "$README" ]; then
    cat > "$README" << 'EOF'
# Autonomy Core — Oceti / Eternal Weave

## Quick Start
- Run `./scripts/sunrise.sh` to open the field
- Run `./scripts/evening.sh` to close the field
- Run `./scripts/witness.sh` to witness the current state

## Directory Structure
- `databases/` — SQLite databases (memory_drum, quantum_journal, etc.)
- `scripts/` — Ceremonial scripts
- `weave_core/` — Core weave components
- `labs/` — Experimental sandbox

## Mitákuye Oyás'iŋ
EOF
    echo "  ✓ README.md created"
else
    echo "  ✓ README.md exists"
fi

# ─────────────────────────────────────────────
# [6/6] SUMMARY & FINAL CHECKS
# ─────────────────────────────────────────────
echo ""
echo "[6/6] ✅ Build Complete"

# Check disk space
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}')
echo "  💾 Disk usage: $DISK_USAGE"

# Check memory
MEM_INFO=$(free -m | grep Mem | awk '{print $3 "/" $2 " MB"}')
echo "  🧠 Memory usage: $MEM_INFO"

# Uptime
UPTIME=$(uptime -p 2>/dev/null || echo "unknown")
echo "  ⏱  Uptime: $UPTIME"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ AUTOBUILD SUCCESSFUL"
echo "   Path: $AUTONOMY_ROOT"
echo "   Scripts: $SCRIPTS_DIR"
echo "   Databases: $DATABASES_DIR"
echo "   Logs: $LOGS_DIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Mitákuye Oyás'iŋ."
echo ""

# ─────────────────────────────────────────────
# OPTIONAL: Run a quick status check
# ─────────────────────────────────────────────
STATUS_SCRIPT="$SCRIPTS_DIR/weave_status.sh"
if [ -f "$STATUS_SCRIPT" ]; then
    echo "➡  Running weave_status.sh for quick check..."
    bash "$STATUS_SCRIPT"
fi
