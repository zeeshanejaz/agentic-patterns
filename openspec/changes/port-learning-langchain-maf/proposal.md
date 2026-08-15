## Why

Learning and adaptation (#9) already exists from scratch (collect feedback → distill lessons → A/B on a held-out ticket), but LangChain and MAF cells are still pending, so the pattern cannot be diffed three ways in Langfuse.

## What Changes

- Add `sd_agentic_langchain.learning` using LCEL chains for distill and reply (clean stays Python). Same `LEARNING_CASES` / `LEARNING_HELD_OUT` and result shape as scratch.
- Add `sd_agentic_maf.learning` using MAF Agents for distill / reply inside the same Python control flow as scratch.
- Reuse shared learning prompts and cases. Same `MIN_RATING` and poison filters. Do not change scratch.
- Tag traces `pattern:learning` and `backend:langchain` / `backend:maf`.
- Update README Progress (learning LangChain + MAF → done), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `learning-ports`: LangChain and MAF ports of from-scratch learning and adaptation on the shared support-inbox task.

### Modified Capabilities

- (none)

## Impact

- New modules: `packages/langchain-lab/src/sd_agentic_langchain/learning.py`, `packages/maf-lab/src/sd_agentic_maf/learning.py`.
- README Progress / Done / Next / Run.
- No changes to `packages/patterns` or shared prompts/cases (already exist).
