## 1. Package scaffold

- [x] 1.1 Add `packages/nooa-lab/pyproject.toml` (`sd-agentic-nooa`, deps: `sd-agentic-shared`, `nooa`, `opentelemetry-exporter-otlp-proto-http`)
- [x] 1.2 Add `src/sd_agentic_nooa/__init__.py` and Windows `fcntl`/`SIGUSR2` shim; register the package in root ruff `src` and `known-first-party`

## 2. Agent and tracing

- [x] 2.1 Add `tracing.py`: map `LANGFUSE_HOST` or `LANGFUSE_BASE_URL` and `enable_tracing(exporters.langfuse())`
- [x] 2.2 Add `agent.py`: `SupportAgent` with tool methods wrapping shared fakes, call recording, CodeAct `handle` using `POLICY`

## 3. Entrypoints

- [x] 3.1 Add `demo.py`: construct `SupportAgent`, call `lookup_order("A-18422")`, print JSON (no `handle`)
- [x] 3.2 Add `support.py`: CodeAct `handle(SUPPORT_EMAIL)`, wrap span tags `pattern:tool_use` / `backend:nooa`, print calls + reply, flush traces

## 4. README

- [x] 4.1 Flip Special labs OO-Agents `demo` and `support` to source links; update pattern 5 notes, Done/Next, and Run
