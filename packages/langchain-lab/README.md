# langchain-lab

LangChain / LangGraph ports of the 21 patterns. Same module name, prompts, and fake support inbox as `packages/patterns`.

Read this file before writing a LangChain port. LangChain and LangGraph are not interchangeable; pick the surface that *is* the pattern.

## LCEL vs LangGraph

**LCEL** (LangChain Expression Language) is the `|` pipe: prompts, models, parsers, retrievers composed into a `Runnable` (`prompt | llm | StrOutputParser()`). Shared `.invoke()` / `.stream()` / `.batch()`. Good for a **static DAG** — steps known when you write the code.

**LangGraph** is the state machine: `StateGraph`, cycles, conditional edges, checkpointers, `interrupt()`, multi-agent `Send`. Good when iteration count, branching, or shared state is **unknown at write time**.

```
LangChain (LCEL)                    LangGraph
────────────────                    ─────────
ChatPromptTemplate                  StateGraph / state
ChatOpenAI, tools, retrievers       cycles + conditional edges
parsers, RunnableParallel           checkpointers, interrupt()
a | b | c  (static DAG)             Send / multi-agent
                                    (runtime control flow)
```

`create_agent` and similar LangChain agent helpers **are LangGraph under the hood**. Using them still counts as a graph port.

## How to port

Compose them. LCEL is the work inside a node; LangGraph is which node runs next.

- Do **not** re-invent a cycle with a Python `while` around LCEL chains. That is the scratch loop with extra wrappers and hides nothing the framework owns.
- Do **not** force a three-step pipe into a graph just for sameness when LCEL *is* the teaching surface (classic RAG, a linear chain, a guardrail wrapper).
- Do **not** use LCEL alone for pause/resume, shared mutable state, or unknown-length loops.

Existing modules 1–7 used `StateGraph` even for linear chaining so every port shared one teaching surface. Later ports should follow the table below, not copy that default blindly.

## When LCEL is enough vs LangGraph is better

| Kind of control flow | Use | Examples |
|---|---|---|
| Known DAG at write time | LCEL (`a \| b \| c`, `RunnableParallel`, `RunnableBranch`) | prompt chaining, sectioning, classic RAG retrieve\|gen, a guardrail around a call, cheap vs expensive model pick |
| Unknown iteration / shared state | LangGraph (`StateGraph`, conditional edges) | reflection, tool use, planning, HITL, multi-agent, memory across turns, ToT / exploration |

### Per pattern

| # | Pattern | LCEL enough? | Prefer LangGraph when |
|---|---|---|---|
| 1 | Prompt chaining | Yes — `summarize \| draft \| check` | Lab consistency with a linear `StateGraph` (already shipped) |
| 2 | Routing | Mostly — `RunnableBranch` | Named specialist nodes, clearer traces |
| 3 | Parallelization | Sectioning: `RunnableParallel`. Voting: weaker | Fan-out / merge as graph nodes |
| 4 | Reflection | Only with a Python `while` | Conditional draft ⇄ critic cycle **is** the pattern |
| 5 | Tool use | `create_agent` — that is LangGraph | `ToolNode` + `tools_condition` |
| 6 | Planning | Python loop around chains | Plan → execute → replan cycle |
| 7 | Multi-agent | You would reinvent a supervisor | Shared state, coordinator, `Send` |
| 8 | Memory | Stores/retrievers exist | Checkpointer + long-term store |
| 9 | Learning | App code + retrieval | Graph optional |
| 11 | Goal monitoring | Possible | Progress in graph state |
| 12 | Exceptions | LCEL retry/fallback is good | Workflow-level recovery edges |
| 13 | HITL | Cannot pause/resume a chain well | `interrupt()` is the feature |
| 14 | RAG | **LangChain wins** for retrieve \| gen | Graph only for agentic RAG (retrieve-then-decide) |
| 15 | A2A | Protocol, not a library | Graph for the topology |
| 16 | Resource-aware | Router chain is enough | Graph if you switch mid-run |
| 17 | Reasoning | CoT is a prompt | ToT / debate / self-consistency loops |
| 18 | Guardrails | Wrappers / parsers | Nodes around an existing graph |
| 19 | Evaluation | Langfuse, not either | — |
| 20 | Prioritization | A Python queue | Re-score loop as a cycle |
| 21 | Exploration | Weak | Branch, score, prune |

HITL is the sharpest LangGraph case (checkpoint + `interrupt()`). Classic RAG is the sharpest LCEL case (retrievers are the LangChain part worth showing).

Quality/safety patterns (exception handling, HITL, guardrails, evaluation) wrap an existing flow when that fits; they do not need a standalone clone of every backend.
