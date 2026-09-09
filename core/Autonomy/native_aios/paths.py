"""Shared path resolver for Native AIOS modules."""
from pathlib import Path
NATIVE = Path(__file__).resolve().parent          # .../Autonomy/native_aios
ROOT = NATIVE.parent                                # .../Autonomy
SCRIPTS = ROOT / "scripts"
CONFIG = NATIVE / "config"
VAR = NATIVE / "var"
LOGS = NATIVE / "logs"
DB = NATIVE / "persistence" / "aios_core.db"
SCHEMA = NATIVE / "persistence" / "schema.sql"
INBOX = VAR / "inbox"
SCAN_CACHE = VAR / "scan_cache"
LOCKS = VAR / "locks"
STATE = VAR / "state"
