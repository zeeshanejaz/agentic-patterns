## Why

Goal setting and monitoring (#11) already exists from scratch (set KPIs → score → adjust within a budget), but LangChain and MAF cells are still pending, so the pattern cannot be diffed three ways in Langfuse.

## What Changes

- Add `sd_agentic_langchain.goal_setting` using LangGraph for the set-goals → adjust → monitor cycle (unknown iteration, progress in graph state).
- Add `sd_agentic_maf.goal_setting` using MAF Agents for set / adjust / monitor inside the same Python control flow as scratch.
- Reuse `SUPPORT_SLA`, goal prompts, `SUPPORT_EMAIL`, `MAX_ATTEMPTS = 3`, fallback goals, and the same result shape. Do not change scratch.
- Tag traces `pattern:goal_setting` and `backend:langchain` / `backend:maf`.
- Update README Progress (goal-setting LangChain + MAF → done), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `goal-setting-ports`: LangChain and MAF ports of from-scratch goal setting and monitoring on the shared support-inbox task.

### Modified Capabilities

- (none)

## Impact

- New modules: `packages/langchain-lab/src/sd_agentic_langchain/goal_setting.py`, `packages/maf-lab/src/sd_agentic_maf/goal_setting.py`.
- README Progress / Done / Next / Run.
- No changes to `packages/patterns` or shared prompts (already exist).
