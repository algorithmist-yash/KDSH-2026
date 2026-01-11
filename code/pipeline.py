# code/pipeline.py

import json
import pathway as pw

# -----------------------------
# Load claims (Python-side)
# -----------------------------
def load_claims(path="claims_output.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------------
# Load novel text (simple version)
# -----------------------------
def load_novel_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text, chunk_size=800, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks    


# -----------------------------
# Build Pathway table (CORRECT)
# -----------------------------
class NovelChunkSchema(pw.Schema):
    chunk_id: int
    text: str


def build_novel_table(novel_path):
    text = load_novel_text(novel_path)
    chunks = chunk_text(text)

    rows = [
        (i, chunk)
        for i, chunk in enumerate(chunks)
    ]

    return pw.debug.table_from_rows(
        schema=NovelChunkSchema,
        rows=rows
    )




# -----------------------------
# Main Pathway pipeline
# -----------------------------
if __name__ == "__main__":
    claims = load_claims()
    novel_table = build_novel_table("../data/novels/example_novel.txt")

    # Attach claims logically (scoring comes later)
    for claim in claims:
        _ = novel_table.select(
            chunk_id=novel_table.chunk_id,
            text=novel_table.text
        )

    print("✅ Pathway pipeline built (ingestion + retrieval scaffold)")
    pw.run()
