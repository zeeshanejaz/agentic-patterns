"""Construct SupportAgent and call lookup_order with no CodeAct."""

from __future__ import annotations

import json

from sd_agentic_nooa.agent import make_support_agent


def demo() -> dict:
    agent = make_support_agent()
    return {"lookup_order": agent.lookup_order("A-18422")}


def main() -> None:
    print(json.dumps(demo(), indent=2))


if __name__ == "__main__":
    main()
