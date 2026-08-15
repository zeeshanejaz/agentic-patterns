## 1. LangChain routing

- [x] 1.1 Add `packages/langchain-lab/src/sd_agentic_langchain/routing.py` with LangGraph classify node, conditional edges to four handler nodes, first-token intent parse with `other` fallback, and `RouteResult(intent, reply)`
- [x] 1.2 Wire `ChatPromptTemplate` chains to `ROUTE_SYSTEM` and the four shared handler prompts; iterate `SAMPLE_EMAILS` in `main`
- [x] 1.3 Tag traces with `pattern:routing` and `backend:langchain` via `propagate_attributes` and Langfuse `CallbackHandler`

## 2. MAF routing

- [x] 2.1 Add `packages/maf-lab/src/sd_agentic_maf/routing.py` with a router `Agent` plus four specialist `Agent`s, first-token intent parse with `other` fallback, and `RouteResult(intent, reply)`
- [x] 2.2 Run exactly one specialist per email using shared prompts; reuse `configure_maf_otel` and `OpenAIChatClient` like prompt chaining; iterate `SAMPLE_EMAILS` in `main`
- [x] 2.3 Create OTEL span `pattern.routing` with attributes `pattern=routing` and `backend=maf`

## 3. README

- [x] 3.1 Flip routing LangChain and MAF Progress cells to `done`; refresh Done/Next; add Run commands for both routing modules
