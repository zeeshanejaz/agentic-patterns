## Context

Scratch parallelization runs two demos on `SUPPORT_EMAIL`:

1. **Sectioning:** three concurrent extractors (order, payment, ask) then a merge LLM call.
2. **Voting:** three concurrent draft workers (temperature 0.8, indexed system prompt) then a merge LLM call.

Prompt-chaining and routing ports already show sequential LangGraph and MAF Agent usage. This change needs real fan-out.

Voting worker instructions are inline in scratch, not in `packages/shared`.

## Goals / Non-Goals

**Goals:**

- Same two modes, same module name `parallelization`, same result shapes.
- Framework-native concurrency (LangGraph parallel branches; MAF `ConcurrentBuilder`), not a hidden `ThreadPoolExecutor` copy of scratch.
- Shared prompts for section extractors, section merge, and vote merge. Duplicate scratch's voting worker prompt text.
- Langfuse tags `pattern:parallelization` and `backend:langchain` / `backend:maf`.
- README cells and run commands.

**Non-Goals:**

- Changing scratch or adding voting worker prompts to shared.
- Configurable N beyond scratch's default of 3.
- MCP or other patterns.

## Decisions

1. **Both labs in one change.** Two small modules; ConcurrentBuilder and LangGraph fan-out are the obvious ports.

2. **LangChain: fan-out edges, then a merge node.** Sectioning: START → three section nodes → `merge_sections`. Voting: START → `draft_1`/`draft_2`/`draft_3` → `vote_merge`. LangGraph runs ready nodes in one superstep (fan-in waits for all parents). `CallbackHandler` + `propagate_attributes`. Voting drafts use `ChatOpenAI(temperature=0.8)` to match scratch.

   Alternative: `ThreadPoolExecutor` inside one node — rejected; would not show what LangGraph hides.

3. **MAF: `ConcurrentBuilder` then a merge Agent.** Identify worker outputs by agent name, not list order. Then `merge_agent.run(...)`. Parent spans `pattern.parallelization.sectioning` / `pattern.parallelization.voting` with `pattern` and `backend` attributes.

   Alternative: aggregator callback that itself calls an LLM — equivalent, but a separate merge Agent matches scratch's two-phase loop more clearly.

4. **CLI prints both modes**, same as scratch.

## Risks / Trade-offs

- [LangGraph sync `invoke` may not overlap HTTP calls] → Graph structure still encodes the pattern; async invoke is optional later.
- [ConcurrentBuilder output order] → Key results by participant name.
- [Voting prompt drift] → Copy scratch's worker string verbatim.

## Migration Plan

Add two modules and README lines. Rollback is delete + revert README.

## Open Questions

None.
