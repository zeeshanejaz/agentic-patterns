"""Langfuse OTLP for the OO-Agents lab via NOOA exporters.langfuse()."""

from __future__ import annotations

import os

from nooa.tracing import enable_tracing, exporters, flush_traces

from sd_agentic_shared.env import load_env

_TRACING_READY = False


def configure_nooa_tracing() -> None:
    global _TRACING_READY
    if _TRACING_READY:
        return
    load_env()
    host = (
        os.environ.get("LANGFUSE_HOST")
        or os.environ.get("LANGFUSE_BASE_URL")
        or "https://cloud.langfuse.com"
    )
    enable_tracing(
        exporters=[
            exporters.langfuse(
                host=host.rstrip("/"),
                public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
                secret_key=os.environ.get("LANGFUSE_SECRET_KEY"),
            )
        ],
        extra_resource_attrs={"pattern": "tool_use", "backend": "nooa"},
    )
    _TRACING_READY = True


def flush_nooa_traces() -> None:
    flush_traces()
