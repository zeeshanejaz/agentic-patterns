## 1. Shared thread and prompts

- [x] 1.1 Add `MEMORY_THREAD` (SUPPORT_EMAIL plus two follow-ups) to `packages/shared/src/sd_agentic_shared/tasks/support_email.py`
- [x] 1.2 Add `MEMORY_EXTRACT_SYSTEM` and `MEMORY_REPLY_SYSTEM` to `packages/shared/src/sd_agentic_shared/prompts.py`, interpolating `POLICY`

## 2. Scratch memory module

- [x] 2.1 Add `packages/patterns/src/sd_agentic_patterns/memory_management.py` with an in-memory three-tier store, `MAX_EPISODIC = 2`, `MAX_LONG_TERM = 8`
- [x] 2.2 Each turn: retrieve → reply → extract JSON memories → compact; print per-turn JSON from `MEMORY_THREAD` in `main`
- [x] 2.3 Tag traces `pattern:memory_management` and `backend:scratch`

## 3. README

- [x] 3.1 Flip memory management scratch Progress cell to `done` (leave LangChain/MAF pending); refresh Done/Next; add the scratch memory Run command
