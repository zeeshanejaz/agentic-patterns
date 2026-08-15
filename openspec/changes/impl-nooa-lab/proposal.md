## Why

The 21-pattern loop is complete. Special lab OO-Agents is still documentation only: NVIDIA OO Agents (code as action, tools as methods on `self`) is the object-oriented harness next to MCP, not a fifth rewrite of every pattern. Scaffold it now so traces can be compared with scratch / LangChain / MAF / MCP on the same support inbox.

## What Changes

- Add workspace package `packages/nooa-lab` (`sd-agentic-nooa`) depending on `nooa` and `sd-agentic-shared`.
- Add `SupportAgent`: shared fake tools (`lookup_order`, `create_refund`, `search_docs`) as ordinary methods; CodeAct generation method `handle(email)`.
- Add `demo`: construct `SupportAgent`, call `lookup_order` with no LLM generation.
- Add `support`: CodeAct on `SUPPORT_EMAIL`; Langfuse tags `pattern:tool_use` / `backend:nooa` via native OTLP (`exporters.langfuse()`).
- Update `README.md` Special labs (demo + support links), pattern 5 notes, Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `nooa-lab`: NVIDIA OO Agents special lab — `SupportAgent` methods as tools, no-LLM demo, CodeAct support loop, Langfuse OTLP tags.

### Modified Capabilities

- (none)

## Impact

- New package under `packages/nooa-lab`. Root ruff paths / first-party names. README Special labs + Run. Shared prompts/emails/tools reused; scratch/LangChain/MAF/MCP unchanged. Not a 21-pattern Progress column.
