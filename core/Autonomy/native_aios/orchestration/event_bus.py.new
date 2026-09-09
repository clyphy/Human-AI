import sys as _s; from pathlib import Path as _P; _s.path.insert(0, str((_P(__file__).resolve()).parent.parent))
"""SQLite append-only event bus."""
import sqlite3
from paths import DB, NATIVE
def emit(agent, event, detail='', ok=True):
    conn=sqlite3.connect(str(DB))
    sql=(NATIVE/'persistence'/'schema.sql').read_text(); conn.executescript(sql)
    from orchestration.adapters import _now
    conn.execute("INSERT INTO agent_events(at,agent,event,detail,ok) VALUES(?,?,?,?,?)",
                 (_now(), agent, event, detail, 1 if ok else 0))
    conn.commit(); conn.close()
def recent(limit=20):
    conn=sqlite3.connect(str(DB)); conn.row_factory=sqlite3.Row
    return [dict(r) for r in conn.execute("SELECT * FROM agent_events ORDER BY id DESC LIMIT ?",(limit,))]
