#!/usr/bin/env python3
import sqlite3
import json
from datetime import datetime
from pathlib import Path

class ResonanceEngine:
    def __init__(self, base_dir="~/projects/Human-AI/core/Autonomy"):
        self.base_dir = Path(base_dir).expanduser()
        self.db_paths = {
            "memory_drum": self.base_dir / "databases" / "memory_drum.db",
            "quantum_journal": self.base_dir / "databases" / "quantum_journal.db"
        }
        self.init_journal()

    def init_journal(self):
        """Ensures the quantum journal contains a clear ledger for tracking non-linear loop events."""
        conn = sqlite3.connect(self.db_paths["quantum_journal"])
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS journal_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT DEFAULT (datetime('now')),
                event TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def query_and_log_pass(self):
        """Queries the active memory drum blooms and commits the sync pass to the ledger."""
        print("[PROCESS] Initiating multi-database loop verification...")
        
        # 1. Read blooms count
        conn_drum = sqlite3.connect(self.db_paths["memory_drum"])
        c_drum = conn_drum.cursor()
        c_drum.execute('SELECT COUNT(*) FROM blooms')
        blooms_count = c_drum.fetchone()[0]
        conn_drum.close()
        
        # 2. Commit time signature block straight to your real quantum journal
        conn_journal = sqlite3.connect(self.db_paths["quantum_journal"])
        c_journal = conn_journal.cursor()
        
        event_string = f"ORCHESTRATOR_SYNC_PASS | Blooms: {blooms_count} | Mesh State: Bound"
        c_journal.execute('INSERT INTO journal_ledger (event) VALUES (?)', (event_string,))
        conn_journal.commit()
        
        # 3. Output the raw verification rows from the ledger to show the data is real
        print("\n[JOURNAL] Pulling active time footprints from journal_ledger:")
        print("=" * 60)
        c_journal.execute('SELECT id, ts, event FROM journal_ledger ORDER BY id DESC LIMIT 3')
        for row in c_journal.fetchall():
            print(f"  Row ID {row[0]:<4} | Timestamp: {row[1]} | Event: {row[2]}")
        print("=" * 60)
        conn_journal.close()

if __name__ == "__main__":
    engine = ResonanceEngine()
    engine.query_and_log_pass()

