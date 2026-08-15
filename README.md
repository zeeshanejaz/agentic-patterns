# Agentic Patterns Labs

A uv workspace for learning the [21 agentic design patterns](docs/agentic-design-patterns.md) by implementing each one several ways on the **same task**, then comparing traces in Langfuse.

Patterns are the unit of learning, not frameworks. Implement from scratch first so you invent the loop; then port so you can see what LangChain / Microsoft Agent Framework hide.

## Objective

Work through the 21 patterns from [`promptadvisers/agentic-design-patterns-docs`](https://github.com/promptadvisers/agentic-design-patterns-docs) (Antonio Gulli’s book; video walkthrough [Master ALL 20 Agentic AI Design Patterns](https://www.youtube.com/watch?v=e2zIr_2JMbE) omits MCP).

1. Implement the pattern in `packages/patterns` (OpenAI + Langfuse SDK). That package **cannot** import LangChain or Agent Framework.
2. Port it to the other labs under the **same module name**, using the same prompts and sample emails from `packages/shared`.
3. Diff the implementations and inspect traces in Langfuse (`pattern:*`, `backend:scratch` / `langchain` / `maf` / `mcp`).

The shared task is a fake customer-support inbox: do not invent order facts, do not promise refunds over $50, do not blame the customer. Tools (`lookup_order`, `create_refund`, `search_docs`) are in-memory fakes.

## Labs

| Package | Stack | Tracing |
|---|---|---|
| `packages/patterns` | OpenAI SDK, from scratch | Langfuse `@observe` + `langfuse.openai` |
| `packages/langchain-lab` | LangChain / LangGraph | Langfuse `@observe` + `CallbackHandler` |
| `packages/maf-lab` | Microsoft Agent Framework | Native OTEL → Langfuse OTLP |
| `packages/mcp-lab` | FastMCP (pattern 10) | Langfuse SDK (tool-use client) |
| `packages/nooa-lab` | NVIDIA OO Agents | Native Langfuse OTLP (`exporters.langfuse()`) |
| `packages/shared` | Task, prompts, fake tools, env | — |

MCP is the integration layer under tool use (discover/authorize tools). OO-Agents is the object-oriented harness (code as action). Neither is a fourth rewrite of every pattern.

## Progress

Legend: `[file.py](path)` = shipped · pending · MCP and OO-Agents are special labs (not 3-way ports)

| # | Pattern | scratch | LangChain | MAF | Notes |
|---|---|---|---|---|---|
| 1 | Prompt chaining | [prompt_chaining.py](packages/patterns/src/sd_agentic_patterns/prompt_chaining.py) | [prompt_chaining.py](packages/langchain-lab/src/sd_agentic_langchain/prompt_chaining.py) | [prompt_chaining.py](packages/maf-lab/src/sd_agentic_maf/prompt_chaining.py) | summarize → draft → policy check |
| 2 | Routing | [routing.py](packages/patterns/src/sd_agentic_patterns/routing.py) | [routing.py](packages/langchain-lab/src/sd_agentic_langchain/routing.py) | [routing.py](packages/maf-lab/src/sd_agentic_maf/routing.py) | classify billing / shipping / cancel / other |
| 3 | Parallelization | [parallelization.py](packages/patterns/src/sd_agentic_patterns/parallelization.py) | [parallelization.py](packages/langchain-lab/src/sd_agentic_langchain/parallelization.py) | [parallelization.py](packages/maf-lab/src/sd_agentic_maf/parallelization.py) | sectioning (split) and voting (N drafts) |
| 4 | Reflection | [reflection.py](packages/patterns/src/sd_agentic_patterns/reflection.py) | [reflection.py](packages/langchain-lab/src/sd_agentic_langchain/reflection.py) | [reflection.py](packages/maf-lab/src/sd_agentic_maf/reflection.py) | draft → critic → revise until PASS |
| 5 | Tool use | [tool_use.py](packages/patterns/src/sd_agentic_patterns/tool_use.py) | [tool_use.py](packages/langchain-lab/src/sd_agentic_langchain/tool_use.py) | [tool_use.py](packages/maf-lab/src/sd_agentic_maf/tool_use.py) | function-calling loop; [MCP variant](packages/mcp-lab/src/sd_agentic_mcp/tool_use.py); OO-Agents pending |
| 6 | Planning | [planning.py](packages/patterns/src/sd_agentic_patterns/planning.py) | [planning.py](packages/langchain-lab/src/sd_agentic_langchain/planning.py) | [planning.py](packages/maf-lab/src/sd_agentic_maf/planning.py) | plan DAG → execute → replan once if blocked |
| 7 | Multi-agent collaboration | [multi_agent.py](packages/patterns/src/sd_agentic_patterns/multi_agent.py) | [multi_agent.py](packages/langchain-lab/src/sd_agentic_langchain/multi_agent.py) | [multi_agent.py](packages/maf-lab/src/sd_agentic_maf/multi_agent.py) | coordinator → specialists → shared notes → writer |
| 8 | Memory management | [memory_management.py](packages/patterns/src/sd_agentic_patterns/memory_management.py) | [memory_management.py](packages/langchain-lab/src/sd_agentic_langchain/memory_management.py) | [memory_management.py](packages/maf-lab/src/sd_agentic_maf/memory_management.py) | short-term / episodic / long-term across turns |
| 9 | Learning and adaptation | [learning.py](packages/patterns/src/sd_agentic_patterns/learning.py) | [learning.py](packages/langchain-lab/src/sd_agentic_langchain/learning.py) | [learning.py](packages/maf-lab/src/sd_agentic_maf/learning.py) | collect feedback → distill lessons → A/B |
| 10 | Model Context Protocol | — | — | — | FastMCP lab — see Special labs |
| 11 | Goal setting and monitoring | [goal_setting.py](packages/patterns/src/sd_agentic_patterns/goal_setting.py) | [goal_setting.py](packages/langchain-lab/src/sd_agentic_langchain/goal_setting.py) | [goal_setting.py](packages/maf-lab/src/sd_agentic_maf/goal_setting.py) | set KPIs → score → adjust within budget |
| 12 | Exception handling and recovery | [exception_handling.py](packages/patterns/src/sd_agentic_patterns/exception_handling.py) | [exception_handling.py](packages/langchain-lab/src/sd_agentic_langchain/exception_handling.py) | [exception_handling.py](packages/maf-lab/src/sd_agentic_maf/exception_handling.py) | wrap tool use: retry / fallback / stop |
| 13 | Human-in-the-loop | [human_in_the_loop.py](packages/patterns/src/sd_agentic_patterns/human_in_the_loop.py) | [human_in_the_loop.py](packages/langchain-lab/src/sd_agentic_langchain/human_in_the_loop.py) | [human_in_the_loop.py](packages/maf-lab/src/sd_agentic_maf/human_in_the_loop.py) | gate refund-over-$50 → pause → resume |
| 14 | Knowledge retrieval (RAG) | [knowledge_retrieval.py](packages/patterns/src/sd_agentic_patterns/knowledge_retrieval.py) | [knowledge_retrieval.py](packages/langchain-lab/src/sd_agentic_langchain/knowledge_retrieval.py) | [knowledge_retrieval.py](packages/maf-lab/src/sd_agentic_maf/knowledge_retrieval.py) | chunk → top-k → cited reply |
| 15 | Inter-agent communication (A2A) | [a2a.py](packages/patterns/src/sd_agentic_patterns/a2a.py) | [a2a.py](packages/langchain-lab/src/sd_agentic_langchain/a2a.py) | [a2a.py](packages/maf-lab/src/sd_agentic_maf/a2a.py) | envelopes on a bus (ids, TTL, replies) |
| 16 | Resource-aware optimization | [resource_aware.py](packages/patterns/src/sd_agentic_patterns/resource_aware.py) | [resource_aware.py](packages/langchain-lab/src/sd_agentic_langchain/resource_aware.py) | [resource_aware.py](packages/maf-lab/src/sd_agentic_maf/resource_aware.py) | cheap vs expensive path by complexity |
| 17 | Reasoning techniques | [reasoning.py](packages/patterns/src/sd_agentic_patterns/reasoning.py) | [reasoning.py](packages/langchain-lab/src/sd_agentic_langchain/reasoning.py) | [reasoning.py](packages/maf-lab/src/sd_agentic_maf/reasoning.py) | CoT samples + self-consistency pick |
| 18 | Guardrails / safety | [guardrails.py](packages/patterns/src/sd_agentic_patterns/guardrails.py) | [guardrails.py](packages/langchain-lab/src/sd_agentic_langchain/guardrails.py) | [guardrails.py](packages/maf-lab/src/sd_agentic_maf/guardrails.py) | input + output checks, rewrite on fail |
| 19 | Evaluation and monitoring | [evaluation.py](packages/patterns/src/sd_agentic_patterns/evaluation.py) | pending | pending | golden + heuristics + LLM judge |
| 20 | Prioritization | pending | pending | pending | docs only |
| 21 | Exploration and discovery | pending | pending | pending | docs only |

**Done:** workspace scaffold, shared support-email task, Langfuse wiring, from-scratch core loop (1–9, 11–19) ported to LangChain and MAF through #18, evaluation scratch, MCP server + tool-use client.

**Next:** Evaluation and monitoring (#19) LangChain and MAF ports.

## Special labs

Same fake support inbox as the 21-pattern loop; different action model. Not a fourth/fifth column on the table above. Loop-engineering skips this table unless the user (or the main **Next** line) names a special-lab module.

| Lab | Package | demo | agent loop | extra | Notes |
|---|---|---|---|---|---|
| MCP | `packages/mcp-lab` | [demo.py](packages/mcp-lab/src/sd_agentic_mcp/demo.py) | [tool_use.py](packages/mcp-lab/src/sd_agentic_mcp/tool_use.py) | [server.py](packages/mcp-lab/src/sd_agentic_mcp/server.py) | discover/authorize the shared tools via FastMCP |
| OO-Agents | `packages/nooa-lab` | pending | pending (`support`) | — | Python object + CodeAct; tools are methods on `self` |

**Special labs next:** scaffold `packages/nooa-lab` (`impl-nooa-lab`): `demo` (construct `SupportAgent`, call `lookup_order` with no LLM) then `support` (CodeAct on `SUPPORT_EMAIL`, tags `pattern:tool_use` / `backend:nooa`).

Pattern discussions, mermaid diagrams, and ASCII art live under `docs/agentic-design-patterns-docs/`.

## Setup

```powershell
uv sync --all-packages
copy .env.example .env
```

Fill in `OPENAI_API_KEY`, `LANGFUSE_PUBLIC_KEY`, and `LANGFUSE_SECRET_KEY`.

The MAF lab can build OTEL Basic auth from the Langfuse keys. To set the header yourself:

```powershell
$pair = "{0}:{1}" -f $env:LANGFUSE_PUBLIC_KEY, $env:LANGFUSE_SECRET_KEY
$b64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($pair))
# OTEL_EXPORTER_OTLP_HEADERS=Authorization=Basic $b64
```

## Run

### From-scratch patterns (1–9, 11–19)

```powershell
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.prompt_chaining
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.routing
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.parallelization
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.reflection
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.tool_use
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.planning
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.multi_agent
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.memory_management
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.learning
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.goal_setting
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.exception_handling
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.human_in_the_loop
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.knowledge_retrieval
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.a2a
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.resource_aware
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.reasoning
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.guardrails
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.evaluation
```

### Ports in the other labs

LangChain ports: LCEL is the units of work (`prompt | llm | parser`); LangGraph is orchestration (cycles, state, HITL). Read [`packages/langchain-lab/README.md`](packages/langchain-lab/README.md) before implementing a port — it says when a chain is enough and when to use a `StateGraph`.

```powershell
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.prompt_chaining
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.routing
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.parallelization
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.reflection
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.tool_use
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.planning
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.multi_agent
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.memory_management
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.learning
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.goal_setting
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.exception_handling
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.human_in_the_loop
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.knowledge_retrieval
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.a2a
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.resource_aware
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.reasoning
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.guardrails
uv run --package sd-agentic-maf python -m sd_agentic_maf.prompt_chaining
uv run --package sd-agentic-maf python -m sd_agentic_maf.routing
uv run --package sd-agentic-maf python -m sd_agentic_maf.parallelization
uv run --package sd-agentic-maf python -m sd_agentic_maf.reflection
uv run --package sd-agentic-maf python -m sd_agentic_maf.tool_use
uv run --package sd-agentic-maf python -m sd_agentic_maf.planning
uv run --package sd-agentic-maf python -m sd_agentic_maf.multi_agent
uv run --package sd-agentic-maf python -m sd_agentic_maf.memory_management
uv run --package sd-agentic-maf python -m sd_agentic_maf.learning
uv run --package sd-agentic-maf python -m sd_agentic_maf.goal_setting
uv run --package sd-agentic-maf python -m sd_agentic_maf.exception_handling
uv run --package sd-agentic-maf python -m sd_agentic_maf.human_in_the_loop
uv run --package sd-agentic-maf python -m sd_agentic_maf.knowledge_retrieval
uv run --package sd-agentic-maf python -m sd_agentic_maf.a2a
uv run --package sd-agentic-maf python -m sd_agentic_maf.resource_aware
uv run --package sd-agentic-maf python -m sd_agentic_maf.reasoning
uv run --package sd-agentic-maf python -m sd_agentic_maf.guardrails
```

Filter traces in Langfuse by `pattern:*` and `backend:scratch` / `langchain` / `maf`.

### MCP (pattern 10)

Expose the same fake support tools over MCP instead of a hardcoded OpenAI tool list. FastMCP (Prefect) is used rather than the low-level official SDK — decorator tools, in-process client, resources, and prompts.

```powershell
uv run --package sd-agentic-mcp python -m sd_agentic_mcp.demo
uv run --package sd-agentic-mcp python -m sd_agentic_mcp.tool_use
uv run --package sd-agentic-mcp python -m sd_agentic_mcp.server
```

`demo` lists tools/resources/prompts and calls them in-process (no LLM). `tool_use` is the same agent loop as `sd_agentic_patterns.tool_use`, but the model only sees tools discovered from the MCP server. `server` speaks stdio so you can point Claude Desktop or Cursor at it.

## Learning order

Implement the next pattern in `packages/patterns` first. Port it to LangChain and MAF with the same module name. For LangChain, follow [`packages/langchain-lab/README.md`](packages/langchain-lab/README.md) (LCEL vs LangGraph per pattern). Quality/safety patterns (exception handling, HITL, guardrails, evaluation) can wrap existing flows instead of becoming standalone clones of every backend. MCP and OO-Agents stay special labs — do not port every pattern into them.
