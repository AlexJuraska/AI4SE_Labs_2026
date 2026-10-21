# Before using run "run pip install -r requirements.txt"

from __future__ import annotations

import argparse
import functools
import os
import re
import shutil
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from email import policy
from email.parser import BytesParser
from pathlib import Path
from typing import Literal, TypedDict

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

MODELS = {
    "extract": ("gpt-5-mini", "low"),
    "synthesize": ("gpt-5.6-luna", "medium"),
    "review": ("gpt-5.4-nano", "low"),
}
REQUEST_TIMEOUT = 300
MAX_RETRIES = 2
EXTRACTION_WORKERS = 6
MAX_REVIEW_ROUNDS = 2
SUPPORTED_SUFFIXES = {".txt", ".md", ".eml"}
MIN_EXPLANATION_WORDS = 25

PRIORITY_MODALS = {
    "Must": ("shall", "must"),
    "Should": ("should",),
    "Could": ("could", "may"),
    "Won't": ("will not", "won't", "shall not"),
}

STYLE_RULES = (
    "Writing rules: (1) Use 'shall' for Must, 'should' for Should, 'could' for Could, and "
    "'will not' for Won't statements. (2) Use one consistent term per concept across all "
    "requirements (for example always 'item' rather than alternating between item, copy and "
    "volume unless they mean different things; always 'patron' rather than user/customer for "
    "library members; always 'staff user' for system operators). (3) Write dates as ISO-8601. "
    "(4) The explanation is one paragraph giving the rationale, context and intended use of "
    "the requirement; it must NOT list source filenames, because sources belong only in the "
    "sources field."
)

class Progress:
    """One status line that refreshes in place; finished steps stay above it."""

    LABEL_WIDTH = 26

    def __init__(self, stream=sys.stdout, interval: float = 0.1):
        self.stream = stream
        self.interval = interval
        self.live = hasattr(stream, "isatty") and stream.isatty()
        unicode_ok = (getattr(stream, "encoding", "") or "").lower().startswith("utf")
        self.frames = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏" if unicode_ok else "|/-\\"
        self.ok_mark = "✔" if unicode_ok else "+"
        self.fail_mark = "✘" if unicode_ok else "x"
        self.sep = "│" if unicode_ok else "|"
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._run_start = time.perf_counter()
        self._stage: str | None = None
        self._stage_start = 0.0
        self._detail = ""
        self._frame = 0
        if self.live and os.name == "nt":
            os.system("")

    @staticmethod
    def fmt(seconds: float) -> str:
        minutes, secs = divmod(seconds, 60)
        return f"{int(minutes)}:{secs:04.1f}" if minutes else f"{secs:.1f}s"

    def _clear(self) -> None:
        if self.live:
            self.stream.write("\r\x1b[2K")

    def _draw(self) -> None:
        if not self.live or self._stage is None:
            return
        now = time.perf_counter()
        frame = self.frames[self._frame % len(self.frames)]
        parts = [
            f"{frame} {self._stage:<{self.LABEL_WIDTH}}",
            f"{self.fmt(now - self._stage_start):>7}",
        ]
        if self._detail:
            parts.append(self._detail)
        parts.append(f"total {self.fmt(now - self._run_start)}")
        line = f" {self.sep} ".join(parts)
        width = max(20, shutil.get_terminal_size().columns - 1)
        self.stream.write("\r\x1b[2K" + line[:width])
        self.stream.flush()

    def _tick(self) -> None:
        while not self._stop.wait(self.interval):
            with self._lock:
                self._frame += 1
                self._draw()

    def start(self) -> None:
        self._run_start = time.perf_counter()
        if self.live:
            self._thread = threading.Thread(target=self._tick, daemon=True)
            self._thread.start()

    def begin(self, stage: str) -> None:
        with self._lock:
            self._stage, self._stage_start, self._detail = stage, time.perf_counter(), ""
            self._draw()

    def detail(self, text: str) -> None:
        with self._lock:
            self._detail = text
            self._draw()

    def log(self, message: str) -> None:
        """Print a permanent line above the live status line."""
        with self._lock:
            self._clear()
            self.stream.write(f"    {message}\n")
            self._draw()
            self.stream.flush()

    def end(self, ok: bool = True, note: str = "") -> None:
        with self._lock:
            if self._stage is None:
                return
            elapsed = time.perf_counter() - self._stage_start
            mark = self.ok_mark if ok else self.fail_mark
            line = f"{mark} {self._stage:<{self.LABEL_WIDTH}} {self.sep} {self.fmt(elapsed):>7}"
            if note:
                line += f" {self.sep} {note}"
            self._clear()
            self.stream.write(line + "\n")
            self.stream.flush()
            self._stage = None

    def stop(self) -> float:
        self._stop.set()
        if self._thread:
            self._thread.join()
        with self._lock:
            self._clear()
            self.stream.flush()
        return time.perf_counter() - self._run_start


PROGRESS = Progress()

def _summarize(node: str, result: dict) -> str:
    """Short note shown next to a finished step."""
    if "validation_issues" in result:
        issues = result["validation_issues"]
        return "all checks passed" if not issues else f"{len(issues)} rule violations"
    if "documents" in result:
        return f"{len(result['documents'])} documents"
    if "candidates" in result:
        return f"{len(result['candidates'])} candidates, {len(result['discarded'])} discarded"
    if "review" in result:
        review = result["review"]
        return "approved" if review.approved else f"{len(review.issues)} issues found"
    if "draft" in result:
        return f"{len(result['draft'].requirements)} requirements"
    return ""


def tracked(name: str, func):
    """Wrap a graph node so its runtime is shown live and recorded when done."""

    @functools.wraps(func)
    def wrapper(state):
        label = name
        if name in ("validate_requirements", "review_requirements", "revise_requirements"):
            label = f"{name} #{state.get('review_round', 0) + 1}"
        PROGRESS.begin(label)
        try:
            result = func(state)
        except KeyboardInterrupt:
            PROGRESS.end(ok=False, note="interrupted")
            raise
        except Exception as exc:
            PROGRESS.end(ok=False, note=f"failed: {type(exc).__name__}")
            raise
        PROGRESS.end(note=_summarize(name, result))
        return result

    return wrapper


class SourceDocument(BaseModel):
    name: str
    path: str
    text: str


class CandidateRequirement(BaseModel):
    id: str = Field(description="Unique identifier in the form R-NNN, for example R-001")
    name: str = Field(description="Short descriptive name, at most about eight words")
    statement: str = Field(description="One-sentence requirement using the modal verb for its priority")
    explanation: str = Field(
        description="One paragraph of rationale and context; never list source filenames here"
    )
    priority: Literal["Must", "Should", "Could", "Won't"]
    sources: list[str] = Field(min_length=1, description="Exact input filenames this was derived from")


DiscardCategory = Literal["conflicting", "nonsensical", "out_of_scope", "non_requirement"]


class DiscardedItem(BaseModel):
    name: str = Field(description="Short name of the discarded candidate requirement or content")
    category: DiscardCategory = Field(
        description="conflicting: contradicts a kept requirement; nonsensical: unclear or "
        "impossible; out_of_scope: valid but outside this system; non_requirement: anecdote, "
        "logistics, metadata or other content that is not a requirement"
    )
    reason: str = Field(description="One or two sentences explaining why it was discarded")
    sources: list[str] = Field(default_factory=list, description="Exact input filenames")


class Extraction(BaseModel):
    requirements: list[CandidateRequirement]
    discarded: list[DiscardedItem] = Field(default_factory=list)


class RequirementDocument(BaseModel):
    title: str
    requirements: list[CandidateRequirement]
    discarded: list[DiscardedItem] = Field(
        default_factory=list,
        description="Only candidates rejected during consolidation (conflicts, nonsensical or "
        "out-of-scope candidates). Do not repeat extraction-stage discarded items.",
    )


class Review(BaseModel):
    approved: bool
    issues: list[str] = Field(default_factory=list)


class NetworkState(TypedDict, total=False):
    input_dir: str
    documents: list[SourceDocument]
    candidates: list[CandidateRequirement]
    discarded: list[DiscardedItem]
    draft: RequirementDocument
    validation_issues: list[str]
    review: Review
    review_round: int
    final: RequirementDocument


def read_document(path: Path) -> str:
    if path.suffix.lower() == ".eml":
        message = BytesParser(policy=policy.default).parsebytes(path.read_bytes())
        parts = [part.get_content() for part in message.walk() if part.get_content_type() == "text/plain"]
        return "\n".join(parts).strip()
    return path.read_text(encoding="utf-8", errors="replace").strip()


def load_documents(state: NetworkState) -> dict[str, object]:
    """Deterministic node: load and normalize every supported corpus file."""
    directory = Path(state["input_dir"])
    if not directory.is_dir():
        raise FileNotFoundError(f"Input directory does not exist: {directory}")
    paths = sorted(
        path for path in directory.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )
    if not paths:
        raise ValueError(f"No {', '.join(sorted(SUPPORTED_SUFFIXES))} documents found in {directory}")
    documents = [
        SourceDocument(name=path.name, path=str(path), text=read_document(path))
        for path in paths
    ]
    return {"documents": documents, "review_round": 0}


def make_model(role: str) -> ChatOpenAI:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required to run the LangGraph network.")
    model, effort = MODELS[role]
    return ChatOpenAI(
        model=model,
        reasoning_effort=effort,
        timeout=REQUEST_TIMEOUT,
        max_retries=MAX_RETRIES,
    )


def _dump(items: list[BaseModel]) -> list[dict]:
    return [item.model_dump() for item in items]


def extract_requirements(state: NetworkState) -> dict[str, object]:
    """Extract candidates from every document in parallel."""
    extractor = make_model("extract").with_structured_output(Extraction)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a requirements analyst. Extract every actionable software requirement "
                "from the document; do not skip requirements that are stated only once or "
                "informally. Preserve source filenames exactly. Do not invent details. Use MoSCoW "
                "priority: Must is essential, Should is important but deferrable, Could is "
                "desirable, and Won't is explicitly out of scope. "
                "Record anything you do not turn into a requirement in discarded, with a category "
                "(conflicting, nonsensical, out_of_scope, non_requirement) and a concrete reason. "
                + STYLE_RULES,
            ),
            ("human", "Source filename: {name}\n\nDocument:\n{text}"),
        ]
    )
    chain = prompt | extractor
    documents = state["documents"]
    total = len(documents)
    results: dict[int, Extraction] = {}
    start = time.perf_counter()
    PROGRESS.detail(f"0/{total} files")

    pool = ThreadPoolExecutor(max_workers=EXTRACTION_WORKERS)
    try:
        futures = {
            pool.submit(chain.invoke, {"name": doc.name, "text": doc.text}): index
            for index, doc in enumerate(documents)
        }
        for done, future in enumerate(as_completed(futures), 1):
            index = futures[future]
            result = future.result()
            results[index] = result
            PROGRESS.log(
                f"{documents[index].name:<45} {len(result.requirements):>3} reqs "
                f"at {Progress.fmt(time.perf_counter() - start)}"
            )
            PROGRESS.detail(f"{done}/{total} files")
    except BaseException:
        pool.shutdown(wait=False, cancel_futures=True)
        raise
    pool.shutdown()

    candidates: list[CandidateRequirement] = []
    discarded: list[DiscardedItem] = []
    for index, document in enumerate(documents):
        for candidate in results[index].requirements:
            candidates.append(candidate.model_copy(update={"sources": [document.name]}))
        for item in results[index].discarded:
            discarded.append(item.model_copy(update={"sources": [document.name]}))
    return {"candidates": candidates, "discarded": discarded}


def synthesize_requirements(state: NetworkState) -> dict[str, RequirementDocument]:
    synthesizer = make_model("synthesize").with_structured_output(RequirementDocument)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are the lead requirements engineer. Merge semantically duplicate candidates "
                "into one requirement, preserving every relevant source filename. Every candidate "
                "must end up either merged into a kept requirement or listed in discarded; do not "
                "silently drop any. Resolve conflicts by keeping the supported, specific "
                "requirement; record each rejected conflicting, nonsensical or out-of-scope "
                "candidate in discarded with its category, a concrete reason and its sources. "
                "Do not repeat the extraction-stage discarded items you are given. Assign unique "
                "IDs R-001, R-002, ... in thematic order. Produce a standalone specification, not "
                "commentary. " + STYLE_RULES,
            ),
            ("human", "Candidates:\n{candidates}\n\nExtraction-stage discarded items (context only):\n{discarded}"),
        ]
    )
    result = (prompt | synthesizer).invoke(
        {"candidates": _dump(state["candidates"]), "discarded": _dump(state.get("discarded", []))}
    )
    return {"draft": result}


def validate_requirements(state: NetworkState) -> dict[str, list[str]]:
    """Deterministic node: enforce rules that do not need an LLM (OS2, OS3, OS4, OS5, OS7, OS8)."""
    draft = state["draft"]
    known = {doc.name for doc in state["documents"]}
    issues: list[str] = []

    seen_ids: dict[str, int] = {}
    for req in draft.requirements:
        if not re.fullmatch(r"R-\d{3}", req.id):
            issues.append(f"{req.id}: ID must have the form R-NNN (for example R-007).")
        seen_ids[req.id] = seen_ids.get(req.id, 0) + 1
    for req_id, count in seen_ids.items():
        if count > 1:
            issues.append(f"{req_id}: ID is used by {count} requirements; IDs must be unique.")

    seen_names: dict[str, str] = {}
    for req in draft.requirements:
        key = re.sub(r"\W+", " ", req.name).strip().lower()
        if key in seen_names:
            issues.append(f"{req.id} and {seen_names[key]} share the name '{req.name}'; merge or rename them.")
        else:
            seen_names[key] = req.id

    for req in draft.requirements:
        for source in req.sources:
            if source not in known:
                issues.append(f"{req.id}: source '{source}' is not an input file; use exact filenames.")
    for item in draft.discarded:
        for source in item.sources:
            if source not in known:
                issues.append(f"Discarded '{item.name}': source '{source}' is not an input file.")

    for req in draft.requirements:
        if len(req.explanation.split()) < MIN_EXPLANATION_WORDS:
            issues.append(f"{req.id}: explanation is shorter than a paragraph; give rationale and context.")
        if any(name in req.explanation for name in known):
            issues.append(f"{req.id}: explanation lists source filenames; keep sources only in the sources field.")
        statement = req.statement.lower()
        if not any(modal in statement for modal in PRIORITY_MODALS[req.priority]):
            expected = " or ".join(f"'{m}'" for m in PRIORITY_MODALS[req.priority])
            issues.append(f"{req.id}: priority is {req.priority} but the statement does not use {expected}.")

    covered = {source for req in draft.requirements for source in req.sources}
    covered |= {source for item in draft.discarded for source in item.sources}
    contributing = {source for cand in state["candidates"] for source in cand.sources}
    for name in sorted(contributing - covered):
        count = sum(name in cand.sources for cand in state["candidates"])
        issues.append(
            f"Completeness: {count} candidate(s) from {name} are neither in any requirement's "
            "sources nor in discarded; restore or explicitly discard them."
        )

    return {"validation_issues": issues}


def review_requirements(state: NetworkState) -> dict[str, Review]:
    reviewer = make_model("review").with_structured_output(Review)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a strict requirements QA reviewer. Check the draft against the candidate "
                "source material for: duplicate or overlapping requirements; contradictory "
                "requirements; candidates whose meaning was dropped (neither merged nor "
                "discarded); missing traceability or priorities; vague names; explanations that "
                "are not a rationale paragraph; inconsistent terminology; vague discarded entries "
                "that do not name a specific candidate; and any wording that refers to earlier "
                "drafts or revisions. Approve only if it is consistent and complete enough to "
                "publish. List concrete repair instructions. " + STYLE_RULES,
            ),
            ("human", "Candidate source material:\n{candidates}\n\nDraft:\n{draft}"),
        ]
    )
    llm_review = (prompt | reviewer).invoke(
        {"candidates": _dump(state["candidates"]), "draft": state["draft"].model_dump()}
    )
    rule_issues = [f"[rule check] {issue}" for issue in state.get("validation_issues", [])]
    return {
        "review": Review(
            approved=llm_review.approved and not rule_issues,
            issues=rule_issues + llm_review.issues,
        )
    }


def route_review(state: NetworkState) -> str:
    review = state["review"]
    if review.approved or state.get("review_round", 0) >= MAX_REVIEW_ROUNDS:
        return "finalize"
    return "revise"


def revise_requirements(state: NetworkState) -> dict[str, object]:
    """Feed review findings back into the synthesis model."""
    synthesizer = make_model("synthesize").with_structured_output(RequirementDocument)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Revise this requirements document by fixing every QA issue. Use the original "
                "candidates to restore any dropped meaning. Keep valid content, deduplicate, "
                "preserve exact source filenames, and keep stable R-NNN IDs where possible. "
                "If you remove a requirement, record it in discarded with category, reason and "
                "sources. Output the final document as a standalone specification: never refer "
                "to earlier drafts, revisions, previous versions or changes (avoid words such as "
                "'remains', 'was removed', 'previously', 'no longer', 'upgraded'). "
                + STYLE_RULES,
            ),
            (
                "human",
                "Original candidates:\n{candidates}\n\nCurrent draft:\n{draft}\n\n"
                "QA issues:\n{issues}\n\nExtraction-stage discarded items (context only):\n{discarded}",
            ),
        ]
    )
    result = (prompt | synthesizer).invoke(
        {
            "candidates": _dump(state["candidates"]),
            "draft": state["draft"].model_dump(),
            "issues": state["review"].issues,
            "discarded": _dump(state.get("discarded", [])),
        }
    )
    return {"draft": result, "review_round": state.get("review_round", 0) + 1}


def finalize(state: NetworkState) -> dict[str, RequirementDocument]:
    """Deterministic node: merge extraction-stage and consolidation discards, deduplicated."""
    draft = state["draft"]
    merged: dict[tuple[str, str], DiscardedItem] = {}
    for item in [*draft.discarded, *state.get("discarded", [])]:
        key = (re.sub(r"\W+", " ", item.name).strip().lower(), item.category)
        if key in merged:
            existing = merged[key]
            sources = sorted(set(existing.sources) | set(item.sources))
            merged[key] = existing.model_copy(update={"sources": sources})
        else:
            merged[key] = item
    return {"final": draft.model_copy(update={"discarded": list(merged.values())})}


def build_network():
    graph = StateGraph(NetworkState)
    nodes = {
        "load_documents": load_documents,
        "extract_requirements": extract_requirements,
        "synthesize_requirements": synthesize_requirements,
        "validate_requirements": validate_requirements,
        "review_requirements": review_requirements,
        "revise_requirements": revise_requirements,
        "finalize": finalize,
    }
    for name, func in nodes.items():
        graph.add_node(name, tracked(name, func))
    graph.add_edge(START, "load_documents")
    graph.add_edge("load_documents", "extract_requirements")
    graph.add_edge("extract_requirements", "synthesize_requirements")
    graph.add_edge("synthesize_requirements", "validate_requirements")
    graph.add_edge("validate_requirements", "review_requirements")
    graph.add_conditional_edges("review_requirements", route_review, {"revise": "revise_requirements", "finalize": "finalize"})
    graph.add_edge("revise_requirements", "validate_requirements")
    graph.add_edge("finalize", END)
    return graph.compile()


CATEGORY_LABELS = {
    "conflicting": "Conflicting",
    "nonsensical": "Nonsensical",
    "out_of_scope": "Out of scope",
}


def render_markdown(document: RequirementDocument) -> str:
    lines = [
        f"# {document.title}",
        "",
        "## Priority scale",
        "- **Must**: essential for the system to meet its primary purpose.",
        "- **Should**: important, but can be deferred without invalidating the release.",
        "- **Could**: useful enhancement considered if capacity permits.",
        "- **Won't**: explicitly out of scope for this release.",
        "",
        "## Requirements",
    ]
    for requirement in document.requirements:
        lines.extend(
            [
                "",
                f"### {requirement.id}: {requirement.name}",
                f"**Priority:** {requirement.priority}",
                f"**Statement:** {requirement.statement}",
                "",
                requirement.explanation,
                "",
                "**Sources:** " + ", ".join(sorted(set(requirement.sources))),
            ]
        )

    rejected = [item for item in document.discarded if item.category != "non_requirement"]
    excluded = [item for item in document.discarded if item.category == "non_requirement"]

    lines.extend(["", "## Discarded requirements (blacklist)", ""])
    if rejected:
        for item in sorted(rejected, key=lambda i: (i.category, i.name.lower())):
            sources = ", ".join(sorted(set(item.sources))) or "n/a"
            lines.append(
                f"- **{item.name}** ({CATEGORY_LABELS[item.category]}): {item.reason} "
                f"*Sources: {sources}*"
            )
    else:
        lines.append("- None.")

    lines.extend(["", "## Excluded non-requirement content", ""])
    if excluded:
        for item in sorted(excluded, key=lambda i: (sorted(i.sources), i.name.lower())):
            sources = ", ".join(sorted(set(item.sources))) or "n/a"
            lines.append(f"- **{item.name}**: {item.reason} *Sources: {sources}*")
    else:
        lines.append("- None.")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_directory", type=Path)
    parser.add_argument("output_file", type=Path)
    args = parser.parse_args(argv)

    PROGRESS.start()
    try:
        result = build_network().invoke({"input_dir": str(args.input_directory)})
    finally:
        elapsed = PROGRESS.stop()

    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    args.output_file.write_text(render_markdown(result["final"]), encoding="utf-8")
    print(f"\nWrote {args.output_file} from {len(result['documents'])} source documents "
          f"in {Progress.fmt(elapsed)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())