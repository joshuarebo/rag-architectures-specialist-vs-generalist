import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Data from LLM judge evaluations - all 4 systems
systems = ['SAC-RAG\nClaude 3.5', 'Base RAG\nClaude 3.5', 'SAC-RAG\nClaude 4.5', 'Base RAG\nClaude 4.5']

# Exact scores from the CSV files
accuracy = [9.3, 9.4, 7.9, 8.7]
completeness = [8.4, 7.6, 6.5, 7.6]
clarity = [9.4, 9.3, 8.5, 9.4]
overall = [9.033333333333333, 8.766666666666667, 7.633333333333333, 8.566666666666666]

# Set up the plot
fig, ax = plt.subplots(figsize=(14, 8))

# X-axis positions
x = np.arange(len(systems))
width = 0.18

# Create bars with distinct colors
bars1 = ax.bar(x - 1.5*width, accuracy, width, label='Accuracy', color='#3498db', alpha=0.9)
bars2 = ax.bar(x - 0.5*width, completeness, width, label='Completeness', color='#e74c3c', alpha=0.9)
bars3 = ax.bar(x + 0.5*width, clarity, width, label='Clarity', color='#2ecc71', alpha=0.9)
bars4 = ax.bar(x + 1.5*width, overall, width, label='Overall Average', color='#f39c12', alpha=0.9, edgecolor='black', linewidth=2)

# Customize plot
ax.set_xlabel('System Configuration', fontsize=13, fontweight='bold', labelpad=10)
ax.set_ylabel('Score (out of 10)', fontsize=13, fontweight='bold')
ax.set_title('SAC-RAG vs Base RAG Performance: Claude 3.5 Sonnet vs Claude 4.5 Sonnet\n(LLM-as-Judge Evaluation on Golden Question Set)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(systems, fontsize=11, fontweight='bold')
ax.set_ylim(0, 11.5)

# Grid
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on ALL bars
def add_value_labels(bars, offset=0.12, fontsize=8, decimals=1):
    for bar in bars:
        height = bar.get_height()
        format_str = f'{{:.{decimals}f}}'
        ax.text(bar.get_x() + bar.get_width()/2., height + offset,
                format_str.format(height),
                ha='center', va='bottom', fontsize=fontsize, fontweight='bold')

# Add labels to all bars
add_value_labels(bars1, offset=0.1, fontsize=8, decimals=1)
add_value_labels(bars2, offset=0.1, fontsize=8, decimals=1)
add_value_labels(bars3, offset=0.1, fontsize=8, decimals=1)
add_value_labels(bars4, offset=0.1, fontsize=9, decimals=2)

# Clean visual separator between models
ax.axvline(x=1.5, color='gray', linestyle='--', linewidth=2, alpha=0.6)

# Model labels at the top - positioned to avoid legend
ax.text(0.5, 11.0, 'Claude 3.5 Sonnet', ha='center', fontsize=12, 
        fontweight='bold', bbox=dict(boxstyle='round,pad=0.6', facecolor='#E3F2FD', alpha=0.9, edgecolor='blue', linewidth=1.5))
ax.text(2.5, 11.0, 'Claude 4.5 Sonnet', ha='center', fontsize=12, 
        fontweight='bold', bbox=dict(boxstyle='round,pad=0.6', facecolor='#FFEBEE', alpha=0.9, edgecolor='red', linewidth=1.5))

# Legend at BOTTOM CENTER - horizontal layout, outside plot area
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), fontsize=10, framealpha=0.95, ncol=4, fancybox=True, shadow=True)

# Winner annotations at the bottom  
ax.text(0.5, 0.8, 'Winner: SAC-RAG (+3.04%)', ha='center', fontsize=9, 
        fontweight='bold', bbox=dict(boxstyle='round,pad=0.4', facecolor='lightgreen', alpha=0.8))
ax.text(2.5, 0.8, 'Winner: Base RAG (+10.89%)', ha='center', fontsize=9, 
        fontweight='bold', bbox=dict(boxstyle='round,pad=0.4', facecolor='lightcoral', alpha=0.8))

plt.tight_layout()
plt.savefig('thesis_visualizations/04_three_way_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Final fix: Legend positioned at bottom center - covers nothing!")
