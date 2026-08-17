window.QUIZ_BANKS = window.QUIZ_BANKS || [];
window.QUIZ_BANKS.push({
  id: "optimization-fundamentals",
  title: "Optimization patterns — pros, cons & when to use (16–19)",
  patterns: ["resource-aware", "reasoning", "guardrails", "evaluation"],
  questions: [
    {
      id: "fund-opt-res-identify",
      pattern: "resource-aware",
      kind: "identify",
      stem: "Task complexity is classified so simple work goes to a cheap/fast model and hard work goes to an expensive one; tokens, time, and spend are monitored; and the system falls back to cache, shorter context, or a cheaper model under pressure. Which pattern?",
      choices: [
        "Resource-aware optimization",
        "Reasoning techniques",
        "Guardrails / safety",
        "Evaluation and monitoring"
      ],
      answer: 0,
      explanation: "Routing by cost/difficulty and watching spend is resource-aware optimization. Reasoning techniques choose a thinking method (chain-of-thought, tree-of-thought) for accuracy, not cost. Guardrails check for harm/compliance. Evaluation sets quality gates and watches for regressions."
    },
    {
      id: "fund-opt-res-when",
      pattern: "resource-aware",
      kind: "when",
      stem: "Which scenario best fits resource-aware optimization?",
      choices: [
        "High-volume work with mixed easy and hard cases and a tight budget, where most requests don't need the most expensive model",
        "A complex multi-step logic puzzle needing careful step-by-step reasoning",
        "A public chatbot needing harm and PII checks before responding",
        "A production system needing golden tests before every deploy"
      ],
      answer: 0,
      explanation: "Resource-aware optimization fits cost-sensitive, variable-difficulty, high-volume work. A hard logic puzzle needing careful reasoning is reasoning techniques; harm/PII checks are guardrails; golden tests before deploy are evaluation and monitoring."
    },
    {
      id: "fund-opt-res-exception",
      pattern: "resource-aware",
      kind: "exception",
      stem: "When is resource-aware routing between cheap and expensive models not worth the effort?",
      choices: [
        "Low, steady volume where every request is roughly the same difficulty, so there's little cost variance to optimize",
        "High volume with a tight budget",
        "Variable difficulty across requests",
        "A multi-tenant system needing fairness in resource use"
      ],
      answer: 0,
      explanation: "The value of routing by cost comes from variance in volume and difficulty. With low, uniform-difficulty traffic, there's little to gain from tiering models. The other options are exactly where resource-aware optimization helps."
    },
    {
      id: "fund-opt-res-tradeoff",
      pattern: "resource-aware",
      kind: "tradeoff",
      stem: "What is a documented cost of resource-aware optimization?",
      choices: [
        "Routing overhead, quality that varies by which model handled a request, threshold tuning, and cache-coherency or uneven-latency issues",
        "It guarantees identical quality regardless of which model is chosen",
        "It removes the need for any threshold tuning",
        "It has no caching concerns at all"
      ],
      answer: 0,
      explanation: "Tiering models by cost/difficulty adds a routing decision, uneven quality across tiers, and cache/latency management — the tradeoff for lower spend. It does not guarantee uniform quality or remove tuning/caching concerns."
    },
    {
      id: "fund-opt-res-disc-reasoning",
      pattern: "resource-aware",
      also: ["reasoning"],
      kind: "discriminate",
      stem: "A dispatcher sends easy FAQs to a small model and hard escalations to a large one to save cost. A separate system runs tree-of-thought branching on a single hard math problem to improve accuracy. Which one is resource-aware optimization?",
      choices: [
        "The dispatcher choosing models by cost",
        "The tree-of-thought branching on one hard problem",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "Choosing a model tier by cost/difficulty is resource-aware optimization. Branching and pruning reasoning paths on one hard problem to improve accuracy is reasoning techniques, chosen for accuracy rather than cost control."
    },
    {
      id: "fund-opt-res-disc-eval",
      pattern: "resource-aware",
      also: ["evaluation"],
      kind: "discriminate",
      stem: "Is monitoring token spend per request and falling back to a cheaper model under budget pressure resource-aware optimization, or evaluation and monitoring?",
      choices: [
        "Resource-aware optimization",
        "Evaluation and monitoring",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "Falling back to a cheaper model under budget pressure is resource-aware optimization's real-time cost-control move. Evaluation and monitoring is about quality gates, golden tests, and drift detection over time, not per-request cost-based model selection."
    },
    {
      id: "fund-opt-reason-identify",
      pattern: "reasoning",
      kind: "identify",
      stem: "A method is chosen to fit the problem — chain-of-thought, tree-of-thought with branching and pruning, self-consistency, or adversarial debate — and candidates are scored against a rubric. Which pattern?",
      choices: [
        "Reasoning techniques",
        "Resource-aware optimization",
        "Guardrails / safety",
        "Evaluation and monitoring"
      ],
      answer: 0,
      explanation: "Picking a structured thinking method matched to problem difficulty is reasoning techniques. Resource-aware optimization picks models by cost, not thinking method. Guardrails screens for harm/policy. Evaluation sets up quality gates and monitors drift."
    },
    {
      id: "fund-opt-reason-when",
      pattern: "reasoning",
      kind: "when",
      stem: "Which scenario best fits an advanced reasoning technique?",
      choices: [
        "Multi-step logic, math, or strategic analysis where the model benefits from exploring or comparing multiple reasoning paths",
        "Routing simple versus hard requests by cost to save spend",
        "Screening input for PII or prompt injection",
        "Watching production accuracy and cost over time"
      ],
      answer: 0,
      explanation: "Reasoning techniques fit systematic, multi-step problems needing structured thought. Cost-based routing is resource-aware optimization; screening for PII/injection is guardrails; long-term monitoring is evaluation and monitoring."
    },
    {
      id: "fund-opt-reason-exception",
      pattern: "reasoning",
      kind: "exception",
      stem: "When is an advanced reasoning technique (like tree-of-thought or debate) the wrong tool?",
      choices: [
        "Everyday, simple tasks where a direct answer is already reliable — advanced techniques mainly add latency, tokens, and risk of overthinking",
        "Multi-step math requiring careful analysis",
        "A strategic decision needing systematic comparison of options",
        "A critical-analysis task with several plausible answers"
      ],
      answer: 0,
      explanation: "Reasoning techniques are advanced and best reserved for genuinely hard, multi-step problems; on simple tasks they mainly add cost, latency, and overthinking. The other options describe exactly where these techniques earn their cost."
    },
    {
      id: "fund-opt-reason-tradeoff",
      pattern: "reasoning",
      kind: "tradeoff",
      stem: "What is a documented cost of advanced reasoning techniques?",
      choices: [
        "Extra latency and token cost, risk of overthinking simple problems, context limits from many paths, and diminishing returns",
        "It guarantees a correct answer every time",
        "It has no token cost regardless of technique",
        "It performs identically well on trivial and hard problems alike"
      ],
      answer: 0,
      explanation: "Exploring multiple reasoning paths costs tokens and time, and returns shrink after enough branches — the tradeoff for higher accuracy on hard problems. It does not guarantee correctness or come free of cost."
    },
    {
      id: "fund-opt-reason-disc-res",
      pattern: "reasoning",
      also: ["resource-aware"],
      kind: "discriminate",
      stem: "System A branches into several candidate solution paths and prunes weak ones before picking the best. System B just picks a cheaper model for an easy request to save money. Which one is reasoning techniques?",
      choices: [
        "System A, branching and pruning candidate paths",
        "System B, picking a cheaper model",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "Branching and pruning candidate reasoning paths is reasoning techniques. Picking a cheaper model for an easy request is resource-aware optimization's cost-based decision, a different concern entirely."
    },
    {
      id: "fund-opt-reason-disc-guard",
      pattern: "reasoning",
      also: ["guardrails"],
      kind: "discriminate",
      stem: "Scoring several candidate arguments against a rubric to pick the strongest one is reasoning techniques, or guardrails/safety?",
      choices: [
        "Reasoning techniques",
        "Guardrails / safety",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "Scoring candidate reasoning paths for quality is reasoning techniques. Guardrails specifically screens for harm, policy violations, PII, or injection — not general reasoning quality."
    },
    {
      id: "fund-opt-guard-identify",
      pattern: "guardrails",
      kind: "identify",
      stem: "Inputs are checked for harm, PII, and injection and classified by risk; controls like blocking, constraining, sandboxing, or human review are applied; and outputs are moderated against policy, compliance, and brand before they go out. Which pattern?",
      choices: [
        "Guardrails / safety",
        "Reasoning techniques",
        "Resource-aware optimization",
        "Evaluation and monitoring"
      ],
      answer: 0,
      explanation: "Screening input/output for harm, PII, injection, and policy is guardrails/safety. Reasoning techniques pick a thinking method. Resource-aware optimization picks models by cost. Evaluation sets quality gates for accuracy/drift, not safety per se."
    },
    {
      id: "fund-opt-guard-when",
      pattern: "guardrails",
      kind: "when",
      stem: "Which scenario best fits guardrails/safety?",
      choices: [
        "A public-facing chatbot in a regulated industry where harmful content, PII leakage, or prompt injection are real risks",
        "Choosing a cheap versus expensive model purely for cost",
        "Branching reasoning paths for a hard math problem",
        "Watching for accuracy drift over several months in production"
      ],
      answer: 0,
      explanation: "Guardrails/safety fits public-facing, regulated, brand-sensitive surfaces. Cost-based model choice is resource-aware optimization; branching for accuracy is reasoning techniques; long-term drift tracking is evaluation and monitoring."
    },
    {
      id: "fund-opt-guard-exception",
      pattern: "guardrails",
      kind: "exception",
      stem: "When do heavy guardrail checks stop being worth their cost?",
      choices: [
        "A fully internal, non-sensitive tool with trusted operators and no public input surface, where the injection/PII/brand risk guardrails address barely applies",
        "A public chatbot in a regulated industry",
        "A system with an open text box as an attack surface",
        "A brand-sensitive, customer-facing product"
      ],
      answer: 0,
      explanation: "Guardrails earn their cost (latency, friction, false positives) when there's real exposure to harm, PII, injection, or brand risk. A fully internal tool with trusted operators and no public surface has little of that exposure. The other options are exactly where guardrails matter."
    },
    {
      id: "fund-opt-guard-tradeoff",
      pattern: "guardrails",
      kind: "tradeoff",
      stem: "What is a documented cost of guardrails/safety checks?",
      choices: [
        "False positives, added latency, user friction, ongoing policy maintenance, and processing cost, with some nuance still missed",
        "It guarantees zero false positives",
        "It removes the need for any policy updates over time",
        "It adds no latency to a response"
      ],
      answer: 0,
      explanation: "Screening inputs/outputs adds latency and friction, needs upkeep as policy evolves, and can still misfire or miss nuance — the tradeoff for fewer harmful or off-brand outputs. It does not guarantee perfection or zero overhead."
    },
    {
      id: "fund-opt-guard-disc-reason",
      pattern: "guardrails",
      also: ["reasoning"],
      kind: "discriminate",
      stem: "Blocking a request that contains a prompt-injection attempt is guardrails/safety, or reasoning techniques?",
      choices: [
        "Guardrails / safety",
        "Reasoning techniques",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "Screening and blocking malicious input like a prompt-injection attempt is guardrails/safety. Reasoning techniques is about choosing a thinking method for a legitimate task, not screening for malicious input."
    },
    {
      id: "fund-opt-guard-disc-eval",
      pattern: "guardrails",
      also: ["evaluation"],
      kind: "discriminate",
      stem: "Is moderating a generated response against brand and compliance policy before sending it guardrails/safety, or evaluation and monitoring?",
      choices: [
        "Guardrails / safety",
        "Evaluation and monitoring",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "Moderating a single response against policy before it ships is guardrails/safety. Evaluation and monitoring is the broader production practice of tracking quality, cost, and drift over time with golden tests, not a per-response policy check."
    },
    {
      id: "fund-opt-eval-identify",
      pattern: "evaluation",
      kind: "identify",
      stem: "Quality gates and golden tests are set before deploy; accuracy, SLAs, cost, and drift are watched continuously in production; and regressions trigger alerts and audits. Which pattern?",
      choices: [
        "Evaluation and monitoring",
        "Guardrails / safety",
        "Resource-aware optimization",
        "Reasoning techniques"
      ],
      answer: 0,
      explanation: "Golden tests plus continuous production monitoring for drift and regressions is evaluation and monitoring. Guardrails screens individual inputs/outputs for harm/policy. Resource-aware optimization picks models by cost. Reasoning techniques picks a thinking method for a single problem."
    },
    {
      id: "fund-opt-eval-when",
      pattern: "evaluation",
      kind: "when",
      stem: "Which scenario best fits evaluation and monitoring?",
      choices: [
        "A production system where you need to catch quality or cost regressions over time, not just check one output for safety",
        "Screening one message for PII before responding",
        "Picking a cheaper model for an easy request",
        "Branching reasoning paths on one hard question"
      ],
      answer: 0,
      explanation: "Evaluation and monitoring is about ongoing production quality/cost/drift tracking. Screening one message is guardrails; picking a cheaper model is resource-aware optimization; branching on one question is reasoning techniques."
    },
    {
      id: "fund-opt-eval-exception",
      pattern: "evaluation",
      kind: "exception",
      stem: "When is building full evaluation and monitoring infrastructure premature?",
      choices: [
        "A small prototype with no production traffic yet, where there's nothing running continuously to monitor for drift or regressions",
        "A production system needing reliability guarantees",
        "A system with compliance requirements",
        "A system where cost and performance need to be tracked over time"
      ],
      answer: 0,
      explanation: "Evaluation and monitoring pays off once something is running in production long enough to drift or regress. A prototype with no live traffic has nothing ongoing to watch yet. The other options describe exactly when this pattern is needed."
    },
    {
      id: "fund-opt-eval-tradeoff",
      pattern: "evaluation",
      kind: "tradeoff",
      stem: "What is a documented cost of evaluation and monitoring?",
      choices: [
        "Monitoring infrastructure and instrumentation overhead, alert fatigue, storage cost, and tests/rollbacks going stale over time",
        "It guarantees regressions never happen",
        "It removes the need for any golden tests",
        "It has no infrastructure cost"
      ],
      answer: 0,
      explanation: "Continuous monitoring requires real infrastructure and upkeep, and stale tests or noisy alerts are documented risks — the tradeoff for catching regressions early. It does not guarantee regression-free systems or come free."
    },
    {
      id: "fund-opt-eval-disc-guard",
      pattern: "evaluation",
      also: ["guardrails"],
      kind: "discriminate",
      stem: "Tracking whether accuracy on a golden test set has dropped this month is evaluation and monitoring, or guardrails/safety?",
      choices: [
        "Evaluation and monitoring",
        "Guardrails / safety",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "Tracking aggregate quality/drift over time against golden tests is evaluation and monitoring. Guardrails is about screening individual inputs/outputs for harm or policy violation, not tracking longer-term quality trends."
    },
    {
      id: "fund-opt-eval-disc-res",
      pattern: "evaluation",
      also: ["resource-aware"],
      kind: "discriminate",
      stem: "Alerting when average cost-per-request creeps up over a quarter is evaluation and monitoring, or resource-aware optimization?",
      choices: [
        "Evaluation and monitoring",
        "Resource-aware optimization",
        "Both equally",
        "Neither"
      ],
      answer: 0,
      explanation: "Detecting and alerting on a longer-term cost trend is evaluation and monitoring. Resource-aware optimization is the real-time act of routing a given request to a cheaper or pricier model, not the longer-term monitoring of that trend."
    },
    {
      id: "fund-opt-res-compose",
      pattern: "resource-aware",
      also: ["guardrails"],
      kind: "compose",
      stem: "A system routes easy requests to a cheap model, and before any response goes out, guardrails screen it for policy violations regardless of which model produced it. How should this be described?",
      choices: [
        "Resource-aware optimization decides which model handles the request; guardrails independently screens the output either way — the two compose rather than compete",
        "Only one pattern applies here, so this is just guardrails/safety",
        "Resource-aware optimization replaces the need for any output screening",
        "Guardrails replaces the need for any cost-based model routing"
      ],
      answer: 0,
      explanation: "Patterns combine: resource-aware optimization controls cost by model choice, and guardrails independently screens the output for safety — one doesn't substitute for the other."
    }
  ]
});
