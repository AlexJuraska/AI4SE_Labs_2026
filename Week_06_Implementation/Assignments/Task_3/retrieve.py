"""Retrieve repository chunks using semantic similarity."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"
EMBEDDINGS_PATH = Path(__file__).with_name("embeddings.npy")
METADATA_PATH = Path(__file__).with_name("embeddings_meta.json")
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

EMBEDDINGS = np.load(EMBEDDINGS_PATH)
METADATA: list[dict[str, Any]] = json.loads(
    METADATA_PATH.read_text(encoding="utf-8")
)
MODEL = SentenceTransformer(MODEL_NAME)


def _chunk_lines(chunk: dict[str, Any]) -> dict[int, str]:
    return {
        line_number: line
        for line_number, line in enumerate(
            str(chunk["text"]).splitlines(),
            start=int(chunk["start_line"]),
        )
    }


def _merge_group(group: list[dict[str, Any]]) -> dict[str, Any]:
    start_line = min(int(hit["start_line"]) for hit in group)
    end_line = max(int(hit["end_line"]) for hit in group)
    lines: dict[int, str] = {}
    for hit in sorted(group, key=lambda item: int(item["start_line"])):
        lines.update({line: text for line, text in _chunk_lines(hit).items() if line not in lines})

    return {
        "path": group[0]["path"],
        "start_line": start_line,
        "end_line": end_line,
        "score": max(float(hit["score"]) for hit in group),
        "text": "\n".join(lines[line] for line in sorted(lines)),
        "chunk_ids": [
            chunk_id
            for hit in group
            for chunk_id in hit["chunk_ids"]
        ],
    }


def _touches(first: dict[str, Any], second: dict[str, Any]) -> bool:
    return (
        first["path"] == second["path"]
        and int(first["start_line"]) <= int(second["end_line"]) + 1
        and int(second["start_line"]) <= int(first["end_line"]) + 1
    )


def search(query: str, k: int = 5, merge: bool = True) -> list[dict]:
    """Return up to ``k`` highest-scoring repository results."""
    if k <= 0:
        return []

    query_vector = MODEL.encode(
        QUERY_PREFIX + query,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )
    scores = EMBEDDINGS @ np.asarray(query_vector, dtype=np.float32)
    ranked_indices = np.argsort(-scores)
    results: list[dict[str, Any]] = []

    for index in ranked_indices:
        metadata = METADATA[int(index)]
        hit = {
            **metadata,
            "score": float(scores[int(index)]),
            "chunk_ids": [metadata["id"]],
        }
        if not merge:
            results.append(
                {
                    "path": hit["path"],
                    "start_line": hit["start_line"],
                    "end_line": hit["end_line"],
                    "score": hit["score"],
                    "text": hit["text"],
                    "chunk_ids": hit["chunk_ids"],
                }
            )
        else:
            matching = [
                result for result in results if _touches(result, hit)
            ]
            if matching:
                merged_group = [
                    hit
                    for result in matching
                    for hit in [
                        {
                            "path": result["path"],
                            "start_line": result["start_line"],
                            "end_line": result["end_line"],
                            "score": result["score"],
                            "text": result["text"],
                            "chunk_ids": result["chunk_ids"],
                        }
                    ]
                ]
                merged_group.append(hit)
                results = [
                    result for result in results if result not in matching
                ]
                results.append(_merge_group(merged_group))
            else:
                results.append(_merge_group([hit]))

        if len(results) >= k:
            break

    return sorted(results, key=lambda result: result["score"], reverse=True)[:k]


def main() -> None:
    parser = argparse.ArgumentParser(description="Search embedded repository chunks.")
    parser.add_argument("query", help="Natural-language search query.")
    parser.add_argument("-k", type=int, default=5, help="Number of results.")
    parser.add_argument("--no-merge", action="store_true", help="Do not merge adjacent hits.")
    arguments = parser.parse_args()

    for result in search(arguments.query, arguments.k, merge=not arguments.no_merge):
        print(
            f"{result['path']}:{result['start_line']}-{result['end_line']} "
            f"(score={result['score']:.4f})"
        )
        preview = result["text"].splitlines()[:3]
        print("\n".join(f"  {line}" for line in preview))


if __name__ == "__main__":
    main()
