#!/usr/bin/env bash
# airlock_quarantine.sh — Leviathan → Sanctuary JSON airlock
set -euo pipefail
STAGING="${1:-./staging.json}"
DB="${HOME}/projects/Human-AI/core/Autonomy/databases/aios_core.db"
JOURNAL="${HOME}/projects/Human-AI/core/Autonomy/databases/quantum_journal.db"
SCHEMA_VERSION="1.0"
REQUIRED_FIELDS='["job_id","entity_id","vector_relation","confidence_score"]'

if [[ ! -f "$STAGING" ]]; then
  echo "ERROR: staging file not found: $STAGING" >&2
  exit 1
fi

if ! python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$STAGING" 2>/dev/null; then
  STATUS="dead_letter"; REASON="invalid_json"
else
  MISSING=$(python3 - <<'PY' "$STAGING" "$REQUIRED_FIELDS"
import json, sys
payload = json.load(open(sys.argv[1]))
required = json.loads(sys.argv[2])
missing = [f for f in required if f not in payload]
print(",".join(missing) if missing else "")
PY
)
  if [[ -n "$MISSING" ]]; then
    STATUS="dead_letter"; REASON="missing_fields:$MISSING"
  else
    STATUS="pending_cascade"; REASON="ok"
  fi
fi

JOB_ID=$(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d.get('job_id','unknown'))" "$STAGING" 2>/dev/null || echo "unknown")
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

sqlite3 "$DB" "CREATE TABLE IF NOT EXISTS review_queue (id TEXT PRIMARY KEY, raw_payload TEXT NOT NULL, is_valid_json BOOLEAN NOT NULL DEFAULT 0, schema_version TEXT NOT NULL DEFAULT '1.0', received_at TEXT NOT NULL, status TEXT NOT NULL, notes TEXT);"
sqlite3 "$DB" "CREATE TABLE IF NOT EXISTS dead_letter (id TEXT PRIMARY KEY, raw_payload TEXT NOT NULL, reason TEXT NOT NULL, received_at TEXT NOT NULL, moved_at TEXT NOT NULL);"
sqlite3 "$JOURNAL" "CREATE TABLE IF NOT EXISTS journal_events (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL, event_type TEXT NOT NULL, source TEXT, detail TEXT);"
sqlite3 "$JOURNAL" "CREATE TABLE IF NOT EXISTS uplink_audit (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL, reason TEXT NOT NULL, job_class TEXT NOT NULL, ram_pressure REAL, why_not_local TEXT, bytes_sent INTEGER);"

if [[ "$STATUS" == "pending_cascade" ]]; then
  sqlite3 "$DB" "INSERT OR REPLACE INTO review_queue (id, raw_payload, is_valid_json, schema_version, received_at, status) VALUES ('$JOB_ID', $(python3 -c "import json,sys; print(json.dumps(open(sys.argv[1]).read()))" "$STAGING"), 1, '$SCHEMA_VERSION', '$TS', '$STATUS');"
  echo "ACCEPTED: $JOB_ID → review_queue"
else
  sqlite3 "$DB" "INSERT OR REPLACE INTO dead_letter (id, raw_payload, reason, received_at, moved_at) VALUES ('$JOB_ID', $(python3 -c "import json,sys; print(json.dumps(open(sys.argv[1]).read()))" "$STAGING"), '$REASON', '$TS', '$TS');"
  echo "DEAD-LETTER: $JOB_ID ($REASON)"
fi

sqlite3 "$JOURNAL" "INSERT INTO journal_events (ts, event_type, source, detail) VALUES ('$TS', 'quarantine', 'airlock_quarantine.sh', json_object('job_id', '$JOB_ID', 'status', '$STATUS', 'reason', '$REASON'));"
[[ "$STATUS" == "dead_letter" ]] && exit 2 || exit 0
