## 1. LangChain tool use

- [x] 1.1 Add `packages/langchain-lab/src/sd_agentic_langchain/tool_use.py` with LangGraph agent ⇄ `ToolNode` cycle, `ToolUseResult`, and `MAX_STEPS = 6`
- [x] 1.2 Bind `lookup_order`, `create_refund`, and `search_docs` from shared; copy scratch SYSTEM prompt; extract call records from messages; run `SUPPORT_EMAIL` in `main`
- [x] 1.3 Tag traces with `pattern:tool_use` and `backend:langchain` via `propagate_attributes` and Langfuse `CallbackHandler`

## 2. MAF tool use

- [x] 2.1 Add `packages/maf-lab/src/sd_agentic_maf/tool_use.py` with a MAF Agent whose tools are the shared fake functions and `ToolUseResult`
- [x] 2.2 Record tool calls via `FunctionMiddleware`; copy scratch SYSTEM prompt; print `SUPPORT_EMAIL` result from `main`
- [x] 2.3 Create OTEL span `pattern.tool_use` with attributes `pattern=tool_use` and `backend=maf`

## 3. README

- [x] 3.1 Flip tool use LangChain and MAF Progress cells to `done`; refresh Done/Next; add Run commands for both tool-use modules
