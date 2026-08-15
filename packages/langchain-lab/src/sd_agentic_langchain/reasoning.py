"""Reasoning: LangGraph CoT sample loop then pick a reply."""

from __future__ import annotations

import json
from typing import Any, Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langfuse import get_client, observe, propagate_attributes
from langfuse.langchain import CallbackHandler
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import REASONING_SYSTEM
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()

N_SAMPLES = 2


class ReasoningSample(BaseModel):
    steps: list[str]
    reply: str


class ReasoningResult(BaseModel):
    samples: list[ReasoningSample]
    reply: str


class ReasoningState(TypedDict):
    email: str
    samples: list[dict[str, Any]]
    reply: str


def _llm() -> ChatOpenAI:
    return ChatOpenAI(model=openai_model(), temperature=0.7)


def _complete(system: str, user: str) -> str:
    message = _llm().invoke(
        [SystemMessage(content=system), HumanMessage(content=user)]
    )
    content = message.content
    return content if isinstance(content, str) else str(content or "")


def _extract_json(text: str) -> dict[str, Any]:
    raw = text.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("no JSON object in model output")
    parsed = json.loads(raw[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("JSON root must be an object")
    return parsed


def _parse_sample(raw: str) -> ReasoningSample:
    try:
        payload = _extract_json(raw)
        steps = [str(item).strip() for item in (payload.get("steps") or []) if str(item).strip()]
        reply = str(payload.get("reply") or "").strip()
        if not steps:
            steps = ["parse produced no steps"]
        if not reply:
            reply = raw.strip()
        return ReasoningSample(steps=steps, reply=reply)
    except (ValueError, json.JSONDecodeError, TypeError):
        return ReasoningSample(steps=["fallback: unparseable CoT"], reply=raw.strip())


def sample_node(state: ReasoningState) -> dict[str, Any]:
    sample = _parse_sample(_complete(REASONING_SYSTEM, state["email"]))
    samples = list(state["samples"]) + [sample.model_dump()]
    return {"samples": samples, "reply": samples[0]["reply"]}


def after_sample(state: ReasoningState) -> Literal["sample", "end"]:
    return "end" if len(state["samples"]) >= N_SAMPLES else "sample"


def build_graph():
    graph = StateGraph(ReasoningState)
    graph.add_node("sample", sample_node)
    graph.add_edge(START, "sample")
    graph.add_conditional_edges(
        "sample",
        after_sample,
        {"sample": "sample", "end": END},
    )
    return graph.compile()


@observe(name="pattern.reasoning")
def run(email: str | None = None) -> ReasoningResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    with propagate_attributes(
        tags=["backend:langchain", "pattern:reasoning"],
        metadata={"pattern": "reasoning", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        result = build_graph().invoke(
            {"email": ticket, "samples": [], "reply": ""},
            config={"callbacks": [handler]},
        )
        return ReasoningResult(
            samples=[ReasoningSample.model_validate(item) for item in result["samples"]],
            reply=result["reply"],
        )


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
