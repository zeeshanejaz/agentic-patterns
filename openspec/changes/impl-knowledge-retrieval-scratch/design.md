## Context

RAG parses/chunks documents, retrieves top-k, generates a grounded answer with citations. `search_docs` is a single blob lookup, not retrieval. Scratch should not need a vector DB — keyword overlap is enough to invent the loop. LangChain later owns embeddings/retrievers.

## Goals / Non-Goals

**Goals:**

- Scratch module `knowledge_retrieval`, tags `pattern:knowledge_retrieval`, `backend:scratch`.
- Shared `RAG_CHUNKS` (at least 6 policy snippets with ids). Retrieve top `K = 3` by token overlap. Generate under POLICY with citations to chunk ids.
- Print JSON: `query`, `retrieved` (id, score, text), `reply`.
- README scratch cell shipped (file link, matching the Progress table convention); Next points at RAG ports.

**Non-Goals:**

- LangChain retrievers / embeddings (ports).
- Vector databases, rerankers, query rewriting.
- Changing `tools.py` DOCS.
- Agentic RAG (retrieve-then-decide loops).

## Decisions

1. **Keyword overlap, not embeddings.** Teaching surface is retrieve-then-ground, not ANN search.

2. **Corpus in shared, not tools.DOCS.** Chunks are citable `{id, title, text}` about refunds, shipping, cancel, duplicate charges, tracking, tone.

3. **K = 3.** Enough to show ranking; not so many that the model ignores them.

4. **Module name `knowledge_retrieval`.**

## Risks / Trade-offs

- [Looks like search_docs] → multiple chunks + scores + citations vs one concatenated string.
- [Hallucinated citations] → prompt forbids citing ids that were not retrieved.

## Migration Plan

Add module + corpus + prompt + README. Rollback is delete those.

## Open Questions

None.
