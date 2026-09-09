#!/usr/bin/env python3
"""Render the real E8 Coxeter-plane projection as SVG.
Every coordinate here comes from actual linear algebra
(e8_coxeter_plane.py) — nothing is placed by hand or by aesthetic
guess.
"""
import numpy as np
from e8_root_system import generate_all_roots, generate_type1_roots
from e8_coxeter_plane import project_roots

def build_svg(path="e8_coxeter_plane.svg", size=900):
    roots, x, y, eigvals = project_roots()
    type1_roots = np.array(generate_type1_roots())

    # classify each projected point: is it a Type-I (D8) root?
    is_type1 = np.array([
        any(np.allclose(r, t1) for t1 in type1_roots) for r in roots
    ])

    scale = (size / 2 - 40) / np.max(np.hypot(x, y))
    cx, cy = size / 2, size / 2

    def px(v): return cx + v * scale
    def py(v): return cy - v * scale

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">')
    lines.append(f'<rect width="{size}" height="{size}" fill="#0a0a14"/>')

    # edges: connect roots whose inner product (in original 8D) is +1 (60 degree angle)
    edge_count = 0
    max_edges = 2000  # cap for file size / render time
    for i in range(len(roots)):
        for j in range(i + 1, len(roots)):
            if edge_count >= max_edges:
                break
            dot = np.dot(roots[i], roots[j])
            if abs(dot - 1.0) < 1e-6:
                lines.append(
                    f'<line x1="{px(x[i]):.2f}" y1="{py(y[i]):.2f}" '
                    f'x2="{px(x[j]):.2f}" y2="{py(y[j]):.2f}" '
                    f'stroke="#3a4a6b" stroke-width="0.3" opacity="0.35"/>'
                )
                edge_count += 1
        if edge_count >= max_edges:
            break

    # nodes
    for i in range(len(roots)):
        color = "#e8b84a" if is_type1[i] else "#4ac8e8"
        r = 3.2 if is_type1[i] else 2.4
        lines.append(f'<circle cx="{px(x[i]):.2f}" cy="{py(y[i]):.2f}" r="{r}" fill="{color}" opacity="0.9"/>')

    lines.append(
        f'<text x="20" y="{size-50}" fill="#8899aa" font-family="monospace" font-size="14">'
        f'E8 root system — Coxeter plane projection (real, computed)</text>'
    )
    lines.append(
        f'<text x="20" y="{size-30}" fill="#8899aa" font-family="monospace" font-size="12">'
        f'240 roots · h=30 · gold=Type-I (D8, 112) · cyan=half-spinor (128) · edges=60° adjacency ({edge_count} shown)</text>'
    )
    lines.append('</svg>')

    svg = "\n".join(lines)
    with open(path, "w") as f:
        f.write(svg)
    return path, edge_count

if __name__ == "__main__":
    path, edges = build_svg()
    print(f"Wrote {path} with {edges} edges")
