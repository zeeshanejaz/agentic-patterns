## ADDED Requirements

### Requirement: LangChain learning module
The langchain-lab package SHALL expose `sd_agentic_langchain.learning` that collects simulated supervisor feedback, distills prompt lessons via LCEL, and compares a baseline reply to an adapted reply on `LEARNING_HELD_OUT`.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.learning`
- **THEN** the process SHALL print JSON that includes kept feedback, the distilled `lessons` string, a `baseline` reply, and an `adapted` reply for `LEARNING_HELD_OUT`

#### Scenario: LCEL owns LLM steps
- **WHEN** the module distills lessons or writes a reply
- **THEN** it MUST use an LCEL chain (`prompt | llm | parser`) rather than a LangGraph `StateGraph` or a hand-rolled OpenAI `complete()` helper

#### Scenario: Clean before distill
- **WHEN** feedback is ingested
- **THEN** the module MUST drop cases with empty corrections, rating below `MIN_RATING`, or corrections that ask to invent order facts, promise a refund over $50, or blame the customer

#### Scenario: Shared cases and prompts
- **WHEN** the module runs
- **THEN** it MUST use `LEARNING_CASES` and `LEARNING_HELD_OUT` from `sd_agentic_shared.tasks.support_email` and `LEARNING_DISTILL_SYSTEM` / `LEARNING_REPLY_SYSTEM` from shared prompts

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:learning` and `backend:langchain`

### Requirement: MAF learning module
The maf-lab package SHALL expose `sd_agentic_maf.learning` that runs the same clean → distill → A/B flow with MAF Agents and returns the same result shape.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.learning`
- **THEN** the process SHALL print JSON that includes kept feedback, `lessons`, `baseline`, and `adapted` for `LEARNING_HELD_OUT`

#### Scenario: Agents own LLM steps
- **WHEN** the module distills lessons or writes a reply
- **THEN** it MUST use MAF Agent invocation rather than a hand-rolled OpenAI `complete()` helper

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** an OTEL span named `pattern.learning` MUST be created with attributes identifying `pattern` as `learning` and `backend` as `maf`

### Requirement: Patterns package stays framework-free
`packages/patterns` MUST NOT import LangChain or Microsoft Agent Framework as part of this change.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch learning MUST remain unmodified

### Requirement: README progress for learning ports
The repository README SHALL record that learning-and-adaptation LangChain and MAF are done and SHALL document run commands for both modules.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** the Progress table row for pattern 9 Learning and adaptation SHALL show scratch, LangChain, and MAF as `done`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run` commands for `sd_agentic_langchain.learning` and `sd_agentic_maf.learning`
