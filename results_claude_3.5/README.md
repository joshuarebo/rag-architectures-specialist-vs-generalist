# Claude 3.5 Sonnet v2 Experiment Results

## Experiment Details
- **Model Used**: `anthropic.claude-3-5-sonnet-20241022-v2:0`
- **Date**: November 2024
- **Dataset**: 10 Golden Questions + 40 Synthetic Questions

## Files in This Folder

### Base RAG vs SAC-RAG Comparison
- `llm_judge_golden_comparison_CLAUDE35.csv` - Summary comparison (Base RAG vs SAC-RAG)
- `base_rag_golden_detailed_CLAUDE35.csv` - Per-question Base RAG scores
- `sac_rag_golden_detailed_CLAUDE35.csv` - Per-question SAC-RAG scores
- `thesis_results_final.csv` - Complete 50-question dataset

### SAC-RAG vs Generic Claude Comparison
- `manual_evaluation_template_CLAUDE35.xlsx` - Template with SAC-RAG & Generic Claude answers
- `blind_evaluation_scoring_sheet_CLAUDE35.xlsx` - Completed blind evaluation scores
- `blind_evaluation_answer_key.xlsx` - Reveals which answer was which system
- `blind_evaluation_results.csv` - Manual evaluation summary

### Automated Evaluation
- `automated_llm_judge_results_CLAUDE35.csv` - Automated LLM-as-a-Judge summary
- `automated_llm_judge_detailed_CLAUDE35.csv` - Per-question automated scores

## Key Findings (Claude 3.5)

### Base RAG vs SAC-RAG (50 Questions)
- SAC-RAG Overall: 9.03/10
- Base RAG Overall: 8.77/10
- **Winner: SAC-RAG (+3.04%)**
- SAC-RAG Completeness: +10.53%

### SAC-RAG vs Generic Claude (10 Golden Questions)

**Manual Blind Evaluation:**
- SAC-RAG (Claude 3.5): 3.6/5
- Generic Claude (Claude 4.0): 4.9/5
- **Winner: Generic Claude (+36%)**

**Automated LLM-as-a-Judge:**
- SAC-RAG: 4.2/5
- Generic Claude: 4.3/5
- **Winner: Generic Claude (+2.3%)**

## Conclusion
Despite domain-specific retrieval, SAC-RAG with Claude 3.5 was outperformed by Generic Claude 4.0, demonstrating that model advancement currently outweighs domain adaptation benefits.

---

**Next Experiment**: Claude Sonnet 4.5 (results in separate folder)
