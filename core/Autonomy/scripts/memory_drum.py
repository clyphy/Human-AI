#!/usr/bin/env python3
import sqlite3
import json
from datetime import datetime
from pathlib import Path

class MemoryDrum:
    def __init__(self, base_db_dir="~/projects/Human-AI/core/Autonomy/databases"):
        self.db_dir = Path(base_db_dir).expanduser()
        
        # Explicit real-world direct paths mapping all core files in your system space
        self.db_paths = {
            "memory_drum": self.db_dir / "memory_drum.db",
            "autonomy": self.db_dir / "autonomy.db",
            "quantum_journal": self.db_dir / "quantum_journal.db",
            "crystallization": self.db_dir / "crystallization.db"
        }

    def store_bloom(self, content_string, affordance_array, tags_string="resonance_loop", score_val=1.0):
        """Indexes data natively into your active database columns to support semantic resonance loops."""
        size_bytes = len(content_string.encode('utf-8'))
        affordances_json = json.dumps(affordance_array)

        conn = sqlite3.connect(self.db_paths["memory_drum"])
        c = conn.cursor()
        try:
            c.execute('''
                INSERT INTO blooms (content, score, tags, affordances, size) 
                VALUES (?, ?, ?, ?, ?)
            ''', (content_string, score_val, tags_string, affordances_json, size_bytes))
            conn.commit()
            return c.lastrowid
        except Exception as e:
            print(f"[!] Target block write failed: {e}")
            return None
        finally:
            conn.close()

    def stats(self):
        """Gathers unified metrics across your active database space, including crystallization nodes."""
        # 1. Fetch data metrics from memory_drum.db
        conn_drum = sqlite3.connect(self.db_paths["memory_drum"])
        c_drum = conn_drum.cursor()
        
        c_drum.execute('SELECT COUNT(*) FROM blooms')
        bloom_count = c_drum.fetchone()[0] or 0
        
        c_drum.execute('SELECT SUM(size) FROM blooms')
        total_size = c_drum.fetchone()[0] or 0
        conn_drum.close()
        
        # 2. Integrate direct data check against crystallization.db
        crystal_count = 0
        if self.db_paths["crystallization"].exists():
            try:
                conn_cryst = sqlite3.connect(self.db_paths["crystallization"])
                c_cryst = conn_cryst.cursor()
                c_cryst.execute('SELECT COUNT(*) FROM promoted_crystals')
                crystal_count = c_cryst.fetchone()[0] or 0
                conn_cryst.close()
            except sqlite3.OperationalError:
                pass # Table or file locked, falls back to zero safely

        return {
            'timestamp': datetime.now().isoformat(),
            'total_blooms_indexed': bloom_count,
            'current_memory_drum_size_mb': total_size / (1024 * 1024),
            'total_solidified_crystals': crystal_count,
            'hardware_ceiling_ram': '8GB'
        }

if __name__ == "__main__":
    drum = MemoryDrum()
    print(f"[+] Unified System Space Metrics:\n{json.dumps(drum.stats(), indent=2)}")

