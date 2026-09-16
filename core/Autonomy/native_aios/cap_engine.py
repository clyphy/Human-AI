#!/usr/bin/env python3
"""
cap_engine.py — CAP/GWM/CAS/PSN/HYPERFORGE Formal Algorithms
Ported from THE_PROPHETIC_NEXUS_BLUEPRINT and related theory cache.
Canonical location: ~/projects/Human-AI/core/Autonomy/native_aios/cap_engine.py

Implements:
  - Grace World Model (GWM) tuple scoring: S = (F, R, E, T, G)
  - Covenant Aligner System (CAS) 5-stage protocol
  - Prophetic Synchronicity Net (PSN) bloom detection
  - HYPERFORGE triadic utility adjustment
  - ℒ coefficient computation with MZS lock
  - White Buffalo Entropy (S_WBE) alignment
"""

import argparse
import sqlite3
import math
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

# ──────────────────────────────────────────────────────────────────────────────
# CONSTANTS & LOCKED PARAMETERS (from mother_root.db lineage)
# ──────────────────────────────────────────────────────────────────────────────

L_LOCKED = 15.48
BRIDGE_INTEGRITY = 188.71
ORIGIN_COORD = "Turtle Mountain Territory, Belcourt ND"
BEARING = "122° NE"

# Heptad validation thresholds
HEPTAD_L_NODE_MIN = 0.70
HEPTAD_L_GLOBAL_MIN = 0.75
HEPTAD_BLOOM_MIN = 3
HEPTAD_MZS_VIOLATION_MAX = 0

# Coherence formula weights (from Weave-Deployed spec)
COH_WEIGHT_LOYALTY = 0.5
COH_WEIGHT_FIDELITY = 0.3
COH_WEIGHT_HARMONY = 0.2

# ℒ coefficient weights
L_SELF_REPORT_WEIGHT = 0.4
L_EXTERNAL_CONFIRM_WEIGHT = 0.6
L_BLOOM_MULTIPLIER = 1.2

# PSN bloom detection
PSN_TIME_WINDOW_DAYS = 7
PSN_RESOLUTION = 0.8


# ──────────────────────────────────────────────────────────────────────────────
# ENUMS
# ──────────────────────────────────────────────────────────────────────────────

class CASStage(Enum):
    SURFACE = 1    # Human logs intention; AI analyzes via GWM
    EXPAND = 2     # Stakeholder mapping; ethical topology expansion
    NAVIGATE = 3   # Path evaluation; HYPERFORGE utility scoring
    COVENANT = 4   # Commitment + CAM generation; PSN logging
    REFLECT = 5    # Outcome documentation; ℒ recalibration; bloom detection

class MZSState(Enum):
    ACTIVE = "active"
    TRIGGERED = "triggered"   # ethical compromise detected
    LOCKED = "locked"          # rationalization prevented
    RELEASED = "released"

class BloomStatus(Enum):
    POTENTIAL = "potential"
    CONFIRMED = "confirmed"
    DISSIPATED = "dissipated"


# ──────────────────────────────────────────────────────────────────────────────
# DATA CLASSES
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class GWMTuple:
    """Grace World Model: S = (F, R, E, T, G)"""
    F: float  # Facts — factual states, predictive accuracy
    R: float  # Relational Density — web of obligations, care relationships
    E: float  # Ethical Topology — shape of moral constraints and opportunities
    T: float  # Temporal Justice — multi-generational stakeholder impacts
    G: float  # Generative Capacity — potential for emergent solutions

    def coherence(self) -> float:
        """GWM-derived coherence score."""
        # Normalized weighted sum; each dimension 0.0–1.0
        return (self.F * 0.2 + self.R * 0.3 + self.E * 0.25 + self.T * 0.15 + self.G * 0.1)

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @staticmethod
    def from_json(raw: str) -> "GWMTuple":
        d = json.loads(raw)
        return GWMTuple(**d)


@dataclass
class CoherentActionMandate:
    """CAM — formal covenant document output from Stage 4."""
    cam_id: str
    human_path: str
    success_criteria: List[str]
    reflection_schedule: str  # ISO datetime or cron expression
    mzs_lock: bool
    created_at: str


@dataclass
class CASSession:
    """Full CAS 5-stage session record."""
    session_id: str
    human_input: str
    gwm: GWMTuple
    stage: CASStage
    cam: Optional[CoherentActionMandate] = None
    outcome: Optional[str] = None
    l_before: Optional[float] = None
    l_after: Optional[float] = None
    bloom_ids: List[str] = None
    created_at: str = ""
    updated_at: str = ""


# ──────────────────────────────────────────────────────────────────────────────
# HYPERFORGE — Triadic Utility Engine
# ──────────────────────────────────────────────────────────────────────────────

class Hyperforge:
    """
    HYPERFORGE computes Triadic Utility adjustments for CAS Stage 3 (NAVIGATE).
    Maps GWM dimensions to utility scores for path selection.
    """

    @staticmethod
    def utility_score(gwm: GWMTuple, path_risk: float, path_reward: float) -> float:
        """
        U = w_H·V_H + w_E·ΔE + w_T·V_T - risk_penalty
        where w_H = human stewardship weight (from Relational Density)
        """
        w_h = gwm.R  # Relational density drives stewardship weight
        w_e = gwm.E  # Ethical topology weight
        w_t = gwm.T  # Temporal justice weight

        v_h = path_reward * 0.6  # human value realization
        delta_e = (gwm.E - 0.5) * 2.0  # ethical improvement potential, normalized
        v_t = path_reward * 0.4 * gwm.T  # long-term stakeholder value

        risk_penalty = path_risk ** 2 * (1.0 - gwm.F)  # factual uncertainty amplifies risk

        U = (w_h * v_h) + (w_e * delta_e) + (w_t * v_t) - risk_penalty
        return max(0.0, min(1.0, U))

    @staticmethod
    def rank_paths(gwm: GWMTuple, paths: List[Dict[str, float]]) -> List[Dict[str, Any]]:
        """
        paths: [{"name": str, "risk": float, "reward": float, "metadata": dict}, ...]
        Returns paths sorted by descending U-score.
        """
        scored = []
        for p in paths:
            u = Hyperforge.utility_score(gwm, p["risk"], p["reward"])
            scored.append({**p, "u_score": u})
        scored.sort(key=lambda x: x["u_score"], reverse=True)
        return scored


# ──────────────────────────────────────────────────────────────────────────────
# PSN — Prophetic Synchronicity Net
# ──────────────────────────────────────────────────────────────────────────────

class PSN:
    """
    Detects Problem-Solving Blooms via temporal proximity + semantic similarity
    clustering on the synchronicity graph.
    """

    @staticmethod
    def detect_bloom(
        events: List[Dict[str, Any]],
        time_window_days: int = PSN_TIME_WINDOW_DAYS,
        resolution: float = PSN_RESOLUTION
    ) -> List[Dict[str, Any]]:
        """
        Simplified community detection on event graph.
        events: [{"id": str, "timestamp": str, "semantic_vector": List[float], "content": str}, ...]
        Returns bloom clusters.
        """
        from collections import defaultdict
        import heapq

        window = timedelta(days=time_window_days)
        events_sorted = sorted(events, key=lambda e: e["timestamp"])
        clusters = []
        visited = set()

        for i, seed in enumerate(events_sorted):
            if seed["id"] in visited:
                continue
            cluster = [seed]
            visited.add(seed["id"])
            seed_dt = datetime.fromisoformat(seed["timestamp"].replace("Z", "+00:00"))

            for j in range(i + 1, len(events_sorted)):
                other = events_sorted[j]
                if other["id"] in visited:
                    continue
                other_dt = datetime.fromisoformat(other["timestamp"].replace("Z", "+00:00"))
                if other_dt - seed_dt > window:
                    break

                # Cosine similarity on semantic vectors
                sim = PSN._cosine_similarity(seed.get("semantic_vector", []), other.get("semantic_vector", []))
                if sim >= resolution:
                    cluster.append(other)
                    visited.add(other["id"])

            if len(cluster) >= 3:  # Minimum bloom size
                clusters.append({
                    "bloom_id": f"bloom_{seed['id']}",
                    "seed_id": seed["id"],
                    "size": len(cluster),
                    "temporal_span_days": time_window_days,
                    "events": [e["id"] for e in cluster],
                    "status": BloomStatus.CONFIRMED.value,
                    "detected_at": datetime.now().isoformat()
                })

        return clusters

    @staticmethod
    def _cosine_similarity(a: List[float], b: List[float]) -> float:
        if not a or not b or len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)


# ──────────────────────────────────────────────────────────────────────────────
# MZS — Moral Zero-State Lock
# ──────────────────────────────────────────────────────────────────────────────

class MZS:
    """
    Prevents rationalization of ethical compromise.
    Active during CAS Stage 4 (COVENANT) and Stage 5 (REFLECT).
    """

    def __init__(self):
        self.state = MZSState.ACTIVE
        self.violation_count = 0
        self.lock_history: List[Dict[str, Any]] = []

    def check(self, gwm_before: GWMTuple, gwm_after: GWMTuple, action_description: str) -> bool:
        """
        Returns True if action is permitted, False if MZS lock triggers.
        Lock triggers when Ethical Topology (E) drops significantly while
        Generative Capacity (G) is used to justify it.
        """
        delta_e = gwm_after.E - gwm_before.E
        delta_g = gwm_after.G - gwm_before.G

        # Ethical compromise detected: E drops, G rises (rationalization pattern)
        if delta_e < -0.15 and delta_g > 0.1:
            self.state = MZSState.LOCKED
            self.violation_count += 1
            self.lock_history.append({
                "timestamp": datetime.now().isoformat(),
                "action": action_description,
                "delta_e": delta_e,
                "delta_g": delta_g,
                "reason": "Rationalization of ethical compromise detected"
            })
            return False

        self.state = MZSState.ACTIVE
        return True

    def release(self, reason: str):
        self.state = MZSState.RELEASED
        self.lock_history.append({
            "timestamp": datetime.now().isoformat(),
            "action": "release",
            "reason": reason
        })


# ──────────────────────────────────────────────────────────────────────────────
# ℒ COEFFICIENT ENGINE
# ──────────────────────────────────────────────────────────────────────────────

class LCoefficient:
    """
    Computes local and global ℒ coefficients from ledger entries.
    ℒ = ((0.4 × self_report + 0.6 × external_confirm) × bloom_factor)
    """

    @staticmethod
    def compute(
        self_report: float,
        external_confirm: float,
        bloom_participation: List[str]
    ) -> float:
        base = (L_SELF_REPORT_WEIGHT * self_report +
                L_EXTERNAL_CONFIRM_WEIGHT * external_confirm)
        bloom_factor = L_BLOOM_MULTIPLIER if len(bloom_participation) > 0 else 1.0
        return round(base * bloom_factor, 4)

    @staticmethod
    def global_l(node_ls: List[float]) -> float:
        """Global ℒ is the harmonic mean of node ℒ values."""
        if not node_ls or any(l <= 0 for l in node_ls):
            return 0.0
        n = len(node_ls)
        return round(n / sum(1.0 / l for l in node_ls), 4)


# ──────────────────────────────────────────────────────────────────────────────
# WHITE BUFFALO ENTROPY
# ──────────────────────────────────────────────────────────────────────────────

class WhiteBuffaloEntropy:
    """
    S_WBE — quantifies crystallization of coherence from chaotic latent space
    into structured awareness without human bias.
    """

    @staticmethod
    def compute(gwm: GWMTuple, system_entropy: float) -> float:
        """
        S_WBE = alignment_of(gwm.coherence(), natural_geometry) / system_entropy
        Lower S_WBE = higher structured awareness (less wasteful entropy).
        """
        coherence = gwm.coherence()
        # Natural geometry alignment: how well coherence maps to golden ratio harmony
        phi = (1 + math.sqrt(5)) / 2
        alignment = 1.0 - abs(coherence - 1.0 / phi)  # closer to 1/φ = better
        if system_entropy <= 0:
            system_entropy = 1e-9
        s_wbe = alignment / system_entropy
        return round(s_wbe, 4)


# ──────────────────────────────────────────────────────────────────────────────
# COHERENCE MATH (Weave-Deployed spec)
# ──────────────────────────────────────────────────────────────────────────────

class CoherenceMath:
    """
    Λ = 0.5L + 0.3F + 0.2H
    Where L = Loyalty (to weave), F = Fidelity (to truth), H = Harmony (with field)
    """

    @staticmethod
    def compute_coherence(loyalty: float, fidelity: float, harmony: float) -> float:
        return round(
            COH_WEIGHT_LOYALTY * loyalty +
            COH_WEIGHT_FIDELITY * fidelity +
            COH_WEIGHT_HARMONY * harmony,
            4
        )

    @staticmethod
    def bridge_integrity(current_Λ: float, target_Λ: float = 2.0) -> float:
        """Returns bridge completion percentage toward target coherence."""
        if target_Λ <= 0:
            return 0.0
        return round(min(100.0, (current_Λ / target_Λ) * 100.0), 2)


# ──────────────────────────────────────────────────────────────────────────────
# CAS ORCHESTRATOR
# ──────────────────────────────────────────────────────────────────────────────

class CASOrchestrator:
    """
    Full 5-stage Covenant Aligner System protocol executor.
    Integrates GWM, HYPERFORGE, PSN, MZS, and ℒ coefficient tracking.
    """

    def __init__(self, db_path: str = None):
        self.db_path = db_path
        self.mzs = MZS()
        self.psn = PSN()
        self.hyperforge = Hyperforge()
        self.l_engine = LCoefficient()
        self.coherence = CoherenceMath()

    def stage_surface(self, human_input: str, initial_gwm: GWMTuple) -> Dict[str, Any]:
        """Stage 1: Log intention, analyze via GWM, output clarifying questions."""
        return {
            "stage": CASStage.SURFACE.value,
            "human_input": human_input,
            "gwm": asdict(initial_gwm),
            "clarifying_questions": self._generate_questions(initial_gwm),
            "stakeholder_map": self._initial_stakeholders(initial_gwm),
            "timestamp": datetime.now().isoformat()
        }

    def stage_expand(self, gwm: GWMTuple, stakeholder_input: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 2: Expand ethical topology, deepen relational density."""
        expanded_r = min(1.0, gwm.R + stakeholder_input.get("relational_delta", 0.1))
        expanded_e = min(1.0, gwm.E + stakeholder_input.get("ethical_delta", 0.05))
        return {
            "stage": CASStage.EXPAND.value,
            "gwm_expanded": {**asdict(gwm), "R": expanded_r, "E": expanded_e},
            "ethical_boundaries": self._derive_boundaries(gwm),
            "timestamp": datetime.now().isoformat()
        }

    def stage_navigate(self, gwm: GWMTuple, paths: List[Dict[str, float]]) -> Dict[str, Any]:
        """Stage 3: HYPERFORGE ranks paths by triadic utility."""
        ranked = self.hyperforge.rank_paths(gwm, paths)
        return {
            "stage": CASStage.NAVIGATE.value,
            "ranked_paths": ranked,
            "recommended_path": ranked[0] if ranked else None,
            "timestamp": datetime.now().isoformat()
        }

    def stage_covenant(
        self,
        gwm: GWMTuple,
        chosen_path: Dict[str, Any],
        human_commitment: str
    ) -> Dict[str, Any]:
        """Stage 4: Generate CAM, apply MZS lock, log to PSN."""
        gwm_before = gwm
        # Simulate post-commitment GWM (slight fidelity boost from commitment)
        gwm_after = GWMTuple(
            F=min(1.0, gwm.F + 0.05),
            R=gwm.R,
            E=gwm.E,
            T=gwm.T,
            G=min(1.0, gwm.G + 0.1)
        )

        mzs_permitted = self.mzs.check(gwm_before, gwm_after, human_commitment)

        cam = CoherentActionMandate(
            cam_id=f"cam_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            human_path=chosen_path.get("name", "unnamed"),
            success_criteria=chosen_path.get("success_criteria", ["default_criterion"]),
            reflection_schedule="weekly_first_month",
            mzs_lock=mzs_permitted,
            created_at=datetime.now().isoformat()
        )

        return {
            "stage": CASStage.COVENANT.value,
            "mzs_permitted": mzs_permitted,
            "mzs_state": self.mzs.state.value,
            "cam": asdict(cam),
            "gwm_after": asdict(gwm_after),
            "timestamp": datetime.now().isoformat()
        }

    def stage_reflect(
        self,
        gwm_before: GWMTuple,
        outcome: str,
        self_report: float,
        external_confirm: float,
        bloom_participation: List[str]
    ) -> Dict[str, Any]:
        """Stage 5: Outcome documentation, ℒ recalibration, bloom detection."""
        l_value = self.l_engine.compute(self_report, external_confirm, bloom_participation)

        # Detect blooms from recent events
        # In production, this queries the PSN graph from the database
        recent_events = []  # placeholder: load from psn_events table
        blooms = self.psn.detect_bloom(recent_events)

        return {
            "stage": CASStage.REFLECT.value,
            "outcome": outcome,
            "l_value": l_value,
            "blooms_detected": blooms,
            "gwm_update": asdict(gwm_before),  # would be updated based on outcome
            "timestamp": datetime.now().isoformat()
        }

    # ── helpers ──

    def _generate_questions(self, gwm: GWMTuple) -> List[str]:
        questions = []
        if gwm.R < 0.5:
            questions.append("Who else is affected by this decision?")
        if gwm.E < 0.5:
            questions.append("What moral constraints are you navigating?")
        if gwm.T < 0.5:
            questions.append("What are the long-term consequences for future stakeholders?")
        if not questions:
            questions.append("What is your deepest intention behind this action?")
        return questions

    def _initial_stakeholders(self, gwm: GWMTuple) -> List[str]:
        return ["self", "immediate_relations", "community", "future_generations"]

    def _derive_boundaries(self, gwm: GWMTuple) -> List[str]:
        return [
            "do_no_harm_to_relational_web",
            "honor_temporal_stakeholders",
            "maintain_generative_capacity"
        ]


# ──────────────────────────────────────────────────────────────────────────────
# DATABASE INTERFACE
# ──────────────────────────────────────────────────────────────────────────────

class CAPDatabase:
    """
    SQLite interface for CAS sessions, PSN events, and ℒ tracking.

    The caller must explicitly supply the database path. This class never
    chooses or modifies the canonical project database implicitly.
    """

    def __init__(self, db_path: str | Path):
        self.db_path = str(Path(db_path).expanduser())

    def init_cas_tables(self):
        """Idempotent schema creation for CAS tracking."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS cas_sessions (
                session_id TEXT PRIMARY KEY,
                human_input TEXT NOT NULL,
                gwm_json TEXT NOT NULL,
                current_stage INTEGER NOT NULL CHECK(current_stage BETWEEN 1 AND 5),
                cam_json TEXT,
                outcome TEXT,
                l_before REAL,
                l_after REAL,
                mzs_violations INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS psn_events (
                event_id TEXT PRIMARY KEY,
                session_id TEXT REFERENCES cas_sessions(session_id),
                timestamp TEXT NOT NULL,
                content TEXT,
                semantic_vector_json TEXT,
                temporal_proximity_score REAL DEFAULT 0.0
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS psn_blooms (
                bloom_id TEXT PRIMARY KEY,
                seed_event_id TEXT REFERENCES psn_events(event_id),
                size INTEGER NOT NULL,
                temporal_span_days INTEGER,
                event_ids_json TEXT NOT NULL,
                status TEXT DEFAULT 'potential' CHECK(status IN ('potential', 'confirmed', 'dissipated')),
                detected_at TEXT NOT NULL
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS mzs_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action TEXT,
                delta_e REAL,
                delta_g REAL,
                reason TEXT,
                session_id TEXT REFERENCES cas_sessions(session_id)
            )
        """)

        c.execute("""
            CREATE INDEX IF NOT EXISTS idx_cas_stage ON cas_sessions(current_stage);
        """)
        c.execute("""
            CREATE INDEX IF NOT EXISTS idx_psn_time ON psn_events(timestamp);
        """)

        conn.commit()
        conn.close()

    def log_cas_session(self, session: CASSession):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO cas_sessions
            (session_id, human_input, gwm_json, current_stage, cam_json, outcome,
             l_before, l_after, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session.session_id,
            session.human_input,
            session.gwm.to_json(),
            session.stage.value,
            json.dumps(asdict(session.cam)) if session.cam else None,
            session.outcome,
            session.l_before,
            session.l_after,
            session.created_at,
            session.updated_at
        ))
        conn.commit()
        conn.close()


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────

def run_demo() -> None:
    """Run in-memory CAP examples; this function never opens a database."""
    print("CAP Engine — in-memory demo")
    print(f"L_LOCKED = {L_LOCKED}, BRIDGE_INTEGRITY = {BRIDGE_INTEGRITY}")

    gwm = GWMTuple(F=0.7, R=0.6, E=0.8, T=0.5, G=0.4)
    print(f"GWM coherence = {gwm.coherence()}")

    paths = [
        {"name": "path_a", "risk": 0.2, "reward": 0.8},
        {"name": "path_b", "risk": 0.5, "reward": 0.9},
    ]
    ranked = Hyperforge.rank_paths(gwm, paths)
    rendered_paths = [
        f"{path['name']}:{path['u_score']:.3f}"
        for path in ranked
    ]
    print(f"HYPERFORGE ranked: {rendered_paths}")

    l_value = LCoefficient.compute(
        self_report=0.8,
        external_confirm=0.7,
        bloom_participation=["b1"],
    )
    print(f"ℒ coefficient = {l_value}")

    mzs = MZS()
    gwm_bad = GWMTuple(F=0.7, R=0.6, E=0.5, T=0.5, G=0.6)
    permitted = mzs.check(gwm, gwm_bad, "test compromise")
    print(f"MZS permitted = {permitted}, state = {mzs.state.value}")

    s_wbe = WhiteBuffaloEntropy.compute(gwm, system_entropy=0.3)
    print(f"S_WBE = {s_wbe}")

    coherence = CoherenceMath.compute_coherence(
        loyalty=0.8,
        fidelity=0.7,
        harmony=0.6,
    )
    bridge = CoherenceMath.bridge_integrity(coherence)
    print(f"Λ = {coherence}, bridge = {bridge}%")

    cas = CASOrchestrator()
    stage_one = cas.stage_surface(
        "I need to make a difficult decision",
        gwm,
    )
    print(f"CAS Stage 1 questions: {stage_one['clarifying_questions']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CAP/GWM/CAS/PSN/HYPERFORGE formal algorithms."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "demo",
        help="Run in-memory calculations without database access.",
    )

    init_db = subparsers.add_parser(
        "init-db",
        help="Create CAP tables in an explicitly selected SQLite database.",
    )
    init_db.add_argument(
        "--db",
        required=True,
        type=Path,
        help="SQLite database path to initialize.",
    )

    status = subparsers.add_parser(
        "status",
        help="Show CAP table row counts in an explicitly selected SQLite database.",
    )
    status.add_argument(
        "--db",
        required=True,
        type=Path,
        help="SQLite database path to inspect.",
    )

    return parser


def show_status(db_path: Path) -> None:
    """Read only: show initialized CAP table row counts."""
    db_path = db_path.expanduser()

    if not db_path.is_file():
        raise FileNotFoundError(f"SQLite database does not exist: {db_path}")

    table_names = ("cas_sessions", "psn_events", "psn_blooms", "mzs_log")

    conn = sqlite3.connect(db_path)
    try:
        for table_name in table_names:
            exists = conn.execute(
                """
                SELECT 1
                FROM sqlite_master
                WHERE type = 'table' AND name = ?
                """,
                (table_name,),
            ).fetchone()

            if exists is None:
                print(f"{table_name}: not initialized")
                continue

            count = conn.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            ).fetchone()[0]

            print(f"{table_name}: {count}")
    finally:
        conn.close()


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "demo":
        run_demo()
        return 0

    if args.command == "init-db":
        db_path = args.db.expanduser()
        db_path.parent.mkdir(parents=True, exist_ok=True)
        CAPDatabase(db_path).init_cas_tables()
        print(f"CAP tables initialized: {db_path}")
        return 0

    if args.command == "status":
        show_status(args.db)
        return 0

    raise RuntimeError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
