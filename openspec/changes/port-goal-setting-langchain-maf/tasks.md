## 1. LangChain goal setting

- [x] 1.1 Add `packages/langchain-lab/src/sd_agentic_langchain/goal_setting.py` with LangGraph nodes `set_goals`, `adjust`, `monitor`, `MAX_ATTEMPTS = 3`, and the scratch result shape
- [x] 1.2 Use `SUPPORT_EMAIL` and shared SLA/goal prompts; loop on failed goals until PASS or budget; print JSON in `main`
- [x] 1.3 Tag traces with `pattern:goal_setting` and `backend:langchain` via `propagate_attributes` and Langfuse `CallbackHandler`

## 2. MAF goal setting

- [x] 2.1 Add `packages/maf-lab/src/sd_agentic_maf/goal_setting.py` with MAF Agents for set / adjust / monitor and the same result shape
- [x] 2.2 Copy scratch set → adjust → monitor loop over `SUPPORT_EMAIL`; print JSON from `main`
- [x] 2.3 Create OTEL span `pattern.goal_setting` with attributes `pattern=goal_setting` and `backend=maf`

## 3. README

- [x] 3.1 Flip goal setting and monitoring LangChain and MAF Progress cells to `done`; refresh Done/Next; add Run commands for both goal-setting modules
