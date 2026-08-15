## 1. Shared prompts

- [x] 1.1 Add `COORDINATOR_SYSTEM`, `COORDINATOR_REVIEW_SYSTEM`, `BILLING_AGENT_SYSTEM`, `SHIPPING_AGENT_SYSTEM`, `POLICY_AGENT_SYSTEM`, and `WRITER_AGENT_SYSTEM` to `packages/shared/src/sd_agentic_shared/prompts.py`, interpolating `POLICY`

## 2. Scratch multi-agent module

- [x] 2.1 Add `packages/patterns/src/sd_agentic_patterns/multi_agent.py` that asks the coordinator for JSON assignments from roster `billing` / `shipping` / `policy` (fallback: assign all three)
- [x] 2.2 Run specialists onto a shared notes board; allow one extra coordinator review round (`MAX_ROUNDS = 2`); writer produces the customer reply from the board
- [x] 2.3 Tag traces `pattern:multi_agent` and `backend:scratch`; run `SUPPORT_EMAIL` in `main`

## 3. README

- [x] 3.1 Flip multi-agent scratch Progress cell to `done` (leave LangChain/MAF pending); refresh Done/Next; add the scratch multi-agent Run command
