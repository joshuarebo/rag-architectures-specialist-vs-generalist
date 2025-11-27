"""
Final Experiment: RAG-Specific Metrics Evaluation
Tests SAC-RAG vs Generic Claude on:
1. Answer Relevance (AR): Does the answer address the user's question?
2. Context Relevance (CR): Are retrieved chunks relevant to the question?
3. Groundedness (G): Is the answer supported by retrieved text?

Note: Generic Claude has no retrieval context, so CR and G will be N/A
"""

import pandas as pd
import time
from botocore.exceptions import ClientError
import re

print("\n" + "="*70)
print("FINAL EXPERIMENT: RAG-SPECIFIC METRICS EVALUATION")
print("Testing Answer Relevance, Context Relevance, Groundedness")
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
        return min(max(score, 0.0), max_score)  # Clamp between 0 and max_score
    return 0.0

# ============================================================
# Metric 1: Answer Relevance (AR)
# ============================================================
def score_answer_relevance(question, answer, llm):
    """
    Does the answer actually address the user's question?
    Score: 0.0 (Completely irrelevant) to 1.0 (Perfectly relevant)
    """
    prompt = f"""You are evaluating whether an answer addresses the user's question.

**User Question:**
{question}

**Answer Provided:**
{answer}

**Task:** Rate how well this answer addresses the user's specific question.
- 1.0 = Perfectly addresses the question, provides exactly what was asked
- 0.75 = Mostly addresses the question, with minor omissions
- 0.5 = Partially addresses the question, but misses key aspects
- 0.25 = Barely addresses the question, mostly irrelevant
- 0.0 = Completely irrelevant, does not answer the question at all

**CRITICAL:** Respond with ONLY a decimal number between 0.0 and 1.0. No explanations."""

    response = invoke_with_retry(llm, prompt)
    return extract_score(response, max_score=1.0)

# ============================================================
# Metric 2: Context Relevance (CR)
# ============================================================
def score_context_relevance(question, contexts, llm):
    """
    Are the retrieved chunks relevant to the question?
    Score: 0.0 (Irrelevant noise) to 1.0 (Highly relevant)
    """
    if not contexts or len(contexts) == 0:
        return None  # N/A for systems without retrieval
    
    contexts_text = "\n\n---\n\n".join(contexts)
    
    prompt = f"""You are evaluating the relevance of retrieved legal text chunks to a question.

**User Question:**
{question}

**Retrieved Text Chunks:**
{contexts_text}

**Task:** Rate how relevant these retrieved chunks are to answering the question.
- 1.0 = All chunks are highly relevant and directly address the question
- 0.75 = Most chunks are relevant, some contain useful information
- 0.5 = Mixed relevance, some chunks are useful, others are noise
- 0.25 = Mostly irrelevant, only minor useful information
- 0.0 = Completely irrelevant noise, no useful information

**CRITICAL:** Respond with ONLY a decimal number between 0.0 and 1.0. No explanations."""

    response = invoke_with_retry(llm, prompt)
    return extract_score(response, max_score=1.0)

# ============================================================
# Metric 3: Groundedness (G)
# ============================================================
def score_groundedness(answer, contexts, llm):
    """
    Is the answer fully supported by the retrieved text?
    Score: 0.0 (Hallucination) to 1.0 (Fully grounded)
    """
    if not contexts or len(contexts) == 0:
        return None  # N/A for systems without retrieval
    
    contexts_text = "\n\n---\n\n".join(contexts)
    
    prompt = f"""You are evaluating whether an answer is grounded in the provided source text.

**Source Text (Retrieved Chunks):**
{contexts_text}

**Answer to Evaluate:**
{answer}

**Task:** Rate how well the answer is supported by the source text.
- 1.0 = Every claim in the answer is directly supported by the source text
- 0.75 = Most claims are supported, minor unsupported details
- 0.5 = Some claims are supported, but significant portions are not
- 0.25 = Few claims are supported, mostly unsupported or inferred
- 0.0 = Hallucination - claims facts not in the source text

**CRITICAL:** Respond with ONLY a decimal number between 0.0 and 1.0. No explanations."""

    response = invoke_with_retry(llm, prompt)
    return extract_score(response, max_score=1.0)

# ============================================================
# Load Data and Evaluate
# ============================================================

# Load results from SAC-RAG evaluation (has contexts)
sac_results = pd.read_csv('sac_rag_golden_detailed.csv')

# Load manual template (has Generic Claude answers)
manual_template = pd.read_excel('manual_evaluation_template.xlsx')

print("📊 Evaluating 10 Golden Questions on RAG-Specific Metrics")
print("="*70 + "\n")

results = []

for i in range(len(sac_results)):
    sac_row = sac_results.iloc[i]
    manual_row = manual_template.iloc[i]
    
    question = sac_row['question']
    sac_answer = sac_row['answer']
    sac_contexts = eval(sac_row['contexts'])  # Convert string representation to list
    generic_answer = manual_row['Generic_Claude_Answer']
    
    print(f"Q{i+1}/10: {question[:60]}...")
    
    # SAC-RAG Evaluation
    print("  [SAC-RAG]")
    print("    Scoring Answer Relevance...", end=" ")
    sac_ar = score_answer_relevance(question, sac_answer, llm_generate)
    print(f"{sac_ar:.2f}")
    time.sleep(2)
    
    print("    Scoring Context Relevance...", end=" ")
    sac_cr = score_context_relevance(question, sac_contexts, llm_generate)
    print(f"{sac_cr:.2f}")
    time.sleep(2)
    
    print("    Scoring Groundedness...", end=" ")
    sac_g = score_groundedness(sac_answer, sac_contexts, llm_generate)
    print(f"{sac_g:.2f}")
    time.sleep(2)
    
    # Generic Claude Evaluation
    print("  [Generic Claude]")
    print("    Scoring Answer Relevance...", end=" ")
    generic_ar = score_answer_relevance(question, generic_answer, llm_generate)
    print(f"{generic_ar:.2f}")
    print("    Context Relevance: N/A (no retrieval)")
    print("    Groundedness: N/A (no retrieval)")
    time.sleep(2)
    
    results.append({
        'Question_ID': f'Q{i+1}',
        'Question': question,
        'SAC_RAG_AR': sac_ar,
        'SAC_RAG_CR': sac_cr,
        'SAC_RAG_G': sac_g,
        'SAC_RAG_Avg': (sac_ar + sac_cr + sac_g) / 3,
        'Generic_AR': generic_ar,
        'Generic_CR': None,
        'Generic_G': None,
        'Generic_Avg': generic_ar  # Only AR is applicable
    })
    
    print()

# Convert to DataFrame
df_results = pd.DataFrame(results)

# Calculate averages
sac_ar_avg = df_results['SAC_RAG_AR'].mean()
sac_cr_avg = df_results['SAC_RAG_CR'].mean()
sac_g_avg = df_results['SAC_RAG_G'].mean()
sac_overall = (sac_ar_avg + sac_cr_avg + sac_g_avg) / 3

generic_ar_avg = df_results['Generic_AR'].mean()

print("\n" + "="*70)
print("📊 RAG-SPECIFIC METRICS RESULTS")
print("="*70 + "\n")

print("SAC-RAG (Claude 4.5 + Domain Retrieval):")
print(f"  Answer Relevance:   {sac_ar_avg:.3f}/1.0")
print(f"  Context Relevance:  {sac_cr_avg:.3f}/1.0")
print(f"  Groundedness:       {sac_g_avg:.3f}/1.0")
print(f"  Overall (Avg):      {sac_overall:.3f}/1.0")

print(f"\nGeneric Claude (Claude 4.0, No Retrieval):")
print(f"  Answer Relevance:   {generic_ar_avg:.3f}/1.0")
print(f"  Context Relevance:  N/A (no retrieval)")
print(f"  Groundedness:       N/A (no retrieval)")

print("\n" + "="*70)
print("🔬 KEY INSIGHTS")
print("="*70)

print(f"\n1. Answer Relevance Comparison:")
print(f"   SAC-RAG: {sac_ar_avg:.3f} vs Generic Claude: {generic_ar_avg:.3f}")
if sac_ar_avg > generic_ar_avg:
    print(f"   Winner: SAC-RAG (+{((sac_ar_avg - generic_ar_avg)/generic_ar_avg*100):.1f}%)")
else:
    print(f"   Winner: Generic Claude (+{((generic_ar_avg - sac_ar_avg)/sac_ar_avg*100):.1f}%)")

print(f"\n2. Retrieval Quality (SAC-RAG only):")
print(f"   Context Relevance: {sac_cr_avg:.3f}/1.0")
if sac_cr_avg >= 0.75:
    print("   ✅ Excellent - retrieves highly relevant legal texts")
elif sac_cr_avg >= 0.5:
    print("   ⚠️ Good - retrieves mostly relevant texts with some noise")
else:
    print("   ❌ Poor - retrieval needs improvement")

print(f"\n3. Hallucination Risk (SAC-RAG only):")
print(f"   Groundedness: {sac_g_avg:.3f}/1.0")
if sac_g_avg >= 0.75:
    print("   ✅ Low Risk - answers are well-grounded in source texts")
elif sac_g_avg >= 0.5:
    print("   ⚠️ Moderate Risk - some unsupported claims")
else:
    print("   ❌ High Risk - significant hallucinations detected")

print(f"\n4. SAC-RAG Advantage:")
print(f"   Summary Augmented Chunking provides:")
print(f"   - Context precision (CR): {sac_cr_avg:.3f}")
print(f"   - Factual grounding (G): {sac_g_avg:.3f}")
print(f"   - Combined RAG quality: {((sac_cr_avg + sac_g_avg)/2):.3f}")

# Export results
df_results.to_csv('rag_metrics_evaluation.csv', index=False)

print("\n✅ Results exported to: rag_metrics_evaluation.csv")
print("\n" + "="*70)
print("✅ Final experiment complete! Ready for thesis report generation.")
print("="*70 + "\n")
