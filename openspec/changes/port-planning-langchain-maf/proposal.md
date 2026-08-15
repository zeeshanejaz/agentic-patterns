## Why

Planning (#6) already exists from scratch (plan DAG → execute → replan once if blocked), but LangChain and MAF cells are still pending, so the pattern cannot be diffed three ways in Langfuse.

## What Changes

- Add `sd_agentic_langchain.planning` using LangGraph for the outer plan → execute-step → optional replan cycle, with the same shared planning prompts and fake tools as scratch.
- Add `sd_agentic_maf.planning` using MAF Agents for planner / repair / step / replan inside the same Python control flow as scratch.
- Reuse `PLAN_SYSTEM`, `PLAN_REPAIR_SYSTEM`, `PLAN_STEP_SYSTEM`, `PLAN_REPLAN_SYSTEM`. Same result shape (`plan`, `execution`, `replans`, `reply`). Tool steps call `sd_agentic_shared.tools.call_tool`. Cap at `MAX_REPLANS = 1`.
- Tag traces `pattern:planning` and `backend:langchain` / `backend:maf`.
- Update README Progress (planning LangChain + MAF → done), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `planning-ports`: LangChain and MAF ports of from-scratch planning on the shared support-inbox task, keeping plan-first DAG execution and one replan on blocked checkpoints.

### Modified Capabilities

- (none)

## Impact

- New modules: `packages/langchain-lab/src/sd_agentic_langchain/planning.py`, `packages/maf-lab/src/sd_agentic_maf/planning.py`.
- README Progress / Done / Next / Run.
- No changes to `packages/patterns` or shared prompts (already exist). No new fake tools.
