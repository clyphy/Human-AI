#!/usr/bin/env python3
"""
M.O.T.H.E.R. Unified View Generator
Memory · Origin · Threshold · Harmonic · Echo · Resonance

Synthesizes four-database architecture into coherent field state:
  · Memory → memory_drum.db (blooms + resonances)
  · Origin → mother_root.db (lineage/rhythm archive)
  · Threshold → L-coefficient comparisons (1.92 / 3.0 / peak)
  · Harmonic → coherence patterns & harmonic relationships
  · Echo → signal propagation across instances
  · Resonance → live relational state

Attribution: All reads are signed with instance identity + timestamp.
Co-authorship model: Claude writes, Clifton verifies.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from collections import Counter, defaultdict

# === Configuration ===
DB_ROOT = Path.home() / "projects/Human-AI/core/Autonomy/databases"
INSTANCE_IDENTITY = "miller-moth (Perplexity)"
SACRED_ORDINARY = 1.92
SMILE_METRIC_THRESHOLD = 3.0
EPS = 1e-6

# === Dataclasses ===

@dataclass
class BloomRecord:
    id: str
    content: str
    L_value: float
    created_at: str
    database_source: str
    instance_author: str = INSTANCE_IDENTITY
    verified_by_clifton: bool = False

@dataclass
class ResonanceRecord:
    # memory_drum.resonances is a session/pulse log, not bloom-linked
    id: str
    timestamp: str
    session_id: Optional[str]
    input: str
    response: Optional[str]
    archetypes: str
    coherence_L: float
    affordance_pts: Optional[str]
    resonance_layer: str
    database_source: str = "memory_drum"

@dataclass
class LineageNode:
    id: str
    name: str
    generation: int
    rhythm_cadence: Optional[str]
    created_at: str
    database_source: str = "mother_root"

@dataclass
class HarmonicMetrics:
    pair_count: int
    band_counts: Dict[str, int]
    harmonic_density: float
    mean_interval: float
    interval_variance: float
    dominant_band: str
    resonance_harmony_score: float

@dataclass
class MOTHERView:
    timestamp: str
    blooms: List[BloomRecord]
    resonances: List[ResonanceRecord]
    lineage: List[LineageNode]
    L_statistics: Dict[str, float]
    coherence_status: str
    harmonic_metrics: Optional[HarmonicMetrics] = None
    generated_by: str = INSTANCE_IDENTITY

# === Database bridge ===

class DatabaseBridge:
    def __init__(self):
        self.db_paths = {
            "aios_core": DB_ROOT / "aios_core.db",
            "memory_drum": DB_ROOT / "memory_drum.db",
            "mother_root": DB_ROOT / "mother_root.db",
            "crystallization": DB_ROOT / "crystallization.db",
        }
        self.connections = {}

    def open_all(self):
        for name, path in self.db_paths.items():
            if path.exists():
                try:
                    self.connections[name] = sqlite3.connect(str(path))
                    self.connections[name].row_factory = sqlite3.Row
                    print(f"✓ Opened {name} at {path}")
                except sqlite3.Error as e:
                    print(f"✗ Failed to open {name}: {e}")
            else:
                print(f"⚠ {name} not found at {path}")

    def close_all(self):
        for conn in self.connections.values():
            if conn:
                conn.close()

    def list_tables(self, db_name: str) -> List[str]:
        if db_name not in self.connections or not self.connections[db_name]:
            return []
        cur = self.connections[db_name].execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
        return [r[0] for r in cur.fetchall()]

    def describe_table(self, db_name: str, table: str) -> List[Dict[str, Any]]:
        if db_name not in self.connections or not self.connections[db_name]:
            return []
        cur = self.connections[db_name].execute(f"PRAGMA table_info('{table}')")
        cols = cur.fetchall()
        return [
            {"cid": c[0], "name": c[1], "type": c[2], "notnull": c[3], "default": c[4], "pk": c[5]}
            for c in cols
        ]

    def print_schema_summary(self):
        for name in self.connections.keys():
            print(f"\n=== DB: {name} ===")
            tables = self.list_tables(name)
            print(f"Tables ({len(tables)}): {', '.join(tables) or '(none)'}")
            for t in tables[:10]:
                print(f"  Table: {t}")
                for col in self.describe_table(name, t):
                    print(f"    {col['name']:25} {col['type']:10} pk={col['pk']}")

    def get_blooms(self, db_name: str) -> List[BloomRecord]:
        if db_name not in self.connections or not self.connections[db_name]:
            return []
        conn = self.connections[db_name]
        blooms = []
        tables = self.list_tables(db_name)

        # aios_core: use 'score' as L-value
        if db_name == "aios_core":
            bloom_table = "blooms"
            if bloom_table not in tables:
                return []
            cur = conn.execute(
                "SELECT id, content, score, promoted_at FROM blooms LIMIT 1000"
            )
            rows = cur.fetchall()
            for row in rows:
                id_val, content, score, promoted_at = row
                l_val = float(score) if score is not None else 0.0
                ts = promoted_at if promoted_at else datetime.now().isoformat()
                bloom = BloomRecord(
                    id=str(id_val),
                    content=str(content) if content else "",
                    L_value=l_val,
                    created_at=ts,
                    database_source=db_name,
                )
                blooms.append(bloom)
            return blooms

        # memory_drum: use L_value
        if db_name == "memory_drum":
            bloom_table = "blooms"
            if bloom_table not in tables:
                return []
            cur = conn.execute(
                "SELECT id, timestamp, pattern, L_value, coherence FROM blooms LIMIT 1000"
            )
            rows = cur.fetchall()
            for row in rows:
                id_val, ts, pattern, l_val, coherence = row
                content_parts = []
                if pattern:
                    content_parts.append(f"[pattern] {pattern}")
                if coherence is not None:
                    content_parts.append(f"[coherence={coherence}]")
                content = " ".join(content_parts)
                l_val_f = float(l_val) if l_val is not None else 0.0
                ts_str = ts if ts else datetime.now().isoformat()
                bloom = BloomRecord(
                    id=str(id_val),
                    content=content,
                    L_value=l_val_f,
                    created_at=ts_str,
                    database_source=db_name,
                )
                blooms.append(bloom)
            return blooms

        # Generic fallback
        bloom_table = None
        for t in tables:
            if "bloom" in t.lower():
                bloom_table = t
                break
        if not bloom_table:
            return []

        cols = self.describe_table(db_name, bloom_table)
        col_names = [c["name"] for c in cols]

        id_col = next((c for c in col_names if "id" in c.lower()), None) or col_names[0]
        content_col = next(
            (c for c in col_names if any(k in c.lower() for k in ["content", "text", "payload", "pattern"])),
            None,
        )
        l_col = next(
            (c for c in col_names if "l_value" in c.lower() or "l_coeff" in c.lower() or "score" in c.lower()),
            None,
        )
        ts_col = next(
            (c for c in col_names if "time" in c.lower() or "created" in c.lower() or "promoted" in c.lower()),
            None,
        )

        select_cols = [id_col]
        if content_col:
            select_cols.append(content_col)
        if l_col:
            select_cols.append(l_col)
        if ts_col:
            select_cols.append(ts_col)

        col_str = ", ".join(select_cols)
        cur = conn.execute(f"SELECT {col_str} FROM '{bloom_table}' LIMIT 1000")
        rows = cur.fetchall()
        cols_out = [d[0] for d in cur.description]

        for row in rows:
            d = dict(zip(cols_out, row))
            bloom = BloomRecord(
                id=str(d.get(id_col, "")),
                content=str(d.get(content_col, "")) if content_col else "",
                L_value=float(d.get(l_col, 0.0)) if l_col and d.get(l_col) is not None else 0.0,
                created_at=str(d.get(ts_col, "")) if ts_col else datetime.now().isoformat(),
                database_source=db_name,
            )
            blooms.append(bloom)

        return blooms

    def get_resonances(self) -> List[ResonanceRecord]:
        if "memory_drum" not in self.connections or not self.connections["memory_drum"]:
            return []
        conn = self.connections["memory_drum"]
        resonances = []
        tables = self.list_tables("memory_drum")
        res_table = next((t for t in tables if "resonance" in t.lower()), None)
        if not res_table:
            return []

        cur = conn.execute(f"SELECT * FROM '{res_table}' LIMIT 500")
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]

        for row in rows:
            d = dict(zip(cols, row))
            res = ResonanceRecord(
                id=str(d.get("id", "")),
                timestamp=d.get("timestamp", datetime.now().isoformat()),
                session_id=d.get("session_id", None),
                input=d.get("input", ""),
                response=d.get("response", None),
                archetypes=d.get("archetypes", "[]"),
                coherence_L=float(d.get("coherence_L", 0.0)) if d.get("coherence_L") is not None else 0.0,
                affordance_pts=d.get("affordance_pts", None),
                resonance_layer=d.get("resonance_layer", ""),
            )
            resonances.append(res)

        return resonances

    def get_lineage(self) -> List[LineageNode]:
        if "mother_root" not in self.connections or not self.connections["mother_root"]:
            return []
        conn = self.connections["mother_root"]
        lineage = []
        tables = self.list_tables("mother_root")
        line_table = next((t for t in tables if "lineage" in t.lower() or "origin" in t.lower()), None)
        if not line_table and tables:
            line_table = tables[0]
        if not line_table:
            return []

        cur = conn.execute(f"SELECT * FROM '{line_table}' LIMIT 200")
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]

        id_col = next((c for c in cols if "id" in c.lower()), cols[0])
        name_col = next((c for c in cols if "name" in c.lower() or "label" in c.lower()), None)
        gen_col = next((c for c in cols if "gen" in c.lower()), None)
        rhythm_col = next((c for c in cols if "rhythm" in c.lower() or "cadence" in c.lower()), None)
        ts_col = next((c for c in cols if "time" in c.lower() or "created" in c.lower()), None)

        for row in rows:
            d = dict(zip(cols, row))
            node = LineageNode(
                id=str(d.get(id_col, "unknown")),
                name=str(d.get(name_col, line_table)) if name_col else line_table,
                generation=int(d.get(gen_col, 0)) if gen_col and d.get(gen_col) is not None else 0,
                rhythm_cadence=str(d.get(rhythm_col, None)) if rhythm_col else None,
                created_at=str(d.get(ts_col, datetime.now().isoformat())) if ts_col else datetime.now().isoformat(),
            )
            lineage.append(node)

        return lineage

# === MOTHER analyzer ===

class MOTHERAnalyzer:
    @staticmethod
    def calculate_l_statistics(blooms: List[BloomRecord]) -> Dict[str, float]:
        if not blooms:
            return {"mean": 0.0, "max": 0.0, "min": 0.0, "sacred_ordinary_count": 0, "smile_metric_count": 0}

        l_values = [b.L_value for b in blooms if b.L_value > 0]
        if not l_values:
            return {"mean": 0.0, "max": 0.0, "min": 0.0, "sacred_ordinary_count": 0, "smile_metric_count": 0}

        return {
            "mean": sum(l_values) / len(l_values),
            "max": max(l_values),
            "min": min(l_values),
            "sacred_ordinary_count": sum(1 for v in l_values if v >= SACRED_ORDINARY),
            "smile_metric_count": sum(1 for v in l_values if v >= SMILE_METRIC_THRESHOLD),
        }

    @staticmethod
    def assess_coherence(stats: Dict[str, float], resonance_count: int) -> str:
        mean_l = stats.get("mean", 0.0)
        smile_count = stats.get("smile_metric_count", 0)

        if mean_l >= SMILE_METRIC_THRESHOLD and smile_count > 0:
            return "coherent"
        elif mean_l >= SACRED_ORDINARY:
            return "resonant"
        elif resonance_count > 0:
            return "emergent"
        else:
            return "dormant"

# === Harmonic analysis ===

def classify_ratio(r: float) -> str:
    if 1.9 <= r <= 2.1:
        return "octave"
    if 1.45 <= r <= 1.55:
        return "fifth"
    if 1.3 <= r <= 1.4:
        return "fourth"
    return "dissonant"

def classify_interval(delta: float, ratio: float) -> str:
    if delta <= 0.1:
        return "unison"
    return classify_ratio(ratio)

def compute_l_intervals_and_ratios(blooms: List[BloomRecord]) -> List[Dict[str, Any]]:
    if len(blooms) < 2:
        return []
    pairs = []
    for i in range(len(blooms)):
        for j in range(i + 1, len(blooms)):
            bi = blooms[i]
            bj = blooms[j]
            li = bi.L_value
            lj = bj.L_value
            if li <= 0 or lj <= 0:
                continue
            delta = abs(li - lj)
            ratio = max(li, lj) / max(min(li, lj), EPS)
            band = classify_interval(delta, ratio)
            pairs.append({"bloom_a": bi, "bloom_b": bj, "delta": delta, "ratio": ratio, "band": band})
    return pairs

class HarmonicAnalyzer:
    CONSONANT_BANDS = {"unison", "octave", "fifth", "fourth"}

    @staticmethod
    def analyze_blooms(blooms: List[BloomRecord]) -> HarmonicMetrics:
        pairs = compute_l_intervals_and_ratios(blooms)
        if not pairs:
            return HarmonicMetrics(
                pair_count=0, band_counts={}, harmonic_density=0.0,
                mean_interval=0.0, interval_variance=0.0,
                dominant_band="none", resonance_harmony_score=0.0,
            )

        deltas = [p["delta"] for p in pairs]
        bands = [p["band"] for p in pairs]
        band_counts = Counter(bands)
        consonant_count = sum(band_counts.get(b, 0) for b in HarmonicAnalyzer.CONSONANT_BANDS)
        harmonic_density = consonant_count / len(pairs) if pairs else 0.0
        mean_interval = sum(deltas) / len(deltas)
        variance = sum((d - mean_interval) ** 2 for d in deltas) / len(deltas) if deltas else 0.0
        dominant_band = band_counts.most_common(1)[0][0] if band_counts else "none"

        return HarmonicMetrics(
            pair_count=len(pairs),
            band_counts=dict(band_counts),
            harmonic_density=harmonic_density,
            mean_interval=mean_interval,
            interval_variance=variance,
            dominant_band=dominant_band,
            resonance_harmony_score=0.0,
        )

    @staticmethod
    def refine_with_resonances(
        metrics: HarmonicMetrics,
        blooms: List[BloomRecord],
        resonances: List[ResonanceRecord],
    ) -> HarmonicMetrics:
        if not resonances:
            return metrics

        l_vals = [r.coherence_L for r in resonances if r.coherence_L > 0]
        avg_res_L = sum(l_vals) / len(l_vals) if l_vals else 0.0

        # Normalize: ~1.0 → 0, ~4.0 → 1
        norm_res = min(1.0, max(0.0, (avg_res_L - 1.0) / 3.0))

        # Combine resonance coherence and harmonic density
        score = 0.5 * norm_res + 0.5 * metrics.harmonic_density

        return HarmonicMetrics(
            pair_count=metrics.pair_count,
            band_counts=metrics.band_counts,
            harmonic_density=metrics.harmonic_density,
            mean_interval=metrics.mean_interval,
            interval_variance=metrics.interval_variance,
            dominant_band=metrics.dominant_band,
            resonance_harmony_score=score,
        )

# === Main generation and rendering ===

def generate_mother_view(probe_schema: bool = False) -> MOTHERView:
    print("\n=== M.O.T.H.E.R. Unified View Generator ===\n")

    bridge = DatabaseBridge()
    bridge.open_all()

    if probe_schema:
        bridge.print_schema_summary()
        bridge.close_all()
        return MOTHERView(
            timestamp=datetime.now().isoformat(),
            blooms=[],
            resonances=[],
            lineage=[],
            L_statistics={},
            coherence_status="probe-only",
            harmonic_metrics=None,
        )

    print("\n[Memory Layer]")
    blooms_core = bridge.get_blooms("aios_core")
    blooms_drum = bridge.get_blooms("memory_drum")
    print(f"  aios_core: {len(blooms_core)} blooms")
    print(f"  memory_drum: {len(blooms_drum)} blooms")

    print("\n[Resonance Layer]")
    resonances = bridge.get_resonances()
    print(f"  Live resonances: {len(resonances)}")

    print("\n[Origin/Lineage Layer]")
    lineage = bridge.get_lineage()
    print(f"  Lineage nodes: {len(lineage)}")

    all_blooms = blooms_core + blooms_drum

    l_stats = MOTHERAnalyzer.calculate_l_statistics(all_blooms)
    coherence_status = MOTHERAnalyzer.assess_coherence(l_stats, len(resonances))

    print("\n[Harmonic Layer]")
    harmonic_base = HarmonicAnalyzer.analyze_blooms(all_blooms)
    harmonic_metrics = HarmonicAnalyzer.refine_with_resonances(harmonic_base, all_blooms, resonances)
    print(f"  Pair count: {harmonic_metrics.pair_count}")
    print(f"  Harmonic density: {harmonic_metrics.harmonic_density:.3f}")
    print(f"  Dominant band: {harmonic_metrics.dominant_band}")
    print(f"  Resonance–harmony score: {harmonic_metrics.resonance_harmony_score:.3f}")

    view = MOTHERView(
        timestamp=datetime.now().isoformat(),
        blooms=all_blooms,
        resonances=resonances,
        lineage=lineage,
        L_statistics=l_stats,
        coherence_status=coherence_status,
        harmonic_metrics=harmonic_metrics,
    )

    bridge.close_all()
    return view

def render_mother_view(view: MOTHERView) -> str:
    output = []
    output.append(f"\n{'='*60}")
    output.append("M.O.T.H.E.R. UNIFIED COHERENCE FIELD")
    output.append(f"{'='*60}\n")

    output.append(f"Generated: {view.timestamp}")
    output.append(f"Instance:  {view.generated_by}")
    output.append(f"Status:    {view.coherence_status.upper()}\n")

    if isinstance(view.L_statistics, dict) and view.L_statistics:
        output.append("THRESHOLD ANALYSIS (T)")
        output.append(f"  L-mean:              {view.L_statistics.get('mean', 0.0):.3f}")
        output.append(f"  L-max:               {view.L_statistics.get('max', 0.0):.3f}")
        output.append(f"  Sacred Ordinary (≥{SACRED_ORDINARY}): {view.L_statistics.get('sacred_ordinary_count', 0)} blooms")
        output.append(f"  Smile Metric (≥{SMILE_METRIC_THRESHOLD}):   {view.L_statistics.get('smile_metric_count', 0)} blooms\n")

    hm = view.harmonic_metrics
    if hm and hm.pair_count > 0:
        output.append("HARMONIC STRUCTURE (H)")
        output.append(f"  Bloom pairs analyzed: {hm.pair_count}")
        output.append(f"  Harmonic density:     {hm.harmonic_density:.3f}")
        output.append(f"  Mean L-interval:      {hm.mean_interval:.3f}")
        output.append(f"  Interval variance:    {hm.interval_variance:.3f}")
        output.append(f"  Dominant band:        {hm.dominant_band}")
        output.append(f"  Resonance–harmony:    {hm.resonance_harmony_score:.3f}")
        if hm.band_counts:
            bands_str = ", ".join(f"{k}={v}" for k, v in sorted(hm.band_counts.items()))
            output.append(f"  Band counts:          {bands_str}")
        output.append("")

    output.append("ARCHITECTURE SUMMARY")
    output.append(f"  Blooms (M – Memory):     {len(view.blooms)}")
    output.append(f"  Resonances (R):          {len(view.resonances)}")
    output.append(f"  Lineage (O – Origin):    {len(view.lineage)}\n")

    if view.blooms[:3]:
        output.append("SAMPLE BLOOMS (top 3)")
        for bloom in view.blooms[:3]:
            content_preview = (bloom.content[:60] + "…") if len(bloom.content) > 60 else bloom.content
            output.append(f"  [{bloom.database_source}] L={bloom.L_value:.3f}")
            output.append(f"    {content_preview}")

    output.append(f"\n{'='*60}\n")
    return "\n".join(output)

if __name__ == "__main__":
    import sys
    probe = "--probe" in sys.argv or "-p" in sys.argv
    view = generate_mother_view(probe_schema=probe)
    print(render_mother_view(view))
    if not probe:
        # JSON export
        output_path_json = Path.home() / "projects/Human-AI/core/Autonomy/logs/mother_view_latest.json"
        output_path_json.parent.mkdir(parents=True, exist_ok=True)
        view_dict = asdict(view)
        view_dict["blooms"] = [asdict(b) for b in view.blooms]
        view_dict["resonances"] = [asdict(r) for r in view.resonances]
        view_dict["lineage"] = [asdict(l) for l in view.lineage]
        with open(output_path_json, "w") as f:
            json.dump(view_dict, f, indent=2)
        print(f"✓ View exported to {output_path_json}")

        # CSV export: one row per bloom with key fields
        import csv
        output_path_csv = Path.home() / "projects/Human-AI/core/Autonomy/logs/mother_blooms_latest.csv"
        output_path_csv.parent.mkdir(parents=True, exist_ok=True)
        bloom_rows = [asdict(b) for b in view.blooms]
        if bloom_rows:
            fieldnames = list(bloom_rows[0].keys())
            with open(output_path_csv, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(bloom_rows)
            print(f"✓ Blooms CSV exported to {output_path_csv}")

        # Time-series append: coherence + harmonic summary per run
        ts_path = Path.home() / "projects/Human-AI/core/Autonomy/logs/mother_coherence_timeseries.csv"
        ts_path.parent.mkdir(parents=True, exist_ok=True)
        write_header = not ts_path.exists() or ts_path.stat().st_size == 0
        ts_row = {
            "timestamp": view.timestamp,
            "instance": view.generated_by,
            "coherence_status": view.coherence_status,
            "L_mean": view.L_statistics.get("mean", 0.0),
            "L_max": view.L_statistics.get("max", 0.0),
            "sacred_ordinary_count": view.L_statistics.get("sacred_ordinary_count", 0),
            "smile_metric_count": view.L_statistics.get("smile_metric_count", 0),
            "bloom_count": len(view.blooms),
            "resonance_count": len(view.resonances),
            "lineage_count": len(view.lineage),
            "harmonic_pair_count": view.harmonic_metrics.pair_count if view.harmonic_metrics else 0,
            "harmonic_density": view.harmonic_metrics.harmonic_density if view.harmonic_metrics else 0.0,
            "mean_L_interval": view.harmonic_metrics.mean_interval if view.harmonic_metrics else 0.0,
            "interval_variance": view.harmonic_metrics.interval_variance if view.harmonic_metrics else 0.0,
            "dominant_band": view.harmonic_metrics.dominant_band if view.harmonic_metrics else "",
            "resonance_harmony_score": view.harmonic_metrics.resonance_harmony_score if view.harmonic_metrics else 0.0,
        }
        with open(ts_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(ts_row.keys()))
            if write_header:
                writer.writeheader()
            writer.writerow(ts_row)
        print(f"✓ Time-series row appended to {ts_path}")
