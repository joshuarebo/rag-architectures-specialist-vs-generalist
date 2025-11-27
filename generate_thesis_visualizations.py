"""
Thesis Visualizations Generator
Generates comprehensive charts and graphs for thesis appendix
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set publication-quality style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# Create output directory
output_dir = Path("thesis_visualizations")
output_dir.mkdir(exist_ok=True)

print("=" * 80)
print("GENERATING THESIS VISUALIZATIONS")
print("=" * 80 + "\n")

# ============================================================================
# 1. BASE RAG vs SAC-RAG COMPARISON (CLAUDE 3.5 vs 4.5)
# ============================================================================
print("1. Generating Base RAG vs SAC-RAG comparison...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Claude 3.5 comparison
models_35 = ['Base RAG', 'SAC-RAG']
scores_35 = [8.7667, 9.0333]
colors_35 = ['#3498db', '#2ecc71']

bars1 = ax1.bar(models_35, scores_35, color=colors_35, alpha=0.7, edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Average Score (/10)', fontweight='bold')
ax1.set_title('Claude 3.5 Sonnet: SAC-RAG Wins (+3.04%)', fontweight='bold', fontsize=13)
ax1.set_ylim(0, 10)
ax1.axhline(y=8.5, color='gray', linestyle='--', alpha=0.3, label='Baseline')
ax1.grid(axis='y', alpha=0.3)

# Add value labels
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}',
             ha='center', va='bottom', fontweight='bold', fontsize=11)

# Claude 4.5 comparison
models_45 = ['Base RAG', 'SAC-RAG']
scores_45 = [8.5667, 7.6333]
colors_45 = ['#2ecc71', '#e74c3c']

bars2 = ax2.bar(models_45, scores_45, color=colors_45, alpha=0.7, edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Average Score (/10)', fontweight='bold')
ax2.set_title('Claude 4.5 Sonnet: Base RAG Wins (+10.89%)', fontweight='bold', fontsize=13)
ax2.set_ylim(0, 10)
ax2.axhline(y=8.0, color='gray', linestyle='--', alpha=0.3, label='Baseline')
ax2.grid(axis='y', alpha=0.3)

# Add value labels
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}',
             ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.suptitle('Model-Dependent Performance: Base RAG vs SAC-RAG', 
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(output_dir / '01_base_vs_sac_comparison.png', dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_dir / '01_base_vs_sac_comparison.png'}")
plt.close()

# ============================================================================
# 2. SAC-RAG MODEL UPGRADE (ABLATION STUDY)
# ============================================================================
print("2. Generating ablation study visualization...")

fig, ax = plt.subplots(figsize=(10, 6))

models = ['Claude 3.5\nSonnet', 'Claude 4.5\nSonnet']
sac_scores = [3.60, 4.70]  # Manual evaluation scores (1-5 scale)
generic_scores = [4.90, 4.80]  # Generic Claude scores

x = np.arange(len(models))
width = 0.35

bars1 = ax.bar(x - width/2, sac_scores, width, label='SAC-RAG', 
               color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x + width/2, generic_scores, width, label='Generic Claude', 
               color='#e67e22', alpha=0.8, edgecolor='black', linewidth=1.5)

ax.set_ylabel('Average Score (/5)', fontweight='bold')
ax.set_title('Ablation Study: Model Upgrade Impact on SAC-RAG\n(Manual Blind Evaluation)', 
             fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.set_ylim(0, 5.5)
ax.legend(frameon=True, shadow=True)
ax.grid(axis='y', alpha=0.3)

# Add value labels and improvement arrows
for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
    height1 = bar1.get_height()
    height2 = bar2.get_height()
    ax.text(bar1.get_x() + bar1.get_width()/2., height1,
            f'{height1:.2f}',
            ha='center', va='bottom', fontweight='bold')
    ax.text(bar2.get_x() + bar2.get_width()/2., height2,
            f'{height2:.2f}',
            ha='center', va='bottom', fontweight='bold')

# Add improvement annotation
ax.annotate('', xy=(0.15, 4.70), xytext=(0.15, 3.60),
            arrowprops=dict(arrowstyle='->', color='green', lw=2.5))
ax.text(0.4, 4.15, '+30.6%\nimprovement', fontsize=11, 
        color='green', fontweight='bold', ha='left')

plt.tight_layout()
plt.savefig(output_dir / '02_ablation_study.png', dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_dir / '02_ablation_study.png'}")
plt.close()

# ============================================================================
# 3. METRIC BREAKDOWN (ACCURACY, COMPLETENESS, CLARITY)
# ============================================================================
print("3. Generating metric breakdown...")

fig, ax = plt.subplots(figsize=(12, 7))

metrics = ['Accuracy', 'Completeness', 'Clarity']
base_rag_scores = [8.70, 7.60, 9.40]
sac_rag_scores = [7.90, 6.50, 8.50]

x = np.arange(len(metrics))
width = 0.35

bars1 = ax.bar(x - width/2, base_rag_scores, width, label='Base RAG (Winner)', 
               color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x + width/2, sac_rag_scores, width, label='SAC-RAG', 
               color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)

ax.set_ylabel('Score (/10)', fontweight='bold')
ax.set_title('Metric Breakdown: Base RAG vs SAC-RAG (Claude 4.5)\nLLM-as-a-Judge Evaluation', 
             fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.set_ylim(0, 10.5)
ax.legend(frameon=True, shadow=True)
ax.grid(axis='y', alpha=0.3)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontweight='bold')

# Add performance gap annotations
gaps = ['-9.20%', '-14.47%', '-9.57%']
for i, gap in enumerate(gaps):
    ax.text(i, 10, gap, ha='center', fontsize=10, 
            color='red', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '03_metric_breakdown.png', dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_dir / '03_metric_breakdown.png'}")
plt.close()

# ============================================================================
# 4. THREE-WAY COMPARISON (NORMALIZED SCORES)
# ============================================================================
print("4. Generating three-way comparison...")

fig, ax = plt.subplots(figsize=(10, 7))

systems = ['Base RAG\n(Claude 4.5)', 'SAC-RAG\n(Claude 4.5)', 'Generic Claude\n(4.0)']
scores = [8.57, 9.40, 9.60]  # Normalized to 0-10
colors = ['#3498db', '#9b59b6', '#e67e22']
contexts = ['vs SAC-RAG\n(LLM Judge)', 'vs Generic\n(Manual)', 'vs SAC-RAG\n(Manual)']

bars = ax.bar(systems, scores, color=colors, alpha=0.7, edgecolor='black', linewidth=2)

ax.set_ylabel('Performance Score (Normalized 0-10)', fontweight='bold')
ax.set_title('Three-Way System Comparison\n(Note: Different evaluation contexts)', 
             fontweight='bold', fontsize=14)
ax.set_ylim(0, 10.5)
ax.grid(axis='y', alpha=0.3)
ax.axhline(y=9.0, color='green', linestyle='--', alpha=0.5, linewidth=2, label='High Performance (9.0+)')

# Add value labels and context
for i, (bar, context) in enumerate(zip(bars, contexts)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}',
            ha='center', va='bottom', fontweight='bold', fontsize=12)
    ax.text(bar.get_x() + bar.get_width()/2., 0.5,
            context,
            ha='center', va='bottom', fontsize=9, style='italic')

ax.legend(loc='lower right')

plt.tight_layout()
plt.savefig(output_dir / '04_three_way_comparison.png', dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_dir / '04_three_way_comparison.png'}")
plt.close()

# ============================================================================
# 5. MODEL QUALITY VS RETRIEVAL IMPACT
# ============================================================================
print("5. Generating impact comparison...")

fig, ax = plt.subplots(figsize=(10, 6))

factors = ['Model Upgrade\n(Claude 3.5→4.5)', 'Retrieval\nOptimization\n(SAC-RAG vs Base)']
impacts = [30.6, 3.04]
colors_impact = ['#2ecc71', '#3498db']

bars = ax.bar(factors, impacts, color=colors_impact, alpha=0.8, 
              edgecolor='black', linewidth=2)

ax.set_ylabel('Performance Improvement (%)', fontweight='bold')
ax.set_title('Impact Comparison: Model Quality vs Retrieval Optimization\n10x Difference', 
             fontweight='bold', fontsize=14)
ax.set_ylim(0, 35)
ax.grid(axis='y', alpha=0.3)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}%',
            ha='center', va='bottom', fontweight='bold', fontsize=13)

# Add 10x annotation
ax.annotate('10x larger\nimpact', xy=(0.5, 16), xytext=(1.3, 20),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=12, color='red', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))

plt.tight_layout()
plt.savefig(output_dir / '05_impact_comparison.png', dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_dir / '05_impact_comparison.png'}")
plt.close()

# ============================================================================
# 6. INTER-RATER RELIABILITY (MANUAL VS AUTOMATED)
# ============================================================================
print("6. Generating inter-rater reliability...")

fig, ax = plt.subplots(figsize=(12, 6))

systems_eval = ['SAC-RAG\n(Claude 3.5)', 'Generic Claude\n(Claude 3.5)', 
                'SAC-RAG\n(Claude 4.5)', 'Generic Claude\n(Claude 4.5)']
manual_scores = [3.60, 4.90, 4.70, 4.80]
automated_scores = [4.20, 4.30, 4.10, 4.60]

x = np.arange(len(systems_eval))
width = 0.35

bars1 = ax.bar(x - width/2, manual_scores, width, label='Manual (Human)', 
               color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x + width/2, automated_scores, width, label='Automated (LLM-as-a-Judge)', 
               color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)

ax.set_ylabel('Average Score (/5)', fontweight='bold')
ax.set_title('Inter-Rater Reliability: Manual vs Automated Evaluation\n±12% average variance', 
             fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(systems_eval)
ax.set_ylim(0, 5.5)
ax.legend(frameon=True, shadow=True)
ax.grid(axis='y', alpha=0.3)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig(output_dir / '06_inter_rater_reliability.png', dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_dir / '06_inter_rater_reliability.png'}")
plt.close()

# ============================================================================
# 7. COST-BENEFIT ANALYSIS
# ============================================================================
print("7. Generating cost-benefit analysis...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Cost comparison
systems_cost = ['Generic\nClaude', 'Base RAG', 'SAC-RAG']
setup_costs = [0, 5, 5]
query_costs = [0, 0.012, 0.012]

x_cost = np.arange(len(systems_cost))
width_cost = 0.35

bars1 = ax1.bar(x_cost - width_cost/2, setup_costs, width_cost, label='Setup Cost ($)', 
                color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax1.bar(x_cost + width_cost/2, [c*1000 for c in query_costs], width_cost, 
                label='Per-Query Cost ($×1000)', 
                color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)

ax1.set_ylabel('Cost ($)', fontweight='bold')
ax1.set_title('Cost Comparison', fontweight='bold')
ax1.set_xticks(x_cost)
ax1.set_xticklabels(systems_cost)
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Performance vs Cost
systems_perf = ['Generic\nClaude', 'SAC-RAG\n(Claude 4.5)', 'Base RAG\n(Claude 4.5)']
performance = [9.60, 9.40, 8.57]
total_cost = [0, 5.12, 5.12]  # Setup + 10 queries

scatter = ax2.scatter(total_cost, performance, s=300, alpha=0.6, 
                     c=['#e67e22', '#9b59b6', '#3498db'], edgecolors='black', linewidth=2)

for i, system in enumerate(systems_perf):
    ax2.annotate(system, (total_cost[i], performance[i]), 
                 xytext=(10, 10), textcoords='offset points',
                 fontweight='bold', fontsize=10,
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))

ax2.set_xlabel('Total Cost for 10 Queries ($)', fontweight='bold')
ax2.set_ylabel('Performance Score (/10)', fontweight='bold')
ax2.set_title('Performance vs Cost Trade-off', fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(-0.5, 6)
ax2.set_ylim(8, 10)

plt.suptitle('Cost-Benefit Analysis', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(output_dir / '07_cost_benefit.png', dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_dir / '07_cost_benefit.png'}")
plt.close()

# ============================================================================
# 8. SUMMARY DASHBOARD
# ============================================================================
print("8. Generating summary dashboard...")

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Top left: Key finding
ax1 = fig.add_subplot(gs[0, :])
ax1.text(0.5, 0.5, 'KEY FINDING: Model Quality Dominates (10x Impact)\n' + 
         'Model Upgrade: +30.6%  |  Retrieval Optimization: +3.04%',
         ha='center', va='center', fontsize=18, fontweight='bold',
         bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.8))
ax1.axis('off')

# Middle left: Claude 3.5 comparison
ax2 = fig.add_subplot(gs[1, 0])
ax2.bar(['Base', 'SAC'], [8.77, 9.03], color=['#3498db', '#2ecc71'], alpha=0.7)
ax2.set_title('Claude 3.5:\nSAC Wins (+3.04%)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Score (/10)')
ax2.set_ylim(0, 10)
ax2.grid(axis='y', alpha=0.3)

# Middle center: Claude 4.5 comparison
ax3 = fig.add_subplot(gs[1, 1])
ax3.bar(['Base', 'SAC'], [8.57, 7.63], color=['#2ecc71', '#e74c3c'], alpha=0.7)
ax3.set_title('Claude 4.5:\nBase Wins (+10.89%)', fontsize=11, fontweight='bold')
ax3.set_ylabel('Score (/10)')
ax3.set_ylim(0, 10)
ax3.grid(axis='y', alpha=0.3)

# Middle right: Model upgrade
ax4 = fig.add_subplot(gs[1, 2])
ax4.bar(['3.5', '4.5'], [3.60, 4.70], color=['#e74c3c', '#2ecc71'], alpha=0.7)
ax4.set_title('SAC-RAG Upgrade:\n+30.6%', fontsize=11, fontweight='bold')
ax4.set_ylabel('Score (/5)')
ax4.set_ylim(0, 5)
ax4.grid(axis='y', alpha=0.3)

# Bottom row: Three-way comparison
ax5 = fig.add_subplot(gs[2, :])
systems_final = ['Base RAG\n(Claude 4.5)', 'SAC-RAG\n(Claude 4.5)', 'Generic Claude\n(4.5)']
scores_final = [8.57, 9.40, 9.60]
colors_final = ['#3498db', '#9b59b6', '#e67e22']
bars_final = ax5.bar(systems_final, scores_final, color=colors_final, alpha=0.7, 
                     edgecolor='black', linewidth=2)
ax5.set_title('Final System Comparison (Normalized Scores)', fontsize=13, fontweight='bold')
ax5.set_ylabel('Performance (/10)', fontweight='bold')
ax5.set_ylim(0, 10.5)
ax5.grid(axis='y', alpha=0.3)
ax5.axhline(y=9.0, color='green', linestyle='--', alpha=0.5, linewidth=1.5)

for bar in bars_final:
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}',
             ha='center', va='bottom', fontweight='bold', fontsize=12)

plt.suptitle('RAG Systems Evaluation Summary Dashboard', 
             fontsize=20, fontweight='bold', y=0.98)
plt.savefig(output_dir / '08_summary_dashboard.png', dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_dir / '08_summary_dashboard.png'}")
plt.close()

print("\n" + "=" * 80)
print("✓ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
print(f"✓ Location: {output_dir.absolute()}")
print("=" * 80)
print("\nGenerated visualizations:")
print("1. Base RAG vs SAC-RAG comparison (model-dependent)")
print("2. Ablation study (model upgrade impact)")
print("3. Metric breakdown (accuracy, completeness, clarity)")
print("4. Three-way system comparison")
print("5. Impact comparison (10x finding)")
print("6. Inter-rater reliability")
print("7. Cost-benefit analysis")
print("8. Summary dashboard")
print("\nReady for thesis appendix! 📊")
