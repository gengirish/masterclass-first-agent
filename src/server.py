"""Minimal FastAPI server that wraps the agent.

This is the file Fly.io serves in production. Keep it tiny - the
real logic lives in `agent_v2_rag.run_agent`.

If you get stuck, peek at `reference/solutions/server.py`.
"""
from __future__ import annotations

import logging
import os

import chromadb
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .agent_v2_rag import CHROMA_DIR, COLLECTION_NAME, run_agent

logger = logging.getLogger(__name__)

app = FastAPI(title="My First Agent", version="0.1.0")


@app.on_event("startup")
def _configure_logging() -> None:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

_DEFAULT_ORIGINS = [
    "https://upskill.intelliforge.tech",
    "https://masterclass-first-agent.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

_extra = os.getenv("CORS_ALLOWED_ORIGINS", "")
ALLOWED_ORIGINS = _DEFAULT_ORIGINS + [
    o.strip() for o in _extra.split(",") if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.intelliforge\.tech",
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    max_iterations: int = Field(default=4, ge=1, le=8)


class AskResponse(BaseModel):
    question: str
    answer: str


class HealthResponse(BaseModel):
    status: str
    service: str
    chroma_ready: bool
    doc_chunks: int | None = None


def _chroma_status() -> tuple[bool, int | None]:
    """Return whether the RAG index is present and how many chunks it holds."""
    if not CHROMA_DIR.is_dir():
        return False, None
    try:
        chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))
        collection = chroma.get_collection(COLLECTION_NAME)
        return True, collection.count()
    except Exception:
        return False, None


@app.get("/")
def root() -> dict[str, str]:
    """Lightweight liveness probe."""
    return {"status": "ok", "service": "my-first-agent"}


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Readiness probe — verifies the Chroma index is mounted."""
    chroma_ready, doc_chunks = _chroma_status()
    status = "ok" if chroma_ready else "degraded"
    return HealthResponse(
        status=status,
        service="my-first-agent",
        chroma_ready=chroma_ready,
        doc_chunks=doc_chunks,
    )


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    """Run the agent on the user's question and return the final answer."""
    chroma_ready, _ = _chroma_status()
    if not chroma_ready:
        logger.error("ask rejected: Chroma index missing at %s", CHROMA_DIR)
        raise HTTPException(
            status_code=503,
            detail="Knowledge base is not ready. Re-run ingest and redeploy.",
        )

    try:
        answer = run_agent(req.question, max_iterations=req.max_iterations)
    except Exception:
        logger.exception("agent failed for question=%r", req.question[:80])
        raise HTTPException(
            status_code=500,
            detail="Agent failed to produce an answer. Try again in a moment.",
        ) from None

    return AskResponse(question=req.question, answer=answer)
