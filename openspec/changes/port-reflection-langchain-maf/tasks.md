## 1. LangChain reflection

- [x] 1.1 Add `packages/langchain-lab/src/sd_agentic_langchain/reflection.py` with LangGraph summarize → draft → critic ⇄ revise cycle, `MAX_ROUNDS = 3`, and `ReflectionResult`
- [x] 1.2 Wire shared summarize/draft/critic/revise prompts; PASS via `startswith("PASS")`; run `SUPPORT_EMAIL` in `main`
- [x] 1.3 Tag traces with `pattern:reflection` and `backend:langchain` via `propagate_attributes` and Langfuse `CallbackHandler`

## 2. MAF reflection

- [x] 2.1 Add `packages/maf-lab/src/sd_agentic_maf/reflection.py` with MAF Agents in the same Python critic/revise loop and `ReflectionResult`
- [x] 2.2 Use shared prompts, `MAX_ROUNDS = 3`, and the same PASS rule; print `SUPPORT_EMAIL` result from `main`
- [x] 2.3 Create OTEL span `pattern.reflection` with attributes `pattern=reflection` and `backend=maf`

## 3. README

- [x] 3.1 Flip reflection LangChain and MAF Progress cells to `done`; refresh Done/Next; add Run commands for both reflection modules
