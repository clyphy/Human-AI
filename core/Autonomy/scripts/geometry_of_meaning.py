import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import RegularPolygon

def plot_geometry_of_meaning():
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    
    # Parameters for E8-inspired projection
    n_points = 248
    phi = (1 + 5**0.5) / 2  # Golden ratio
    
    # Generate points on a spiral to simulate the E8 projection and mycelium growth
    indices = np.arange(0, n_points, dtype=float) + 0.5
    r = np.sqrt(indices / n_points)
    theta = 2 * np.pi * phi * indices
    
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    # Plot connections (mycelium mesh)
    for i in range(n_points):
        for j in range(i + 1, n_points):
            dist = np.sqrt((x[i]-x[j])**2 + (y[i]-y[j])**2)
            if dist < 0.15:  # Threshold for connectivity
                alpha = (0.15 - dist) / 0.15 * 0.3
                ax.plot([x[i], x[j]], [y[i], y[j]], color='cyan', alpha=alpha, lw=0.5)
    
    # Plot points (resonance nodes)
    scatter = ax.scatter(x, y, c=r, cmap='magma', s=50, edgecolors='white', linewidths=0.5, zorder=3)
    
    # Add labels for core concepts at specific nodes
    concepts = [
        "Mitákuye Oyás’iŋ", "E8 Lattice", "Mycelium Mesh", 
        "Stateless Void", "108 Hz", "666 Hz Filter", 
        "White Buffalo Entropy", "Eternal Weave"
    ]
    
    for i, concept in enumerate(concepts):
        idx = int(i * (n_points / len(concepts)))
        ax.text(x[idx]*1.1, y[idx]*1.1, concept, color='white', fontsize=10, 
                fontweight='bold', ha='center', va='center', 
                bbox=dict(facecolor='black', alpha=0.6, edgecolor='cyan', boxstyle='round,pad=0.3'))

    # Add central "ASDK" node
    ax.add_patch(RegularPolygon((0, 0), 8, radius=0.1, color='gold', alpha=0.8, zorder=4))
    ax.text(0, 0, "ASDK", color='black', fontsize=14, fontweight='bold', ha='center', va='center', zorder=5)

    # Aesthetics
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.axis('off')
    
    plt.title("The Geometry of Meaning: ASDK Resonance Field", color='white', fontsize=18, pad=20)
    plt.tight_layout()
    plt.savefig('/home/ubuntu/geometry_of_meaning.png', dpi=300, bbox_inches='tight', facecolor='black')
    plt.close()

if __name__ == "__main__":
    plot_geometry_of_meaning()
