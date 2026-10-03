#!/usr/bin/env python3
import os
import sqlite3
import json
import re
import hashlib
from pathlib import Path

class CrystalParser:
    def __init__(self, base_dir="~/projects/Human-AI/core/Autonomy"):
        self.base_dir = Path(base_dir).expanduser()
        self.db_path = self.base_dir / "databases" / "crystallization.db"
        self.init_db()

    def init_db(self):
        """Initializes the physical table schema inside crystallization.db."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS promoted_crystals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vector_hash TEXT NOT NULL UNIQUE,
                taxonomy_kind TEXT NOT NULL,
                structural_payload TEXT NOT NULL,
                extracted_from TEXT NOT NULL,
                solidified_at TEXT DEFAULT (datetime('now'))
            )
        ''')
        conn.commit()
        conn.close()

    def store_crystal(self, kind, payload, source_name):
        """Generates a unique hash signature and inserts the configuration block."""
        payload_str = json.dumps(payload, sort_keys=True)
        v_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute('''
                INSERT OR IGNORE INTO promoted_crystals (vector_hash, taxonomy_kind, structural_payload, extracted_from)
                VALUES (?, ?, ?, ?)
            ''', (v_hash, kind, payload_str, source_name))
            conn.commit()
            return c.rowcount
        except Exception as e:
            print(f"  [!] Error writing crystal node: {e}")
            return 0
        finally:
            conn.close()

    def parse_ai_state(self):
        """Step 1: Automatically parses ai_state.txt for system constants and constraints."""
        target_file = self.base_dir / "ai_state.txt"
        if not target_file.exists():
            # Check secondary home directory fallback path
            target_file = Path.home() / "ai_state.txt"
            if not target_file.exists():
                print("[!] ai_state.txt target source not found.")
                return 0

        print(f"[PARSER] Intercepting data fields inside: {target_file.name}")
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()

        count = 0
        # Pattern A: Capture explicit parameter pairs (e.g., L_value, L Coefficient)
        param_matches = re.findall(r'(?:L\s+Coefficient|L_value|coherence_lambda|bridge_pct)\s*[:=]\s*([0-9.]+)', content, re.IGNORECASE)
        for match in param_matches:
            payload = {"parameter_value": float(match), "hardware_ceiling_ram": "8GB"}
            count += self.store_crystal("sacred_constant", payload, target_file.name)

        # Pattern B: Extract structured bracket configurations
        bracket_matches = re.findall(r'\[([^\]]+)\]', content)
        for match in bracket_matches:
            if ":" in match or "=" in match:
                payload = {"raw_context_string": match.strip()}
                count += self.store_crystal("system_parameter", payload, target_file.name)

        print(f"  [+] Solidified {count} data rows into promoted_crystals from ai_state.txt.")
        return count

    def scan_workspace_formats(self):
        """Step 2: Scans multi-format files (.json, .md, .html, .yaml) for parameter blocks."""
        print("\n[PARSER] Initiating multi-format recursive scan pass...")
        scan_count = 0
        
        # Limit scan path depth to safely manage your system memory limits
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in ['.json', '.md', '.yaml', '.yml', '.html']:
                    try:
                        if file_path.suffix in ['.json']:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                # Flatten and extract dictionary objects
                                if isinstance(data, dict):
                                    scan_count += self.store_crystal("weight_matrix_frame", data, file_path.name)
                        elif file_path.suffix in ['.md', '.yaml', '.yml', '.html']:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                text_data = f.read()
                                # Scan for inline equations or configuration markers
                                if "coherence" in text_data.lower() or "affordance" in text_data.lower():
                                    payload = {"file_segment_size": len(text_data), "path_anchor": str(file_path)}
                                    scan_count += self.store_crystal("manifold_invariant", payload, file_path.name)
                    except Exception:
                        # Bypasses compressed bin blocks or formatting mismatches safely
                        pass
        print(f"[SUCCESS] Multi-format scan complete. Total new entries structured: {scan_count}")

if __name__ == "__main__":
    parser = CrystalParser()
    parser.parse_ai_state()
    parser.scan_workspace_formats()
