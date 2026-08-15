## Why

Memory management (#8) already exists from scratch (three-tier store over a support thread), but LangChain and MAF cells are still pending, so the pattern cannot be diffed three ways in Langfuse.

## What Changes

- Add `sd_agentic_langchain.memory_management` using LangGraph for the per-turn retrieve → reply → extract cycle over `MEMORY_THREAD`.
- Add `sd_agentic_maf.memory_management` using MAF Agents for reply / extract inside the same Python control flow as scratch.
- Reuse `MEMORY_THREAD`, `MEMORY_EXTRACT_SYSTEM`, and `MEMORY_REPLY_SYSTEM`. Same result shape (`turn`, `retrieved`, `reply`, memory snapshot). Same caps `MAX_EPISODIC = 2`, `MAX_LONG_TERM = 8`.
- Tag traces `pattern:memory_management` and `backend:langchain` / `backend:maf`.
- Update README Progress (memory LangChain + MAF → done), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `memory-management-ports`: LangChain and MAF ports of from-scratch memory management on the shared support-inbox thread.

### Modified Capabilities

- (none)

## Impact

- New modules: `packages/langchain-lab/src/sd_agentic_langchain/memory_management.py`, `packages/maf-lab/src/sd_agentic_maf/memory_management.py`.
- README Progress / Done / Next / Run.
- No changes to `packages/patterns` or shared prompts/thread (already exist).
