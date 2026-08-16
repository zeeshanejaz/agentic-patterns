## Context

The repo’s learning loop is implement-then-port. Docs already explain the 21 patterns (`docs/agentic-design-patterns-docs/` locally; gitignored clone) and point at a video transcript that is not on disk. There is no practice surface for choosing patterns. The quiz is a static learning aid, not a lab.

## Goals / Non-Goals

**Goals:**

- Double-click `docs/quiz/index.html` and practice with no server, no `fetch`, no ES modules.
- Five banks matching the source groups: Core (1–5), Advanced (6–10), System (11–15), Optimization (16–19), Strategic (20–21).
- Immediate right/wrong + explanation; end-of-bank summary (score, weak patterns, retry missed).
- Banks generated at implement time from pattern-discussion, ascii-art, mermaid-diagrams, and the video transcript; committed as JS.
- Questions teach pattern choice (identify / when / tradeoff / discriminate / compose-within-bank), never framework or package code.
- Add the missing transcript file the summary doc already links.
- README pointer only.

**Non-Goals:**

- Runtime LLM, Python generator package, or uv dependency.
- A sixth cross-group compose bank.
- Exam mode (delayed scoring), accounts, spaced repetition.
- Quiz questions about LangChain, MAF, FastMCP APIs, OO-Agents, Langfuse, or lab modules.
- Changing pattern implementations or the Progress table.
- Hosting or a local HTTP server.

## Decisions

1. **Classic scripts, same folder, no JSON fetch.** `file://` blocks `fetch` and often ES `import`. `index.html` loads `quiz.js` and `bank-*.js` via `<script src>`. Each bank file calls `window.QUIZ_BANKS.push({...})`. Alternative considered: embed all questions in one HTML file (harder to regenerate per bank) or `python -m http.server` (user asked to run from disk).

2. **Five banks = docs groups, not confusion-pair clusters.** Sibling distractors stay inside the bank so Core does not leak Planning. Strategic is short (~12–16 items); that is acceptable. Alternative considered: pedagogical clusters (sequencing / quality / knowledge); rejected because it fights the source grouping the user asked to use.

3. **Generate once, commit the banks.** Apply-time LLM reads a source pack per bank and writes `bank-*.js`. `docs/quiz/GENERATION.md` holds the rubric and source paths so regeneration is possible. Alternative considered: a Python script that calls OpenAI on every regen (extra package, nondeterministic CI); or regex over Pros/Cons (low quality).

4. **Transcript is a first-class source.** Author `docs/transcripts/master-20-agentic-design-patterns.md` from the YouTube captions ([Master ALL 20 Agentic AI Design Patterns](https://www.youtube.com/watch?v=e2zIr_2JMbE)). Prefer spoken distinctions for `discriminate` items. MCP is docs-only (video omits it); Advanced still includes MCP. Alternative considered: skip the transcript until it exists — rejected; the summary doc already links it and the user named it as a source.

5. **Question shape.** Each item: `id`, `pattern` (canonical slug), optional `also` (confusion partners), `kind` (`identify` | `when` | `tradeoff` | `discriminate` | `compose`), `stem`, `choices` (exactly four strings), `answer` (0-based index), `explanation` (why this, why not the others). No code fences, no API names. Target ~6–8 questions per pattern (Strategic can sit at the low end).

6. **Session flow.** Start: pick a bank. One question at a time; lock the choice; show correct vs selected + explanation; Next. Shuffle question order per session; do not shuffle choices (keeps review stable). Summary: count correct/total, per-pattern miss rates, missed stems, Retry missed, Back to banks.

7. **Styles live in `index.html` (or a sibling `quiz.css` loaded with `<link>`).** Either works on `file://`. Prefer a sibling CSS only if the HTML would otherwise be noisy; default is inline or one `quiz.css`. No build step.

8. **README.** A short “Practice” or learning-aid line pointing at `docs/quiz/index.html`. Do not add a Progress-table column or a `uv run` command.

## Risks / Trade-offs

- [file:// still blocks some browsers] → keep scripts as classic tags in `docs/quiz/` (not nested deep); no modules. If a browser still blocks, document “open the HTML file directly from Explorer/Finder.”
- [Shallow generated questions] → GENERATION.md forbids restating Pros/Cons bullets; requires sibling-pattern distractors and a why/why-not explanation. Spot-check a sample per bank during apply.
- [Clone gitignored; regen needs local docs] → committed banks are enough to take the quiz. Regen requires `docs/agentic-design-patterns-docs/` present (already cloned locally).
- [Transcript quality / missing captions] → store cleaned captions as markdown; if auto-captions are messy, lightly edit for readability without adding framework content.
- [Strategic bank too small] → still ship it as its own group; do not merge into Optimization.
- [Stale banks if docs change] → docs are a book companion and rarely move; regen via GENERATION.md when needed.

## Migration Plan

Add `docs/quiz/*`, `docs/transcripts/master-20-agentic-design-patterns.md`, and a README pointer. Rollback is delete those files and revert the README line.

## Open Questions

None. Compose/mix bank stays out of this change.
