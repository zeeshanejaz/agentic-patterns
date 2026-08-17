# Regenerating pattern quiz banks

Banks are committed JavaScript. The page never calls a model. There are two bank sets, generated from different sources — see below before regenerating either one.

## Output files

### Transcript-grounded banks (require having watched/read the source)

| File | Group | Patterns |
|---|---|---|
| `bank-core.js` | Core (1–5) | prompt-chaining, routing, parallelization, reflection, tool-use |
| `bank-advanced.js` | Advanced (6–10) | planning, multi-agent, memory-management, learning, mcp |
| `bank-system.js` | System (11–15) | goal-setting, exception-handling, human-in-the-loop, knowledge-retrieval, a2a |
| `bank-optimization.js` | Optimization (16–19) | resource-aware, reasoning, guardrails, evaluation |
| `bank-strategic.js` | Strategic (20–21) | prioritization, exploration |

### Fundamentals banks (self-contained, no prior reading required)

| File | Group | Patterns |
|---|---|---|
| `bank-core-fundamentals.js` | Core (1–5) | prompt-chaining, routing, parallelization, reflection, tool-use |
| `bank-advanced-fundamentals.js` | Advanced (6–10) | planning, multi-agent, memory-management, learning, mcp |
| `bank-system-fundamentals.js` | System (11–15) | goal-setting, exception-handling, human-in-the-loop, knowledge-retrieval, a2a |
| `bank-optimization-fundamentals.js` | Optimization (16–19) | resource-aware, reasoning, guardrails, evaluation |
| `bank-strategic-fundamentals.js` | Strategic (20–21) | prioritization, exploration |

Each file must call `window.QUIZ_BANKS.push({ id, title, patterns, questions })`. Canonical `pattern` slugs are the strings in the table. Fundamentals bank ids are the group name plus `-fundamentals` (for example `core-fundamentals`) so they don't collide with the transcript-grounded bank ids.

## Sources (read these, not lab code)

Per pattern, for the transcript-grounded banks (`bank-core.js`, `bank-advanced.js`, `bank-system.js`, `bank-optimization.js`, `bank-strategic.js`):

- `docs/agentic-design-patterns-docs/pattern-discussion/<file>.md`
- `docs/agentic-design-patterns-docs/ascii-art/<file>.txt` (KEY CONCEPTS)
- `docs/agentic-design-patterns-docs/mermaid-diagrams/<file>.mmd` (flow, not syntax)
- Matching `##` section in `docs/transcripts/master-20-agentic-design-patterns.md`

The video **omits MCP**. Advanced MCP items come only from `pattern-discussion/model-context-protocol.md` (and ascii/mermaid). Spoken order in the transcript swaps evaluation (#19) ahead of guardrails (#18); banks still follow the table above.

The clone under `docs/agentic-design-patterns-docs/` is gitignored. Regeneration needs it locally. Taking the quiz only needs the committed `bank-*.js` files.

For the **fundamentals banks** (`bank-*-fundamentals.js`), the only source is the committed pros/cons table in [`docs/agentic-design-patterns.md`](../agentic-design-patterns.md) (Description / When to apply / Pros / Cons columns). Do **not** pull from the transcript, the pattern-discussion docs, or the ascii/mermaid diagrams for these banks — every stem must stand on its own for someone who has never opened those sources.

## Rubric

Shared by both bank sets unless noted:

- About **6–8 questions per pattern** (Strategic may sit at the low end).
- Each item: `id`, `pattern`, optional `also` (confusion partners), `kind`, `stem`, `choices` (exactly four strings), `answer` (0-based), `explanation`.
- Wrong choices are **sibling patterns or design moves in the same bank**, not APIs or code.
- `explanation` says why the keyed answer is right **and** why at least one distractor is wrong.
- **Do not** name LangChain, LangGraph, Microsoft Agent Framework, FastMCP, OO-Agents, Langfuse, or lab module paths.
- Mix kinds inside each pattern. Include at least one `when` (including when *not*) per pattern.
- `compose` stays **inside the bank** (e.g. routing + tool use in Core). No cross-group mix bank.

### Transcript-grounded banks only

- `kind` is one of `identify` | `when` | `tradeoff` | `discriminate` | `compose`.
- Stems are **scenarios** or **when-not-to-use**, not restated Pros/Cons bullets.
- Prefer transcript phrasing for `discriminate` items; discussions for when/tradeoff/examples.
- Include at least one `discriminate` per pattern.

### Fundamentals banks only

- `kind` is one of `identify` | `when` | `exception` | `tradeoff` | `discriminate` | `compose`. `exception` stems ask specifically when the usual advice flips (a documented "when not to apply" or edge case), separate from a general `when` question.
- Every stem must be **self-contained**: state (or generically scenario-ize) enough of the description/pros/cons/when-to-apply text that someone who has never read the docs or watched the video can still reason to the answer. Never reference "the video," "the docs," or assume outside context.
- Distractor choices restate real pros/cons/when-to-apply language from sibling patterns in the same bank group, not invented failure modes.
- Include at least one `exception` and one `discriminate` per pattern.

## Shape

```js
window.QUIZ_BANKS = window.QUIZ_BANKS || [];
window.QUIZ_BANKS.push({
  id: "core-fundamentals",
  title: "Core patterns — pros, cons & when to use (1–5)",
  patterns: ["prompt-chaining", "routing", "parallelization", "reflection", "tool-use"],
  questions: [
    {
      id: "fund-core-route-exception",
      pattern: "routing",
      kind: "exception",
      stem: "…",
      choices: ["A", "B", "C", "D"],
      answer: 1,
      explanation: "…"
    }
  ]
});
```
