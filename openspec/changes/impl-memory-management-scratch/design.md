## Context

The pattern classifies information as short-term, episodic, or long-term, stores recency/relevance, and retrieves without overflowing the context window. Existing labs are single-shot one email. Memory needs a **multi-turn thread** from the same customer so later turns can use earlier facts (order ids, refund vs shipping preference) without asking again.

## Goals / Non-Goals

**Goals:**

- Scratch module `memory_management` with Langfuse tags `pattern:memory_management`, `backend:scratch`.
- In-memory three-tier store: short-term = current email; episodic = per-turn summaries; long-term = durable facts.
- Each turn: retrieve → reply under POLICY → extract new memories → drop oldest episodic if over cap.
- Shared `MEMORY_THREAD` (SUPPORT_EMAIL plus two follow-ups) and prompts.
- README scratch cell done; Next points at memory ports or learning-and-adaptation scratch.

**Non-Goals:**

- LangChain / MAF ports (including LangGraph checkpointers).
- Vector DB / embeddings (RAG is #14). Learning from ratings (#9).
- Real persistence, PII vaults, or cross-process sync.
- Changing existing fake tool data.

## Decisions

1. **In-process lists, not a database.** Teaching surface is classify / retrieve / compact, not infra.

2. **Caps:** short-term is replaced every turn. Episodic keeps the last `MAX_EPISODIC = 2` summaries (drop oldest). Long-term keeps at most `MAX_LONG_TERM = 8` facts (skip duplicates, drop oldest if over).

3. **Retrieve** concatenates all long-term facts plus remaining episodic items. No embeddings. Recency is list order.

4. **Extract** is one JSON `complete()` per turn: `{episodic, long_term: [..]}`. Parse failure → episodic = first 200 chars of the email, no new long-term.

5. **`MEMORY_THREAD`** is three related emails in `support_email.py` so the demo shows recall (order ids) and an update (customer drops the refund ask).

## Risks / Trade-offs

- [Looks like prompt chaining] → state survives across turns; later replies must be able to use stored order ids.
- [JSON fragility] → fallback episodic snippet, skip long-term.
- [Stale long-term] → extract prompt says to record preference changes (e.g. refund withdrawn).

## Migration Plan

Add module + prompts + thread + README. Rollback is delete those.

## Open Questions

None.
