# KDSH 2026 – Track A Submission
## Team Algorithmist

### Team Members
- **Yash Raj** (26KTJYAS643839)
- **Shreyanshu Ranjan** (26KTJSHR703353)
- **Sparsh Bajoria** (26KTJSPA589622)
- **Tanay Tushar** (26KTJTAN769353)

Department of Computer Science and Engineering  
Kalinga Institute of Industrial Technology (KIIT)

---

## Problem Overview
The task is to determine whether a character’s backstory is globally consistent with
the events described in a long narrative (novel-length text).
The challenge lies in reasoning over long contexts while relying on evidence,
not surface-level similarity.

---

## Solution Overview
We designed a multi-stage reasoning pipeline:

1. **Atomic Claim Extraction**
   - Backstories are decomposed into atomic, verifiable claims
   - Prevents vague or entangled reasoning
   - Implemented using a local instruction-following language model

2. **Long-Context Ingestion (Pathway)**
   - Novels are chunked and loaded into a Pathway table
   - Explicit schemas ensure type safety
   - Lazy evaluation allows scaling to very long texts

3. **Evidence Retrieval**
   - For each claim, relevant novel chunks are retrieved
   - Retrieval and reasoning are deliberately separated

4. **Contradiction Detection**
   - A Natural Language Inference (MNLI) model classifies claim–evidence pairs
   - Detects support, contradiction, or neutrality

5. **Deterministic Aggregation**
   - Strong contradictions lead to an inconsistent label
   - Otherwise, the story is considered consistent

---

## Engineering Challenges & How We Solved Them

### Pathway API Differences
- Encountered missing or renamed APIs across versions
- Solved by:
  - Using explicit schemas
  - Avoiding version-specific persistence APIs
  - Building a unified ingestion + retrieval pipeline

### Model Size Constraints
- Large models caused memory and download issues
- Switched to lightweight local models for:
  - Claim extraction
  - Natural Language Inference

### Environment Issues
- Python version conflicts
- Missing system tools (zip)

All issues were handled incrementally with reproducible fixes.

---

## Reproducibility
- Fully local execution
- No external APIs required
- Deterministic scoring logic
- Clear separation of pipeline stages

---

## Output
- Final predictions are written to `results.csv`
- Format strictly follows competition requirements

---

## Repository Structure
```
KDSH_2026/
├── code/
│   ├── claims.py
│   ├── pipeline.py
│   ├── score.py
│   └── ingest.py
├── results.csv
├── README.md
└── report.pdf
```

---

## Conclusion
This repository implements an interpretable, scalable, and evidence-based approach
to long-narrative consistency checking using Pathway and structured reasoning.
