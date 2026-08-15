## Context

Scratch memory keeps short-term / episodic / long-term lists over `MEMORY_THREAD`, retrieving before each reply and compacting to `MAX_EPISODIC = 2` and `MAX_LONG_TERM = 8`. Shared prompts and the thread already exist.

## Goals / Non-Goals

**Goals:**

- Same store semantics, same caps, same result shape, same module name `memory_management`.
- LangGraph encodes one turn (retrieve → reply → extract) and loops until the thread is empty.
- MAF uses Agent.run for reply / extract inside the same control flow as scratch.
- Tags `pattern:memory_management` and `backend:langchain` / `backend:maf`.
- README cells and run commands.

**Non-Goals:**

- Changing scratch, prompts, or `MEMORY_THREAD`.
- Vector stores / LangGraph checkpointers as the memory (the in-memory lists are the teaching surface).
- RAG (#14) or learning from ratings (#9).

## Decisions

1. **Both labs in one change.** One store, two small modules.

2. **LangChain: LangGraph turn cycle.** State holds remaining emails, turn index, store lists, accumulated results. Nodes: `ingest` (pop next email into short-term), `retrieve`, `reply`, `extract` (parse JSON, compact). After extract, loop to `ingest` if emails remain else END.

   Alternative: Python for-loop of LCEL — rejected; would not show LangGraph cycles.

3. **MAF: Python for-loop of Agents.** Reply and extract are Agents. Store class copied from scratch. Parent span `pattern.memory_management` with `pattern` / `backend` attributes.

4. **CLI runs `MEMORY_THREAD`**, same as scratch.

## Risks / Trade-offs

- [JSON fragility] → same fallback as scratch (episodic snippet, no new long-term).
- [Checkpointer temptation] → keep explicit lists so Langfuse diffs show the same store shape.

## Migration Plan

Add two modules and README lines. Rollback is delete + revert README.

## Open Questions

None.
