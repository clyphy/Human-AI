#!/usr/bin/env python3
import sys as _s; from pathlib import Path as _P; _s.path.insert(0, str((_P(__file__).resolve()).parent.parent))
import sys, os, json, sqlite3, argparse, fcntl, time
from pathlib import Path
from paths import ROOT, SCRIPTS, DB, CONFIG, LOGS, LOCKS, NATIVE
from scanner.ocr_adapter import ocr_image, install_hint
from scanner.metadata import sha256_file, git_info, image_dims, now_iso
from scanner.bloom_extractor import extract_findings
from scanner.redaction import redact, contains_secret

CFG = json.loads((CONFIG/'aios_config.json').read_text())
SCAN_ROOTS = json.loads((CONFIG/'scan_roots.json').read_text())

def connect():
    conn = sqlite3.connect(str(DB)); conn.row_factory=sqlite3.Row
    sql = (NATIVE/'persistence'/'schema.sql').read_text()
    conn.executescript(sql); conn.commit(); return conn

def acquire_lock():
    LOCKS.mkdir(parents=True, exist_ok=True)
    lf = open(LOCKS/'scan.lock','w')
    try:
        fcntl.flock(lf, fcntl.LOCK_EX|fcntl.LOCK_NB); return lf
    except BlockingIOError:
        print("scan already running (lock held).", file=sys.stderr); sys.exit(1)

def iter_files(paths, exts, skip_dirs):
    for base in paths:
        base = Path(base)
        if base.is_file(): yield base; continue
        for dp, dns, fns in os.walk(base):
            dns[:] = [d for d in dns if d not in skip_dirs]
            for fn in fns:
                p = Path(dp)/fn
                if p.suffix.lower() in exts: yield p

def ingest_text(conn, run_id, path, text, source_type='text', ocr_engine=None):
    sha, size = sha256_file(path)
    if sha is None: return 0
    existing = conn.execute("SELECT id FROM sources WHERE sha256=?", (sha,)).fetchone()
    if existing: return 0
    gi = git_info(str(path))
    iw, ih = (None, None)
    if source_type=='ocr': iw, ih = image_dims(str(path))
    cur = conn.execute(
        "INSERT INTO sources(run_id,path,sha256,size,mtime,ext,source_type,ocr_engine,image_w,image_h,git_repo,git_branch,git_commit,scanned_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (run_id, str(path), sha, size, int(path.stat().st_mtime) if path.exists() else None, path.suffix.lower(), source_type, ocr_engine, iw, ih, gi.get('repo'), gi.get('branch'), gi.get('commit'), now_iso()))
    sid = cur.lastrowid
    chash = __import__('hashlib').sha256(text.encode('utf-8','ignore')).hexdigest()[:16]
    conn.execute("INSERT INTO extracted_text(source_id,line_start,line_end,content,content_hash) VALUES(?,?,?,?,?)", (sid, None, None, text[:200000], chash))
    findings, flags = extract_findings(text)
    for f in findings:
        content = f['content']
        redacted = 0
        if contains_secret(content): content = redact(content); redacted = 1
        conn.execute("INSERT INTO review_queue(source_id,kind,content,score,context,line_start,line_end,terminology_flags,redacted,status,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                     (sid, f['kind'], content, f.get('score',0), f.get('context'), f.get('line_start'), f.get('line_end'), json.dumps(flags), redacted, 'pending', now_iso()))
        if f['kind']=='bloom':
            conn.execute("INSERT INTO blooms(source_id,content,trigger,score) VALUES(?,?,?,?)", (sid, content, f.get('trigger',''), f.get('score',0)))
        elif f['kind']=='code':
            conn.execute("INSERT OR IGNORE INTO code_snippets(source_id,language,content,content_hash,line_start,line_end) VALUES(?,?,?,?,?,?)", (sid, f.get('language','?'), content, f.get('content_hash'), f.get('line_start'), f.get('line_end')))
        elif f['kind']=='formula':
            conn.execute("INSERT OR IGNORE INTO formulas(source_id,content,content_hash,line_start) VALUES(?,?,?,?)", (sid, content, f.get('content_hash'), f.get('line_start')))
        elif f['kind']=='concept':
            conn.execute("INSERT INTO concepts(source_id,term,occurrence_count) VALUES(?,?,?)", (sid, content, f.get('occurrence_count',1)))
        elif f['kind']=='timestamp':
            conn.execute("INSERT INTO timestamps(source_id,raw,iso,line) VALUES(?,?,?,?)", (sid, content, None, f.get('line_start')))
    return len(findings)

def scan(paths, deep=False, use_legacy=False, dry_run=False):
    if dry_run: print("DRY RUN ENABLED: No database writes will occur.")
    lf = None if dry_run else acquire_lock()
    conn = None if dry_run else connect()
    if not dry_run:
        cur = conn.execute("INSERT INTO scan_runs(started_at,root,status) VALUES(?,?,?)", (now_iso(), ' '.join(str(p) for p in paths), 'running'))
        run_id = cur.lastrowid
    else: run_id = 0
    files=images=findings=0
    text_exts=set(SCAN_ROOTS['text_exts']); image_exts=set(SCAN_ROOTS['image_exts']); skip=set(SCAN_ROOTS['skip_dirs'])
    cap_mb = CFG['deep_max_file_mb'] if deep else CFG['max_file_mb']
    if use_legacy and not dry_run:
        legacy = SCRIPTS/'substrate-scanner.py'
        if legacy.exists():
            import subprocess
            try: subprocess.run(['python3', str(legacy)], timeout=120, capture_output=True)
            except Exception: pass
    for p in iter_files(paths, text_exts|image_exts, skip):
        try:
            if p.stat().st_size > cap_mb*1024*1024: continue
        except OSError: continue
        if p.suffix.lower() in image_exts:
            text, engine = ocr_image(str(p))
            if text:
                if not dry_run:
                    n = ingest_text(conn, run_id, p, text, source_type='ocr', ocr_engine=engine)
                    findings+=n
                else: print(f"[DRY-RUN] OCR'd {p}")
                images+=1
            files+=1
        else:
            try: 
                text = p.read_text(encoding='utf-8', errors='ignore')
                if not dry_run:
                    n = ingest_text(conn, run_id, p, text, source_type='text')
                    findings+=n
                else: print(f"[DRY-RUN] Read {p}")
                files+=1
            except Exception: continue
    if not dry_run:
        conn.execute("UPDATE scan_runs SET finished_at=?,files_scanned=?,images_ocrd=?,findings=?,status=? WHERE id=?", (now_iso(), files, images, findings, 'complete', run_id))
        conn.commit(); conn.close(); lf.close()
    print(f"scan complete: {files} files, {images} images OCR'd, {findings} findings -> review_queue")
    if images>0 and findings==0 and not any(_has_tesseract()): print(install_hint())

def _has_tesseract():
    import shutil; return [shutil.which('tesseract')] if shutil.which('tesseract') else []

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='*')
    ap.add_argument('--root', default=None)
    ap.add_argument('--deep', action='store_true')
    ap.add_argument('--legacy', action='store_true', help='also invoke legacy substrate-scanner.py')
    ap.add_argument('--dry-run', action='store_true', help='simulate scan without DB writes')
    args = ap.parse_args()
    paths = [Path(p) for p in args.paths] if args.paths else []
    if not paths:
        for r in SCAN_ROOTS['roots']:
            rp = Path(r['path'])
            if not rp.is_absolute(): rp = ROOT/rp
            if rp.exists(): paths.append(rp)
        for ib in SCAN_ROOTS['inbox_roots']:
            ip = ROOT/ib if not Path(ib).is_absolute() else Path(ib)
            if ip.exists(): paths.append(ip)
    if not paths: print("no scan roots found."); return
    scan(paths, deep=args.deep, use_legacy=args.legacy, dry_run=args.dry_run)

if __name__=='__main__': main()
