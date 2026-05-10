"""Step 0 of the masterclass: a baseline chatbot.

This is the *before* picture. It demonstrates that the OpenAI client is
working, but it has no tools, no memory beyond a single turn, and no loop.
It is NOT an agent. The next file (`agent_v1_tools.py`) turns it into one.
"""
from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

from .llm import make_client, model_name

load_dotenv()

MODEL = os.environ.get("MODEL", "openai/gpt-4o-mini")


def chat(user_message: str) -> str:
    """Send a single message to the LLM and return the reply."""
    client = make_client(MODEL)
    response = client.chat.completions.create(
        model=model_name(MODEL),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Hello! Briefly, who are you?"
    print(chat(question))
