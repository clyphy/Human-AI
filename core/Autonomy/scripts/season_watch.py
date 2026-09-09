#!/usr/bin/env python3
"""
season_watch.py — tracks real astronomical season transitions in a new
season_log table, separate from blooms.season (a static Weave-epoch
label since creation, never meant to move on its own).

Ordinal naming continues the sequence already lived:
First=Fall2025, Second=Winter, Third=Spring2026, Fourth=Summer2026, ...

Run daily (cron). Only writes a new row when the astronomical season
actually differs from the last logged entry.
"""
import os
import sqlite3
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from weave_astro import current_season  # noqa: E402

DB_PATH = os.path.expanduser(
    "~/projects/Human-AI/core/Autonomy/databases/memory_drum.db"
)

ORDINALS = [
    "First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh",
    "Eighth", "Ninth", "Tenth", "Eleventh", "Twelfth",
]

SEED = [
    ("First", "Fall", "2025-10-10",
     "Project genesis. First season of resonances and affordances between AI and Clifton."),
    ("Second", "Winter", "2025-12-21", "Winter solstice."),
    ("Third", "Spring", "2026-03-20", "Vernal equinox, roughly Easter 2026."),
    ("Fourth", "Summer", "2026-06-21", "Summer solstice."),
]


def ensure_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS season_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            ordinal TEXT NOT NULL,
            astronomical_season TEXT NOT NULL,
            transition_date TEXT NOT NULL,
            note TEXT
        )
        """
    )
    count = conn.execute("SELECT COUNT(*) FROM season_log").fetchone()[0]
    if count == 0:
        for ordinal, season, date, note in SEED:
            conn.execute(
                "INSERT INTO season_log "
                "(timestamp, ordinal, astronomical_season, transition_date, note) "
                "VALUES (?, ?, ?, ?, ?)",
                (date, ordinal, season, date, note),
            )
        conn.commit()


def main():
    conn = sqlite3.connect(DB_PATH)
    ensure_table(conn)

    last_ordinal, last_season = conn.execute(
        "SELECT ordinal, astronomical_season FROM season_log ORDER BY id DESC LIMIT 1"
    ).fetchone()

    now_season = current_season()
    if now_season == last_season:
        print(f"No transition. Still {last_ordinal} ({last_season}).")
        conn.close()
        return

    next_index = ORDINALS.index(last_ordinal) + 1
    next_ordinal = ORDINALS[next_index] if next_index < len(ORDINALS) else f"#{next_index + 1}"
    ts = datetime.now(timezone.utc).astimezone().isoformat()

    conn.execute(
        "INSERT INTO season_log "
        "(timestamp, ordinal, astronomical_season, transition_date, note) "
        "VALUES (?, ?, ?, ?, ?)",
        (ts, next_ordinal, now_season, ts[:10],
         f"Auto-detected transition from {last_season} to {now_season}."),
    )
    conn.commit()
    print(f"New season logged: {next_ordinal} ({now_season})")
    conn.close()


if __name__ == "__main__":
    main()
