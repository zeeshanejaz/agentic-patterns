## 1. Shared prompt

- [x] 1.1 Add `A2A_MESSAGE_SYSTEM` to `packages/shared/src/sd_agentic_shared/prompts.py`

## 2. Scratch A2A module

- [x] 2.1 Add `packages/patterns/src/sd_agentic_patterns/a2a.py` with an envelope bus, TTL, `MAX_MESSAGES = 8`, coordinator → billing/shipping → writer on `SUPPORT_EMAIL`
- [x] 2.2 Tag traces `pattern:a2a` and `backend:scratch`

## 3. README

- [x] 3.1 Flip A2A scratch Progress cell to shipped (leave LangChain/MAF pending); refresh Done/Next; add the scratch A2A Run command
