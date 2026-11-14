"""Match an input task embedding against the stored chunk embeddings.

The stored embeddings, metadata, model and overlap-merging helpers are reused
from Task 3 (``retrieve.py``) rather than duplicated, so both tasks always use
the same vectors, the same model and the same merging rules.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import numpy as np

TASK_3_DIRECTORY = Path(__file__).resolve().parents[1] / "Task_3"
sys.path.insert(0, str(TASK_3_DIRECTORY))

import retrieve

DEFAULT_N = 6


def embed_task(task: str) -> np.ndarray:
    """Turn a task description into a normalised query embedding.

    Uses the same model and BGE query prefix as Task 3, so the result is
    directly comparable with the stored chunk embeddings.
    """
    vector = retrieve.MODEL.encode(
        retrieve.QUERY_PREFIX + task,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )
    return np.asarray(vector, dtype=np.float32)


def match(
    query_embedding: np.ndarray,
    n: int = DEFAULT_N,
    merge: bool = True,
    min_score: float | None = None,
) -> list[dict[str, Any]]:
    """Return the ``n`` stored chunks most similar to ``query_embedding``.

    Similarity is cosine similarity. Each result contains path, start_line,
    end_line, score, text and the ids of the chunks it was built from.

    Args:
        query_embedding: vector with the same dimension as the stored embeddings.
        n: number of results to return.
        merge: combine overlapping or touching hits from the same file into one
            result, then keep taking candidates until ``n`` results exist.
        min_score: if given, ignore chunks scoring below this value.
    """
    if n <= 0:
        return []

    query = np.asarray(query_embedding, dtype=np.float32).reshape(-1)
    if query.shape[0] != retrieve.EMBEDDINGS.shape[1]:
        raise ValueError(
            f"expected a {retrieve.EMBEDDINGS.shape[1]}-dimensional embedding, "
            f"got {query.shape[0]}"
        )
    norm = float(np.linalg.norm(query))
    if norm == 0.0:
        raise ValueError("query embedding must not be all zeros")
    query = query / norm  # stored vectors are unit length, so dot product = cosine

    scores = retrieve.EMBEDDINGS @ query
    results: list[dict[str, Any]] = []

    for index in np.argsort(-scores):
        score = float(scores[index])
        if min_score is not None and score < min_score:
            break  # candidates are in descending order, so the rest score lower

        chunk = retrieve.METADATA[int(index)]
        hit = {
            "path": chunk["path"],
            "start_line": chunk["start_line"],
            "end_line": chunk["end_line"],
            "score": score,
            "text": chunk["text"],
            "chunk_ids": [chunk["id"]],
        }

        if merge:
            overlapping = [result for result in results if retrieve._touches(result, hit)]
            if overlapping:
                results = [
                    result
                    for result in results
                    if not any(result is other for other in overlapping)
                ]
                hit = retrieve._merge_group([*overlapping, hit])

        results.append(hit)
        if len(results) >= n:
            break

    return sorted(results, key=lambda result: result["score"], reverse=True)[:n]


def match_task(
    task: str,
    n: int = DEFAULT_N,
    merge: bool = True,
    min_score: float | None = None,
) -> list[dict[str, Any]]:
    """Convenience wrapper: embed ``task`` and return its ``n`` best matches."""
    return match(embed_task(task), n=n, merge=merge, min_score=min_score)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find the repository chunks most relevant to a coding task."
    )
    parser.add_argument("task", help="Description of the coding task.")
    parser.add_argument("-n", type=int, default=DEFAULT_N, help="Number of results.")
    parser.add_argument("--no-merge", action="store_true", help="Do not merge overlapping hits.")
    parser.add_argument("--min-score", type=float, default=None, help="Ignore weaker matches.")
    arguments = parser.parse_args()

    results = match_task(
        arguments.task,
        n=arguments.n,
        merge=not arguments.no_merge,
        min_score=arguments.min_score,
    )
    for rank, result in enumerate(results, start=1):
        print(
            f"{rank}. {result['path']}:{result['start_line']}-{result['end_line']} "
            f"(score={result['score']:.4f})"
        )


if __name__ == "__main__":
    main()