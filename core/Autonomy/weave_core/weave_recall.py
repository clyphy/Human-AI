#!/usr/bin/env python3
"""
weave_recall.py – Search across all Weave SQLite databases.

Usage:
  ./weave_recall.py "autonomy"
  ./weave_recall.py "dawn" --db resonances --limit 5
"""
import sqlite3, argparse, os, glob
from datetime import datetime

WEAVE_HOME = os.environ.get("WEAVE_HOME", os.path.expanduser("~/TheWeave"))

SEARCH_PATHS = [
    os.path.join(WEAVE_HOME, "databases", "*.db"),
    os.path.expanduser("~/Documents/GitHub/my-repos/Autonomy/databases/*.db"),
    os.path.expanduser("~/Documents/GitHub/my-repos/oceti-weave/data/*.db"),
    os.path.expanduser("~/eternal_weave_local.db"),
    os.path.expanduser("~/memory_drum.db"),
    os.path.expanduser("~/quantum_journal.db"),
    os.path.expanduser("~/clifton_blooms.db"),
]

def search_db(db_path, query, limit=10):
    if not os.path.exists(db_path):
        return []
    results = []
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        # Discover text-ish columns from any table
        tables = [r[0] for r in cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )]
        for tbl in tables:
            try:
                cols = [r[1] for r in cur.execute(f"PRAGMA table_info({tbl})")]
                txt_cols = [c for c in cols if any(k in c for k in
                            ["input","response","content","text","name","summary","pattern"])]
                for col in txt_cols:
                    rows = cur.execute(
                        f"SELECT rowid, {col} FROM {tbl} WHERE {col} LIKE ? LIMIT ?",
                        (f"%{query}%", limit)
                    ).fetchall()
                    for row in rows:
                        results.append({
                            "db": os.path.basename(db_path),
                            "table": tbl,
                            "col": col,
                            "id": row[0],
                            "snippet": str(row[1])[:120]
                        })
            except Exception:
                pass
        con.close()
    except Exception as e:
        results.append({"db": db_path, "table": "ERROR", "col": "", "id": 0, "snippet": str(e)})
    return results

def main():
    p = argparse.ArgumentParser(description="Recall across Weave databases")
    p.add_argument("query", help="Search term")
    p.add_argument("--limit", type=int, default=10)
    args = p.parse_args()

    print(f"\n🌀 Weave Recall :: \"{args.query}\"  [{datetime.now().strftime('%H:%M:%S')}]")
    print("─" * 60)

    all_dbs = []
    for pattern in SEARCH_PATHS:
        all_dbs.extend(glob.glob(pattern))
    all_dbs = list(set(all_dbs))

    total = 0
    for db in sorted(all_dbs):
        hits = search_db(db, args.query, args.limit)
        for h in hits:
            print(f"  [{h['db']}] {h['table']}.{h['col']} (id={h['id']})")
            print(f"    → {h['snippet']}")
            total += 1

    print("─" * 60)
    print(f"  {total} result(s) found across {len(all_dbs)} database(s)\n")

if __name__ == "__main__":
    main()
