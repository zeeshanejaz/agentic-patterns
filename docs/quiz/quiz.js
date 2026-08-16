(function () {
  var PATTERN_LABELS = {
    "prompt-chaining": "Prompt chaining",
    routing: "Routing",
    parallelization: "Parallelization",
    reflection: "Reflection",
    "tool-use": "Tool use",
    planning: "Planning",
    "multi-agent": "Multi-agent collaboration",
    "memory-management": "Memory management",
    learning: "Learning and adaptation",
    mcp: "Model Context Protocol",
    "goal-setting": "Goal setting and monitoring",
    "exception-handling": "Exception handling and recovery",
    "human-in-the-loop": "Human-in-the-loop",
    "knowledge-retrieval": "Knowledge retrieval (RAG)",
    a2a: "Inter-agent communication",
    "resource-aware": "Resource-aware optimization",
    reasoning: "Reasoning techniques",
    guardrails: "Guardrails / safety",
    evaluation: "Evaluation and monitoring",
    prioritization: "Prioritization",
    exploration: "Exploration and discovery"
  };

  var banks = window.QUIZ_BANKS || [];
  var session = null;

  var pickerEl = document.getElementById("picker");
  var questionEl = document.getElementById("question");
  var summaryEl = document.getElementById("summary");

  function label(slug) {
    return PATTERN_LABELS[slug] || slug;
  }

  function shuffle(items) {
    var copy = items.slice();
    for (var i = copy.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = copy[i];
      copy[i] = copy[j];
      copy[j] = tmp;
    }
    return copy;
  }

  function show(which) {
    pickerEl.classList.toggle("hidden", which !== "picker");
    questionEl.classList.toggle("hidden", which !== "question");
    summaryEl.classList.toggle("hidden", which !== "summary");
  }

  function renderPicker() {
    var html = "<p class=\"meta\">Pick a related group.</p><div class=\"bank-list\">";
    for (var i = 0; i < banks.length; i++) {
      var b = banks[i];
      var names = (b.patterns || []).map(label).join(" · ");
      html +=
        "<button type=\"button\" class=\"bank-btn\" data-bank=\"" +
        escapeAttr(b.id) +
        "\">" +
        escapeHtml(b.title) +
        "<small>" +
        escapeHtml(names) +
        " · " +
        b.questions.length +
        " questions</small></button>";
    }
    html += "</div>";
    pickerEl.innerHTML = html;
    pickerEl.onclick = function (ev) {
      var btn = ev.target.closest("[data-bank]");
      if (!btn) return;
      startBank(btn.getAttribute("data-bank"));
    };
    show("picker");
  }

  function findBank(id) {
    for (var i = 0; i < banks.length; i++) {
      if (banks[i].id === id) return banks[i];
    }
    return null;
  }

  function startBank(id) {
    var bank = findBank(id);
    if (!bank) return;
    startSession(bank, bank.questions.slice());
  }

  function startSession(bank, questions) {
    session = {
      bank: bank,
      items: shuffle(questions),
      index: 0,
      selected: null,
      graded: false,
      results: []
    };
    renderQuestion();
  }

  function currentItem() {
    return session.items[session.index];
  }

  function renderQuestion() {
    var item = currentItem();
    var n = session.index + 1;
    var total = session.items.length;
    var html =
      "<p class=\"meta\">" +
      escapeHtml(session.bank.title) +
      " · " +
      n +
      " / " +
      total +
      "</p><p class=\"stem\">" +
      escapeHtml(item.stem) +
      "</p><div class=\"choices\">";
    for (var i = 0; i < item.choices.length; i++) {
      var cls = "choice";
      if (session.graded) {
        if (i === item.answer) cls += " correct";
        else if (i === session.selected) cls += " wrong";
      }
      html +=
        "<button type=\"button\" class=\"" +
        cls +
        "\" data-choice=\"" +
        i +
        "\"" +
        (session.graded ? " disabled" : "") +
        ">" +
        escapeHtml(item.choices[i]) +
        "</button>";
    }
    html += "</div>";
    if (session.graded) {
      var ok = session.selected === item.answer;
      html +=
        "<div class=\"feedback\"><p class=\"verdict " +
        (ok ? "ok" : "bad") +
        "\">" +
        (ok ? "Correct" : "Incorrect") +
        "</p><p>" +
        escapeHtml(item.explanation) +
        "</p><div class=\"actions\"><button type=\"button\" class=\"nav-btn primary\" id=\"next-btn\">" +
        (session.index + 1 === session.items.length ? "See summary" : "Next") +
        "</button></div></div>";
    }
    questionEl.innerHTML = html;
    questionEl.onclick = function (ev) {
      var choiceBtn = ev.target.closest("[data-choice]");
      if (choiceBtn && !session.graded) {
        grade(Number(choiceBtn.getAttribute("data-choice")));
        return;
      }
      if (ev.target.id === "next-btn") next();
    };
    show("question");
  }

  function grade(choiceIndex) {
    var item = currentItem();
    session.selected = choiceIndex;
    session.graded = true;
    session.results.push({
      item: item,
      selected: choiceIndex,
      correct: choiceIndex === item.answer
    });
    renderQuestion();
  }

  function next() {
    if (session.index + 1 >= session.items.length) {
      renderSummary();
      return;
    }
    session.index += 1;
    session.selected = null;
    session.graded = false;
    renderQuestion();
  }

  function renderSummary() {
    var results = session.results;
    var correct = 0;
    var byPattern = {};
    var missed = [];
    var i;
    for (i = 0; i < session.bank.patterns.length; i++) {
      byPattern[session.bank.patterns[i]] = { correct: 0, total: 0 };
    }
    for (i = 0; i < results.length; i++) {
      var r = results[i];
      var slug = r.item.pattern;
      if (!byPattern[slug]) byPattern[slug] = { correct: 0, total: 0 };
      byPattern[slug].total += 1;
      if (r.correct) {
        correct += 1;
        byPattern[slug].correct += 1;
      } else {
        missed.push(r);
      }
    }

    var html =
      "<p class=\"meta\">" +
      escapeHtml(session.bank.title) +
      "</p><p class=\"score\">" +
      correct +
      " / " +
      results.length +
      " correct</p><table><thead><tr><th>Pattern</th><th>Score</th></tr></thead><tbody>";
    for (i = 0; i < session.bank.patterns.length; i++) {
      var p = session.bank.patterns[i];
      var row = byPattern[p] || { correct: 0, total: 0 };
      html +=
        "<tr><td>" +
        escapeHtml(label(p)) +
        "</td><td>" +
        row.correct +
        " / " +
        row.total +
        "</td></tr>";
    }
    html += "</tbody></table>";
    if (missed.length) {
      html += "<p class=\"meta\">Missed</p><ul class=\"missed\">";
      for (i = 0; i < missed.length; i++) {
        var m = missed[i];
        html +=
          "<li>" +
          escapeHtml(m.item.stem) +
          "<br><span class=\"right\">Answer: " +
          escapeHtml(m.item.choices[m.item.answer]) +
          "</span></li>";
      }
      html += "</ul>";
    }
    html += "<div class=\"actions\">";
    if (missed.length) {
      html += "<button type=\"button\" class=\"nav-btn primary\" id=\"retry-btn\">Retry missed</button>";
    }
    html += "<button type=\"button\" class=\"nav-btn\" id=\"home-btn\">Pick another bank</button></div>";
    summaryEl.innerHTML = html;
    summaryEl.onclick = function (ev) {
      if (ev.target.id === "retry-btn") {
        var onlyMissed = missed.map(function (x) {
          return x.item;
        });
        startSession(session.bank, onlyMissed);
      } else if (ev.target.id === "home-btn") {
        renderPicker();
      }
    };
    show("summary");
  }

  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function escapeAttr(text) {
    return escapeHtml(text);
  }

  renderPicker();
})();
