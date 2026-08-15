## 1. LangChain planning

- [x] 1.1 Add `packages/langchain-lab/src/sd_agentic_langchain/planning.py` with LangGraph nodes `plan`, `execute`, `replan`, `reply`, the scratch plan/step models, and `MAX_REPLANS = 1`
- [x] 1.2 Copy JSON parse / repair / fallback / topo / blocked helpers from scratch; use shared planning prompts and `call_tool`; run `SUPPORT_EMAIL` in `main`
- [x] 1.3 Tag traces with `pattern:planning` and `backend:langchain` via `propagate_attributes` and Langfuse `CallbackHandler`

## 2. MAF planning

- [x] 2.1 Add `packages/maf-lab/src/sd_agentic_maf/planning.py` with MAF Agents for planner / repair / step / replan and the same result shape
- [x] 2.2 Execute tool steps via `call_tool`; copy scratch DAG / replan control flow; print `SUPPORT_EMAIL` result from `main`
- [x] 2.3 Create OTEL span `pattern.planning` with attributes `pattern=planning` and `backend=maf`

## 3. README

- [x] 3.1 Flip planning LangChain and MAF Progress cells to `done`; refresh Done/Next; add Run commands for both planning modules
