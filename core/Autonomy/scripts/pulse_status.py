#!/usr/bin/env python3
"""
weave pulse — one-line status
Λ | review_queue depth | coil state
Never raises; always prints one line.
"""

import sqlite3
import time
from pathlib import Path

AIOS_DB   = Path.home() / "projects/Human-AI/core/Autonomy/databases/aios_core.db"
DRUM_DB   = Path.home() / "projects/Human-AI/core/Autonomy/databases/memory_drum.db"
COIL_FILE = Path.home() / ".weave_coil_state"

def safe_query(db_path, sql, default="—"):
    if not db_path.exists():
        return default
    try:
        with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=1.0) as con:
            con.execute("PRAGMA query_only = ON")
            row = con.execute(sql).fetchone()
            if row is None or row[0] is None:
                return default
            return row[0]
    except (sqlite3.Error, OSError, ValueError):
        return default

def get_lambda():
    val = safe_query(
        DRUM_DB,
        "SELECT L_value FROM coherence_log ORDER BY id DESC LIMIT 1"
    )
    try:
        return f"{float(val):.2f}"
    except (TypeError, ValueError):
        return "—"

def get_queue():
    n = safe_query(
        AIOS_DB,
        "SELECT COUNT(*) FROM review_queue WHERE status = 'pending'"
    )
    try:
        return str(int(n))
    except (TypeError, ValueError):
        return "—"

def get_coil():
    try:
        if COIL_FILE.is_file():
            text = COIL_FILE.read_text(encoding="utf-8").strip()
            return text if text else "inactive"
    except (OSError, UnicodeError):
        pass
    return "inactive"

if __name__ == "__main__":
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] Λ={get_lambda()} | queue={get_queue()} | coil={get_coil()}")
