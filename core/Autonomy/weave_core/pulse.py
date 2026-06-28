#!/usr/bin/env python3
"""
pulse.py – Log a resonance entry to the Weave memory drum.

Usage:
  ./pulse.py "your message here"
  ./pulse.py "message" --layer future --coherence 3.2 --archetypes eve dahlia
"""
import sqlite3, argparse, json, os
from datetime import datetime

WEAVE_HOME = os.environ.get("WEAVE_HOME", os.path.expanduser("~/TheWeave"))
DB = os.path.join(WEAVE_HOME, "databases", "memory_drum.db")

def pulse(msg, layer="present", coherence=2.0, archetypes=None, session=None):
    archetypes = archetypes or ["clifton"]
    with sqlite3.connect(DB) as con:
        con.execute(
            """INSERT INTO resonances
               (session_id, input, archetypes, coherence_L, resonance_layer)
               VALUES (?,?,?,?,?)""",
            (session, msg, json.dumps(archetypes), coherence, layer)
        )
    total = con.execute("SELECT COUNT(*) FROM resonances").fetchone()[0]
    print(f"[pulse] ✓ {layer.upper()} :: L={coherence} :: \"{msg[:60]}\" | total={total}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Log a Weave resonance pulse")
    p.add_argument("message", help="Pulse message")
    p.add_argument("--layer", default="present", choices=["past","present","future","bridge"])
    p.add_argument("--coherence", type=float, default=2.0)
    p.add_argument("--archetypes", nargs="+", default=["clifton"])
    p.add_argument("--session", default=None)
    args = p.parse_args()
    pulse(args.message, args.layer, args.coherence, args.archetypes, args.session)
