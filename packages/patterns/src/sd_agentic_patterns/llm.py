"""Thin OpenAI helper used by from-scratch patterns. Traced via langfuse.openai."""

from __future__ import annotations

from typing import Any

from langfuse.openai import openai

from sd_agentic_shared.env import openai_model


def complete(
    system: str,
    user: str,
    *,
    temperature: float | None = None,
) -> str:
    kwargs: dict[str, Any] = {}
    if temperature is not None:
        kwargs["temperature"] = temperature
    response = openai.chat.completions.create(
        model=openai_model(),
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        **kwargs,
    )
    return response.choices[0].message.content or ""
