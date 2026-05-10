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

from .llm import make_client, model_name
from .tools import TOOLS, dispatch_tool

load_dotenv()

MODEL = os.environ.get("MODEL", "openai/gpt-4o-mini")
SYSTEM_PROMPT = (
    "You are a careful research assistant. "
    "Think step by step. When a question requires a calculation or a web "
    "lookup, use the appropriate tool instead of guessing. "
    "If a tool returns an error, try a different approach. "
    "Cite the tool you used in your final answer."
)


def run_agent(user_message: str, max_iterations: int = 6) -> str:
    """Run the agent loop until it returns a final answer or budget runs out."""
    client = make_client(MODEL)

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for iteration in range(max_iterations):
        print(f"\n--- iteration {iteration + 1} ---")

        response = client.chat.completions.create(
            model=model_name(MODEL),
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
    question = " ".join(sys.argv[1:]) or "What is 17% of 4,829? Then briefly explain why."
    print("\nFINAL ANSWER:\n", run_agent(question))
