## Context

Scratch learning cleans simulated supervisor feedback, distills a lessons block, then A/B's POLICY-only vs POLICY+lessons replies on `LEARNING_HELD_OUT`. Shared cases and prompts already exist. LangChain lab README says LCEL is enough for this pattern (known DAG); graph is optional.

## Goals / Non-Goals

**Goals:**

- Same clean/distill/A/B semantics, same result shape, same module name `learning`.
- LangChain: LCEL `prompt | llm | parser` for distill and reply; Python for clean. No StateGraph.
- MAF: Agents for distill / reply inside the same control flow as scratch.
- Tags `pattern:learning` and `backend:langchain` / `backend:maf`.
- README cells and run commands.

**Non-Goals:**

- Changing scratch, prompts, or `LEARNING_CASES` / `LEARNING_HELD_OUT`.
- Fine-tuning, vector stores, or LangGraph (would hide that this is a static DAG).
- Automated scoring (#19) or HITL (#13).

## Decisions

1. **Both labs in one change.** Linear four-step flow; two small modules.

2. **LangChain: LCEL, not LangGraph.** Distill and reply are known-at-write-time chains. Clean is Python. Invoke distill once, then two reply invokes (baseline then adapted). A Python `while` around LCEL is unnecessary because there is no unknown-length loop.

   Alternative: StateGraph for sameness with memory — rejected; lab README says not to force a graph when LCEL is the teaching surface.

3. **MAF: Python sequence of Agents.** Distill and reply are Agents. Clean copied from scratch. Parent span `pattern.learning` with `pattern` / `backend` attributes.

4. **CLI runs default `LEARNING_CASES` + `LEARNING_HELD_OUT`**, same as scratch.

## Risks / Trade-offs

- [Looks like a Python loop of chains] → that is correct for MAF; LangChain still shows LCEL as the LLM units of work.
- [Duplicated clean logic] → copy `MIN_RATING` / poison markers like the memory store was copied, so labs stay independently runnable.

## Migration Plan

Add two modules and README lines. Rollback is delete + revert README.

## Open Questions

None.
