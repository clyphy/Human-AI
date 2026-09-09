#!/usr/bin/env python3
"""
Real Coxeter-plane projection of the E8 root system.

Method (standard, e.g. Coxeter 1985 / Baez):
  1. Build the Coxeter element w = s1 s2 ... s8 (product of the 8
     simple-root reflections, in order).
  2. w has eigenvalues e^(2*pi*i*m_k/h) where h=30 is the Coxeter
     number and m_k are the exponents {1,7,11,13,17,19,23,29}.
  3. The eigenvector for the primitive eigenvalue e^(2*pi*i/30) is
     complex; its real and imaginary parts span the Coxeter plane.
  4. Projecting all 240 roots onto that 2D plane gives the classic
     image with exact 30-fold rotational symmetry (verified below,
     not assumed).
"""
import numpy as np
from e8_root_system import generate_all_roots, SIMPLE_ROOTS

def reflection_matrix(alpha):
    alpha = alpha / np.linalg.norm(alpha)
    return np.eye(8) - 2.0 * np.outer(alpha, alpha)

def coxeter_element(simple_roots):
    W = np.eye(8)
    for alpha in simple_roots:
        W = reflection_matrix(alpha) @ W
    return W

def coxeter_plane_basis():
    W = coxeter_element(SIMPLE_ROOTS)
    eigvals, eigvecs = np.linalg.eig(W)
    h = 30
    target = np.exp(2j * np.pi / h)
    idx = np.argmin(np.abs(eigvals - target))
    v = eigvecs[:, idx]
    u1 = np.real(v)
    u2 = np.imag(v)
    u1 /= np.linalg.norm(u1)
    u2 = u2 - np.dot(u2, u1) * u1
    u2 /= np.linalg.norm(u2)
    return u1, u2, eigvals

def project_roots():
    roots = generate_all_roots()
    u1, u2, eigvals = coxeter_plane_basis()
    x = roots @ u1
    y = roots @ u2
    return roots, x, y, eigvals

def verify_symmetry(x, y, h=30):
    """Check that rotating by 2*pi/h maps the point set onto itself
    (within numerical tolerance) — proof this is a real Coxeter
    plane, not decoration."""
    theta = 2 * np.pi / h
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])
    pts = np.stack([x, y], axis=1)
    rotated = pts @ R.T
    matches = 0
    for p in rotated:
        d = np.min(np.linalg.norm(pts - p, axis=1))
        if d < 1e-6:
            matches += 1
    return matches, len(pts)

if __name__ == "__main__":
    roots, x, y, eigvals = project_roots()
    matches, total = verify_symmetry(x, y)
    print(f"Roots projected: {total}")
    print(f"30-fold symmetry check: {matches}/{total} points map onto the root set under 12° rotation")
    print(f"Radii range: {np.hypot(x,y).min():.4f} to {np.hypot(x,y).max():.4f}")
    unique_radii = np.unique(np.round(np.hypot(x, y), 4))
    print(f"Distinct radial shells: {len(unique_radii)}")
