## 1. LangChain exception handling

- [x] 1.1 Add `packages/langchain-lab/src/sd_agentic_langchain/exception_handling.py` wrapping the tool-use LangGraph with Recovery (two lookup timeouts, retries, fallback, MAX_EVENTS stop)
- [x] 1.2 Use `SUPPORT_EMAIL` and `EXCEPTION_FALLBACK_SYSTEM`; print JSON with `events`, `calls`, `reply`, `stopped` in `main`
- [x] 1.3 Tag traces with `pattern:exception_handling` and `backend:langchain` via `propagate_attributes` and Langfuse `CallbackHandler`

## 2. MAF exception handling

- [x] 2.1 Add `packages/maf-lab/src/sd_agentic_maf/exception_handling.py` wrapping MAF Agent tools with the same Recovery / result shape
- [x] 2.2 Print JSON from `main`; catch CriticalError and write the fallback reply
- [x] 2.3 Create OTEL span `pattern.exception_handling` with attributes `pattern=exception_handling` and `backend=maf`

## 3. README

- [x] 3.1 Flip exception handling LangChain and MAF Progress cells to `done`; refresh Done/Next; add Run commands for both modules
