## Why

Resource-aware (#16) exists from scratch but LangChain and MAF cells are pending. LCEL `RunnableBranch` is the teaching surface.

## What Changes

- Add `sd_agentic_langchain.resource_aware` with LCEL classify + `RunnableBranch` cheap/expensive (no StateGraph).
- Add `sd_agentic_maf.resource_aware` with MAF Agents for classify / cheap / expensive.
- Same prompts, SAMPLE_EMAILS, result shape. Tags `pattern:resource_aware`. README shipped links.

## Capabilities

### New Capabilities

- `resource-aware-ports`: LangChain and MAF ports of cheap/expensive support routing.

### Modified Capabilities

- (none)

## Impact

- Two new modules + README. Scratch unchanged.
