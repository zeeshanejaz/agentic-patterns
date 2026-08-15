## Context

Scratch routing (`packages/patterns/.../routing.py`) classifies a support email into `billing` / `shipping` / `cancel` / `other`, then calls one specialist handler. Prompt chaining is already ported: LangChain uses a sequential LangGraph; MAF uses `SequentialBuilder`. Routing needs a branch, so those sequential builders cannot be copied as-is.

Shared prompts and `SAMPLE_EMAILS` already exist. `RouteResult` lives on the scratch module; labs must not import LangChain/MAF into `packages/patterns`, and langchain/maf labs do not depend on the patterns package.

## Goals / Non-Goals

**Goals:**

- Same classify-then-one-handler loop in both labs, same module name `routing`.
- Same prompts and sample emails as scratch.
- Result shape `{intent, reply}`.
- Langfuse tags `pattern:routing` and `backend:langchain` / `backend:maf`.
- README Progress cells for routing LangChain and MAF flip to done.

**Non-Goals:**

- Changing scratch routing or shared prompts.
- MAF `HandoffBuilder` (conversational idle loop, not one-shot classify+handle).
- MCP, new tools, or other patterns.
- Moving `RouteResult` into shared (duplicate the tiny model in each lab).

## Decisions

1. **Both labs in one change.** Branching is small (four known intents). Each lab is one module mirroring scratch, not a new architecture.

   Alternative: one lab per cycle — rejected; reviewable as two small files plus README.

2. **LangChain: LangGraph classify node + conditional edges.** `ChatPromptTemplate | ChatOpenAI | StrOutputParser` like prompt chaining. Classify parses the first token the same way scratch does (`split()[0]`, fallback `other`). Four handler nodes, one per intent. `CallbackHandler` + `propagate_attributes` tags.

   Alternative: a single LLM call with a tools/router chain — rejected; hides the pattern.

3. **MAF: router Agent, then one specialist Agent.** Reuse `OpenAIChatClient` / `configure_maf_otel` from the prompt-chaining port. Parent OTEL span `pattern.routing` with attributes `pattern=routing`, `backend=maf`. Do not use `SequentialBuilder` (no branch) or `HandoffBuilder` (multi-turn).

   Alternative: `SwitchCaseEdgeGroup` on a low-level `WorkflowBuilder` — more framework-native, but heavier than the learning goal of “same loop, different stack.”

4. **CLI runs all `SAMPLE_EMAILS`**, same as scratch (not a single `SUPPORT_EMAIL` like prompt chaining).

## Risks / Trade-offs

- [Misroute vs scratch] → Same `ROUTE_SYSTEM` and token parse; traces still comparable even if a model call differs.
- [MAF tags weaker than Langfuse `@observe`] → Set span name and attributes; document that MAF traces arrive via OTEL.
- [Handoff would look more “MAF-native”] → Semantics would not match scratch; skip.

## Migration Plan

Add two modules and README lines. No data migration. Rollback is delete the modules and revert README cells.

## Open Questions

None. Classify fallback and intent set are already defined in scratch.
