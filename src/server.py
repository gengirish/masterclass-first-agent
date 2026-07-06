"""Minimal FastAPI server that wraps the agent.

This is the file Fly.io serves in production. Keep it tiny - the
real logic lives in `agent_v2_rag.run_agent`.

If you get stuck, peek at `reference/solutions/server.py`.
"""
from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .agent_v2_rag import run_agent

app = FastAPI(title="My First Agent", version="0.1.0")

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
    question: str
    max_iterations: int = 4


class AskResponse(BaseModel):
    question: str
    answer: str


@app.get("/")
def root() -> dict[str, str]:
    """Health check. Returns 200 OK if the service is up."""
    return {"status": "ok", "service": "my-first-agent"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    """Run the agent on the user's question and return the final answer."""
    answer = run_agent(req.question, max_iterations=req.max_iterations)
    return AskResponse(question=req.question, answer=answer)
