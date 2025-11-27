# Response Comparison Tables for Thesis Appendix

These tables demonstrate the quality differences between SAC-RAG and Generic Claude responses across different model generations.

---

## Table 1: SAC-RAG (Claude 3.5) vs Generic Claude (Claude 4.5)

This comparison shows how the domain-adapted RAG system with an older model performed against the more advanced generic system.

### Example 1: Constitutional Law Question

**Question:** What are the key provisions of Article 40 of the Constitution of Kenya 2010 regarding property rights?

| System | Response (Truncated) | Observation |
|--------|---------------------|-------------|
| **SAC-RAG (Claude 3.5)** | Article 40 of the Constitution provides that every person has the right to acquire and own property of any description in any part of Kenya. The article outlines several key provisions including the right to own property individually or in association with others... | Domain-grounded but older model shows verbosity, less precise structuring |
| **Generic Claude (4.5)** | Article 40 establishes property rights with three core provisions: (1) Right to acquisition and ownership (2) No arbitrary deprivation without compensation (3) State obligation to support access. The article balances individual rights with public interest... | Superior reasoning and concise structure despite no retrieval |

**Performance Gap:** Generic Claude scored 4.90/5, SAC-RAG scored 3.60/5 (+36.1% advantage)

---

### Example 2: Succession Law Question

**Question:** Under the Law of Succession Act, what happens when a person dies intestate in Kenya?

| System | Response (Trust) | Observation |
|--------|------------------|-------------|
| **SAC-RAG (Claude 3.5)** | When a person dies intestate in Kenya under the Law of Succession Act Cap 160, the estate is distributed according to specific statutory provisions. The Act provides for distribution among dependents including spouse, children, and in some cases extended family members. The distribution follows a hierarchy... | Cites relevant statute but lacks specific section references |
| **Generic Claude (4.5)** | Section 29 of the Law of Succession Act (Cap 160) governs intestate succession. Distribution hierarchy: (1) Spouse and children take precedence (2) Parents if no children (3) Siblings if no parents. Net intestate estate divided per statutory formula... | Specific section citation (Section 29), clear hierarchy despite no document access |

**Performance Gap:** Generic Claude's superior reasoning compensated for lack of retrieval

---

### Example 3: Tax Law Question

**Question:** What were the key tax changes introduced in Kenya's Finance Act 2023?

| System | Response (Truncated) | Observation |
|--------|---------------------|-------------|
| **SAC-RAG (Claude 3.5)** | The Finance Act 2023 introduced several significant tax changes affecting individuals and businesses in Kenya. These included adjustments to income tax rates, modifications to VAT provisions, and new compliance requirements for digital services... | Retrieved from corpus but lacked immediate analytical clarity |
| **Generic Claude (4.5)** | Key Finance Act 2023 changes include: (1) Housing levy introduction at 1.5% (2) VAT rate adjustments (3) Digital services tax expansion (4) PAYE modifications. These changes aimed to increase revenue collection and formalize the digital economy... | Strong general knowledge with current information, well-organized |

**Performance Gap:** Model quality dominated despite SAC-RAG having document access

---

## Table 2: SAC-RAG (Claude 4.5) vs Generic Claude (Claude 4.5)

This comparison shows near-parity when both systems use equivalent state-of-the-art models.

### Example 1: Constitutional Rights

**Question:** Does Article 40(3) of the Constitution protect a title deed obtained fraudulently?

| System | Response (Truncated) | Observation |
|--------|---------------------|-------------|
| **SAC-RAG (Claude 4.5)** | Article 40(3) states that property shall not be taken without compensation, but this protection does not extend to fraudulently obtained titles. The Constitution's integrity principles (Article 10) override claims based on fraud. Case law supports voiding fraudulent titles... | ✅ Cites specific article, references constitutional principles, mentions case law precedent |
| **Generic Claude (4.5)** | While Article 40 protects property rights, fraudulent acquisition vitiates legal title. Kenyan courts consistently hold that fraud nullifies protection. The principle "fraud unravels all" applies - documented titles obtained through misrepresentation lack constitutional safeguarding... | ✅ Strong legal reasoning, correct principle, lacks specific article subsection |

**Scores:** SAC-RAG (4.70/5), Generic Claude (4.80/5) - **Only 2.1% gap**

---

### Example 2: Land Law

**Question:** What is the process for registering community land under the Community Land Act?

| System | Response (Truncated) | Observation |
|--------|---------------------|-------------|
| **SAC-RAG (Claude 4.5)** | The Community Land Act provides for registration through several stages: (1) Community identification and verification (2) Land mapping and demarcation (3) Board of Trustees establishment (4) Formal registration with National Land Commission. Section 8 outlines requirements... | ✅ Step-by-step process, cites Section 8, references specific institutions |
| **Generic Claude (4.5)** | Community land registration follows structured process: (1) Community self-organization (2) Adjudication proceedings (3) Trustee appointment (4) Title issuance. Process ensures collective rights protection while maintaining governance transparency per statutory framework... | ✅ Accurate process, clear structure, general statutory reference |

**Scores:** SAC-RAG (4.80/5), Generic Claude (4.70/5) - **SAC-RAG wins this question**

---

### Example 3: Employment Law

**Question:** What are the key protections for employees under Kenyan labor law regarding unfair dismissal?

| System | Response (Truncated) | Observation |
|--------|---------------------|-------------|
| **SAC-RAG (Claude 4.5)** | Kenyan employment law provides robust unfair dismissal protections through the Employment Act 2007. Employees must receive fair hearing, proper notice per Section 45, and valid dismissal grounds. Remedies include reinstatement, compensation (6-12 months' pay), and relief from ELRC tribunals... | ✅ Cites Employment Act 2007, specific section, accurate remedies |
| **Generic Claude (4.5)** | Employment Act 2007 mandates procedural fair hearing before dismissal. Grounds must be substantiated (misconduct, capacity, operational). Remedies: reinstatement or compensation (typically 6-12 months). ELRC provides affordable dispute resolution maintaining labor standards... | ✅ Accurate statute, correct procedure, appropriate remedies |

**Scores:** Both scored 4.7/5 - **Near-perfect parity**

---

## Key Observations from Response Comparisons:

### Table 1 (Claude 3.5 vs 4.5):
1. **Model quality dominated** - Generic Claude's superior reasoning outweighed SAC-RAG's document access
2. **Older SAC-RAG was verbose** - Claude 3.5 generated longer, less focused responses
3. **Generic Claude's knowledge was current** - Had 2023 information despite no retrieval

### Table 2 (Both Claude 4.5):
1. **Near-parity achieved** - 2.1% gap shows retrieval becomes competitive with strong models
2. **SAC-RAG provided specificity** - Cited exact sections and provisions
3. **Generic Claude demonstrated breadth** - Strong general legal knowledge
4. **Trade-off emerged** - SAC-RAG won on statutory detail, Generic Claude on reasoning clarity

### Thesis Implication:
These examples demonstrate that **both model quality and retrieval matter**, but their relative importance depends on the baseline model capability and the specific information needs (proprietary vs. general legal knowledge).
