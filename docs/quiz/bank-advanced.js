window.QUIZ_BANKS = window.QUIZ_BANKS || [];
window.QUIZ_BANKS.push({
  id: "advanced",
  title: "Advanced patterns (6–10)",
  patterns: ["planning", "multi-agent", "memory-management", "learning", "mcp"],
  questions: [
    {
      id: "adv-plan-identify-1",
      pattern: "planning",
      kind: "identify",
      stem: "You decompose a goal into milestones, build a dependency graph, check time/budget constraints, assign agents and tools, execute, and replan at checkpoints if the world changes. Which pattern?",
      choices: [
        "Planning",
        "Multi-agent collaboration",
        "Memory management",
        "Learning and adaptation"
      ],
      answer: 0,
      explanation: "ASCII: milestones, dependency graph, allocate under constraints, monitor and replan. Multi-agent is specialists under a coordinator. Memory stores context. Learning updates prompts from feedback."
    },
    {
      id: "adv-plan-when-1",
      pattern: "planning",
      kind: "when",
      stem: "A migration has schema design blocking scripts, a deadline, and a rollback path if a load fails. Which pattern owns that?",
      choices: [
        "Memory management — store the schema in long-term memory and stop",
        "Planning — dependencies, constraints, execute, replan on blockage",
        "MCP — any graph of work is a protocol",
        "Learning — A/B the migration after it fails in production"
      ],
      answer: 1,
      explanation: "Docs: multi-step projects with dependencies and uncertain environments. Memory does not schedule. MCP standardizes tool access. Learning is for improving future behavior from feedback, not this run’s DAG."
    },
    {
      id: "adv-plan-when-2",
      pattern: "planning",
      kind: "when",
      stem: "When is planning the wrong default?",
      choices: [
        "Long-running work with blockers you expect to hit",
        "A three-stage transform that always runs extract → validate → load",
        "A project whose milestones depend on each other",
        "You must replan when a tool is down"
      ],
      answer: 1,
      explanation: "The transcript: planning is like a road trip with checkpoints — not merely forwarding each stage’s output. A fixed short pipeline is a sequential handoff (a design move from Core chaining), and over-planning adds freeze and latency."
    },
    {
      id: "adv-plan-tradeoff-1",
      pattern: "planning",
      kind: "tradeoff",
      stem: "You spend as long planning as executing, then freeze the graph even when a dependency dies. What did you buy?",
      choices: [
        "Better long-term memories",
        "Upfront latency plus rigidity; you skipped adaptive replanning",
        "MCP versioning for free",
        "A distilled lessons block from user ratings"
      ],
      answer: 1,
      explanation: "Planning cons: overhead, rigidity, prediction error, replanning cost. The pattern includes checkpoints — a frozen graph is a misuse. Memory, MCP, and learning are other Advanced patterns."
    },
    {
      id: "adv-plan-disc-1",
      pattern: "planning",
      also: ["multi-agent"],
      kind: "discriminate",
      stem: "You have one goal graph and may assign steps to agents, but the distinctive artifact is the DAG plus replan. How is that not ‘just multi-agent’?",
      choices: [
        "Multi-agent forbids tools",
        "Multi-agent’s center is specialist roles and shared work; planning’s center is milestones, dependencies, and adapting the plan",
        "Planning forbids more than one agent",
        "They are identical if a coordinator exists"
      ],
      answer: 1,
      explanation: "You can plan with one agent. Multi-agent is division of labor under a coordinator (film crew). Planning can *use* agents without being that pattern."
    },
    {
      id: "adv-plan-disc-2",
      pattern: "planning",
      kind: "discriminate",
      stem: "The video contrast: you are ‘not necessarily carrying over the output of the previous one to the next one’; you walk a step list toward a goal and replan. That contrast is with which design move?",
      choices: [
        "A fixed assembly line that validates and forwards each stage’s output",
        "Storing episodic memories of each step",
        "Fine-tuning weights after the trip",
        "Publishing a standard tool protocol"
      ],
      answer: 0,
      explanation: "Spoken planning vs sequential handoff: execute steps toward a goal, track progress, replan — not ‘output of stage n is the only input to n+1.’ Memory, learning, and MCP are different jobs."
    },
    {
      id: "adv-plan-compose-1",
      pattern: "planning",
      kind: "compose",
      stem: "A planner assigns research vs analysis specialists and stores the current graph in working memory. Which statement is true?",
      choices: [
        "MCP must replace the planner",
        "Planning can sit above multi-agent assignment; memory can hold plan state",
        "Learning is required before any graph is allowed",
        "If specialists exist you must delete the DAG"
      ],
      answer: 1,
      explanation: "Advanced patterns stack: plan the work, optionally staff it with specialists, remember where you are. MCP is how tools are discovered, not a substitute for a goal graph."
    },
    {
      id: "adv-ma-identify-1",
      pattern: "multi-agent",
      kind: "identify",
      stem: "A director coordinates camera, sound, and lighting on one script. Specialists share artifacts and acceptance criteria; there is a max retry if the cut fails. Which pattern?",
      choices: [
        "Planning",
        "Multi-agent collaboration",
        "Memory management",
        "MCP"
      ],
      answer: 1,
      explanation: "Film-crew analogy from the video. Planning is the itinerary. Memory is how they share context, not the collaboration pattern itself. MCP is a standard for tools/resources, not the crew."
    },
    {
      id: "adv-ma-when-1",
      pattern: "multi-agent",
      kind: "when",
      stem: "A content pipeline needs research, writing, and editing as different expertise, possibly in parallel workstreams. Which pattern?",
      choices: [
        "Learning and adaptation — wait for CSAT then rewrite the org chart",
        "Multi-agent collaboration — specialist roles plus a coordinator",
        "MCP — protocols replace editors",
        "Memory management — one agent with a bigger context window is enough"
      ],
      answer: 1,
      explanation: "Docs: multi-faceted problems, parallel workstreams, specialized knowledge. A bigger window is not specialization. MCP does not write copy. Learning improves future behavior, it does not staff this job."
    },
    {
      id: "adv-ma-when-2",
      pattern: "multi-agent",
      kind: "when",
      stem: "When should you not reach for a seven-agent mesh?",
      choices: [
        "When several domains must work the same ticket",
        "When one specialist path with a simple coordinator (or none) already meets the bar",
        "When you need iterative refinement from multiple perspectives",
        "When failure of one role should not kill the whole production"
      ],
      answer: 1,
      explanation: "The video mocks giant graphs. Coordination cost, extra spend, and debugging across agents are the cons. Start smaller; add specialists when the work is actually multi-faceted."
    },
    {
      id: "adv-ma-tradeoff-1",
      pattern: "multi-agent",
      kind: "tradeoff",
      stem: "Specialists disagree and shared notes drift. What did you take on?",
      choices: [
        "Only token-limit issues inside one context window",
        "Coordination, conflict, and state-sync cost — the ‘HR for agents’ problem",
        "Prompt poisoning from a fake cockroach review",
        "Need for a wire protocol before any role exists"
      ],
      answer: 1,
      explanation: "Transcript: more employees need more management. Learning’s cockroach story is poisoned feedback. MCP is optional infrastructure under tools, not the first diagnosis."
    },
    {
      id: "adv-ma-disc-1",
      pattern: "multi-agent",
      also: ["mcp"],
      kind: "discriminate",
      stem: "You have a coordinator and three specialists. You do not yet have a standard for discovering tools across vendors. What is missing vs what you already have?",
      choices: [
        "You already have MCP; you still need multi-agent",
        "You have multi-agent collaboration; MCP would standardize tool/resource access under them",
        "Memory management is the missing protocol",
        "Learning replaces both"
      ],
      answer: 1,
      explanation: "Multi-agent is who does the work. MCP is a universal interface for tools/data (docs: discoverability, auth, versioning). You can collaborate with hardcoded tools; MCP is the integration layer when that does not scale."
    },
    {
      id: "adv-ma-disc-2",
      pattern: "multi-agent",
      also: ["memory-management"],
      kind: "discriminate",
      stem: "The crew shares a script and timeline. Is ‘shared memory’ the pattern name for the whole design?",
      choices: [
        "Yes — shared memory is multi-agent",
        "No — shared memory is a supporting store; multi-agent is roles, coordinator, and acceptance criteria",
        "Yes — without a vector index there are no agents",
        "No — shared memory is always MCP"
      ],
      answer: 1,
      explanation: "The video says shared memory must be well structured so memories do not overlap. That is memory management inside a multi-agent system, not the definition of collaboration."
    },
    {
      id: "adv-ma-compose-1",
      pattern: "multi-agent",
      kind: "compose",
      stem: "Coordinator assigns tickets; specialists write notes; a writer sees only the board. Which Advanced pieces are in play?",
      choices: [
        "Only MCP",
        "Multi-agent structure, with memory as the shared board; planning if the ticket graph has dependencies",
        "Only learning, because notes exist",
        "Memory forbids a writer agent"
      ],
      answer: 1,
      explanation: "Roles + coordinator = multi-agent. The board is memory. A dependency-aware ticket order is planning. Notes are not automatically a learn-from-feedback loop."
    },
    {
      id: "adv-mem-identify-1",
      pattern: "memory-management",
      kind: "identify",
      stem: "Classify information as short-term (session), episodic (events), or long-term knowledge; store recency/relevance; retrieve without overflowing the window. Which pattern?",
      choices: [
        "Planning",
        "Multi-agent collaboration",
        "Memory management",
        "Learning and adaptation"
      ],
      answer: 2,
      explanation: "That taxonomy is memory management. Learning updates prompts/policies from feedback. Multi-agent is roles. Planning is a goal graph."
    },
    {
      id: "adv-mem-when-1",
      pattern: "memory-management",
      kind: "when",
      stem: "A tutor should remember that the student failed concept A so later lessons over-explain the A-dependent parts of B. Which pattern?",
      choices: [
        "MCP",
        "Planning a new curriculum DAG every turn with no store",
        "Memory management — continuity and personalization across turns",
        "Multi-agent — spawn a new tutor per sentence"
      ],
      answer: 2,
      explanation: "Video: educational assistants that keep weaknesses. That is stored context, not a protocol and not a new agent per utterance."
    },
    {
      id: "adv-mem-when-2",
      pattern: "memory-management",
      kind: "when",
      stem: "When is memory management the wrong diagnosis?",
      choices: [
        "Multi-turn support that must not re-ask the order number",
        "You want the *agent’s policy* to improve from ratings, not to recall this customer’s facts",
        "A personal assistant that should know preferred stores",
        "A project bot that must keep milestone state"
      ],
      answer: 1,
      explanation: "Customer facts vs agent behavior: memory vs learning. The other options are memory fits (continuity, personalization, workflow state)."
    },
    {
      id: "adv-mem-tradeoff-1",
      pattern: "memory-management",
      kind: "tradeoff",
      stem: "You persist everything forever, including stale and sensitive items. What goes wrong?",
      choices: [
        "The coordinator cannot assign tickets",
        "Privacy risk, retrieval noise, and stale memories — flush/score recency instead of hoarding",
        "MCP cannot version tools",
        "A/B tests become illegal"
      ],
      answer: 1,
      explanation: "Docs/transcript: privacy, context limits, over-storing, need a rule for when a memory is old. That is not a coordinator or MCP failure."
    },
    {
      id: "adv-mem-disc-1",
      pattern: "memory-management",
      also: ["learning"],
      kind: "discriminate",
      stem: "After a session you still know this user’s address, but you did not change how you write any future user’s refunds. What did you do?",
      choices: [
        "Learning and adaptation",
        "Memory management",
        "Planning",
        "MCP"
      ],
      answer: 1,
      explanation: "Address is a fact about this user (memory). Changing refund wording from feedback is learning. Do not mix the two stores."
    },
    {
      id: "adv-mem-disc-2",
      pattern: "memory-management",
      kind: "discriminate",
      stem: "The context window is full. Memory management’s move is to compress or evict with metadata — not which of these?",
      choices: [
        "Drop low-recency session chatter",
        "Fine-tune a new model on the full chat log as the default next step",
        "Index remaining items with topic tags for later retrieve",
        "Keep long-term facts and compress the rest"
      ],
      answer: 1,
      explanation: "Transcript: if the window is full, compress; fine-tuning is a rare learning option, not the memory pattern’s first move."
    },
    {
      id: "adv-mem-compose-1",
      pattern: "memory-management",
      kind: "compose",
      stem: "Specialists share a notes board tagged by recency. Which pairing is accurate?",
      choices: [
        "Memory is illegal inside multi-agent systems",
        "Multi-agent needs a memory design so notes do not collide",
        "MCP stores all memories by definition",
        "Learning deletes memory on every turn"
      ],
      answer: 1,
      explanation: "Video: shared memory must be structured. MCP may expose a memory *server*, but the pattern of classifying/retrieving is still memory management."
    },
    {
      id: "adv-learn-identify-1",
      pattern: "learning",
      kind: "identify",
      stem: "Collect corrections and ratings, clean noise, update prompts/policies/examples (rarely weights), then A/B whether it helped. Which pattern?",
      choices: [
        "Memory management",
        "Learning and adaptation",
        "Planning",
        "Multi-agent collaboration"
      ],
      answer: 1,
      explanation: "Recipe analogy in the video: adjust from taste tests. Memory stores; it does not run that improvement loop."
    },
    {
      id: "adv-learn-when-1",
      pattern: "learning",
      kind: "when",
      stem: "Supervisors keep correcting the same refund phrasing. You want fewer repeats next week. Which pattern?",
      choices: [
        "Planning a new milestone named ‘sound nicer’",
        "Learning and adaptation — distill lessons into the prompt and compare",
        "MCP so tools discover the phrasing",
        "Multi-agent — add a fourth specialist who only says sorry"
      ],
      answer: 1,
      explanation: "Error reduction from feedback is learning. A milestone does not update policy. Extra agents without a feedback loop still repeat the mistake."
    },
    {
      id: "adv-learn-when-2",
      pattern: "learning",
      kind: "when",
      stem: "A review claims the restaurant is full of cockroaches; it is not. What must learning do before updating the prompt?",
      choices: [
        "Always trust every rating so the loop is fast",
        "Clean/validate: drop malicious or policy-violating feedback so you do not learn the wrong lesson",
        "Store the review as long-term memory and stop",
        "Replan the seating DAG"
      ],
      answer: 1,
      explanation: "Transcript: denoise, log, do not let the system warn every diner about fictional pests. That clean step is part of learning, not planning."
    },
    {
      id: "adv-learn-tradeoff-1",
      pattern: "learning",
      kind: "tradeoff",
      stem: "You let a model rewrite the system prompt after every thumbs-down. What combinatorial problem appears?",
      choices: [
        "Dependency graphs cannot have cycles",
        "Training/update cost, regressions, and possible poisoning",
        "Tool registries cannot list more than two functions",
        "Short-term memory becomes impossible"
      ],
      answer: 1,
      explanation: "Docs: feedback quality, cost, regressions, poisoning, drift. Unbounded prompt rewrites are how you buy all of those."
    },
    {
      id: "adv-learn-disc-1",
      pattern: "learning",
      also: ["memory-management"],
      kind: "discriminate",
      stem: "You remember order #4411 for this chat. Separately, you add a lesson ‘never invent ship dates.’ Which is which?",
      choices: [
        "Both are learning",
        "Order id is memory; the rule for future tickets is learning",
        "Both are MCP resources",
        "The rule is planning; the id is multi-agent"
      ],
      answer: 1,
      explanation: "Facts about this case vs behavior change for later cases. That split is the Advanced bank’s most important fork."
    },
    {
      id: "adv-learn-disc-2",
      pattern: "learning",
      also: ["planning"],
      kind: "discriminate",
      stem: "A/B on a held-out email after distilling lessons is learning. Replanning a blocked DAG mid-task is what instead?",
      choices: [
        "Still learning — any change is learning",
        "Planning’s adaptive execution, not a feedback-distill-evaluate loop",
        "MCP handshake",
        "Memory eviction"
      ],
      answer: 1,
      explanation: "Replan is in-task adaptation of the graph. Learning is across-task improvement from outcomes, with an A/B. Do not name every change ‘learning.’"
    },
    {
      id: "adv-learn-compose-1",
      pattern: "learning",
      kind: "compose",
      stem: "You drop POLICY-violating corrections, distill a short lessons block, keep episodic memories of this customer separate. What did you combine?",
      choices: [
        "MCP and planning only",
        "Learning (clean → distill → A/B) with memory for customer facts, without mixing them",
        "Multi-agent because two stores exist",
        "Planning because A/B is a milestone"
      ],
      answer: 1,
      explanation: "Clean/distill is learning. Customer facts stay in memory. Two stores do not equal two agents."
    },
    {
      id: "adv-mcp-identify-1",
      pattern: "mcp",
      kind: "identify",
      stem: "You want one protocol so agents can discover tools, data, and services with consistent auth, versioning, and observability instead of one-off integrations. The video skipped this. Which pattern?",
      choices: [
        "Multi-agent collaboration",
        "Memory management",
        "Model Context Protocol",
        "Learning and adaptation"
      ],
      answer: 2,
      explanation: "MCP is the 21st pattern in the docs: universal interface, dynamic discovery, built-in auth. The walkthrough omitted it as already widely covered. Multi-agent is roles, not the wire standard."
    },
    {
      id: "adv-mcp-when-1",
      pattern: "mcp",
      kind: "when",
      stem: "When do the docs say to invest in MCP rather than hardcoded tool lists?",
      choices: [
        "A demo with three stable fake tools and one agent",
        "Enterprise-scale, many changing resources, access control, interoperability across systems",
        "Whenever you store a user preference",
        "Whenever two agents share notes"
      ],
      answer: 1,
      explanation: "When-to-use: enterprise, multi-tool, standardization, security, dynamic resources, interoperability. A tiny hardcoded demo does not need the protocol overhead."
    },
    {
      id: "adv-mcp-when-2",
      pattern: "mcp",
      kind: "when",
      stem: "When is MCP the wrong first move?",
      choices: [
        "You must authorize tools the same way for many agents",
        "You have one agent and a frozen list of three functions",
        "Vendors expose incompatible tool APIs you must wrap once",
        "Resources appear and disappear at runtime"
      ],
      answer: 1,
      explanation: "Cons: upfront protocol work, extra latency, learning curve. Hardcoded tools are fine until discovery/auth/versioning actually hurt."
    },
    {
      id: "adv-mcp-tradeoff-1",
      pattern: "mcp",
      kind: "tradeoff",
      stem: "What do you pay for the ‘write once, use across agents’ benefit?",
      choices: [
        "Nothing — MCP is only a slogan",
        "Abstraction, migration of existing tools, and ecosystem/support needs",
        "You must delete multi-agent designs",
        "You can no longer store memories"
      ],
      answer: 1,
      explanation: "Docs cons: implementation overhead, extra layer, migration, vendor support. It does not outlaw collaboration or memory."
    },
    {
      id: "adv-mcp-disc-1",
      pattern: "mcp",
      also: ["multi-agent"],
      kind: "discriminate",
      stem: "Five specialists call tools. Is that already MCP?",
      choices: [
        "Yes — more than one agent implies MCP",
        "No — that is multi-agent (and ordinary tool use); MCP is a standard for discovery/auth/versioning of those tools",
        "Yes — shared notes are MCP",
        "No — MCP is a synonym for learning"
      ],
      answer: 1,
      explanation: "Collaboration ≠ protocol. You can have a crew with baked-in function calls. MCP is how the crew finds and is allowed to use resources consistently."
    },
    {
      id: "adv-mcp-disc-2",
      pattern: "mcp",
      kind: "discriminate",
      stem: "An agent already ‘uses tools’ (discover in a prompt, call, parse). What extra problem is MCP for?",
      choices: [
        "Critiquing the prose of the tool result",
        "Replacing one-off integrations with a shared contract for resources across agents and vendors",
        "Building the milestone DAG",
        "A/B testing refund wording"
      ],
      answer: 1,
      explanation: "Tool use (Core) is the call loop. MCP is the integration layer under that loop when lists, auth, and versions must be standard. The other choices are reflection-like, planning, and learning."
    },
    {
      id: "adv-mcp-compose-1",
      pattern: "mcp",
      kind: "compose",
      stem: "Coordinator’s specialists must only see tools they are authorized for, listed at runtime. Which stack?",
      choices: [
        "Learning only",
        "Multi-agent for roles, MCP for discover/authorize, memory optional for shared notes",
        "Planning forbids runtime discovery",
        "MCP replaces the coordinator"
      ],
      answer: 1,
      explanation: "MCP sits under tool use in multi-agent setups. It does not remove the need for a coordinator or for memory of the ticket."
    }
  ]
});
