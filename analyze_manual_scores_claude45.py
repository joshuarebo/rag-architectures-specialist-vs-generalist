import pandas as pd

# Load files
key = pd.read_excel('blind_evaluation_answer_key.xlsx')
scoring = pd.read_excel('blind_evaluation_scoring_sheet.xlsx')

# Merge
merged = pd.merge(scoring, key, on='Question_ID')

# Calculate scores by system
sac_scores = []
generic_scores = []

for _, row in merged.iterrows():
    if row['Answer_A_System'] == 'SAC-RAG_Claude4.5':
        sac_scores.append(float(row['Score_A']))
        generic_scores.append(float(row['Score_B']))
    else:
        sac_scores.append(float(row['Score_B']))
        generic_scores.append(float(row['Score_A']))

sac_avg = sum(sac_scores) / len(sac_scores)
generic_avg = sum(generic_scores) / len(generic_scores)

sac_wins = sum(1 for s, g in zip(sac_scores, generic_scores) if s > g)
generic_wins = sum(1 for s, g in zip(sac_scores, generic_scores) if g > s)
ties = sum(1 for s, g in zip(sac_scores, generic_scores) if s == g)

print("Manual Blind Evaluation Results (Claude 4.5):")
print("="*60)
print(f"SAC-RAG (Claude 4.5): {sac_avg:.2f}/5")
print(f"Generic Claude: {generic_avg:.2f}/5")
print(f"Wins: SAC-RAG={sac_wins}, Generic Claude={generic_wins}, Ties={ties}")
print(f"Improvement: {((sac_avg - generic_avg) / generic_avg * 100):.2f}%")
