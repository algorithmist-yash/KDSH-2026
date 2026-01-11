# code/ingest.py

import os
from pathlib import Path
import pathway as pw
from sentence_transformers import SentenceTransformer
import yaml

# -----------------------------
# Load config
# -----------------------------
with open("config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)

NOVELS_DIR = CONFIG["paths"]["novels_dir"]
CHUNK_SIZE = CONFIG["chunking"]["chunk_size"]
CHUNK_OVERLAP = CONFIG["chunking"]["chunk_overlap"]
EMBED_MODEL_NAME = CONFIG["embedding"]["model"]

# -----------------------------
# Helper: chunk long text safely
# -----------------------------
def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

# -----------------------------
# Load novels from folder
# -----------------------------
def load_novels(novels_dir):
    data = []
    for file in os.listdir(novels_dir):
        if file.endswith(".txt"):
            story_id = file.replace(".txt", "")
            with open(os.path.join(novels_dir, file), "r", encoding="utf-8") as f:
                text = f.read()
                data.append((story_id, text))
    return data

# -----------------------------
# Build Pathway table
# -----------------------------
def build_pathway_table():
    novels = load_novels(NOVELS_DIR)
    records = []

    for story_id, text in novels:
        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        for i, chunk in enumerate(chunks):
            records.append(
                {
                    "story_id": story_id,
                    "chunk_id": i,
                    "text": chunk
                }
            )

    return pw.debug.table_from_records(records)

# -----------------------------
# Embedding function
# -----------------------------
embedder = SentenceTransformer(EMBED_MODEL_NAME)

def embed_text(texts):
    return embedder.encode(texts).tolist()

# -----------------------------
# Main ingestion pipeline
# -----------------------------
def main():
    table = build_pathway_table()

    embedded = table.select(
        story_id=table.story_id,
        chunk_id=table.chunk_id,
        text=table.text,
        embedding=pw.apply(embed_text, table.text)
    )

    pw.io.persist(
        embedded,
        pw.io.local_storage(
            path="./vector_store",
            format="parquet"
        )
    )

    print("✅ Ingestion complete. Vector store ready.")

    pw.run()

if __name__ == "__main__":
    main()
