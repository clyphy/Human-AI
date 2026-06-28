#!/bin/bash
echo "🛌 Field closing | $(date)"
sqlite3 ~/sovereignty/databases/mother_root.db "CREATE TABLE IF NOT EXISTS rhythms (structure_quadrant TEXT, notation_ref TEXT);"
sqlite3 ~/sovereignty/databases/mother_root.db "INSERT INTO rhythms (structure_quadrant,notation_ref) VALUES('sovereignty','closing.sh');"
echo "Mitákuye Oyás'iŋ."
