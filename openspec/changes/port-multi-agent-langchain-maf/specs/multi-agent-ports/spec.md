## ADDED Requirements

### Requirement: LangChain multi-agent module
The langchain-lab package SHALL expose `sd_agentic_langchain.multi_agent` that runs a coordinator, named specialists, a shared notes board, and a writer via LangGraph, then returns a customer reply.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.multi_agent`
- **THEN** the process SHALL print JSON that includes `assignments`, `notes`, `rounds`, and `reply` for `SUPPORT_EMAIL`

#### Scenario: Coordinator assigns specialists
- **WHEN** a plan of work is produced
- **THEN** each assignment MUST name an agent from the roster `billing`, `shipping`, `policy` and include an instruction

#### Scenario: Specialists write shared notes
- **WHEN** a specialist runs
- **THEN** it MUST append a note `{agent, text}` to the shared board rather than sending a customer email

#### Scenario: Extra coordinator round
- **WHEN** the first specialist round finishes
- **THEN** the coordinator MAY assign more specialists at most once (`MAX_ROUNDS = 2`) before the writer runs

#### Scenario: Shared multi-agent prompts
- **WHEN** the module coordinates, reviews, runs a specialist, or writes
- **THEN** it MUST use the shared `COORDINATOR_SYSTEM`, `COORDINATOR_REVIEW_SYSTEM`, specialist, and `WRITER_AGENT_SYSTEM` prompts

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:multi_agent` and `backend:langchain`

### Requirement: MAF multi-agent module
The maf-lab package SHALL expose `sd_agentic_maf.multi_agent` that runs the same coordinator → specialists → writer flow with MAF Agents and returns the same result shape.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.multi_agent`
- **THEN** the process SHALL print JSON that includes `assignments`, `notes`, `rounds`, and `reply` for `SUPPORT_EMAIL`

#### Scenario: Agents own LLM steps
- **WHEN** the module coordinates, reviews, runs a specialist, or writes
- **THEN** it MUST use MAF Agent invocation rather than a hand-rolled OpenAI `complete()` helper

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** an OTEL span named `pattern.multi_agent` MUST be created with attributes identifying `pattern` as `multi_agent` and `backend` as `maf`

### Requirement: Patterns package stays framework-free
`packages/patterns` MUST NOT import LangChain or Microsoft Agent Framework as part of this change.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch multi-agent MUST remain unmodified

### Requirement: README progress for multi-agent ports
The repository README SHALL record that multi-agent LangChain and MAF are done and SHALL document run commands for both modules.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** the Progress table row for pattern 7 Multi-agent collaboration SHALL show scratch, LangChain, and MAF as `done`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run` commands for `sd_agentic_langchain.multi_agent` and `sd_agentic_maf.multi_agent`
