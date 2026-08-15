## ADDED Requirements

### Requirement: LangChain tool-use module
The langchain-lab package SHALL expose `sd_agentic_langchain.tool_use` that lets the model call the shared fake tools `lookup_order`, `create_refund`, and `search_docs` via LangGraph, then returns a final support reply.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.tool_use`
- **THEN** the process SHALL print JSON with `calls` (each with `name`, `arguments`, `result`) and `reply` for `SUPPORT_EMAIL`

#### Scenario: Shared fake tools
- **WHEN** the model requests a tool
- **THEN** the module MUST execute the matching function from `sd_agentic_shared.tools` (not a reimplemented store)

#### Scenario: Step cap
- **WHEN** the graph exceeds six model turns of tool use
- **THEN** the reply MUST be `Stopped: too many tool steps.`

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:tool_use` and `backend:langchain`

### Requirement: MAF tool-use module
The maf-lab package SHALL expose `sd_agentic_maf.tool_use` that runs a MAF Agent with the shared fake tools `lookup_order`, `create_refund`, and `search_docs` and returns the same result shape.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.tool_use`
- **THEN** the process SHALL print JSON with `calls` and `reply` for `SUPPORT_EMAIL`

#### Scenario: Shared fake tools
- **WHEN** the Agent invokes a tool
- **THEN** the module MUST execute the matching function from `sd_agentic_shared.tools`

#### Scenario: Framework owns the loop
- **WHEN** tool use runs
- **THEN** the module MUST use MAF Agent tool invocation rather than a hand-rolled OpenAI `tools=` loop

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** an OTEL span named `pattern.tool_use` MUST be created with attributes identifying `pattern` as `tool_use` and `backend` as `maf`

### Requirement: Patterns package stays framework-free
`packages/patterns` MUST NOT import LangChain or Microsoft Agent Framework as part of this change.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch tool use MUST remain unmodified

### Requirement: README progress for tool-use ports
The repository README SHALL record that tool use LangChain and MAF are done and SHALL document run commands for both modules.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** the Progress table row for pattern 5 Tool use SHALL show LangChain and MAF as `done`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run` commands for `sd_agentic_langchain.tool_use` and `sd_agentic_maf.tool_use`
