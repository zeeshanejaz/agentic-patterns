## 1. Shared corpus and prompt

- [x] 1.1 Add `packages/shared/src/sd_agentic_shared/corpus.py` with at least six `RAG_CHUNKS` (`id`, `title`, `text`)
- [x] 1.2 Add `RAG_REPLY_SYSTEM` to `packages/shared/src/sd_agentic_shared/prompts.py`, interpolating `POLICY`

## 2. Scratch RAG module

- [x] 2.1 Add `packages/patterns/src/sd_agentic_patterns/knowledge_retrieval.py`: keyword top-`K=3` retrieve then cited reply on `SUPPORT_EMAIL`; print JSON from `main`
- [x] 2.2 Tag traces `pattern:knowledge_retrieval` and `backend:scratch`

## 3. README

- [x] 3.1 Flip knowledge-retrieval scratch Progress cell to shipped (leave LangChain/MAF pending); refresh Done/Next; add the scratch RAG Run command
