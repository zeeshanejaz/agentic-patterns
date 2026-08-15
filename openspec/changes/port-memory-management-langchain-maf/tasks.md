## 1. LangChain memory management

- [x] 1.1 Add `packages/langchain-lab/src/sd_agentic_langchain/memory_management.py` with LangGraph nodes `ingest`, `retrieve`, `reply`, `extract`, the scratch store caps, and turn results
- [x] 1.2 Use `MEMORY_THREAD` and shared memory prompts; compact oldest episodic/long-term items; print per-turn JSON in `main`
- [x] 1.3 Tag traces with `pattern:memory_management` and `backend:langchain` via `propagate_attributes` and Langfuse `CallbackHandler`

## 2. MAF memory management

- [x] 2.1 Add `packages/maf-lab/src/sd_agentic_maf/memory_management.py` with MAF Agents for reply / extract and the same store / result shape
- [x] 2.2 Copy scratch retrieve → reply → extract loop over `MEMORY_THREAD`; print per-turn JSON from `main`
- [x] 2.3 Create OTEL span `pattern.memory_management` with attributes `pattern=memory_management` and `backend=maf`

## 3. README

- [x] 3.1 Flip memory management LangChain and MAF Progress cells to `done`; refresh Done/Next; add Run commands for both memory modules
