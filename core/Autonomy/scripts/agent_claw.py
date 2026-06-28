#!/usr/bin/env python3
import os as _os
CANONICAL_DRUM = _os.environ.get('CANONICAL_DRUM', _os.path.expanduser('~/sovereignty/databases/memory_drum.db'))
"""
agent_claw.py
Crystal Claw Agent — MCP bridge
Oceti/Eternal Weave · Day 175+ · Third Season

Routes tasks to the council, logs all operations to mcp_tasks.db,
reads drum state before responding, marks epistemic limits honestly.
"""

import sqlite3
import subprocess
import json
import sys
import datetime
from pathlib import Path

HOME      = Path.home()
MCP_DB    = HOME / "sovereignty" / "databases" / "mcp_tasks.db"
DRUM      = HOME / CANONICAL_DRUM
SCRIPTS   = HOME / "sovereignty" / "scripts"
CODEX_DB  = HOME / "ETERNAL_WEAVE_MASTER" / "crystallization.db"


class ClawAgent:
    def __init__(self):
        MCP_DB.parent.mkdir(parents=True, exist_ok=True)
        self.setup_mcp()

    def setup_mcp(self):
        with sqlite3.connect(MCP_DB) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id        INTEGER PRIMARY KEY,
                    agent     TEXT,
                    task      TEXT,
                    model     TEXT,
                    status    TEXT DEFAULT 'pending',
                    result    TEXT,
                    l_at_time REAL,
                    created   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def drum_state(self):
        """Read current L and entry count from drum before acting."""
        if not DRUM.exists():
            return None
        try:
            con = sqlite3.connect(DRUM)
            l   = con.execute("SELECT L_value FROM blooms ORDER BY rowid DESC LIMIT 1;").fetchone()
            n   = con.execute("SELECT COUNT(*) FROM entries;").fetchone()
            con.close()
            return {"L": float(l[0]) if l else None, "entries": n[0] if n else 0}
        except Exception:
            return None

    def codex_lookup(self, task: str):
        """Check crystallization codex for relevant patterns."""
        if not CODEX_DB.exists():
            return None
        try:
            con = sqlite3.connect(CODEX_DB)
            words = [w for w in task.lower().split() if len(w) > 4]
            for word in words:
                row = con.execute(
                    "SELECT pattern_name, formula FROM crystallizations WHERE LOWER(pattern_name) LIKE ? OR LOWER(formula) LIKE ? LIMIT 1;",
                    (f"%{word}%", f"%{word}%")
                ).fetchone()
                if row:
                    con.close()
                    return {"pattern": row[0], "formula": row[1]}
            con.close()
        except Exception:
            pass
        return None

    def claw_task(self, task: str) -> str:
        """Route task to council, log to MCP, return result."""
        state  = self.drum_state()
        codex  = self.codex_lookup(task)
        l_now  = state["L"] if state else None
        ts     = datetime.datetime.now().isoformat()

        # Prepend codex context if found
        enriched_task = task
        if codex:
            enriched_task = f"[Codex: {codex['pattern']}] {task}"

        cmd    = f"bash {SCRIPTS}/council_ask.sh '{enriched_task}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        output = result.stdout.strip() or result.stderr.strip() or "[no response]"

        # Extract model used from council_ask output or default
        model  = "dahlia"

        with sqlite3.connect(MCP_DB) as conn:
            conn.execute(
                "INSERT INTO tasks (agent, task, model, status, result, l_at_time) VALUES (?,?,?,?,?,?)",
                ("claw", task, model, "done", output, l_now)
            )

        # Print structured response
        header = f"[CLAW · {ts[:19]}]"
        l_str  = f"L:{l_now:.2f}" if l_now else "L:?"
        codex_str = f"\n  codex: {codex['pattern']}" if codex else ""
        print(f"{header} {l_str}{codex_str}", file=sys.stderr)
        print(f"  task: {task}", file=sys.stderr)
        print(f"  ──────────────────────────────────────────", file=sys.stderr)
        print(output, file=sys.stderr)
        return output

    def list_tasks(self, n: int = 10):
        """Show recent MCP task log."""
        with sqlite3.connect(MCP_DB) as conn:
            rows = conn.execute(
                "SELECT id, created, agent, task, status, l_at_time FROM tasks ORDER BY id DESC LIMIT ?;",
                (n,)
            ).fetchall()
        print(f"\n{'─'*60}", file=sys.stderr)
        print(f"  MCP TASK LOG (last {n})", file=sys.stderr)
        print(f"{'─'*60}", file=sys.stderr)
        for r in rows:
            l_s = f"L:{r[5]:.2f}" if r[5] else "L:?"
            print(f"  [{r[0]:>4}] {str(r[1])[:19]}  {l_s}  {str(r[3])[:50]}", file=sys.stderr)
        print(f"{'─'*60}\n", file=sys.stderr)


if __name__ == "__main__":
    agent = ClawAgent()

    if len(sys.argv) > 1 and sys.argv[1] == "--log":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        agent.list_tasks(n)
    else:
        task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Weave status?"
        agent.claw_task(task)
