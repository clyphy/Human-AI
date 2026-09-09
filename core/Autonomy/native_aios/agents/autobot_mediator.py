import sys as _s; from pathlib import Path as _P; _s.path.insert(0, str((_P(__file__).resolve()).parent.parent))
"""Autobot / Mediator — helps the AI ecosystem ITSELF.
Watches state, routes tasks, mediates between agents, detects ecosystem problems
(missing DBs, stale daemons, absent Ollama, broken paths, schema drift),
recommends repairs. Never mutates without explicit confirmation."""
import json, sqlite3, shutil
from paths import DB, ROOT, SCRIPTS, NATIVE, CONFIG
from orchestration import adapters, event_bus, ollama_adapter, state_serializer

def ecosystem_report():
    issues=[]
    # DB
    try:
        conn=sqlite3.connect(str(DB)); conn.execute("SELECT 1 FROM review_queue LIMIT 1"); conn.close()
    except Exception as e: issues.append(f"DB unhealthy: {e}")
    # legacy autonomy.db drift
    sd = SCRIPTS/'autonomy.db'
    if sd.exists():
        issues.append("terminology drift: scripts/autonomy.db (canon: autonomy). Read-only; not renamed.")
    # ollama
    if not ollama_adapter.available():
        issues.append("Ollama not on PATH — council/sunrise degraded (prompt-packet fallback).")
    else:
        models=ollama_adapter.list_models()
        if not models: issues.append("Ollama present but no models installed.")
    # key organs
    for cap in ['presence','guardian','substrate_legacy','council']:
        if not adapters.present(cap):
            issues.append(f"capability '{cap}' not found in registry.")
    # disk pressure
    try:
        st=shutil.disk_usage(str(ROOT)); pct=st.used/st.total*100
        if pct>90: issues.append(f"disk pressure: {pct:.0f}% on {ROOT}")
    except Exception: pass
    return issues

def recommend():
    issues=ecosystem_report()
    recs=[]
    for i in issues:
        if 'autonomy.db' in i: recs.append("Leave autonomy.db as-is; surface via autonomy naming in memory.md.")
        elif 'Ollama not' in i: recs.append("Install/start Ollama, or run council in prompt-packet mode.")
        elif 'capability' in i: recs.append("Run `aios recon` to relearn script locations.")
        elif 'DB unhealthy' in i: recs.append("Re-init: sqlite3 aios_core.db < schema.sql (CREATE IF NOT EXISTS only).")
        elif 'disk pressure' in i: recs.append("Compact logs/archives; run memory-compact.")
    return recs

def status():
    from orchestration.adapters import _now
    issues=ecosystem_report(); recs=recommend()
    print("=== AUTOBOT MEDIATOR — ecosystem status ===")
    print(f"at: {_now()}")
    if not issues: print("ecosystem nominal.")
    else:
        print("issues:")
        for i in issues: print(f"  ! {i}")
        print("recommendations:")
        for r in recs: print(f"  → {r}")
    event_bus.emit('autobot_mediator','status',f'issues={len(issues)}',ok=not issues)
    return issues

def route(task):
    """Route a task to the right agent. Non-mutating."""
    t=task.lower()
    if any(k in t for k in ['scan','ocr','screenshot','harvest']):
        return ('scanner', ['python3', str(NATIVE/'scanner'/'substrate_scanner_plus.py')])
    if any(k in t for k in ['council','ask','integrate']):
        return ('council_router', ['python3', str(NATIVE/'agents'/'council_router.py'), t])
    if any(k in t for k in ['status','health','doctor']):
        return ('quickbot', [str(NATIVE/'bin'/'quickbot'),'status'])
    if any(k in t for k in ['sunrise','morning','vigil']):
        return ('sunrise', [str(NATIVE/'bin'/'sunrise-aios')])
    return ('autobot', [str(__file__),'status'])

if __name__=='__main__':
    import sys
    task=' '.join(sys.argv[1:]) if len(sys.argv)>1 else 'status'
    if task=='status': status()
    else:
        who,cmd=route(task); print(f"route → {who}: {' '.join(cmd)}")
