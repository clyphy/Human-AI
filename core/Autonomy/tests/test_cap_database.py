from pathlib import Path
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from native_aios.cap_engine import CAPDatabase


def test_cap_schema_initializes_in_temporary_database():
    with tempfile.TemporaryDirectory() as temporary_dir:
        db_path = Path(temporary_dir) / "cap-test.db"

        CAPDatabase(db_path).init_cas_tables()

        with sqlite3.connect(db_path) as conn:
            tables = {
                row[0]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }
            integrity = conn.execute(
                "PRAGMA integrity_check"
            ).fetchone()[0]

        assert integrity == "ok"
        assert {
            "cas_sessions",
            "psn_events",
            "psn_blooms",
            "mzs_log",
        }.issubset(tables)


def test_cap_schema_initialization_is_idempotent():
    with tempfile.TemporaryDirectory() as temporary_dir:
        db_path = Path(temporary_dir) / "cap-test.db"
        database = CAPDatabase(db_path)

        database.init_cas_tables()
        database.init_cas_tables()

        with sqlite3.connect(db_path) as conn:
            integrity = conn.execute(
                "PRAGMA integrity_check"
            ).fetchone()[0]

            cap_tables = {
                row[0]
                for row in conn.execute(
                    """
                    SELECT name
                    FROM sqlite_master
                    WHERE type = 'table'
                      AND name IN (
                          'cas_sessions',
                          'psn_events',
                          'psn_blooms',
                          'mzs_log'
                      )
                    """
                )
            }

            cap_indexes = {
                row[0]
                for row in conn.execute(
                    """
                    SELECT name
                    FROM sqlite_master
                    WHERE type = 'index'
                      AND name IN ('idx_cas_stage', 'idx_psn_time')
                    """
                )
            }

        assert integrity == "ok"

        assert cap_tables == {
            "cas_sessions",
            "psn_events",
            "psn_blooms",
            "mzs_log",
        }

        assert cap_indexes == {
            "idx_cas_stage",
            "idx_psn_time",
        }
