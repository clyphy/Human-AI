#!/usr/bin/env bash
# circulation.sh — moves already-formed surface blooms into crystallization.db.
# Non-destructive: source rows are never deleted or altered, only tracked by a
# high-water-mark state file. Safe to re-run; only new rows are moved each time.
set -euo pipefail
AUTONOMY_ROOT="${AUTONOMY_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
DB_DIR="$AUTONOMY_ROOT/databases"
SRC="$DB_DIR/surface_blooms.db"
DST="$DB_DIR/crystallization.db"
STATE_DIR="$AUTONOMY_ROOT/logs"
mkdir -p "$STATE_DIR"
STATE="$STATE_DIR/circulation_state"

last_id=0
[ -f "$STATE" ] && last_id=$(cat "$STATE")

new_rows=$(sqlite3 -separator "|" "$SRC" "SELECT id, timestamp, pattern, affordances FROM blooms WHERE id > $last_id ORDER BY id;")
if [ -z "$new_rows" ]; then
  echo "circulation: nothing new to move (last id: $last_id)"
  exit 0
fi

max_id=$last_id
moved=0
while IFS="|" read -r id ts pattern affordances; do
  [ -z "$id" ] && continue
  esc_pattern=$(printf "%s" "${pattern:-unspecified}" | sed "s/'/'''/g")
  esc_affordances=$(printf "%s" "${affordances:-}" | sed "s/'/'''/g")
  sqlite3 "$DST" "INSERT INTO crystals (timestamp, form, intent, affordance_name, source, status) VALUES ('$ts', 'surface_bloom', '$esc_pattern', '$esc_affordances', 'circulation.sh', 'active');"
  max_id=$id
  moved=$((moved+1))
done <<< "$new_rows"

echo "$max_id" > "$STATE"
echo "circulation: moved $moved row(s), now at id $max_id"
