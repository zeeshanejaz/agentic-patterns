## Context

MCP is the special lab for discover/authorize tools. OO-Agents is the other special lab: a Python object whose methods are the tools, and whose `...` methods are implemented by CodeAct (LLM writes Python in a REPL with `self`). Same fake support inbox as the 21-pattern loop. `packages/nooa-lab` does not exist yet.

NVIDIA OO Agents (`nooa`) traces via OpenTelemetry. Langfuse ingest is `exporters.langfuse()`, which reads `LANGFUSE_HOST` + keys. This repo uses `LANGFUSE_BASE_URL`.

## Goals / Non-Goals

**Goals:**

- Workspace package `sd-agentic-nooa` with `SupportAgent`, `demo`, and `support`.
- Tools are methods wrapping `sd_agentic_shared.tools`; policy text from `POLICY`; email from `SUPPORT_EMAIL`.
- `demo` constructs the agent and calls `lookup_order("A-18422")` without invoking a generation method.
- `support` runs CodeAct `handle` on `SUPPORT_EMAIL`; traces tagged `pattern:tool_use` / `backend:nooa`.
- README Special labs cells + Run commands; pattern 5 notes point at the OO-Agents variant. No new Progress column.

**Non-Goals:**

- Porting patterns 1–21 into NOOA.
- FastMCP inside this lab (MCP stays `packages/mcp-lab`).
- Requiring `nooa-cli` / the local trace viewer.
- Changing scratch / LangChain / MAF / MCP modules.

## Decisions

1. **One agent class, two entrypoints.** `SupportAgent` lives in `agent.py`. `demo` and `support` both construct it. Demo never calls `handle()`. Alternative: a plain tools class for demo — rejected; the point of the lab is that tools *are* methods on the agent.

2. **LLM at construction, unused in demo.** NOOA requires an LLM to instantiate `Agent`. Demo still passes `get_llm_client(openai_model())` but only calls `lookup_order`. Alternative: a dummy LLM — rejected; same client as `support` is simpler.

3. **Default CodeAct, not Predict.** `handle` uses the default `CodeActStrategy` so the model writes Python that calls `self.lookup_order` / `create_refund` / `search_docs`. Predict is single-shot with no tool loop.

4. **Langfuse via `exporters.langfuse()`, host from `LANGFUSE_BASE_URL`.** A small `tracing.py` maps `LANGFUSE_HOST` or `LANGFUSE_BASE_URL` (default `https://cloud.langfuse.com`) and calls `enable_tracing(exporters=[exporters.langfuse(host=...)])`. Tags go on a wrapping OTEL span (`langfuse.trace.tags` plus `pattern` / `backend` attributes), matching MAF’s span attributes. Depend on `opentelemetry-exporter-otlp-proto-http` because `exporters.otlp` is optional in `nooa`.

5. **Record method calls on the instance.** Tool methods append `{name, arguments, result}` so `support` can print JSON comparable to scratch/MCP `ToolUseResult`. Traces still come from NOOA’s native spans.

6. **Package layout mirrors MCP.** `src/sd_agentic_nooa/` with hatchling; add the path and `sd_agentic_nooa` to root ruff. Python range stays workspace `>=3.12` (`nooa` itself is `<3.14`; uv will resolve).

7. **Windows import shim.** `nooa` import-time code uses POSIX `fcntl` (SQLite flock) and `SIGUSR2` (debug handler). This lab uses in-memory storage only, so on `win32` install a no-op `fcntl` stub and alias `SIGUSR2` before importing `nooa`. Import `Agent` from `nooa.agent`.

## Risks / Trade-offs

- [CodeAct executes LLM-generated Python] → Lab methods only wrap in-memory fakes; no shell/network tools; AST deny-lists are defense-in-depth, not a sandbox. Document like the upstream safety note, keep scope to the fake inbox.
- [NOOA import fails on Windows (`fcntl`)] → Stub `fcntl` in package `__init__` before importing `nooa`; do not use SQLite persistence.
- [NOOA exporter wants `LANGFUSE_HOST`] → Map from existing `LANGFUSE_BASE_URL`.
- [Agent init needs an LLM even for demo] → Document that demo does not *invoke* generation; construction still needs `OPENAI_API_KEY` in env for the client object.
- [Tags via OTEL may not appear as Langfuse SDK tags] → Also set `langfuse.trace.tags` on the wrap span; filter still works via metadata attributes.

## Migration Plan

Add the package, `uv sync --all-packages`, README. Rollback is delete the package and revert README/ruff.

## Open Questions

None.
