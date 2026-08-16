# Regenerating pattern quiz banks

Banks are committed JavaScript. The page never calls a model. To regenerate, read the sources below, write `bank-*.js` in this folder, and keep the question shape in `quiz.js`.

## Output files

| File | Group | Patterns |
|---|---|---|
| `bank-core.js` | Core (1–5) | prompt-chaining, routing, parallelization, reflection, tool-use |
| `bank-advanced.js` | Advanced (6–10) | planning, multi-agent, memory-management, learning, mcp |
| `bank-system.js` | System (11–15) | goal-setting, exception-handling, human-in-the-loop, knowledge-retrieval, a2a |
| `bank-optimization.js` | Optimization (16–19) | resource-aware, reasoning, guardrails, evaluation |
| `bank-strategic.js` | Strategic (20–21) | prioritization, exploration |

Each file must call `window.QUIZ_BANKS.push({ id, title, patterns, questions })`. Canonical `pattern` slugs are the strings in the table.

## Sources (read these, not lab code)

Per pattern:

- `docs/agentic-design-patterns-docs/pattern-discussion/<file>.md`
- `docs/agentic-design-patterns-docs/ascii-art/<file>.txt` (KEY CONCEPTS)
- `docs/agentic-design-patterns-docs/mermaid-diagrams/<file>.mmd` (flow, not syntax)
- Matching `##` section in `docs/transcripts/master-20-agentic-design-patterns.md`

The video **omits MCP**. Advanced MCP items come only from `pattern-discussion/model-context-protocol.md` (and ascii/mermaid). Spoken order in the transcript swaps evaluation (#19) ahead of guardrails (#18); banks still follow the table above.

The clone under `docs/agentic-design-patterns-docs/` is gitignored. Regeneration needs it locally. Taking the quiz only needs the committed `bank-*.js` files.

## Rubric

- About **6–8 questions per pattern** (Strategic may sit at the low end).
- Each item: `id`, `pattern`, optional `also` (confusion partners), `kind` (`identify` | `when` | `tradeoff` | `discriminate` | `compose`), `stem`, `choices` (exactly four strings), `answer` (0-based), `explanation`.
- Stems are **scenarios** or **when-not-to-use**, not restated Pros/Cons bullets.
- Wrong choices are **sibling patterns or design moves in the same bank**, not APIs or code.
- `explanation` says why the keyed answer is right **and** why at least one distractor is wrong.
- Prefer transcript phrasing for `discriminate` items; discussions for when/tradeoff/examples.
- **Do not** name LangChain, LangGraph, Microsoft Agent Framework, FastMCP, OO-Agents, Langfuse, or lab module paths.
- Mix kinds inside each pattern. Include at least one `discriminate` and one `when` (including when *not*) per pattern.
- `compose` stays **inside the bank** (e.g. routing + tool use in Core). No cross-group mix bank.

## Shape

```js
window.QUIZ_BANKS = window.QUIZ_BANKS || [];
window.QUIZ_BANKS.push({
  id: "core",
  title: "Core patterns (1–5)",
  patterns: ["prompt-chaining", "routing", "parallelization", "reflection", "tool-use"],
  questions: [
    {
      id: "core-routing-disc-1",
      pattern: "routing",
      also: ["prompt-chaining"],
      kind: "discriminate",
      stem: "…",
      choices: ["A", "B", "C", "D"],
      answer: 1,
      explanation: "…"
    }
  ]
});
```
