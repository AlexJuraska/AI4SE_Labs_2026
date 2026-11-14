"""Split a text repository into overlapping JSON chunks for retrieval."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_CHUNK_LINES = 80
DEFAULT_OVERLAP_LINES = 10
DEFAULT_SOURCE = Path(__file__).parents[1] / "AI4SE_Playground"
EXCLUDED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "node_modules",
}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create line-based, overlapping chunks from a text repository."
    )
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Repository directory to process.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(__file__).with_name("chunks.json"),
        help="JSON file to create.",
    )
    parser.add_argument(
        "--chunk-lines",
        type=int,
        default=DEFAULT_CHUNK_LINES,
        help=f"Maximum lines per chunk (default: {DEFAULT_CHUNK_LINES}).",
    )
    parser.add_argument(
        "--overlap-lines",
        type=int,
        default=DEFAULT_OVERLAP_LINES,
        help=f"Lines repeated between adjacent chunks (default: {DEFAULT_OVERLAP_LINES}).",
    )
    return parser.parse_args()


def read_text_file(path: Path) -> str | None:
    data = path.read_bytes()
    if b"\x00" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def repository_files(source: Path) -> list[Path]:
    return sorted(
        path
        for path in source.rglob("*")
        if path.is_file()
        and not any(part in EXCLUDED_DIRECTORIES for part in path.relative_to(source).parts)
    )


def make_chunks(
    source: Path, chunk_lines: int, overlap_lines: int
) -> list[dict[str, int | str]]:
    chunks: list[dict[str, int | str]] = []
    step = chunk_lines - overlap_lines

    for path in repository_files(source):
        text = read_text_file(path)
        if text is None:
            continue

        lines = text.splitlines()
        if not lines:
            continue

        relative_path = path.relative_to(source).as_posix()
        chunk_number = 0
        for start in range(0, len(lines), step):
            end = min(start + chunk_lines, len(lines))
            chunks.append(
                {
                    "id": f"{relative_path}:{start + 1}-{end}",
                    "path": relative_path,
                    "start_line": start + 1,
                    "end_line": end,
                    "chunk_number": chunk_number,
                    "text": "\n".join(lines[start:end]),
                }
            )
            chunk_number += 1
            if end == len(lines):
                break

    return chunks


def main() -> None:
    arguments = parse_arguments()
    if not arguments.source.is_dir():
        raise SystemExit(f"Source directory does not exist: {arguments.source}")
    if arguments.chunk_lines <= 0:
        raise SystemExit("--chunk-lines must be greater than zero")
    if not 0 <= arguments.overlap_lines < arguments.chunk_lines:
        raise SystemExit("--overlap-lines must be non-negative and smaller than --chunk-lines")

    chunks = make_chunks(
        arguments.source,
        arguments.chunk_lines,
        arguments.overlap_lines,
    )
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(chunks, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(chunks)} chunks to {arguments.output}")


if __name__ == "__main__":
    main()
