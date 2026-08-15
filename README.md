# sd-agentic

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

Legend: done · pending · MCP and OO-Agents are special labs (not 3-way ports)

| # | Pattern | scratch | LangChain | MAF | Notes |
|---|---|---|---|---|---|
| 1 | Prompt chaining | done | done | done | summarize → draft → policy check |
| 2 | Routing | done | done | done | classify billing / shipping / cancel / other |
| 3 | Parallelization | done | done | done | sectioning (split) and voting (N drafts) |
| 4 | Reflection | done | done | done | draft → critic → revise until PASS |
| 5 | Tool use | done | done | done | function-calling loop; MCP variant done; OO-Agents pending |
| 6 | Planning | done | pending | pending | plan DAG → execute → replan once if blocked |
| 7 | Multi-agent collaboration | pending | pending | pending | docs only |
| 8 | Memory management | pending | pending | pending | docs only |
| 9 | Learning and adaptation | pending | pending | pending | docs only |
| 10 | Model Context Protocol | — | — | — | FastMCP lab done — see Special labs |
| 11 | Goal setting and monitoring | pending | pending | pending | docs only |
| 12 | Exception handling and recovery | pending | pending | pending | docs only |
| 13 | Human-in-the-loop | pending | pending | pending | docs only |
| 14 | Knowledge retrieval (RAG) | pending | pending | pending | docs only |
| 15 | Inter-agent communication (A2A) | pending | pending | pending | docs only |
| 16 | Resource-aware optimization | pending | pending | pending | docs only |
| 17 | Reasoning techniques | pending | pending | pending | docs only |
| 18 | Guardrails / safety | pending | pending | pending | docs only |
| 19 | Evaluation and monitoring | pending | pending | pending | docs only |
| 20 | Prioritization | pending | pending | pending | docs only |
| 21 | Exploration and discovery | pending | pending | pending | docs only |

**Done:** workspace scaffold, shared support-email task, Langfuse wiring, from-scratch core loop (1–5) ported to LangChain and MAF, planning from scratch, MCP server + tool-use client.

**Next:** either Multi-agent collaboration (#7) from scratch, or port planning so it can be diffed three ways.

## Special labs

Same fake support inbox as the 21-pattern loop; different action model. Not a fourth/fifth column on the table above. Loop-engineering skips this table unless **Next** names a special-lab module.

| Lab | Package | demo | agent loop | extra | Notes |
|---|---|---|---|---|---|
| MCP | `packages/mcp-lab` | done | done (`tool_use`) | done (`server`) | discover/authorize the shared tools via FastMCP |
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

### From-scratch patterns (1–6)

```powershell
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.prompt_chaining
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.routing
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.parallelization
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.reflection
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.tool_use
uv run --package sd-agentic-patterns python -m sd_agentic_patterns.planning
```

### Ports in the other labs

```powershell
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.prompt_chaining
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.routing
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.parallelization
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.reflection
uv run --package sd-agentic-langchain python -m sd_agentic_langchain.tool_use
uv run --package sd-agentic-maf python -m sd_agentic_maf.prompt_chaining
uv run --package sd-agentic-maf python -m sd_agentic_maf.routing
uv run --package sd-agentic-maf python -m sd_agentic_maf.parallelization
uv run --package sd-agentic-maf python -m sd_agentic_maf.reflection
uv run --package sd-agentic-maf python -m sd_agentic_maf.tool_use
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

Implement the next pattern in `packages/patterns` first. Port it to LangChain and MAF with the same module name. Quality/safety patterns (exception handling, HITL, guardrails, evaluation) can wrap existing flows instead of becoming standalone clones of every backend. MCP and OO-Agents stay special labs — do not port every pattern into them.
