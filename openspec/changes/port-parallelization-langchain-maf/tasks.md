## 1. LangChain parallelization

- [x] 1.1 Add `packages/langchain-lab/src/sd_agentic_langchain/parallelization.py` with LangGraph sectioning (three fan-out extractors then merge) and voting (three draft nodes then merge), plus `SectionResult` and `VoteResult`
- [x] 1.2 Wire shared section/merge/vote-merge prompts; copy scratch voting worker prompt text; use `SUPPORT_EMAIL` in `main`; voting drafts at temperature 0.8
- [x] 1.3 Tag traces with `pattern:parallelization` and `backend:langchain` via `propagate_attributes` and Langfuse `CallbackHandler`

## 2. MAF parallelization

- [x] 2.1 Add `packages/maf-lab/src/sd_agentic_maf/parallelization.py` with `ConcurrentBuilder` sectioning and voting, merge Agents, and the same result models
- [x] 2.2 Use shared prompts and scratch voting worker text; identify worker outputs by agent name; print both modes from `main`
- [x] 2.3 Create OTEL spans `pattern.parallelization.sectioning` and `pattern.parallelization.voting` with attributes `pattern=parallelization` and `backend=maf`

## 3. README

- [x] 3.1 Flip parallelization LangChain and MAF Progress cells to `done`; refresh Done/Next; add Run commands for both parallelization modules
