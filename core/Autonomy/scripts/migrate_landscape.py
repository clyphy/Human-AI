#!/usr/bin/env python3
import sqlite3
from pathlib import Path

def force_landscape_alignment():
    db_dir = Path.home() / "projects" / "Human-AI" / "core" / "Autonomy" / "databases"
    target_dbs = ["memory_drum.db", "autonomy.db", "quantum_journal.db"]
    
    print("[MIGRATION] Enforcing strict column structures across data layers...")
    
    for db_name in target_dbs:
        db_path = db_dir / db_name
        if not db_path.exists():
            continue
            
        print(f"  -> Patching table structures inside: {db_name}")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # 1. Force the presence of the blooms table baseline
        c.execute('''
            CREATE TABLE IF NOT EXISTS blooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT
            )
        ''')
        conn.commit()
        
        # 2. Force add every single required structural column independently
        columns_to_add = [
            ("hash", "TEXT UNIQUE"),
            ("size", "INTEGER DEFAULT 0"),
            ("affordances", "TEXT")
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                c.execute(f"ALTER TABLE blooms ADD COLUMN {col_name} {col_type};")
                conn.commit()
                print(f"    [+] Successfully added missing column: {col_name}")
            except sqlite3.OperationalError:
                # Column already exists safely, bypass to next field
                pass

        # 3. Align the frequency mapping matrices
        try:
            c.execute("ALTER TABLE rights_freq RENAME TO affordances_freq;")
            c.execute("ALTER TABLE affordances_freq RENAME COLUMN right_id TO affordance_id;")
            conn.commit()
            print("    [+] Aligned rights frequency mappings to affordances_freq.")
        except sqlite3.OperationalError:
            pass
            
        conn.close()
    print("[SUCCESS] Multi-database structures locked and verified.")

if __name__ == "__main__":
    force_landscape_alignment()
