## 1. Shared fallback prompt

- [x] 1.1 Add `EXCEPTION_FALLBACK_SYSTEM` to `packages/shared/src/sd_agentic_shared/prompts.py`, interpolating `POLICY`

## 2. Scratch exception-handling module

- [x] 2.1 Add `packages/patterns/src/sd_agentic_patterns/exception_handling.py` wrapping the tool-use loop: inject two `lookup_order` timeouts, classify, retry (`MAX_RETRIES = 2`), fallback, emergency-stop at `MAX_EVENTS`; print JSON from `main`
- [x] 2.2 Tag traces `pattern:exception_handling` and `backend:scratch`

## 3. README

- [x] 3.1 Flip exception handling and recovery scratch Progress cell to `done` (leave LangChain/MAF pending); refresh Done/Next; add the scratch exception-handling Run command
