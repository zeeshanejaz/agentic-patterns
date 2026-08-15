"""Human-in-the-loop: LangGraph interrupt at the refund gate, then resume."""

from __future__ import annotations

import json
import re
from typing import Any, Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langfuse import get_client, observe, propagate_attributes
from langfuse.langchain import CallbackHandler
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
from pydantic import BaseModel

from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import (
    DRAFT_SYSTEM,
    HITL_GATE_SYSTEM,
    HITL_RESUME_SYSTEM,
    SUMMARIZE_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import HITL_DECISION, SUPPORT_EMAIL, HITLDecision

load_env()


class GateResult(BaseModel):
    risk: str
    reason: str
    needs_human: bool


class HITLResult(BaseModel):
    summary: str
    draft: str
    gate: GateResult
    decision: HITLDecision | None
    reply: str
    interrupted: bool


class HITLState(TypedDict):
    email: str
    summary: str
    draft: str
    gate: dict[str, Any]
    decision: dict[str, Any]
    reply: str
    interrupted: bool


def _llm() -> ChatOpenAI:
    return ChatOpenAI(model=openai_model())


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


def _refund_over_50(text: str) -> bool:
    blob = text.lower()
    if "refund" not in blob and "chargeback" not in blob:
        return False
    for match in re.findall(r"\$(\d+(?:\.\d+)?)", blob):
        if float(match) > 50:
            return True
    return "full refund" in blob


def _parse_gate(email: str, draft: str, raw: str) -> GateResult:
    try:
        payload = _extract_json(raw)
        risk = str(payload.get("risk") or "high").strip().lower()
        if risk not in {"high", "medium", "low"}:
            risk = "high"
        reason = str(payload.get("reason") or "").strip()
        needs_human = bool(payload.get("needs_human"))
    except (ValueError, json.JSONDecodeError, TypeError):
        risk, reason, needs_human = "high", "gate parse failed", True
    if _refund_over_50(email) or _refund_over_50(draft):
        needs_human = True
        if not reason:
            reason = "refund over $50 requires a human"
        risk = "high"
    return GateResult(risk=risk, reason=reason, needs_human=needs_human)


def summarize_node(state: HITLState) -> dict[str, str]:
    return {"summary": _complete(SUMMARIZE_SYSTEM, state["email"])}


def draft_node(state: HITLState) -> dict[str, str]:
    user = f"Original email:\n{state['email']}\n\nFact summary:\n{state['summary']}"
    return {"draft": _complete(DRAFT_SYSTEM, user)}


def gate_node(state: HITLState) -> dict[str, Any]:
    raw = _complete(
        HITL_GATE_SYSTEM,
        f"Email:\n{state['email']}\n\nDraft:\n{state['draft']}",
    )
    gate = _parse_gate(state["email"], state["draft"], raw)
    return {"gate": gate.model_dump(), "interrupted": gate.needs_human}


def human_node(state: HITLState) -> dict[str, Any]:
    payload = interrupt(
        {
            "email": state["email"],
            "summary": state["summary"],
            "draft": state["draft"],
            "gate": state["gate"],
        }
    )
    if isinstance(payload, dict):
        decision = payload
    else:
        decision = HITL_DECISION.model_dump()
    return {"decision": decision, "interrupted": True}


def resume_node(state: HITLState) -> dict[str, str]:
    decision = HITLDecision.model_validate(state["decision"])
    action = decision.action.strip().lower()
    if action == "edit" and decision.edited_reply.strip():
        return {"reply": decision.edited_reply.strip()}
    user = (
        f"Action: {action}\nNote: {decision.note}\n\n"
        f"Edited text:\n{decision.edited_reply or '(none)'}\n\n"
        f"Draft:\n{state['draft']}\n\nEmail:\n{state['email']}"
    )
    return {"reply": _complete(HITL_RESUME_SYSTEM, user)}


def after_gate(state: HITLState) -> Literal["human", "auto"]:
    return "human" if state["gate"].get("needs_human") else "auto"


def auto_node(state: HITLState) -> dict[str, Any]:
    return {"reply": state["draft"], "interrupted": False, "decision": {}}


def build_graph():
    graph = StateGraph(HITLState)
    graph.add_node("summarize", summarize_node)
    graph.add_node("draft", draft_node)
    graph.add_node("gate", gate_node)
    graph.add_node("human", human_node)
    graph.add_node("resume", resume_node)
    graph.add_node("auto", auto_node)
    graph.add_edge(START, "summarize")
    graph.add_edge("summarize", "draft")
    graph.add_edge("draft", "gate")
    graph.add_conditional_edges(
        "gate",
        after_gate,
        {"human": "human", "auto": "auto"},
    )
    graph.add_edge("human", "resume")
    graph.add_edge("resume", END)
    graph.add_edge("auto", END)
    return graph.compile(checkpointer=MemorySaver())


@observe(name="pattern.human_in_the_loop")
def run(email: str | None = None) -> HITLResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    with propagate_attributes(
        tags=["backend:langchain", "pattern:human_in_the_loop"],
        metadata={"pattern": "human_in_the_loop", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        config = {
            "callbacks": [handler],
            "configurable": {"thread_id": "hitl-support-email"},
        }
        graph = build_graph()
        result = graph.invoke(
            {
                "email": ticket,
                "summary": "",
                "draft": "",
                "gate": {},
                "decision": {},
                "reply": "",
                "interrupted": False,
            },
            config=config,
        )
        if result.get("__interrupt__") or (
            result.get("interrupted") and not result.get("reply")
        ):
            result = graph.invoke(
                Command(resume=HITL_DECISION.model_dump()),
                config=config,
            )
        gate = GateResult.model_validate(result["gate"])
        raw_decision = result.get("decision") or None
        decision = (
            HITLDecision.model_validate(raw_decision)
            if raw_decision
            else None
        )
        return HITLResult(
            summary=result["summary"],
            draft=result["draft"],
            gate=gate,
            decision=decision,
            reply=result["reply"],
            interrupted=bool(result.get("interrupted")),
        )


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
