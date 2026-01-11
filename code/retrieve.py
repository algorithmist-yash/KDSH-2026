# code/retrieve.py

import json
import pathway as pw

# -----------------------------
# Load claims
# -----------------------------
def load_claims(path="claims_output.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------------
# Load Pathway vector store
# -----------------------------
def load_vector_store():
    return pw.io.parquet.read("./vector_store")


# -----------------------------
# Retrieve evidence per claim
# -----------------------------
def retrieve_evidence(claims, table, top_k=5):
    results = []

    for claim in claims:
        query = claim["claim_text"]

        retrieved = (
            table
            .select(
                story_id=table.story_id,
                chunk_id=table.chunk_id,
                text=table.text
            )
            .limit(top_k)
        )

        # NOTE: For now, we attach raw evidence.
        # Support/contradiction is decided in Phase 4.
        evidence_list = []

        for row in retrieved:
            evidence_list.append({
                "text": row.text,
                "relation": "unknown"
            })

        results.append({
            "claim_id": claim["claim_id"],
            "claim_text": claim["claim_text"],
            "evidence": evidence_list
        })

    return results

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    claims = load_claims()
    table = load_vector_store()

    evidence = retrieve_evidence(claims, table)

    with open("evidence_output.json", "w", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2)

    print("✅ Evidence retrieved from Pathway vector store")

