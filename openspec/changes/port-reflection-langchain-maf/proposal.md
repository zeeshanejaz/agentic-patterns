## Why

Reflection (#4) already exists from scratch (draft → critic → revise until PASS), but LangChain and MAF cells are still pending, so the pattern cannot be diffed three ways in Langfuse.

## What Changes

- Add `sd_agentic_langchain.reflection` as a LangGraph cycle: summarize → draft → critic → (revise → critic)* until PASS or `MAX_ROUNDS`.
- Add `sd_agentic_maf.reflection` using MAF Agents for the same steps in a Python loop (MAF has no SequentialBuilder cycle primitive that matches this).
- Reuse `SUMMARIZE_SYSTEM`, `DRAFT_SYSTEM`, `CRITIC_SYSTEM`, `REVISE_SYSTEM`, and `SUPPORT_EMAIL`. Same `ReflectionResult` shape as scratch (`summary`, `rounds`, `final`, `passed`). `MAX_ROUNDS = 3`. PASS means critique text starts with `PASS`.
- Tag traces `pattern:reflection` and `backend:langchain` / `backend:maf`.
- Update README Progress (reflection LangChain + MAF → done), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `reflection-ports`: LangChain and MAF ports of from-scratch reflection on the shared support-inbox task.

### Modified Capabilities

- (none)

## Impact

- New modules: `packages/langchain-lab/src/sd_agentic_langchain/reflection.py`, `packages/maf-lab/src/sd_agentic_maf/reflection.py`.
- README Progress / Done / Next / Run.
- No changes to `packages/patterns`. No new shared prompts. No MCP work.
