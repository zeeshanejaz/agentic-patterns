"""Memory management: LangGraph retrieve → reply → extract cycle over a support thread."""

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
from sd_agentic_shared.prompts import MEMORY_EXTRACT_SYSTEM, MEMORY_REPLY_SYSTEM
from sd_agentic_shared.tasks.support_email import MEMORY_THREAD

load_env()

MAX_EPISODIC = 2
MAX_LONG_TERM = 8


class MemoryItem(BaseModel):
    kind: str
    text: str
    turn: int


class MemorySnapshot(BaseModel):
    short_term: str
    episodic: list[str]
    long_term: list[str]


class TurnResult(BaseModel):
    turn: int
    retrieved: list[MemoryItem]
    reply: str
    memory: MemorySnapshot


class MemoryState(TypedDict):
    emails: list[str]
    turn: int
    short_term: str
    episodic: list[dict[str, Any]]
    long_term: list[dict[str, Any]]
    retrieved: list[dict[str, Any]]
    reply: str
    results: list[dict[str, Any]]


class MemoryStore:
    def __init__(self) -> None:
        self.short_term = ""
        self.episodic: list[MemoryItem] = []
        self.long_term: list[MemoryItem] = []

    def set_short_term(self, email: str) -> None:
        self.short_term = email

    def retrieve(self) -> list[MemoryItem]:
        return list(self.long_term) + list(self.episodic)

    def add_episodic(self, text: str, turn: int) -> None:
        blob = text.strip()
        if not blob:
            return
        self.episodic.append(MemoryItem(kind="episodic", text=blob, turn=turn))
        overflow = len(self.episodic) - MAX_EPISODIC
        if overflow > 0:
            self.episodic = self.episodic[overflow:]

    def add_long_term(self, facts: list[str], turn: int) -> None:
        existing = {item.text.strip().lower() for item in self.long_term}
        for fact in facts:
            blob = fact.strip()
            if not blob or blob.lower() in existing:
                continue
            self.long_term.append(MemoryItem(kind="long_term", text=blob, turn=turn))
            existing.add(blob.lower())
        overflow = len(self.long_term) - MAX_LONG_TERM
        if overflow > 0:
            self.long_term = self.long_term[overflow:]

    def snapshot(self) -> MemorySnapshot:
        return MemorySnapshot(
            short_term=self.short_term,
            episodic=[item.text for item in self.episodic],
            long_term=[item.text for item in self.long_term],
        )


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


def _retrieved_blob(items: list[MemoryItem]) -> str:
    if not items:
        return "(none)"
    return "\n".join(f"- [{item.kind} t{item.turn}] {item.text}" for item in items)


def _store_from_state(state: MemoryState) -> MemoryStore:
    store = MemoryStore()
    store.short_term = state["short_term"]
    store.episodic = [MemoryItem.model_validate(item) for item in state["episodic"]]
    store.long_term = [MemoryItem.model_validate(item) for item in state["long_term"]]
    return store


def ingest_node(state: MemoryState) -> dict[str, Any]:
    emails = list(state["emails"])
    email = emails.pop(0)
    return {
        "emails": emails,
        "turn": state["turn"] + 1,
        "short_term": email,
        "reply": "",
        "retrieved": [],
    }


def retrieve_node(state: MemoryState) -> dict[str, Any]:
    store = _store_from_state(state)
    retrieved = store.retrieve()
    return {"retrieved": [item.model_dump() for item in retrieved]}


def reply_node(state: MemoryState) -> dict[str, str]:
    retrieved = [MemoryItem.model_validate(item) for item in state["retrieved"]]
    user = (
        f"Retrieved memory:\n{_retrieved_blob(retrieved)}\n\n"
        f"Current email:\n{state['short_term']}"
    )
    return {"reply": _complete(MEMORY_REPLY_SYSTEM, user)}


def extract_node(state: MemoryState) -> dict[str, Any]:
    retrieved = [MemoryItem.model_validate(item) for item in state["retrieved"]]
    user = (
        f"Retrieved memory:\n{_retrieved_blob(retrieved)}\n\n"
        f"Current email:\n{state['short_term']}\n\n"
        f"Reply that was sent:\n{state['reply']}"
    )
    raw = _complete(MEMORY_EXTRACT_SYSTEM, user)
    try:
        payload = _extract_json(raw)
        episodic = str(payload.get("episodic") or "").strip()
        facts_raw = payload.get("long_term") or []
        facts = [str(item).strip() for item in facts_raw if str(item).strip()]
    except (ValueError, json.JSONDecodeError, TypeError):
        episodic = state["short_term"][:200]
        facts = []
    store = _store_from_state(state)
    store.add_episodic(episodic, state["turn"])
    store.add_long_term(facts, state["turn"])
    snapshot = store.snapshot()
    result = TurnResult(
        turn=state["turn"],
        retrieved=retrieved,
        reply=state["reply"],
        memory=snapshot,
    )
    return {
        "episodic": [item.model_dump() for item in store.episodic],
        "long_term": [item.model_dump() for item in store.long_term],
        "results": state["results"] + [result.model_dump()],
    }


def after_extract(state: MemoryState) -> Literal["ingest", "end"]:
    return "ingest" if state["emails"] else "end"


def build_graph():
    graph = StateGraph(MemoryState)
    graph.add_node("ingest", ingest_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("reply", reply_node)
    graph.add_node("extract", extract_node)
    graph.add_edge(START, "ingest")
    graph.add_edge("ingest", "retrieve")
    graph.add_edge("retrieve", "reply")
    graph.add_edge("reply", "extract")
    graph.add_conditional_edges(
        "extract",
        after_extract,
        {"ingest": "ingest", "end": END},
    )
    return graph.compile()


@observe(name="pattern.memory_management")
def run(thread: list[str] | None = None) -> list[TurnResult]:
    emails = list(thread if thread is not None else MEMORY_THREAD)
    with propagate_attributes(
        tags=["backend:langchain", "pattern:memory_management"],
        metadata={"pattern": "memory_management", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        result = build_graph().invoke(
            {
                "emails": emails,
                "turn": 0,
                "short_term": "",
                "episodic": [],
                "long_term": [],
                "retrieved": [],
                "reply": "",
                "results": [],
            },
            config={"callbacks": [handler]},
        )
        return [TurnResult.model_validate(item) for item in result["results"]]


def main() -> None:
    for item in run(MEMORY_THREAD):
        print(item.model_dump_json(indent=2))
        print()
    get_client().flush()


if __name__ == "__main__":
    main()
