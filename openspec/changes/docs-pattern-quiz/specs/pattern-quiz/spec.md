## ADDED Requirements

### Requirement: Disk-openable practice page
The repository SHALL provide a static MCQ practice page at `docs/quiz/index.html` that loads without a web server, without `fetch`, and without ES modules.

#### Scenario: Open from disk
- **WHEN** a learner opens `docs/quiz/index.html` from the filesystem
- **THEN** the page SHALL load its script and bank files via classic relative `<script src>` tags and SHALL present a bank picker

#### Scenario: No network runtime
- **WHEN** the page is used
- **THEN** it MUST NOT call a remote API, MUST NOT use `fetch` to load questions, and MUST NOT require Python or uv

### Requirement: Five grouped banks
The quiz SHALL expose five banks aligned with the source docs groups, each as a committed JavaScript file that registers itself on `window.QUIZ_BANKS`.

#### Scenario: Bank list
- **WHEN** the start screen is shown
- **THEN** the learner SHALL be able to choose Core (patterns 1–5), Advanced (6–10), System (11–15), Optimization (16–19), or Strategic (20–21)

#### Scenario: Bank files
- **WHEN** the page loads
- **THEN** `bank-core.js`, `bank-advanced.js`, `bank-system.js`, `bank-optimization.js`, and `bank-strategic.js` MUST each push one bank object with `id`, `title`, `patterns`, and `questions`

#### Scenario: Advanced includes MCP
- **WHEN** the Advanced bank is loaded
- **THEN** it MUST include Model Context Protocol questions sourced from the written pattern discussion even though the video transcript omits MCP

#### Scenario: Coverage
- **WHEN** a bank is generated
- **THEN** it MUST contain about 6–8 questions per pattern in that group (Strategic MAY be at the low end) and each question MUST have exactly four choices and a 0-based `answer` index

### Requirement: Immediate feedback and summary
Answering a question SHALL show whether the choice was correct, then a session summary SHALL appear after the last question in the bank (or after the last missed item on retry).

#### Scenario: Grade on answer
- **WHEN** the learner selects a choice
- **THEN** the page SHALL lock further changes for that question, SHALL show correct vs incorrect, and SHALL show the item’s `explanation`

#### Scenario: Next
- **WHEN** the learner continues after feedback
- **THEN** the page SHALL show the next unanswered question in the session order

#### Scenario: Summary
- **WHEN** the last question of the session is graded
- **THEN** the page SHALL show total correct/total, per-pattern results for that bank, and the missed stems with the right answers

#### Scenario: Retry missed
- **WHEN** the learner chooses retry missed after a summary that includes misses
- **THEN** the next session SHALL contain only the missed items from that bank run

#### Scenario: Shuffle
- **WHEN** a new bank session starts
- **THEN** question order MUST be shuffled and choice order MUST stay as authored

### Requirement: Pattern-only question quality
Questions SHALL teach agentic pattern choice from the docs and transcript, not frameworks or lab code.

#### Scenario: Kinds
- **WHEN** a question is authored
- **THEN** it MUST set `kind` to one of `identify`, `when`, `tradeoff`, `discriminate`, or `compose`

#### Scenario: Distractors
- **WHEN** a question offers wrong choices
- **THEN** those choices MUST be sibling patterns or design moves from the same bank, not APIs or code

#### Scenario: No framework trivia
- **WHEN** any bank question is displayed
- **THEN** its stem, choices, and explanation MUST NOT name LangChain, LangGraph, Microsoft Agent Framework, FastMCP, OO-Agents, Langfuse, or lab module paths

#### Scenario: Explanation
- **WHEN** feedback is shown
- **THEN** the explanation MUST say why the keyed answer is right and why at least one distractor is wrong

### Requirement: Generated from docs and transcript
Banks SHALL be produced from the pattern-discussion, ascii-art, and mermaid-diagram files plus the video transcript, using a committed generation prompt.

#### Scenario: Transcript file
- **WHEN** this change lands
- **THEN** `docs/transcripts/master-20-agentic-design-patterns.md` MUST exist as captions for the Master ALL 20 Agentic AI Design Patterns video

#### Scenario: Generation prompt
- **WHEN** a developer opens `docs/quiz/GENERATION.md`
- **THEN** they SHALL find the rubric, the five bank groupings, and the source paths to regenerate banks

#### Scenario: Committed output
- **WHEN** a learner takes the quiz
- **THEN** questions MUST come from the committed `bank-*.js` files, not from generating at page load

### Requirement: README pointer
The repository README SHALL tell a learner how to open the quiz and SHALL NOT treat it as a Progress-table lab.

#### Scenario: Discoverable
- **WHEN** a developer reads the README
- **THEN** they SHALL find a pointer to `docs/quiz/index.html` as a pattern-practice aid

#### Scenario: Progress table unchanged
- **WHEN** this change lands
- **THEN** the 21-pattern Progress table MUST NOT gain a quiz column or change shipped/pending cells because of the quiz
