## ADDED Requirements

### Requirement: SupportAgent is a NOOA object with tools as methods
`packages/nooa-lab` SHALL expose a `SupportAgent` subclass of `nooa.Agent` whose deterministic methods wrap the shared fake tools `lookup_order`, `create_refund`, and `search_docs`. A generation method `handle(email: str) -> str` SHALL use CodeAct (ellipsis body) so the model acts by writing Python that calls those methods on `self`. The class docstring and `handle` docstring MUST include the shared `POLICY`. The package MUST NOT import LangChain or Microsoft Agent Framework.

#### Scenario: Tools are ordinary methods
- **WHEN** a `SupportAgent` is constructed
- **THEN** `lookup_order`, `create_refund`, and `search_docs` MUST be callable Python methods that delegate to `sd_agentic_shared.tools` (same in-memory fakes as the other labs)

#### Scenario: CodeAct handle
- **WHEN** `handle` is invoked with a customer email
- **THEN** it MUST run as a NOOA generation method (ellipsis / CodeAct), not a hardcoded function-calling loop

#### Scenario: No LangChain or MAF
- **WHEN** the package is inspected
- **THEN** it MUST NOT import LangChain, LangGraph, or Microsoft Agent Framework

### Requirement: Demo constructs SupportAgent and calls lookup_order without generation
`sd_agentic_nooa.demo` SHALL construct `SupportAgent` and call `lookup_order` for order `A-18422` without invoking `handle` or any other generation method.

#### Scenario: Demo is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-nooa python -m sd_agentic_nooa.demo`
- **THEN** stdout JSON SHALL include a `lookup_order` result that matches the shared fake for `A-18422` (processing, paid 89, tracking none)

#### Scenario: Demo does not run CodeAct
- **WHEN** `demo` executes
- **THEN** it MUST NOT call `handle` or any ellipsis method

### Requirement: Support loop on SUPPORT_EMAIL with Langfuse tags
`sd_agentic_nooa.support` SHALL run `SupportAgent.handle` on the shared `SUPPORT_EMAIL`. Tracing MUST use NOOA `exporters.langfuse()` (host from `LANGFUSE_HOST` or `LANGFUSE_BASE_URL`). Tags MUST include `pattern:tool_use` and `backend:nooa`.

#### Scenario: Support is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-nooa python -m sd_agentic_nooa.support`
- **THEN** stdout JSON SHALL include a customer-facing `reply` and a `calls` list of method invocations recorded from `self`

#### Scenario: Shared task and policy
- **WHEN** `support` runs
- **THEN** it MUST use `SUPPORT_EMAIL` and MUST NOT invent order facts, promise refunds over $50, or blame the customer (policy lives on the agent / handle docstrings)

#### Scenario: Langfuse tags
- **WHEN** `support` runs
- **THEN** the wrapping trace MUST carry tags `pattern:tool_use` and `backend:nooa`

### Requirement: README Special labs progress
The Special labs OO-Agents row SHALL link `demo` and `support`. Pattern 5 notes SHALL mention the OO-Agents variant. The 21-pattern table MUST NOT gain an OO-Agents column.

#### Scenario: Special labs cells
- **WHEN** this change lands
- **THEN** OO-Agents demo SHALL link `packages/nooa-lab/src/sd_agentic_nooa/demo.py` and agent loop SHALL link `packages/nooa-lab/src/sd_agentic_nooa/support.py`

#### Scenario: Run section
- **WHEN** a developer reads Run
- **THEN** they SHALL find `sd_agentic_nooa.demo` and `sd_agentic_nooa.support` commands
