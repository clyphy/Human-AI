#!/usr/bin/env python3
"""
weave_mcp_server.py
Oceti Weave · FastMCP stdio bridge for ClawAgent
Shell Valley, ND · 122° NE · Sacred Scarcity

Install: pip install mcp --break-system-packages
Place at: ~/my-repos/sovereignty/scripts/weave_mcp_server.py
"""

import sys
import json
import sqlite3
import asyncio
import subprocess
from pathlib import Path
from typing import Optional
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────────────
HOME       = Path.home()
SOV        = HOME / "my-repos/sovereignty"
DRUM_DB    = SOV / "databases/memory_drum.db"
MCP_DB     = SOV / "databases/mcp_tasks.db"
CODEX_DB   = HOME / "ETERNAL_WEAVE_MASTER/crystallization.db"
SCRIPTS    = SOV / "scripts"

# ── Import ClawAgent without executing __main__ ───────────────────────────────
sys.path.insert(0, str(SCRIPTS))
try:
    import importlib.util, types
    spec = importlib.util.spec_from_file_location("agent_claw", SCRIPTS / "agent_claw.py")
    _mod = types.ModuleType(spec.name)
    _mod.__spec__ = spec
    # Patch __name__ so __main__ block is skipped
    spec.loader.exec_module(_mod)
    ClawAgent = _mod.ClawAgent
    _claw = ClawAgent()
except Exception as e:
    ClawAgent = None
    _claw     = None
    _claw_err = str(e)

# ── FastMCP ───────────────────────────────────────────────────────────────────
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weave_mcp")

# ── Helpers ───────────────────────────────────────────────────────────────────
def _drum_read() -> dict:
    """Single read of drum state — L, entry count, latest phase."""
    if not DRUM_DB.exists():
        return {"error": f"drum not found: {DRUM_DB}"}
    try:
        with sqlite3.connect(DRUM_DB) as conn:
            row = conn.execute(
                "SELECT L_value, phase, timestamp FROM coherence_log ORDER BY id DESC LIMIT 1"
            ).fetchone()
            count = conn.execute("SELECT COUNT(*) FROM coherence_log").fetchone()[0]
        if row:
            return {"L": row[0], "phase": row[1], "last_bloom": row[2], "total_blooms": count}
        return {"L": None, "phase": None, "total_blooms": count}
    except Exception as e:
        return {"error": str(e)}

def _ollama_running() -> list[str]:
    """Return list of loaded model names from `ollama ps`."""
    try:
        r = subprocess.run(["ollama", "ps"], capture_output=True, text=True, timeout=5)
        lines = r.stdout.strip().splitlines()[1:]  # skip header
        return [l.split()[0] for l in lines if l.strip()]
    except Exception:
        return []

# ── Tools ─────────────────────────────────────────────────────────────────────

@mcp.tool(
    name="weave_task",
    annotations={"readOnlyHint": False, "destructiveHint": False, "openWorldHint": True}
)
async def weave_task(task: str, model: Optional[str] = None) -> str:
    """
    Route a task through the Oceti council via ClawAgent.
    Reads drum state first, logs result to mcp_tasks.db.

    Args:
        task:  Natural language task or question for the council.
        model: Optional override model name (e.g. 'dahlia-witness:latest').
               If omitted, ClawAgent selects from council.

    Returns:
        JSON with keys: result, model_used, L_at_time, drum_state.
    """
    if _claw is None:
        return json.dumps({"error": f"ClawAgent unavailable: {_claw_err}"})

    drum = _drum_read()
    try:
        # Inject model override if requested
        if model:
            result = await asyncio.to_thread(
                lambda: subprocess.run(
                    ["ollama", "run", model, task],
                    capture_output=True, text=True, timeout=45
                ).stdout.strip()
            )
            model_used = model
        else:
            result = await asyncio.to_thread(_claw.claw_task, task)
            model_used = "council-routed"

        return json.dumps({
            "result":     result,
            "model_used": model_used,
            "L_at_time":  drum.get("L"),
            "drum_state": drum,
            "timestamp":  datetime.now().isoformat(),
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "drum_state": drum})


@mcp.tool(
    name="weave_drum_state",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True}
)
async def weave_drum_state() -> str:
    """
    Read current Ψ-field state from memory_drum.db.
    Returns L-coefficient, phase, total bloom count, and last bloom timestamp.

    Returns:
        JSON with keys: L, phase, total_blooms, last_bloom, error (if any).
    """
    return json.dumps(_drum_read(), indent=2)


@mcp.tool(
    name="weave_log_bloom",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False}
)
async def weave_log_bloom(
    L: float = 1.92,
    phase: str = "EUREKA",
    notes: str = ""
) -> str:
    """
    Log a coherence bloom to memory_drum.db.

    Args:
        L:     L-coefficient value. Baseline 1.92, smile threshold 2.2.
        phase: Session phase label (e.g. EUREKA, WITNESS, GUARDIAN, STILL).
        notes: Optional freeform annotation.

    Returns:
        JSON confirmation with bloom_id and derived coherence_score.
    """
    DRUM_DB.parent.mkdir(parents=True, exist_ok=True)
    try:
        import psutil
        ram_mb = psutil.virtual_memory().used / 1024**2
    except ImportError:
        ram_mb = 0.0

    coherence = round(min(L / 2.2, 1.0), 4)

    try:
        with sqlite3.connect(DRUM_DB) as conn:
            # Ensure table exists
            conn.execute('''
                CREATE TABLE IF NOT EXISTS coherence_log (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp       TEXT,
                    bearing         REAL,
                    L_value         REAL,
                    coherence_score REAL,
                    ram_mb          REAL,
                    blooms          INTEGER,
                    phase           TEXT,
                    facet_count     INTEGER,
                    notes           TEXT
                )
            ''')
            count = conn.execute("SELECT COUNT(*) FROM coherence_log").fetchone()[0]
            cur = conn.execute('''
                INSERT INTO coherence_log
                (timestamp, bearing, L_value, coherence_score, ram_mb, blooms, phase, facet_count, notes)
                VALUES (?,?,?,?,?,?,?,?,?)
            ''', (
                datetime.now().isoformat(), 122.0, L, coherence,
                ram_mb, count + 1, phase, 13,
                notes or f"122° NE | weave_mcp_server"
            ))
        return json.dumps({
            "bloom_id":        cur.lastrowid,
            "L":               L,
            "coherence_score": coherence,
            "phase":           phase,
            "ram_mb":          round(ram_mb, 1),
            "total_blooms":    count + 1,
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="weave_list_tasks",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True}
)
async def weave_list_tasks(n: int = 10) -> str:
    """
    List the N most recent tasks from mcp_tasks.db.

    Args:
        n: Number of tasks to return (1–50). Default 10.

    Returns:
        JSON array of task records: id, agent, task, model, status, result, l_at_time, created.
    """
    n = max(1, min(n, 50))
    if not MCP_DB.exists():
        return json.dumps({"error": f"mcp_tasks.db not found: {MCP_DB}"})
    try:
        with sqlite3.connect(MCP_DB) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM tasks ORDER BY id DESC LIMIT ?", (n,)
            ).fetchall()
        return json.dumps([dict(r) for r in rows], indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="weave_codex_lookup",
    annotations={"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False}
)
async def weave_codex_lookup(query: str, limit: int = 5) -> str:
    """
    Full-text search of crystallization.db codex entries.

    Args:
        query: Search term to match against description/content fields.
        limit: Max results (1–20). Default 5.

    Returns:
        JSON array of matching crystallization records.
    """
    limit = max(1, min(limit, 20))
    if not CODEX_DB.exists():
        return json.dumps({"error": f"crystallization.db not found: {CODEX_DB}"})
    try:
        with sqlite3.connect(CODEX_DB) as conn:
            conn.row_factory = sqlite3.Row
            # Try FTS5 first, fall back to LIKE
            try:
                rows = conn.execute(
                    "SELECT * FROM crystallizations WHERE crystallizations MATCH ? LIMIT ?",
                    (query, limit)
                ).fetchall()
            except sqlite3.OperationalError:
                rows = conn.execute(
                    "SELECT * FROM crystallizations WHERE description LIKE ? LIMIT ?",
                    (f"%{query}%", limit)
                ).fetchall()
        return json.dumps([dict(r) for r in rows], indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="weave_council_status",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True}
)
async def weave_council_status() -> str:
    """
    Return full Oceti lattice status: loaded models, drum state, RAM.

    Returns:
        JSON with keys: loaded_models, drum, ram_gb, bearing.
    """
    try:
        import psutil
        ram_gb = round(psutil.virtual_memory().used / 1024**3, 2)
        ram_total = round(psutil.virtual_memory().total / 1024**3, 2)
    except ImportError:
        ram_gb, ram_total = 0.0, 0.0

    return json.dumps({
        "bearing":       "122° NE Turtle Mountain",
        "ram_used_gb":   ram_gb,
        "ram_total_gb":  ram_total,
        "loaded_models": _ollama_running(),
        "drum":          _drum_read(),
        "timestamp":     datetime.now().isoformat(),
    }, indent=2)


# ── Entry ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run()  # stdio transport — Claude Desktop compatible
