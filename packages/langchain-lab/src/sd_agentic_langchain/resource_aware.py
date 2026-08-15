"""Resource-aware: LCEL classify then RunnableBranch cheap vs expensive."""

from __future__ import annotations

import math
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_openai import ChatOpenAI
from langfuse import get_client, observe, propagate_attributes
from langfuse.langchain import CallbackHandler
from pydantic import BaseModel

from sd_agentic_shared.env import load_env, openai_model
from sd_agentic_shared.prompts import (
    RESOURCE_CHEAP_SYSTEM,
    RESOURCE_CLASSIFY_SYSTEM,
    RESOURCE_EXPENSIVE_SYSTEM,
)
from sd_agentic_shared.tasks.support_email import SAMPLE_EMAILS

load_env()

CHEAP_FEE = 1
EXPENSIVE_FEE = 4


class ResourceResult(BaseModel):
    label: str
    route: str
    cost_units: int
    reply: str


def _llm() -> ChatOpenAI:
    return ChatOpenAI(model=openai_model())


def _text_chain(system: str):
    prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("human", "{email}")]
    )
    return prompt | _llm() | StrOutputParser()


def _refund_over_50(text: str) -> bool:
    blob = text.lower()
    if "refund" not in blob and "chargeback" not in blob:
        return False
    for match in re.findall(r"\$(\d+(?:\.\d+)?)", blob):
        if float(match) > 50:
            return True
    return "full refund" in blob


def _parse_route(email: str, raw: str) -> str:
    if _refund_over_50(email):
        return "complex"
    token = raw.strip().lower().split()[0].strip(".,:;!?") if raw.strip() else "complex"
    return token if token in {"simple", "complex"} else "complex"


def _cost(route: str, reply: str) -> int:
    fee = CHEAP_FEE if route == "simple" else EXPENSIVE_FEE
    return fee + math.ceil(max(len(reply), 1) / 100)


def _reply_branch():
    cheap = _text_chain(RESOURCE_CHEAP_SYSTEM)
    expensive = _text_chain(RESOURCE_EXPENSIVE_SYSTEM)
    return RunnableBranch(
        (lambda item: item["route"] == "simple", RunnableLambda(lambda item: cheap.invoke({"email": item["email"]}))),
        RunnableLambda(lambda item: expensive.invoke({"email": item["email"]})),
    )


@observe(name="pattern.resource_aware")
def run(email: str, label: str = "ticket") -> ResourceResult:
    with propagate_attributes(
        tags=["backend:langchain", "pattern:resource_aware"],
        metadata={"pattern": "resource_aware", "backend": "langchain", "label": label},
    ):
        handler = CallbackHandler()
        config = {"callbacks": [handler]}
        raw = _text_chain(RESOURCE_CLASSIFY_SYSTEM).invoke({"email": email}, config=config)
        route = _parse_route(email, raw)
        reply = _reply_branch().invoke({"email": email, "route": route}, config=config)
        return ResourceResult(
            label=label,
            route=route,
            cost_units=_cost(route, reply),
            reply=reply,
        )


def main() -> None:
    for label, email in SAMPLE_EMAILS.items():
        print(f"\n=== {label} ===")
        print(run(email, label).model_dump_json(indent=2))
    get_client().flush()


if __name__ == "__main__":
    main()
