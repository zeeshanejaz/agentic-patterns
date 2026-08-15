## Why

Parallelization (#3) already exists from scratch (sectioning and voting), but LangChain and MAF cells are still pending, so the pattern cannot be diffed three ways in Langfuse. Ports of existing scratch come before new scratch patterns.

## What Changes

- Add `sd_agentic_langchain.parallelization` with LangGraph fan-out/fan-in for sectioning (order / payment / ask → merge) and voting (N drafts → merge).
- Add `sd_agentic_maf.parallelization` using `ConcurrentBuilder` for the parallel workers, then a sequential merge Agent.
- Reuse shared section/merge/vote-merge prompts and `SUPPORT_EMAIL`. Same `SectionResult` / `VoteResult` shapes as scratch. Voting worker prompt stays the same inline text as scratch (not a new shared prompt).
- Tag traces `pattern:parallelization` and `backend:langchain` / `backend:maf`.
- Update README Progress (parallelization LangChain + MAF → done), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `parallelization-ports`: LangChain and MAF ports of from-scratch parallelization (sectioning + voting) on the shared support-inbox task.

### Modified Capabilities

- (none)

## Impact

- New modules: `packages/langchain-lab/src/sd_agentic_langchain/parallelization.py`, `packages/maf-lab/src/sd_agentic_maf/parallelization.py`.
- README Progress / Done / Next / Run.
- No changes to `packages/patterns`. No new shared prompts. No MCP work.
