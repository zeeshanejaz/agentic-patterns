window.QUIZ_BANKS = window.QUIZ_BANKS || [];
window.QUIZ_BANKS.push({
  id: "optimization",
  title: "Optimization patterns (16–19)",
  patterns: ["resource-aware", "reasoning", "guardrails", "evaluation"],
  questions: [
    {
      id: "opt-res-identify-1",
      pattern: "resource-aware",
      kind: "identify",
      stem: "Classify task complexity and send simple work to cheap/fast models and hard work to expensive ones; watch tokens, time, and spend; fall back to cache, shorter context, or a cheaper model. Walk / bus / taxi. Which pattern?",
      choices: [
        "Resource-aware optimization",
        "Reasoning techniques",
        "Guardrails / safety",
        "Evaluation and monitoring"
      ],
      answer: 0,
      explanation: "That is resource-aware routing by cost/difficulty. Reasoning picks CoT vs tree-of-thought. Guardrails check harm. Evaluation is quality gates in production."
    },
    {
      id: "opt-res-when-1",
      pattern: "resource-aware",
      kind: "when",
      stem: "High volume, tight budget, mixed easy FAQs and rare hard cases. Which pattern?",
      choices: [
        "Reasoning techniques on every FAQ",
        "Resource-aware optimization — right-size the model",
        "Guardrails instead of a model choice",
        "Evaluation with no runtime routing"
      ],
      answer: 1,
      explanation: "Docs: cost-sensitive, variable difficulty, budget caps. Tree-of-thought on every FAQ is the overthinking the reasoning pattern warns about."
    },
    {
      id: "opt-res-when-2",
      pattern: "resource-aware",
      kind: "when",
      stem: "When is resource-aware routing overkill?",
      choices: [
        "Millions of calls with a CFO watching unit cost",
        "A hobby script with one model and no bill that matters",
        "Multi-tenant fairness on a shared platform",
        "Dev vs prod model tiers"
      ],
      answer: 1,
      explanation: "The video: mom-and-pop rarely needs this; it is enterprise-scale cost control. Classification overhead is not free."
    },
    {
      id: "opt-res-tradeoff-1",
      pattern: "resource-aware",
      kind: "tradeoff",
      stem: "Users complain that ‘sometimes it is brilliant, sometimes it is dumb and fast.’ What did you trade?",
      choices: [
        "A missing input filter",
        "Quality and latency variance from sending different complexities to different models",
        "Lack of golden tests",
        "Too much chain-of-thought on purpose"
      ],
      answer: 1,
      explanation: "Cons: quality varies by model, uneven latency, threshold tuning. Guardrails and eval do not pick GPT-cheap vs GPT-heavy."
    },
    {
      id: "opt-res-disc-1",
      pattern: "resource-aware",
      also: ["reasoning"],
      kind: "discriminate",
      stem: "You pick a small model for ‘reset password’ and a large one for a contract. That is not tree-of-thought. Why?",
      choices: [
        "They are the same: both spend more tokens",
        "Resource-aware chooses how expensive the engine is; reasoning chooses a thinking method (CoT, ToT, debate) for a hard problem",
        "Resource-aware is a safety filter",
        "Reasoning is only for caching"
      ],
      answer: 1,
      explanation: "Cheap vs expensive vs step-by-step vs branch-and-prune. You can combine them; they are not synonyms."
    },
    {
      id: "opt-res-disc-2",
      pattern: "resource-aware",
      also: ["evaluation"],
      kind: "discriminate",
      stem: "A dashboard shows cost per request after deploy. Is that the resource-aware pattern by itself?",
      choices: [
        "Yes — any chart is resource-aware routing",
        "No — evaluation/monitoring watches production; resource-aware is the live classify-and-route (and cache) policy",
        "Yes — dashboards prune thought trees",
        "No — dashboards are guardrails"
      ],
      answer: 1,
      explanation: "Seeing cost is evaluation. Acting on complexity before the call is resource-aware. You want both."
    },
    {
      id: "opt-res-compose-1",
      pattern: "resource-aware",
      kind: "compose",
      stem: "Over budget mid-task you switch to a cheaper model and also enable prompt caching. Which pattern’s playbook is that?",
      choices: [
        "Guardrails — caching is a safety score",
        "Resource-aware optimization — cut context, cache, cheaper model",
        "Reasoning — always add more branches when over budget",
        "Evaluation — golden tests rewrite the prompt live"
      ],
      answer: 1,
      explanation: "Transcript fallbacks: trim context, cache, cheaper model. Adding ToT branches would spend more, not less."
    },
    {
      id: "opt-rea-identify-1",
      pattern: "reasoning",
      kind: "identify",
      stem: "Choose a method: chain-of-thought, tree-of-thought (branch, evaluate, prune), self-consistency, or adversarial debate; score candidates on a rubric. Which pattern?",
      choices: [
        "Resource-aware optimization",
        "Reasoning techniques",
        "Guardrails / safety",
        "Evaluation and monitoring"
      ],
      answer: 1,
      explanation: "Puzzle-solving with multiple strategies. Resource-aware is model tier. Eval is production QA. Guardrails are harm/PII."
    },
    {
      id: "opt-rea-when-1",
      pattern: "reasoning",
      kind: "when",
      stem: "The video’s default advice for everyday tasks is:",
      choices: [
        "Always run debate plus ToT plus self-consistency",
        "Skip it nine times out of ten — this is advanced and easy to overthink",
        "Use it instead of guardrails on open chat boxes",
        "Use it instead of any cheaper model"
      ],
      answer: 1,
      explanation: "Spoken: not cool for 90%+ of use cases; experimental unless you have bandwidth. Legal/medical-style meaty problems are the listed fits."
    },
    {
      id: "opt-rea-when-2",
      pattern: "reasoning",
      kind: "when",
      stem: "A differential diagnosis with several plausible paths might use tree-of-thought. A ‘what is 2+2’ widget should use what instead?",
      choices: [
        "More pruning of dead branches",
        "Not this pattern — extra reasoning latency is waste",
        "Adversarial debate until one agent concedes",
        "Self-consistency with 50 samples"
      ],
      answer: 1,
      explanation: "Overthinking simple work is a listed con. Save ToT for problems that branch."
    },
    {
      id: "opt-rea-tradeoff-1",
      pattern: "reasoning",
      kind: "tradeoff",
      stem: "You explore many paths and keep all of them in context. What explodes?",
      choices: [
        "Only the safety score",
        "Tokens, latency, and sometimes accuracy via overthinking",
        "The golden test suite size only",
        "Cache hit rate in a good way always"
      ],
      answer: 1,
      explanation: "Cons: token consumption, complexity, overthinking, cost of many paths, diminishing returns."
    },
    {
      id: "opt-rea-disc-1",
      pattern: "reasoning",
      also: ["resource-aware"],
      kind: "discriminate",
      stem: "GPT-quick vs GPT-hard for the same prompt is resource-aware. Generating three solution trees and pruning is which?",
      choices: [
        "Guardrails",
        "Reasoning techniques",
        "Evaluation",
        "Still only resource-aware"
      ],
      answer: 1,
      explanation: "Model SKU vs search method. A ‘hard thinking’ product mode may mix both; the pattern names stay distinct."
    },
    {
      id: "opt-rea-disc-2",
      pattern: "reasoning",
      also: ["evaluation"],
      kind: "discriminate",
      stem: "Scoring candidate thoughts against a rubric *inside one problem* is reasoning. Scoring the deployed system against golden tests over weeks is which?",
      choices: [
        "The same pattern",
        "Evaluation and monitoring",
        "Guardrails",
        "Resource-aware caching"
      ],
      answer: 1,
      explanation: "In-the-loop method selection vs production quality infrastructure. The video: evaluation is factory QC, not a ToT."
    },
    {
      id: "opt-rea-compose-1",
      pattern: "reasoning",
      kind: "compose",
      stem: "Only the ‘complex’ bucket runs self-consistency; simple bucket is a cheap model with no CoT. What did you combine?",
      choices: [
        "Guardrails and nothing else",
        "Resource-aware routing plus reasoning only where it pays",
        "Evaluation deleting the cheap path",
        "ToT on every request by policy"
      ],
      answer: 1,
      explanation: "That combination is how the two Optimization patterns cooperate instead of fighting the budget."
    },
    {
      id: "opt-grd-identify-1",
      pattern: "guardrails",
      kind: "identify",
      stem: "Airport security: sanitize input, detect PII and injection, classify risk, block/constrain/sandbox/human-review, then moderate outputs against policy and brand. Catch issues upstream. Which pattern?",
      choices: [
        "Resource-aware optimization",
        "Reasoning techniques",
        "Guardrails / safety",
        "Evaluation and monitoring"
      ],
      answer: 2,
      explanation: "Top-of-funnel controls. Evaluation is ongoing QC after deploy. Reasoning is how to think. Resource-aware is how expensive to think."
    },
    {
      id: "opt-grd-when-1",
      pattern: "guardrails",
      kind: "when",
      stem: "A public chatbot with an open text box is, in the video, a common attack surface. What should you add?",
      choices: [
        "Only more tree-of-thought so jailbreaks get pruned",
        "Guardrails — input/output checks; consider constrained journeys if the box is too dangerous",
        "Cheaper models so attacks cost less",
        "Golden tests instead of any input filter"
      ],
      answer: 1,
      explanation: "Injection, PII, harm. ToT does not replace a filter. Pre-prompted click journeys are the spoken mitigation when open chat is too risky."
    },
    {
      id: "opt-grd-when-2",
      pattern: "guardrails",
      kind: "when",
      stem: "When are guardrails still required even if evaluation looks green?",
      choices: [
        "Never — green eval means no attacks",
        "Public or regulated surfaces: eval does not block the next injected prompt",
        "Only when using expensive models",
        "Only when using CoT"
      ],
      answer: 1,
      explanation: "Eval watches quality/cost/drift. Guardrails intercept harm. Both exist in Optimization because they are different jobs."
    },
    {
      id: "opt-grd-tradeoff-1",
      pattern: "guardrails",
      kind: "tradeoff",
      stem: "The filter blocks a legitimate medical question. What con is that?",
      choices: [
        "Diminishing returns on the 12th ToT branch",
        "False positives and user friction vs the need for safety",
        "Cache coherency",
        "Alert fatigue from golden tests"
      ],
      answer: 1,
      explanation: "Docs: false positives, latency, frustration, missed nuance. Balance friction with safety — safety still takes precedence in the video, but the tradeoff is real."
    },
    {
      id: "opt-grd-disc-1",
      pattern: "guardrails",
      also: ["evaluation"],
      kind: "discriminate",
      stem: "A safety score on *this* request vs a weekly harm-rate dashboard. Which is which?",
      choices: [
        "Both are resource-aware",
        "This-request controls are guardrails; the dashboard is evaluation/monitoring",
        "Both are reasoning",
        "Dashboards replace input sanitization"
      ],
      answer: 1,
      explanation: "Inline policy vs system health over time. You still need the inline check."
    },
    {
      id: "opt-grd-disc-2",
      pattern: "guardrails",
      also: ["reasoning"],
      kind: "discriminate",
      stem: "A debate between proponent and opponent agents is reasoning. Scanning the user text for injection before any debate is which?",
      choices: [
        "Resource-aware optimization",
        "Guardrails / safety",
        "Evaluation and monitoring",
        "Still reasoning — debate is safety"
      ],
      answer: 1,
      explanation: "Do not start a parliament on an unsanitized prompt. Filter first."
    },
    {
      id: "opt-grd-compose-1",
      pattern: "guardrails",
      kind: "compose",
      stem: "High-risk input is sandboxed and also sent to a reviewer; later you alert if jailbreak rate drifts. Stack?",
      choices: [
        "Guardrails on the request; evaluation to watch the rate; (HITL is outside this bank but fits the reviewer)",
        "Only cheaper models",
        "Only ToT",
        "Evaluation forbids sandboxing"
      ],
      answer: 0,
      explanation: "Inline controls plus production monitoring. Model tier does not sanitize."
    },
    {
      id: "opt-eval-identify-1",
      pattern: "evaluation",
      kind: "identify",
      stem: "Set quality gates and golden tests before deploy. Continuously watch accuracy, SLAs, cost, and drift; alert and audit on regressions. Factory QC. Which pattern?",
      choices: [
        "Resource-aware optimization",
        "Reasoning techniques",
        "Guardrails / safety",
        "Evaluation and monitoring"
      ],
      answer: 3,
      explanation: "Infrastructure, not something a model invents for itself (video). Guardrails are per-request filters. This is the plant’s QC line."
    },
    {
      id: "opt-eval-when-1",
      pattern: "evaluation",
      kind: "when",
      stem: "The same prompt’s answers get worse over months (drift). Which pattern is supposed to catch that?",
      choices: [
        "Resource-aware caching",
        "Evaluation and monitoring — golden tests, drift, regression vs the mean",
        "Tree-of-thought on one user question",
        "A single PII regex"
      ],
      answer: 1,
      explanation: "Spoken definition of drift. ToT will not notice last quarter’s quality. A regex is a guardrail, not a trend."
    },
    {
      id: "opt-eval-when-2",
      pattern: "evaluation",
      kind: "when",
      stem: "When is a huge eval harness the wrong first spend?",
      choices: [
        "A regulated healthcare deployment",
        "A weekend prototype with no users",
        "A multi-tenant SaaS in production",
        "A trading desk with an SLA"
      ],
      answer: 1,
      explanation: "The video: ask whether the case deserves this robustness. Prototypes can wait; production/regulated should not."
    },
    {
      id: "opt-eval-tradeoff-1",
      pattern: "evaluation",
      kind: "tradeoff",
      stem: "You alert on every tiny metric blip and keep stale tests. What do you get?",
      choices: [
        "Free ToT",
        "Alert fatigue, instrumentation cost, and false rollbacks",
        "Automatic jailbreak blocking",
        "Cheaper models"
      ],
      answer: 1,
      explanation: "Docs cons: overhead, complexity, alert fatigue, stale tests, false positives. Guardrails block jailbreaks; eval does not by itself."
    },
    {
      id: "opt-eval-disc-1",
      pattern: "evaluation",
      also: ["guardrails"],
      kind: "discriminate",
      stem: "A golden test fails in CI after a prompt change. That is evaluation. Blocking a live SQL-injection string is which?",
      choices: [
        "Resource-aware optimization",
        "Guardrails / safety",
        "Reasoning techniques",
        "Still evaluation because a test exists somewhere"
      ],
      answer: 1,
      explanation: "CI/prod metrics vs live input defense. A unit test is not a WAF."
    },
    {
      id: "opt-eval-disc-2",
      pattern: "evaluation",
      also: ["resource-aware"],
      kind: "discriminate",
      stem: "Eval tells you cost per ticket went up. Resource-aware’s job after that insight is:",
      choices: [
        "Write more golden tests only",
        "Change routing thresholds, cache, or model mix so the next tickets are cheaper",
        "Add a debate agent",
        "Redact PII"
      ],
      answer: 1,
      explanation: "Monitoring informs; resource-aware acts on complexity/budget. PII is guardrails. Debate is reasoning."
    },
    {
      id: "opt-eval-compose-1",
      pattern: "evaluation",
      kind: "compose",
      stem: "Golden tests, live drift alerts, and a harm filter on every input. Which trio?",
      choices: [
        "Evaluation + guardrails (resource-aware optional for cost)",
        "Reasoning only",
        "ToT only",
        "Caching only"
      ],
      answer: 0,
      explanation: "QC + safety layer, with optional cost routing. That is the Optimization group working as a set."
    }
  ]
});
