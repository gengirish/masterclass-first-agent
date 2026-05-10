"""Step 2 of the masterclass agent: add a RAG layer with ChromaDB.

We reuse `run_agent` from `agent_v1_tools.py` because the agent loop is
identical. The only thing that changes is:

  1. The system prompt now tells the agent to ground its answers in docs.
  2. The `search_docs` tool is already registered in `tools.py`.
  3. We expose an `ingest_pdf` helper that chunks + embeds a PDF or
     Markdown file into Chroma.

Run `uv run python -m scripts.ingest` once to populate Chroma, then ask
the agent questions about the document.

If you get stuck, peek at `reference/solutions/agent_v2_rag.py`.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import chromadb
from dotenv import load_dotenv
from pypdf import PdfReader

from .llm import embed, make_client, model_name
from .tools import TOOLS, dispatch_tool

load_dotenv()

MODEL = os.environ.get("MODEL", "openai/gpt-4o-mini")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "openai/text-embedding-3-small")
COLLECTION_NAME = "intelliforge-docs"
CHROMA_DIR = Path(".chroma")

SYSTEM_PROMPT = (
    "You are the IntelliForge documentation assistant. "
    "When the user asks anything about IntelliForge, the bootcamp, pricing, "
    "or course content, ALWAYS call `search_docs` first to ground your answer "
    "in real documentation. If the docs don't contain the answer, say so. "
    "Cite which chunk you used."
)


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    """Sliding-window character chunking. Good enough for short docs."""
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def _read_doc(path: Path) -> str:
    """Read a .pdf, .md, or .txt file and return its plain text."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix in {".md", ".txt"}:
        return path.read_text(encoding="utf-8")
    raise ValueError(f"Unsupported file type: {suffix}")


def ingest_pdf(doc_path: Path) -> int:
    """Read a doc, chunk it, embed each chunk, write to Chroma. Returns chunk count."""
    print(f"Ingesting {doc_path}...")
    full_text = _read_doc(doc_path)
    chunks = chunk_text(full_text)
    print(f"  -> {len(chunks)} chunks")

    client = make_client(EMBED_MODEL)
    vectors = embed(client, EMBED_MODEL, chunks, kind="passage")

    chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = chroma.get_or_create_collection(COLLECTION_NAME)
    collection.upsert(
        ids=[f"chunk-{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=vectors,
        metadatas=[{"source": doc_path.name, "chunk_index": i} for i in range(len(chunks))],
    )
    print(f"  -> wrote {len(chunks)} chunks to Chroma at {CHROMA_DIR}")
    return len(chunks)


# Re-export run_agent for `python -m src.agent_v2_rag "..."` and the FastAPI server.
# The skeleton intentionally re-implements it here so students see the same loop
# from Step 1 but with the doc-grounded SYSTEM_PROMPT.
def run_agent(user_message: str, max_iterations: int = 6) -> str:
    """Run the RAG-augmented agent loop. Same shape as Step 1."""
    import json

    client = make_client(MODEL)
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for iteration in range(max_iterations):
        print(f"\n--- iteration {iteration + 1} ---")

        response = client.chat.completions.create(
            model=model_name(MODEL),
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )
        choice = response.choices[0].message
        messages.append(choice.model_dump(exclude_none=True))

        if choice.tool_calls:
            for tool_call in choice.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                print(f"  -> tool: {name}({args})")
                result = dispatch_tool(name, args)
                preview = result[:120] + ("..." if len(result) > 120 else "")
                print(f"  <- result: {preview}")
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": result,
                    }
                )
            continue

        return choice.content or ""

    return "Agent ran out of iterations without producing a final answer."


if __name__ == "__main__":
    question = (
        " ".join(sys.argv[1:])
        or "How long is the IntelliForge bootcamp and what does it cost?"
    )
    print("\nFINAL ANSWER:\n", run_agent(question))
