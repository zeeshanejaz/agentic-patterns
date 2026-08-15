"""Tool use via MCP discovery instead of a hardcoded OpenAI tool list."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from fastmcp import Client
from langfuse import get_client, observe, propagate_attributes
from langfuse.openai import openai
from pydantic import BaseModel

from sd_agentic_mcp.demo import _schema, _text
from sd_agentic_mcp.server import SUPPORT_AGENT_PROMPT, create_server
from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()

MAX_STEPS = 6


class ToolCallRecord(BaseModel):
    name: str
    arguments: dict[str, Any]
    result: str


class ToolUseResult(BaseModel):
    calls: list[ToolCallRecord]
    reply: str


def _openai_tools(mcp_tools: list) -> list[dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": _schema(tool) or {"type": "object", "properties": {}},
            },
        }
        for tool in mcp_tools
    ]


@observe(as_type="tool", name="mcp.call_tool")
async def execute_mcp_tool(client: Client, name: str, arguments: dict[str, Any]) -> str:
    result = await client.call_tool(name, arguments)
    return _text(result)


@observe(name="pattern.mcp_tool_use")
async def run(email: str) -> ToolUseResult:
    with propagate_attributes(
        tags=["backend:mcp", "pattern:tool_use"],
        metadata={"pattern": "model_context_protocol", "backend": "mcp"},
    ):
        server = create_server()
        async with Client(server) as client:
            mcp_tools = await client.list_tools()
            openai_tools = _openai_tools(mcp_tools)
            messages: list[dict[str, Any]] = [
                {"role": "system", "content": SUPPORT_AGENT_PROMPT},
                {"role": "user", "content": email},
            ]
            calls: list[ToolCallRecord] = []
            reply = ""

            for _ in range(MAX_STEPS):
                response = openai.chat.completions.create(
                    model=openai_model(),
                    messages=messages,
                    tools=openai_tools,
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
                    result = await execute_mcp_tool(client, name, arguments)
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
    print(asyncio.run(run(SUPPORT_EMAIL)).model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
