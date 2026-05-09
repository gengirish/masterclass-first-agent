"""Step 1 of the masterclass agent: tool calling + memory.

You will fill in the four TODO blocks during the live session.
If you get stuck, peek at `reference/solutions/agent_v1_tools.py`.
"""
from __future__ import annotations

import json
import os
import sys
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from .tools import TOOLS, dispatch_tool

load_dotenv()

MODEL = os.environ.get("MODEL", "gpt-4o-mini")
SYSTEM_PROMPT = (
    "You are a careful research assistant. "
    "Think step by step. When a question requires a calculation or a web "
    "lookup, use the appropriate tool instead of guessing. "
    "If a tool returns an error, try a different approach. "
    "Cite the tool you used in your final answer."
)


def run_agent(user_message: str, max_iterations: int = 6) -> str:
    """Run the agent loop until it returns a final answer or budget runs out."""
    client = OpenAI()

    # TODO 1 - initialize messages with the system prompt and the user's question.
    # Hint: messages is a list of dicts. Each dict has a "role" and "content" key.
    messages: list[dict[str, Any]] = ...  # replace this

    for iteration in range(max_iterations):
        print(f"\n--- iteration {iteration + 1} ---")

        # TODO 2 - call the LLM with the tools registered.
        # Hint: client.chat.completions.create(model=..., messages=..., tools=TOOLS, tool_choice="auto")
        response = ...  # replace this

        choice = response.choices[0].message
        messages.append(choice.model_dump(exclude_none=True))

        # TODO 3 - if the LLM wants to call a tool, run it and loop back.
        # Hint: choice.tool_calls is a list. Each item has .id, .function.name,
        # .function.arguments (a JSON string). Use dispatch_tool(name, args).
        # Append a {"role": "tool", "tool_call_id": ..., "name": ..., "content": ...}
        # message for each tool call, then `continue`.
        if choice.tool_calls:
            ...  # replace this
            continue

        # TODO 4 - no more tool calls => the LLM is done. Return its text.
        return choice.content or ""

    return "Agent ran out of iterations without producing a final answer."


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "What is 17% of 4,829? Then briefly explain why."
    print("\nFINAL ANSWER:\n", run_agent(question))
