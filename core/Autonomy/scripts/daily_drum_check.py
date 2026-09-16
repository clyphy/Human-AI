#!/usr/bin/env python3
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DRUM_PATH = PROJECT_ROOT / "databases" / "memory_drum.db"


def main() -> int:
    drum_path = Path(
        __import__("os").environ.get("CANONICAL_DRUM", DEFAULT_DRUM_PATH)
    ).expanduser()

    if not drum_path.is_file():
        print(f"error: memory drum database not found: {drum_path}", file=sys.stderr)
        return 1

    database_uri = f"{drum_path.resolve().as_uri()}?mode=ro"

    try:
        with sqlite3.connect(database_uri, uri=True) as conn:
            count, latest = conn.execute(
                "SELECT COUNT(*), MAX(timestamp) FROM entries"
            ).fetchone()
    except sqlite3.Error as exc:
        print(f"error: could not read memory drum: {exc}", file=sys.stderr)
        return 1

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(
        f"Drum entries: {count} | "
        f"Latest: {latest or 'None'} | "
        f"checked_at_utc: {now}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
