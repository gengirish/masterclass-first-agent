"""End-to-end smoke test for every provider wired into src/llm.py.

Run with::

    uv run python -m scripts.smoke_test

Exits 0 if all paths green, 1 otherwise.
"""
from __future__ import annotations

import os
import sys
import time

from dotenv import load_dotenv

load_dotenv()


def banner(label: str) -> None:
    print(f"\n=== {label} ".ljust(64, "="))


def time_call(fn):
    t0 = time.perf_counter()
    result = fn()
    dt = (time.perf_counter() - t0) * 1000
    return result, dt


def test_chat(model_slug: str) -> tuple[bool, str]:
    from src.llm import make_client, model_name

    try:
        client = make_client(model_slug)
        response, dt = time_call(lambda: client.chat.completions.create(
            model=model_name(model_slug),
            messages=[{"role": "user", "content": "Reply with just one word: pong."}],
            max_tokens=8,
        ))
        text = (response.choices[0].message.content or "").strip()
        return True, f"OK in {dt:6.0f} ms -> {text!r}  (model: {response.model})"
    except Exception as exc:
        return False, f"FAIL -> {type(exc).__name__}: {exc}"


def test_embed(model_slug: str, kind: str = "passage") -> tuple[bool, str]:
    from src.llm import embed, make_client

    try:
        client = make_client(model_slug)
        vectors, dt = time_call(lambda: embed(client, model_slug, ["pong"], kind=kind))
        return True, f"OK in {dt:6.0f} ms -> dim {len(vectors[0])}"
    except Exception as exc:
        return False, f"FAIL -> {type(exc).__name__}: {exc}"


def test_tavily() -> tuple[bool, str]:
    from src.tools import web_search

    if not os.environ.get("TAVILY_API_KEY"):
        return False, "SKIP -> TAVILY_API_KEY not set"
    try:
        result, dt = time_call(lambda: web_search("What is the IntelliForge bootcamp?"))
        snippet = result[:140].replace("\n", " ")
        return True, f"OK in {dt:6.0f} ms -> {snippet!r}..."
    except Exception as exc:
        return False, f"FAIL -> {type(exc).__name__}: {exc}"


def main() -> int:
    failures: list[str] = []

    cases_chat = [
        ("OpenRouter chat (default)", "openai/gpt-4o-mini"),
        ("Groq chat",                  "groq:llama-3.3-70b-versatile"),
        ("NIM chat",                   "nim:meta/llama-3.3-70b-instruct"),
    ]
    cases_embed = [
        ("OpenRouter embed", "openai/text-embedding-3-small", "passage"),
        ("NIM embed",        "nim:nvidia/nv-embedqa-e5-v5",   "query"),
    ]

    banner("CHAT")
    for label, slug in cases_chat:
        ok, msg = test_chat(slug)
        print(f"  {label:30s} {msg}")
        if not ok:
            failures.append(label)

    banner("EMBEDDINGS")
    for label, slug, kind in cases_embed:
        ok, msg = test_embed(slug, kind)
        print(f"  {label:30s} {msg}")
        if not ok:
            failures.append(label)

    banner("WEB SEARCH (Tavily)")
    ok, msg = test_tavily()
    print(f"  {'Tavily search':30s} {msg}")
    if not ok and "SKIP" not in msg:
        failures.append("Tavily")

    banner("SUMMARY")
    if failures:
        print(f"  FAILED: {', '.join(failures)}")
        return 1
    print("  all green.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
