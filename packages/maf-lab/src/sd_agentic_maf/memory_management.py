"""Memory management with MAF Agents over a support thread. Traces via OTEL."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from agent_framework import Agent
from agent_framework.observability import get_tracer
from agent_framework.openai import OpenAIChatClient
from opentelemetry import trace
from pydantic import BaseModel

from sd_agentic_maf.otel import configure_maf_otel
from sd_agentic_shared.env import load_env, openai_model, workspace_root
from sd_agentic_shared.prompts import MEMORY_EXTRACT_SYSTEM, MEMORY_REPLY_SYSTEM
from sd_agentic_shared.tasks.support_email import MEMORY_THREAD

load_env()
_OTEL_READY = False

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


def _ensure_otel() -> None:
    global _OTEL_READY
    if not _OTEL_READY:
        configure_maf_otel()
        _OTEL_READY = True


def _client() -> OpenAIChatClient:
    return OpenAIChatClient(
        model=openai_model(),
        env_file_path=str(workspace_root() / ".env"),
    )


def build_agents() -> dict[str, Agent]:
    client = _client()
    return {
        "reply": Agent(client=client, name="reply", instructions=MEMORY_REPLY_SYSTEM),
        "extract": Agent(client=client, name="extract", instructions=MEMORY_EXTRACT_SYSTEM),
    }


async def _complete(agent: Agent, user: str) -> str:
    return (await agent.run(user)).text or ""


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


async def run(thread: list[str] | None = None) -> list[TurnResult]:
    emails = thread if thread is not None else MEMORY_THREAD
    _ensure_otel()
    agents = build_agents()
    with get_tracer().start_as_current_span("pattern.memory_management") as span:
        span.set_attribute("pattern", "memory_management")
        span.set_attribute("backend", "maf")
        store = MemoryStore()
        results: list[TurnResult] = []
        for index, email in enumerate(emails, start=1):
            store.set_short_term(email)
            retrieved = store.retrieve()
            reply = await _complete(
                agents["reply"],
                f"Retrieved memory:\n{_retrieved_blob(retrieved)}\n\nCurrent email:\n{email}",
            )
            raw = await _complete(
                agents["extract"],
                (
                    f"Retrieved memory:\n{_retrieved_blob(retrieved)}\n\n"
                    f"Current email:\n{email}\n\n"
                    f"Reply that was sent:\n{reply}"
                ),
            )
            try:
                payload = _extract_json(raw)
                episodic = str(payload.get("episodic") or "").strip()
                facts_raw = payload.get("long_term") or []
                facts = [str(item).strip() for item in facts_raw if str(item).strip()]
            except (ValueError, json.JSONDecodeError, TypeError):
                episodic = email[:200]
                facts = []
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
    for item in asyncio.run(run(MEMORY_THREAD)):
        print(item.model_dump_json(indent=2))
        print()
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
