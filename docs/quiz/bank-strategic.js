window.QUIZ_BANKS = window.QUIZ_BANKS || [];
window.QUIZ_BANKS.push({
  id: "strategic",
  title: "Strategic patterns (20–21)",
  patterns: ["prioritization", "exploration"],
  questions: [
    {
      id: "str-pri-identify-1",
      pattern: "prioritization",
      kind: "identify",
      stem: "Score tasks on value, risk, effort, urgency, and dependencies. Execute the top item, then re-score because the first action can change what should happen next (ER triage, not a static list). Which pattern?",
      choices: [
        "Prioritization",
        "Exploration and discovery",
        "Score once and freeze the list forever",
        "Explore every task to equal depth before acting"
      ],
      answer: 0,
      explanation: "Triage plus re-score. Exploration is broad search of a knowledge space, not a work queue. A frozen list denies the gym/traffic story."
    },
    {
      id: "str-pri-when-1",
      pattern: "prioritization",
      kind: "when",
      stem: "A support queue has limited agents, SLA clocks, and tickets that block other tickets. Which pattern?",
      choices: [
        "Exploration and discovery — read every knowledge paper first",
        "Prioritization — constrained capacity, dependencies, deadlines",
        "Treat all tickets as equally deep research",
        "Never re-score after the first close"
      ],
      answer: 1,
      explanation: "Docs: limited capacity, competing goals, dependencies, time-sensitive ops. Exploration is for mapping a new space, not draining a queue."
    },
    {
      id: "str-pri-when-2",
      pattern: "prioritization",
      kind: "when",
      stem: "When is a heavy priority formula the wrong tool?",
      choices: [
        "A real ER-style mix of urgent and blocking work",
        "A single sequential chore with no competitors for attention",
        "Manufacturing with changeovers",
        "DevOps with incident vs backlog"
      ],
      answer: 1,
      explanation: "If nothing competes, scoring overhead is ceremony. Use the pattern when the next action is actually a choice."
    },
    {
      id: "str-pri-tradeoff-1",
      pattern: "prioritization",
      kind: "tradeoff",
      stem: "Low-priority tickets never age and the scorer reshuffles every minute. What goes wrong?",
      choices: [
        "You invent too many hypotheses",
        "Starvation, context switching, and unstable scores",
        "The knowledge space is too broad",
        "Novelty scoring replaces urgency"
      ],
      answer: 1,
      explanation: "Docs: starvation, preemption overhead, subjective scores. Novelty/impact are exploration criteria, not the queue’s failure mode."
    },
    {
      id: "str-pri-disc-1",
      pattern: "prioritization",
      also: ["exploration"],
      kind: "discriminate",
      stem: "You went to the gym, traffic exploded, so you skip cooking and drive through on the way to work. Why is that prioritization rather than exploration?",
      choices: [
        "You searched academic papers about traffic",
        "The first action changed the environment, so you re-ranked remaining tasks",
        "You clustered themes in a knowledge map",
        "You scored novelty of restaurants"
      ],
      answer: 1,
      explanation: "Video: action one creates environment two; reassess. Exploration would be gathering clues about an unknown domain, not reordering today’s list."
    },
    {
      id: "str-pri-disc-2",
      pattern: "prioritization",
      also: ["exploration"],
      kind: "discriminate",
      stem: "A backlog of known tickets vs an unknown market you have not mapped. Which pairing?",
      choices: [
        "Both are exploration",
        "Known competing work: prioritization. Unknown space: exploration",
        "Both are a frozen FIFO list",
        "Unknown space is always prioritization because everything is a ticket"
      ],
      answer: 1,
      explanation: "Queue vs search. Calling every unknown a ticket without exploring first is how you prioritize the wrong work."
    },
    {
      id: "str-pri-compose-1",
      pattern: "prioritization",
      kind: "compose",
      stem: "After you close the top incident, several new blockers appear. What does the pattern demand?",
      choices: [
        "Continue the original printed order",
        "Re-score; do not assume the old #2 is still next",
        "Start a full literature review before any other incident",
        "Explore drug-discovery papers"
      ],
      answer: 1,
      explanation: "Re-score is the distinctive compose-with-itself loop. A literature review is exploration, not incident triage."
    },
    {
      id: "str-exp-identify-1",
      pattern: "exploration",
      kind: "identify",
      stem: "Start broad across papers, data, and experts; cluster themes; score novelty, impact, gaps, and feasibility; deep-dive the best leads; synthesize insights and next steps. Detective gathering clues. Which pattern?",
      choices: [
        "Prioritization",
        "Exploration and discovery",
        "Execute the current top ticket and stop",
        "Re-score a closed queue"
      ],
      answer: 1,
      explanation: "Research-agent shape (the video points at long ‘deep research’ runs). Prioritization ranks known work; it does not map an unknown space."
    },
    {
      id: "str-exp-when-1",
      pattern: "exploration",
      kind: "when",
      stem: "R&D wants to know which drug targets are even worth a lab week. Which pattern?",
      choices: [
        "Prioritization of a list you have not discovered yet",
        "Exploration and discovery — then maybe prioritize the surviving leads",
        "FIFO on random papers",
        "Triage as if the ER already has every patient named"
      ],
      answer: 1,
      explanation: "Docs: drug discovery, hypothesis-driven research, knowledge gaps. You cannot honestly prioritize an empty, unmapped set."
    },
    {
      id: "str-exp-when-2",
      pattern: "exploration",
      kind: "when",
      stem: "When should you not open a 40-minute multi-agent research expedition?",
      choices: [
        "A genuinely new domain with unclear leads",
        "A known ticket whose next action is already scored",
        "Competitive analysis you have never done",
        "Academic survey of a field you are entering"
      ],
      answer: 1,
      explanation: "Exploration is slow and expensive (docs). If the work is already a ranked queue item, do that pattern instead."
    },
    {
      id: "str-exp-tradeoff-1",
      pattern: "exploration",
      kind: "tradeoff",
      stem: "What are the characteristic cons?",
      choices: [
        "Starvation of low-priority tickets in a stable queue",
        "Time, compute, uncertain payoff, scope creep, information overload",
        "Re-scoring too often",
        "Aging policies that are too fair"
      ],
      answer: 1,
      explanation: "Exploration cons are search costs and focus. Starvation/aging are prioritization cons."
    },
    {
      id: "str-exp-disc-1",
      pattern: "exploration",
      also: ["prioritization"],
      kind: "discriminate",
      stem: "You cluster themes and pick where to deep-dive using a novelty score. Why is that not the ER triage formula (value × urgency / effort)?",
      choices: [
        "It is the same formula with new names",
        "Exploration selects what is worth investigating in an unknown map; triage ranks known work waiting on limited capacity",
        "Novelty is always urgency",
        "Deep-dives are always the next SLA ticket"
      ],
      answer: 1,
      explanation: "Different scoring objects: knowledge leads vs operational tasks. Mixing them is how research eats the incident queue (or vice versa)."
    },
    {
      id: "str-exp-disc-2",
      pattern: "exploration",
      also: ["prioritization"],
      kind: "discriminate",
      stem: "Deep research runs for 40 minutes spinning many searchers, then recommends next steps. After that report, you have five concrete projects and two engineers. What pattern takes over?",
      choices: [
        "More exploration until the universe is fully clustered",
        "Prioritization — limited capacity on a now-known set",
        "Exploration forever because reports are not work",
        "Never re-score those five projects"
      ],
      answer: 1,
      explanation: "Explore until the space is mapped enough; then triage what to staff. That handoff is the Strategic bank."
    },
    {
      id: "str-exp-compose-1",
      pattern: "exploration",
      kind: "compose",
      stem: "Cluster → score leads → deep-dive → a short list. How do the two Strategic patterns meet?",
      choices: [
        "They cannot meet",
        "Exploration produces candidates; prioritization (and re-score as results land) decides the order of pursuit",
        "Prioritization forbids using a novelty score at any stage",
        "Exploration requires you to execute all leads in parallel equally"
      ],
      answer: 1,
      explanation: "Search then rank. Equal-depth execution of every lead is how exploration’s resource con gets worse."
    }
  ]
});
