## Why

A2A (#15) already exists from scratch (envelope bus with TTL), but LangChain and MAF cells are still pending.

## What Changes

- Add `sd_agentic_langchain.a2a` using LangGraph nodes for dispatch / specialists / forward / writer over bus state.
- Add `sd_agentic_maf.a2a` using MAF Agents for specialist and writer notes on the same Python bus as scratch.
- Reuse `A2A_MESSAGE_SYSTEM` and specialist prompts. Same result shape. Do not change scratch.
- Tag traces `pattern:a2a` and `backend:langchain` / `backend:maf`.
- Update README Progress (A2A LangChain + MAF → shipped), Done/Next, and Run.

## Capabilities

### New Capabilities

- `a2a-ports`: LangChain and MAF ports of from-scratch A2A on the shared support-inbox task.

### Modified Capabilities

- (none)

## Impact

- New modules under langchain-lab and maf-lab. README. Scratch unchanged.
