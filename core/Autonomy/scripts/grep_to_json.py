#!/usr/bin/env python3
import json, re, os
ROOT = "/home/wayfinder/projects/Human-AI"
PATTERNS = ["modelfile", "ecosystem", "AI", "oy"]
EXTENSIONS = [".modelfile", ".html", ".yaml", ".yml", ".json", ".md", ".txt", ".sh", ".bak"]
EXCLUDE_DIRS = {".git", ".venv", "__pycache__", "node_modules", "substrate"}
OUTPUT = "/home/wayfinder/projects/Human-AI/core/Autonomy/databases/grep_output.json"
pattern = re.compile("|".join(PATTERNS), re.IGNORECASE)
results = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
    for fname in filenames:
        if any(fname.endswith(ext) for ext in EXTENSIONS):
            fpath = os.path.join(dirpath, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        if pattern.search(line):
                            results.append({"file": fpath, "line": line_num, "match": line.strip()})
            except Exception:
                pass
with open(OUTPUT, "w", encoding="utf-8") as out:
    json.dump(results, out, indent=2, ensure_ascii=False)
print(f"Wrote {len(results)} matches to {OUTPUT}")
