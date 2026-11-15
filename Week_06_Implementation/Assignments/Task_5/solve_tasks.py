"""Solve missing-method tasks with the RAG pipeline, then run the unit tests.

For every entry in ``missing_code.json`` the script:
1. turns the entry into a textual task,
2. retrieves the top 5 matching chunks,
3. sends the task and the chunks to an LLM,
4. writes the returned method into the target source file.

Afterwards it runs the repository's unit tests and saves the output.

Requires the ``OPENAI_API_KEY`` environment variable.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any

from openai import OpenAI

TASK_DIRECTORY = Path(__file__).resolve().parent
ASSIGNMENTS_DIRECTORY = TASK_DIRECTORY.parent
REPOSITORY_ROOT = ASSIGNMENTS_DIRECTORY / "AI4SE_Playground"
MISSING_CODE_PATH = ASSIGNMENTS_DIRECTORY / "missing_code.json"
TEST_DIRECTORY = REPOSITORY_ROOT / "playground"
RUN_LOG_PATH = TASK_DIRECTORY / "run_log.json"
TEST_OUTPUT_PATH = TASK_DIRECTORY / "test_results.txt"

sys.path.insert(0, str(ASSIGNMENTS_DIRECTORY / "Task_4"))
from match_chunks import match_task

MODEL = "gpt-5-mini"
REASONING_EFFORT = "medium"
TOP_N = 5
MAX_ATTEMPTS = 2

SYSTEM_PROMPT = (
    "You are a Python developer implementing one missing method in an existing codebase. "
    "Use the repository context to follow its conventions: reuse existing helpers, raise the "
    "same exception types with the same messages, and match the behaviour the unit tests "
    "expect. Keep the exact signature and any decorators from the stub, and include the given "
    "docstring. Return only the complete method definition as plain Python code, with no "
    "markdown fences, no explanation and no surrounding class."
)


# ---------------------------------------------------------------------------
# Locating and replacing a method in a source file
# ---------------------------------------------------------------------------

def _find_method(tree: ast.Module, class_name: str, method_name: str) -> ast.FunctionDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == method_name:
                    return item
    raise LookupError(f"{class_name}.{method_name} not found")


def _start_line(node: ast.FunctionDef) -> int:
    """First line of the method, including its decorators (1-based)."""
    return min([node.lineno, *(decorator.lineno for decorator in node.decorator_list)])


def read_stub(path: Path, class_name: str, method_name: str) -> tuple[str, bool]:
    """Return the method's current source and whether it is still an unimplemented stub."""
    source = path.read_text(encoding="utf-8")
    node = _find_method(ast.parse(source), class_name, method_name)
    lines = source.splitlines()[_start_line(node) - 1 : node.end_lineno]
    body = [statement for statement in node.body if not (
        isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Constant)
    )]
    is_stub = len(body) == 1 and isinstance(body[0], ast.Pass)
    return "\n".join(lines), is_stub


def extract_method(code: str, method_name: str) -> str:
    """Pull the method definition out of the LLM reply, dedented to column 0."""
    fenced = re.search(r"```(?:python)?\s*\n(.*?)```", code, re.DOTALL)
    if fenced:
        code = fenced.group(1)
    code = textwrap.dedent(code).strip("\n")
    tree = ast.parse(code)
    candidates = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == method_name
    ]
    if not candidates:
        raise ValueError(f"reply does not define {method_name}")
    node = candidates[0]
    lines = code.splitlines()[_start_line(node) - 1 : node.end_lineno]
    return textwrap.dedent("\n".join(lines))


def replace_method(path: Path, class_name: str, method_name: str, new_method: str) -> None:
    """Swap the method in ``path`` for ``new_method``; refuse if the result does not parse."""
    source = path.read_text(encoding="utf-8")
    node = _find_method(ast.parse(source), class_name, method_name)
    start = _start_line(node)
    lines = source.splitlines(keepends=True)
    indent = re.match(r"\s*", lines[start - 1]).group(0)
    if node.decorator_list and not new_method.lstrip().startswith("@"):
        # The model dropped the stub's decorators (e.g. @property); keep the originals.
        decorators = textwrap.dedent("".join(lines[start - 1 : node.lineno - 1]))
        new_method = decorators + new_method
    replacement = textwrap.indent(new_method, indent).rstrip("\n") + "\n"
    updated = "".join(lines[: start - 1]) + replacement + "".join(lines[node.end_lineno :])
    _find_method(ast.parse(updated), class_name, method_name)  # raises if broken
    path.write_text(updated, encoding="utf-8")


# ---------------------------------------------------------------------------
# RAG: task -> chunks -> prompt -> LLM -> source file
# ---------------------------------------------------------------------------

def describe_task(entry: dict[str, str]) -> str:
    """Turn a missing_code.json entry into a textual task."""
    summary = entry["docstring"].strip().strip('"').strip()
    return (
        f"Implement the method {entry['class']}.{entry['method']} "
        f"in {entry['file']}. {summary}"
    )


def build_prompt(task: str, stub: str, chunks: list[dict[str, Any]]) -> str:
    context = "\n\n".join(
        f"### {chunk['path']} (lines {chunk['start_line']}-{chunk['end_line']})\n"
        f"```python\n{chunk['text']}\n```"
        for chunk in chunks
    )
    return (
        f"Task: {task}\n\n"
        f"Current stub:\n```python\n{stub}\n```\n\n"
        f"Relevant repository context:\n\n{context}"
    )


def ask_llm(client: OpenAI, prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        reasoning_effort=REASONING_EFFORT,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""


def solve_task(
    client: OpenAI,
    task: str,
    target_file: Path,
    class_name: str,
    method_name: str,
) -> dict[str, Any]:
    """Retrieve context for ``task``, ask the LLM, and write the method into ``target_file``."""
    stub, _ = read_stub(target_file, class_name, method_name)
    chunks = match_task(f"{class_name}.{method_name}: {task}", n=TOP_N)
    prompt = build_prompt(task, stub, chunks)
    record: dict[str, Any] = {
        "task": task,
        "retrieved": [
            f"{chunk['path']}:{chunk['start_line']}-{chunk['end_line']} ({chunk['score']:.3f})"
            for chunk in chunks
        ],
    }

    error = ""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        reply = ask_llm(client, prompt)
        try:
            method = extract_method(reply, method_name)
            replace_method(target_file, class_name, method_name, method)
        except (SyntaxError, ValueError, LookupError) as exc:
            error = f"{type(exc).__name__}: {exc}"
            continue
        record.update(status="written", attempts=attempt, code=method)
        return record

    record.update(status="failed", attempts=MAX_ATTEMPTS, error=error)
    return record


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

def run_tests() -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=TEST_DIRECTORY,
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr
    TEST_OUTPUT_PATH.write_text(output, encoding="utf-8")
    return result.returncode, output


def main() -> int:
    parser = argparse.ArgumentParser(description="Implement missing methods with RAG, then run tests.")
    parser.add_argument("--force", action="store_true", help="Regenerate methods that are already implemented.")
    parser.add_argument("--tests-only", action="store_true", help="Skip generation and only run the tests.")
    arguments = parser.parse_args()

    if not arguments.tests_only:
        if not os.getenv("OPENAI_API_KEY"):
            print("OPENAI_API_KEY is not set.", file=sys.stderr)
            return 1
        client = OpenAI(timeout=300, max_retries=2)
        entries = json.loads(MISSING_CODE_PATH.read_text(encoding="utf-8"))
        log: list[dict[str, Any]] = []

        for number, entry in enumerate(entries, start=1):
            target = REPOSITORY_ROOT / entry["file"]
            name = f"{entry['class']}.{entry['method']}"
            _, is_stub = read_stub(target, entry["class"], entry["method"])
            if not is_stub and not arguments.force:
                print(f"[{number}/{len(entries)}] {name}: already implemented, skipped")
                log.append({"task": name, "status": "skipped"})
                continue

            record = solve_task(client, describe_task(entry), target, entry["class"], entry["method"])
            record["target"] = f"{entry['file']}::{name}"
            log.append(record)
            print(f"[{number}/{len(entries)}] {name}: {record['status']}")
            for hit in record["retrieved"]:
                print(f"      {hit}")
            if record["status"] == "failed":
                print(f"      {record['error']}")

        RUN_LOG_PATH.write_text(json.dumps(log, indent=2) + "\n", encoding="utf-8")

    print("\nRunning unit tests...")
    return_code, output = run_tests()
    summary = [line for line in output.splitlines() if re.match(r"^(Ran \d+|OK|FAILED)", line)]
    print("\n".join(summary))
    print(f"Full output saved to {TEST_OUTPUT_PATH.name}")
    return return_code


if __name__ == "__main__":
    sys.exit(main())