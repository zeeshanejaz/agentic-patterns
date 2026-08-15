## 1. LangChain learning

- [x] 1.1 Add `packages/langchain-lab/src/sd_agentic_langchain/learning.py` with Python clean (`MIN_RATING`, poison filters) and LCEL chains for distill and reply
- [x] 1.2 Use `LEARNING_CASES`, `LEARNING_HELD_OUT`, and shared learning prompts; print baseline vs adapted JSON in `main`
- [x] 1.3 Tag traces with `pattern:learning` and `backend:langchain` via `propagate_attributes` and Langfuse `CallbackHandler`

## 2. MAF learning

- [x] 2.1 Add `packages/maf-lab/src/sd_agentic_maf/learning.py` with MAF Agents for distill / reply and the same clean / result shape
- [x] 2.2 Copy scratch clean → distill → A/B loop over `LEARNING_CASES` / `LEARNING_HELD_OUT`; print JSON from `main`
- [x] 2.3 Create OTEL span `pattern.learning` with attributes `pattern=learning` and `backend=maf`

## 3. README

- [x] 3.1 Flip learning-and-adaptation LangChain and MAF Progress cells to `done`; refresh Done/Next; add Run commands for both learning modules
