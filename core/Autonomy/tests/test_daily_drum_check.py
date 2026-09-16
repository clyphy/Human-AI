from pathlib import Path
import os
import sqlite3
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "daily_drum_check.py"


def test_daily_drum_check_reads_explicit_database_without_modifying_it():
    with tempfile.TemporaryDirectory() as temporary_dir:
        db_path = Path(temporary_dir) / "memory_drum.db"

        with sqlite3.connect(db_path) as conn:
            conn.execute(
                """
                CREATE TABLE entries (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT
                )
                """
            )
            conn.execute(
                "INSERT INTO entries (timestamp) VALUES (?)",
                ("2026-09-16T20:00:00+00:00",),
            )

        before = db_path.read_bytes()

        environment = os.environ.copy()
        environment["CANONICAL_DRUM"] = str(db_path)

        result = subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, result.stderr
        assert "Drum entries: 1" in result.stdout
        assert "Latest: 2026-09-16T20:00:00+00:00" in result.stdout
        assert db_path.read_bytes() == before


def test_daily_drum_check_fails_without_creating_missing_database():
    with tempfile.TemporaryDirectory() as temporary_dir:
        missing_path = Path(temporary_dir) / "missing-memory-drum.db"

        environment = os.environ.copy()
        environment["CANONICAL_DRUM"] = str(missing_path)

        result = subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "memory drum database not found" in result.stderr
        assert not missing_path.exists()
