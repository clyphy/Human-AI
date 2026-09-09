#!/usr/bin/env fish
# EUREKA BLOOM GARDENING SCRIPT - Oceti Weave v3.0
# Targets weave_log table in aios_core.db

set DB_PATH "$HOME/projects/Human-AI/core/Autonomy/aios_core.db"
set MEMORY_FILE "$HOME/projects/Human-AI/core/Autonomy/memory.md"
set LOG_DIR "$HOME/projects/Human-AI/core/Autonomy/logs"
set LOG_FILE "$LOG_DIR/gardening.log"
set LOCK_FILE "$MEMORY_FILE.lock"
set MAX_BLOOMS 5
set EUREKA_THRESHOLD 3.0
set TIMESTAMP (date +"%Y-%m-%d %H:%M:%S")

function log_action
    set level $argv[1]
    set msg $argv[2]
    echo "[$TIMESTAMP] [$level] $msg" >> $LOG_FILE
    echo "[$level] $msg"
end

function acquire_lock
    set timeout 30
    set elapsed 0
    while test $elapsed -lt $timeout
        if mkdir $LOCK_FILE 2>/dev/null
            log_action "INFO" "Lock acquired"
            return 0
        end
        set elapsed (math $elapsed + 1)
        sleep 1
    end
    log_action "ERROR" "Lock timeout"
    return 1
end

function release_lock
    rm -rf $LOCK_FILE
    log_action "INFO" "Lock released"
end

trap release_lock EXIT

log_action "INFO" "🌱 Gardening started (threshold: $EUREKA_THRESHOLD)"

if not test -f $DB_PATH
    log_action "ERROR" "DB not found: $DB_PATH"
    exit 1
end

if not acquire_lock
    exit 1
end

# Add harvested column if it doesn't exist
sqlite3 $DB_PATH "ALTER TABLE weave_log ADD COLUMN harvested INTEGER DEFAULT 0;" 2>/dev/null

# Query unharvested blooms with coherence >= threshold
set BLOOMS (sqlite3 -separator '|' $DB_PATH "SELECT id, glyph, response, coherence, ts FROM weave_log WHERE coherence >= $EUREKA_THRESHOLD AND harvested = 0 ORDER BY coherence DESC, ts DESC LIMIT $MAX_BLOOMS;")
set BLOOM_COUNT (count $BLOOMS)

if test "$BLOOM_COUNT" -eq 0
    log_action "INFO" "No ripe blooms ready. ✨"
    release_lock
    exit 0
end

log_action "INFO" "Found $BLOOM_COUNT ripe blooms"

set PROCESSED_IDS
set APPEND_CONTENT ""

for line in $BLOOMS
    test -z "$line"; and continue
    set parts (string split '|' $line)
    set id $parts[1]
    set glyph $parts[2]
    set content $parts[3]
    set score $parts[4]
    set ts $parts[5]

    log_action "INFO" "Promoting bloom #$id: '$glyph' (coherence: $score)"

    set APPEND_CONTENT "$APPEND_CONTENT

---

**EUREKA BLOOM** | Coherence: $score | ID: $id | Timestamp: $ts

### $glyph

$content

*Promoted: $TIMESTAMP*"
    set PROCESSED_IDS $PROCESSED_IDS $id
end

if test -n "$APPEND_CONTENT"
    echo -e $APPEND_CONTENT >> $MEMORY_FILE
    log_action "INFO" "Appended $BLOOM_COUNT blooms to memory.md"
end

# Mark harvested
for id in $PROCESSED_IDS
    sqlite3 $DB_PATH "UPDATE weave_log SET harvested = 1 WHERE id = $id;"
    log_action "INFO" "Marked bloom #$id as harvested"
end

log_action "INFO" "🌿 Gardening complete. $BLOOM_COUNT blooms harvested."
release_lock
