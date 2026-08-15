## 1. LangChain RAG

- [x] 1.1 Add `packages/langchain-lab/src/sd_agentic_langchain/knowledge_retrieval.py` with `InMemoryVectorStore` over `RAG_CHUNKS` and LCEL generation (`K = 3`)
- [x] 1.2 Use `SUPPORT_EMAIL` and `RAG_REPLY_SYSTEM`; print JSON from `main`
- [x] 1.3 Tag traces with `pattern:knowledge_retrieval` and `backend:langchain` via `propagate_attributes` and Langfuse `CallbackHandler`

## 2. MAF RAG

- [x] 2.1 Add `packages/maf-lab/src/sd_agentic_maf/knowledge_retrieval.py` with keyword top-k retrieve and a MAF Agent for the cited reply
- [x] 2.2 Print JSON from `main`
- [x] 2.3 Create OTEL span `pattern.knowledge_retrieval` with attributes `pattern=knowledge_retrieval` and `backend=maf`

## 3. README

- [x] 3.1 Flip knowledge-retrieval LangChain and MAF Progress cells to shipped; refresh Done/Next; add Run commands for both RAG modules
