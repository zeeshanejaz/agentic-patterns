## Context

Scratch exception handling wraps tool execution: first two `lookup_order` calls timeout, transients retry (`MAX_RETRIES = 2`), permanent/exhausted → `search_docs` fallback, `MAX_EVENTS` → emergency-stop. Shared `EXCEPTION_FALLBACK_SYSTEM` exists. LangChain README: LCEL retry/fallback is good; graph for workflow-level recovery edges. This wraps the existing tool-use graphs rather than cloning a new inbox task.

## Goals / Non-Goals

**Goals:**

- Same Recovery semantics, same result shape, same module name `exception_handling`.
- LangChain: LangGraph agent ⇄ tools, but tool functions call Recovery (retry/fallback). CriticalError stops the graph and writes a fallback reply.
- MAF: Agent with wrapped tools (or middleware) using the same Recovery.
- Tags `pattern:exception_handling` and `backend:langchain` / `backend:maf`.
- README cells and run commands.

**Non-Goals:**

- Changing scratch, `tools.py`, or `EXCEPTION_FALLBACK_SYSTEM`.
- Real backoff sleeps (`BACKOFF_SECONDS = 0`).
- HITL / guardrails / evaluation.

## Decisions

1. **Both labs in one change.** One Recovery wrapper, two modules.

2. **LangChain: wrap tools, keep ToolNode graph.** `StructuredTool` functions call `Recovery.execute`. Custom tools node (or wrapped functions) catch `CriticalError`, set `stopped`, invoke fallback prompt. Do not reimplement the agent loop as a Python `while` around LCEL.

3. **MAF: wrap the three functions** so `Agent(..., tools=[...])` still owns the call loop; Recovery is inside the wrappers. Catch `CriticalError` around `agent.run` and write the fallback reply.

4. **Copy Recovery** (timeouts, retries, fallback, MAX_EVENTS) from scratch into each lab, like the memory store was copied.

## Risks / Trade-offs

- [Looks like tool use] → teaching surface is `events` (retry/fallback/stop), not the tool list.
- [LLM may skip lookup_order] → same SUPPORT_EMAIL as tool use; empty events still a valid run.

## Migration Plan

Add two modules and README lines. Rollback is delete + revert README.

## Open Questions

None.
