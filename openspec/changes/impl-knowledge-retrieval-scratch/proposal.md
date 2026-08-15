## Why

Knowledge retrieval / RAG (#14) is the next scratch pattern: HITL (#13) is implemented and ported. Scratch must invent chunk → retrieve top-k → generate with citations before LangChain retrievers hide it.

## What Changes

- Add `sd_agentic_patterns.knowledge_retrieval`: in-memory support-policy chunks, keyword top-k retrieval, grounded reply with citations. No vector database.
- Add shared `RAG_CHUNKS` and a generate-with-citations prompt so later ports reuse them. Same `SUPPORT_EMAIL` task.
- Do not invent order facts; do not promise refunds over $50. Cite retrieved chunks; if a fact is not in chunks, say so.
- Tag traces `pattern:knowledge_retrieval` and `backend:scratch`.
- Update README Progress (RAG scratch → shipped; LangChain/MAF stay pending), Done/Next, and Run commands.

## Capabilities

### New Capabilities

- `knowledge-retrieval-scratch`: From-scratch RAG on the shared support-inbox task: chunked corpus, top-k retrieve, cited reply.

### Modified Capabilities

- (none)

## Impact

- New module: `packages/patterns/src/sd_agentic_patterns/knowledge_retrieval.py`.
- New corpus + prompt in `packages/shared`.
- README Progress / Done / Next / Run.
- `packages/patterns` still must not import LangChain or MAF. No ports this change.
