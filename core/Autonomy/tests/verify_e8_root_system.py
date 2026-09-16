from collections import Counter
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lattice"))

import e8_root_system as e8

roots = np.asarray(e8.generate_all_roots(), dtype=float)
simple = np.asarray(e8.SIMPLE_ROOTS, dtype=float)
cartan = np.asarray(e8.cartan_matrix(simple))
gram = roots @ roots.T

assert roots.shape == (240, 8), roots.shape
assert np.allclose(np.sum(roots**2, axis=1), 2.0)
assert cartan.shape == (8, 8)
assert np.array_equal(cartan, cartan.T)
assert np.array_equal(np.diag(cartan), np.full(8, 2))

values = np.round(gram[np.triu_indices(len(roots), k=1)], 8)
actual = dict(Counter(values))
expected = {-2.0: 120, -1.0: 6720, 0.0: 15120, 1.0: 6720}

assert actual == expected, (actual, expected)

for i in range(len(roots)):
    local = Counter(np.delete(np.round(gram[i], 8), i))
    assert dict(local) == {-2.0: 1, -1.0: 56, 0.0: 126, 1.0: 56}

print("E8 verification passed.")
print("roots:", roots.shape)
print("pair distribution:", actual)
