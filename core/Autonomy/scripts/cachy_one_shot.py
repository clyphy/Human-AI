#!/usr/bin/env python3
import os
import re
import json
import sqlite3
import subprocess
from datetime import datetime
from typing import Dict, Any, List, Tuple

# Multi-Database System Paths
DB_PATHS = {
    "memory_drum": os.path.expanduser("~/memory_drum.db"),
    "autonomy": os.path.expanduser("~/Documents/GitHub/my-repos/autonomy/databases/autonomy.db"),
    "quantum_journal": os.path.expanduser("~/Documents/GitHub/my-repos/autonomy/databases/quantum_journal.db")
}
MCP_CONFIG_PATH = os.path.expanduser("~/.config/cachy_mcp_config.json")

def init_all_dbs():
    for name, path in DB_PATHS.items():
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
            except Exception:
                continue
        try:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resonance_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    event_type TEXT,
                    status TEXT,
                    details TEXT
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"\033[1;31mSkipped initialization for {name}: {e}\033[0m")

def log_event_to_all(event_type: str, status: str, details: str):
    for name, path in DB_PATHS.items():
        try:
            if not os.path.exists(path):
                continue
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO resonance_history (timestamp, event_type, status, details) VALUES (?, ?, ?, ?)",
                (datetime.now().isoformat(), event_type, status, f"[{name.upper()}] {details}")
            )
            conn.commit()
            conn.close()
        except Exception:
            pass

def load_mcp_integration() -> Dict[str, Any]:
    if os.path.exists(MCP_CONFIG_PATH):
        try:
            with open(MCP_CONFIG_PATH, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    
    default_config = {
        "mcpServers": {
            "cachyos-skeptic-filter": {
                "command": "node",
                "args": [os.path.expanduser("~/Documents/GitHub/my-repos/resonances_affordances/server.js")]
            }
        }
    }
    try:
        os.makedirs(os.path.dirname(MCP_CONFIG_PATH), exist_ok=True)
        with open(MCP_CONFIG_PATH, 'w') as f:
            json.dump(default_config, f, indent=2)
    except Exception:
        pass
    return default_config

class UndercoverFilter:
    def __init__(self):
        self.forbidden_patterns = {
            'CODENAME_OPUS_4_7': re.compile(r'\b(opus[-_\s]?4\.7)\b', re.IGNORECASE),
            'CODENAME_SONNET_4_8': re.compile(r'\b(sonnet[-_\s]?4\.8)\b', re.IGNORECASE),
            'INTERNAL_PROJECT_FENNEC': re.compile(r'\b(fennec)\b', re.IGNORECASE),
            'INTERNAL_PROJECT_NUMBAT': re.compile(r'\b(numbat)\b', re.IGNORECASE),
            'INTERNAL_PROJECT_CAPYBARA': re.compile(r'\b(capybara)\b', re.IGNORECASE)
        }
    def sanitize(self, output: str) -> Tuple[str, bool, List[str]]:
        clean_text = output
        is_triggered = False
        redacted_labels = []
        for label, pattern in self.forbidden_patterns.items():
            if pattern.search(clean_text):
                is_triggered = True
                redacted_labels.append(label)
                clean_text = pattern.sub('[REDACTED_INTERNAL_TERM]', clean_text)
        return clean_text, is_triggered, redacted_labels

class SkepticalEngine:
    @staticmethod
    def verify_file_state(file_path: str, expected_snippet: str) -> Dict[str, Any]:
        expanded_path = os.path.expanduser(file_path)
        if not os.path.exists(expanded_path):
            return {"is_valid": False, "error": f"Path missing: {file_path}", "status": "MISSING"}
        try:
            with open(expanded_path, 'r', encoding='utf-8', errors='ignore') as f:
                is_valid = expected_snippet in f.read()
                return {"is_valid": is_valid, "status": "SUCCESS" if is_valid else "MISMATCH"}
        except Exception as e:
            return {"is_valid": False, "error": str(e), "status": "ERROR"}

class CachyLogAnalyzer:
    @staticmethod
    def scan_journal_errors(line_count: int = 5) -> List[str]:
        try:
            cmd = ["journalctl", "-p", "0..3", "-n", str(line_count), "--no-pager"]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return res.stdout.strip().split("\n") if res.stdout.strip() else ["No critical system errors."]
        except Exception as e:
            return [f"Log scan skipped: {str(e)}"]

def main():
    init_all_dbs()
    mcp_config = load_mcp_integration()
    filter_engine = UndercoverFilter()
    skeptic = SkepticalEngine()
    log_tool = CachyLogAnalyzer()
    
    print("\033[1;36m=== CachyOS Remixed Multi-DB Terminal Pipeline ===\033[0m")
    print("Commands: 'scan-logs', 'test-verify', 'view-db', 'view-mcp', 'exit'\n")
    
    while True:
        try:
            user_input = input("\033[1;32mcachy-agent❯\033[0m ").strip()
            if not user_input:
                continue
            if user_input.lower() == 'exit':
                print("Exiting pipeline cleanly.")
                break
            
            if user_input.lower() == 'view-mcp':
                print(f"\033[1;34mActive MCP Configuration Matrix:\033[0m")
                print(json.dumps(mcp_config, indent=2))
                log_event_to_all("MCP_CONFIG_VIEW", "SUCCESS", "Viewed configuration profile mapping")
                continue

            if user_input.lower() == 'view-db':
                for db_name, db_path in DB_PATHS.items():
                    print(f"\033[1;35mRecent entries for storage field: {db_name}\033[0m")
                    if not os.path.exists(db_path):
                        print("  File path does not exist currently.")
                        continue
                    try:
                        conn = sqlite3.connect(db_path)
                        rows = conn.cursor().execute("SELECT * FROM resonance_history ORDER BY id DESC LIMIT 3").fetchall()
                        conn.close()
                        if not rows:
                            print("  No database entries found yet.")
                        for r in rows: 
                            print(f"  ID {r} | {r[:19]} | {r} | {r} | {r}")
                    except Exception as e:
                        print(f"  Error reading DB: {e}")
                continue
                
            if user_input.lower() == 'scan-logs':
                logs = log_tool.scan_journal_errors()
                for err in logs: 
                    print(f"  > {err}")
                log_event_to_all("LOG_SCAN", "SUCCESS", f"Lines retrieved: {len(logs)}")
                continue
                
            if user_input.lower() == 'test-verify':
                path = input("File path: ").strip()
                snippet = input("Expected text snippet: ").strip()
                res = skeptic.verify_file_state(path, snippet)
                print(f"Result: {res}")
                log_event_to_all("SKEPTICAL_CHECK", res.get("status"), f"Path: {path}")
                continue
                
            clean, triggered, leaks = filter_engine.sanitize(user_input)
            if triggered: 
                print(f"\033[1;31m[BLOCKED LEAK]: {leaks}\033[0m\nSanitized text: {clean}\n")
                log_event_to_all("FILTER_TRIGGERED", "BLOCKED", f"Leaks: {leaks}")
            else: 
                print("\033[1;34m[Secure Text Path] Passed verification pipeline.\033[0m\n")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting pipeline cleanly.")
            break

if __name__ == "__main__":
    main()
