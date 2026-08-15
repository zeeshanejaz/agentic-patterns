"""Knowledge retrieval (RAG): keyword top-k over policy chunks, then a cited reply."""

from __future__ import annotations

import re

from langfuse import get_client, observe, propagate_attributes
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.corpus import RAG_CHUNKS, RagChunk
from sd_agentic_shared.env import load_env
from sd_agentic_shared.prompts import RAG_REPLY_SYSTEM
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()

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
    overlap = q & blob
    return len(overlap) / len(q)


@observe(name="step.retrieve")
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


@observe(name="step.generate")
def generate(email: str, retrieved: list[RetrievedChunk]) -> str:
    blob = "\n\n".join(
        f"[{item.id}] {item.title}: {item.text}" for item in retrieved
    ) or "(none)"
    user = f"Retrieved chunks:\n{blob}\n\nEmail:\n{email}"
    return complete(RAG_REPLY_SYSTEM, user)


@observe(name="pattern.knowledge_retrieval")
def run(email: str | None = None) -> RagResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    with propagate_attributes(
        tags=["backend:scratch", "pattern:knowledge_retrieval"],
        metadata={"pattern": "knowledge_retrieval", "backend": "scratch"},
    ):
        retrieved = retrieve(ticket)
        reply = generate(ticket, retrieved)
        return RagResult(query=ticket, retrieved=retrieved, reply=reply)


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
