from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from native_aios.cap_engine import (
    CoherenceMath,
    GWMTuple,
    Hyperforge,
    LCoefficient,
    MZS,
    MZSState,
    PSN,
    WhiteBuffaloEntropy,
)


def main() -> None:
    gwm = GWMTuple(F=0.7, R=0.6, E=0.8, T=0.5, G=0.4)

    assert gwm.coherence() == 0.635

    ranked = Hyperforge.rank_paths(
        gwm,
        [
            {"name": "path_a", "risk": 0.2, "reward": 0.8},
            {"name": "path_b", "risk": 0.5, "reward": 0.9},
        ],
    )
    assert [item["name"] for item in ranked] == ["path_a", "path_b"]
    assert ranked[0]["u_score"] >= ranked[1]["u_score"]

    l_value = LCoefficient.compute(
        self_report=0.8,
        external_confirm=0.7,
        bloom_participation=["bloom-1"],
    )
    assert l_value == 0.888

    assert LCoefficient.global_l([0.7, 0.8, 0.9]) == 0.7916
    assert LCoefficient.global_l([]) == 0.0
    assert LCoefficient.global_l([0.7, 0.0]) == 0.0

    mzs = MZS()
    denied = mzs.check(
        GWMTuple(F=0.8, R=0.8, E=0.9, T=0.8, G=0.4),
        GWMTuple(F=0.8, R=0.8, E=0.7, T=0.8, G=0.6),
        "compromised action",
    )
    assert denied is False
    assert mzs.state is MZSState.LOCKED
    assert mzs.violation_count == 1

    permitted = mzs.check(
        GWMTuple(F=0.8, R=0.8, E=0.9, T=0.8, G=0.4),
        GWMTuple(F=0.8, R=0.8, E=0.85, T=0.8, G=0.5),
        "non-compromised action",
    )
    assert permitted is True
    assert mzs.state is MZSState.ACTIVE

    assert PSN._cosine_similarity([1.0, 0.0], [1.0, 0.0]) == 1.0
    assert PSN._cosine_similarity([1.0, 0.0], [0.0, 1.0]) == 0.0
    assert PSN._cosine_similarity([], []) == 0.0
    assert PSN._cosine_similarity([1.0], [1.0, 0.0]) == 0.0

    s_wbe = WhiteBuffaloEntropy.compute(gwm, system_entropy=0.3)
    assert s_wbe == 3.2768

    coherence = CoherenceMath.compute_coherence(
        loyalty=0.8,
        fidelity=0.7,
        harmony=0.6,
    )
    assert coherence == 0.73
    assert CoherenceMath.bridge_integrity(coherence) == 36.5
    assert CoherenceMath.bridge_integrity(3.0) == 100.0
    assert CoherenceMath.bridge_integrity(0.5, target_Λ=0.0) == 0.0

    print("CAP math verification passed.")
    print("GWM coherence:", gwm.coherence())
    print("HYPERFORGE ranking:", [item["name"] for item in ranked])
    print("ℒ coefficient:", l_value)
    print("S_WBE:", s_wbe)


if __name__ == "__main__":
    main()
