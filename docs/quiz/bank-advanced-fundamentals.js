window.QUIZ_BANKS = window.QUIZ_BANKS || [];
window.QUIZ_BANKS.push({
  id: "advanced-fundamentals",
  title: "Advanced patterns — pros, cons & when to use (6–10)",
  patterns: ["planning", "multi-agent", "memory-management", "learning", "mcp"],
  questions: [
    {
      id: "fund-adv-plan-identify",
      pattern: "planning",
      kind: "identify",
      stem: "A goal is broken into milestones with a dependency graph; constraints are checked, agents/tools are assigned, and progress is tracked while the plan is revised if the environment changes. Which pattern?",
      choices: [
        "Planning",
        "Prompt chaining",
        "Multi-agent collaboration",
        "Memory management"
      ],
      answer: 0,
      explanation: "Building a dependency graph toward a goal and replanning when things change is planning's signature. Chaining is a fixed forward sequence with no goal graph. Multi-agent is about dividing labor among specialized agents, not building the graph itself. Memory management is about storing/retrieving information over time."
    },
    {
      id: "fund-adv-plan-when",
      pattern: "planning",
      kind: "when",
      stem: "Which task best fits planning?",
      choices: [
        "A multi-step project with dependencies between milestones, uncertain conditions, and a need to replan if things change",
        "A single fixed three-step pipeline with no branching",
        "One agent answering a single one-off question",
        "Storing a user's stated preferences across sessions"
      ],
      answer: 0,
      explanation: "Planning fits goal-oriented, dependency-heavy, uncertain, long-running work. A fixed three-step pipeline is chaining. A one-off answer needs no goal graph. Storing preferences over time is memory management."
    },
    {
      id: "fund-adv-plan-exception",
      pattern: "planning",
      kind: "exception",
      stem: "When is elaborate upfront planning the wrong call, even for work that looks project-like?",
      choices: [
        "When the task is small and linear with no real dependencies, or the environment is so volatile that any plan would be stale before it's used",
        "When there are dependencies between milestones",
        "When resources need to be allocated across steps",
        "When the environment might change and replanning is possible"
      ],
      answer: 0,
      explanation: "Planning's documented downsides include upfront latency and over-planning freezing flexibility; in a small/linear task or an extremely volatile environment, that cost buys little. The other options describe exactly when planning helps, not when to skip it."
    },
    {
      id: "fund-adv-plan-tradeoff",
      pattern: "planning",
      kind: "tradeoff",
      stem: "What is a documented cost of planning?",
      choices: [
        "Upfront planning latency, over-planning that freezes flexibility, and replanning cost when predictions miss",
        "It removes the need for any agents or tools to execute the plan",
        "It guarantees the environment will never change",
        "It has no coordination overhead"
      ],
      answer: 0,
      explanation: "Planning trades some latency and rigidity for strategic, dependency-aware execution — prediction errors and replanning are real costs. It does not remove the need for execution, guarantee a static environment, or avoid coordination overhead."
    },
    {
      id: "fund-adv-plan-disc-multiagent",
      pattern: "planning",
      also: ["multi-agent"],
      kind: "discriminate",
      stem: "One agent builds and tracks its own milestone dependency graph and reassigns its own tool calls as conditions change; no other agents are involved. Why is this planning rather than multi-agent collaboration?",
      choices: [
        "Multi-agent collaboration requires several distinct agents dividing the work; a single agent's dependency graph and replanning is planning regardless of complexity",
        "Planning always requires at least two agents",
        "Multi-agent collaboration never uses a dependency graph",
        "A single agent can never replan"
      ],
      answer: 0,
      explanation: "Multi-agent collaboration's defining trait is dividing a task across distinct specialized agents. A single agent managing its own goal graph and replanning is planning, even if the plan is elaborate."
    },
    {
      id: "fund-adv-plan-disc-chain",
      pattern: "planning",
      also: ["prompt-chaining"],
      kind: "discriminate",
      stem: "One workflow tracks milestones and re-derives the remaining steps after a delay changes the environment. Another workflow always runs the same three steps in order no matter what happens. Which one is planning?",
      choices: [
        "The one that tracks milestones and replans after a change",
        "The one with a fixed three-step order",
        "Both, because both have more than one step",
        "Neither, without a live tool call"
      ],
      answer: 0,
      explanation: "Replanning in response to a changed environment is planning's defining behavior. A fixed sequence that never adapts is chaining, regardless of step count."
    },
    {
      id: "fund-adv-multiagent-identify",
      pattern: "multi-agent",
      kind: "identify",
      stem: "Several specialized agents each own a distinct part of a complex task under a coordinator, sharing structured memory and artifacts toward common acceptance criteria. Which pattern?",
      choices: [
        "Multi-agent collaboration",
        "Planning",
        "Learning and adaptation",
        "Model Context Protocol"
      ],
      answer: 0,
      explanation: "Division of labor across distinct specialized agents under a coordinator is multi-agent collaboration's signature. Planning is one agent's own goal graph. Learning is about improving from feedback over time. MCP standardizes tool/data access, not the org chart of agents."
    },
    {
      id: "fund-adv-multiagent-when",
      pattern: "multi-agent",
      kind: "when",
      stem: "Which scenario best fits multi-agent collaboration?",
      choices: [
        "A problem with genuinely distinct sub-domains (say, legal, financial, and technical review) that benefit from separate expert agents working in parallel",
        "A single simple task with no distinct expertise required",
        "Storing what a user asked for across several past sessions",
        "Standardizing how tools are discovered and authorized across an organization"
      ],
      answer: 0,
      explanation: "Multi-agent collaboration fits multi-faceted problems needing specialized knowledge and parallel workstreams. A single simple task needs no division of labor; storing past requests is memory management; standardizing tool access is MCP."
    },
    {
      id: "fund-adv-multiagent-exception",
      pattern: "multi-agent",
      kind: "exception",
      stem: "When is spinning up multiple collaborating agents the wrong choice?",
      choices: [
        "When one agent could handle the whole task alone; the coordination and shared-context overhead then outweighs any benefit",
        "When the task has genuinely distinct expertise needs",
        "When parallel workstreams would speed things up",
        "When robustness matters if one part of the work fails"
      ],
      answer: 0,
      explanation: "If a single agent suffices, adding coordinators and shared context just adds cost and complexity without gain. The other options describe exactly when multi-agent collaboration pays off."
    },
    {
      id: "fund-adv-multiagent-tradeoff",
      pattern: "multi-agent",
      kind: "tradeoff",
      stem: "What is a documented cost of multi-agent collaboration?",
      choices: [
        "Coordination and shared-context overhead, more API spend, and harder cross-agent debugging",
        "It guarantees lower total cost than a single agent",
        "It removes the need for any coordinator",
        "It eliminates state-synchronization issues between agents"
      ],
      answer: 0,
      explanation: "Splitting work across agents adds real coordination cost, spend, and debugging difficulty — the tradeoff for specialization and parallelism. It does not guarantee lower cost, remove the coordinator role, or eliminate sync issues."
    },
    {
      id: "fund-adv-multiagent-disc-mcp",
      pattern: "multi-agent",
      also: ["mcp"],
      kind: "discriminate",
      stem: "Team A standardizes how every agent discovers and authenticates against tools and services, regardless of who calls them. Team B has several distinct expert agents dividing a single task under a coordinator. Which team's setup is multi-agent collaboration?",
      choices: [
        "Team B, because distinct expert agents are dividing the task",
        "Team A, because it involves agents",
        "Both, because both involve more than one agent",
        "Neither, without a shared memory store"
      ],
      answer: 0,
      explanation: "Team B's org chart of specialized agents dividing a task is multi-agent collaboration. Team A's standardized discovery/auth layer is MCP — the integration layer, not the division of labor."
    },
    {
      id: "fund-adv-multiagent-disc-learning",
      pattern: "multi-agent",
      also: ["learning"],
      kind: "discriminate",
      stem: "A task routes different parts of the work to a legal-expert agent and a finance-expert agent, each contributing their piece to a shared result. Why is this multi-agent collaboration rather than learning and adaptation?",
      choices: [
        "Learning and adaptation updates a system's behavior over time from feedback; dividing a task among distinct expert roles right now is multi-agent collaboration",
        "Learning and adaptation always involves more than one agent",
        "Multi-agent collaboration requires an A/B test before it counts",
        "Both patterns describe the same thing whenever more than one role is involved"
      ],
      answer: 0,
      explanation: "Learning and adaptation is about improving a system's policy or prompts from outcomes over time. Assigning distinct expert roles to a current task is the division-of-labor move that defines multi-agent collaboration."
    },
    {
      id: "fund-adv-memory-identify",
      pattern: "memory-management",
      kind: "identify",
      stem: "Information is classified as short-term, episodic, or long-term, stored with recency/relevance metadata, and retrieved or updated without overflowing the context window. Which pattern?",
      choices: [
        "Memory management",
        "Learning and adaptation",
        "Planning",
        "Multi-agent collaboration"
      ],
      answer: 0,
      explanation: "Classifying, storing, and retrieving state across turns is memory management. Learning changes behavior/policy from feedback, not just storing facts. Planning tracks a milestone graph. Multi-agent collaboration divides labor among agents."
    },
    {
      id: "fund-adv-memory-when",
      pattern: "memory-management",
      kind: "when",
      stem: "Which scenario is the best fit for memory management?",
      choices: [
        "A multi-turn assistant that must recall a user's prior preferences and past conversation context without re-asking every time",
        "A single one-off question with no follow-up expected",
        "A single agent's milestone dependency tracking for one project",
        "Several agents dividing a task under a coordinator"
      ],
      answer: 0,
      explanation: "Memory management fits conversational continuity, personalization, and multi-turn state. A single one-off question needs no persistence; milestone tracking is planning; dividing a task is multi-agent collaboration."
    },
    {
      id: "fund-adv-memory-exception",
      pattern: "memory-management",
      kind: "exception",
      stem: "When does adding a memory layer stop paying for itself?",
      choices: [
        "When interactions are all single-turn and stateless, so there's nothing worth persisting between them",
        "When a user's preferences should be recalled across sessions",
        "When personalization depends on prior context",
        "When multi-step state needs to survive across turns"
      ],
      answer: 0,
      explanation: "If nothing carries over between interactions, storing and retrieving memory adds overhead with no payoff. The other options describe exactly the use cases memory management targets."
    },
    {
      id: "fund-adv-memory-tradeoff",
      pattern: "memory-management",
      kind: "tradeoff",
      stem: "What is a documented cost of memory management?",
      choices: [
        "Storage and privacy concerns, retrieval quality issues, stale memories, and context-window limits",
        "It guarantees perfect recall forever with no storage cost",
        "It removes any privacy considerations",
        "It cannot be personalized to a specific user"
      ],
      answer: 0,
      explanation: "Persisting state introduces storage/privacy exposure, retrieval-quality risk, staleness, and window limits — the tradeoff for continuity and personalization. It does not guarantee perfect, cost-free recall or eliminate privacy concerns."
    },
    {
      id: "fund-adv-memory-disc-learning",
      pattern: "memory-management",
      also: ["learning"],
      kind: "discriminate",
      stem: "The system recalls that a user prefers metric units from a past session and reuses that fact, without changing any underlying prompts or policy. Why is this memory management rather than learning and adaptation?",
      choices: [
        "Nothing about the system's behavior or policy changed from feedback; a fact was simply stored and retrieved, which is memory rather than learning",
        "Learning and adaptation never touches user preferences",
        "Memory management always requires an A/B test",
        "Both patterns describe the same behavior whenever a preference is involved"
      ],
      answer: 0,
      explanation: "Learning and adaptation updates prompts, policy, or examples based on aggregated feedback. Recalling a previously stored fact without changing behavior elsewhere is memory management's simpler job."
    },
    {
      id: "fund-adv-memory-disc-plan",
      pattern: "memory-management",
      also: ["planning"],
      kind: "discriminate",
      stem: "Which of these is memory management: tracking a project's milestone dependency graph, or storing what a user asked for three sessions ago so it isn't asked again?",
      choices: [
        "Storing what the user asked for three sessions ago",
        "Tracking the milestone dependency graph",
        "Both are memory management",
        "Neither is memory management"
      ],
      answer: 0,
      explanation: "Recalling episodic facts across sessions is memory management. The milestone dependency graph belongs to planning and has nothing to do with episodic/long-term fact storage."
    },
    {
      id: "fund-adv-learning-identify",
      pattern: "learning",
      kind: "identify",
      stem: "Corrections, ratings, and outcomes are collected and cleaned, then used to update prompts, policies, examples, or (rarely) weights, followed by an A/B test to confirm the change helped. Which pattern?",
      choices: [
        "Learning and adaptation",
        "Memory management",
        "Multi-agent collaboration",
        "Model Context Protocol"
      ],
      answer: 0,
      explanation: "Closing the loop from feedback into updated prompts/policy plus validation is learning and adaptation. Memory management just stores/retrieves facts without changing policy. Multi-agent collaboration divides a task among agents. MCP standardizes tool access."
    },
    {
      id: "fund-adv-learning-when",
      pattern: "learning",
      kind: "when",
      stem: "Which scenario best fits learning and adaptation?",
      choices: [
        "A system whose performance should measurably improve over time as it collects corrections and feedback from real use",
        "A one-off transaction with no repeat interactions",
        "A stateless calculator that always computes the same way",
        "A protocol for how agents discover and call tools"
      ],
      answer: 0,
      explanation: "Learning and adaptation fits systems meant to improve with use via feedback loops. A one-off transaction, a stateless calculator, and a tool-discovery protocol don't involve updating behavior from outcomes."
    },
    {
      id: "fund-adv-learning-exception",
      pattern: "learning",
      kind: "exception",
      stem: "When is building a learning/feedback loop premature or risky?",
      choices: [
        "When feedback volume or quality is too low or noisy to trust, since a change trained on bad signal can regress behavior rather than improve it",
        "When there's abundant, well-labeled feedback validated by an A/B test",
        "When personalization from past outcomes is desired",
        "When error reduction over time is a goal"
      ],
      answer: 0,
      explanation: "Learning and adaptation's documented risk is being poisoned by noisy or insufficient feedback, causing regressions. The other options describe conditions where a learning loop is appropriate, not risky."
    },
    {
      id: "fund-adv-learning-tradeoff",
      pattern: "learning",
      kind: "tradeoff",
      stem: "What is a documented cost of learning and adaptation?",
      choices: [
        "Needing enough quality feedback, update/training cost, risk of regressions, and drift if user behavior shifts",
        "It guarantees improvement on every single update",
        "It needs no validation before deploying a change",
        "It has no risk of learning the wrong lesson from feedback"
      ],
      answer: 0,
      explanation: "Learning and adaptation depends on feedback quality and volume, costs something to retrain/update, and can regress or drift — that's the tradeoff for continuous improvement. It does not guarantee improvement or skip validation."
    },
    {
      id: "fund-adv-learning-disc-memory",
      pattern: "learning",
      also: ["memory-management"],
      kind: "discriminate",
      stem: "A system starts giving shorter answers to a specific user after that user repeatedly down-voted long answers, and the change is validated with an A/B test. Why is this learning and adaptation rather than memory management?",
      choices: [
        "The system's policy or behavior itself changed based on aggregated feedback and was validated, not just a stored fact being recalled",
        "Memory management always involves an A/B test",
        "Learning and adaptation never involves a specific user",
        "Both patterns are identical whenever a user's behavior is involved"
      ],
      answer: 0,
      explanation: "Memory management would simply recall a stored preference. Here the system's underlying behavior was updated from feedback and validated — that update-and-validate loop is learning and adaptation."
    },
    {
      id: "fund-adv-learning-disc-multiagent",
      pattern: "learning",
      also: ["multi-agent"],
      kind: "discriminate",
      stem: "A prompt template is revised after analyzing months of user corrections, and the new template is tested against the old one. Why is this learning and adaptation rather than multi-agent collaboration?",
      choices: [
        "No task is being divided among specialized agents here; a single system's policy is being updated from feedback data",
        "Multi-agent collaboration always requires an A/B test",
        "Learning and adaptation always involves more than one agent",
        "Both patterns describe the same activity whenever a prompt changes"
      ],
      answer: 0,
      explanation: "Multi-agent collaboration's defining move is dividing a task across distinct expert agents. Updating and testing a single system's prompt from feedback has no division of labor and is learning and adaptation."
    },
    {
      id: "fund-adv-mcp-identify",
      pattern: "mcp",
      kind: "identify",
      stem: "Agents discover and call tools, data, and services through one standardized protocol that also handles authentication, versioning, and observability, instead of building one-off integrations for each tool. Which pattern?",
      choices: [
        "Model Context Protocol",
        "Multi-agent collaboration",
        "Memory management",
        "Learning and adaptation"
      ],
      answer: 0,
      explanation: "Standardizing tool/data discovery, auth, and versioning across an ecosystem is MCP's role. Multi-agent collaboration divides a task among agents. Memory management stores/retrieves facts. Learning updates policy from feedback."
    },
    {
      id: "fund-adv-mcp-when",
      pattern: "mcp",
      kind: "when",
      stem: "Which scenario is the clearest fit for adopting a protocol like MCP?",
      choices: [
        "An enterprise with many external tools and resources needing consistent auth, versioning, and discovery across multiple agents and vendors",
        "A single team simply recalling a user's past preferences",
        "A single system updating its own prompt from user feedback",
        "One agent dividing a small, one-off job between two sub-agents"
      ],
      answer: 0,
      explanation: "MCP's value is largest with many tools/vendors needing a consistent interface, auth, and versioning. Recalling preferences is memory management; updating a prompt from feedback is learning; a small one-off division of labor is multi-agent collaboration at a scale too small to need a protocol."
    },
    {
      id: "fund-adv-mcp-exception",
      pattern: "mcp",
      kind: "exception",
      stem: "When is adopting a full protocol layer like MCP overkill?",
      choices: [
        "A small system with one or two hardcoded integrations that rarely change, where the protocol's abstraction, auth, and versioning overhead outweigh the benefit",
        "A system integrating with many vendors and changing resources",
        "A system where multiple agents need consistent authentication",
        "A system that must support discovery of new tools over time"
      ],
      answer: 0,
      explanation: "MCP pays off at scale, with many or changing integrations. For one or two fixed, hardcoded integrations, the protocol's setup and abstraction cost isn't justified. The other options are exactly where MCP earns its overhead."
    },
    {
      id: "fund-adv-mcp-tradeoff",
      pattern: "mcp",
      kind: "tradeoff",
      stem: "What is a documented cost of adopting a protocol layer like MCP?",
      choices: [
        "Upfront protocol work, extra abstraction and latency, a learning curve, and migration cost for existing tools",
        "It guarantees zero added latency",
        "It removes the need for authentication entirely",
        "It works without any ecosystem or tooling support"
      ],
      answer: 0,
      explanation: "Standardizing integrations costs setup time, adds an abstraction layer, and requires migrating existing one-off tools — the tradeoff for a universal, reusable interface. It does not eliminate latency, auth, or the need for ecosystem support."
    },
    {
      id: "fund-adv-mcp-disc-multiagent",
      pattern: "mcp",
      also: ["multi-agent"],
      kind: "discriminate",
      stem: "Team A standardizes how every agent discovers and authenticates against tools and services. Team B has distinct expert agents dividing a single task under a coordinator. Which team's setup is MCP?",
      choices: [
        "Team A, because it standardizes tool discovery and auth",
        "Team B, because it involves agents",
        "Both, because both involve agents calling something",
        "Neither, without a shared memory store"
      ],
      answer: 0,
      explanation: "Team A's standardized discovery/auth layer is MCP. Team B's org chart of specialized agents dividing a task is multi-agent collaboration, a different concern entirely."
    },
    {
      id: "fund-adv-mcp-disc-memory",
      pattern: "mcp",
      also: ["memory-management"],
      kind: "discriminate",
      stem: "Is a shared, versioned catalog that lets any agent discover and call approved external services best described as MCP or memory management?",
      choices: [
        "MCP",
        "Memory management",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "MCP standardizes tool/service discovery, auth, and versioning. Memory management is about storing conversational/episodic facts over time, not standardizing access to tools or services."
    },
    {
      id: "fund-adv-plan-compose",
      pattern: "planning",
      also: ["multi-agent"],
      kind: "compose",
      stem: "A coordinator agent builds a milestone dependency graph for a project and then assigns each milestone to a different specialized agent. How should you describe this?",
      choices: [
        "Planning provides the goal graph and replanning; multi-agent collaboration provides the specialized agents executing pieces of it — the two compose rather than compete",
        "Only one of the two patterns can apply at a time, so this is just memory management",
        "Multi-agent collaboration replaces the need for any plan",
        "Planning replaces the need for any specialized agents"
      ],
      answer: 0,
      explanation: "Patterns combine in real systems: a plan's dependency graph can be executed by several specialized agents, with planning owning the graph/replanning and multi-agent collaboration owning who does each piece."
    }
  ]
});
