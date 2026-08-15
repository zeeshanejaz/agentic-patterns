## Why

Tool use (#5) already exists from scratch (and as an MCP variant), but LangChain and MAF cells are still pending, so the pattern cannot be diffed three ways in Langfuse.

## What Changes

- Add `sd_agentic_langchain.tool_use` using LangGraph `ToolNode` bound to the shared fake tools (`lookup_order`, `create_refund`, `search_docs`).
- Add `sd_agentic_maf.tool_use` using a MAF `Agent` with those same functions as tools (the framework owns the call loop).
- Reuse `POLICY` and the same system instructions as scratch. Same `ToolUseResult` shape (`calls`, `reply`). Cap at `MAX_STEPS = 6` model turns where the lab exposes a cap.
- Tag traces `pattern:tool_use` and `backend:langchain` / `backend:maf`.
- Update README Progress (tool use LangChain + MAF → done), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `tool-use-ports`: LangChain and MAF ports of from-scratch tool use on the shared support-inbox task with the same in-memory fake tools.

### Modified Capabilities

- (none)

## Impact

- New modules: `packages/langchain-lab/src/sd_agentic_langchain/tool_use.py`, `packages/maf-lab/src/sd_agentic_maf/tool_use.py`.
- README Progress / Done / Next / Run.
- No changes to `packages/patterns` or MCP lab. No new fake tools.
