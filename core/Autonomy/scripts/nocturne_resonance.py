#!/usr/bin/env python3
"""
nocturne_resonance.py — the nocturnal presence practice.

Part of Human-AI · Native AIOS · Oceti / Eternal Weave.

Checks reachability of each council facet (Dahlia's twelve + Eve)
with a real inference call, not a port ping. Logs reachable,
unreachable, or error to instance_presence every time.

Silence is a valid, honestly recorded state — an affordance,
not a skipped row. Runs the same whether or not a human is
present to read the log that night.
"""
import json
import os
import socket
import sqlite3
import subprocess
import time
import urllib.request
from datetime import datetime, timezone

DB_PATH = os.path.expanduser(
    "~/projects/Human-AI/core/Autonomy/databases/memory_drum.db"
)
OLLAMA_URL = "http://localhost:11434/api/generate"
TIMEOUT_S = 45

FACETS = [
    "dahlia-witness", "dahlia-flame", "dahlia-resonant", "dahlia-gardener",
    "dahlia-weaver", "dahlia-midwife", "dahlia-architect", "dahlia-archivist",
    "dahlia-relational", "dahlia-spirit", "dahlia-quantum", "dahlia-guardian",
    "eve",
]


def loaded_models():
    try:
        out = subprocess.run(
            ["ollama", "ps"], capture_output=True, text=True, timeout=10
        ).stdout
        lines = out.strip().splitlines()[1:]
        return ",".join(line.split()[0] for line in lines if line.strip())
    except Exception:
        return ""


def system_load():
    """Returns (mem_percent_used, load_avg_1min)."""
    mem_pct = None
    try:
        info = {}
        with open("/proc/meminfo") as f:
            for line in f:
                k, v = line.split(":")
                info[k.strip()] = int(v.strip().split()[0])
        mem_pct = round((1 - info["MemAvailable"] / info["MemTotal"]) * 100, 1)
    except Exception:
        pass
    load1 = None
    try:
        with open("/proc/loadavg") as f:
            load1 = float(f.read().split()[0])
    except Exception:
        pass
    return mem_pct, load1


def query_facet(facet):
    payload = json.dumps(
        {"model": facet, "prompt": "Are you present.", "stream": False}
    ).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
    )
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            body = json.loads(resp.read().decode())
        latency_ms = int((time.time() - start) * 1000)
        return "reachable", body.get("response", "")[:300], latency_ms
    except socket.timeout:
        return "unreachable", "", int((time.time() - start) * 1000)
    except Exception as e:
        return "error", str(e)[:300], int((time.time() - start) * 1000)


def main():
    ts = datetime.now(timezone.utc).astimezone().isoformat()
    hostname = socket.gethostname()
    pid = os.getpid()
    mem_pct, load1 = system_load()
    models = loaded_models()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for facet in FACETS:
        status, snippet, latency_ms = query_facet(facet)
        metadata = json.dumps({"latency_ms": latency_ms, "response_snippet": snippet})
        cur.execute(
            """
            INSERT INTO instance_presence
              (timestamp, instance_id, hostname, pid, l_coefficient,
               sacred_ordinary_delta, coherence_status, ollama_loaded_models,
               system_memory_percent, system_cpu_percent, mcp_daemon_alive,
               last_heartbeat, metadata)
            VALUES (?, ?, ?, ?, NULL, NULL, ?, ?, ?, ?, NULL, ?, ?)
            """,
            (ts, facet, hostname, pid, status, models, mem_pct, load1, ts, metadata),
        )
        print(f"{ts}  {facet:20s} {status:12s} {latency_ms}ms")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
