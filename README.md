# RAG Architectures: Specialist vs Generalist
## Comparative Study of Domain-Adapted RAG for Kenyan Legal Practice

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange.svg)](https://aws.amazon.com/bedrock/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

This repository contains the complete experimental codebase for a rigorous comparative study of **Retrieval-Augmented Generation (RAG) systems** in the Kenyan legal domain. The research investigates whether domain-adapted RAG systems provide meaningful performance advantages over general-purpose foundation models in data-scarce, specialized contexts.

### Core Research Contribution

**Critical Finding:** RAG system performance is **model-dependent**. Summary-Augmented Chunking (SAC-RAG) outperformed Base RAG by +3.04% with Claude 3.5 Sonnet but underperformed by -10.89% with Claude 4.5 Sonnet, demonstrating that retrieval optimization strategies must **co-evolve with model capabilities**.

---

## Key Findings

### 1. Model Quality Dominates (10x Impact)
- **Model upgrade:** SAC-RAG improved +30.6% (Claude 3.5 → 4.5)
- **Retrieval optimization:** SAC-RAG improved +3.04% over Base RAG (Claude 3.5)
- **Ratio:** 30.6% ÷ 3.04% ≈ **10x**

### 2. Model-Dependent Performance Reversal
| Model | Winner | Performance Gap |
|-------|--------|----------------|
| Claude 3.5 Sonnet | SAC-RAG | +3.04% |
| Claude 4.5 Sonnet | Base RAG | +10.89% |

**Implication:** Chunking strategies are not universally optimal; they must adapt to model generation.

### 3. Near-Parity with Equivalent Models
When both systems used Claude Sonnet 4.5:
- **SAC-RAG:** 9.40/10
- **Generic Claude:** 9.60/10
- **Gap:** Only 2.1%

**Implication:** Retrieval becomes competitive when model quality is matched.

---

## System Architecture

### Three Systems Evaluated

#### 1. Base RAG
```
Document Parsing → Chunking → Vector Embedding → Retrieval → LLM Generation
```
- **Chunking:** RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
- **Embeddings:** AWS Titan Text Embeddings v2 (1024 dimensions)
- **LLM:** Claude 3.5/4.5 Sonnet (AWS Bedrock)

#### 2. SAC-RAG (Summary-Augmented Chunking)
```
Document Parsing → Summarization → Summary-Prepended Chunking → 
Vector Embedding → Retrieval → LLM Generation
```
- **Innovation:** Each chunk prepended with document summary for context preservation
- **Performance:** Model-dependent (helps Claude 3.5, hinders Claude 4.5)

#### 3. Generic Claude
```
No Retrieval → Direct LLM Inference (Claude 4.0/4.5 via claude.ai)
```
- **Advantage:** Superior reasoning, broad legal knowledge, web search capability
- **Limitation:** No access to proprietary/recent Kenyan legal documents

---

## Experimental Setup

### Dataset
- **Corpus:** 11 Kenyan statutes + 48 court judgments (59 PDFs total)
- **Key Documents:** Constitution of Kenya 2010, Law of Succession Act, Land Registration Act, Finance Act 2023, Supreme Court precedents
- **Evaluation Set:** 10 expert-curated Golden Questions spanning constitutional law, succession, land law, taxation, employment

### Evaluation Methodology

1. **Manual Blind Evaluation (1-5 Rubric)** - Human expert scoring with randomized A/B labeling
2. **Automated LLM-as-a-Judge (0-10 Scale)** - Claude 3.5/4.5 as evaluator
3. **Ablation Study** - Isolated model upgrade effect (Claude 3.5 → 4.5)

---

## Results

### Primary Results

| Comparison | Baseline → Modified | Impact | Interpretation |
|------------|---------------------|--------|----------------|
| **Model Upgrade** | SAC-RAG (3.5 → 4.5) | **+30.6%** | Dominant factor |
| **Retrieval (Claude 4.5)** | Base RAG → SAC-RAG | **-10.89%** | Advanced models prefer focused chunks |
| **Retrieval (Claude 3.5)** | Base RAG → SAC-RAG | **+3.04%** | Older models benefit from summaries |
| **Generic vs SAC-RAG (4.5)** | Generic vs SAC-RAG | **+2.1%** | Near-parity with strong models |

###  Cost-Benefit Analysis

| System | Setup Cost | Per-Query | Latency | Performance | Best Use Case |
|--------|------------|-----------|---------|-------------|---------------|
| Generic Claude | $0 | $0 | ~3s | 9.60/10 | General legal research |
| SAC-RAG (4.5) | $5 | $0.012 | ~5s | 9.40/10 | Proprietary documents |
| Base RAG (4.5) | $5 | $0.012 | ~5s | 8.57/10 | Claude 4.5+ deployments |

**Recommended Strategy:** 80% Generic Claude, 15% Domain RAG, 5% Manual Research

---

## Repository Structure

```
├── kenyan_legal_rag_enhanced.ipynb    # Main experimental notebook
├── legal_pdfs/                         # Kenyan legal corpus (59 PDFs)
├── results_claude_3.5/                 # Claude 3.5 experiment results
│   ├── base_rag_golden_detailed_CLAUDE35.csv
│   ├── sac_rag_golden_detailed_CLAUDE35.csv
│   └── manual_evaluation_template_CLAUDE35.xlsx
├── base_rag_golden_detailed.csv       # Claude 4.5 Base RAG results
├── sac_rag_golden_detailed.csv        # Claude 4.5 SAC-RAG results
├── manual_evaluation_template.xlsx    # Claude 4.5 evaluation template
├── blind_evaluation_scoring_sheet.xlsx # Manual blind scoring
├── thesis_visualizations/             # Publication-quality charts
│   ├── 01_base_vs_sac_comparison.png
│   ├── 02_ablation_study.png
│   └── [6 more visualizations]
├── response_comparison_tables.md      # Qualitative response analysis
├── research_questions_answered.md     # Complete RQ analysis
└── README.md                          # This file
```

---

## Installation & Usage

### Prerequisites
- Python 3.8+
- AWS Account with Bedrock access
- GROBID Server (optional, for enhanced parsing)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/joshuarebo/rag-architectures-specialist-vs-generalist.git
cd rag-architectures-specialist-vs-generalist
```

2. **Install dependencies**
```bash
pip install pandas boto3 langchain-aws chromadb jupyter matplotlib seaborn
```

3. **Configure AWS credentials**
```bash
export AWS_ACCESS_KEY_ID=your_key_here
export AWS_SECRET_ACCESS_KEY=your_secret_here
export AWS_DEFAULT_REGION=us-east-1
```

4. **Run the main notebook**
```bash
jupyter notebook kenyan_legal_rag_enhanced.ipynb
```

### Generate Visualizations
```bash
python generate_thesis_visualizations.py
```
Output: 8 publication-quality charts in `thesis_visualizations/`

---

## Research Questions Answered

1. **Do domain-adapted RAG systems outperform general RAG systems?**
   - **Model-dependent** (SAC-RAG wins with Claude 3.5, loses with Claude 4.5)

2. **Does marginal accuracy improvement reduce verification time?**
   - **Threshold effects** observed (small gains may not justify costs)

3. **Do RAG systems in data-scarce regions perform well?**
   - **Yes, with workarounds** (achieved 9.40/10 despite AWS throttling)

4. **Is the retrieval database the primary performance driver?**
   - **No** — Model quality had **10x larger impact**

---

## Citation

If you use this work in your research, please cite:

```bibtex
@misc{rebo2025rag,
  author = {Rebo, Joshua},
  title = {RAG Architectures: Specialist vs Generalist - Comparative Study of Domain-Adapted RAG for Kenyan Legal Practice},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/joshuarebo/rag-architectures-specialist-vs-generalist}
}
```

---

## Key Takeaways

1. **Model quality currently dominates retrieval optimization** (10x impact)
2. **Retrieval strategies must co-evolve with model capabilities** (SAC-RAG is model-dependent)
3. **RAG becomes competitive with strong foundation models** (2.1% gap with Claude 4.5)
4. **Infrastructure workarounds enable RAG in developing regions**
5. **Both retrieval and model quality matter** (context-dependent, not either-or)

---

## Contact & Contributions

Contributions, issues, and feature requests are welcome!  
For questions or collaborations, please open an issue on GitHub.

---

## License

This project is licensed under the MIT License.

---

## Author

**Joshua Rebo**

*Research Thesis: Comparative Analysis of Retrieval-Augmented Generation Systems for Kenyan Legal Practice*

Year: 2025

---

**⭐ If you found this research useful, please consider starring the repository!**
