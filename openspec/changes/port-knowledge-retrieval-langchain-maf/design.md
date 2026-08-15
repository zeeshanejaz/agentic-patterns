## Context

Scratch RAG ranks `RAG_CHUNKS` by token overlap (`K = 3`) then generates a cited reply. LangChain README: classic RAG is LCEL retrieve | gen; graph only for agentic RAG.

## Goals / Non-Goals

**Goals:**

- Same result shape `{query, retrieved, reply}`, same module name `knowledge_retrieval`.
- LangChain: `InMemoryVectorStore` + `OpenAIEmbeddings` over the shared chunks; LCEL prompt | llm | parser for generation. No StateGraph.
- MAF: copy scratch keyword retrieve; Agent writes the cited reply.
- Tags `pattern:knowledge_retrieval` and `backend:langchain` / `backend:maf`.
- README cells and run commands.

**Non-Goals:**

- Changing scratch or the corpus.
- External vector DBs, rerankers, query rewrite.
- Agentic RAG graphs.

## Decisions

1. **Both labs in one change.** Tiny corpus; two modules.

2. **LangChain: embeddings + LCEL.** That is what the lab README says LangChain wins at. Documents use chunk `id` as metadata.

3. **MAF: keyword retrieve.** MAF has no retriever primitive here; showing Agents on already-retrieved chunks is honest.

4. **K = 3** in both.

## Risks / Trade-offs

- [Embedding ranking ≠ keyword ranking] → expected; traces will differ.
- [Embedding API cost] → seven short chunks, one query.

## Migration Plan

Add two modules and README lines. Rollback is delete + revert README.

## Open Questions

None.
