window.QUIZ_BANKS = window.QUIZ_BANKS || [];
window.QUIZ_BANKS.push({
  id: "core",
  title: "Core patterns (1–5)",
  patterns: ["prompt-chaining", "routing", "parallelization", "reflection", "tool-use"],
  questions: [
    {
      id: "core-chain-identify-1",
      pattern: "prompt-chaining",
      kind: "identify",
      stem: "A messy spreadsheet needs labeled columns, then typed rows, then a validated load. Each station must check the previous output against a data contract before handing off. Which pattern is this?",
      choices: [
        "Prompt chaining — sequential steps with validated handoffs",
        "Routing — send the whole sheet to a specialist by intent",
        "Parallelization — workers each clean a different column at once",
        "Reflection — draft a load, then a critic scores it until it passes"
      ],
      answer: 0,
      explanation: "Chaining is an assembly line: execute, validate, hand off. Routing would classify the request, not stage a pipeline. Parallelization needs independent chunks, not a typed-rows step that depends on labeled columns. Reflection critiques one artifact in a loop rather than contracting between stages."
    },
    {
      id: "core-chain-when-1",
      pattern: "prompt-chaining",
      kind: "when",
      stem: "When is prompt chaining the right default rather than a single generation?",
      choices: [
        "The work is one short FAQ with a known answer",
        "You need to debug and retry at each stage of a multi-step transform",
        "Ten PDFs can be summarized with no shared order",
        "The model must call a live order-status API"
      ],
      answer: 1,
      explanation: "The video and docs put chaining on complex multi-step / ETL work where each step can fail independently. A one-shot FAQ does not need a chain (over-engineering). Independent PDFs are parallelization. A live API is tool use."
    },
    {
      id: "core-chain-when-2",
      pattern: "prompt-chaining",
      kind: "when",
      stem: "A teammate wants a 50-step LLM chain so every micro-check is a model call. What should you do?",
      choices: [
        "Keep all 50 steps — more validation always reduces hallucination",
        "Prefer a short chain (often 3–5) because long chains explode context and overthink",
        "Replace the chain with routing so each micro-check is a specialist agent",
        "Run the 50 steps in parallel so latency does not accumulate"
      ],
      answer: 1,
      explanation: "The transcript’s ‘magic number’ is often three to five; 50 steps invite context explosion and new hallucinations. Routing does not fix a sequential contract. Parallelizing dependent micro-checks breaks the handoff."
    },
    {
      id: "core-chain-tradeoff-1",
      pattern: "prompt-chaining",
      kind: "tradeoff",
      stem: "You forward every intermediate JSON payload into the next prompt through seven stages. What is the characteristic failure?",
      choices: [
        "Misrouting to the wrong specialist",
        "Context explosion and inherited early errors",
        "Workers finishing out of order",
        "The critic flattening the author’s voice"
      ],
      answer: 1,
      explanation: "Carrying full payloads down a chain burns tokens and lets step-1 mistakes poison step-7. Misrouting is a routing failure. Out-of-order merge is parallelization. Flattened voice is a reflection over-optimization risk."
    },
    {
      id: "core-chain-disc-1",
      pattern: "prompt-chaining",
      also: ["routing"],
      kind: "discriminate",
      stem: "Support mail always follows the same path: extract facts, draft, policy-check. Intents are not forked. Which pattern?",
      choices: [
        "Routing — classify billing vs shipping first",
        "Prompt chaining — the same sequential pipeline for every mail",
        "Parallelization — draft and policy-check at the same time",
        "Tool use — look up the order before anything else"
      ],
      answer: 1,
      explanation: "Same stages, every time, with validation between them is chaining. Routing forks by intent. Policy-check that needs the draft is not independent, so it is not parallelization. Tool use may appear inside a step but is not the overall pattern."
    },
    {
      id: "core-chain-disc-2",
      pattern: "prompt-chaining",
      also: ["parallelization"],
      kind: "discriminate",
      stem: "Stage B cannot start until stage A’s contract passes. Why is this not parallelization?",
      choices: [
        "Parallelization never uses more than one worker",
        "Parallelization needs independent chunks; a validated handoff is sequential",
        "Parallelization is only for web scraping",
        "If anything is validated, the pattern must be reflection"
      ],
      answer: 1,
      explanation: "ASCII for chaining is sequential execution plus validated handoffs. Parallelization splits work that does not wait on a sibling. Validation alone is not reflection (that is draft → critic → revise)."
    },
    {
      id: "core-chain-compose-1",
      pattern: "prompt-chaining",
      kind: "compose",
      stem: "You chain summarize → draft → policy check, and the last stage may call lookup_order. How do the patterns sit?",
      choices: [
        "Tool use replaces chaining because a tool appears",
        "Chaining is the backbone; tool use is a step inside one stage",
        "Routing must wrap the chain or the policy check is invalid",
        "Reflection is required whenever a policy check exists"
      ],
      answer: 1,
      explanation: "Production flows combine patterns. A chain can contain a tool call without becoming ‘just tool use.’ Routing is for intent forks, not for a fixed three-stage path. A policy check can be a contract, not a critic loop."
    },
    {
      id: "core-route-identify-1",
      pattern: "routing",
      kind: "identify",
      stem: "Incoming requests are classified and sent to tech, sales, or billing. If confidence is low, the system asks a clarifying question instead of guessing. Which pattern?",
      choices: [
        "Prompt chaining",
        "Routing",
        "Parallelization",
        "Reflection"
      ],
      answer: 1,
      explanation: "The video’s receptionist: analyze intent, send to a specialist, clarify when unsure. ASCII: confidence thresholds and a fallback. Chaining is one pipeline. Parallelization is concurrent chunks. Reflection is a quality loop on one draft."
    },
    {
      id: "core-route-when-1",
      pattern: "routing",
      kind: "when",
      stem: "A healthcare voice front door must send ‘hours?’ to FAQ, ‘chest pain’ to triage, and ‘reschedule’ to booking. Which pattern?",
      choices: [
        "Routing — multi-domain, specialized handlers",
        "Prompt chaining — hours, then triage, then booking for every caller",
        "Parallelization — run FAQ, triage, and booking on every call",
        "Tool use — any phone tree is just function calling"
      ],
      answer: 0,
      explanation: "Docs list healthcare triage and multi-domain systems under routing. Running every department on every call wastes work (not parallelization of independent chunks of one job). A fixed chain would delay emergencies. Tools may be used after the route."
    },
    {
      id: "core-route-when-2",
      pattern: "routing",
      kind: "when",
      stem: "The classifier says 4/10 confidence that an email is ‘billing.’ What does routing specifically tell you to do?",
      choices: [
        "Always pick the cheapest model and continue",
        "Ask clarifying questions (or quarantine) until confidence is usable",
        "Spawn three workers and majority-vote the intent",
        "Generate a draft reply and let a critic fix a wrong department"
      ],
      answer: 1,
      explanation: "Routing’s distinctive move is clarify / fallback when the operator is unsure. Voting is parallelization. A critic polishing a misrouted draft is the wrong layer. Cheap-vs-expensive models are not this bank’s routing story."
    },
    {
      id: "core-route-tradeoff-1",
      pattern: "routing",
      kind: "tradeoff",
      stem: "What is the characteristic risk of a router in front of many specialists?",
      choices: [
        "Context explosion from carrying every prior JSON",
        "Misrouting and a router that becomes a bottleneck",
        "API throttling from endless critic loops",
        "A successful-but-wrong tool call poisoning later math"
      ],
      answer: 1,
      explanation: "Docs: router complexity, misrouting, extra decision latency, edge cases that fit no category. Context explosion is chaining. Throttling from retries is reflection. Poisoned tool output is tool use."
    },
    {
      id: "core-route-disc-1",
      pattern: "routing",
      also: ["prompt-chaining"],
      kind: "discriminate",
      stem: "Inbox mail is billing, shipping, or cancel — different tools and policies per bucket. You classify first. Why not prompt chaining as the top-level pattern?",
      choices: [
        "Chaining cannot include a policy check",
        "Chaining is a sequential pipeline for one workflow, not a fork by intent",
        "Chaining is only for ETL spreadsheets",
        "Chaining forbids more than two steps"
      ],
      answer: 1,
      explanation: "Chaining hands off along one path. Routing chooses which path. A chain can still live inside a specialist after the route."
    },
    {
      id: "core-route-disc-2",
      pattern: "routing",
      also: ["parallelization"],
      kind: "discriminate",
      stem: "One email should go to exactly one department. A teammate wants to run billing, shipping, and cancel agents on every message and merge. Why is that the wrong pattern?",
      choices: [
        "Parallelization requires a critic",
        "The chunks are not independent parts of one job — they are mutually exclusive routes",
        "Parallelization cannot merge outputs",
        "Only tool use can touch departments"
      ],
      answer: 1,
      explanation: "Parallelization is independent concurrent work (ten chapters). Exclusive intents are routing. Merging three department answers on one ticket creates coordination mess the video warns about."
    },
    {
      id: "core-route-compose-1",
      pattern: "routing",
      kind: "compose",
      stem: "After a confident ‘billing’ route, the billing specialist may call payment tools. Which description is right?",
      choices: [
        "Tool use makes routing unnecessary",
        "Routing selects the specialist; tool use is how that specialist acts",
        "Reflection must approve every route",
        "Parallelization must call all tools then pick a department"
      ],
      answer: 1,
      explanation: "Routing often sits in front of tool use. Tools do not replace intent classification. Reflection is for polishing an artifact, not for choosing a department."
    },
    {
      id: "core-par-identify-1",
      pattern: "parallelization",
      kind: "identify",
      stem: "Ten people each read a different chapter at the same time; you normalize formats, merge, and keep provenance of who wrote which part. Which pattern?",
      choices: [
        "Prompt chaining",
        "Routing",
        "Parallelization",
        "Reflection"
      ],
      answer: 2,
      explanation: "That is the video’s parallelization analogy. Chaining would read chapter 2 only after chapter 1 validates. Routing would send the whole book to one specialist. Reflection would critique a single draft."
    },
    {
      id: "core-par-when-1",
      pattern: "parallelization",
      kind: "when",
      stem: "You must enrich 5,000 customer records from three independent APIs that do not depend on each other, and wall-clock time matters. Which pattern?",
      choices: [
        "Prompt chaining — API A, then B, then C per record, in series",
        "Routing — classify each record into one API",
        "Parallelization — concurrent workers, then merge",
        "Tool use — a single tool call replaces concurrency"
      ],
      answer: 2,
      explanation: "Independent, time-sensitive, multi-source work is parallelization (docs: API aggregation, enrichment). Serial chaining adds latency. Routing picks one path, not three independent fetches. Tool use is how a worker calls an API, not the split/merge pattern."
    },
    {
      id: "core-par-when-2",
      pattern: "parallelization",
      kind: "when",
      stem: "When should you refuse parallelization?",
      choices: [
        "Whenever more than one document exists",
        "When step B’s input is step A’s validated output",
        "When you care about provenance",
        "When web scraping is involved"
      ],
      answer: 1,
      explanation: "Dependent handoffs are chaining. Provenance is a parallelization feature, not a reason to skip it. Scraping is a listed fit when pages are independent."
    },
    {
      id: "core-par-tradeoff-1",
      pattern: "parallelization",
      kind: "tradeoff",
      stem: "Workers return apples, oranges, and pineapples. What extra work does parallelization force?",
      choices: [
        "Ask clarifying questions until one fruit remains",
        "Normalize to one format, merge, and keep which worker produced which part",
        "Run a critic until all fruits become the same essay",
        "Discover a pantry of fruit tools"
      ],
      answer: 1,
      explanation: "The transcript: normalize, merge, provenance so you can ‘talk to’ the failing worker. Clarifying is routing. A critic loop is reflection. Tool discovery is tool use."
    },
    {
      id: "core-par-disc-1",
      pattern: "parallelization",
      also: ["prompt-chaining"],
      kind: "discriminate",
      stem: "You can start worker C without waiting for worker A’s contract. That fact selects which pattern over chaining?",
      choices: [
        "Reflection",
        "Routing",
        "Parallelization",
        "Tool use"
      ],
      answer: 2,
      explanation: "Independence is the fork: chain if you must wait; parallelize if you must not. Routing still picks one path. Reflection iterates one artifact."
    },
    {
      id: "core-par-disc-2",
      pattern: "parallelization",
      also: ["routing"],
      kind: "discriminate",
      stem: "A CEO goal ‘cut churn 20%’ is split into independent subtasks (surveys, exit interviews, each with its own worker). Why is this not routing?",
      choices: [
        "Routing never uses more than two specialists",
        "Routing sends one request to one handler; here many workers run concurrent parts of one goal",
        "Routing forbids customer-service work",
        "If a CEO is involved the pattern must be reflection"
      ],
      answer: 1,
      explanation: "The video uses that churn split as parallel workers on one ambitious goal. Routing would classify a single incoming request to one department."
    },
    {
      id: "core-par-tradeoff-2",
      pattern: "parallelization",
      kind: "tradeoff",
      stem: "You scale to dozens of concurrent LLM workers. What cost shows up again and again in the docs?",
      choices: [
        "Rate limits, merge complexity, and multiplied spend",
        "A receptionist who asks too many questions",
        "Diminishing returns after the third critic pass",
        "Carrying step-1 JSON into step-7"
      ],
      answer: 0,
      explanation: "Parallelization cons: coordination, rate limits, harder debugging, cost/memory multiply. Clarifying questions are routing. Critic diminishing returns are reflection. JSON carry-over is chaining."
    },
    {
      id: "core-ref-identify-1",
      pattern: "reflection",
      kind: "identify",
      stem: "Generate a draft, a critic scores it against a rubric, revise, repeat until it meets the bar or a max retry count (the ‘school essay’ stop). Which pattern?",
      choices: [
        "Prompt chaining",
        "Routing",
        "Parallelization",
        "Reflection"
      ],
      answer: 3,
      explanation: "Draft → critic → revise with a hard stop is reflection. A chain validates handoffs between different stages, not the same artifact against a rubric. Routing classifies. Parallelization splits independent work."
    },
    {
      id: "core-ref-when-1",
      pattern: "reflection",
      kind: "when",
      stem: "Thousands of product descriptions must not be generic AI slop, but you also cannot loop forever. Which pattern?",
      choices: [
        "Routing each SKU to a random specialist",
        "Reflection with a quality rubric and a max iteration count",
        "Parallelization without a critic because speed is quality",
        "Tool use to fetch the weather for each SKU"
      ],
      answer: 1,
      explanation: "The video’s Amazon-style descriptions: use the model’s chaos, then constrain with critique and a cap. Routing does not polish voice. Parallelization can generate many drafts but merge is not a rubric. Weather tools are unrelated."
    },
    {
      id: "core-ref-when-2",
      pattern: "reflection",
      kind: "when",
      stem: "When should you skip reflection?",
      choices: [
        "Legal drafting with a compliance bar",
        "A deterministic lookup whose answer is already known",
        "Academic writing that needs citations checked",
        "Code generation that must pass tests"
      ],
      answer: 1,
      explanation: "Reflection costs latency and tokens. Use it when quality is non-negotiable. A known lookup does not need a critic loop (over-engineering, same family of ‘don’t chain 50 steps’)."
    },
    {
      id: "core-ref-tradeoff-1",
      pattern: "reflection",
      kind: "tradeoff",
      stem: "You reflect 12 times on every blog post. What does the pattern warn you about?",
      choices: [
        "Misrouting to the documentation agent",
        "Diminishing returns, extra cost, and over-optimization that flattens voice",
        "Workers finishing out of order",
        "A pantry with no permission to use the oven"
      ],
      answer: 1,
      explanation: "Docs/transcript: later iterations help little, APIs throttle, voice goes generic — hence a max count. The other options are routing, parallelization, and tool-use failure modes."
    },
    {
      id: "core-ref-disc-1",
      pattern: "reflection",
      also: ["prompt-chaining"],
      kind: "discriminate",
      stem: "How does reflection differ from prompt chaining?",
      choices: [
        "Reflection forbids more than one model call",
        "Chaining is a forward assembly line of different stages; reflection loops generate ↔ critique on the same artifact",
        "Chaining always uses a rubric; reflection never does",
        "They are the same pattern with two names"
      ],
      answer: 1,
      explanation: "A chain’s step 2 is a new job on step 1’s output. Reflection’s critic judges whether the draft is good enough and sends it back. Both may validate; the control flow differs."
    },
    {
      id: "core-ref-disc-2",
      pattern: "reflection",
      also: ["parallelization"],
      kind: "discriminate",
      stem: "You sample N drafts at once and pick a winner without a critic rubric. That is closer to which Core pattern than reflection?",
      choices: [
        "Routing",
        "Tool use",
        "Parallelization (sectioning/voting style concurrent workers)",
        "Prompt chaining"
      ],
      answer: 2,
      explanation: "Concurrent independent drafts plus a merge/vote is parallelization. Reflection is sequential critique against standards, not ‘ship whichever worker finished.’"
    },
    {
      id: "core-ref-compose-1",
      pattern: "reflection",
      kind: "compose",
      stem: "A chain writes a draft, then a critic loop polishes it before send. Which statement is true?",
      choices: [
        "You must delete the chain; only one pattern is allowed",
        "Chaining can produce the draft; reflection is the quality loop on that draft",
        "If a critic exists, routing is mandatory",
        "Tool use forbids critics"
      ],
      answer: 1,
      explanation: "Patterns stack. The chain is the pipeline; reflection is the quality layer. Routing is unrelated unless you also fork by intent."
    },
    {
      id: "core-tool-identify-1",
      pattern: "tool-use",
      kind: "identify",
      stem: "The model needs live facts. It discovers tools, checks it is allowed, calls one with parameters, parses the result, and falls back on failure. Analogy: chef, pantry, permission, recipe. Which pattern?",
      choices: [
        "Prompt chaining",
        "Routing",
        "Reflection",
        "Tool use"
      ],
      answer: 3,
      explanation: "That is tool use / function calling. Chaining sequences stages. Routing picks a specialist. Reflection critiques text."
    },
    {
      id: "core-tool-when-1",
      pattern: "tool-use",
      kind: "when",
      stem: "A support agent must not invent order dates; it should read them from a lookup. Which pattern is the primary move?",
      choices: [
        "Reflection until the invented date looks plausible",
        "Parallelization of three guessed dates",
        "Tool use — external data, not more prose",
        "Routing the user to a FAQ that also lacks the order"
      ],
      answer: 2,
      explanation: "When the model lacks ground truth, call a tool. Reflecting on a guess still fabricates. Parallel guesses are not facts. Routing to a page without the order fails the same way."
    },
    {
      id: "core-tool-when-2",
      pattern: "tool-use",
      kind: "when",
      stem: "When is tool use the wrong first move?",
      choices: [
        "You need a calculator for a precise total",
        "The answer is already fully determined by the user message and policy",
        "You must write a file the model cannot otherwise touch",
        "You need current inventory from a store system"
      ],
      answer: 1,
      explanation: "Tools add latency, credentials, and ‘successful but wrong’ risk. If no external action or data is required, do not fetch. The other options are classic tool-use fits."
    },
    {
      id: "core-tool-tradeoff-1",
      pattern: "tool-use",
      kind: "tradeoff",
      stem: "A tool returns HTTP 200 with the wrong order. The agent treats it as truth. The video’s school-math analogy is warning about what?",
      choices: [
        "Context explosion in a seven-step chain",
        "A successful-but-wrong call poisoning every later step",
        "Diminishing returns on the 12th critic pass",
        "Asking one clarifying question"
      ],
      answer: 1,
      explanation: "Wrong division in step 1 makes the whole solution wrong even if later arithmetic is valid. That is tool-use’s ‘passed but shouldn’t have’ failure, not chaining’s token pile-up or reflection’s extra loops."
    },
    {
      id: "core-tool-disc-1",
      pattern: "tool-use",
      also: ["routing"],
      kind: "discriminate",
      stem: "You always need lookup_order, whether the intent is billing or shipping. Is the top-level pattern routing?",
      choices: [
        "Yes — any tool implies a router",
        "No — routing forks handlers; a shared tool call is tool use (routing is extra only if specialists differ)",
        "No — it must be reflection",
        "Yes — tools are a kind of parallelization"
      ],
      answer: 1,
      explanation: "Routing is for different specialists/paths. One shared lookup is tool use. You add routing when billing vs shipping should not share tools or prompts."
    },
    {
      id: "core-tool-disc-2",
      pattern: "tool-use",
      also: ["prompt-chaining"],
      kind: "discriminate",
      stem: "Discover → permission → call → parse → maybe retry the same tool. Why is that not prompt chaining?",
      choices: [
        "Chaining never retries",
        "The loop is acting on the world (tools), not a pipeline of different generation stages with data contracts",
        "Chaining requires parallel workers",
        "If JSON appears, it is always chaining"
      ],
      answer: 1,
      explanation: "Tool use’s loop is select/call/parse/fallback. Chaining is sequential different tasks (extract, then transform, then write) with contracts. JSON is just a payload format."
    },
    {
      id: "core-tool-compose-1",
      pattern: "tool-use",
      kind: "compose",
      stem: "Router sends ‘cancel’ to a specialist; the specialist must call cancel APIs only after a permission check. What is the honest composition?",
      choices: [
        "Only routing exists; tools are an implementation detail you should ignore while learning patterns",
        "Routing chooses the path; tool use is the specialist’s external actions",
        "Reflection replaces both if quality matters",
        "Parallelization must call cancel on every email"
      ],
      answer: 1,
      explanation: "Learn both layers: classification vs acting on systems. Ignoring tools because they feel ‘implementation’ is how people invent order facts. Reflection and parallel cancel-all are the wrong shapes."
    }
  ]
});
