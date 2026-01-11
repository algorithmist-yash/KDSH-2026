# code/score.py

import json
from transformers import pipeline

# -----------------------------
# Load claims
# -----------------------------
def load_claims(path="claims_output.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------------
# Load dummy evidence (for now)
# Later: replace with real Pathway-exported chunks
# -----------------------------
def load_evidence():
    # Minimal placeholder evidence to complete the pipeline
    # When you add real novels, replace this with actual chunks
    return [
        {
            "text": "The character avoided conflict and preferred peaceful solutions.",
        },
        {
            "text": "Later in life, the character was forced into violent confrontations.",
        }
    ]

# -----------------------------
# NLI model (local, light)
# -----------------------------
nli = pipeline(
    "text-classification",
    model="roberta-large-mnli",
    device_map="auto"
)

def classify_relation(claim, passage):
    premise = passage
    hypothesis = claim
    out = nli(f"{premise} </s></s> {hypothesis}", truncation=True)[0]
    return out["label"], out["score"]

# -----------------------------
# Score claims
# -----------------------------
def score_claims(claims, evidence):
    claim_scores = []
    rationales = []

    for c in claims:
        claim_text = c["claim_text"]
        score = 0

        for ev in evidence:
            label, conf = classify_relation(claim_text, ev["text"])

            if label == "CONTRADICTION" and conf > 0.6:
                score -= 2
                rationales.append(
                    f"Contradicted by passage: '{ev['text'][:60]}...'"
                )
            elif label == "ENTAILMENT" and conf > 0.6:
                score += 1

        claim_scores.append(score)

    return claim_scores, rationales

# -----------------------------
# Aggregate to final decision
# -----------------------------
def aggregate(claim_scores):
    if any(s <= -2 for s in claim_scores):
        return 0
    return 1

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    claims = load_claims()
    evidence = load_evidence()

    claim_scores, rationales = score_claims(claims, evidence)
    prediction = aggregate(claim_scores)

    result = {
        "story_id": "example_story",
        "prediction": prediction,
        "rationale": rationales[:2]
    }

    with open("results.csv", "w", encoding="utf-8") as f:
        f.write("story_id,prediction,rationale\n")
        f.write(
            f"{result['story_id']},{result['prediction']},\"{' | '.join(result['rationale'])}\"\n"
        )

    print("✅ results.csv generated")
