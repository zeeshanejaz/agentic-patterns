## Why

Multi-agent collaboration (#7) already exists from scratch (coordinator → specialists → shared notes → writer), but LangChain and MAF cells are still pending, so the pattern cannot be diffed three ways in Langfuse.

## What Changes

- Add `sd_agentic_langchain.multi_agent` using LangGraph for the outer coordinate → specialists → optional review cycle, then writer.
- Add `sd_agentic_maf.multi_agent` using MAF Agents for coordinator / specialists / writer inside the same Python control flow as scratch.
- Reuse the shared multi-agent prompts. Same result shape (`assignments`, `notes`, `rounds`, `reply`). Cap at `MAX_ROUNDS = 2`.
- Tag traces `pattern:multi_agent` and `backend:langchain` / `backend:maf`.
- Update README Progress (multi-agent LangChain + MAF → done), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `multi-agent-ports`: LangChain and MAF ports of from-scratch multi-agent collaboration on the shared support-inbox task.

### Modified Capabilities

- (none)

## Impact

- New modules: `packages/langchain-lab/src/sd_agentic_langchain/multi_agent.py`, `packages/maf-lab/src/sd_agentic_maf/multi_agent.py`.
- README Progress / Done / Next / Run.
- No changes to `packages/patterns` or shared prompts (already exist). No new fake tools.
