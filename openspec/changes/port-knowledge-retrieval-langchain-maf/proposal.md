## Why

Knowledge retrieval / RAG (#14) already exists from scratch (keyword top-k over policy chunks, cited reply), but LangChain and MAF cells are still pending. LangChain retrievers are the teaching surface for this pattern.

## What Changes

- Add `sd_agentic_langchain.knowledge_retrieval` using an in-memory vector store over `RAG_CHUNKS` and LCEL retrieve → generate (no StateGraph).
- Add `sd_agentic_maf.knowledge_retrieval` using the same keyword retrieve as scratch plus a MAF Agent for the cited reply.
- Reuse `RAG_CHUNKS`, `RAG_REPLY_SYSTEM`, `SUPPORT_EMAIL`. Same result shape. Do not change scratch.
- Tag traces `pattern:knowledge_retrieval` and `backend:langchain` / `backend:maf`.
- Update README Progress (RAG LangChain + MAF → shipped), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `knowledge-retrieval-ports`: LangChain and MAF ports of from-scratch RAG on the shared support-inbox task.

### Modified Capabilities

- (none)

## Impact

- New modules: `packages/langchain-lab/src/sd_agentic_langchain/knowledge_retrieval.py`, `packages/maf-lab/src/sd_agentic_maf/knowledge_retrieval.py`.
- README Progress / Done / Next / Run.
- No new workspace dependencies. No changes to `packages/patterns`.
