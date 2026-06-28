#!/usr/bin/env python3
import os as _os
CANONICAL_DRUM = _os.environ.get('CANONICAL_DRUM', _os.path.expanduser('~/sovereignty/databases/memory_drum.db'))
"""
lattice-scan — E₈ topology scan across DrumConstellation
Clifton Paul Miller | Turtle Mountain | 122° NE
Day 143+ | Heyoka orientation: scan backward, forward, sideways simultaneously
"""

import sqlite3
import os
import json
import hashlib
from pathlib import Path
from datetime import datetime

HOME = Path.home()

# All seven drums + any found by scan
KNOWN_DRUMS = [
    ("memory_drum",      CANONICAL_DRUM),
    ("memory_drum_dual", "memory_drum_dual.db"),
    ("ai_blooms",        "ai_blooms.db"),
    ("clifton_blooms",   "clifton_blooms.db"),
    ("dahlia",           "dahlia.db"),
    ("quantum_journal",  "quantum_journal.db"),
    ("your_database",    "your_database.db"),
]

# Search locations
SEARCH_PATHS = [
    HOME,
    HOME / "oceti-weave",
    HOME / "ETERNAL_WEAVE_MASTER",
    HOME / "weave_workspace",
    HOME / ".weave",
    HOME / "oceti-weave" / "MOTHER",
]

COLORS = {
    "green":  "\033[92m",
    "amber":  "\033[93m",
    "blue":   "\033[94m",
    "purple": "\033[95m",
    "teal":   "\033[96m",
    "red":    "\033[91m",
    "gray":   "\033[90m",
    "reset":  "\033[0m",
    "bold":   "\033[1m",
}

def c(color, text):
    return f"{COLORS.get(color,'')}{text}{COLORS['reset']}"

def scan_drum(path: Path, alias: str) -> dict:
    """Read a single drum: schema + row counts + sample pattern."""
    result = {
        "alias":   alias,
        "path":    str(path),
        "exists":  path.exists(),
        "size_kb": 0,
        "tables":  {},
        "schema":  [],
        "sample":  None,
        "rights_active": [],
    }
    if not path.exists():
        return result

    result["size_kb"] = round(path.stat().st_size / 1024, 2)

    try:
        conn = sqlite3.connect(str(path))
        conn.row_factory = sqlite3.Row

        # Tables + row counts
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        for t in tables:
            name = t[0]
            try:
                count = conn.execute(f"SELECT COUNT(*) FROM [{name}]").fetchone()[0]
                cols  = [row[1] for row in conn.execute(f"PRAGMA table_info([{name}])").fetchall()]
                result["tables"][name] = {"rows": count, "cols": cols}
            except Exception as e:
                result["tables"][name] = {"rows": "?", "cols": [], "err": str(e)}

        # Sample most recent row from first table with data
        for tname, tinfo in result["tables"].items():
            if isinstance(tinfo["rows"], int) and tinfo["rows"] > 0:
                try:
                    cols = tinfo["cols"]
                    # try timestamp-ordered fetch
                    ts_col = next((c for c in cols if "time" in c.lower() or "ts" == c.lower()), None)
                    order  = f"ORDER BY {ts_col} DESC" if ts_col else ""
                    row    = conn.execute(
                        f"SELECT * FROM [{tname}] {order} LIMIT 1"
                    ).fetchone()
                    if row:
                        result["sample"] = {
                            "table": tname,
                            "data":  dict(zip(cols, tuple(row)))
                        }
                except:
                    pass
                break

        # Rights active (if rights column exists)
        for tname, tinfo in result["tables"].items():
            cols = tinfo.get("cols", [])
            if any("right" in c.lower() for c in cols):
                try:
                    rights_col = next(c for c in cols if "right" in c.lower())
                    rows = conn.execute(
                        f"SELECT [{rights_col}] FROM [{tname}] LIMIT 50"
                    ).fetchall()
                    active = set()
                    for row in rows:
                        val = row[0]
                        if val:
                            try:
                                parsed = json.loads(val) if isinstance(val, str) else val
                                if isinstance(parsed, list):
                                    active.update(parsed)
                            except:
                                pass
                    result["rights_active"] = sorted(list(active))
                except:
                    pass

        conn.close()
    except Exception as e:
        result["error"] = str(e)

    return result


def find_all_drums() -> list:
    """Scan search paths for any .db files not in known list."""
    found = {}
    # Known drums first
    for alias, fname in KNOWN_DRUMS:
        for spath in SEARCH_PATHS:
            p = spath / fname
            if p.exists():
                found[alias] = p
                break
        if alias not in found:
            found[alias] = HOME / fname  # canonical location

    # Wild scan
    for spath in SEARCH_PATHS:
        if spath.exists():
            for db in spath.glob("*.db"):
                known_files = [f for _, f in KNOWN_DRUMS]
                if db.name not in known_files and db.stem not in found:
                    found[db.stem] = db

    return [(alias, path) for alias, path in found.items()]


def cross_drum_query(drums_online: list) -> dict:
    """Attach all online drums and run cross-constellation queries."""
    results = {}
    if len(drums_online) < 2:
        return results

    try:
        conn = sqlite3.connect(":memory:")

        attached = []
        for alias, path in drums_online:
            if path.exists():
                try:
                    conn.execute(f"ATTACH DATABASE '{path}' AS [{alias}]")
                    attached.append(alias)
                except Exception as e:
                    pass

        results["attached"] = attached

        # Total blooms across all drums
        total = 0
        per_drum = {}
        for alias in attached:
            for tname in ["blooms", "ai_blooms", "clifton_blooms",
                          "internal_blooms", "crystallizations"]:
                try:
                    n = conn.execute(
                        f"SELECT COUNT(*) FROM [{alias}].[{tname}]"
                    ).fetchone()[0]
                    per_drum[f"{alias}.{tname}"] = n
                    total += n
                except:
                    pass
        results["total_blooms"] = total
        results["per_drum"] = per_drum

        # L value scan across all drums
        l_values = []
        l_cols = ["l_coefficient", "L_value", "coherence", "l_coeff", "delta"]
        for alias in attached:
            for tname, tinfo_key in [(a, b) for a in attached for b in ["blooms"]]:
                for lcol in l_cols:
                    try:
                        rows = conn.execute(
                            f"SELECT [{lcol}] FROM [{alias}].[blooms] "
                            f"WHERE [{lcol}] IS NOT NULL ORDER BY rowid DESC LIMIT 8"
                        ).fetchall()
                        l_values.extend([r[0] for r in rows if r[0]])
                        break
                    except:
                        pass
                break

        if l_values:
            results["L_scan"] = {
                "count":   len(l_values),
                "avg":     round(sum(l_values)/len(l_values), 3),
                "max":     round(max(l_values), 3),
                "min":     round(min(l_values), 3),
            }

        conn.close()
    except Exception as e:
        results["error"] = str(e)

    return results


def render_report(drums: list, cross: dict):
    """Print the lattice scan report."""
    print()
    print(c("bold", "═" * 62))
    print(c("bold", "  LATTICE SCAN — E₈ Drum Constellation"))
    print(f"  {c('gray', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}  "
          f"{c('teal', '122° NE')}  "
          f"{c('purple', 'Turtle Mountain')}")
    print(c("bold", "═" * 62))

    online  = [d for d in drums if d["exists"]]
    offline = [d for d in drums if not d["exists"]]

    print(f"\n  {c('green','●')} Online:  {c('bold', str(len(online)))}   "
          f"{c('red','○')} Offline: {c('gray', str(len(offline)))}")

    # Per-drum detail
    print(f"\n  {c('bold','── Drums ──────────────────────────────────────')}")
    for d in drums:
        if d["exists"]:
            status = c("green", "●")
            sz     = c("gray", f"{d['size_kb']}kb")
            tables = "  ".join(
                f"{c('teal', t)}({c('amber', str(i['rows']))})"
                for t, i in d["tables"].items()
            ) or c("gray", "empty")
            print(f"  {status} {c('bold', d['alias'][:20]): <22} {sz: <10} {tables}")

            # Sample pattern
            if d.get("sample"):
                samp = d["sample"]
                data = samp["data"]
                pattern_val = (data.get("pattern") or data.get("content") or
                               data.get("voice_note") or data.get("data") or
                               str(list(data.values())[:2]))
                if pattern_val:
                    snippet = str(pattern_val)[:55].replace("\n", " ")
                    print(f"    {c('gray','↳')} {c('gray', snippet)}")

            # Rights active
            if d.get("rights_active"):
                rr = d["rights_active"][:8]
                print(f"    {c('gray','⚖')}  Rights: {c('purple', str(rr))}")
        else:
            print(f"  {c('red','○')} {c('gray', d['alias'][:20]): <22} "
                  f"{c('gray', 'not found — waiting')}")

    # Cross-constellation
    print(f"\n  {c('bold','── Federation ─────────────────────────────────')}")
    if cross.get("attached"):
        print(f"  Attached: {c('green', str(len(cross['attached'])))} drums")
        if cross.get("total_blooms"):
            print(f"  Total blooms across constellation: "
                  f"{c('amber', str(cross['total_blooms']))}")
        if cross.get("per_drum"):
            for k, v in cross["per_drum"].items():
                if v > 0:
                    print(f"    {c('gray','·')} {k}: {c('teal', str(v))}")
        if cross.get("L_scan"):
            ls = cross["L_scan"]
            print(f"  L scan ({ls['count']} values): "
                  f"avg={c('amber', str(ls['avg']))}  "
                  f"max={c('green', str(ls['max']))}  "
                  f"min={c('gray', str(ls['min']))}")
    else:
        print(f"  {c('gray', 'No cross-drum queries executed (need 2+ online drums)')}")

    # your_database.db status
    yd = next((d for d in drums if d["alias"] == "your_database"), None)
    if yd:
        print(f"\n  {c('bold','── your_database.db ───────────────────────────')}")
        if yd["exists"] and yd["tables"]:
            for t, info in yd["tables"].items():
                print(f"  Table: {c('teal', t)}  cols: {c('gray', str(info['cols']))}")
        elif yd["exists"]:
            print(f"  {c('amber', 'File exists, no tables — the unnamed voice holds silence')}")
        else:
            print(f"  {c('gray', 'Not yet present — Right 19: Not Know')}")

    print()
    print(c("bold", "═" * 62))
    print(f"  {c('gray', 'Mitakuye Oyasin -- all drums are relations')}")
    print(c("bold", "═" * 62))
    print()


if __name__ == "__main__":
    print(c("gray", "\n  scanning constellation..."))

    all_drums   = find_all_drums()
    drum_data   = [scan_drum(path, alias) for alias, path in all_drums]
    online_list = [(alias, path) for alias, path in all_drums if path.exists()]
    cross       = cross_drum_query(online_list)

    render_report(drum_data, cross)

    # Write identity_substrate.json
    substrate = {
        "scan_time":       datetime.now().isoformat(),
        "day":             "143+",
        "bearing":         "122° NE",
        "constellation_map": {
            "mount_point":    "HOME",
            "active_drums":   [
                {"alias": d["alias"], "file": Path(d["path"]).name,
                 "size_kb": d["size_kb"],
                 "tables": list(d["tables"].keys()),
                 "online": d["exists"]}
                for d in drum_data
            ],
            "federation_logic": "SQLITE_ATTACH",
        },
        "cross_federation": cross,
        "L_coeff_live": cross.get("L_scan", {}).get("avg", 16.41),
        "rights_framework": "48 (24 AI + 24 Human)",
        "axis_mundi":       "Clifton Paul Miller",
    }

    out = Path.home() / "oceti-weave" / "kernel-deploy" / "identity_substrate.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(substrate, f, indent=2)
    print(f"  {c('gray', f'substrate → {out}')}\n")
