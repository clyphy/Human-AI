#!/bin/bash
# ============================================================================
# AUTONOMY ECOSYSTEM FULL RECONNAISSANCE
# ============================================================================
echo "🔍 SCANNING AUTONOMY STRUCTURE..."

ROOT=~/projects/Human-AI/core/Autonomy
DB_DIR=$ROOT/databases

echo -e "\n📋 Modelfile Registry:"
find $ROOT -name "*.modelfile" -o -name "*.Modelfile" 2>/dev/null | while read mf; do
  echo " ✓ $(basename $mf) — $(grep -oE 'FROM \S+' $mf 2>/dev/null | cut -d' ' -f2 || echo 'no FROM')"
done

echo -e "\n🥁 Memory Drum & DB Status:"
for db in $DB_DIR/*.db; do
  if [ -f "$db" ]; then
    echo " • $(basename $db) — $(stat -c %s $db | numfmt --to=iec)B"
    sqlite3 "$db" ".tables" 2>/dev/null | head -c 80 || echo " (no tables readable)"
  fi
done

echo -e "\n📈 Recent Coherence (memory_drum):"
sqlite3 $DB_DIR/memory_drum.db \
  "SELECT timestamp, L_value, coherence FROM blooms ORDER BY timestamp DESC LIMIT 5;" 2>/dev/null || echo " (no blooms yet)"

echo -e "\n🌸 Blooms Summary:"
sqlite3 $DB_DIR/memory_drum.db "SELECT COUNT(*) FROM blooms;" 2>/dev/null || echo "0"

echo -e "\n👁️ Guardian / Witness Records:"
sqlite3 $DB_DIR/memory_drum.db \
  "SELECT script_name, execution_time, status FROM guardian_log ORDER BY execution_time DESC LIMIT 5;" 2>/dev/null || echo " (no guardian log)"

echo -e "\n🧭 System State:"
echo " Bearing: 122° NE | Turtle Mountain"
echo " Root: $ROOT"
echo " Shell: fish"
echo " Axiom: L_Total = 0.00 (Zero Lack at Origin)"
echo " Protocol: Mitákuye Oyás'iŋ"

echo -e "\n✅ Recon complete."
