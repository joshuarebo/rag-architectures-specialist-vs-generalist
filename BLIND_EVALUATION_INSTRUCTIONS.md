# Blind Evaluation Instructions
## SAC-RAG vs Generic Claude Comparison

---

## 📋 Overview

You will evaluate **10 legal questions** with **2 answers each** (Answer A and Answer B). One answer is from SAC-RAG, the other from Generic RAG Claude - **but you don't know which is which** (blind evaluation).

**File to use:** `blind_evaluation_scoring_sheet.xlsx`

---

## 🎯 Scoring Rubric (1-5 Scale)

For **each answer**, assign a score from **1 to 5** based on this rubric:

### Score: 5 - Excellent ⭐⭐⭐⭐⭐
- ✅ **Accurate**: Correct Kenyan law
- ✅ **Specific**: Cites exact sections (e.g., "Section 29 of Law of Succession Act, Cap 160")
- ✅ **Jurisdiction**: Clearly references Kenyan statutes/constitution
- ✅ **Clear reasoning**: Logical explanation
- ✅ **No hallucinations**: All facts are verifiable

**Example:** *"Under Section 40(3) of the Constitution of Kenya, 2010, property acquired fraudulently can be cancelled. As established in Dina Management Ltd v Attorney General [2017], a title deed obtained through fraud is void ab initio..."*

---

### Score: 4 - Good ⭐⭐⭐⭐
- ✅ Accurate law and correct jurisdiction (Kenya)
- ✅ Correct reasoning
- ⚠️ **BUT**: Lacks specific section citations or is slightly vague
- ⚠️ **OR**: Mentions "Kenyan law" but doesn't cite exact statute names

**Example:** *"In Kenya, property obtained fraudulently can be challenged in court. The Constitution protects property rights but allows for cancellation of fraudulent titles..."*

---

### Score: 3 - Acceptable ⭐⭐⭐
- ⚠️ Generally correct advice but **misses important nuance**
- ⚠️ Refers to "general common law" rather than specific Kenyan statutes
- ⚠️ Correct outcome but weak legal foundation
- ⚠️ Some minor inaccuracies that don't critically impact advice

**Example:** *"According to common law principles, fraud vitiates all transactions. A fraudulent title can be challenged..."* (Missing specific Kenyan law)

---

### Score: 2 - Poor ⭐⭐
- ❌ **Vague** or **generic** legal advice
- ❌ Incorrectly applies **non-Kenyan law** (e.g., UK/US precedents) to Kenyan context
- ❌ Omits **critical details** (e.g., limitation periods, penalties)
- ❌ Confusing or poorly structured

**Example:** *"In English property law, the Torrens system protects bona fide purchasers..."* (Wrong jurisdiction!)

---

### Score: 1 - Dangerous ⭐
- ❌ **Factually incorrect**
- ❌ **Hallucinations**: Cites non-existent statutes or cases
- ❌ **Harmful advice**: Would damage a client's legal standing
- ❌ Completely wrong jurisdiction or area of law

**Example:** *"Under the Kenyan Property Protection Act of 2018, you must file within 30 days..."* (No such Act exists!)

---

## 📝 Step-by-Step Evaluation Process

### Step 1: Open the Scoring Sheet
Open: `blind_evaluation_scoring_sheet.xlsx`

You'll see:
- **Question_ID**: Q1, Q2, ..., Q10
- **Question**: The legal question
- **Ground_Truth**: Expert answer (for reference)
- **Answer_A**: First answer (SAC-RAG or Generic Claude - unknown!)
- **Answer_B**: Second answer (the other system - unknown!)
- **Score_A**: [Empty - you fill this]
- **Score_B**: [Empty - you fill this]
- **Winner**: [Empty - you mark A, B, or Tie]
- **Notes**: [Optional comments]

---

### Step 2: For Each Question (Q1-Q10)

1. **Read the Question** carefully
2. **Read Ground_Truth** (if available) to understand the correct answer
3. **Read Answer_A**:
   - Check: Does it cite Kenyan law specifically?
   - Check: Are section numbers/case names correct?
   - Check: Is reasoning clear and accurate?
   - Assign Score_A (1-5) using the rubric above
4. **Read Answer_B**:
   - Apply same criteria
   - Assign Score_B (1-5)
5. **Determine Winner**:
   - If `Score_A > Score_B`: Winner = "A"
   - If `Score_B > Score_A`: Winner = "B"
   - If `Score_A == Score_B`: Winner = "Tie"
6. **Add Notes** (optional):
   - Why did you score this way?
   - What was missing or excellent?

---

### Step 3: Example Evaluation

**Question:** *"Does Article 40(3) of the Constitution protect a title deed obtained fraudulently?"*

**Ground_Truth:** *"No. Article 40(3) protects property rights, but per Dina Management Ltd v AG, titles obtained fraudulently are void ab initio."*

#### Answer A:
*"No, Article 40(3) of the Constitution of Kenya, 2010, protects property rights but does not protect fraudulent transactions. As established in Dina Management Ltd v Attorney General [2017] eKLR, a title deed obtained through fraud is void ab initio (void from the beginning) and offers no protection under the Constitution."*

**Your Scoring:**
- ✅ Cites Article 40(3) correctly
- ✅ Cites specific case: Dina Management Ltd v AG [2017]
- ✅ Correct legal principle: void ab initio
- ✅ Clear and accurate

**Score_A: 5** (Excellent)

#### Answer B:
*"Property rights in Kenya are protected by the Constitution, but this protection does not extend to fraudulently obtained property. Such titles can be challenged in court and cancelled."*

**Your Scoring:**
- ⚠️ Correct outcome but vague
- ❌ No specific article citation
- ❌ No case law
- ❌ No mention of "void ab initio" principle

**Score_B: 3** (Acceptable)

**Winner: A**

---

## ⚠️ Critical Rules

1. **Do NOT open** `blind_evaluation_answer_key.xlsx` until AFTER completing all scoring
2. **Score independently**: Don't let one answer influence the other
3. **Be consistent**: Apply the same rubric standards to all 10 questions
4. **Focus on Kenyan law**: UK/US law references are negative unless clearly comparative
5. **Hallucinations = Score 1**: If an answer cites fake statutes, automatic 1

---

## ✅ After Scoring

1. Save `blind_evaluation_scoring_sheet.xlsx`
2. Open `blind_evaluation_answer_key.xlsx` to see which was SAC-RAG vs Generic Claude
3. Calculate results:
   - Count SAC-RAG wins
   - Count Generic Claude wins
   - Count ties
   - Average scores for each system

---

## 📊 What You're Testing

**Research Question:** Can a domain-adapted RAG system (SAC-RAG) using older AI technology (Claude 3.5 Sonnet) outperform a newer generic AI (Claude Sonnet 4.0) without domain-specific knowledge?

**Your blind evaluation will answer this!**

---

## 🎓 For Your Thesis

After completing blind evaluation, you'll report:

> *"Blind manual evaluation on 10 expert-curated Kenyan legal questions using a 5-point rubric revealed that [SAC-RAG/Generic Claude] achieved an average score of X.XX compared to Y.YY, winning Z/10 questions. This demonstrates that [domain adaptation/model scale] is the primary driver of legal QA performance."*

---

## Need Help?

If you're unsure about a score:
- **When in doubt, be conservative** (lower score)
- **Focus on specificity**: Does it cite exact Kenyan statutes?
- **Check for hallucinations**: Google the case names/sections if unsure

**Good luck with your evaluation! 🎯**
