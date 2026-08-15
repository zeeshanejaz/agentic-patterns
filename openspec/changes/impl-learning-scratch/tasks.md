## 1. Shared cases and prompts

- [x] 1.1 Add `LEARNING_CASES` (at least two `{email, rating, correction}` items) and `LEARNING_HELD_OUT` (a distinct support email) to `packages/shared/src/sd_agentic_shared/tasks/support_email.py`
- [x] 1.2 Add `LEARNING_DISTILL_SYSTEM` and `LEARNING_REPLY_SYSTEM` to `packages/shared/src/sd_agentic_shared/prompts.py`, interpolating `POLICY`

## 2. Scratch learning module

- [x] 2.1 Add `packages/patterns/src/sd_agentic_patterns/learning.py`: clean feedback (`MIN_RATING`), distill lessons, baseline vs adapted replies on `LEARNING_HELD_OUT`; print JSON from `main`
- [x] 2.2 Tag traces `pattern:learning` and `backend:scratch`

## 3. README

- [x] 3.1 Flip learning-and-adaptation scratch Progress cell to `done` (leave LangChain/MAF pending); refresh Done/Next; add the scratch learning Run command
