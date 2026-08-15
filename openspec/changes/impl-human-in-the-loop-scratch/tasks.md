## 1. Shared prompts and canned decision

- [x] 1.1 Add `HITL_DECISION` to `packages/shared/src/sd_agentic_shared/tasks/support_email.py`
- [x] 1.2 Add `HITL_GATE_SYSTEM` and `HITL_RESUME_SYSTEM` to `packages/shared/src/sd_agentic_shared/prompts.py`, interpolating `POLICY`

## 2. Scratch HITL module

- [x] 2.1 Add `packages/patterns/src/sd_agentic_patterns/human_in_the_loop.py`: summarize → draft → gate → reviewer callback → resume; print JSON from `main` using canned `HITL_DECISION`
- [x] 2.2 Tag traces `pattern:human_in_the_loop` and `backend:scratch`

## 3. README

- [x] 3.1 Flip human-in-the-loop scratch Progress cell to `done` (leave LangChain/MAF pending); refresh Done/Next; add the scratch HITL Run command
