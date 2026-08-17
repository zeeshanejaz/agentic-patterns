window.QUIZ_BANKS = window.QUIZ_BANKS || [];
window.QUIZ_BANKS.push({
  id: "system-fundamentals",
  title: "System patterns — pros, cons & when to use (11–15)",
  patterns: ["goal-setting", "exception-handling", "human-in-the-loop", "knowledge-retrieval", "a2a"],
  questions: [
    {
      id: "fund-sys-goal-identify",
      pattern: "goal-setting",
      kind: "identify",
      stem: "Measurable goals like deadlines, budgets, and KPIs are defined; quality gates run continuously; progress is compared to targets; and resources, plan, or scope are adjusted when the system drifts. Which pattern?",
      choices: [
        "Goal setting and monitoring",
        "Exception handling and recovery",
        "Human-in-the-loop",
        "Knowledge retrieval (RAG)"
      ],
      answer: 0,
      explanation: "Defining measurable targets and adjusting when progress drifts from them is goal setting and monitoring. Exception handling reacts to failures, not general progress-vs-target drift. Human-in-the-loop pauses for human judgment. Knowledge retrieval grounds answers in a document corpus."
    },
    {
      id: "fund-sys-goal-when",
      pattern: "goal-setting",
      kind: "when",
      stem: "Which scenario best fits goal setting and monitoring?",
      choices: [
        "Autonomous, long-running work toward a business objective with budget or SLA constraints that should be tracked against targets",
        "A single failed API call that needs a retry",
        "A single high-risk decision needing a person's sign-off",
        "A factual question that needs a citation from a document"
      ],
      answer: 0,
      explanation: "Goal setting and monitoring fits objective-driven, resource-constrained, long-running work. A failed call is exception handling; a decision needing sign-off is human-in-the-loop; a cited factual answer is knowledge retrieval."
    },
    {
      id: "fund-sys-goal-exception",
      pattern: "goal-setting",
      kind: "exception",
      stem: "When is heavy goal-monitoring machinery unnecessary?",
      choices: [
        "A short, one-off task with no ongoing targets, deadlines, or budget to track",
        "A long-running project with a KPI and a deadline",
        "Work with resource or SLA constraints",
        "Work that should stay aligned with a business objective"
      ],
      answer: 0,
      explanation: "Without any ongoing target to compare progress against, monitoring machinery has nothing useful to measure. The other options describe exactly the situations goal setting and monitoring is built for."
    },
    {
      id: "fund-sys-goal-tradeoff",
      pattern: "goal-setting",
      kind: "tradeoff",
      stem: "What is a documented cost of goal setting and monitoring?",
      choices: [
        "Extra machinery and overhead, rigid constraints, hard-to-quantify goals, and risk of metric gaming or conflicting goals",
        "It guarantees every goal is easy to quantify",
        "It removes the need for any ongoing monitoring",
        "It eliminates conflicts between competing goals"
      ],
      answer: 0,
      explanation: "Tracking measurable targets adds overhead and can be gamed or produce conflicting objectives — the tradeoff for purposeful, accountable execution. It does not guarantee easy quantification or eliminate goal conflicts."
    },
    {
      id: "fund-sys-goal-disc-exception",
      pattern: "goal-setting",
      also: ["exception-handling"],
      kind: "discriminate",
      stem: "One system compares 'tasks completed' against a weekly target and reallocates resources when it's behind. Another system retries a failed network call with backoff and escalates once retries are exhausted. Which one is goal setting and monitoring?",
      choices: [
        "The one comparing progress against a weekly target",
        "The one retrying a failed network call",
        "Both, because both react to a problem",
        "Neither, without a human involved"
      ],
      answer: 0,
      explanation: "Comparing progress against a measurable target and reallocating resources is goal setting and monitoring. Reacting to an individual failure with retry/backoff/escalation is exception handling and recovery."
    },
    {
      id: "fund-sys-goal-disc-hitl",
      pattern: "goal-setting",
      also: ["human-in-the-loop"],
      kind: "discriminate",
      stem: "Is comparing project velocity against a KPI and re-scoping when behind an example of goal setting and monitoring, or human-in-the-loop?",
      choices: [
        "Goal setting and monitoring",
        "Human-in-the-loop",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "This is goal setting and monitoring: tracking a measurable target and adjusting scope. Human-in-the-loop specifically pauses execution for a person to approve, edit, deny, or take over — no such pause is described here."
    },
    {
      id: "fund-sys-except-identify",
      pattern: "exception-handling",
      kind: "identify",
      stem: "Failures are caught and classified as temporary or permanent; temporary ones are retried with capped backoff; the system degrades to a fallback when needed; and critical errors trigger an emergency stop plus an alert. Which pattern?",
      choices: [
        "Exception handling and recovery",
        "Goal setting and monitoring",
        "Human-in-the-loop",
        "Inter-agent communication"
      ],
      answer: 0,
      explanation: "Classify-retry-degrade-alert on failures is exception handling and recovery. Goal setting tracks progress vs. targets, not failure recovery. Human-in-the-loop pauses for a person's judgment, not automated retry logic. Inter-agent communication is about messaging between agents."
    },
    {
      id: "fund-sys-except-when",
      pattern: "exception-handling",
      kind: "when",
      stem: "Which scenario is the clearest fit for exception handling and recovery?",
      choices: [
        "Production systems calling unreliable external APIs, where transient failures should be retried and permanent ones should degrade gracefully rather than fail closed",
        "A long-running project needing KPI tracking against a deadline",
        "A high-stakes decision needing a person's sign-off",
        "Agents needing a shared, structured messaging protocol"
      ],
      answer: 0,
      explanation: "Exception handling and recovery is aimed squarely at unreliable dependencies and production reliability. KPI tracking is goal setting; sign-off is human-in-the-loop; a shared messaging protocol is inter-agent communication."
    },
    {
      id: "fund-sys-except-exception",
      pattern: "exception-handling",
      kind: "exception",
      stem: "When is heavy retry/fallback machinery unnecessary?",
      choices: [
        "A purely deterministic, local computation with no external dependency and no way to fail transiently",
        "A system that calls unreliable external APIs",
        "A user-facing system that must not fail closed",
        "A pipeline exposed to network or quota issues"
      ],
      answer: 0,
      explanation: "If there is no external dependency or transient-failure mode, retry/backoff/fallback logic has nothing to protect against. The other options describe exactly where exception handling and recovery is needed."
    },
    {
      id: "fund-sys-except-tradeoff",
      pattern: "exception-handling",
      kind: "tradeoff",
      stem: "What is a documented cost of exception handling and recovery?",
      choices: [
        "Added code and infrastructure complexity, retry latency, false positives, and risk of alert fatigue or cascading retries if poorly designed",
        "It guarantees zero latency overhead",
        "It removes the need for any alerting",
        "It can never cascade or make things worse"
      ],
      answer: 0,
      explanation: "Building robust failure handling adds real complexity and latency, and poorly designed retries or alerts can misfire or cascade — the tradeoff for resilience. It does not guarantee zero overhead or risk-free retries."
    },
    {
      id: "fund-sys-except-disc-goal",
      pattern: "exception-handling",
      also: ["goal-setting"],
      kind: "discriminate",
      stem: "A payment API times out, gets retried twice with backoff, and then falls back to a queued retry job. Is this exception handling and recovery, or goal setting and monitoring?",
      choices: [
        "Exception handling and recovery",
        "Goal setting and monitoring",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "Reacting to an individual failure with retry, backoff, and fallback is exception handling and recovery. Goal setting and monitoring is about tracking progress against a measurable target, not about a single failed call."
    },
    {
      id: "fund-sys-except-disc-hitl",
      pattern: "exception-handling",
      also: ["human-in-the-loop"],
      kind: "discriminate",
      stem: "A critical error triggers an automatic emergency stop and alert with no person involved in the decision to stop. Is this exception handling and recovery, or human-in-the-loop?",
      choices: [
        "Exception handling and recovery",
        "Human-in-the-loop",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "An automated stop-and-alert with no human decision point is exception handling and recovery. Human-in-the-loop specifically requires pausing for a person to approve, edit, deny, or take over, which is absent here."
    },
    {
      id: "fund-sys-hitl-identify",
      pattern: "human-in-the-loop",
      kind: "identify",
      stem: "At a high-risk, low-confidence, or compliance-sensitive point, the system pauses so a human can approve, edit, deny, or take over, then execution resumes. Which pattern?",
      choices: [
        "Human-in-the-loop",
        "Exception handling and recovery",
        "Goal setting and monitoring",
        "Knowledge retrieval (RAG)"
      ],
      answer: 0,
      explanation: "Pausing specifically for human judgment at a risk point is human-in-the-loop. Exception handling reacts to failures automatically. Goal setting compares progress to targets. Knowledge retrieval grounds answers in documents."
    },
    {
      id: "fund-sys-hitl-when",
      pattern: "human-in-the-loop",
      kind: "when",
      stem: "Which scenario best fits human-in-the-loop?",
      choices: [
        "A high-stakes decision (medical, legal, financial) where a wrong automated call is costly and a person should sign off",
        "A transient network failure that should just be retried",
        "Tracking a budget against a weekly target",
        "Answering from a document corpus with citations"
      ],
      answer: 0,
      explanation: "Human-in-the-loop is for high-stakes, compliance-sensitive, or low-confidence decisions. A transient failure is exception handling; budget tracking is goal setting; citing sources is knowledge retrieval."
    },
    {
      id: "fund-sys-hitl-exception",
      pattern: "human-in-the-loop",
      kind: "exception",
      stem: "When does inserting a human checkpoint stop making sense?",
      choices: [
        "High-volume, low-stakes, well-understood decisions where waiting for a person mainly adds cost and delay without meaningfully reducing risk",
        "A high-stakes decision with real consequences",
        "A compliance-sensitive review",
        "An unusual edge case the system hasn't seen before"
      ],
      answer: 0,
      explanation: "Human-in-the-loop's documented cost is throughput/latency/cost from waiting on a person — not worth it for low-stakes, routine decisions. The other options are exactly where a human checkpoint earns its cost."
    },
    {
      id: "fund-sys-hitl-tradeoff",
      pattern: "human-in-the-loop",
      kind: "tradeoff",
      stem: "What is a documented cost of human-in-the-loop?",
      choices: [
        "Throughput and cost limits, wait time, inconsistent reviewers, fatigue, and difficulty covering review around the clock",
        "It guarantees an instant response every time",
        "It removes any need for review criteria",
        "It scales infinitely at no added cost"
      ],
      answer: 0,
      explanation: "Adding a human checkpoint bounds throughput, adds wait time, and depends on reviewer consistency and availability — the tradeoff for human judgment on risky decisions. It does not guarantee instant, free, infinite scaling."
    },
    {
      id: "fund-sys-hitl-disc-except",
      pattern: "human-in-the-loop",
      also: ["exception-handling"],
      kind: "discriminate",
      stem: "A low-confidence medical recommendation is paused for a clinician to approve before it reaches a patient. A separate case has a timed-out API call automatically retried three times before falling back. Which one is human-in-the-loop?",
      choices: [
        "The recommendation paused for clinician approval",
        "The timed-out call being retried automatically",
        "Both, because both handle a problem",
        "Neither, without an emergency stop"
      ],
      answer: 0,
      explanation: "Pausing for a person's approval is human-in-the-loop. Automated retry and fallback on a timeout, with no human involved, is exception handling and recovery."
    },
    {
      id: "fund-sys-hitl-disc-goal",
      pattern: "human-in-the-loop",
      also: ["goal-setting"],
      kind: "discriminate",
      stem: "Which is human-in-the-loop: pausing an automated loan decision for a compliance officer to approve, or comparing loan-approval throughput against a weekly target?",
      choices: [
        "Pausing the loan decision for a compliance officer to approve",
        "Comparing throughput against a weekly target",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "A pause for a person's approval is human-in-the-loop. Comparing throughput to a target is goal setting and monitoring, with no human decision point described."
    },
    {
      id: "fund-sys-know-identify",
      pattern: "knowledge-retrieval",
      kind: "identify",
      stem: "Documents are parsed, chunked, and embedded; the top-k most relevant chunks are retrieved (optionally reranked); and a grounded answer is generated with citations back to the source. Which pattern?",
      choices: [
        "Knowledge retrieval (RAG)",
        "Human-in-the-loop",
        "Exception handling and recovery",
        "Inter-agent communication"
      ],
      answer: 0,
      explanation: "Chunk, embed, retrieve, and cite is knowledge retrieval's (RAG) signature. Human-in-the-loop pauses for a person. Exception handling reacts to failures. Inter-agent communication is structured messages between agents."
    },
    {
      id: "fund-sys-know-when",
      pattern: "knowledge-retrieval",
      kind: "when",
      stem: "Which scenario best fits knowledge retrieval (RAG)?",
      choices: [
        "Answering domain questions from a large or frequently changing document corpus where factual accuracy and citations matter",
        "A high-stakes decision needing a person's sign-off",
        "A flaky external API call that needs a retry",
        "Agents needing a shared messaging protocol"
      ],
      answer: 0,
      explanation: "Knowledge retrieval fits large/dynamic corpora where grounding and citations reduce hallucination. Sign-off is human-in-the-loop; retrying a flaky call is exception handling; a shared messaging protocol is inter-agent communication."
    },
    {
      id: "fund-sys-know-exception",
      pattern: "knowledge-retrieval",
      kind: "exception",
      stem: "When does adding a retrieval layer over a document corpus stop paying off?",
      choices: [
        "When the needed facts are small, stable, and easily fit directly in the prompt, so indexing and retrieval infrastructure adds overhead without meaningfully reducing hallucination",
        "When the corpus is large and changes often",
        "When answers must cite their sources",
        "When factual accuracy is a priority"
      ],
      answer: 0,
      explanation: "Retrieval infrastructure earns its cost against a large or dynamic corpus. If the needed facts already fit comfortably in the prompt, building an index adds overhead for little benefit. The other options describe exactly when retrieval helps."
    },
    {
      id: "fund-sys-know-tradeoff",
      pattern: "knowledge-retrieval",
      kind: "tradeoff",
      stem: "What is a documented cost of knowledge retrieval (RAG)?",
      choices: [
        "Vector/index infrastructure to build and maintain, retrieval and chunking quality issues, extra latency, and upkeep as the corpus grows",
        "It guarantees zero hallucination",
        "It removes the need for any chunking strategy",
        "It has no infrastructure cost"
      ],
      answer: 0,
      explanation: "Retrieval requires real infrastructure (indexes, embeddings), and chunking/retrieval quality directly affects answer quality — the tradeoff for grounded, citable answers. It does not guarantee zero hallucination or come free of infrastructure."
    },
    {
      id: "fund-sys-know-disc-hitl",
      pattern: "knowledge-retrieval",
      also: ["human-in-the-loop"],
      kind: "discriminate",
      stem: "A support answer cites two retrieved policy documents and their sections. A different support answer is held for a human reviewer before being sent. Which one demonstrates knowledge retrieval?",
      choices: [
        "The answer citing retrieved policy documents",
        "The answer held for human review",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "Grounding an answer in retrieved, cited sources is knowledge retrieval (RAG). Holding an answer for a person before sending it, with no retrieval or citation step described, is human-in-the-loop."
    },
    {
      id: "fund-sys-know-disc-a2a",
      pattern: "knowledge-retrieval",
      also: ["a2a"],
      kind: "discriminate",
      stem: "Is retrieving the top-k relevant passages from a document index to ground an answer best described as knowledge retrieval, or inter-agent communication?",
      choices: [
        "Knowledge retrieval (RAG)",
        "Inter-agent communication",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "Retrieving and citing passages from a document index is knowledge retrieval. Inter-agent communication is about structured messages (with IDs, expiry, auth) passed between agents, not document retrieval."
    },
    {
      id: "fund-sys-a2a-identify",
      pattern: "a2a",
      kind: "identify",
      stem: "Agents exchange structured messages with IDs, expiry, and authentication, following rules for resolving conflicts, across a topology such as a coordinator, peers, or a shared board; loops are capped and stale messages are dropped. Which pattern?",
      choices: [
        "Inter-agent communication (A2A)",
        "Knowledge retrieval (RAG)",
        "Goal setting and monitoring",
        "Human-in-the-loop"
      ],
      answer: 0,
      explanation: "Structured inter-agent messaging with IDs/expiry/auth and a topology is A2A's signature. Knowledge retrieval grounds answers in documents. Goal setting tracks progress vs. targets. Human-in-the-loop pauses for a person."
    },
    {
      id: "fund-sys-a2a-when",
      pattern: "a2a",
      kind: "when",
      stem: "Which scenario best fits inter-agent communication (A2A)?",
      choices: [
        "A complex multi-agent workflow where agents need a reliable, structured way to pass messages, requests, and results to each other",
        "Answering a question from a document corpus",
        "Tracking a project's KPI drift over time",
        "Pausing for a compliance officer's sign-off"
      ],
      answer: 0,
      explanation: "A2A is the wiring for complex, multi-agent workflows that need structured messaging. Answering from a corpus is knowledge retrieval; KPI drift is goal setting; a sign-off pause is human-in-the-loop."
    },
    {
      id: "fund-sys-a2a-exception",
      pattern: "a2a",
      kind: "exception",
      stem: "When is building a formal inter-agent messaging protocol overkill?",
      choices: [
        "A setup with only one or two agents and no real message routing between them, where the overhead of IDs, expiry, and conflict rules isn't justified — a simpler design is preferable",
        "A composable, distributed multi-agent system",
        "A service-oriented design with several collaborating agents",
        "A complex multi-agent workflow needing message tracing"
      ],
      answer: 0,
      explanation: "A2A's documented advice is to prefer simpler designs unless there is dedicated engineering behind a real multi-agent system. With only one or two agents and no real routing need, the protocol's overhead outweighs the benefit."
    },
    {
      id: "fund-sys-a2a-tradeoff",
      pattern: "a2a",
      kind: "tradeoff",
      stem: "What is a documented cost of inter-agent communication (A2A)?",
      choices: [
        "Protocol complexity, message latency, hard-to-debug distributed interactions, and consistency/security concerns between agents",
        "It guarantees zero message latency",
        "It removes the need for any authentication between agents",
        "It eliminates any debugging difficulty across agents"
      ],
      answer: 0,
      explanation: "Formalizing agent-to-agent messaging adds protocol overhead, latency, and distributed-debugging difficulty — the tradeoff for modularity and scale. It does not eliminate latency, auth needs, or debugging complexity."
    },
    {
      id: "fund-sys-a2a-disc-know",
      pattern: "a2a",
      also: ["knowledge-retrieval"],
      kind: "discriminate",
      stem: "Which is inter-agent communication: two agents exchanging a structured request/response message with an expiry and an ID, or a single agent retrieving the top-k passages from a document index?",
      choices: [
        "The structured message exchange between two agents",
        "The retrieval of top-k passages",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "A structured, IDed message exchange between agents is inter-agent communication. Retrieving passages from a document index, with no agent-to-agent messaging involved, is knowledge retrieval instead."
    },
    {
      id: "fund-sys-a2a-disc-goal",
      pattern: "a2a",
      also: ["goal-setting"],
      kind: "discriminate",
      stem: "A shared message board lets agents post and claim tasks, with conflict rules for duplicate claims. Is this inter-agent communication, or goal setting and monitoring?",
      choices: [
        "Inter-agent communication",
        "Goal setting and monitoring",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "A shared board with posting, claiming, and conflict rules describes how agents pass messages to each other — inter-agent communication. Goal setting and monitoring is about comparing progress to measurable targets, which isn't described here."
    },
    {
      id: "fund-sys-hitl-compose",
      pattern: "goal-setting",
      also: ["human-in-the-loop"],
      kind: "compose",
      stem: "A goal-setting monitor detects the project is behind its KPI target and escalates a specific budget decision to a human for sign-off before reallocating funds. How should this be described?",
      choices: [
        "Goal setting and monitoring detects the drift; human-in-the-loop is the escalation step for the risky decision — the two compose rather than compete",
        "Only one pattern ever applies, so this is just goal setting and monitoring with no human involved",
        "Goal setting and monitoring replaces the need for any human check",
        "Human-in-the-loop replaces the need to track any KPI"
      ],
      answer: 0,
      explanation: "Patterns combine: goal setting and monitoring flags the drift against a target, and human-in-the-loop handles the risky decision point that follows. Neither replaces the other."
    }
  ]
});
