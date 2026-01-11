# code/claims.py

import json
from transformers import pipeline

# -----------------------------
# Prompt template
# -----------------------------
CLAIM_EXTRACTION_PROMPT = """
You are a strict narrative analyst.

Given a hypothetical backstory of a character, extract ONLY atomic,
verifiable claims that could later be tested against a novel.

Rules:
- Each claim must express exactly ONE idea
- Do NOT invent facts
- Do NOT rephrase creatively
- If something is vague, keep it vague
- Focus on beliefs, behaviors, events, motivations, constraints

Output MUST be valid JSON.
Do NOT include explanations.

Schema:
[
  {
    "claim_id": "C1",
    "claim_text": "...",
    "claim_type": "belief | behavior | event | constraint | motivation",
    "time_scope": "early_life | adulthood | entire_life",
    "confidence": "low | medium | high"
  }
]

Backstory:
<<<BACKSTORY>>>
"""

# -----------------------------
# Load local model
# -----------------------------
print("⏳ Loading local model (first time may take a few minutes)...")

extractor = pipeline(
    "text-generation",
    model="google/flan-t5-large",
    device_map="auto",
    max_new_tokens=600
)

print("✅ Model loaded")

# -----------------------------
# Local extractor
# -----------------------------
def extract_claims_local(backstory_text):
    prompt = CLAIM_EXTRACTION_PROMPT.replace("<<<BACKSTORY>>>", backstory_text)

    output = extractor(prompt)[0]["generated_text"]

    # Try to isolate JSON
    json_start = output.find("[")
    json_end = output.rfind("]") + 1

    if json_start == -1 or json_end == -1:
        raise ValueError("Model did not produce JSON output")

    return json.loads(output[json_start:json_end])


# -----------------------------
# Utility
# -----------------------------
def load_backstory(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    backstory_path = "../data/backstories/example.txt"
    backstory_text = load_backstory(backstory_path)

    claims = extract_claims_local(backstory_text)

    with open("claims_output.json", "w", encoding="utf-8") as f:
        json.dump(claims, f, indent=2)

    print(f"✅ Extracted {len(claims)} atomic claims (LOCAL)")

