"""A2A with MAF Agents on a TTL message bus. Traces via OTEL."""

from __future__ import annotations

import asyncio

from agent_framework import Agent
from agent_framework.observability import get_tracer
from agent_framework.openai import OpenAIChatClient
from opentelemetry import trace
from pydantic import BaseModel

from sd_agentic_maf.otel import configure_maf_otel
from sd_agentic_shared.env import load_env, openai_model, workspace_root
from sd_agentic_shared.prompts import (
    A2A_MESSAGE_SYSTEM,
    BILLING_AGENT_SYSTEM,
    SHIPPING_AGENT_SYSTEM,
    WRITER_AGENT_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()
_OTEL_READY = False

MAX_MESSAGES = 8


class Envelope(BaseModel):
    id: str
    sender: str
    recipient: str
    body: str
    ttl: int
    in_reply_to: str | None = None


class A2AResult(BaseModel):
    envelopes: list[Envelope]
    delivered: list[Envelope]
    dropped: list[str]
    reply: str


class Bus:
    def __init__(self) -> None:
        self.posted: list[Envelope] = []
        self.seq = 0

    def post(
        self,
        sender: str,
        recipient: str,
        body: str,
        ttl: int,
        in_reply_to: str | None = None,
    ) -> Envelope | None:
        if len(self.posted) >= MAX_MESSAGES:
            return None
        self.seq += 1
        env = Envelope(
            id=f"m{self.seq}",
            sender=sender,
            recipient=recipient,
            body=body.strip(),
            ttl=ttl,
            in_reply_to=in_reply_to,
        )
        self.posted.append(env)
        return env

    def deliver(self, recipient: str, turn: int) -> tuple[list[Envelope], list[str]]:
        inbox: list[Envelope] = []
        dropped: list[str] = []
        for env in self.posted:
            if env.recipient != recipient:
                continue
            if env.ttl < turn:
                dropped.append(env.id)
                continue
            inbox.append(env)
        return inbox, dropped


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


def _blob(envelopes: list[Envelope]) -> str:
    if not envelopes:
        return "(empty inbox)"
    lines = []
    for env in envelopes:
        reply = f" in_reply_to={env.in_reply_to}" if env.in_reply_to else ""
        lines.append(
            f"{env.id} {env.sender}->{env.recipient} ttl={env.ttl}{reply}: {env.body}"
        )
    return "\n".join(lines)


async def run(email: str | None = None) -> A2AResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    _ensure_otel()
    client = _client()
    agents = {
        "billing": Agent(
            client=client,
            name="billing",
            instructions=f"{BILLING_AGENT_SYSTEM}\n{A2A_MESSAGE_SYSTEM}",
        ),
        "shipping": Agent(
            client=client,
            name="shipping",
            instructions=f"{SHIPPING_AGENT_SYSTEM}\n{A2A_MESSAGE_SYSTEM}",
        ),
        "writer": Agent(client=client, name="writer", instructions=WRITER_AGENT_SYSTEM),
    }
    with get_tracer().start_as_current_span("pattern.a2a") as span:
        span.set_attribute("pattern", "a2a")
        span.set_attribute("backend", "maf")
        bus = Bus()
        dropped: list[str] = []
        bus.post(
            "coordinator",
            "billing",
            f"Customer email:\n{ticket}\n\nInstruction: Investigate charges, duplicate pending $89, and the refund ask.",
            ttl=2,
        )
        bus.post(
            "coordinator",
            "shipping",
            f"Customer email:\n{ticket}\n\nInstruction: Investigate tracking/status for the headphones order ids in the email.",
            ttl=2,
        )
        turn = 2
        for name in ("billing", "shipping"):
            inbox, stale = bus.deliver(name, turn)
            dropped.extend(stale)
            note = (
                await agents[name].run(
                    f"Inbox:\n{_blob(inbox)}\n\nWrite your bus note to coordinator."
                )
            ).text or ""
            if inbox:
                bus.post(name, "coordinator", note, ttl=3, in_reply_to=inbox[0].id)
        turn = 3
        coord_inbox, stale = bus.deliver("coordinator", turn)
        dropped.extend(stale)
        bus.post(
            "coordinator",
            "writer",
            f"Specialist mail:\n{_blob(coord_inbox)}\n\nWrite the customer reply.",
            ttl=3,
        )
        writer_inbox, stale = bus.deliver("writer", turn)
        dropped.extend(stale)
        reply = (
            await agents["writer"].run(
                f"Customer email:\n{ticket}\n\nBus mail:\n{_blob(writer_inbox)}"
            )
        ).text or ""
        return A2AResult(
            envelopes=bus.posted,
            delivered=writer_inbox,
            dropped=sorted(set(dropped)),
            reply=reply,
        )


def main() -> None:
    print(asyncio.run(run()).model_dump_json(indent=2))
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


if __name__ == "__main__":
    main()
