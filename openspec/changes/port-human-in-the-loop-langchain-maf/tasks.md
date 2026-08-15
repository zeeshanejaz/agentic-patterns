## 1. LangChain HITL

- [x] 1.1 Add `packages/langchain-lab/src/sd_agentic_langchain/human_in_the_loop.py` with LangGraph nodes summarize / draft / gate / human (`interrupt`) / resume and a MemorySaver checkpointer
- [x] 1.2 Resume with canned `HITL_DECISION`; print JSON from `main`
- [x] 1.3 Tag traces with `pattern:human_in_the_loop` and `backend:langchain` via `propagate_attributes` and Langfuse `CallbackHandler`

## 2. MAF HITL

- [x] 2.1 Add `packages/maf-lab/src/sd_agentic_maf/human_in_the_loop.py` with MAF Agents for summarize / draft / gate / resume and the canned reviewer
- [x] 2.2 Print JSON from `main`
- [x] 2.3 Create OTEL span `pattern.human_in_the_loop` with attributes `pattern=human_in_the_loop` and `backend=maf`

## 3. README

- [x] 3.1 Flip human-in-the-loop LangChain and MAF Progress cells to `done`; refresh Done/Next; add Run commands for both HITL modules
