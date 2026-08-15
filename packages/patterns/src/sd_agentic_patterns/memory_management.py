"""Memory management: short-term, episodic, and long-term store across support turns."""

from __future__ import annotations

import json
from typing import Any

from langfuse import get_client, observe, propagate_attributes
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env
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


class MemoryStore:
    def __init__(self) -> None:
        self.short_term = ""
        self.episodic: list[MemoryItem] = []
        self.long_term: list[MemoryItem] = []

    def set_short_term(self, email: str, turn: int) -> None:
        self.short_term = email
        _ = turn

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


@observe(name="step.retrieve")
def retrieve(store: MemoryStore) -> list[MemoryItem]:
    return store.retrieve()


@observe(name="step.reply")
def write_reply(email: str, retrieved: list[MemoryItem]) -> str:
    user = (
        f"Retrieved memory:\n{_retrieved_blob(retrieved)}\n\n"
        f"Current email:\n{email}"
    )
    return complete(MEMORY_REPLY_SYSTEM, user)


@observe(name="step.extract")
def extract_memories(email: str, reply: str, retrieved: list[MemoryItem]) -> tuple[str, list[str]]:
    user = (
        f"Retrieved memory:\n{_retrieved_blob(retrieved)}\n\n"
        f"Current email:\n{email}\n\n"
        f"Reply that was sent:\n{reply}"
    )
    raw = complete(MEMORY_EXTRACT_SYSTEM, user)
    try:
        payload = _extract_json(raw)
        episodic = str(payload.get("episodic") or "").strip()
        facts_raw = payload.get("long_term") or []
        facts = [str(item).strip() for item in facts_raw if str(item).strip()]
        return episodic, facts
    except (ValueError, json.JSONDecodeError, TypeError):
        return email[:200], []


@observe(name="pattern.memory_management")
def run(thread: list[str] | None = None) -> list[TurnResult]:
    emails = thread if thread is not None else MEMORY_THREAD
    with propagate_attributes(
        tags=["backend:scratch", "pattern:memory_management"],
        metadata={"pattern": "memory_management", "backend": "scratch"},
    ):
        store = MemoryStore()
        results: list[TurnResult] = []
        for index, email in enumerate(emails, start=1):
            store.set_short_term(email, index)
            retrieved = retrieve(store)
            reply = write_reply(email, retrieved)
            episodic, facts = extract_memories(email, reply, retrieved)
            store.add_episodic(episodic, index)
            store.add_long_term(facts, index)
            results.append(
                TurnResult(
                    turn=index,
                    retrieved=retrieved,
                    reply=reply,
                    memory=store.snapshot(),
                )
            )
        return results


def main() -> None:
    for item in run(MEMORY_THREAD):
        print(item.model_dump_json(indent=2))
        print()
    get_client().flush()


if __name__ == "__main__":
    main()
