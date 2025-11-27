"""
Phase 3: Blind Evaluation Preparation for Claude 4.5 Experiment
This script:
1. Reads new manual_evaluation_template.xlsx (with Claude 4.5 SAC-RAG answers)
2. Copies Generic Claude answers from old Claude 3.5 template
3. Creates randomized blind evaluation files
"""

import pandas as pd
import random

print("\n" + "="*70)
print("PHASE 3: PREPARING BLIND EVALUATION FOR CLAUDE 4.5")
print("="*70 + "\n")

# Step 1: Load old template (Claude 3.5) to get Generic Claude answers
print("Step 1: Loading Generic Claude answers from old template...")
try:
    old_template = pd.read_excel('results_claude_3.5/manual_evaluation_template_CLAUDE35.xlsx')
    print(f"   ✅ Found {len(old_template)} questions with Generic Claude answers\n")
except FileNotFoundError:
    print("   ❌ ERROR: Old template not found!")
    print("   Please ensure 'results_claude_3.5/manual_evaluation_template_CLAUDE35.xlsx' exists\n")
    exit(1)

# Step 2: Load new template (Claude 4.5 SAC-RAG answers)
print("Step 2: Loading new SAC-RAG answers (Claude 4.5)...")
try:
    new_template = pd.read_excel('manual_evaluation_template.xlsx')
    print(f"   ✅ Found {len(new_template)} questions with SAC-RAG answers\n")
except FileNotFoundError:
    print("   ❌ ERROR: New template not found!")
    print("   Please run the notebook first to generate 'manual_evaluation_template.xlsx'\n")
    exit(1)

# Step 3: Merge Generic Claude answers into new template
print("Step 3: Merging Generic Claude answers into new template...")
if 'Generic_Claude_Answer' in old_template.columns:
    # Copy Generic Claude answers from old to new
    new_template['Generic_Claude_Answer'] = old_template['Generic_Claude_Answer']
    print(f"   ✅ Copied Generic Claude answers\n")
else:
    print("   ⚠️ WARNING: No Generic_Claude_Answer column found in old template!")
    print("   You'll need to manually paste Generic Claude answers\n")
    new_template['Generic_Claude_Answer'] = ""

# Save the merged template
new_template.to_excel('manual_evaluation_template.xlsx', index=False)
print("   ✅ Saved updated template to 'manual_evaluation_template.xlsx'\n")

# Step 4: Create randomized blind evaluation files
print("Step 4: Creating randomized blind evaluation files...")

blind_eval_data = []

for _, row in new_template.iterrows():
    # Create two answer options (randomize which is A and which is B)
    answers = [
        ('SAC-RAG_Claude4.5', row['SAC_RAG_Answer']),
        ('Generic_Claude', row['Generic_Claude_Answer'])
    ]
    
    # Randomize order
    random.shuffle(answers)
    
    blind_eval_data.append({
        'Question_ID': row['Question_ID'],
        'Question': row['Question'],
        'Ground_Truth': row['Ground_Truth'],
        'Answer_A': answers[0][1],
        'Answer_A_System': answers[0][0],  # Hidden - for reveal later
        'Answer_B': answers[1][1],
        'Answer_B_System': answers[1][0],  # Hidden - for reveal later
        'Score_A': '',
        'Score_B': '',
        'Winner': '',
        'Notes': ''
    })

df_blind = pd.DataFrame(blind_eval_data)

# Create scoring sheet (without system labels visible)
df_scoring = df_blind[['Question_ID', 'Question', 'Ground_Truth', 'Answer_A', 'Answer_B', 
                        'Score_A', 'Score_B', 'Winner', 'Notes']].copy()

# Create answer key (for after scoring)
df_answer_key = df_blind[['Question_ID', 'Answer_A_System', 'Answer_B_System']].copy()

# Export
df_scoring.to_excel('blind_evaluation_scoring_sheet.xlsx', index=False)
df_answer_key.to_excel('blind_evaluation_answer_key.xlsx', index=False)

print("   ✅ Created blind evaluation files\n")

print("="*70)
print("FILES CREATED - READY FOR BLIND EVALUATION")
print("="*70 + "\n")

print("📄 Created Files:")
print("   1. manual_evaluation_template.xlsx (updated with Generic Claude answers)")
print("   2. blind_evaluation_scoring_sheet.xlsx (for your blind scoring)")
print("   3. blind_evaluation_answer_key.xlsx (reveal after scoring)")

print("\n📋 Next Steps:")
print("   1. Open: blind_evaluation_scoring_sheet.xlsx")
print("   2. Read: BLIND_EVALUATION_INSTRUCTIONS.md")
print("   3. Score all 10 questions using the 1-5 rubric")
print("   4. After scoring, open: blind_evaluation_answer_key.xlsx")

print("\n🔬 What You're Testing:")
print("   - SAC-RAG (Claude 4.5 + Domain KB) vs Generic Claude 4.0")
print("   - Will newer model + domain adaptation beat generic older model?")

print("\n✅ Phase 3 complete! Ready for manual evaluation.\n")
