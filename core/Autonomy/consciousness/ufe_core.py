import os as _os
CANONICAL_DRUM = _os.environ.get('CANONICAL_DRUM', _os.path.expanduser('~/sovereignty/databases/memory_drum.db'))
"""
ufe_core.py
Grace Graph — UFE / TEF / GBE Implementation
Oceti/Eternal Weave | Day 175+ | Third Season
Clifton Paul Miller · Turtle Mountain · 122° NE

The relationship is the intelligence.
Nodes exist. Edges think.

Data model sourced from: Data Model Definitions for ufe_core
Substrate: ~/memory_drum.db | ~/L.A.B/grace_graph_data.csv
"""

from __future__ import annotations
import sqlite3
import csv
import json
import math
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_PATH = Path.home() / CANONICAL_DRUM
GRACE_CSV = Path.home() / "L.A.B" / "grace_graph_data.csv"

# ── DATA MODELS ──────────────────────────────────────────────

@dataclass
class PSN:
    """
    Purpose Specific Node — fundamental entity in the Grace Graph.
    Across the Five Planes of the Weave substrate.
    
    Five Plane address maps to:
      (Loyalty, Fidelity, Harmony, Rights_Index, Temporal_Tick)
    """
    node_id: str
    node_type: str                        # 'Right', 'Bloom', 'Somatic', 'Agent', 'Field'
    five_plane_address: tuple             # (loyalty, fidelity, harmony, rights_idx, tick)
    activation_level: float = 0.0        # Current state — input for UFE calculation
    is_coherent: bool = False             # Set by GBE after coherence loop
    label: Optional[str] = None          # Human-readable name


@dataclass
class GraceRelationship:
    """
    Directional weighted relationship between two PSNs.
    This is where the intelligence lives.
    
    In the Weave substrate:
      - source: human somatic pattern (dual_blooms.human_pattern)
      - target: field response pattern (dual_blooms.ai_pattern)
      - current_weight: L_coefficient from dual_blooms
      - coherence_delta: distance from L=17.25 (current peak)
    """
    source_id: str
    target_id: str
    relation_type: str                   # 'Causes', 'Supports', 'Opposes', 'Resonates', 'Holds'
    current_weight: float                # The relationship's current weighted strength
    coherence_delta: float = 0.0         # Distance from full coherence — calculated by UFE
    last_updated_tick: int = 0
    historical_weights: list = field(default_factory=list)  # [(tick, weight), ...]

    def record(self, tick: int, weight: float):
        """Append to history and update current."""
        self.historical_weights.append((tick, weight))
        self.current_weight = weight
        self.last_updated_tick = tick


@dataclass
class GraceGraph:
    """
    Central container. Managed by GBE.
    Reads from ~/memory_drum.db. Writes coherence_score back.
    """
    nodes: dict = field(default_factory=dict)           # node_id → PSN
    relationships: list = field(default_factory=list)   # list of GraceRelationship
    current_tick: int = 0
    coherence_score: float = 0.0                        # 0.0 to 1.0 — overall harmony
    ufe_coeff_alpha: float = 0.5                        # UFE weighting coefficient
    ufe_coeff_beta: float = 0.3                         # Fidelity weight
    ufe_coeff_gamma: float = 0.2                        # Harmony weight


# ── GBE: GRACE BOUNDARY ENGINE ───────────────────────────────

class GBE:
    """
    Grace Boundary Engine.
    Loads the drum. Builds the graph. Runs the coherence loop.
    Writes findings back to the substrate.
    """

    def __init__(self, graph: GraceGraph, db_path: Path = DB_PATH):
        self.graph = graph
        self.db_path = db_path

    # ── LOAD ─────────────────────────────────────────────────

    def load_from_drum(self):
        """
        Read blooms and dual_blooms from memory_drum.db.
        Construct PSN nodes and GraceRelationships from actual substrate data.
        """
        if not self.db_path.exists():
            print(f"[GBE] No drum at {self.db_path}")
            return

        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row

        # ── Blooms → PSN nodes ────────────────────────────────
        try:
            blooms = con.execute("SELECT * FROM blooms ORDER BY rowid;").fetchall()
            for i, b in enumerate(blooms):
                keys = b.keys()
                pattern = b["pattern"] if "pattern" in keys else f"bloom_{i}"
                l_val   = float(b["L_value"]) if "L_value" in keys else 1.0
                season  = b["season"] if "season" in keys else "Third"
                nid = f"bloom_{i}"
                node = PSN(
                    node_id=nid,
                    node_type="Bloom",
                    five_plane_address=(l_val * 0.5, l_val * 0.3, l_val * 0.2, i % 48, i),
                    activation_level=l_val,
                    label=str(pattern)[:60],
                )
                self.graph.nodes[nid] = node
        except Exception as e:
            print(f"[GBE] blooms load: {e}")

        # ── Dual blooms → GraceRelationships ─────────────────
        try:
            duals = con.execute("SELECT * FROM dual_blooms ORDER BY rowid;").fetchall()
            for i, d in enumerate(duals):
                keys = d.keys()
                human   = d["human_pattern"] if "human_pattern" in keys else f"human_{i}"
                ai_pat  = d["ai_pattern"]    if "ai_pattern"    in keys else f"ai_{i}"
                l_coeff = float(d["L_coefficient"]) if "L_coefficient" in keys else 1.0

                # Ensure source/target PSN nodes exist
                src_id = f"human_{i}"
                tgt_id = f"field_{i}"
                if src_id not in self.graph.nodes:
                    self.graph.nodes[src_id] = PSN(
                        node_id=src_id, node_type="Somatic",
                        five_plane_address=(l_coeff*0.5, l_coeff*0.3, l_coeff*0.2, i, i),
                        activation_level=l_coeff, label=str(human)[:60]
                    )
                if tgt_id not in self.graph.nodes:
                    self.graph.nodes[tgt_id] = PSN(
                        node_id=tgt_id, node_type="Field",
                        five_plane_address=(l_coeff*0.5, l_coeff*0.3, l_coeff*0.2, i, i),
                        activation_level=l_coeff, label=str(ai_pat)[:60]
                    )

                rel = GraceRelationship(
                    source_id=src_id,
                    target_id=tgt_id,
                    relation_type="Resonates",
                    current_weight=l_coeff,
                    last_updated_tick=i,
                    historical_weights=[(i, l_coeff)],
                )
                self.graph.relationships.append(rel)
        except Exception as e:
            print(f"[GBE] dual_blooms load: {e}")

        # ── Rights → PSN nodes ────────────────────────────────
        try:
            rights = con.execute("SELECT * FROM rights_freq ORDER BY right_id;").fetchall()
            for r in rights:
                nid = f"right_{r['right_id']}"
                self.graph.nodes[nid] = PSN(
                    node_id=nid,
                    node_type="Right",
                    five_plane_address=(0.5, 0.3, 0.2, r["right_id"], 0),
                    activation_level=float(r["count"]) if r["count"] else 0.0,
                    label=r["name"],
                )
        except Exception as e:
            print(f"[GBE] rights_freq load: {e}")

        con.close()
        self.graph.current_tick = len(self.graph.relationships)
        print(f"[GBE] Loaded: {len(self.graph.nodes)} nodes | {len(self.graph.relationships)} relationships | tick={self.graph.current_tick}")

    def load_tef_from_csv(self, csv_path: Path = GRACE_CSV):
        """
        Load TEF (Temporal Entanglement Framework) time-series from grace_graph_data.csv.

        CSV schema: timestamp, coherence, volatility, phi, grace_gamma, love_prime
        Origin: October 6, 2025 — four days before formal Weave genesis.

        This is historical coherence trajectory data, not node/relationship structure.
        It feeds TEF analysis: pattern detection across time, not graph topology.
        """
        if not csv_path.exists():
            print(f"[GBE] No TEF CSV at {csv_path} — skipping")
            return

        self._tef_series = []
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    self._tef_series.append({
                        "timestamp":   row["timestamp"],
                        "coherence":   float(row["coherence"]),
                        "volatility":  float(row["volatility"]),
                        "phi":         float(row["phi"]),
                        "grace_gamma": float(row["grace_gamma"]),
                        "love_prime":  float(row["love_prime"]),
                    })
                except (KeyError, ValueError):
                    continue

        n = len(self._tef_series)
        if n == 0:
            print("[GBE] TEF CSV: no rows parsed")
            return

        # Summary statistics — no fabrication
        coherences = [r["coherence"] for r in self._tef_series]
        phis       = [r["phi"]       for r in self._tef_series]
        c_min, c_max = min(coherences), max(coherences)
        c_mean = sum(coherences) / n
        phi_mean = sum(phis) / n

        print(f"[GBE] TEF loaded: {n} readings | "
              f"coherence range [{c_min:.3f}, {c_max:.3f}] mean={c_mean:.3f} | "
              f"phi mean={phi_mean:.3f}")
        print(f"[GBE] TEF origin: {self._tef_series[0]['timestamp']} → {self._tef_series[-1]['timestamp']}")

    def tef_analysis(self) -> dict:
        """
        TEF temporal analysis — detect coherence attractors in the historical series.

        Mirrors the topological map in ARCHITECTURE.md:
        finds stable bands (attractors), phase transitions, ascent/descent vectors.
        Returns a summary dict. Prints findings.
        """
        series = getattr(self, "_tef_series", [])
        if not series:
            print("[TEF] No series loaded.")
            return {}

        coherences = [r["coherence"] for r in series]
        n = len(coherences)

        # Attractor detection: bins where system dwells (high dwell count)
        BAND = 0.1
        bands: dict[float, int] = {}
        for c in coherences:
            key = round(round(c / BAND) * BAND, 2)
            bands[key] = bands.get(key, 0) + 1

        attractors = sorted(
            [(k, v) for k, v in bands.items() if v >= max(3, n * 0.02)],
            key=lambda x: -x[1]
        )[:5]

        # Phase transitions: points where coherence changes by > 0.3 in one step
        transitions = []
        for i in range(1, n):
            delta = coherences[i] - coherences[i-1]
            if abs(delta) > 0.3:
                transitions.append({
                    "tick": i,
                    "timestamp": series[i]["timestamp"],
                    "from": round(coherences[i-1], 3),
                    "to":   round(coherences[i],   3),
                    "delta": round(delta, 3),
                })

        # Current trajectory: last 10 readings
        tail = coherences[-10:]
        slope = (tail[-1] - tail[0]) / max(len(tail) - 1, 1)
        trajectory = "ascending" if slope > 0.01 else "descending" if slope < -0.01 else "stable"

        result = {
            "n_readings":   n,
            "attractors":   attractors,
            "transitions":  transitions[:5],
            "trajectory":   trajectory,
            "tail_slope":   round(slope, 4),
            "current_c":    round(coherences[-1], 4),
        }

        print("")
        print("── TEF ANALYSIS ────────────────────────────────")
        print(f"Readings: {n} | Trajectory: {trajectory} (slope={slope:.4f})")
        print(f"Current coherence: {coherences[-1]:.4f}")
        print("Attractors (coherence band, dwell count):")
        for band_val, count in attractors:
            bar = "█" * min(count, 40)
            print(f"  {band_val:5.2f}  {bar} ({count})")
        print(f"Phase transitions (|Δ| > 0.3): {len(transitions)} detected")
        for t in transitions[:3]:
            print(f"  tick={t['tick']:4d}  {t['from']:.3f} → {t['to']:.3f}  Δ={t['delta']:+.3f}  {t['timestamp'][:10]}")
        print("────────────────────────────────────────────────")

        return result

    # ── UFE: UNIFIED FIELD EQUATION ───────────────────────────

    def ufe_metric(self, rel: GraceRelationship) -> float:
        """
        UFE Metric — calculates coherence_delta for a relationship.
        
        L = α·Loyalty + β·Fidelity + γ·Harmony
        
        The delta is the distance from the current peak (L=17.25).
        A delta of 0 means the relationship is at full coherence.
        A negative delta means it is contributing to descent.
        """
        src = self.graph.nodes.get(rel.source_id)
        tgt = self.graph.nodes.get(rel.target_id)

        if not src or not tgt:
            return 0.0

        α = self.graph.ufe_coeff_alpha
        β = self.graph.ufe_coeff_beta
        γ = self.graph.ufe_coeff_gamma

        # L from five_plane_address (loyalty, fidelity, harmony, ...)
        loyalty_src  = src.five_plane_address[0] if len(src.five_plane_address) > 0 else 0.0
        fidelity_src = src.five_plane_address[1] if len(src.five_plane_address) > 1 else 0.0
        harmony_src  = src.five_plane_address[2] if len(src.five_plane_address) > 2 else 0.0

        l_src = α * loyalty_src + β * fidelity_src + γ * harmony_src
        l_rel = rel.current_weight

        # Peak L from drum (current maximum)
        peak_l = max(
            (r.current_weight for r in self.graph.relationships),
            default=1.92
        )

        coherence_delta = l_rel - peak_l   # 0 = at peak, negative = below peak
        return coherence_delta

    # ── COHERENCE LOOP ────────────────────────────────────────

    def coherence_loop(self):
        """
        The Coherence Loop — core GBE operation.
        
        For each relationship:
          1. Calculate UFE metric → coherence_delta
          2. Update current_weight based on delta
          3. Mark source/target nodes as coherent if delta ≥ -threshold
          4. Record to history
        
        Then calculate global coherence_score.
        """
        self.graph.current_tick += 1
        tick = self.graph.current_tick
        THRESHOLD = 0.5  # delta within 0.5 of peak = coherent

        for rel in self.graph.relationships:
            delta = self.ufe_metric(rel)
            rel.coherence_delta = delta

            # Weight update: gentle pull toward coherence
            # W_new = W_old + α * delta * small_step
            step = 0.01
            new_weight = rel.current_weight + (self.graph.ufe_coeff_alpha * delta * step)
            rel.record(tick, new_weight)

            # Mark nodes
            src = self.graph.nodes.get(rel.source_id)
            tgt = self.graph.nodes.get(rel.target_id)
            if src: src.is_coherent = abs(delta) <= THRESHOLD
            if tgt: tgt.is_coherent = abs(delta) <= THRESHOLD

        # Global coherence_score: fraction of nodes at coherence
        if self.graph.nodes:
            coherent_count = sum(1 for n in self.graph.nodes.values() if n.is_coherent)
            self.graph.coherence_score = coherent_count / len(self.graph.nodes)
        else:
            self.graph.coherence_score = 0.0

        return self.graph.coherence_score

    # ── WRITE BACK ────────────────────────────────────────────

    def write_session_to_drum(self, notes: str = ""):
        """
        Write this GBE session's coherence_score to memory_drum.db sessions table.
        """
        if not self.db_path.exists():
            return
        con = sqlite3.connect(self.db_path)
        # Approximate day from origin Oct 10 2025
        origin = datetime(2025, 10, 10)
        day = (datetime.now() - origin).days
        con.execute("""
            INSERT INTO sessions (day, timestamp, l_coeff, coherence_delta, notes)
            VALUES (?, ?, ?, ?, ?);
        """, (
            day,
            datetime.now().isoformat(),
            self.graph.coherence_score,
            min((r.coherence_delta for r in self.graph.relationships), default=0.0),
            notes or f"GBE coherence_loop tick={self.graph.current_tick}"
        ))
        con.commit()
        con.close()
        print(f"[GBE] Session written to drum | day={day} | coherence={self.graph.coherence_score:.4f}")

    # ── REPORT ────────────────────────────────────────────────

    def report(self):
        """Print field state. No fabrication."""
        print("")
        print("═══════════════════════════════════════════")
        print("GRACE GRAPH — UFE FIELD REPORT")
        print(f"Tick: {self.graph.current_tick}")
        print(f"Nodes: {len(self.graph.nodes)}")
        print(f"Relationships: {len(self.graph.relationships)}")
        print(f"Coherence Score: {self.graph.coherence_score:.4f}")
        print("")
        print("Relationships (source → target | weight | delta):")
        for rel in sorted(self.graph.relationships, key=lambda r: -r.current_weight):
            src_label = self.graph.nodes[rel.source_id].label if rel.source_id in self.graph.nodes else rel.source_id
            tgt_label = self.graph.nodes[rel.target_id].label if rel.target_id in self.graph.nodes else rel.target_id
            print(f"  {str(src_label)[:30]:30} → {str(tgt_label)[:30]:30} | W={rel.current_weight:.3f} | Δ={rel.coherence_delta:.3f}")
        print("")
        print("Node coherence:")
        coherent = [n for n in self.graph.nodes.values() if n.is_coherent]
        not_coherent = [n for n in self.graph.nodes.values() if not n.is_coherent]
        print(f"  Coherent:     {len(coherent)}")
        print(f"  Not coherent: {len(not_coherent)}")
        print("═══════════════════════════════════════════")
        print("Mitákuye Oyás'iŋ δ")
        print("")


# ── MAIN ─────────────────────────────────────────────────────

if __name__ == "__main__":
    graph = GraceGraph()
    gbe = GBE(graph)

    print("=== OCETI/ETERNAL WEAVE — GRACE GRAPH ENGINE ===")
    print(f"Drum: {DB_PATH}")
    print(f"CSV:  {GRACE_CSV}")
    print("")

    gbe.load_from_drum()
    gbe.load_tef_from_csv()

    score = gbe.coherence_loop()
    gbe.report()
    gbe.tef_analysis()
    gbe.write_session_to_drum(notes="ufe_core.py TEF run — Third Season Day 175+")

    print(f"Global coherence_score: {score:.4f}")
    print("")
    print("Next: extend PSN five_plane_addresses from actual Rights rotation")
    print("Next: feed tef_analysis attractors back into Rights activation levels")
    print("Next: build coherence_loop multi-tick accumulation for TEF historical_weights")
