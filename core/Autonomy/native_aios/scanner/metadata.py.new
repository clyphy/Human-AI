import sys as _s; from pathlib import Path as _P; _s.path.insert(0, str((_P(__file__).resolve()).parent.parent))
"""File provenance metadata."""
import hashlib, os, subprocess
from datetime import datetime, timezone
def sha256_file(path, limit_mb=10):
    h = hashlib.sha256(); n=0; cap = limit_mb*1024*1024
    try:
        with open(path,'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                h.update(chunk); n+=len(chunk)
                if n>=cap: break
    except OSError: return None, None
    return h.hexdigest(), n
def git_info(path):
    d = os.path.dirname(path) or '.'
    info = {'repo': None, 'branch': None, 'commit': None}
    try:
        r = subprocess.run(['git','-C',d,'rev-parse','--show-toplevel'],
                           capture_output=True, text=True, timeout=3)
        if r.returncode==0 and r.stdout.strip():
            info['repo']=r.stdout.strip()
            b = subprocess.run(['git','-C',d,'rev-parse','--abbrev-ref','HEAD'],
                               capture_output=True, text=True, timeout=3)
            info['branch']=b.stdout.strip() or None
            c = subprocess.run(['git','-C',d,'rev-parse','--short','HEAD'],
                               capture_output=True, text=True, timeout=3)
            info['commit']=c.stdout.strip() or None
    except Exception: pass
    return info
def image_dims(path):
    try:
        from PIL import Image
        with Image.open(path) as im: return im.size  # (w,h)
    except Exception: return None, None
def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')
