"""Resource-aware optimization: cheap vs expensive reply paths by ticket complexity."""

from __future__ import annotations

import math
import re

from langfuse import get_client, observe, propagate_attributes
from pydantic import BaseModel

from sd_agentic_patterns.llm import complete
from sd_agentic_shared.env import load_env
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


def _refund_over_50(text: str) -> bool:
    blob = text.lower()
    if "refund" not in blob and "chargeback" not in blob:
        return False
    for match in re.findall(r"\$(\d+(?:\.\d+)?)", blob):
        if float(match) > 50:
            return True
    return "full refund" in blob


@observe(name="step.classify")
def classify(email: str) -> str:
    if _refund_over_50(email):
        return "complex"
    raw = complete(RESOURCE_CLASSIFY_SYSTEM, email).strip().lower().split()
    token = raw[0].strip(".,:;!?") if raw else "complex"
    return token if token in {"simple", "complex"} else "complex"


@observe(name="step.reply")
def write_reply(email: str, route: str) -> str:
    system = RESOURCE_CHEAP_SYSTEM if route == "simple" else RESOURCE_EXPENSIVE_SYSTEM
    return complete(system, email)


def _cost(route: str, reply: str) -> int:
    fee = CHEAP_FEE if route == "simple" else EXPENSIVE_FEE
    return fee + math.ceil(max(len(reply), 1) / 100)


@observe(name="pattern.resource_aware")
def run(email: str, label: str = "ticket") -> ResourceResult:
    with propagate_attributes(
        tags=["backend:scratch", "pattern:resource_aware"],
        metadata={"pattern": "resource_aware", "backend": "scratch", "label": label},
    ):
        route = classify(email)
        reply = write_reply(email, route)
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
