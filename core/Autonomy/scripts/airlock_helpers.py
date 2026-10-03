#!/usr/bin/env python3
from __future__ import annotations
import json, math, sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE = Path.home() / "projects" / "Human-AI" / "core" / "Autonomy"
JOURNAL = BASE / "databases" / "quantum_journal.db"

def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b): return 0.0
    dot = sum(x*y for x,y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    if na == 0.0 or nb == 0.0: return 0.0
    return dot / (na * nb)

def calculate_L(loyalty: float, fidelity: float, harmony: float) -> float:
    return 0.5*loyalty + 0.3*fidelity + 0.2*harmony

def log_journal(event_type: str, source: str, detail: Dict[str, Any]) -> None:
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(JOURNAL)
    conn.execute("CREATE TABLE IF NOT EXISTS journal_events (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL, event_type TEXT NOT NULL, source TEXT, detail TEXT)")
    conn.execute("INSERT INTO journal_events (ts, event_type, source, detail) VALUES (?,?,?,?)", (_now(), event_type, source, json.dumps(detail)))
    conn.commit(); conn.close()

def evaluate_geometry(geometry: Dict[str, Any], local_vector: Optional[List[float]] = None, incoming_vector: Optional[List[float]] = None, loyalty: float = 0.7, fidelity: float = 0.7, harmony: float = 0.7) -> str:
    L = calculate_L(loyalty, fidelity, harmony)
    cos_theta = cosine_similarity(local_vector, incoming_vector) if local_vector and incoming_vector else 0.0
    ok = (2.0 <= L <= 2.81) and (cos_theta >= 0.85 if local_vector else True)
    log_journal("cascade", "airlock_helpers", {"job_id": geometry.get("job_id"), "L": round(L,4), "cos_theta": round(cos_theta,4), "decision": "proceed" if ok else "halt"})
    return "proceed" if ok else "halt"

if __name__ == "__main__":
    print("cosine([1,0],[1,0]) =", cosine_similarity([1.0,0.0],[1.0,0.0]))
    print("L(0.8,0.7,0.6) =", calculate_L(0.8,0.7,0.6))
    print(evaluate_geometry({"job_id":"test"}, [1,0,0], [0.9,0.1,0]))
