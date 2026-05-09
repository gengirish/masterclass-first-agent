"""One-shot ingest: read every doc under data/ and embed it into ChromaDB.

Run once before using `agent_v2_rag.py` or hitting `/ask` on the server.

    uv run python -m scripts.ingest
"""
from __future__ import annotations

from pathlib import Path

from src.agent_v2_rag import ingest_pdf

DATA_DIR = Path("data")
SUPPORTED_SUFFIXES = {".pdf", ".md", ".txt"}


def main() -> None:
    if not DATA_DIR.exists():
        raise SystemExit(f"data/ folder not found at {DATA_DIR.resolve()}")

    docs = sorted(p for p in DATA_DIR.iterdir() if p.suffix.lower() in SUPPORTED_SUFFIXES)
    if not docs:
        raise SystemExit(
            f"No supported docs ({', '.join(SUPPORTED_SUFFIXES)}) found in {DATA_DIR.resolve()}"
        )

    total_chunks = 0
    for doc in docs:
        total_chunks += ingest_pdf(doc)

    print(f"\nDone. {len(docs)} doc(s), {total_chunks} chunks total.")


if __name__ == "__main__":
    main()
