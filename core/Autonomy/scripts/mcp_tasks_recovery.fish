#!/usr/bin/env fish
# MCP_TASKS.DB RECOVERY - Oceti Weave v3.0
set DB "$HOME/projects/Human-AI/core/Autonomy/databases/mcp_tasks.db"
set BACKUP "$DB.backup.(date +%s)"

echo "🔧 Attempting recovery of mcp_tasks.db"

# Backup first
cp $DB $BACKUP 2>/dev/null; or echo "⚠️ Could not backup (DB may be fully corrupted)"

# Try dump and rebuild
set DUMP (sqlite3 $DB ".dump" 2>/dev/null)
if test $status -eq 0
    echo "✅ Dump succeeded. Rebuilding..."
    rm $DB
    echo $DUMP | sqlite3 $DB
    echo "✅ Rebuilt from dump"
else
    echo "❌ Dump failed. Trying PRAGMA recovery..."
    sqlite3 $DB "PRAGMA integrity_check;" 2>/dev/null
    sqlite3 $DB "REINDEX;" 2>/dev/null
    sqlite3 $DB "VACUUM;" 2>/dev/null
    echo "⚠️ Recovery attempted. Check with: sqlite3 $DB '.tables'"
end

# If all fails, create fresh schema
if not test -f $DB
    echo "🌱 Creating fresh mcp_tasks.db"
    sqlite3 $DB "CREATE TABLE tasks (id INTEGER PRIMARY KEY, agent TEXT, task TEXT, model TEXT, status TEXT DEFAULT 'pending', result TEXT, l_at_time REAL, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
    echo "✅ Fresh database created"
end
