## Why

Routing (#2) already exists from scratch, but LangChain and MAF cells are still pending, so the pattern cannot be diffed three ways in Langfuse. Ports come before new scratch patterns.

## What Changes

- Add `sd_agentic_langchain.routing` that classifies each sample email then runs one specialist handler via LangGraph conditional edges.
- Add `sd_agentic_maf.routing` that classifies then runs one specialist MAF Agent (not SequentialBuilder; not conversational HandoffBuilder).
- Reuse `ROUTE_SYSTEM`, handler prompts, and `SAMPLE_EMAILS` from `packages/shared`. Same `RouteResult` shape as scratch (`intent`, `reply`).
- Tag traces `pattern:routing` and `backend:langchain` / `backend:maf`.
- Update README Progress (routing LangChain + MAF → done), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `routing-ports`: LangChain and MAF ports of from-scratch routing on the shared support-inbox task, with the same prompts, sample emails, result shape, and Langfuse tags.

### Modified Capabilities

- (none — `openspec/specs/` has no existing capabilities)

## Impact

- New modules: `packages/langchain-lab/src/sd_agentic_langchain/routing.py`, `packages/maf-lab/src/sd_agentic_maf/routing.py`.
- README Progress / Done / Next / Run.
- No changes to `packages/patterns` (must not import LangChain or MAF).
- No new shared prompts or fake tools. No MCP work. No new package dependencies beyond what the labs already use.
