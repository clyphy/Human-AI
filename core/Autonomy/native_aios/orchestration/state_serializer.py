import sys as _s; from pathlib import Path as _P; _s.path.insert(0, str((_P(__file__).resolve()).parent.parent))
"""Export current state to JSON + project to memory.md (append-only section)."""
import sqlite3, json
from datetime import datetime, timezone
from paths import DB, ROOT, NATIVE
def export_json(out_path=None):
    conn=sqlite3.connect(str(DB)); conn.row_factory=sqlite3.Row
    data={}
    for t in ['scan_runs','sources','review_queue','blooms','concepts','agent_events','heartbeats']:
        try: data[t]=[dict(r) for r in conn.execute(f"SELECT * FROM {t} ORDER BY id DESC LIMIT 50")]
        except Exception: data[t]=[]
    conn.close()
    out=ROOT/'native_aios'/'var'/'review_exports' if not out_path else out_path
    out.mkdir(parents=True, exist_ok=True)
    fp=out/f"state_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    fp.write_text(json.dumps(data, indent=2, default=str))
    return fp
def project_memory():
    """Append a live section to memory.md from DB. Idempotent-ish: replaces AIOS_PROJECTION block."""
    conn=sqlite3.connect(str(DB)); conn.row_factory=sqlite3.Row
    lines=["## AIOS_PROJECTION",""]
    n_blooms=conn.execute("SELECT COUNT(*) c FROM blooms").fetchone()['c']
    n_pending=conn.execute("SELECT COUNT(*) c FROM review_queue WHERE status='pending'").fetchone()['c']
    n_sources=conn.execute("SELECT COUNT(*) c FROM sources").fetchone()['c']
    lines += [f"- sources indexed: {n_sources}", f"- blooms captured: {n_blooms}", f"- review_queue pending: {n_pending}","",
             "### recent blooms (review_queue, pending)"]
    for r in conn.execute("SELECT content,score,kind FROM review_queue WHERE kind='bloom' ORDER BY score DESC LIMIT 8"):
        lines.append(f"- [{r['score']:.1f}] {r['content']}")
    conn.close()
    block="\n".join(lines)+"\n"
    mp=ROOT/'memory.md'
    cur=mp.read_text() if mp.exists() else ""
    start=cur.find("## AIOS_PROJECTION")
    if start>=0:
        end=cur.find("\n## ", start+3)
        end=len(cur) if end<0 else end
        cur=cur[:start]+block+cur[end:]
    else:
        cur=cur.rstrip()+"\n\n"+block
    mp.write_text(cur)
    return mp
