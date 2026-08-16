## Why

The labs teach patterns by implementing them; there is no lightweight way to drill *when to pick which pattern* without reading code or frameworks. A disk-openable MCQ practice page, generated from the pattern docs and the video transcript, fills that gap while the 21-pattern table is already complete.

## What Changes

- Add a static quiz under `docs/quiz/`: HTML + JavaScript, no server, no `fetch`. Double-click `index.html` to practice.
- Add five question banks grouped as in the source docs: Core, Advanced, System, Optimization, Strategic. Banks are committed JS files (generated at implement time from the docs, not at runtime).
- Immediate right/wrong feedback with an explanation after each answer; a summary at the end (score, weak patterns in that bank, retry missed).
- Add the missing video transcript at `docs/transcripts/master-20-agentic-design-patterns.md` (captions for [Master ALL 20 Agentic AI Design Patterns](https://www.youtube.com/watch?v=e2zIr_2JMbE); omits MCP).
- Commit a generation prompt so banks can be regenerated later. Questions teach patterns (identify, when/not, tradeoff, discriminate, compose), never framework or lab code.
- Point README at the quiz as a learning aid. Not a lab package and not a Progress-table row.

## Capabilities

### New Capabilities

- `pattern-quiz`: Disk-openable MCQ practice for the 21 agentic patterns: five grouped banks generated from pattern-discussion/ascii/mermaid plus the video transcript, immediate feedback, end-of-bank summary.

### Modified Capabilities

- (none)

## Impact

- New files under `docs/quiz/` (HTML, JS shell, five bank scripts, generation prompt).
- New `docs/transcripts/master-20-agentic-design-patterns.md`.
- README: short pointer to the quiz (Setup/learning, not a new Progress cell).
- No Python packages, no uv deps, no Langfuse, no runtime LLM.
- `docs/agentic-design-patterns-docs/` stays gitignored; generation reads it locally. The committed summary table in `docs/agentic-design-patterns.md` is not the primary source for stems.
