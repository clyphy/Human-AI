import sys as _s; from pathlib import Path as _P; _s.path.insert(0, str((_P(__file__).resolve()).parent.parent))
"""Defensive capability->script adapters. Probe registry; first existing+exec wins."""
import json, subprocess, os, time
from paths import CONFIG, SCRIPTS, ROOT
REG = json.loads((CONFIG/'existing_script_registry.json').read_text())
LOG = ROOT/'native_aios'/'logs'/'adapter.log'
# Capabilities that mutate state/files — require explicit allow_mutate=True.
MUTATING = {'build_facets', 'bridge', 'dream', 'mcp', 'sunrise_patch', 'quarantine'}
def _log(agent, event, detail, ok):
    import sqlite3
    from paths import DB, NATIVE
    try:
        conn=sqlite3.connect(str(DB))
        sql=(NATIVE/'persistence'/'schema.sql').read_text(); conn.executescript(sql)
        conn.execute("INSERT INTO agent_events(at,agent,event,detail,ok) VALUES(?,?,?,?,?)",
                     (_now(), agent, event, detail, 1 if ok else 0)); conn.commit(); conn.close()
    except Exception: pass
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG,'a') as f: f.write(f"{_now()} {agent} {event} ok={ok} {detail}\n")
def _now():
    from datetime import datetime,timezone; return datetime.now(timezone.utc).isoformat(timespec='seconds')
def resolve(capability):
    for rel in REG.get(capability, []):
        p = ROOT/rel if not rel.startswith('/') else Path(rel)
        if p.exists():
            return p
    return None
def call(capability, args=None, timeout=120, allow_exec=True, allow_mutate=False):
    """Run the first available script for a capability. Returns (rc, stdout, stderr, path).
    Refuses mutating capabilities unless allow_mutate=True."""
    p = resolve(capability)
    if p is None:
        _log('adapter', f'capability_missing:{capability}', '', False)
        return (127, '', f'no script for capability: {capability}', None)
    if capability in MUTATING and not allow_mutate:
        _log('adapter', f'refused_mutating:{capability}', str(p), False)
        return (126, '', f'mutating capability {capability!r} requires allow_mutate=True', p)
    if not allow_exec:
        _log('adapter', f'dry_probe:{p.name}', str(p), True); return (0,'',str(p),p)
    try:
        r = subprocess.run(_build_cmd(p, args), capture_output=True, text=True, timeout=timeout)
        _log('adapter', f'called:{p.name}', f'rc={r.returncode}', r.returncode==0)
        return (r.returncode, r.stdout, r.stderr, p)
    except subprocess.TimeoutExpired:
        _log('adapter', f'timeout:{p.name}', str(args), False)
        return (124,'',f'timeout after {timeout}s', p)
    except Exception as e:
        _log('adapter', f'error:{p.name}', str(e), False)
        return (1,'',str(e), p)
def _build_cmd(p, args):
    if p.suffix=='.py':
        return ['python3', str(p)] + (args or [])
    return ['bash', str(p)] + (args or [])
def present(capability): return resolve(capability) is not None
