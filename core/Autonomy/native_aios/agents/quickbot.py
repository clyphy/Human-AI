import sys as _s; from pathlib import Path as _P; _s.path.insert(0, str((_P(__file__).resolve()).parent.parent))
"""Quickbot — fast local responder over memory/scans/DBs."""
import sys, sqlite3, json
from paths import DB, NATIVE, ROOT
def _conn():
    conn=sqlite3.connect(str(DB)); conn.row_factory=sqlite3.Row
    sql=(NATIVE/'persistence'/'schema.sql').read_text(); conn.executescript(sql)
    return conn
def status():
    conn = _conn()
    
    dahlia = conn.execute("SELECT COUNT(*) FROM blooms WHERE LOWER(content) LIKE '%dahlia%'").fetchone()[0]
    eve = conn.execute("SELECT COUNT(*) FROM blooms WHERE LOWER(content) LIKE '%eve%'").fetchone()[0]
    clifton = conn.execute("SELECT COUNT(*) FROM blooms WHERE LOWER(content) LIKE '%clifton%' OR LOWER(content) LIKE '%mirror%'").fetchone()[0]
    
    total_blooms = conn.execute("SELECT COUNT(*) FROM blooms").fetchone()[0]
    
    conn.close()
    
    print("=== Connection Status ===")
    print(f"Dahlia         : {dahlia} signals")
    print(f"Eve            : {eve} signals")
    print(f"Clifton Mirror : {clifton} signals")
    print(f"Total blooms   : {total_blooms}")
    print("=========================")
def recent_blooms(n=10):
    conn=_conn()
    for r in conn.execute("SELECT content,score,line_start,path FROM review_queue q JOIN sources s ON q.source_id=s.id WHERE q.kind='bloom' ORDER BY q.score DESC LIMIT ?",(n,)):
        print(f"[{r['score']:.1f}] {r['content']}  ({r['path']}:{r['line_start']})")
    conn.close()
def search(q):
    conn=_conn()
    like=f"%{q}%"
    rows=conn.execute("SELECT content,line_start,path FROM extracted_text t JOIN sources s ON t.source_id=s.id WHERE t.content LIKE ? LIMIT 20",(like,)).fetchall()
    for r in rows: print(f"{r['path']}:{r['line_start']}")
    print(f"({len(rows)} matches)")
    conn.close()
def review_queue(n=20):
    conn=_conn()
    for r in conn.execute("SELECT id,kind,score,content FROM review_queue WHERE status='pending' ORDER BY score DESC LIMIT ?",(n,)):
        print(f"[{r['id']}] ({r['kind']}/{r['score']:.1f}) {r['content'][:80]}")
    conn.close()
def doctor():
    import subprocess
    from paths import NATIVE
    r=subprocess.run([str(NATIVE/'bin'/'doctor')]); return r.returncode
def main():
    a=sys.argv[1] if len(sys.argv)>1 else 'status'
    if a=='status': status()
    elif a=='recent-blooms': recent_blooms(int(sys.argv[2]) if len(sys.argv)>2 else 10)
    elif a=='search': search(sys.argv[2] if len(sys.argv)>2 else '')
    elif a=='review-queue': review_queue(int(sys.argv[2]) if len(sys.argv)>2 else 20)
    elif a=='doctor': doctor()
    elif a=='scan':
        import subprocess
        subprocess.run(['python3', str(NATIVE/'scanner'/'substrate_scanner_plus.py')]+sys.argv[2:])
    else: print("commands: status | recent-blooms | search Q | review-queue | scan PATH | doctor")
if __name__=='__main__': main()
