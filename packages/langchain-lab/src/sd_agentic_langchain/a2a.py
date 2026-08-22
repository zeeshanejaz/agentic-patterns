"""A2A: LangGraph dispatch → specialists → forward → writer over a TTL bus."""

from __future__ import annotations

from typing import Any, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langfuse import get_client, observe, propagate_attributes
from langfuse.langchain import CallbackHandler
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import (
    A2A_MESSAGE_SYSTEM,
    BILLING_AGENT_SYSTEM,
    SHIPPING_AGENT_SYSTEM,
    WRITER_AGENT_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import SUPPORT_EMAIL

load_env()

MAX_MESSAGES = 8
# ttl is the last turn an envelope may be delivered.
DISPATCH_TTL = 2  # specialists read at turn 2
REPLY_TTL = 3  # coordinator and writer read at turn 3


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


class A2AState(TypedDict):
    email: str
    envelopes: list[dict[str, Any]]
    delivered: list[dict[str, Any]]
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


def _llm() -> ChatOpenAI:
    return ChatOpenAI(model=openai_model())


def _complete(system: str, user: str) -> str:
    message = _llm().invoke(
        [SystemMessage(content=system), HumanMessage(content=user)]
    )
    content = message.content
    return content if isinstance(content, str) else str(content or "")


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


def build_graph(bus: Bus, dropped: list[str]):
    def dispatch_node(state: A2AState) -> dict[str, str]:
        ticket = state["email"]
        for recipient, instruction in (
            ("billing", "Investigate charges, duplicate pending $89, and the refund ask."),
            ("shipping", "Investigate tracking/status for the headphones order ids in the email."),
        ):
            bus.post(
                "coordinator",
                recipient,
                f"Customer email:\n{ticket}\n\nInstruction: {instruction}",
                ttl=DISPATCH_TTL,
            )
        return {}

    def specialists_node(state: A2AState) -> dict[str, str]:
        _ = state
        turn = 2
        for agent, system in (
            ("billing", BILLING_AGENT_SYSTEM),
            ("shipping", SHIPPING_AGENT_SYSTEM),
        ):
            inbox, stale = bus.deliver(agent, turn)
            dropped.extend(stale)
            if not inbox:
                continue
            note = _complete(
                f"{system}\n{A2A_MESSAGE_SYSTEM}",
                f"Inbox:\n{_blob(inbox)}\n\nWrite your bus note to coordinator.",
            )
            bus.post(agent, "coordinator", note, ttl=REPLY_TTL, in_reply_to=inbox[0].id)
        return {}

    def forward_node(state: A2AState) -> dict[str, Any]:
        _ = state
        turn = 3
        coord_inbox, stale = bus.deliver("coordinator", turn)
        dropped.extend(stale)
        bus.post(
            "coordinator",
            "writer",
            f"Specialist mail:\n{_blob(coord_inbox)}\n\nWrite the customer reply.",
            ttl=REPLY_TTL,
        )
        return {}

    def write_node(state: A2AState) -> dict[str, Any]:
        turn = 3
        writer_inbox, stale = bus.deliver("writer", turn)
        dropped.extend(stale)
        reply = _complete(
            WRITER_AGENT_SYSTEM,
            f"Customer email:\n{state['email']}\n\nBus mail:\n{_blob(writer_inbox)}",
        )
        return {
            "envelopes": [item.model_dump() for item in bus.posted],
            "delivered": [item.model_dump() for item in writer_inbox],
            "dropped": sorted(set(dropped)),
            "reply": reply,
        }

    graph = StateGraph(A2AState)
    graph.add_node("dispatch", dispatch_node)
    graph.add_node("specialists", specialists_node)
    graph.add_node("forward", forward_node)
    graph.add_node("write", write_node)
    graph.add_edge(START, "dispatch")
    graph.add_edge("dispatch", "specialists")
    graph.add_edge("specialists", "forward")
    graph.add_edge("forward", "write")
    graph.add_edge("write", END)
    return graph.compile()


@observe(name="pattern.a2a")
def run(email: str | None = None) -> A2AResult:
    ticket = email if email is not None else SUPPORT_EMAIL
    with propagate_attributes(
        tags=["backend:langchain", "pattern:a2a"],
        metadata={"pattern": "a2a", "backend": "langchain"},
    ):
        handler = CallbackHandler()
        bus = Bus()
        dropped: list[str] = []
        result = build_graph(bus, dropped).invoke(
            {
                "email": ticket,
                "envelopes": [],
                "delivered": [],
                "dropped": [],
                "reply": "",
            },
            config={"callbacks": [handler]},
        )
        return A2AResult(
            envelopes=[Envelope.model_validate(item) for item in result["envelopes"]],
            delivered=[Envelope.model_validate(item) for item in result["delivered"]],
            dropped=result["dropped"],
            reply=result["reply"],
        )


def main() -> None:
    print(run().model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
