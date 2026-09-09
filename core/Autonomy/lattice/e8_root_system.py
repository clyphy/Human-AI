#!/usr/bin/env python3
"""
E8 root system — real generation, not approximation.

The 240 roots live in R^8 (NOT 248 — that's dim of the Lie algebra,
a separate object; e8_manifest.json has this conflated, fixed here).

Two families:
  Type I  (D8 roots):   (+-1, +-1, 0,0,0,0,0,0) and all permutations
                         -> C(8,2) * 4 = 112 roots
  Type II (half-spinor): (+-1/2)^8 with an EVEN number of minus signs
                         -> 2^7 = 128 roots
  112 + 128 = 240 total, each of squared length 2.
"""
import itertools
import numpy as np

def generate_type1_roots():
    roots = []
    for i, j in itertools.combinations(range(8), 2):
        for si, sj in itertools.product([1, -1], repeat=2):
            v = np.zeros(8)
            v[i], v[j] = si, sj
            roots.append(v)
    return roots  # 112

def generate_type2_roots():
    roots = []
    for signs in itertools.product([1, -1], repeat=8):
        if signs.count(-1) % 2 == 0:  # even number of minus signs
            roots.append(np.array(signs) * 0.5)
    return roots  # 128

def generate_all_roots():
    roots = generate_type1_roots() + generate_type2_roots()
    arr = np.array(roots)
    assert arr.shape == (240, 8), f"expected (240,8), got {arr.shape}"
    lengths_sq = np.sum(arr ** 2, axis=1)
    assert np.allclose(lengths_sq, 2.0), "all roots must have squared length 2"
    return arr

# Bourbaki simple roots for E8 (standard reference basis)
SIMPLE_ROOTS = np.array([
    [1, -1, 0, 0, 0, 0, 0, 0],
    [0, 1, -1, 0, 0, 0, 0, 0],
    [0, 0, 1, -1, 0, 0, 0, 0],
    [0, 0, 0, 1, -1, 0, 0, 0],
    [0, 0, 0, 0, 1, -1, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 0],
    [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
    [0, 0, 0, 0, 0, 1, -1, 0],
], dtype=float)

def cartan_matrix(simple_roots):
    n = len(simple_roots)
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            C[i, j] = 2 * np.dot(simple_roots[i], simple_roots[j]) / np.dot(simple_roots[j], simple_roots[j])
    return np.round(C).astype(int)

def nearest_root(vec, roots):
    dists = np.linalg.norm(roots - vec, axis=1)
    idx = np.argmin(dists)
    return idx, roots[idx], dists[idx]
