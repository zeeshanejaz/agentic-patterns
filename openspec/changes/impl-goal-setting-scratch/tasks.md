## 1. Shared SLA and prompts

- [x] 1.1 Add `SUPPORT_SLA`, `GOAL_SET_SYSTEM`, `GOAL_MONITOR_SYSTEM`, and `GOAL_ADJUST_SYSTEM` to `packages/shared/src/sd_agentic_shared/prompts.py`, interpolating `POLICY`

## 2. Scratch goal-setting module

- [x] 2.1 Add `packages/patterns/src/sd_agentic_patterns/goal_setting.py`: set 3–5 goals, draft → monitor → adjust within `MAX_ATTEMPTS = 3` on `SUPPORT_EMAIL`; print JSON from `main`
- [x] 2.2 Tag traces `pattern:goal_setting` and `backend:scratch`

## 3. README

- [x] 3.1 Flip goal setting and monitoring scratch Progress cell to `done` (leave LangChain/MAF pending); refresh Done/Next; add the scratch goal-setting Run command
