import pandas as pd
import random

# Read the manual evaluation template (should have both SAC-RAG and Generic Claude answers)
df_manual = pd.read_excel('manual_evaluation_template.xlsx')

print(f"Creating blind evaluation from {len(df_manual)} questions...\n")

# Create blind evaluation data
blind_eval_data = []

for _, row in df_manual.iterrows():
    answers = [
        ('SAC-RAG_Claude4.5', row['SAC_RAG_Answer']),
        ('Generic_Claude', row['Generic_Claude_Answer'])
    ]
    
    random.shuffle(answers)
    
    blind_eval_data.append({
        'Question_ID': row['Question_ID'],
        'Question': row['Question'],
        'Ground_Truth': row['Ground_Truth'],
        'Answer_A': answers[0][1],
        'Answer_A_System': answers[0][0],
        'Answer_B': answers[1][1],
        'Answer_B_System': answers[1][0],
        'Score_A': '',
        'Score_B': '',
        'Winner': '',
        'Notes': ''
    })

df_blind = pd.DataFrame(blind_eval_data)

# Create files
df_scoring = df_blind[['Question_ID', 'Question', 'Ground_Truth', 'Answer_A', 'Answer_B', 
                        'Score_A', 'Score_B', 'Winner', 'Notes']].copy()
df_answer_key = df_blind[['Question_ID', 'Answer_A_System', 'Answer_B_System']].copy()

df_scoring.to_excel('blind_evaluation_scoring_sheet.xlsx', index=False)
df_answer_key.to_excel('blind_evaluation_answer_key.xlsx', index=False)

print("✅ Created:")
print("   - blind_evaluation_scoring_sheet.xlsx")
print("   - blind_evaluation_answer_key.xlsx")
print("\nReady for blind evaluation!")
