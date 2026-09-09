import sys as _s; from pathlib import Path as _P; _s.path.insert(0, str((_P(__file__).resolve()).parent.parent))
"""Serial Ollama adapter (low-RAM: NEVER parallel)."""
import shutil, subprocess, json
from paths import CONFIG
TIMEOUT = json.loads((CONFIG/'aios_config.json').read_text()).get('ollama_timeout_s',120)
def available():
    return shutil.which('ollama') is not None
def list_models():
    if not available(): return []
    try:
        r=subprocess.run(['ollama','list'],capture_output=True,text=True,timeout=10)
        out=[]
        for line in r.stdout.splitlines()[1:]:
            parts=line.split()
            if parts: out.append(parts[0])
        return out
    except Exception: return []
def has(model): return model in list_models()
def run(model, prompt, timeout=None):
    if not available(): return None, 'ollama not installed'
    try:
        r=subprocess.run(['ollama','run',model,prompt],capture_output=True,text=True,timeout=timeout or TIMEOUT)
        return r.stdout, r.stderr
    except subprocess.TimeoutExpired: return None, 'timeout'
    except Exception as e: return None, str(e)
def first_available(preferred):
    models=list_models()
    for m in preferred:
        if m in models: return m
    return models[0] if models else None
