## ADDED Requirements

### Requirement: LangChain human-in-the-loop module
The langchain-lab package SHALL expose `sd_agentic_langchain.human_in_the_loop` that drafts a support reply, pauses with LangGraph `interrupt()` when the gate fires, and resumes with a human decision.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.human_in_the_loop`
- **THEN** the process SHALL print JSON that includes `summary`, `draft`, `gate`, `decision`, `reply`, and `interrupted`

#### Scenario: Interrupt is the pause
- **WHEN** the gate needs a human
- **THEN** the graph MUST call LangGraph `interrupt()` (not only a Python `if` that applies the decision in the same turn) and MUST resume with `HITL_DECISION`

#### Scenario: Gate on high-risk refund
- **WHEN** the email asks for a refund over $50
- **THEN** `interrupted` MUST be true and the final reply MUST NOT promise a refund over $50 when the canned decision is `deny`

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:human_in_the_loop` and `backend:langchain`

### Requirement: MAF human-in-the-loop module
The maf-lab package SHALL expose `sd_agentic_maf.human_in_the_loop` that runs the same summarize → draft → gate → review → resume flow with MAF Agents and the canned reviewer.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.human_in_the_loop`
- **THEN** the process SHALL print JSON that includes `summary`, `draft`, `gate`, `decision`, `reply`, and `interrupted`

#### Scenario: Agents own LLM steps
- **WHEN** the module summarizes, drafts, gates, or resumes
- **THEN** it MUST use MAF Agent invocation rather than a hand-rolled OpenAI `complete()` helper

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** an OTEL span named `pattern.human_in_the_loop` MUST be created with attributes identifying `pattern` as `human_in_the_loop` and `backend` as `maf`

### Requirement: Patterns package stays framework-free
`packages/patterns` MUST NOT import LangChain or Microsoft Agent Framework as part of this change.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch HITL MUST remain unmodified

### Requirement: README progress for HITL ports
The repository README SHALL record that human-in-the-loop LangChain and MAF are done and SHALL document run commands for both modules.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** the Progress table row for pattern 13 Human-in-the-loop SHALL show scratch, LangChain, and MAF as `done`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run` commands for `sd_agentic_langchain.human_in_the_loop` and `sd_agentic_maf.human_in_the_loop`
