"""Embed Task 2 repository chunks for semantic retrieval."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"
TASK_2_DIRECTORY = Path(__file__).resolve().parents[1] / "Task_2"
CHUNKS_PATH = TASK_2_DIRECTORY / "chunks.json"
EMBEDDINGS_PATH = Path(__file__).with_name("embeddings.npy")
METADATA_PATH = Path(__file__).with_name("embeddings_meta.json")


def embedding_text(chunk: dict[str, object]) -> str:
    return (
        f"File: {chunk['path']} "
        f"(lines {chunk['start_line']}-{chunk['end_line']})\n"
        f"{chunk['text']}"
    )


def main() -> None:
    chunks = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))
    embedded_chunks = [
        chunk for chunk in chunks if not str(chunk["path"]).endswith(".gitignore")
    ]
    skipped = len(chunks) - len(embedded_chunks)

    model = SentenceTransformer(MODEL_NAME)
    vectors = model.encode(
        [embedding_text(chunk) for chunk in embedded_chunks],
        normalize_embeddings=True,
        convert_to_numpy=True,
    )
    embeddings = np.asarray(vectors, dtype=np.float32)

    metadata = [
        {
            **chunk,
            "model": MODEL_NAME,
        }
        for chunk in embedded_chunks
    ]
    np.save(EMBEDDINGS_PATH, embeddings)
    METADATA_PATH.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Embedded {len(embedded_chunks)} chunks; skipped {skipped}")
    print(f"Matrix shape: {embeddings.shape}")


if __name__ == "__main__":
    main()
