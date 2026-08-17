window.QUIZ_BANKS = window.QUIZ_BANKS || [];
window.QUIZ_BANKS.push({
  id: "core-fundamentals",
  title: "Core patterns — pros, cons & when to use (1–5)",
  patterns: ["prompt-chaining", "routing", "parallelization", "reflection", "tool-use"],
  questions: [
    {
      id: "fund-core-chain-identify",
      pattern: "prompt-chaining",
      kind: "identify",
      stem: "A task is broken into ordered steps where each step's output must pass a validation check before the next step begins, and results are merged and logged at the end. Which pattern is this?",
      choices: [
        "Prompt chaining — sequential steps with validated handoffs",
        "Routing — classify then send to one specialist",
        "Parallelization — split into independent chunks run at once",
        "Reflection — draft then critique until it passes"
      ],
      answer: 0,
      explanation: "Ordered steps with validated handoffs between them is chaining. Routing forks by intent rather than staging one pipeline. Parallelization needs chunks that don't depend on each other. Reflection is a draft/critique loop on one artifact, not staged handoffs."
    },
    {
      id: "fund-core-chain-when",
      pattern: "prompt-chaining",
      kind: "when",
      stem: "You're deciding whether to model a task as a prompt chain. Which situation best fits?",
      choices: [
        "A complex, multi-step transformation where each stage can fail independently and should be validated before the next runs",
        "A single short question with one obvious answer",
        "Ten unrelated documents that can each be summarized in any order",
        "A request that just needs a live lookup from an external system"
      ],
      answer: 0,
      explanation: "Chaining is for multi-step, quality-critical handoffs. A one-shot FAQ doesn't need staged validation (over-engineering). Independent documents are parallelization. A live lookup is tool use."
    },
    {
      id: "fund-core-chain-exception",
      pattern: "prompt-chaining",
      kind: "exception",
      stem: "Which of these is a good reason to shorten or avoid a prompt chain, even though the task is technically multi-step?",
      choices: [
        "The chain has grown to dozens of steps, so full context keeps getting re-passed forward and cost/latency balloon while early mistakes ride along",
        "The task has more than one step",
        "A human should never see intermediate output",
        "The steps must run in the same order every time"
      ],
      answer: 0,
      explanation: "Long chains are a documented failure mode: context explosion, accumulating latency/cost, and early errors propagating downstream — a reason to keep chains short (often 3–5 steps), not evidence that chaining itself is wrong. Having more than one step, hidden intermediates, or a fixed order are not by themselves problems."
    },
    {
      id: "fund-core-chain-tradeoff",
      pattern: "prompt-chaining",
      kind: "tradeoff",
      stem: "What is a commonly cited downside of prompt chaining, even when it is used correctly?",
      choices: [
        "Latency and cost accumulate across stages, and an early-stage error can propagate to later stages",
        "It cannot be debugged stage by stage",
        "It never produces reusable segments",
        "It requires no validation between steps"
      ],
      answer: 0,
      explanation: "Chaining trades speed/cost for modularity: each added stage adds latency and cost, and mistakes made early can poison downstream steps. The other options describe chaining's actual strengths (per-stage debugging, reusable segments, validated handoffs), not its weaknesses."
    },
    {
      id: "fund-core-chain-disc-parallel",
      pattern: "prompt-chaining",
      also: ["parallelization"],
      kind: "discriminate",
      stem: "Stage 2 needs the validated output of stage 1 before it can run at all. Why is this chaining rather than parallelization?",
      choices: [
        "Parallelization requires exactly one worker",
        "Parallelization splits independent work that doesn't wait on a sibling task; a dependent handoff is inherently sequential",
        "Chaining never has more than one stage",
        "Parallelization is only for scraping"
      ],
      answer: 1,
      explanation: "The defining trait of parallelization is independence between chunks so they can run concurrently. A hard dependency between stage 1 and stage 2 removes that independence, so it's a chain."
    },
    {
      id: "fund-core-chain-disc-routing",
      pattern: "prompt-chaining",
      also: ["routing"],
      kind: "discriminate",
      stem: "Every request goes through the same fixed sequence of steps (extract, draft, check) regardless of what the request is about. Why is this chaining rather than routing?",
      choices: [
        "Routing forks requests to different specialists based on classified intent; a single fixed path applied to everyone is a pipeline, not a fork",
        "Chaining can only have two steps",
        "Routing never uses confidence thresholds",
        "A fixed path is always routing"
      ],
      answer: 0,
      explanation: "Routing's defining move is classifying intent and branching to different handlers (with a clarify/fallback path when unsure). A single sequential path applied uniformly to every request is chaining, not routing."
    },
    {
      id: "fund-core-chain-compose",
      pattern: "prompt-chaining",
      also: ["tool-use"],
      kind: "compose",
      stem: "A workflow chains summarize → draft → policy-check, and the policy-check stage calls a live compliance-lookup function. How should you describe this?",
      choices: [
        "Chaining is the backbone (staged, validated handoffs); the compliance lookup inside one stage is tool use, not a separate top-level pattern",
        "The lookup call turns the whole workflow into tool use and the chain no longer matters",
        "The chain is invalid because a step calls an external function",
        "Routing must wrap this or the lookup is not allowed"
      ],
      answer: 0,
      explanation: "Patterns compose: a chain can contain a tool call inside one of its stages without ceasing to be a chain overall. A tool call inside a stage doesn't erase the staged/validated structure, nor does it require a routing wrapper."
    },
    {
      id: "fund-core-route-identify",
      pattern: "routing",
      kind: "identify",
      stem: "Incoming requests are first classified by intent, then handed to one of several specialist handlers; when the classifier's confidence is low, the system asks a clarifying question instead of guessing. Which pattern?",
      choices: ["Routing", "Prompt chaining", "Parallelization", "Reflection"],
      answer: 0,
      explanation: "Classify then branch to a specialist, with a clarify/fallback path for low confidence, is routing's signature. Chaining runs one fixed pipeline for everyone. Parallelization fans out to many workers at once rather than picking one. Reflection critiques a single draft."
    },
    {
      id: "fund-core-route-when",
      pattern: "routing",
      kind: "when",
      stem: "Which scenario is the clearest fit for routing?",
      choices: [
        "A multi-domain support line where billing, tech, and sales questions each need a different specialist and different tools",
        "A single-purpose calculator that only ever does one type of computation",
        "A batch of ten independent files each needing the same summary",
        "A single draft that needs to be polished against a rubric"
      ],
      answer: 0,
      explanation: "Routing shines in multi-domain systems needing specialized handlers and tool access. A single-purpose calculator has nothing to route between. Independent files fit parallelization. Polishing one draft is reflection."
    },
    {
      id: "fund-core-route-exception",
      pattern: "routing",
      kind: "exception",
      stem: "When is adding a routing/classification layer the wrong move?",
      choices: [
        "When there is effectively only one type of request, so the classifier adds latency and a bottleneck with nothing to differentiate",
        "When requests come from more than one department",
        "When you want specialized handlers per domain",
        "When low-confidence cases should be clarified rather than guessed"
      ],
      answer: 0,
      explanation: "If every request needs the same handling, a router just adds a decision point (and a potential bottleneck or misrouting risk) with no benefit. The other options describe exactly when routing helps."
    },
    {
      id: "fund-core-route-tradeoff",
      pattern: "routing",
      kind: "tradeoff",
      stem: "What is a well-known cost of a routing layer?",
      choices: [
        "The router itself can become a bottleneck, and misclassified requests get sent to the wrong specialist",
        "It cannot support more than one route",
        "It removes the need for any specialist logic",
        "It guarantees zero latency overhead"
      ],
      answer: 0,
      explanation: "Centralizing the routing decision creates a single point that must scale, and a wrong classification sends work down the wrong path — both are documented cons. Routing is meant to add routes easily, not forbid them."
    },
    {
      id: "fund-core-route-disc-parallel",
      pattern: "routing",
      also: ["parallelization"],
      kind: "discriminate",
      stem: "A request is classified and sent to exactly one specialist team. Why is this routing rather than parallelization?",
      choices: [
        "Parallelization fans the same job out to multiple concurrent workers; routing picks a single path for one request",
        "Routing always uses more workers than parallelization",
        "Parallelization also requires a classifier step first",
        "Routing cannot use confidence scores"
      ],
      answer: 0,
      explanation: "Routing is a fork to one handler based on intent. Parallelization is running several workers on independent chunks of the same job at once. Sending one request to exactly one specialist is routing's shape."
    },
    {
      id: "fund-core-route-disc-chain",
      pattern: "routing",
      also: ["prompt-chaining"],
      kind: "discriminate",
      stem: "System A always runs extract → draft → policy-check in that order for every ticket. System B first decides whether the ticket is billing, tech, or sales, then hands it to a different handler for each. Which system demonstrates routing?",
      choices: [
        "System A, because it has multiple steps",
        "System B, because it forks handling based on classified intent",
        "Both, because they both process tickets",
        "Neither, because routing requires a live tool call"
      ],
      answer: 1,
      explanation: "System B classifies and branches — that's routing. System A is a fixed sequential pipeline for everyone — that's chaining, regardless of step count."
    },
    {
      id: "fund-core-parallel-identify",
      pattern: "parallelization",
      kind: "identify",
      stem: "A large batch of independent files must each be processed by their own worker at the same time, and the outputs are later normalized, merged, and tagged with which worker produced which part. Which pattern?",
      choices: ["Parallelization", "Prompt chaining", "Routing", "Reflection"],
      answer: 0,
      explanation: "Concurrent independent workers plus a merge/provenance step is parallelization's signature. Chaining is sequential and dependent. Routing sends one request to one specialist. Reflection loops a single draft through critique."
    },
    {
      id: "fund-core-parallel-when",
      pattern: "parallelization",
      kind: "when",
      stem: "Which task is the best fit for parallelization?",
      choices: [
        "Summarizing 500 unrelated documents where each summary doesn't depend on any other",
        "A workflow where step two must validate step one's output before proceeding",
        "A single request that must be classified before handling",
        "A single draft that needs iterative polishing"
      ],
      answer: 0,
      explanation: "Independent, large-scale, time-sensitive work is the classic parallelization fit. A dependent step-two-needs-step-one workflow is chaining. Single-request classification is routing. Iterative polishing of one draft is reflection."
    },
    {
      id: "fund-core-parallel-exception",
      pattern: "parallelization",
      kind: "exception",
      stem: "When should you avoid splitting work into parallel workers even though there appears to be a lot of it?",
      choices: [
        "When each unit of work actually depends on the output of another unit, so there is nothing genuinely independent to run concurrently",
        "When there are more than ten items to process",
        "When the items come from different sources",
        "When the results need to be merged afterward"
      ],
      answer: 0,
      explanation: "Parallelization requires real independence between chunks. If everything depends on a prior result, forcing concurrency doesn't help and coordination/merge overhead just adds cost. Item count, mixed sources, and needing a merge step are normal, not disqualifying."
    },
    {
      id: "fund-core-parallel-tradeoff",
      pattern: "parallelization",
      kind: "tradeoff",
      stem: "What is a documented downside of parallelization?",
      choices: [
        "Coordination and merge complexity, rate limits, and multiplied cost/memory across workers",
        "It cannot scale workers up or down",
        "It provides no fault isolation between workers",
        "It is always slower than doing the same work sequentially"
      ],
      answer: 0,
      explanation: "Running many workers concurrently adds coordination/merge work, can hit rate limits, and multiplies memory and API cost — the classic tradeoff for the speed gain. Parallelization is prized for scaling workers and isolating faults, and it's typically faster than sequential execution, not slower."
    },
    {
      id: "fund-core-parallel-disc-chain",
      pattern: "parallelization",
      also: ["prompt-chaining"],
      kind: "discriminate",
      stem: "Two workers each independently scrape a different website and neither needs the other's output before starting. Why is this parallelization rather than chaining?",
      choices: [
        "Chaining requires validated sequential handoffs; independent tasks with no handoff between them can run concurrently instead",
        "Chaining never involves more than one worker",
        "Parallelization always requires a router first",
        "Chaining is faster whenever more than one task exists"
      ],
      answer: 0,
      explanation: "The absence of a dependency (no task waits on another's validated output) is exactly what allows concurrent execution — that's parallelization's condition, not chaining's."
    },
    {
      id: "fund-core-parallel-disc-route",
      pattern: "parallelization",
      also: ["routing"],
      kind: "discriminate",
      stem: "A single incoming request is fanned out so that three different workers each analyze it from a different angle at the same time, then the results are merged. Why is this parallelization rather than routing?",
      choices: [
        "Routing sends a request to exactly one specialist based on intent; running several workers on the same request concurrently and merging their output is parallelization",
        "Routing always runs faster than parallelization",
        "Parallelization cannot merge results",
        "Routing requires independent workers"
      ],
      answer: 0,
      explanation: "Routing forks to a single handler. Fanning one request out to multiple concurrent workers and merging their outputs is parallelization's shape, even though only one request came in."
    },
    {
      id: "fund-core-reflect-identify",
      pattern: "reflection",
      kind: "identify",
      stem: "A first draft is produced, then a separate critic step scores it against a rubric or tests; the draft is revised and re-scored until it passes or a maximum number of retries is hit. Which pattern?",
      choices: ["Reflection", "Tool use", "Routing", "Parallelization"],
      answer: 0,
      explanation: "Draft → critic → revise-until-passing (with a hard stop) is reflection's loop. Tool use calls an external system for data or action. Routing picks a specialist. Parallelization runs independent concurrent workers."
    },
    {
      id: "fund-core-reflect-when",
      pattern: "reflection",
      kind: "when",
      stem: "Which situation calls for a reflection (draft-then-critique) loop?",
      choices: [
        "A piece of creative or compliance-sensitive writing where quality must clear a bar before it ships",
        "A one-line factual lookup with a single correct answer",
        "A batch of independent files that can each be summarized once",
        "A request that only needs a live database read"
      ],
      answer: 0,
      explanation: "Reflection is for quality-critical, error-prone, or creative output that benefits from a critique-and-revise cycle. A single factual lookup doesn't need iterative polishing; independent files fit parallelization; a live read is tool use."
    },
    {
      id: "fund-core-reflect-exception",
      pattern: "reflection",
      kind: "exception",
      stem: "When should a reflection loop be stopped even though the output could theoretically be improved further?",
      choices: [
        "When additional critique passes show diminishing returns, or a maximum retry count is reached, since more looping mainly adds latency/cost and risks flattening the author's voice",
        "As soon as the first draft exists, no matter its quality",
        "Never — a hard retry cap should not be used",
        "Whenever a critic disagrees even slightly with the draft, however minor"
      ],
      answer: 0,
      explanation: "Reflection's documented failure mode is over-optimization: diminishing returns, extra API cost/latency, and a flattened voice — so stopping after diminishing returns (or hitting a retry cap) is the right call, not looping forever."
    },
    {
      id: "fund-core-reflect-tradeoff",
      pattern: "reflection",
      kind: "tradeoff",
      stem: "What is a well-known cost of adding a reflection loop?",
      choices: [
        "Extra latency and cost per revision cycle, with diminishing quality gains and a risk of over-optimizing the output",
        "It guarantees the first draft is already correct",
        "It removes the need for any rubric or scoring criteria",
        "It cannot be capped at a maximum number of retries"
      ],
      answer: 0,
      explanation: "Each critique-revise cycle costs tokens and time, gains shrink over iterations, and pushing too far can over-polish the work — the classic reflection tradeoff. It requires a rubric/criteria and is normally capped by a max-retry limit."
    },
    {
      id: "fund-core-reflect-disc-tool",
      pattern: "reflection",
      also: ["tool-use"],
      kind: "discriminate",
      stem: "A system re-reads its own draft, compares it to a rubric, and rewrites the weak parts. Why is this reflection rather than tool use?",
      choices: [
        "Tool use calls an external system for data or action; reflection critiques and revises an artifact the model already produced, with no outside call needed",
        "Tool use always requires a rubric",
        "Reflection cannot use a scoring rubric",
        "Tool use and reflection are the same pattern"
      ],
      answer: 0,
      explanation: "Reflection's loop stays internal to the artifact (draft, critique, revise). Tool use is defined by reaching out to an external system for data or an action — that's a different move entirely."
    },
    {
      id: "fund-core-reflect-disc-chain",
      pattern: "reflection",
      also: ["prompt-chaining"],
      kind: "discriminate",
      stem: "System A revises the same paragraph three times based on a critic's score. System B moves a document through three distinct stages (extract, draft, policy-check), each doing different work. Which one is reflection?",
      choices: [
        "System A, because it loops critique and revision over one evolving artifact",
        "System B, because it has three steps",
        "Both, because both have multiple passes",
        "Neither, because reflection requires a live API call"
      ],
      answer: 0,
      explanation: "Reflection is a loop over one artifact between a generator and a critic. System B's three distinct, forward-only stages describe chaining instead — different work per step rather than a critique loop."
    },
    {
      id: "fund-core-tool-identify",
      pattern: "tool-use",
      kind: "identify",
      stem: "The agent needs data that only exists outside the model (like a live order status), so it discovers an available function, checks permissions, calls it with the right parameters, and parses the result — falling back if the call fails. Which pattern?",
      choices: ["Tool use", "Reflection", "Routing", "Prompt chaining"],
      answer: 0,
      explanation: "Discover → authorize → call → parse → fallback for an external data/action need is tool use (function calling). Reflection is an internal critique loop. Routing picks a specialist. Chaining is a fixed sequential pipeline."
    },
    {
      id: "fund-core-tool-when",
      pattern: "tool-use",
      kind: "when",
      stem: "When is tool use the right choice?",
      choices: [
        "The agent needs real-time external data, precise computation, or to take a concrete action a language model can't do on its own",
        "The task is a purely creative rewrite of existing text with no outside facts needed",
        "Independent chunks of text must be summarized concurrently",
        "A request just needs to be classified into one of three categories"
      ],
      answer: 0,
      explanation: "Tool use is for reaching outside the model: live data, system integration, exact computation, or real actions. A pure rewrite, independent-chunk summarization, and simple classification don't need an external call."
    },
    {
      id: "fund-core-tool-exception",
      pattern: "tool-use",
      kind: "exception",
      stem: "When should you avoid adding a tool call to a workflow?",
      choices: [
        "When the task can be answered from the model's own reasoning with no need for live data, external action, or exact computation — adding a call only adds latency, dependency, and credential risk for no benefit",
        "Whenever the answer must be numerically precise",
        "Whenever the underlying data changes over time",
        "Whenever a real-world action needs to be taken"
      ],
      answer: 0,
      explanation: "If nothing external is actually needed, a tool call adds risk (credentials, failure modes, latency) without benefit. The other options are exactly the situations where tool use is warranted, not where it should be skipped."
    },
    {
      id: "fund-core-tool-tradeoff",
      pattern: "tool-use",
      kind: "tradeoff",
      stem: "What is a specific risk of tool use beyond added latency?",
      choices: [
        "Security/credential exposure, and a call that 'succeeds' but returns the wrong result can quietly poison every later step",
        "It can never fail, so no fallback is required",
        "It removes the need to check permissions before calling",
        "It guarantees deterministic output regardless of the tool"
      ],
      answer: 0,
      explanation: "Granting an agent access to real systems introduces credential/security exposure, and a technically-successful-but-wrong call can silently corrupt downstream reasoning — a distinctly worse failure mode than a clean error. Tool use still requires permission checks and fallback handling."
    },
    {
      id: "fund-core-tool-disc-route",
      pattern: "tool-use",
      also: ["routing"],
      kind: "discriminate",
      stem: "The agent calls a get_order_status function with specific parameters and parses a structured result. Why is this tool use rather than routing?",
      choices: [
        "Routing picks which specialist handler should own an incoming request; calling a specific function to fetch or act on external data is tool use, even if it happens inside a routed flow",
        "Routing always involves calling an external API",
        "Tool use never has parameters",
        "Routing and tool use always occur together"
      ],
      answer: 0,
      explanation: "Routing is about choosing a handler for a request. Invoking a concrete function with parameters to get external data or perform an action is tool use — a step that can happen inside any pattern, including a routed one."
    },
    {
      id: "fund-core-tool-disc-reflect",
      pattern: "tool-use",
      also: ["reflection"],
      kind: "discriminate",
      stem: "After a draft is produced, the system calls a live pricing API to verify a number instead of asking a critic to re-read the draft. Why is this tool use rather than reflection?",
      choices: [
        "Reflection improves an artifact via internal critique and revision; fetching ground truth from an external system is tool use, regardless of when in the flow it happens",
        "Reflection always calls external APIs to check facts",
        "Tool use requires a rubric to grade the draft",
        "Both patterns are identical whenever a draft already exists"
      ],
      answer: 0,
      explanation: "Reflection's loop is generate → critique → revise using the model's own judgment. Reaching out to an external, authoritative source for ground truth is tool use's defining move."
    }
  ]
});
