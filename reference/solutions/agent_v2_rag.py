"""Reference solution for `src/agent_v2_rag.py`.

The skeleton in `src/agent_v2_rag.py` is already complete (because the
loop is identical to Step 1). This file exists as the canonical reference
in case you want a side-by-side reading.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

from src.tools import TOOLS, dispatch_tool

load_dotenv()

MODEL = os.environ.get("MODEL", "gpt-4o-mini")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "text-embedding-3-small")
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
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix in {".md", ".txt"}:
        return path.read_text(encoding="utf-8")
    raise ValueError(f"Unsupported file type: {suffix}")


def ingest_pdf(doc_path: Path) -> int:
    full_text = _read_doc(doc_path)
    chunks = chunk_text(full_text)

    client = OpenAI()
    response = client.embeddings.create(model=EMBED_MODEL, input=chunks)
    vectors = [e.embedding for e in response.data]

    chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = chroma.get_or_create_collection(COLLECTION_NAME)
    collection.upsert(
        ids=[f"chunk-{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=vectors,
        metadatas=[{"source": doc_path.name, "chunk_index": i} for i in range(len(chunks))],
    )
    return len(chunks)


def run_agent(user_message: str, max_iterations: int = 6) -> str:
    client = OpenAI()
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for iteration in range(max_iterations):
        print(f"\n--- iteration {iteration + 1} ---")
        response = client.chat.completions.create(
            model=MODEL,
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
