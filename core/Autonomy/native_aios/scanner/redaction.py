import sys as _s; from pathlib import Path as _P; _s.path.insert(0, str((_P(__file__).resolve()).parent.parent))
"""Secret redaction. Strips API keys/tokens/passwords before storing snippets."""
import re
_PATTERNS = [
    (re.compile(r'(sk-[A-Za-z0-9]{16,})'), 'sk-REDACTED'),
    (re.compile(r'(gh[pousr]_[A-Za-z0-9]{20,})'), 'ghp-REDACTED'),
    (re.compile(r'(AKIA[0-9A-Z]{16})'), 'AKIA-REDACTED'),
    (re.compile(r'(xox[baprs]-[A-Za-z0-9-]{10,})'), 'xox-REDACTED'),
    (re.compile(r'(?i)(password|passwd|pwd|secret|token|api_key|apikey)\s*[:=]\s*\S+'), r'\1=REDACTED'),
    (re.compile(r'(Bearer\s+[A-Za-z0-9._\-]{16,})'), 'Bearer REDACTED'),
]
def redact(text):
    if not text: return text
    out = text
    for pat, rep in _PATTERNS:
        out = pat.sub(rep, out)
    return out
def contains_secret(text):
    if not text: return False
    return any(pat.search(text) for pat, _ in _PATTERNS)
