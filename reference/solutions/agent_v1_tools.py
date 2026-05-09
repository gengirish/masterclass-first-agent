"""Reference solution for `src/agent_v1_tools.py`.

This is the same file with all four TODOs filled in. Compare against your
own work - line shapes should match closely. Don't run this in place of
the skeleton during the live session; the point is to type it yourself.
"""
from __future__ import annotations

import json
import os
import sys
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from src.tools import TOOLS, dispatch_tool

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

    # TODO 1 - initialize messages.
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for iteration in range(max_iterations):
        print(f"\n--- iteration {iteration + 1} ---")

        # TODO 2 - call the LLM with tools.
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        choice = response.choices[0].message
        messages.append(choice.model_dump(exclude_none=True))

        # TODO 3 - run tool calls and loop back.
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

        # TODO 4 - return the final answer.
        return choice.content or ""

    return "Agent ran out of iterations without producing a final answer."


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "What is 17% of 4,829? Then briefly explain why."
    print("\nFINAL ANSWER:\n", run_agent(question))
