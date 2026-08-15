## ADDED Requirements

### Requirement: LangChain knowledge-retrieval module
The langchain-lab package SHALL expose `sd_agentic_langchain.knowledge_retrieval` that retrieves top-k policy chunks via a LangChain retriever/vector store and generates a cited reply with LCEL.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-langchain python -m sd_agentic_langchain.knowledge_retrieval`
- **THEN** the process SHALL print JSON that includes `query`, `retrieved` chunks with ids, and a `reply`

#### Scenario: LCEL retrieve then generate
- **WHEN** the module runs
- **THEN** it MUST retrieve via a LangChain vector store or retriever (not only the scratch keyword scorer) and MUST generate with an LCEL chain, not a LangGraph `StateGraph`

#### Scenario: Shared corpus and prompt
- **WHEN** the module runs
- **THEN** it MUST use `RAG_CHUNKS` and `RAG_REPLY_SYSTEM`

#### Scenario: Langfuse tags
- **WHEN** `run` executes
- **THEN** the Langfuse trace MUST include tags `pattern:knowledge_retrieval` and `backend:langchain`

### Requirement: MAF knowledge-retrieval module
The maf-lab package SHALL expose `sd_agentic_maf.knowledge_retrieval` that retrieves top-k chunks and generates a cited reply with a MAF Agent.

#### Scenario: Module is runnable
- **WHEN** a developer runs `uv run --package sd-agentic-maf python -m sd_agentic_maf.knowledge_retrieval`
- **THEN** the process SHALL print JSON that includes `query`, `retrieved`, and `reply`

#### Scenario: Agent owns generation
- **WHEN** the module writes the reply
- **THEN** it MUST use MAF Agent invocation rather than a hand-rolled OpenAI `complete()` helper

#### Scenario: Observability
- **WHEN** `run` executes
- **THEN** an OTEL span named `pattern.knowledge_retrieval` MUST be created with attributes identifying `pattern` as `knowledge_retrieval` and `backend` as `maf`

### Requirement: Patterns package stays framework-free
`packages/patterns` MUST NOT import LangChain or Microsoft Agent Framework as part of this change.

#### Scenario: Scratch unchanged
- **WHEN** this change is implemented
- **THEN** scratch knowledge retrieval MUST remain unmodified

### Requirement: README progress for knowledge-retrieval ports
The repository README SHALL record that knowledge-retrieval LangChain and MAF are shipped and SHALL document run commands for both modules.

#### Scenario: Progress cells
- **WHEN** the ports land
- **THEN** the Progress table row for pattern 14 Knowledge retrieval (RAG) SHALL show scratch, LangChain, and MAF as shipped

#### Scenario: Run section
- **WHEN** a developer reads the README Run section
- **THEN** they SHALL find `uv run` commands for `sd_agentic_langchain.knowledge_retrieval` and `sd_agentic_maf.knowledge_retrieval`
