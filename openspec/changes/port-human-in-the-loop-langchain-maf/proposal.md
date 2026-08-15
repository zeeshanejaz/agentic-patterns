## Why

Human-in-the-loop (#13) already exists from scratch (gate → reviewer callback → resume), but LangChain and MAF cells are still pending. LangGraph `interrupt()` is the teaching surface for this pattern.

## What Changes

- Add `sd_agentic_langchain.human_in_the_loop` using LangGraph with a checkpointer and `interrupt()` at the gate; resume with canned `HITL_DECISION`.
- Add `sd_agentic_maf.human_in_the_loop` using MAF Agents for summarize / draft / gate / resume and the same canned reviewer callback as scratch.
- Reuse shared HITL prompts, `HITL_DECISION`, and `SUPPORT_EMAIL`. Same result shape. Do not change scratch.
- Tag traces `pattern:human_in_the_loop` and `backend:langchain` / `backend:maf`.
- Update README Progress (HITL LangChain + MAF → done), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `human-in-the-loop-ports`: LangChain and MAF ports of from-scratch HITL on the shared support-inbox task.

### Modified Capabilities

- (none)

## Impact

- New modules: `packages/langchain-lab/src/sd_agentic_langchain/human_in_the_loop.py`, `packages/maf-lab/src/sd_agentic_maf/human_in_the_loop.py`.
- README Progress / Done / Next / Run.
- No changes to `packages/patterns` or shared prompts/decision (already exist).
