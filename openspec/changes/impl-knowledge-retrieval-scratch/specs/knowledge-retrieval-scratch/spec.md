## ADDED Requirements

### Requirement: Scratch knowledge-retrieval module
The patterns package SHALL expose `sd_agentic_patterns.knowledge_retrieval` that retrieves top-k support-policy chunks and generates a cited reply, without importing LangChain or Microsoft Agent Framework.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.knowledge_retrieval`
- **THEN** the process SHALL print JSON that includes `query`, `retrieved` chunks (each with `id` and `score`), and a `reply`

#### Scenario: Top-k retrieve then generate
- **WHEN** `run` executes
- **THEN** it MUST retrieve at most `K` chunks from `RAG_CHUNKS` before writing the reply, and the reply MUST be produced from those chunks plus the email (not from uncited extra policy)

#### Scenario: Citations
- **WHEN** a reply is written
- **THEN** it MUST mention retrieved chunk ids when it uses their facts, and MUST NOT invent order tracking or refund amounts

#### Scenario: Policy
- **WHEN** a reply is written
- **THEN** it MUST be produced under the shared support `POLICY`

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:knowledge_retrieval` and `backend:scratch`

### Requirement: Shared RAG corpus and prompt
The policy chunks and RAG reply prompt SHALL live in `packages/shared` so later ports can reuse them.

#### Scenario: Corpus is importable
- **WHEN** a lab imports `RAG_CHUNKS` from `sd_agentic_shared.corpus`
- **THEN** it MUST be a sequence of at least six items each with `id`, `title`, and `text`

#### Scenario: Prompt is importable
- **WHEN** a lab imports `RAG_REPLY_SYSTEM` from `sd_agentic_shared.prompts`
- **THEN** it MUST be defined and interpolate `POLICY`

### Requirement: README progress for knowledge-retrieval scratch
The repository README SHALL record that knowledge-retrieval scratch is shipped and SHALL document a run command for the module. LangChain and MAF RAG cells SHALL remain pending.

#### Scenario: Progress cells
- **WHEN** this change lands
- **THEN** the Progress table row for pattern 14 Knowledge retrieval (RAG) SHALL show scratch as shipped and LangChain and MAF as `pending`

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run --package sd-agentic-patterns python -m sd_agentic_patterns.knowledge_retrieval`
