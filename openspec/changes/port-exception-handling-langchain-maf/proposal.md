## Why

Exception handling (#12) already exists from scratch (wrap tool use: classify, retry, fallback, emergency-stop), but LangChain and MAF cells are still pending, so the pattern cannot be diffed three ways in Langfuse.

## What Changes

- Add `sd_agentic_langchain.exception_handling` wrapping the existing LangGraph tool-use loop: tools run through the same Recovery (injected lookup timeouts, retries, `search_docs` fallback, max-events stop).
- Add `sd_agentic_maf.exception_handling` wrapping the MAF tool-use Agent with the same Recovery around bound functions.
- Reuse `EXCEPTION_FALLBACK_SYSTEM`, `POLICY`, `SUPPORT_EMAIL`, and the same result shape (`events`, `calls`, `reply`, `stopped`). Do not change scratch or fake tool implementations.
- Tag traces `pattern:exception_handling` and `backend:langchain` / `backend:maf`.
- Update README Progress (exception-handling LangChain + MAF → done), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `exception-handling-ports`: LangChain and MAF ports of from-scratch exception handling wrapping the tool-use support loop.

### Modified Capabilities

- (none)

## Impact

- New modules: `packages/langchain-lab/src/sd_agentic_langchain/exception_handling.py`, `packages/maf-lab/src/sd_agentic_maf/exception_handling.py`.
- README Progress / Done / Next / Run.
- No changes to `packages/patterns` or `packages/shared` tools.
