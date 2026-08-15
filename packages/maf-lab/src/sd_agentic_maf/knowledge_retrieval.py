"""Knowledge retrieval (RAG) with keyword retrieve and a MAF Agent. Traces via OTEL."""

from __future__ import annotations

import asyncio
import re

from agent_framework import Agent
from agent_framework.observability import get_tracer
from agent_framework.openai import OpenAIChatClient
from opentelemetry import trace
from pydantic import BaseModel

from sd_agentic_maf.otel import configure_maf_otel
from sd_agentic_shared.corpus import RAG_CHUNKS, RagChunk
from sd_agentic_shared.env import load_env, openai_model, workspace_root
from sd_agentic_shared.prompts import RAG_REPLY_SYSTEM
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()
_OTEL_READY = False

K = 3
STOPWORDS = {
    "a",
    "an",
    "and",
    "the",
    "to",
    "of",
    "for",
    "in",
    "on",
    "is",
    "it",
    "my",
    "i",
    "you",
    "we",
}


class RetrievedChunk(BaseModel):
    id: str
    title: str
    text: str
    score: float


class RagResult(BaseModel):
    query: str
    retrieved: list[RetrievedChunk]
    reply: str


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


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9$]+", text.lower())
        if token not in STOPWORDS and len(token) > 1
    }


def _score(query: str, chunk: RagChunk) -> float:
    q = _tokens(query)
    if not q:
        return 0.0
    blob = _tokens(f"{chunk.title} {chunk.text} {chunk.id}")
    return len(q & blob) / len(q)


def retrieve(query: str, k: int = K) -> list[RetrievedChunk]:
    ranked = sorted(
        (
            RetrievedChunk(
                id=chunk.id,
                title=chunk.title,
                text=chunk.text,
                score=round(_score(query, chunk), 4),
            )
            for chunk in RAG_CHUNKS
        ),
        key=lambda item: item.score,
        reverse=True,
    )
    return [item for item in ranked[:k] if item.score > 0] or ranked[:k]


async def run(email: str | None = None) -> RagResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    _ensure_otel()
    agent = Agent(client=_client(), name="rag_reply", instructions=RAG_REPLY_SYSTEM)
    with get_tracer().start_as_current_span("pattern.knowledge_retrieval") as span:
        span.set_attribute("pattern", "knowledge_retrieval")
        span.set_attribute("backend", "maf")
        retrieved = retrieve(ticket)
        blob = "\n\n".join(
            f"[{item.id}] {item.title}: {item.text}" for item in retrieved
        ) or "(none)"
        reply = (
            await agent.run(f"Retrieved chunks:\n{blob}\n\nEmail:\n{ticket}")
        ).text or ""
        return RagResult(query=ticket, retrieved=retrieved, reply=reply)


def main() -> None:
    print(asyncio.run(run()).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
