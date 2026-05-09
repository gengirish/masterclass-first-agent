"""Tools available to the agent.

Each tool is a regular Python function. We also expose a JSON-Schema
description (`TOOLS`) so the LLM can decide *when* to call which tool.

The single most underrated piece of agent engineering is the `description`
field of each tool - the LLM reads it like API docs. Vague description,
dumb agent. Specific description, smart agent.
"""
from __future__ import annotations

import json
from typing import Any

from simpleeval import simple_eval


def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression safely.

    Uses `simpleeval` instead of Python's built-in `eval` so the LLM
    cannot smuggle arbitrary code through this tool.
    """
    try:
        result = simple_eval(expression)
        return str(result)
    except Exception as exc:
        return f"ERROR: could not evaluate `{expression}`: {exc}"


def web_search(query: str) -> str:
    """Stub web search. Replace with a real provider (Tavily, Serper, Bing) later.

    For the masterclass we keep this offline so we don't need extra API keys.
    """
    canned = {
        "openai": "OpenAI is an AI research company. ChatGPT was launched in Nov 2022.",
        "intelliforge": "IntelliForge is an AI engineering bootcamp run by Girish Hiremath.",
        "fly.io": "Fly.io runs containers close to users. Free tier supports small apps.",
    }
    q = query.lower()
    for key, value in canned.items():
        if key in q:
            return f"[stub web result for '{query}']\n{value}"
    return (
        f"[stub web result for '{query}']\n"
        "No canned result found. In production, plug in Tavily / Serper / Bing here."
    )


def search_docs(query: str, k: int = 3) -> str:
    """Search the ingested IntelliForge docs and return the top-k matching chunks.

    Used by `agent_v2_rag.py` (Hour 2 Step 2). Requires that you've run
    `python -m scripts.ingest` first to populate the Chroma collection.
    """
    import chromadb
    from openai import OpenAI

    client = OpenAI()
    embedding = (
        client.embeddings.create(model="text-embedding-3-small", input=[query])
        .data[0]
        .embedding
    )

    chroma = chromadb.PersistentClient(path=".chroma")
    try:
        collection = chroma.get_collection("intelliforge-docs")
    except Exception:
        return (
            "ERROR: docs collection not found. "
            "Run `uv run python -m scripts.ingest` first."
        )

    results = collection.query(query_embeddings=[embedding], n_results=k)
    chunks = results["documents"][0] if results["documents"] else []

    if not chunks:
        return f"No matching docs found for '{query}'."

    return "\n\n---\n\n".join(
        f"[chunk {i + 1}]\n{chunk}" for i, chunk in enumerate(chunks)
    )


def dispatch_tool(name: str, args: dict[str, Any]) -> str:
    """Look up the named tool and call it with the given arguments."""
    if name == "calculator":
        return calculator(**args)
    if name == "web_search":
        return web_search(**args)
    if name == "search_docs":
        return search_docs(**args)
    return f"ERROR: unknown tool '{name}'"


TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "Evaluate a basic arithmetic expression. "
                "Use this for any numeric calculation - percentages, "
                "ratios, sums, products. Example expression: '0.17 * 4829'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "A Python-style arithmetic expression. "
                            "Supports +, -, *, /, **, parentheses."
                        ),
                    },
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the web for general knowledge questions whose answers "
                "may have changed recently or are outside your training data. "
                "Returns a short text summary."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The natural-language search query.",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_docs",
            "description": (
                "Search the IntelliForge documentation. Use this whenever the "
                "user asks a question that might be answered by company docs, "
                "FAQs, bootcamp pricing, course content, or product details."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The natural-language question to search for.",
                    },
                    "k": {
                        "type": "integer",
                        "description": "Number of top chunks to return (default 3).",
                        "default": 3,
                    },
                },
                "required": ["query"],
            },
        },
    },
]


if __name__ == "__main__":
    print("Available tools:")
    for tool in TOOLS:
        print(f"  - {tool['function']['name']}: {tool['function']['description'][:80]}...")
    print("\nSmoke test - calculator(17 * 4829 / 100):")
    print(" ", calculator("17 * 4829 / 100"))
    print("\nSchema (JSON):")
    print(json.dumps(TOOLS[0], indent=2))
