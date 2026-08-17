window.QUIZ_BANKS = window.QUIZ_BANKS || [];
window.QUIZ_BANKS.push({
  id: "strategic-fundamentals",
  title: "Strategic patterns — pros, cons & when to use (20–21)",
  patterns: ["prioritization", "exploration"],
  questions: [
    {
      id: "fund-str-pri-identify",
      pattern: "prioritization",
      kind: "identify",
      stem: "Tasks are scored on value, risk, effort, urgency, and dependencies; the top-scored item is executed, then everything is re-scored because the first action can change what should happen next. Which pattern?",
      choices: [
        "Prioritization",
        "Exploration and discovery",
        "Freeze the list once and never reorder it",
        "Give every task equal depth of investigation before acting"
      ],
      answer: 0,
      explanation: "Triage-and-rescore based on value/risk/urgency/dependencies is prioritization. Exploration is broad search across a knowledge space, not a work queue. The other two options describe the opposite of prioritization's re-scoring behavior."
    },
    {
      id: "fund-str-pri-when",
      pattern: "prioritization",
      kind: "when",
      stem: "Which scenario best fits prioritization?",
      choices: [
        "A support queue with limited agents, SLA deadlines, and tickets that block other tickets",
        "Mapping an entirely new market with no known tasks yet",
        "A single task with no competitors for attention",
        "Reading every available paper on a topic before doing anything"
      ],
      answer: 0,
      explanation: "Limited capacity, competing goals, dependencies, and deadlines are prioritization's classic fit. Mapping an unknown market is exploration; a single uncontested task and reading everything up front don't need a triage/scoring formula."
    },
    {
      id: "fund-str-pri-exception",
      pattern: "prioritization",
      kind: "exception",
      stem: "When is a heavy priority-scoring formula the wrong tool?",
      choices: [
        "There is only one thing to do next, so there is no real competition between tasks to score",
        "Capacity is limited and several tasks compete for it",
        "Tasks have dependencies on each other",
        "Deadlines force tradeoffs between tasks"
      ],
      answer: 0,
      explanation: "Scoring only matters when tasks genuinely compete for limited capacity. With nothing to choose between, the formula is pure overhead. The other options are exactly the conditions prioritization is meant to handle."
    },
    {
      id: "fund-str-pri-tradeoff",
      pattern: "prioritization",
      kind: "tradeoff",
      stem: "What is a documented cost of prioritization?",
      choices: [
        "Scoring complexity, reorder overhead, and starvation of low-priority items if aging isn't applied",
        "It guarantees no task is ever delayed",
        "It removes the need for any scoring criteria",
        "It eliminates reordering overhead entirely"
      ],
      answer: 0,
      explanation: "Constant re-scoring and reordering has a real cost, and low-priority work can starve without an aging mechanism — the tradeoff for responsive triage. It does not guarantee zero delay or remove the need for scoring/reordering."
    },
    {
      id: "fund-str-pri-disc-1",
      pattern: "prioritization",
      also: ["exploration"],
      kind: "discriminate",
      stem: "A backlog of well-understood tickets is competing for a fixed number of agents, versus an unmapped market with unknown opportunities. Which one calls for prioritization?",
      choices: [
        "The backlog of well-understood tickets competing for agents",
        "The unmapped market with unknown opportunities",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "Triaging known, competing work against limited capacity is prioritization. An unmapped market with unknown opportunities calls for exploration and discovery instead, since there isn't yet a known list of tasks to score."
    },
    {
      id: "fund-str-pri-disc-2",
      pattern: "prioritization",
      also: ["exploration"],
      kind: "discriminate",
      stem: "A queue's top item changes because a new high-urgency ticket arrived and a dependency shifted. Is re-ranking the remaining queue prioritization, or exploration and discovery?",
      choices: [
        "Prioritization",
        "Exploration and discovery",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "Re-scoring a known queue after conditions change is prioritization's defining behavior. Exploration and discovery instead scores unknown leads for novelty, impact, and feasibility — it doesn't re-rank an existing backlog."
    },
    {
      id: "fund-str-exp-identify",
      pattern: "exploration",
      kind: "identify",
      stem: "A broad search is run across papers, data, and experts; themes are clustered; leads are scored on novelty, impact, gaps, and feasibility; the best ones are deep-dived; and insights plus next steps are synthesized. Which pattern?",
      choices: [
        "Exploration and discovery",
        "Prioritization",
        "Execute the single highest-scored task from a known backlog",
        "Skip synthesis and just report raw search results"
      ],
      answer: 0,
      explanation: "Broad search plus clustering plus novelty/impact/feasibility scoring plus deep-dive and synthesis is exploration and discovery. Prioritization triages a backlog of known competing tasks, not an unknown space. The other two options skip exploration's defining steps."
    },
    {
      id: "fund-str-exp-when",
      pattern: "exploration",
      kind: "when",
      stem: "Which scenario best fits exploration and discovery?",
      choices: [
        "Entering a new domain or market where the goal is to map what's worth pursuing before committing resources",
        "A support queue with known tickets competing for limited agents",
        "A single well-defined task with no ambiguity about what to do next",
        "A production system needing golden tests before deploy"
      ],
      answer: 0,
      explanation: "Exploration and discovery fits new domains, innovation, and mapping knowledge gaps. A support queue with known tickets is prioritization; a single well-defined task needs no mapping; golden tests before deploy is evaluation and monitoring."
    },
    {
      id: "fund-str-exp-exception",
      pattern: "exploration",
      kind: "exception",
      stem: "When is a full exploration and discovery effort the wrong investment?",
      choices: [
        "The problem space is already well understood, and the real question is just which known task to do next, not what exists to be found",
        "The team is entering a genuinely new domain",
        "The team wants to map knowledge gaps before committing resources",
        "The team is doing competitive or market analysis of an unfamiliar space"
      ],
      answer: 0,
      explanation: "Exploration earns its cost when there's an unknown space to map. If the space is already well understood, broad search and clustering just add slow, uncertain overhead. The other options describe exactly when exploration pays off."
    },
    {
      id: "fund-str-exp-tradeoff",
      pattern: "exploration",
      kind: "tradeoff",
      stem: "What is a documented cost of exploration and discovery?",
      choices: [
        "It's slow and compute-heavy, payoff is uncertain, scope can creep, and information overload makes it hard to decide where to focus",
        "It guarantees a valuable discovery every time",
        "It has no risk of scope creep",
        "It is faster than working a known backlog"
      ],
      answer: 0,
      explanation: "Broad search across an unknown space is inherently slow, uncertain, and prone to scope creep and information overload — the tradeoff for finding what's worth pursuing. It does not guarantee results or run faster than triaging a known backlog."
    },
    {
      id: "fund-str-exp-disc-1",
      pattern: "exploration",
      also: ["prioritization"],
      kind: "discriminate",
      stem: "Clustering themes across a hundred unread research papers to find promising gaps is exploration and discovery, or prioritization?",
      choices: [
        "Exploration and discovery",
        "Prioritization",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "Clustering unread material to find promising, unknown gaps is exploration and discovery. Prioritization would instead be scoring and ordering a set of already-known competing tasks, not searching for unknown leads."
    },
    {
      id: "fund-str-exp-disc-2",
      pattern: "exploration",
      also: ["prioritization"],
      kind: "discriminate",
      stem: "A team already has a clear, ranked backlog of known features to build. Is deciding which one to build next prioritization, or exploration and discovery?",
      choices: [
        "Prioritization",
        "Exploration and discovery",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "Choosing among already-known, competing items is prioritization. Exploration and discovery would apply if the team didn't yet know what the possible features or opportunities even were."
    },
    {
      id: "fund-str-pri-compose",
      pattern: "prioritization",
      also: ["exploration"],
      kind: "compose",
      stem: "After an exploration effort identifies a promising new opportunity, it gets added to a backlog and scored against existing work for what to do next. How should this be described?",
      choices: [
        "Exploration and discovery surfaces the candidate; prioritization decides where it lands relative to competing work — the two compose in sequence",
        "Only exploration matters once discovery happens, so prioritization is unnecessary here",
        "Prioritization replaces the need for any exploration",
        "Both patterns describe the exact same activity"
      ],
      answer: 0,
      explanation: "Patterns combine in sequence: exploration and discovery finds and scores unknown leads, and once a lead becomes a known candidate, prioritization decides how it ranks against other competing work."
    }
  ]
});
