"""
Generate Metric Breakdown Visualization for Claude Sonnet 4.5
Base RAG vs SAC-RAG Comparison
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Set publication-quality style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# Data from original generate_thesis_visualizations.py
metrics = ['Accuracy', 'Completeness', 'Clarity']
base_rag_scores = [8.70, 7.60, 9.40]
sac_rag_scores = [7.90, 6.50, 8.50]

# Calculate performance gaps
gaps = [((sac - base) / base * 100) for sac, base in zip(sac_rag_scores, base_rag_scores)]

# Create figure
fig, ax = plt.subplots(figsize=(12, 7))

x = np.arange(len(metrics))
width = 0.35

# Base RAG won overall, so it's the winner (green)
# SAC-RAG is comparison (red)
bars1 = ax.bar(x - width/2, base_rag_scores, width, label='Base RAG (Winner)', 
               color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x + width/2, sac_rag_scores, width, label='SAC-RAG', 
               color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)

ax.set_ylabel('Score (/10)', fontweight='bold')
ax.set_title('Claude Sonnet 4.5: Base RAG vs SAC-RAG\nLLM-as-a-Judge Evaluation', 
             fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.set_ylim(0, 10.5)
ax.legend(frameon=True, shadow=True)
ax.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontweight='bold')

# Add overall result annotation (top)
ax.text(0.5, 0.95, 'Overall: Base RAG +10.89%', 
        transform=ax.transAxes, fontsize=11, 
        fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', 
                  edgecolor='green', alpha=0.7))

# Add performance gap annotations below the banner
gap_labels = [f'{gap:+.2f}%' for gap in gaps]
gap_colors = ['#e74c3c' if gap < 0 else '#2ecc71' for gap in gaps]

for i, (gap_label, color) in enumerate(zip(gap_labels, gap_colors)):
    # Position below the overall banner
    ax.text(i, 9.2, gap_label, ha='center', fontsize=11, 
            color=color, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                     edgecolor=color, alpha=0.8, linewidth=1.5))

plt.tight_layout()

# Save to thesis_visualizations
output_path = Path('thesis_visualizations') / '03_metric_breakdown.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Saved: {output_path}")
plt.close()

print("\nMetric Breakdown Summary (Claude Sonnet 4.5):")
print("=" * 60)
for metric, base, sac, gap in zip(metrics, base_rag_scores, sac_rag_scores, gaps):
    winner = "Base RAG" if gap < 0 else "SAC-RAG" if gap > 0 else "Tie"
    print(f"{metric:15s}: Base={base:.1f}, SAC={sac:.1f}, Gap={gap:+.2f}% ({winner})")
print(f"\nOverall Average: Base=8.57, SAC=7.63, Gap=-10.89% (Base RAG wins)")
print("=" * 60)
