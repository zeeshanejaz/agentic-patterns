## 1. LangChain multi-agent

- [x] 1.1 Add `packages/langchain-lab/src/sd_agentic_langchain/multi_agent.py` with LangGraph nodes `coordinate`, `specialists`, `review`, `write`, the scratch models, and `MAX_ROUNDS = 2`
- [x] 1.2 Copy JSON parse / roster / fallback helpers from scratch; use shared multi-agent prompts; run `SUPPORT_EMAIL` in `main`
- [x] 1.3 Tag traces with `pattern:multi_agent` and `backend:langchain` via `propagate_attributes` and Langfuse `CallbackHandler`

## 2. MAF multi-agent

- [x] 2.1 Add `packages/maf-lab/src/sd_agentic_maf/multi_agent.py` with MAF Agents for coordinator / review / specialists / writer and the same result shape
- [x] 2.2 Copy scratch coordinator loop; print `SUPPORT_EMAIL` result from `main`
- [x] 2.3 Create OTEL span `pattern.multi_agent` with attributes `pattern=multi_agent` and `backend=maf`

## 3. README

- [x] 3.1 Flip multi-agent LangChain and MAF Progress cells to `done`; refresh Done/Next; add Run commands for both multi-agent modules
