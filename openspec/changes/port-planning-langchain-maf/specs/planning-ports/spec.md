## ADDED Requirements

### Requirement: LangChain planning module
The langchain-lab package SHALL expose `sd_agentic_langchain.planning` that decomposes a support email into a step plan with dependencies, executes ready steps via LangGraph, and produces a customer reply.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.planning`
- **THEN** the process SHALL print JSON that includes a `plan` (with `goal` and `steps`), `execution` results per step, `replans`, and `reply` for `SUPPORT_EMAIL`

#### Scenario: Plan has a dependency graph
- **WHEN** a plan is produced
- **THEN** each step MUST have an `id`, an `instruction`, optional `tool` / `arguments`, and `depends_on` listing prior step ids

#### Scenario: Tool steps use shared fakes
- **WHEN** a step names `lookup_order`, `create_refund`, or `search_docs`
- **THEN** the executor MUST call `sd_agentic_shared.tools.call_tool` with that name and arguments (not a live API and not a LangGraph ToolNode ReAct loop)

#### Scenario: Replan on blocked checkpoint
- **WHEN** a tool result indicates the order was not found or a refund was refused
- **THEN** the module MUST replan remaining steps at most once before continuing

#### Scenario: Shared planning prompts
- **WHEN** the module plans, repairs, executes a text step, or replans
- **THEN** it MUST use `PLAN_SYSTEM`, `PLAN_REPAIR_SYSTEM`, `PLAN_STEP_SYSTEM`, and `PLAN_REPLAN_SYSTEM` from `sd_agentic_shared.prompts`

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:planning` and `backend:langchain`

### Requirement: MAF planning module
The maf-lab package SHALL expose `sd_agentic_maf.planning` that runs the same plan → execute → replan flow with MAF Agents and returns the same result shape.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.planning`
- **THEN** the process SHALL print JSON that includes `plan`, `execution`, `replans`, and `reply` for `SUPPORT_EMAIL`

#### Scenario: Tool steps use shared fakes
- **WHEN** a step names a shared fake tool
- **THEN** the module MUST execute it via `sd_agentic_shared.tools.call_tool`

#### Scenario: Agents own LLM steps
- **WHEN** the module plans, repairs a plan, executes a text step, or replans
- **THEN** it MUST use MAF Agent invocation rather than a hand-rolled OpenAI `complete()` helper

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** an OTEL span named `pattern.planning` MUST be created with attributes identifying `pattern` as `planning` and `backend` as `maf`

### Requirement: Patterns package stays framework-free
`packages/patterns` MUST NOT import LangChain or Microsoft Agent Framework as part of this change.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch planning MUST remain unmodified

### Requirement: README progress for planning ports
The repository README SHALL record that planning LangChain and MAF are done and SHALL document run commands for both modules.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** the Progress table row for pattern 6 Planning SHALL show scratch, LangChain, and MAF as `done`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run` commands for `sd_agentic_langchain.planning` and `sd_agentic_maf.planning`
