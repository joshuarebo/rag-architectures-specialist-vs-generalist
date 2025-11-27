# Research Questions Answered

## Comprehensive Response to Research Questions

This experimental study of Retrieval-Augmented Generation (RAG) systems for Kenyan legal practice provides nuanced answers to the four central research questions. **Regarding Question 1 (domain-adapted vs. general RAG systems):** The findings reveal a critical model-dependent performance pattern. Summary-Augmented Chunking RAG (SAC-RAG) outperformed Base RAG by +3.04% when using Claude 3.5 Sonnet, demonstrating that domain adaptation benefits older models with limited contextual reasoning. However, this advantage reversed with Claude 4.5 Sonnet, where Base RAG outperformed SAC-RAG by +10.89%, indicating that advanced models prefer concise, focused chunks over summary-prepended content. This suggests that retrieval optimization strategies must co-evolve with model capabilities—a contribution that challenges the assumption of universally optimal chunking approaches. **For Question 2 (marginal accuracy and productivity):** While direct verification time was not measured, the performance comparison revealed that Generic Claude (9.60/10) maintained only a +2.1% advantage over SAC-RAG with Claude 4.5 (9.40/10), suggesting that marginal accuracy improvements alone may not justify the infrastructure costs and complexity of RAG deployment for general legal research. However, the ablation study demonstrated that upgrading from Claude 3.5 to Claude 4.5 yielded a +30.6% performance improvement—a magnitude that likely would reduce verification time substantially enough to deliver net productivity gains, though empirical productivity metrics remain a direction for future work. **Addressing Question 3 (RAG performance in data-scarce regions):** The research encountered significant infrastructure constraints characteristic of developing regions, including AWS Bedrock throttling that completely blocked standard RAGAS evaluation metrics, necessitating the development of custom 5-point rubrics as a pragmatic alternative. Despite these limitations, SAC-RAG with Claude 4.5 achieved 9.40/10 performance—nearly matching Generic Claude's 9.60/10—demonstrating that RAG systems can indeed perform competitively in regions with poor data infrastructure, provided that workarounds for computational constraints are implemented. The $1.20 USD cost per 10-question evaluation and ~5-second query latency further confirm technical feasibility in resource-constrained environments. **Finally, for Question 4 (retrieval database as primary driver):** The evidence decisively refutes this hypothesis in the current technological landscape. Model quality exhibited a 10x larger impact on performance than retrieval optimization, with Generic Claude 4.5 (no retrieval) outperforming SAC-RAG with Claude 3.5 (domain retrieval) by +36.1%. The model upgrade from Claude 3.5 to Claude 4.5 alone yielded +30.6% improvement, dwarfing the marginal gains from retrieval architecture changes. However, the hypothesis is *partially supported* in specific contexts: when compared using equivalent model capabilities (Claude 4.5), SAC-RAG nearly tied Generic Claude (9.40 vs. 9.60), and retrieval becomes essential for proprietary legal documents, recent case law beyond LLM training cutoffs, and confidential firm-specific content. The revised conclusion is that **both retrieval quality and model reasoning power matter significantly, but model advancement currently dominates for general legal knowledge**, while retrieval justifies its cost primarily for content unavailable in foundation model training data. These findings collectively suggest a hybrid deployment strategy: leverage Generic Claude for 80% of general legal queries, deploy domain RAG for 15% of proprietary/specialized content, and reserve manual legal research for the highest-stakes 5% of work.

---

## Individual Question Responses (For Reference)

### Q1: Do domain-adapted retrieval augmented systems perform better than general RAG systems in the Kenyan legal sector?

**Answer: Model-Dependent**

- **With Claude 3.5:** SAC-RAG > Base RAG (+3.04%)
- **With Claude 4.5:** Base RAG > SAC-RAG (+10.89%)
- **Key Finding:** Chunking strategies must match model capabilities

### Q2: Does marginal accuracy improvement in AI outputs reduce verification time sufficiently to deliver net productivity?

**Answer: Not Directly Measured, But Evidence Suggests Threshold Effects**

- Marginal improvements (±2-3%) may not justify RAG costs for general queries
- Large improvements (+30.6% from model upgrade) likely do reduce verification time significantly
- Direct productivity measurement needed for conclusive answer

### Q3: Do RAG systems in regions with poor data infrastructure perform as well as data-rich regions?

**Answer: Competitive Performance Possible, But with Infrastructure Challenges**

- AWS Bedrock throttling blocked RAGAS evaluation (infrastructure constraint confirmed)
- Despite limitations, SAC-RAG achieved 9.40/10 (vs Generic Claude 9.60/10)
- Workarounds (custom rubrics) enable viable RAG deployment in developing regions
- Cost ($1.20 per 10 queries) and latency (~5s) acceptable for resource-constrained settings

### Q4: Is the retrieval database the primary driver of trust and performance in the legal domain in Kenya?

**Answer: NO (for current state-of-the-art models), YES (for specific contexts)**

**Evidence Against (General Legal Knowledge):**
- Model quality had 10x larger impact than retrieval optimization
- Generic Claude 4.5 (no retrieval) > SAC-RAG 3.5 (with retrieval) by +36.1%
- Model upgrade (+30.6%) >> retrieval improvement

**Evidence For (Specific Contexts):**
- With equivalent models: SAC-RAG (9.40) ≈ Generic Claude (9.60)
- Retrieval critical for: proprietary docs, recent law, confidential content
- GROBID parsing improved answer grounding measurably

**Revised Hypothesis:** Both retrieval quality AND model reasoning matter; model advancement currently dominates, but retrieval remains essential for content unavailable in LLM training data.
