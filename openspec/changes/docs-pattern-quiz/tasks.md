## 1. Transcript

- [x] 1.1 Add `docs/transcripts/master-20-agentic-design-patterns.md` with captions from [Master ALL 20 Agentic AI Design Patterns](https://www.youtube.com/watch?v=e2zIr_2JMbE) (MCP omitted; lightly clean auto-captions for readability)

## 2. Generation prompt

- [x] 2.1 Add `docs/quiz/GENERATION.md`: rubric (kinds, sibling distractors, why/why-not, no framework names), five bank groupings, and source paths (pattern-discussion, ascii-art, mermaid, transcript)

## 3. Practice shell

- [x] 3.1 Add `docs/quiz/index.html` that loads `quiz.js` and the five `bank-*.js` files via classic `<script src>`, with a bank picker, one-question view, feedback, and summary
- [x] 3.2 Add `docs/quiz/quiz.js`: shuffle question order (not choices), grade on select, show explanation, summary with per-pattern results and retry-missed

## 4. Question banks

- [x] 4.1 Generate `docs/quiz/bank-core.js` (patterns 1–5, ~6–8 questions each) from Core docs + transcript
- [x] 4.2 Generate `docs/quiz/bank-advanced.js` (patterns 6–10, including MCP from written docs) from Advanced docs + transcript
- [x] 4.3 Generate `docs/quiz/bank-system.js` (patterns 11–15) from System docs + transcript
- [x] 4.4 Generate `docs/quiz/bank-optimization.js` (patterns 16–19) from Optimization docs + transcript
- [x] 4.5 Generate `docs/quiz/bank-strategic.js` (patterns 20–21) from Strategic docs + transcript

## 5. README

- [x] 5.1 Point README at `docs/quiz/index.html` as a pattern-practice aid; leave the Progress table unchanged
