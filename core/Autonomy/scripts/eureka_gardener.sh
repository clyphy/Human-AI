#!/usr/bin/env bash

DB_PATH="$HOME/projects/Human-AI/core/Autonomy/databases/aios_core.db"
MEMORY_FILE="$HOME/projects/Human-AI/core/Autonomy/memory.md"
LOG_DIR="$HOME/projects/Human-AI/core/Autonomy/logs"
LOG_FILE="$LOG_DIR/gardening.log"
LOCK_FILE="$MEMORY_FILE.lock"

MAX_BLOOMS=30
EUREKA_THRESHOLD=1.2
DRY_RUN=false

if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
fi

log_action() {
    local level="$1"
    local msg="$2"
    local ts
    ts=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$ts] [$level] $msg" | tee -a "$LOG_FILE"
}

acquire_lock() {
    local timeout=30
    local elapsed=0
    while (( elapsed < timeout )); do
        if mkdir "$LOCK_FILE" 2>/dev/null; then
            log_action "INFO" "Lock acquired"
            return 0
        fi
        ((elapsed++))
        sleep 1
    done
    log_action "ERROR" "Lock timeout"
    return 1
}

release_lock() {
    if [[ -d "$LOCK_FILE" ]]; then
        rm -rf "$LOCK_FILE"
        log_action "INFO" "Lock released"
    fi
}

trap release_lock EXIT

ensure_promoted_at_column() {
    local exists
    exists=$(sqlite3 "$DB_PATH" "PRAGMA table_info(review_queue);" | grep -c "promoted_at" || true)
    if [[ "$exists" -eq 0 ]]; then
        log_action "INFO" "Adding promoted_at column..."
        if $DRY_RUN; then
            log_action "DRY-RUN" "Would add promoted_at column"
        else
            sqlite3 "$DB_PATH" "ALTER TABLE review_queue ADD COLUMN promoted_at TEXT;"
            log_action "INFO" "promoted_at column created"
        fi
    fi
}

promote_pass() {
    local pass_name="$1"
    local kind_sql="$2"
    local limit="$3"

    mapfile -t IDS < <(sqlite3 "$DB_PATH" "
        SELECT id
        FROM review_queue
        WHERE score >= $EUREKA_THRESHOLD
          AND status = 'pending'
          AND redacted = 0
          AND kind IN ($kind_sql)
        ORDER BY score DESC, created_at DESC
        LIMIT $limit;
    ")

    local count=${#IDS[@]}

    if [[ $count -eq 0 ]]; then
        log_action "INFO" "[$pass_name] No ripe blooms found"
        return
    fi

    log_action "INFO" "[$pass_name] Harvested $count items"

    for id in "${IDS[@]}"; do
        IFS=$'\t' read -r kind score created context content < <(
            sqlite3 -separator $'\t' "$DB_PATH" "
                SELECT kind, score, created_at, context, content
                FROM review_queue
                WHERE id = $id;
            "
        )

        log_action "INFO" "[$pass_name] Promoting #$id [$kind] score=$score"

        if $DRY_RUN; then
            log_action "DRY-RUN" "Would promote #$id"
        else
            {
                echo ""
                echo "---"
                echo "Bloom #$id | $kind | $created | score=$score"
                echo "Context: $context"
                echo ""
                echo "$content"
                echo "---"
            } >> "$MEMORY_FILE"

            sqlite3 "$DB_PATH" "UPDATE review_queue SET status = 'promoted', promoted_at = datetime('now') WHERE id = $id;"
        fi
    done
}

# ==================== MAIN ====================
log_action "INFO" "🌱 Gardening cycle started (threshold: $EUREKA_THRESHOLD) | dry-run=$DRY_RUN"

if [[ ! -f "$DB_PATH" ]]; then
    log_action "ERROR" "Database not found"
    exit 1
fi

if ! acquire_lock; then
    exit 1
fi

ensure_promoted_at_column

promote_pass "HIGH-PRIORITY (bloom)" "'bloom'" 15
promote_pass "REGULAR" "'concept','formula'" $MAX_BLOOMS

log_action "INFO" "Gardening cycle complete"
