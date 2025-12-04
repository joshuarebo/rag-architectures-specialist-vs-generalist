import pandas as pd
import numpy as np
from scipy import stats

print("=" * 70)
print("CALCULATING INTER-RATER CORRELATION")
print("Manual Evaluation vs LLM-as-Judge Scores")
print("=" * 70 + "\n")

# Load manual evaluation (Claude 3.5) - this is on 1-5 scale
manual_c35 = pd.read_csv('results_claude_3.5/blind_evaluation_results.csv')
print("Manual Blind Evaluation (Claude 3.5):")
print(manual_c35)
print()

# For correlation, we need the actual paired scores
# Manual evaluation: SAC-RAG=3.6/5, Generic Claude=4.9/5
# We need to compare with LLM-as-judge scores normalized to same scale

# Load LLM judge results (these are on 0-10 scale)
llm_c35 = pd.read_csv('results_claude_3.5/llm_judge_golden_comparison_CLAUDE35.csv')
print("LLM-as-Judge Evaluation (Claude 3.5):")
print(llm_c35)
print()

# Extract the overall average scores
manual_sac = 3.6  # from manual evaluation
manual_generic = 4.9

llm_sac = llm_c35.iloc[3, 2]  # SAC-RAG overall from LLM judge
llm_base = llm_c35.iloc[3, 1]  # Base RAG overall from LLM judge

print(f"Manual Scores (1-5 scale):")
print(f"  SAC-RAG: {manual_sac}")
print(f"  Generic Claude: {manual_generic}")
print()

# Normalize LLM scores to 1-5 scale for fair comparison
llm_sac_normalized = (llm_sac / 10) * 5
llm_base_normalized = (llm_base / 10) * 5

print(f"LLM-as-Judge Scores (normalized to 1-5 scale):")
print(f"  SAC-RAG: {llm_sac_normalized:.2f} (original: {llm_sac:.2f}/10)")
print(f"  Base RAG: {llm_base_normalized:.2f} (original: {llm_base:.2f}/10)")
print()

# We only have 2 paired data points (SAC-RAG and Generic Claude)
# This is insufficient for meaningful correlation
# We need per-question scores for proper correlation

print("=" * 70)
print("ISSUE: Insufficient data for correlation calculation")
print("=" * 70)
print("\nWe only have aggregate scores (2 systems), not per-question scores.")
print("For valid Pearson correlation, we need individual question scores.")
print("\nRecommendation:")
print("  - Remove the (r = 0.78, p < 0.01) statistic")
print("  - OR use qualitative statement: 'demonstrating general alignment'")
print("  - OR calculate based on ±12% variance mentioned in inter-rater graph")
print()

# Calculate the absolute difference
manual_diff = abs(manual_generic - manual_sac)
llm_diff = abs(llm_base_normalized - llm_sac_normalized)

print("System Ranking Agreement:")
print(f"  Manual: Generic Claude > SAC-RAG (diff: {manual_diff:.2f})")
print(f"  LLM Judge: Base RAG > SAC-RAG (diff: {llm_diff:.2f})")
print(f"  → Both agree SAC-RAG underperforms, suggesting qualitative alignment")
print()

print("=" * 70)
print("CONCLUSION")
print("=" * 70)
print("\nWithout per-question manual scores, we cannot calculate")
print("a valid Pearson correlation coefficient.")
print("\nRecommended text:")
print('  "...triangulated against independent manual blind evaluation,')
print('   demonstrating consistent system rankings despite methodological')
print('   differences (±12% average score variance)."')
