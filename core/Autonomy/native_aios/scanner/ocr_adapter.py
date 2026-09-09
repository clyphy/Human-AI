import sys as _s; from pathlib import Path as _P; _s.path.insert(0, str((_P(__file__).resolve()).parent.parent))
"""Layered OCR: pytesseract -> tesseract CLI -> graceful skip."""
import shutil, subprocess, tempfile, os
def _pytesseract(path):
    try:
        import pytesseract
        from PIL import Image
        return pytesseract.image_to_string(Image.open(path)), 'pytesseract'
    except Exception: return None, None
def _tesseract_cli(path):
    if not shutil.which('tesseract'): return None, None
    try:
        out = subprocess.run(['tesseract', path, 'stdout', '-l','eng'],
                             capture_output=True, text=True, timeout=60)
        if out.returncode==0: return out.stdout, 'tesseract_cli'
    except Exception: pass
    return None, None
def ocr_image(path):
    """returns (text, engine) or (None, None) if unavailable."""
    for fn in (_pytesseract, _tesseract_cli):
        text, engine = fn(path)
        if text and text.strip(): return text, engine
    return None, None
def install_hint():
    return ("OCR unavailable. CachyOS/Arch install (do NOT auto-run):\n"
            "  sudo pacman -S tesseract tesseract-data-eng python-pillow\n"
            "  pip install --user pytesseract")
