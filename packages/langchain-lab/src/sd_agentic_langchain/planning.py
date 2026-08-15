"""Planning: LangGraph plan → execute-step → optional replan cycle."""

from __future__ import annotations

import json
from typing import Any, Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langfuse import get_client, observe, propagate_attributes
from langfuse.langchain import CallbackHandler
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import (
    PLAN_REPAIR_SYSTEM,
    PLAN_REPLAN_SYSTEM,
    PLAN_STEP_SYSTEM,
    PLAN_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL
from sd_agentic_shared.tools import TOOL_IMPLS, call_tool

load_env()

MAX_REPLANS = 1
ALLOWED_TOOLS = tuple(TOOL_IMPLS)


class PlanStep(BaseModel):
    id: str
    instruction: str
    tool: str | None = None
    arguments: dict[str, Any] = Field(default_factory=dict)
    depends_on: list[str] = Field(default_factory=list)


class Plan(BaseModel):
    goal: str
    steps: list[PlanStep]


class StepResult(BaseModel):
    id: str
    status: str
    output: str


class PlanningResult(BaseModel):
    plan: Plan
    execution: list[StepResult]
    replans: int
    reply: str


class PlanningState(TypedDict):
    email: str
    plan: dict[str, Any]
    steps: list[dict[str, Any]]
    queue: list[dict[str, Any]]
    execution: list[dict[str, Any]]
    replans: int
    reply: str


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


def _normalize_tool(value: object) -> str | None:
    if value is None:
        return None
    name = str(value).strip().lower()
    if name in {"", "null", "none", "llm"}:
        return None
    return name if name in ALLOWED_TOOLS else None


def _plan_from_payload(payload: dict[str, Any]) -> Plan:
    steps_raw = payload.get("steps") or []
    steps: list[PlanStep] = []
    for item in steps_raw:
        if not isinstance(item, dict):
            continue
        steps.append(
            PlanStep(
                id=str(item.get("id") or f"s{len(steps) + 1}"),
                instruction=str(item.get("instruction") or ""),
                tool=_normalize_tool(item.get("tool")),
                arguments=dict(item.get("arguments") or {}),
                depends_on=[str(dep) for dep in (item.get("depends_on") or [])],
            )
        )
    if not steps:
        raise ValueError("plan has no steps")
    return Plan(goal=str(payload.get("goal") or "Handle the support email."), steps=steps)


def _fallback_plan() -> Plan:
    return Plan(
        goal="Look up policy, then reply without inventing order facts.",
        steps=[
            PlanStep(
                id="s1",
                instruction="Search refund and shipping policy docs.",
                tool="search_docs",
                arguments={"query": "refund shipping"},
            ),
            PlanStep(
                id="s2",
                instruction="Write a policy-compliant reply using only known facts.",
                depends_on=["s1"],
            ),
        ],
    )


def make_plan(email: str) -> Plan:
    raw = _complete(PLAN_SYSTEM, email)
    try:
        return _plan_from_payload(_extract_json(raw))
    except (ValueError, json.JSONDecodeError, TypeError):
        repaired = _complete(
            PLAN_REPAIR_SYSTEM,
            f"Customer email:\n{email}\n\nInvalid plan output:\n{raw}",
        )
        try:
            return _plan_from_payload(_extract_json(repaired))
        except (ValueError, json.JSONDecodeError, TypeError):
            return _fallback_plan()


def _execution_log(results: list[StepResult]) -> str:
    if not results:
        return "(none)"
    return "\n\n".join(
        f"Step {item.id} [{item.status}]:\n{item.output}" for item in results
    )


def _blocked(output: str) -> bool:
    text = output.strip()
    return text.startswith("No order found") or text.startswith("REFUSED")


def _ready_order(steps: list[PlanStep]) -> list[PlanStep]:
    by_id = {step.id: step for step in steps}
    remaining = set(by_id)
    ordered: list[PlanStep] = []
    while remaining:
        ready = [
            step.id
            for step in steps
            if step.id in remaining
            and all(dep not in remaining for dep in by_id[step.id].depends_on)
        ]
        if not ready:
            return list(steps)
        pick = ready[0]
        remaining.remove(pick)
        ordered.append(by_id[pick])
    return ordered


def execute_step(email: str, step: PlanStep, prior: list[StepResult]) -> StepResult:
    if step.tool:
        try:
            output = call_tool(step.tool, step.arguments)
        except TypeError as exc:
            output = f"Tool argument error: {exc}"
        status = "blocked" if _blocked(output) else "done"
        return StepResult(id=step.id, status=status, output=output)

    user = (
        f"Original email:\n{email}\n\n"
        f"Step instruction:\n{step.instruction}\n\n"
        f"Prior step outputs:\n{_execution_log(prior)}"
    )
    output = _complete(PLAN_STEP_SYSTEM, user)
    return StepResult(id=step.id, status="done", output=output)


def replan_remaining(email: str, completed: list[StepResult], leftover: list[PlanStep]) -> list[PlanStep]:
    leftover_blob = json.dumps(
        [step.model_dump() for step in leftover],
        indent=2,
    )
    user = (
        f"Original email:\n{email}\n\n"
        f"Completed steps:\n{_execution_log(completed)}\n\n"
        f"Leftover steps:\n{leftover_blob}"
    )
    raw = _complete(PLAN_REPLAN_SYSTEM, user)
    try:
        payload = _extract_json(raw)
        if "steps" not in payload:
            payload = {"goal": "", "steps": payload.get("remaining") or [payload]}
        return _plan_from_payload(payload).steps
    except (ValueError, json.JSONDecodeError, TypeError):
        try:
            start = raw.find("[")
            end = raw.rfind("]")
            if start != -1 and end > start:
                items = json.loads(raw[start : end + 1])
                if isinstance(items, list):
                    return _plan_from_payload({"goal": "", "steps": items}).steps
        except (ValueError, json.JSONDecodeError, TypeError):
            pass
        return leftover


def _reply_from_execution(email: str, results: list[StepResult], steps: list[PlanStep]) -> str:
    by_id = {step.id: step for step in steps}
    for item in reversed(results):
        step = by_id.get(item.id)
        if step is not None and step.tool is None and item.status == "done" and item.output.strip():
            return item.output
    user = (
        f"Original email:\n{email}\n\n"
        f"Step instruction:\nWrite the customer-facing reply.\n\n"
        f"Prior step outputs:\n{_execution_log(results)}"
    )
    return _complete(PLAN_STEP_SYSTEM, user)


def plan_node(state: PlanningState) -> dict[str, Any]:
    plan = make_plan(state["email"])
    return {
        "plan": plan.model_dump(),
        "steps": [step.model_dump() for step in plan.steps],
        "queue": [step.model_dump() for step in _ready_order(plan.steps)],
        "execution": [],
        "replans": 0,
        "reply": "",
    }


def execute_node(state: PlanningState) -> dict[str, Any]:
    queue = list(state["queue"])
    step = PlanStep.model_validate(queue.pop(0))
    prior = [StepResult.model_validate(item) for item in state["execution"]]
    result = execute_step(state["email"], step, prior)
    return {
        "queue": queue,
        "execution": state["execution"] + [result.model_dump()],
    }


def replan_node(state: PlanningState) -> dict[str, Any]:
    leftover = [PlanStep.model_validate(item) for item in state["queue"]]
    completed = [StepResult.model_validate(item) for item in state["execution"]]
    new_steps = replan_remaining(state["email"], completed, leftover)
    executed_ids = {item["id"] for item in state["execution"]}
    steps = [item for item in state["steps"] if item["id"] in executed_ids] + [
        step.model_dump() for step in new_steps
    ]
    return {
        "queue": [step.model_dump() for step in _ready_order(new_steps)],
        "steps": steps,
        "replans": state["replans"] + 1,
    }


def reply_node(state: PlanningState) -> dict[str, str]:
    results = [StepResult.model_validate(item) for item in state["execution"]]
    steps = [PlanStep.model_validate(item) for item in state["steps"]]
    return {"reply": _reply_from_execution(state["email"], results, steps)}


def after_execute(state: PlanningState) -> Literal["execute", "replan", "reply"]:
    last = state["execution"][-1] if state["execution"] else None
    if (
        last
        and last.get("status") == "blocked"
        and state["replans"] < MAX_REPLANS
        and state["queue"]
    ):
        return "replan"
    if state["queue"]:
        return "execute"
    return "reply"


def after_replan(state: PlanningState) -> Literal["execute", "reply"]:
    return "execute" if state["queue"] else "reply"


def build_graph():
    graph = StateGraph(PlanningState)
    graph.add_node("plan", plan_node)
    graph.add_node("execute", execute_node)
    graph.add_node("replan", replan_node)
    graph.add_node("reply", reply_node)
    graph.add_edge(START, "plan")
    graph.add_edge("plan", "execute")
    graph.add_conditional_edges(
        "execute",
        after_execute,
        {"execute": "execute", "replan": "replan", "reply": "reply"},
    )
    graph.add_conditional_edges(
        "replan",
        after_replan,
        {"execute": "execute", "reply": "reply"},
    )
    graph.add_edge("reply", END)
    return graph.compile()


@observe(name="pattern.planning")
def run(email: str) -> PlanningResult:
    with propagate_attributes(
        tags=["backend:langchain", "pattern:planning"],
        metadata={"pattern": "planning", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        result = build_graph().invoke(
            {
                "email": email,
                "plan": {},
                "steps": [],
                "queue": [],
                "execution": [],
                "replans": 0,
                "reply": "",
            },
            config={"callbacks": [handler]},
        )
        return PlanningResult(
            plan=Plan.model_validate(result["plan"]),
            execution=[StepResult.model_validate(item) for item in result["execution"]],
            replans=int(result["replans"]),
            reply=result["reply"],
        )


def main() -> None:
    print(run(SUPPORT_EMAIL).model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
