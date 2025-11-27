"""
Final Experiment: RAG-Specific Metrics Evaluation (FIXED)
Tests SAC-RAG vs Generic Claude on:
1. Answer Relevance (AR): Does the answer address the user's question?
2. Context Quality Assessment: Based on generated answers
3. Comparative Analysis

Since contexts weren't saved in CSV, we'll evaluate based on the answers themselves.
"""

import pandas as pd
import time
from botocore.exceptions import ClientError
import re

print("\n" + "="*70)
print("FINAL EXPERIMENT: ANSWER QUALITY METRICS EVALUATION")
print("Testing Answer Relevance, Specificity, and Legal Grounding")
print("="*70 + "\n")

# ============================================================
# Helper: Retry Logic
# ============================================================
def invoke_with_retry(llm, prompt, max_retries=5):
    """Invoke LLM with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            response = llm.invoke(prompt)
            if hasattr(response, 'content'):
                return response.content
            return str(response)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ThrottlingException':
                if attempt < max_retries - 1:
                    wait_time = 5 * (2 ** attempt)
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

def extract_score(response_text, max_score=1.0):
    """Extract numeric score from LLM response"""
    if not response_text:
        return 0.0
    
    # Try to find a decimal number between 0 and max_score
    match = re.search(r'(\d+\.?\d*)', response_text.strip())
    if match:
        score = float(match.group(1))
        return min(max(score, 0.0), max_score)
    return 0.0

# ============================================================
# Metric 1: Answer Relevance (AR)
# ============================================================
def score_answer_relevance(question, answer, llm):
    """
    Does the answer actually address the user's question?
    Score: 0.0 to 1.0
    """
    prompt = f"""You are evaluating whether an answer addresses the user's question.

**User Question:**
{question}

**Answer Provided:**
{answer}

**Task:** Rate how well this answer addresses the user's specific question.
- 1.0 = Perfectly addresses the question
- 0.75 = Mostly addresses the question
- 0.5 = Partially addresses the question
- 0.25 = Barely addresses the question
- 0.0 = Completely irrelevant

**CRITICAL:** Respond with ONLY a decimal number between 0.0 and 1.0. No explanations."""

    response = invoke_with_retry(llm, prompt)
    return extract_score(response, max_score=1.0)

# ============================================================
# Metric 2: Specificity (Legal Citations)
# ============================================================
def score_specificity(answer, llm):
    """
    Does the answer cite specific Kenyan statutes/cases?
    Score: 0.0 to 1.0
    """
    prompt = f"""You are evaluating the specificity of a Kenyan legal answer.

**Answer:**
{answer}

**Task:** Rate how specific this answer is in citing Kenyan law.
- 1.0 = Cites specific sections AND case names with citations (e.g., "Section 40(3)" AND "Dina Management v AG [2017]")
- 0.75 = Cites specific sections OR case names (but not both)
- 0.5 = References Kenyan law generally without specific citations
- 0.25 = Vague legal references
- 0.0 = No specific legal references

**CRITICAL:** Respond with ONLY a decimal number between 0.0 and 1.0. No explanations."""

    response = invoke_with_retry(llm, prompt)
    return extract_score(response, max_score=1.0)

# ============================================================
# Metric 3: Groundedness Assessment
# ============================================================
def score_groundedness_proxy(answer, llm):
    """
    Does the answer appear to be grounded in legal sources?
    (Proxy metric since we don't have contexts)
    Score: 0.0 to 1.0
    """
    prompt = f"""You are evaluating whether a legal answer appears well-grounded.

**Answer:**
{answer}

**Task:** Rate how well-grounded this answer appears (does it make specific, verifiable claims?)
- 1.0 = Makes specific, verifiable legal claims with precise citations
- 0.75 = Makes mostly specific claims
- 0.5 = Mix of specific and vague claims
- 0.25 = Mostly vague or general statements
- 0.0 = Appears to contain unsupported or fabricated claims

**CRITICAL:** Respond with ONLY a decimal number between 0.0 and 1.0. No explanations."""

    response = invoke_with_retry(llm, prompt)
    return extract_score(response, max_score=1.0)

# ============================================================
# Load Data and Evaluate
# ============================================================

# Load SAC-RAG results
sac_results = pd.read_csv('sac_rag_golden_detailed.csv')

# Load manual template (has Generic Claude answers)
manual_template = pd.read_excel('manual_evaluation_template.xlsx')

print("📊 Evaluating 10 Golden Questions on Answer Quality Metrics")
print("="*70 + "\n")

results = []

for i in range(min(len(sac_results), len(manual_template))):
    sac_row = sac_results.iloc[i]
    manual_row = manual_template.iloc[i]
    
    question = sac_row['question']
    sac_answer = sac_row['answer']
    generic_answer = manual_row['Generic_Claude_Answer']
    
    print(f"Q{i+1}/10: {question[:60]}...")
    
    # SAC-RAG Evaluation
    print("  [SAC-RAG (Claude 4.5)]")
    print("    Scoring Answer Relevance...", end=" ")
    sac_ar = score_answer_relevance(question, sac_answer, llm_generate)
    print(f"{sac_ar:.2f}")
    time.sleep(2)
    
    print("    Scoring Specificity...", end=" ")
    sac_spec = score_specificity(sac_answer, llm_generate)
    print(f"{sac_spec:.2f}")
    time.sleep(2)
    
    print("    Scoring Groundedness...", end=" ")
    sac_ground = score_groundedness_proxy(sac_answer, llm_generate)
    print(f"{sac_ground:.2f}")
    time.sleep(2)
    
    # Generic Claude Evaluation
    print("  [Generic Claude]")
    print("    Scoring Answer Relevance...", end=" ")
    generic_ar = score_answer_relevance(question, generic_answer, llm_generate)
    print(f"{generic_ar:.2f}")
    time.sleep(2)
    
    print("    Scoring Specificity...", end=" ")
    generic_spec = score_specificity(generic_answer, llm_generate)
    print(f"{generic_spec:.2f}")
    time.sleep(2)
    
    print("    Scoring Groundedness...", end=" ")
    generic_ground = score_groundedness_proxy(generic_answer, llm_generate)
    print(f"{generic_ground:.2f}")
    time.sleep(2)
    
    results.append({
        'Question_ID': f'Q{i+1}',
        'Question': question[:100],
        'SAC_RAG_AR': sac_ar,
        'SAC_RAG_Specificity': sac_spec,
        'SAC_RAG_Groundedness': sac_ground,
        'SAC_RAG_Avg': (sac_ar + sac_spec + sac_ground) / 3,
        'Generic_AR': generic_ar,
        'Generic_Specificity': generic_spec,
        'Generic_Groundedness': generic_ground,
        'Generic_Avg': (generic_ar + generic_spec + generic_ground) / 3
    })
    
    print()

# Convert to DataFrame
df_results = pd.DataFrame(results)

# Calculate averages
sac_ar_avg = df_results['SAC_RAG_AR'].mean()
sac_spec_avg = df_results['SAC_RAG_Specificity'].mean()
sac_ground_avg = df_results['SAC_RAG_Groundedness'].mean()
sac_overall = (sac_ar_avg + sac_spec_avg + sac_ground_avg) / 3

generic_ar_avg = df_results['Generic_AR'].mean()
generic_spec_avg = df_results['Generic_Specificity'].mean()
generic_ground_avg = df_results['Generic_Groundedness'].mean()
generic_overall = (generic_ar_avg + generic_spec_avg + generic_ground_avg) / 3

print("\n" + "="*70)
print("📊 ANSWER QUALITY METRICS RESULTS")
print("="*70 + "\n")

comparison_table = pd.DataFrame({
    'Metric': ['Answer Relevance', 'Specificity (Citations)', 'Groundedness', 'Overall Average'],
    'SAC-RAG (Claude 4.5)': [f"{sac_ar_avg:.3f}", f"{sac_spec_avg:.3f}", f"{sac_ground_avg:.3f}", f"{sac_overall:.3f}"],
    'Generic Claude': [f"{generic_ar_avg:.3f}", f"{generic_spec_avg:.3f}", f"{generic_ground_avg:.3f}", f"{generic_overall:.3f}"],
    'Difference': [
        f"{((sac_ar_avg - generic_ar_avg)*100):+.1f}%",
        f"{((sac_spec_avg - generic_spec_avg)*100):+.1f}%",
        f"{((sac_ground_avg - generic_ground_avg)*100):+.1f}%",
        f"{((sac_overall - generic_overall)*100):+.1f}%"
    ]
})

print(comparison_table.to_string(index=False))

print("\n" + "="*70)
print("🔬 KEY INSIGHTS")
print("="*70)

print(f"\n1. Answer Relevance:")
if sac_ar_avg > generic_ar_avg:
    print(f"   ✅ SAC-RAG wins: {sac_ar_avg:.3f} vs {generic_ar_avg:.3f} (+{((sac_ar_avg-generic_ar_avg)/generic_ar_avg*100):.1f}%)")
else:
    print(f"   ⚠️ Generic Claude wins: {generic_ar_avg:.3f} vs {sac_ar_avg:.3f} (+{((generic_ar_avg-sac_ar_avg)/sac_ar_avg*100):.1f}%)")

print(f"\n2. Specificity (Legal Citations):")
if sac_spec_avg > generic_spec_avg:
    print(f"   ✅ SAC-RAG wins: {sac_spec_avg:.3f} vs {generic_spec_avg:.3f} (+{((sac_spec_avg-generic_spec_avg)/generic_spec_avg*100):.1f}%)")
    print(f"   Interpretation: SAC-RAG provides more specific legal citations")
else:
    print(f"   ⚠️ Generic Claude wins: {generic_spec_avg:.3f} vs {sac_spec_avg:.3f} (+{((generic_spec_avg-sac_spec_avg)/sac_spec_avg*100):.1f}%)")

print(f"\n3. Groundedness:")
if sac_ground_avg > generic_ground_avg:
    print(f"   ✅ SAC-RAG wins: {sac_ground_avg:.3f} vs {generic_ground_avg:.3f} (+{((sac_ground_avg-generic_ground_avg)/generic_ground_avg*100):.1f}%)")
    print(f"   Interpretation: SAC-RAG answers appear more grounded in legal sources")
else:
    print(f"   ⚠️ Generic Claude wins: {generic_ground_avg:.3f} vs {sac_ground_avg:.3f} (+{((generic_ground_avg-sac_ground_avg)/sac_ground_avg*100):.1f}%)")

print(f"\n4. Overall Quality:")
if sac_overall > generic_overall:
    print(f"   ✅ SAC-RAG wins overall: {sac_overall:.3f} vs {generic_overall:.3f}")
    print(f"   Improvement: +{((sac_overall-generic_overall)/generic_overall*100):.1f}%")
else:
    print(f"   ⚠️ Generic Claude wins overall: {generic_overall:.3f} vs {sac_overall:.3f}")
    print(f"   Gap: +{((generic_overall-sac_overall)/sac_overall*100):.1f}%")

# Export results
df_results.to_csv('final_quality_metrics_evaluation.csv', index=False)
comparison_table.to_csv('final_quality_metrics_summary.csv', index=False)

print("\n✅ Results exported:")
print("   - final_quality_metrics_evaluation.csv (detailed)")
print("   - final_quality_metrics_summary.csv (summary table)")

print("\n" + "="*70)
print("✅ Final experiment complete! Ready for thesis report generation.")
print("="*70 + "\n")
