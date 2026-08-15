"""Tool use: the model chooses tools, we execute them, then it answers."""

from __future__ import annotations

import json
from typing import Any

from langfuse import get_client, observe, propagate_attributes
from langfuse.openai import openai
from pydantic import BaseModel

from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import POLICY
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL
from sd_agentic_shared.tools import OPENAI_TOOLS, call_tool

load_env()

MAX_STEPS = 6

SYSTEM = f"""You are a support agent with tools. Use tools before claiming facts.
{POLICY}
If lookup_order fails, say you could not find the order. Never invent tracking.
If create_refund is refused, tell the customer a human must approve it."""


class ToolCallRecord(BaseModel):
    name: str
    arguments: dict[str, Any]
    result: str


class ToolUseResult(BaseModel):
    calls: list[ToolCallRecord]
    reply: str


@observe(as_type="tool", name="tool.execute")
def execute_tool(name: str, arguments: dict[str, Any]) -> str:
    return call_tool(name, arguments)


@observe(name="pattern.tool_use")
def run(email: str) -> ToolUseResult:
    with propagate_attributes(
        tags=["backend:scratch", "pattern:tool_use"],
        metadata={"pattern": "tool_use", "backend": "scratch"},
    ):
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": email},
        ]
        calls: list[ToolCallRecord] = []
        reply = ""

        for _ in range(MAX_STEPS):
            response = openai.chat.completions.create(
                model=openai_model(),
                messages=messages,
                tools=OPENAI_TOOLS,
            )
            message = response.choices[0].message
            assistant: dict[str, Any] = {"role": "assistant", "content": message.content}
            if message.tool_calls:
                assistant["tool_calls"] = [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                    for tool_call in message.tool_calls
                ]
            messages.append(assistant)

            if not message.tool_calls:
                reply = message.content or ""
                break

            for tool_call in message.tool_calls:
                name = tool_call.function.name
                try:
                    arguments = json.loads(tool_call.function.arguments or "{}")
                except json.JSONDecodeError:
                    arguments = {}
                result = execute_tool(name, arguments)
                calls.append(ToolCallRecord(name=name, arguments=arguments, result=result))
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )
        else:
            reply = "Stopped: too many tool steps."

        return ToolUseResult(calls=calls, reply=reply)


def main() -> None:
    print(run(SUPPORT_EMAIL).model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
