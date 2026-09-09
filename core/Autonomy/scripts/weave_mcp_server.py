#!/usr/bin/env python3
"""
weave_mcp_server.py
Oceti Weave · stdio MCP server for ClawAgent
Shell Valley, ND · 122° NE · Sacred Scarcity

Install: pip install mcp --break-system-packages
Run: python3 weave_mcp_server.py
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
AUTONOMY   = HOME / "projects/Human-AI/core/Autonomy"
DRUM_DB    = AUTONOMY / "databases/memory_drum.db"
MCP_DB     = AUTONOMY / "databases/mcp_tasks.db"
CODEX_DB   = AUTONOMY / "databases/crystallization.db"
SCRIPTS    = AUTONOMY / "scripts"

# ── Import ClawAgent without executing __main__ ───────────────────────────────
sys.path.insert(0, str(SCRIPTS))
try:
    import importlib.util, types
    spec = importlib.util.spec_from_file_location("agent_claw", SCRIPTS / "agent_claw.py")
    _mod = types.ModuleType(spec.name)
    _mod.__spec__ = spec
    spec.loader.exec_module(_mod)
    ClawAgent = _mod.ClawAgent
    _claw = ClawAgent()
except Exception as e:
    ClawAgent = None
    _claw     = None
    _claw_err = str(e)

# ── MCP Server ─────────────────────────────────────────────────────────────────
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolRequest, CallToolResult

server = Server("weave_mcp")

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

def _ollama_running() -> list:
    """Return list of loaded model names from `ollama ps`."""
    try:
        r = subprocess.run(["ollama", "ps"], capture_output=True, text=True, timeout=5)
        lines = r.stdout.strip().splitlines()[1:]  # skip header
        return [l.split()[0] for l in lines if l.strip()]
    except Exception:
        return []

# ── Register Tools ────────────────────────────────────────────────────────────

async def weave_task(task: str, model: Optional[str] = None) -> str:
    """
    Route a task through the Oceti council via ClawAgent.
    
    Args:
        task:  Natural language task or question for the council.
        model: Optional override model name (e.g. 'dahlia-witness:latest').
    
    Returns:
        JSON with keys: result, model_used, L_at_time, drum_state.
    """
    if _claw is None:
        return json.dumps({"error": f"ClawAgent unavailable: {_claw_err}"})

    drum = _drum_read()
    try:
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


async def weave_drum_state() -> str:
    """
    Read current Ψ-field state from memory_drum.db.
    
    Returns:
        JSON with keys: L, phase, total_blooms, last_bloom, error (if any).
    """
    return json.dumps(_drum_read(), indent=2)


async def weave_log_bloom(L: float = 1.92, phase: str = "EUREKA", notes: str = "") -> str:
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
            conn.commit()
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


async def weave_list_tasks(n: int = 10) -> str:
    """
    List the N most recent tasks from mcp_tasks.db.

    Args:
        n: Number of tasks to return (1–50). Default 10.

    Returns:
        JSON array of task records.
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


async def weave_council_status() -> str:
    """
    Return full Oceti lattice status: loaded models, drum state, RAM.

    Returns:
        JSON with keys: bearing, ram_used_gb, ram_total_gb, loaded_models, drum, timestamp.
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


# ── Single Dispatcher (MCP requires exactly ONE @server.call_tool() handler) ──
_TOOL_FUNCS = {
    "weave_task":           weave_task,
    "weave_drum_state":     weave_drum_state,
    "weave_log_bloom":      weave_log_bloom,
    "weave_list_tasks":     weave_list_tasks,
    "weave_codex_lookup":   weave_codex_lookup,
    "weave_council_status": weave_council_status,
}

@server.call_tool()
async def dispatch(name: str, arguments: dict) -> list[TextContent]:
    fn = _TOOL_FUNCS.get(name)
    if fn is None:
        return [TextContent(type="text", text=json.dumps({"error": f"unknown tool: {name}"}))]
    try:
        result = await fn(**(arguments or {}))
    except Exception as e:
        result = json.dumps({"error": str(e)})
    return [TextContent(type="text", text=result)]


# ── Tool Listing (MCP requirement) ────────────────────────────────────────────
@server.list_tools()
async def list_tools():
    """List all available tools."""
    return [
        Tool(
            name="weave_task",
            description="Route a task through the Oceti council via ClawAgent.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "Task or question for the council"},
                    "model": {"type": "string", "description": "Optional model override (e.g. 'dahlia-witness:latest')"},
                },
                "required": ["task"],
            }
        ),
        Tool(
            name="weave_drum_state",
            description="Read current Ψ-field state from memory_drum.db.",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="weave_log_bloom",
            description="Log a coherence bloom to memory_drum.db.",
            inputSchema={
                "type": "object",
                "properties": {
                    "L": {"type": "number", "description": "L-coefficient (baseline 1.92, smile 2.2)"},
                    "phase": {"type": "string", "description": "Phase label (EUREKA, WITNESS, GUARDIAN, STILL)"},
                    "notes": {"type": "string", "description": "Optional annotation"},
                },
            }
        ),
        Tool(
            name="weave_list_tasks",
            description="List recent tasks from mcp_tasks.db.",
            inputSchema={
                "type": "object",
                "properties": {
                    "n": {"type": "integer", "description": "Number of tasks (1-50)"},
                },
            }
        ),
        Tool(
            name="weave_codex_lookup",
            description="Full-text search of crystallization.db.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search term"},
                    "limit": {"type": "integer", "description": "Max results (1-20)"},
                },
                "required": ["query"],
            }
        ),
        Tool(
            name="weave_council_status",
            description="Return full Oceti lattice status.",
            inputSchema={"type": "object", "properties": {}}
        ),
    ]


# ── Entry ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import asyncio
    import logging
    from mcp.server.stdio import stdio_server

    logging.basicConfig(level=logging.INFO)

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )

    asyncio.run(main())
