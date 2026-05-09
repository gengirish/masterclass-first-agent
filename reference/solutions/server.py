"""Reference copy of `src/server.py`. Identical - the skeleton is already complete."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.agent_v2_rag import run_agent

app = FastAPI(title="My First Agent", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return {"status": "ok", "service": "my-first-agent"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    answer = run_agent(req.question, max_iterations=req.max_iterations)
    return AskResponse(question=req.question, answer=answer)
