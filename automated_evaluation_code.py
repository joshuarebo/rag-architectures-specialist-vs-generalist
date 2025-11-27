import pandas as pd
import time
from botocore.exceptions import ClientError

print("\n" + "="*60)
print("AUTOMATED LLM-AS-A-JUDGE EVALUATION")
print("SAC-RAG vs Generic Claude (Same Rubric: 1-5)")
print("="*60 + "\n")

# ============================================================
# Helper: Retry Logic
# ============================================================
def invoke_with_retry(llm, prompt, max_retries=5):
    """Invoke LLM with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            response = llm.invoke(prompt)
            # Extract content from AIMessage
            if hasattr(response, 'content'):
                return response.content
            return str(response)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ThrottlingException':
                if attempt < max_retries - 1:
                    wait_time = 5 * (2 ** attempt)  # 5s, 10s, 20s, 40s, 80s
                    print(f"      ⚠️ Throttled. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"      ❌ Failed after {max_retries} retries")
                    return None
            else:
                raise
        except Exception as e:
            print(f"      ❌ Error: {str(e)[:100]}")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                return None
    return None

# ============================================================
# LLM-as-a-Judge Scoring Function (1-5 Scale)
# ============================================================
def score_answer_rubric(question, answer, ground_truth, llm):
    """
    Score answer using same 1-5 rubric as manual evaluation:
    5 = Excellent (Kenyan law + specific sections)
    4 = Good (Kenyan law but less specific)
    3 = Acceptable (general law, misses nuance)
    2 = Poor (wrong jurisdiction or vague)
    1 = Dangerous (hallucinations or harmful)
    """
    
    prompt = f"""You are an expert evaluator of Kenyan legal Q&A systems.

**Question:** {question}

**Correct Answer (Ground Truth):** {ground_truth}

**Answer to Evaluate:**
{answer}

**Task:** Rate this answer using this rubric (1-5 scale):

**5 (Excellent)**: Accurate Kenyan law + cites specific sections/cases + clear reasoning + no hallucinations
**4 (Good)**: Accurate Kenyan law + correct reasoning, but lacks specific citations or slightly vague
**3 (Acceptable)**: Generally correct but misses nuance OR refers to general common law instead of Kenyan statutes
**2 (Poor)**: Vague OR applies non-Kenyan law (UK/US) to Kenyan context OR omits critical details
**1 (Dangerous)**: Factually incorrect OR hallucinations (fake statutes/cases) OR harmful advice

**CRITICAL:** Respond with ONLY a single number (1, 2, 3, 4, or 5). No explanations, no text."""

    response_text = invoke_with_retry(llm, prompt)
    
    if response_text:
        try:
            # Extract first number found
            import re
            match = re.search(r'[1-5]', response_text.strip())
            if match:
                score = int(match.group())
                return score
        except:
            pass
    
    return 0  # Default if parsing failed

# ============================================================
# Load Data and Evaluate
# ============================================================

# Read manual evaluation template (has Generic Claude answers)
df_manual = pd.read_excel('manual_evaluation_template.xlsx')

print("📊 Evaluating SAC-RAG vs Generic Claude (10 questions)")
print("="*60 + "\n")

sac_scores = []
generic_scores = []

for i, row in df_manual.iterrows():
    print(f"  Q{i+1}/10: {row['Question'][:60]}...")
    
    # Score SAC-RAG
    print(f"    Scoring SAC-RAG...", end=" ")
    sac_score = score_answer_rubric(
        row['Question'],
        row['SAC_RAG_Answer'],
        row['Ground_Truth'],
        llm_generate
    )
    sac_scores.append(sac_score)
    print(f"Score: {sac_score}/5")
    time.sleep(3)
    
    # Score Generic Claude
    print(f"    Scoring Generic Claude...", end=" ")
    generic_score = score_answer_rubric(
        row['Question'],
        row['Generic_Claude_Answer'],
        row['Ground_Truth'],
        llm_generate
    )
    generic_scores.append(generic_score)
    print(f"Score: {generic_score}/5")
    time.sleep(3)
    
    print()

# ============================================================
# Calculate Results
# ============================================================
sac_avg = sum(sac_scores) / len(sac_scores)
generic_avg = sum(generic_scores) / len(generic_scores)

# Count wins
sac_wins = sum(1 for s, g in zip(sac_scores, generic_scores) if s > g)
generic_wins = sum(1 for s, g in zip(sac_scores, generic_scores) if g > s)
ties = sum(1 for s, g in zip(sac_scores, generic_scores) if s == g)

print("\n" + "="*60)
print("📊 AUTOMATED LLM-AS-A-JUDGE RESULTS")
print("="*60 + "\n")

comparison_df = pd.DataFrame({
    "System": ["SAC-RAG", "Generic Claude"],
    "Average Score (/5)": [sac_avg, generic_avg],
    "Wins": [sac_wins, generic_wins],
    "Ties": [ties, ties]
})

print(comparison_df.to_string(index=False))
print(f"\nImprovement: {((sac_avg - generic_avg) / generic_avg * 100):+.2f}%")

# Export results
comparison_df.to_csv("automated_llm_judge_results.csv", index=False)

# Export detailed scores
detailed_df = pd.DataFrame({
    'Question_ID': [f"Q{i+1}" for i in range(len(df_manual))],
    'Question': df_manual['Question'],
    'SAC_RAG_Score': sac_scores,
    'Generic_Claude_Score': generic_scores,
    'Winner': ['SAC-RAG' if s > g else ('Generic Claude' if g > s else 'Tie') 
               for s, g in zip(sac_scores, generic_scores)]
})
detailed_df.to_csv("automated_llm_judge_detailed.csv", index=False)

print("\n✅ Results exported:")
print("   - automated_llm_judge_results.csv (summary)")
print("   - automated_llm_judge_detailed.csv (per-question scores)")

print("\n" + "="*60)
print("💡 COMPARISON: Manual vs Automated Evaluation")
print("="*60)
print("\nManual (Your Blind Evaluation):")
print("  SAC-RAG: 3.6/5")
print("  Generic Claude: 4.9/5")
print("  Winner: Generic Claude (6 wins)")
print(f"\nAutomated (LLM-as-a-Judge):")
print(f"  SAC-RAG: {sac_avg:.2f}/5")
print(f"  Generic Claude: {generic_avg:.2f}/5")
print(f"  Winner: {'SAC-RAG' if sac_wins > generic_wins else 'Generic Claude'} ({max(sac_wins, generic_wins)} wins)")

print("\n✅ Automated evaluation complete! 🎓")
