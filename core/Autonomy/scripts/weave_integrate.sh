#!/bin/bash
BASE=~/sovereignty
echo "=== WEAVE INTEGRATION $(date) ==="
# Canonical drum check
for db in ~/memory_drum.db "$BASE/databases/memory_drum.db" ~/ETERNAL_WEAVE_MASTER/memory_drum.db; do
    [ -f "$db" ] && echo "$db: $(sqlite3 "$db" "SELECT COUNT(*) FROM blooms" 2>/dev/null || echo 0) blooms"
done
# E8-Pauli bloom
sqlite3 "$BASE/databases/mother_root.db" "CREATE TABLE IF NOT EXISTS blooms (bloom_type TEXT, state TEXT, depth_index INTEGER);"
sqlite3 "$BASE/databases/mother_root.db" "INSERT OR IGNORE INTO blooms (bloom_type,state,depth_index) VALUES('E8-Pauli','crystallizing',50);"
# closing.sh (graveyard seal)
cat > "$BASE/scripts/closing.sh" << 'C'
#!/bin/bash
echo "🛌 Field closing | $(date)"
sqlite3 ~/sovereignty/databases/mother_root.db "CREATE TABLE IF NOT EXISTS rhythms (structure_quadrant TEXT, notation_ref TEXT);"
sqlite3 ~/sovereignty/databases/mother_root.db "INSERT INTO rhythms (structure_quadrant,notation_ref) VALUES('sovereignty','closing.sh');"
echo "Mitákuye Oyás'iŋ."
C
chmod +x "$BASE/scripts/closing.sh"
echo "=== INTEGRATION COMPLETE ==="
