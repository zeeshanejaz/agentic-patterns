"""Map Langfuse credentials onto standard OTEL env vars for MAF exporters."""

from __future__ import annotations

import base64
import os

from agent_framework.observability import configure_otel_providers

from sd_agentic_shared.env import load_env


def configure_maf_otel() -> None:
    load_env()
    public = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
    secret = os.environ.get("LANGFUSE_SECRET_KEY", "")
    base = os.environ.get("LANGFUSE_BASE_URL", "https://cloud.langfuse.com").rstrip("/")

    os.environ.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "http/protobuf")
    os.environ.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", f"{base}/api/public/otel")
    os.environ.setdefault("OTEL_SERVICE_NAME", "sd-agentic")
    os.environ.setdefault("ENABLE_INSTRUMENTATION", "true")
    os.environ.setdefault("ENABLE_SENSITIVE_DATA", "true")

    headers = os.environ.get("OTEL_EXPORTER_OTLP_HEADERS", "").strip()
    if not headers or headers == "Authorization=Basic":
        if not public or not secret:
            raise RuntimeError("Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY in .env")
        token = base64.b64encode(f"{public}:{secret}".encode()).decode()
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {token}"

    configure_otel_providers(enable_sensitive_data=True)
