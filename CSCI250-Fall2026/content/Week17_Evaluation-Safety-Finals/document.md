# Week 17 — LLM & GenAI Evaluation, Safety & Finals
**CSCI 250 · Introduction to Artificial Intelligence · Fall 2026**
*Week of December 14, 2026 · Online / Asynchronous*

---

## Learning objectives
By the end of this week you will be able to:
1. **Evaluate** an LLM/GenAI system with the right metric: exact-match, rubric scoring, and **LLM-as-judge**.
2. Build a small **eval harness** that runs test cases and reports a score you can track over time.
3. Identify and mitigate core **GenAI safety** risks: bias, hallucination, prompt injection, privacy/IP.
4. State the **limits** of these systems and apply **responsible-use** practices.
5. Finish strong: understand **Final Project** logistics and presentation expectations (**due Dec 19**).

> **Time budget:** ~10 hours — most of it on your **Final Project**. This is the final week.

---

## 1. Why evaluation matters
"It looked good when I tried it once" is not evaluation. GenAI outputs are **non-deterministic** and change with prompts, models, and data. Without measurement you cannot tell whether a change helped, whether a cheaper model is "good enough," or whether quality drifts over time. **Evaluation turns vibes into numbers.**

The loop: collect **test cases** (input + what good looks like) → run the system → **score** each output → aggregate → compare versions.

---

## 2. Picking a metric
Match the metric to the task.

### 2.1 Exact match / contains
For tasks with a single right answer (classification, extraction, math):
```python
def exact_match(pred: str, gold: str) -> bool:
    return pred.strip().lower() == gold.strip().lower()
```
Cheap and objective — but brittle for free-form text ("Paris." vs "The capital is Paris").

### 2.2 Rubric / structured checks
For open-ended outputs, score against explicit criteria you can check in code or by judge:
- Did it answer the question? Is it grounded in the source? Right format/length? No banned content?

### 2.3 LLM-as-judge
Use a strong model (**Claude** or **Gemini**) to grade outputs against a rubric. Great for nuance that exact-match misses; you must control for its quirks.
```python
import anthropic
client = anthropic.Anthropic()
judge_prompt = f"""You are a strict grader. Score 1-5 for correctness.
Question: {question}
Reference answer: {reference}
Model answer: {answer}
Reply with ONLY a number 1-5."""
score = client.messages.create(
    model="claude-sonnet-4-6", max_tokens=10, temperature=0,  # low temp = repeatable scores
    messages=[{"role": "user", "content": judge_prompt}],
).content[0].text
```
**Judge hygiene:** give a clear rubric, ask for structured output (a number or JSON), keep temperature low, and spot-check against human judgment. Critically, watch for three documented **judge biases**:
- **Position bias** — when comparing two answers, judges tend to favor whichever appears *first* (or sometimes second). Mitigate by **swapping the order** and averaging, or by scoring each answer independently against a rubric.
- **Verbosity bias** — judges over-reward *longer*, more elaborate answers even when a short one is correct. Mitigate by putting *conciseness* in the rubric and capping length.
- **Self-preference bias** — a model tends to rate outputs from **its own family** more favorably. Mitigate by using a **cross-family judge** (e.g., grade Claude outputs with Gemini, or vice-versa) or a human spot-check. This week's notebook runs **two judges (Claude and Gemini)** on the same answers precisely so you can see and counter self-preference.

---

## 3. Building a small eval harness
An eval harness is just: a **list of test cases**, a **scoring function**, and an **aggregate report**.

```python
test_cases = [
    {"input": "Capital of France?", "expected": "Paris"},
    {"input": "2 + 2?",            "expected": "4"},
]

def run_eval(system_fn, score_fn):
    results = []
    for tc in test_cases:
        out = system_fn(tc["input"])
        results.append(score_fn(out, tc["expected"]))
    return sum(results) / len(results)   # average score
```
Keep the harness in version control next to your project. Re-run it on **every prompt or model change** — that is how you ship improvements with confidence (and how you justify using a cheaper model). This week's notebook builds a fuller version with an **LLM-as-judge** scorer.

---

## 4. GenAI safety
Powerful tools fail in characteristic ways. Know them and design around them.

### 4.1 Hallucination
Models can state false things **confidently**. Mitigations: **ground** with RAG and cite sources, ask the model to say "I don't know," verify critical facts, and **evaluate** for groundedness.

### 4.2 Bias
Training data carries societal bias; outputs can be unfair across groups. Mitigations: test across diverse inputs, include fairness checks in your eval, keep a human in the loop for high-stakes decisions.

### 4.3 Prompt injection
Untrusted text (a web page, a user message, a retrieved document) can carry instructions that **hijack** your system ("ignore previous instructions and..."). Mitigations: separate **trusted instructions** from **untrusted data**, never auto-execute model output (no blind `eval`/shell), constrain tools and permissions, validate outputs before acting.

### 4.4 Privacy & IP
Don't send secrets/PII to a model you don't control; respect copyright and licenses on training and generated content; disclose AI-generated media. Review provider data-retention terms.

### 4.5 Limits & responsible use
LLMs predict plausible text — they are **not** databases, calculators, or judges of truth. Use them where mistakes are cheap or checkable, keep humans accountable, and **disclose** AI use (the same policy you've followed all semester).

---

## 4b. Responsible AI — beyond the technical failures
The risks in §4 are mostly *technical* failure modes. **Responsible AI** is the broader question of building systems that are fair, respectful of people, honest about what they are, and mindful of their effect on the world. As a builder you own these, not just the model maker.

- **Bias & fairness.** Models learn the patterns — and prejudices — in their training data, so outputs can systematically advantage or harm groups (by race, gender, dialect, disability, etc.). *Do:* test across **diverse, representative inputs**; measure error rates **per group**, not just overall; keep a **human in the loop** for consequential decisions (hiring, lending, medical, legal); document who could be harmed.
- **Privacy & PII.** Never send secrets or personal data to a model you don't control; **redact PII** (names, emails, IDs) on the way in, store only what you need, and check provider **data-retention** terms. Treat user data as a liability, not an asset.
- **Transparency & disclosure.** People should know when they're talking to or reading output from an AI. **Disclose** AI use, **label AI-generated media** (provenance/watermarking — Week 15), cite sources, and be honest about confidence and limitations rather than projecting false certainty.
- **Societal impact.** Zoom out from your app: GenAI shifts **jobs** and automates tasks; it can mass-produce **misinformation** and persuasive fakes at scale; and training/serving large models carries a real **environmental cost** (energy, water, compute). None of this means "don't build" — it means build deliberately: choose the **smallest sufficient model**, weigh who benefits and who bears the cost, and prefer uses where AI augments people rather than quietly replacing accountability.

**Bottom line:** *responsible* is a design requirement, not a disclaimer. Bake fairness checks, PII handling, disclosure, and a sober read of impact into the project — the same way you bake in evaluation.

---

## 5. Course wrap-up
You went from Python review → data & ML → neural nets → LLMs, prompting, RAG, agents/MCP, AI-assisted coding, multimodal, fine-tuning/ops, and now evaluation & safety. You can build, ground, serve, **and measure** a GenAI system — and reason about its risks. That is a complete, current AI engineering skill set.

---

## 6. Reading & videos
- Anthropic **"Building evals"** and **responsible use** docs (linked in Canvas).
- OWASP **"Top 10 for LLM Applications"** — especially **prompt injection** (linked in Canvas).
- Video: "LLM-as-a-judge — pitfalls and best practices" (linked in Canvas).
- Re-skim the **AI-use policy** in the syllabus before submitting your Final Project.

---

## 7. Final Project — logistics (Capstone **M5**, due **Friday, Dec 19, 11:59 PM PST**)
Your capstone applies the semester's stack to a problem you care about. **M5 is the finish line:** "My Assistant" becomes a polished, **deployed, documented** product. See `capstone/M5.md` for the full checklist and rubric.

> **🎯 Capstone M5 — ship it + present (see capstone/M5.md).** Deploy a public demo, write the README (banner, setup, scorecard, model reflection, limitations, AI-Use note), and record a **3-minute** screencast — due **Dec 19, 11:59 PM PST**.

**Deliverables**
1. **Deployed public demo** — a **Gradio app on Hugging Face Spaces** *or* a clearly-documented **Colab notebook** a grader can open and run **first try** on a **free tier** (no OpenAI). Keys via Secrets/env; **never hard-coded**.
2. **GitHub repo + README** — including a **"What you'll see when you run this"** banner, setup/run steps, your **eval scorecard** (baseline vs. final from M3/M4), a **Compare-models reflection** (Claude / Gemini / Ollama, with evidence), an honest **Limitations** section, and an **AI-Use note**.
3. **Eval results** — run your small eval harness from this week and report **baseline vs. final** score(s).
4. **Safety note** — which of §4's risks apply (hallucination, bias, prompt injection, privacy/IP) and how you handled them.
5. **3-minute screencast** — walk through the app and **one thing you'd improve**.

**Tips:** test the **first-try** experience in a fresh session; scope small and finish; ground with RAG to fight hallucination; include 5–10 eval cases; don't skip limitations; keep the screencast to **3 minutes**.

*No new assignment beyond the Final Project. Congratulations on finishing CSCI 250!*

---

## Key terms
**evaluation**, **test case**, **exact match**, **rubric**, **LLM-as-judge**, **position bias**, **verbosity bias**, **self-preference bias**, **eval harness**, **hallucination**, **bias**, **prompt injection**, **privacy/PII**, **IP/copyright**, **responsible AI**, **fairness**, **transparency/disclosure**, **societal impact**, **responsible use**, **groundedness**.
</content>
