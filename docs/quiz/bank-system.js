window.QUIZ_BANKS = window.QUIZ_BANKS || [];
window.QUIZ_BANKS.push({
  id: "system",
  title: "System patterns (11–15)",
  patterns: ["goal-setting", "exception-handling", "human-in-the-loop", "knowledge-retrieval", "a2a"],
  questions: [
    {
      id: "sys-goal-identify-1",
      pattern: "goal-setting",
      kind: "identify",
      stem: "You define measurable goals (deadlines, budgets, KPIs), run quality gates, compare progress to targets, and adjust resources, plan, or scope when the system drifts — like a GPS that recalculates. Which pattern?",
      choices: [
        "Goal setting and monitoring",
        "Exception handling and recovery",
        "Human-in-the-loop",
        "Knowledge retrieval (RAG)"
      ],
      answer: 0,
      explanation: "SMART-style objectives plus continuous compare-to-target. Exceptions catch failures. HITL pauses for a person. RAG retrieves documents."
    },
    {
      id: "sys-goal-when-1",
      pattern: "goal-setting",
      kind: "when",
      stem: "An autonomous publisher must hit a weekly quota and a cost cap, and should warn early if it is off-pace. Which pattern?",
      choices: [
        "A2A — agents email each other the quota",
        "Goal setting and monitoring — KPIs, gates, drift, adjust",
        "RAG — embed the quota document",
        "HITL — a human types every headline"
      ],
      answer: 1,
      explanation: "Docs: autonomous work toward objectives, SLAs, cost control. A2A is the message fabric. RAG does not track a KPI. HITL is a gate, not a dashboard."
    },
    {
      id: "sys-goal-when-2",
      pattern: "goal-setting",
      kind: "when",
      stem: "When is goal setting the wrong extra machinery?",
      choices: [
        "A multi-week pipeline with a real budget",
        "A one-shot lookup with no objective besides ‘answer this’",
        "Sales pipeline conversion targets",
        "Cost management on a long batch"
      ],
      answer: 1,
      explanation: "The video calls this advanced: overhead, rigid constraints, metric gaming. Do not wrap every call in KPIs."
    },
    {
      id: "sys-goal-tradeoff-1",
      pattern: "goal-setting",
      kind: "tradeoff",
      stem: "The agent maximizes ‘tickets closed’ by closing them empty. What pattern failure is that?",
      choices: [
        "A2A loop with no TTL",
        "Metric gaming / wrong KPI — a goal-setting con",
        "Missing citations in RAG",
        "A human never being asked"
      ],
      answer: 1,
      explanation: "Docs: false metrics, goal conflicts, over-optimization. Empty closes are not an A2A TTL bug."
    },
    {
      id: "sys-goal-disc-1",
      pattern: "goal-setting",
      also: ["exception-handling"],
      kind: "discriminate",
      stem: "Spend is 20% over budget but no API has thrown. Which pattern should notice?",
      choices: [
        "Exception handling — treat budget as an HTTP error",
        "Goal setting and monitoring — compare metric to target and adjust",
        "RAG — retrieve the finance PDF",
        "A2A — send a message with no expiry"
      ],
      answer: 1,
      explanation: "Drift vs crash: exceptions classify failures and retry. Goal monitoring watches KPIs while the system is still ‘succeeding.’"
    },
    {
      id: "sys-goal-disc-2",
      pattern: "goal-setting",
      also: ["human-in-the-loop"],
      kind: "discriminate",
      stem: "Off-course, the GPS recalculates by itself within policy. When would you add HITL instead of only adjusting?",
      choices: [
        "Never — KPIs replace humans",
        "When the adjustment is high-stakes, out of policy, or an edge the metrics cannot settle",
        "Whenever a number is compared to a target",
        "Only if RAG is also present"
      ],
      answer: 1,
      explanation: "Goal setting can auto-adjust scope/resources. HITL is the pause for a person when autonomy is not allowed."
    },
    {
      id: "sys-goal-compose-1",
      pattern: "goal-setting",
      kind: "compose",
      stem: "You monitor cost KPIs and, on a hard SLA miss, stop and alert. Which pairing?",
      choices: [
        "Goal setting for the metric; exception/recovery (or emergency stop) when it is no longer a soft drift",
        "Only RAG",
        "Only A2A",
        "HITL forbids metrics"
      ],
      answer: 0,
      explanation: "Soft drift → adjust. Hard failure → exception path. Humans still join if policy says so."
    },
    {
      id: "sys-exc-identify-1",
      pattern: "exception-handling",
      kind: "identify",
      stem: "Catch failures, classify temporary vs permanent, retry with capped backoff, degrade to fallbacks, emergency-stop and alert on critical errors. Which pattern?",
      choices: [
        "Goal setting and monitoring",
        "Exception handling and recovery",
        "Human-in-the-loop",
        "Knowledge retrieval (RAG)"
      ],
      answer: 1,
      explanation: "The video: this is how you catch errors in other agentic patterns. Goal setting is KPI drift. HITL is a person. RAG is documents."
    },
    {
      id: "sys-exc-when-1",
      pattern: "exception-handling",
      kind: "when",
      stem: "A payments API rate-limits you. What should the recovery pattern do first?",
      choices: [
        "Retrieve more chunks from the vector index",
        "Treat it as likely temporary: capped backoff, then fallback gateway or saved state",
        "Open a human review for every 429 including retries already in policy",
        "Start an A2A democracy so every agent votes on the HTTP code"
      ],
      answer: 1,
      explanation: "Temporary vs permanent, exponential backoff with a cap, plan B. RAG and A2A do not classify HTTP failures. HITL is a backup option, not the first move on a known rate limit."
    },
    {
      id: "sys-exc-when-2",
      pattern: "exception-handling",
      kind: "when",
      stem: "The video says you can use this in every pattern. What is still a misuse?",
      choices: [
        "Wrapping production tool calls",
        "Infinite retries with no cap so a permanent outage never surfaces",
        "Saving work before an emergency stop",
        "Falling back to a simpler method"
      ],
      answer: 1,
      explanation: "Uncapped retries can cascade (docs) and hide permanent faults. Caps, classify, then fallback or stop."
    },
    {
      id: "sys-exc-tradeoff-1",
      pattern: "exception-handling",
      kind: "tradeoff",
      stem: "You page the team on every retry. What happens?",
      choices: [
        "Better RAG precision",
        "Alert fatigue — the boy who cried wolf, so real incidents get ignored",
        "Goals become SMART automatically",
        "A2A TTLs reset"
      ],
      answer: 1,
      explanation: "Transcript: be judicious about what is worth an alert. That is an exception-handling con, not a retrieval metric."
    },
    {
      id: "sys-exc-disc-1",
      pattern: "exception-handling",
      also: ["human-in-the-loop"],
      kind: "discriminate",
      stem: "A transient timeout vs a $500 refund the model must not complete. Which mapping is right?",
      choices: [
        "Both are RAG ranking problems",
        "Timeout: exception retry/fallback; refund-over-threshold: HITL gate",
        "Both must always be HITL",
        "Both must always be backoff"
      ],
      answer: 1,
      explanation: "Recovery vs required human judgment. Do not make people click through timeouts, and do not retry a policy-forbidden refund."
    },
    {
      id: "sys-exc-disc-2",
      pattern: "exception-handling",
      also: ["goal-setting"],
      kind: "discriminate",
      stem: "Quality is slowly getting worse with no exception thrown. Is that exception handling?",
      choices: [
        "Yes — any bad output is an exception",
        "No — that is monitoring/goals (or later, evaluation); exceptions are failure classification and recovery",
        "Yes — backoff the whole week",
        "No — it is only A2A"
      ],
      answer: 1,
      explanation: "Crashes vs drift. Slow quality belongs with goals/evaluation, not retry loops."
    },
    {
      id: "sys-exc-compose-1",
      pattern: "exception-handling",
      kind: "compose",
      stem: "Tool call fails, backoff exhausted, fallback is ‘ask a human.’ Which stack?",
      choices: [
        "Exception handling owns retry/fallback; HITL is the last fallback",
        "RAG owns retries",
        "A2A forbids fallbacks",
        "Goals replace catch blocks"
      ],
      answer: 0,
      explanation: "The video lists human-in-the-loop among backup options after classify/retry. HITL is not a substitute for backoff on blips."
    },
    {
      id: "sys-hitl-identify-1",
      pattern: "human-in-the-loop",
      kind: "identify",
      stem: "At a high-risk or low-confidence point the agent pauses, a person approves/edits/denies/takes over, then the workflow resumes. Which pattern?",
      choices: [
        "Exception handling and recovery",
        "Human-in-the-loop",
        "Goal setting and monitoring",
        "Inter-agent communication"
      ],
      answer: 1,
      explanation: "Pause → human action → resume. Exceptions can run without a person. A2A is agent-to-agent messages."
    },
    {
      id: "sys-hitl-when-1",
      pattern: "human-in-the-loop",
      kind: "when",
      stem: "A browser agent needs the user to type credentials. Which pattern?",
      choices: [
        "RAG — retrieve a password from the handbook",
        "Human-in-the-loop — take over, then return control",
        "A2A — another agent types the password",
        "Goal setting — a KPI named ‘logged in’"
      ],
      answer: 1,
      explanation: "Transcript: ChatGPT-style agent mode asks you to intervene. Do not retrieve secrets from a corpus as a substitute."
    },
    {
      id: "sys-hitl-when-2",
      pattern: "human-in-the-loop",
      kind: "when",
      stem: "When is HITL the wrong default for every token?",
      choices: [
        "Medical advice that must be signed off",
        "A high-volume FAQ the policy already allows the model to answer",
        "Large financial approvals",
        "Legal documents that require an attorney"
      ],
      answer: 1,
      explanation: "HITL costs latency, money, and 24/7 coverage. Use it where stakes, regulation, or edges demand it — not on every FAQ."
    },
    {
      id: "sys-hitl-tradeoff-1",
      pattern: "human-in-the-loop",
      kind: "tradeoff",
      stem: "Reviewers take ten minutes and disagree with each other. What did you add?",
      choices: [
        "Zero extra latency by definition",
        "Throughput limits, wait time, and inconsistent human decisions",
        "Automatic RAG citations",
        "Permanent vs temporary error classes"
      ],
      answer: 1,
      explanation: "Docs cons: scalability, cost, latency, inconsistency, fatigue. Error classes are exception handling."
    },
    {
      id: "sys-hitl-disc-1",
      pattern: "human-in-the-loop",
      also: ["exception-handling"],
      kind: "discriminate",
      stem: "The model is confident and the API is healthy, but refunds over $50 are forbidden without a person. That gate is which pattern?",
      choices: [
        "Exception handling — $50 is a timeout",
        "Human-in-the-loop — policy pause, not a crash",
        "A2A — message the refund tool",
        "RAG — chunk the refund policy and skip the human"
      ],
      answer: 1,
      explanation: "Nothing failed; policy requires oversight. RAG can inform the agent but does not sign the approval."
    },
    {
      id: "sys-hitl-disc-2",
      pattern: "human-in-the-loop",
      also: ["a2a"],
      kind: "discriminate",
      stem: "Two agents arguing is not a human gate. What is A2A vs HITL?",
      choices: [
        "They are the same if messages exist",
        "A2A is structured agent messages; HITL inserts a person at a decision point",
        "HITL is only for email between agents",
        "A2A requires a human on every envelope"
      ],
      answer: 1,
      explanation: "Transcript even says HITL can unstick an A2A loop — that is composition, not identity."
    },
    {
      id: "sys-hitl-compose-1",
      pattern: "human-in-the-loop",
      kind: "compose",
      stem: "Low-confidence route, then a person, then resume. Which System ideas combine?",
      choices: [
        "HITL as the unclear-case path; exceptions still wrap the tools after resume",
        "Only A2A",
        "RAG forbids humans",
        "Goals mean no pauses"
      ],
      answer: 0,
      explanation: "Unsure → human. After resume, tool failures still need recovery. Patterns stack."
    },
    {
      id: "sys-rag-identify-1",
      pattern: "knowledge-retrieval",
      kind: "identify",
      stem: "Parse, chunk, embed, retrieve top-k (optionally rewrite/rerank), generate a grounded answer with citations. Which pattern?",
      choices: [
        "Goal setting and monitoring",
        "Exception handling and recovery",
        "Knowledge retrieval (RAG)",
        "Inter-agent communication"
      ],
      answer: 2,
      explanation: "Librarian / vector match. The video treats this as familiar RAG. A2A is messaging, not a corpus index."
    },
    {
      id: "sys-rag-when-1",
      pattern: "knowledge-retrieval",
      kind: "when",
      stem: "Answers must cite the current policy handbook, which changes monthly. Which pattern?",
      choices: [
        "HITL — a human recites the handbook each time",
        "Knowledge retrieval — update the corpus instead of baking it into the prompt",
        "A2A — agents gossip the old policy",
        "Exception handling — retry until the model remembers"
      ],
      answer: 1,
      explanation: "Docs: large/dynamic corpora, citations, less fabrication. HITL does not scale as a search engine. Retry will not create sources."
    },
    {
      id: "sys-rag-when-2",
      pattern: "knowledge-retrieval",
      kind: "when",
      stem: "When should you not crank k to 50 ‘for safety’?",
      choices: [
        "When you want more hallucination surface from extra weakly related chunks",
        "When a small k already grounds the answer",
        "When citations are required and you already have the right passages",
        "When the corpus is tiny and precise"
      ],
      answer: 0,
      explanation: "Transcript: more matches give the model more to hallucinate from. Tune chunking and k; more is not safer."
    },
    {
      id: "sys-rag-tradeoff-1",
      pattern: "knowledge-retrieval",
      kind: "tradeoff",
      stem: "What infrastructure tax does RAG add?",
      choices: [
        "None — retrieval is free",
        "Index/embeddings, chunking quality, latency, and maintenance as the corpus grows",
        "Mandatory HITL on every chunk",
        "A2A expiry on each vector"
      ],
      answer: 1,
      explanation: "Docs cons: vector store, processing, retrieval quality, latency, upkeep."
    },
    {
      id: "sys-rag-disc-1",
      pattern: "knowledge-retrieval",
      kind: "discriminate",
      stem: "You retrieve handbook paragraphs. That is not the same as remembering this customer’s last ticket. Why?",
      choices: [
        "They are identical stores",
        "RAG is an external corpus with citations; customer history is session/episodic state (a different pattern family)",
        "RAG requires A2A",
        "Customer history must be top-k 50"
      ],
      answer: 1,
      explanation: "Grounding in documents vs continuity of a person. System bank’s RAG vs the Advanced memory idea — here the distractor is ‘treat them as the same,’ which is wrong."
    },
    {
      id: "sys-rag-disc-2",
      pattern: "knowledge-retrieval",
      also: ["exception-handling"],
      kind: "discriminate",
      stem: "Retrieval returns nothing useful. Is the first move infinite tool-retry?",
      choices: [
        "Yes — exceptions always retry the embedder forever",
        "No — tune retrieve/rewrite/k; use exception handling for actual index/API failures, not ‘empty but healthy’ search",
        "Yes — HITL must paste Wikipedia",
        "No — switch to A2A peer mesh"
      ],
      answer: 1,
      explanation: "Empty search is a retrieval-quality problem. Exceptions are for outages and timeouts of the index service."
    },
    {
      id: "sys-rag-compose-1",
      pattern: "knowledge-retrieval",
      kind: "compose",
      stem: "Cited draft, then a human for medical advice. Which stack?",
      choices: [
        "RAG for grounding; HITL because the domain is high-stakes",
        "A2A only",
        "Goals only",
        "Exceptions only"
      ],
      answer: 0,
      explanation: "Sources plus a physician sign-off. Neither layer replaces the other."
    },
    {
      id: "sys-a2a-identify-1",
      pattern: "a2a",
      kind: "identify",
      stem: "Agents talk through structured messages with IDs, expiry, auth, and conflict rules. Topologies: coordinator, peers, or a shared board. Cap loops and drop stale messages. Which pattern?",
      choices: [
        "Goal setting and monitoring",
        "Knowledge retrieval (RAG)",
        "Inter-agent communication (A2A)",
        "Exception handling and recovery"
      ],
      answer: 2,
      explanation: "Office email with read receipts and spam filters. RAG is documents. Exceptions are failures of calls, not the envelope format."
    },
    {
      id: "sys-a2a-when-1",
      pattern: "a2a",
      kind: "when",
      stem: "The video’s advice for most teams considering a full peer ‘democracy’ of agents is:",
      choices: [
        "Always ship it — it is the easiest production pattern",
        "Prefer simpler designs; full A2A meshes are complex and rarely seen done well",
        "Replace all tools with messages",
        "Use A2A instead of any human gate"
      ],
      answer: 1,
      explanation: "Transcript: looks beautiful, often a bad production system unless you have serious engineering. Docs: prefer simpler unless you have dedicated work."
    },
    {
      id: "sys-a2a-when-2",
      pattern: "a2a",
      kind: "when",
      stem: "When is A2A actually warranted?",
      choices: [
        "A single agent with one tool",
        "Distributed/composable agents that must pass typed, expiring, authenticated messages",
        "Any time you retrieve a PDF",
        "Any KPI dashboard"
      ],
      answer: 1,
      explanation: "Docs: complex multi-agent workflows, modular distributed agents. Not RAG and not goals."
    },
    {
      id: "sys-a2a-tradeoff-1",
      pattern: "a2a",
      kind: "tradeoff",
      stem: "What is the one pro the video wants you to remember if you do build this?",
      choices: [
        "It is cheaper than one agent",
        "Fault isolation and traceable messages — you can pin which agent caused the mess",
        "No debugging is required",
        "Context never grows"
      ],
      answer: 1,
      explanation: "Fault isolation vs a human org where blame is fuzzy. Cons still include protocol complexity, latency, and overloaded context."
    },
    {
      id: "sys-a2a-disc-1",
      pattern: "a2a",
      also: ["human-in-the-loop"],
      kind: "discriminate",
      stem: "Agents enter an endless reply-all. A2A’s own controls are TTL, loop caps, drop stale, maybe designate who may speak. When is HITL the extra move?",
      choices: [
        "Instead of TTL — never expire messages",
        "When those controls fail and a person must unstick or approve",
        "HITL is the name of the message bus",
        "Never; A2A forbids humans"
      ],
      answer: 1,
      explanation: "Protocol first, human as backstop. Do not skip expiry because a human exists."
    },
    {
      id: "sys-a2a-disc-2",
      pattern: "a2a",
      kind: "discriminate",
      stem: "A coordinator assigns work. Is that already A2A?",
      choices: [
        "Yes — any coordinator is A2A",
        "Not necessarily — A2A is the message protocol (ids, expiry, auth); a coordinator topology is one way to use it",
        "Yes — coordinators forbid messages",
        "No — A2A means only peer democracy"
      ],
      answer: 1,
      explanation: "The video lists boss / equals / shared board as communication topologies. The pattern is the envelope rules, not ‘having a manager’ alone."
    },
    {
      id: "sys-a2a-compose-1",
      pattern: "a2a",
      kind: "compose",
      stem: "Typed envelopes on a bus, plus emergency stop if a storm of errors starts. Which pair?",
      choices: [
        "A2A for messages; exception handling to stop/alert when communication itself fails",
        "Only RAG",
        "Goals delete messages",
        "HITL means no IDs on messages"
      ],
      answer: 0,
      explanation: "Stuck agents and storms need recovery, not more un-expiring mail."
    }
  ]
});
